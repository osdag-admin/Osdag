"""
OCC Memory Manager - Centralized memory management for OpenCASCADE objects.

This module provides a singleton manager that:
1. Tracks ALL OCC objects (shapes, AIS objects, contexts) to prevent premature GC
2. Provides thread-safe cleanup operations with proper ordering
3. Ensures Python GC doesn't free C++ objects while OCC/OpenGL are still using them
4. Provides AISContextLock for safe context synchronization

The root cause of heap corruption:
- Python garbage collector frees OCC wrapper objects
- But OpenCASCADE's C++ layer still holds references to underlying memory
- This causes use-after-free and heap corruption

Solution:
- Register all OCC objects with this manager
- Objects are only freed when explicitly released via safe_cleanup()
- Cleanup follows proper order: context → AIS objects → shapes
- Use AISContextLock when modifying AIS context during processEvents

Author: Nishi Kant Mandal
"""

import gc
import threading
from typing import Dict, List, Any, Optional
from weakref import WeakValueDictionary


class AISContextLock:
    """
    Thread-safe lock for AIS context operations.
    
    Use this lock when:
    1. Adding/removing shapes from AIS context
    2. Calling processEvents() during CAD operations
    3. Swapping CAD widgets in/out
    
    Example:
        with AISContextLock.acquire():
            context.Display(ais_shape, True)
    """
    
    _lock = threading.RLock()  # Reentrant lock allows same thread to acquire multiple times
    _holder_thread: Optional[int] = None
    _operation_in_progress = False
    _processEvents_blocked = False
    
    @classmethod
    def acquire(cls, blocking: bool = True, timeout: float = -1) -> bool:
        """
        Acquire the AIS context lock.
        
        Args:
            blocking: If True, wait for lock. If False, return immediately.
            timeout: Maximum time to wait (-1 = infinite)
            
        Returns:
            True if lock was acquired, False otherwise.
        """
        result = cls._lock.acquire(blocking=blocking, timeout=timeout if timeout > 0 else -1)
        if result:
            cls._holder_thread = threading.current_thread().ident
            cls._operation_in_progress = True
        return result
    
    @classmethod
    def release(cls):
        """Release the AIS context lock."""
        cls._operation_in_progress = False
        cls._holder_thread = None
        try:
            cls._lock.release()
        except RuntimeError:
            pass  # Lock not held
    
    @classmethod
    def is_operation_in_progress(cls) -> bool:
        """Check if an AIS operation is currently in progress."""
        return cls._operation_in_progress
    
    @classmethod
    def is_held_by_current_thread(cls) -> bool:
        """Check if current thread holds the lock."""
        return cls._holder_thread == threading.current_thread().ident
    
    @classmethod
    def block_processEvents(cls):
        """Block processEvents() calls during critical sections."""
        cls._processEvents_blocked = True
    
    @classmethod
    def unblock_processEvents(cls):
        """Unblock processEvents() calls."""
        cls._processEvents_blocked = False
    
    @classmethod
    def is_processEvents_blocked(cls) -> bool:
        """Check if processEvents() should be skipped."""
        return cls._processEvents_blocked or cls._operation_in_progress
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False


def safe_processEvents():
    """
    Safe wrapper for QApplication.processEvents().
    
    Only calls processEvents() if:
    1. No AIS context operation is in progress
    2. processEvents is not blocked
    
    Use this instead of QApplication.processEvents() during CAD operations.
    """
    if AISContextLock.is_processEvents_blocked():
        return  # Skip - operation in progress
    
    try:
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
    except Exception:
        pass


def clean_shape(shape):
    """
    Clean cached data from a TopoDS_Shape to free memory.
    
    This removes:
    - Triangulation data
    - Polygon curves
    - Face normals cache
    
    Call this after boolean operations to prevent memory bloat.
    
    Args:
        shape: TopoDS_Shape object
    """
    try:
        from OCC.Core.BRepTools import BRepTools
        BRepTools.Clean_s(shape)
    except Exception:
        pass  # BRepTools not available or shape is None


