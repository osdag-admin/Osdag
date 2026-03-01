"""
Author : Nishi Kant Mandal
"""
import gc
import threading
from typing import Optional

# Expose a getter for the singleton
_cleanup_coordinator_instance = None

def get_cleanup_coordinator():
    global _cleanup_coordinator_instance
    if _cleanup_coordinator_instance is None:
        _cleanup_coordinator_instance = CleanupCoordinator()
    return _cleanup_coordinator_instance

class CleanupCoordinator:
    """Centralized cleanup orchestrator for OpenCASCADE memory management.

    Ensures:
    1. Single entry point for all cleanup scenarios.
    2. Consistent ordering of cleanup steps.
    3. Concurrency control (no overlapping cleanups).
    4. GC management (disable during critical sections).
    5. Signal blocking to avoid recursive cleanup.
    """

    _instance: Optional['CleanupCoordinator'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'CleanupCoordinator':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._cleanup_in_progress = False
        self._initialized = True

    def _execute_cleanup(self, cad_widget, display, clear_output: bool = False, clear_logs: bool = False,
                         output_dock=None, logs_dock=None, is_final: bool = False) -> bool:
        """Core cleanup execution with proper ordering.

        Steps:
        0. Acquire AISContextLock to prevent race conditions
        1. Block signals
        2. Disable GC
        3. Clear Python references (widget-specific cleanup)
        4. Remove from OCC context
        5. OCCMemoryManager.safe_cleanup()
        6. Repaint display
        7. Enable GC
        8. Unblock signals
        9. Release AISContextLock
        """
        with self._lock:
            if self._cleanup_in_progress:
                print("[CleanupCoordinator] Cleanup already in progress")
                return False
            self._cleanup_in_progress = True

        gc_was_enabled = gc.isenabled()
        
        # Import AISContextLock for thread-safe context operations
        try:
            from osdag_gui.OS_safety_protocols import AISContextLock
            ais_lock_available = True
        except ImportError:
            ais_lock_available = False
            
        try:
            # Step 0: Acquire AIS context lock
            if ais_lock_available:
                AISContextLock.block_processEvents()
                
            # Step 1: Block signals
            if cad_widget:
                cad_widget.blockSignals(True)

            # Step 2: Disable GC
            gc.disable()

            # Step 3: Clear Python references via widget's own cleanup method if present
            if cad_widget and hasattr(cad_widget, 'cleanup_for_new_model'):
                cad_widget.cleanup_for_new_model()

            # Step 4: Remove from OCC context (protected by AISContextLock)
            if display:
                try:
                    display.EraseAll()
                except Exception as e:
                    print(f"[CleanupCoordinator] EraseAll error: {e}")

            # Step 5: OCCMemoryManager safe cleanup
            try:
                from osdag_gui.OS_safety_protocols import get_occ_memory_manager
                manager = get_occ_memory_manager()
                widget_id = id(cad_widget)
                context = display.Context if display else None
                if is_final:
                    manager.unregister_widget(widget_id)
                else:
                    manager.safe_cleanup(widget_id, context)
            except Exception as e:
                print(f"[CleanupCoordinator] Memory manager error: {e}")

            # Step 6: Repaint display
            if display:
                try:
                    display.Repaint()
                except Exception:
                    pass

            # Step 7: Clear output/logs if requested
            if clear_output and output_dock:
                self._clear_output_dock(output_dock)
            if clear_logs and logs_dock:
                self._clear_logs_dock(logs_dock)

            return True
        except Exception as e:
            print(f"[CleanupCoordinator] Cleanup error: {e}")
            return False
        finally:
            # Step 8: Enable GC if it was originally enabled
            if gc_was_enabled:
                gc.enable()
            # Unblock signals
            if cad_widget:
                cad_widget.blockSignals(False)
            # Step 9: Release AISContextLock
            if ais_lock_available:
                AISContextLock.unblock_processEvents()
            with self._lock:
                self._cleanup_in_progress = False

    # Public API methods for each scenario
    def cleanup_for_redesign(self, template_page) -> bool:
        """Called when user unlocks input dock and wants to redesign."""
        return self._execute_cleanup(
            cad_widget=template_page.cad_widget,
            display=template_page.display,
            clear_output=True,
            clear_logs=True,
            output_dock=getattr(template_page, 'output_dock', None),
            logs_dock=getattr(template_page, 'logs_dock', None)
        )

    def cleanup_for_new_design(self, cad_widget, display) -> bool:
        """Called before displaying a new design."""
        return self._execute_cleanup(
            cad_widget=cad_widget,
            display=display,
            clear_output=False,
            clear_logs=False
        )

    def cleanup_for_tab_close(self, template_page) -> bool:
        """Called when closing a module tab."""
        # Prevent double cleanup
        if getattr(template_page, '_cleanup_done', False):
            return True
        
        # CRITICAL: Clean PSO resources FIRST to avoid stale widget references
        # The PSO manager may hold references to widgets (e.g., _hidden_cad_widget)
        # that must be cleared before we erase OCC objects, otherwise we get
        # "free(): corrupted unsorted chunks" heap corruption on deleteLater()
        if hasattr(template_page, '_pso_manager') and template_page._pso_manager:
            try:
                template_page._pso_manager.cleanup()
                template_page._pso_manager = None
            except Exception as e:
                print(f"[CleanupCoordinator] PSO cleanup error: {e}")
            
        result = self._execute_cleanup(
            cad_widget=template_page.cad_widget,
            display=template_page.display,
            clear_output=True,
            clear_logs=True,
            output_dock=getattr(template_page, 'output_dock', None),
            logs_dock=getattr(template_page, 'logs_dock', None),
            is_final=True
        )
        
        # Mark as cleaned up to prevent reentry (e.g. from closeEvent)
        template_page._cleanup_done = True
        return result

    def cleanup_for_app_exit(self, main_window) -> bool:
        """Called before application exit to clean all tabs."""
        # Iterate over all tabs and clean them
        for i in range(len(main_window.tab_widget_content) - 1, -1, -1):
            template = main_window._get_template_instance(i)
            if hasattr(template, 'cad_widget'):
                self.cleanup_for_tab_close(template)
        return True

    # Helper methods for clearing docks (implementation can be simple placeholders)
    def _clear_output_dock(self, dock):
        try:
            dock.clear_output_fields()
        except Exception as e:
            print(f"[CleanupCoordinator] clear_output_dock error: {e}")

    def _clear_logs_dock(self, dock):
        try:
            dock.clear_logs()
        except Exception as e:
            print(f"[CleanupCoordinator] clear_logs_dock error: {e}")