def clean_shapes(*shapes):
    """
    Clean cached data from multiple shapes.
    
    Args:
        *shapes: Variable number of TopoDS_Shape objects or containers
    """
    def _clean_recursive(obj):
        if obj is None:
            return
        if isinstance(obj, dict):
            for v in obj.values():
                _clean_recursive(v)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                _clean_recursive(item)
        else:
            clean_shape(obj)
    
    for shape in shapes:
        _clean_recursive(shape)


class OCCMemoryManager:
    """
    Singleton manager for OCC object lifecycle.
    
    Prevents heap corruption by:
    1. Holding strong references to OCC objects until explicit cleanup
    2. Disabling GC during cleanup operations
    3. Ensuring proper cleanup order (context first, then AIS, then shapes)
    4. Using AISContextLock for thread-safe context operations
    """
    
    _instance: Optional['OCCMemoryManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'OCCMemoryManager':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._registry: Dict[int, Dict[str, List[Any]]] = {}
        self._contexts: Dict[int, Any] = {}
        self._cleanup_in_progress: Dict[int, bool] = {}
        self._gc_disabled = False
        self._lock = threading.Lock()
        self._initialized = True
        
        print("[OCCMemoryManager] Initialized")
    
    @classmethod
    def get_instance(cls) -> 'OCCMemoryManager':
        """Get the singleton instance."""
        return cls()
    
    def register_widget(self, widget_id: int, context: Any = None):
        """
        Register a CAD widget for memory tracking.
        
        Args:
            widget_id: Unique identifier for the widget (use id(widget))
            context: Optional AIS_InteractiveContext for the widget
        """
        with self._lock:
            if widget_id not in self._registry:
                self._registry[widget_id] = {
                    'shapes': [],
                    'ais_objects': [],
                    'edge_ais_objects': [],
                    'other': []
                }
                self._cleanup_in_progress[widget_id] = False
            
            if context is not None:
                self._contexts[widget_id] = context
    
    def register_shape(self, widget_id: int, shape: Any):
        """
        Register a TopoDS_Shape to prevent garbage collection.
        
        Args:
            widget_id: Widget that owns this shape
            shape: The TopoDS_Shape object
        """
        with self._lock:
            if widget_id not in self._registry:
                self.register_widget(widget_id)
            self._registry[widget_id]['shapes'].append(shape)
    
    def register_ais_object(self, widget_id: int, ais_obj: Any, is_edge: bool = False):
        """
        Register an AIS object to prevent garbage collection.
        
        Args:
            widget_id: Widget that owns this AIS object
            ais_obj: The AIS_Shape or similar object
            is_edge: If True, store in edge_ais_objects list
        """
        with self._lock:
            if widget_id not in self._registry:
                self.register_widget(widget_id)
            
            if is_edge:
                self._registry[widget_id]['edge_ais_objects'].append(ais_obj)
            else:
                self._registry[widget_id]['ais_objects'].append(ais_obj)
    
    def register_object(self, widget_id: int, obj: Any):
        """
        Register any OCC object to prevent garbage collection.
        
        Args:
            widget_id: Widget that owns this object
            obj: Any OCC object
        """
        with self._lock:
            if widget_id not in self._registry:
                self.register_widget(widget_id)
            self._registry[widget_id]['other'].append(obj)
    
    def is_cleanup_in_progress(self, widget_id: int) -> bool:
        """Check if cleanup is in progress for a widget."""
        with self._lock:
            return self._cleanup_in_progress.get(widget_id, False)
    
    def safe_cleanup(self, widget_id: int, context: Any = None) -> bool:
        """
        Safely cleanup all OCC objects for a widget.
        
        This follows the proper order:
        1. Acquire AIS context lock
        2. Disable GC
        3. Block processEvents
        4. Remove all from OCC context
        5. Clean shape caches (BRepTools.Clean)
        6. Clear AIS objects (edge first, then main)
        7. Clear shapes
        8. Unblock processEvents
        9. Re-enable GC
        
        Args:
            widget_id: Widget to cleanup
            context: Optional context override
            
        Returns:
            True if cleanup was performed, False if skipped (already in progress)
        """
        with self._lock:
            # Skip if widget was already unregistered (e.g., tab closed)
            # This prevents use-after-free on already-cleaned widgets
            if widget_id not in self._registry:
                return False
            
            if self._cleanup_in_progress.get(widget_id, False):
                print(f"[OCCMemoryManager] Cleanup already in progress for widget {widget_id}")
                return False
            self._cleanup_in_progress[widget_id] = True
        
        try:
            # Step 0: Acquire context lock and block processEvents
            with AISContextLock():
                AISContextLock.block_processEvents()
                
                try:
                    # Step 1: Disable garbage collection during entire cleanup
                    gc_was_enabled = gc.isenabled()
                    gc.disable()
                    
                    # Get context
                    ctx = context or self._contexts.get(widget_id)
                    
                    # Step 2: Remove all from OCC context first
                    if ctx is not None:
                        try:
                            ctx.RemoveAll(False)  # False = don't update view immediately
                        except Exception as e:
                            print(f"[OCCMemoryManager] Error in RemoveAll: {e}")
                    
                    # Step 3: Clean shape caches before clearing references
                    with self._lock:
                        if widget_id in self._registry:
                            shapes = self._registry[widget_id].get('shapes', [])
                            clean_shapes(shapes)
                    
                    # Step 4: Clear all references in correct order
                    with self._lock:
                        if widget_id in self._registry:
                            # Clear in reverse order of dependency
                            self._registry[widget_id]['edge_ais_objects'].clear()
                            self._registry[widget_id]['ais_objects'].clear()
                            self._registry[widget_id]['other'].clear()
                            self._registry[widget_id]['shapes'].clear()
                    
                    # NOTE: DO NOT call gc.collect() here!
                    # It forces Python to destroy OCC wrappers in arbitrary order,
                    # but OpenCascade's Handle system requires View→Context→Driver order.
                    # Let natural reference counting handle cleanup.
                    
                    print(f"[OCCMemoryManager] Cleanup complete for widget {widget_id}")
                    return True
                    
                finally:
                    # Re-enable GC if it was enabled before
                    if gc_was_enabled:
                        gc.enable()
                    AISContextLock.unblock_processEvents()
            
        except Exception as e:
            print(f"[OCCMemoryManager] Error during cleanup: {e}")
            return False
            
        finally:
            with self._lock:
                self._cleanup_in_progress[widget_id] = False
    
    def unregister_widget(self, widget_id: int):
        """
        Unregister a widget and cleanup all its objects.
        
        Args:
            widget_id: Widget to unregister
        """
        self.safe_cleanup(widget_id)
        
        with self._lock:
            self._registry.pop(widget_id, None)
            self._contexts.pop(widget_id, None)
            self._cleanup_in_progress.pop(widget_id, None)
    
    def get_stats(self, widget_id: int) -> Dict[str, int]:
        """Get memory statistics for a widget."""
        with self._lock:
            if widget_id not in self._registry:
                return {'shapes': 0, 'ais_objects': 0, 'edge_ais_objects': 0, 'other': 0}
            
            reg = self._registry[widget_id]
            return {
                'shapes': len(reg['shapes']),
                'ais_objects': len(reg['ais_objects']),
                'edge_ais_objects': len(reg['edge_ais_objects']),
                'other': len(reg['other'])
            }


# Convenience function to get the manager
def get_occ_memory_manager() -> OCCMemoryManager:
    """Get the singleton OCCMemoryManager instance."""
    return OCCMemoryManager.get_instance()

