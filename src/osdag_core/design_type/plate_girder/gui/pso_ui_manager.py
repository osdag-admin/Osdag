"""
PSO UI Manager for Plate Girder Module
=======================================
Manages PSO visualization lifecycle including CAD/PSO widget swapping,
cleanup, and toggle functionality.

This module encapsulates all plate girder-specific UI logic that was
previously scattered in template_page.py for better maintainability.
"""

from typing import TYPE_CHECKING, Optional, Callable
import time

from PySide6.QtWidgets import QApplication, QComboBox, QWidget
from PySide6.QtCore import QTimer

# Import safe_processEvents for thread-safe UI updates during CAD operations
try:
    from osdag_gui.OS_safety_protocols import safe_processEvents
except ImportError:
    # Fallback to direct call if not available
    def safe_processEvents():
        QApplication.processEvents()

if TYPE_CHECKING:
    from osdag_gui.ui.windows.template_page import TemplatePage


class PSOUIManager:
    """Manages PSO visualization UI for Plate Girder module.
    
    Encapsulates all the CAD/PSO widget swapping, cleanup, and toggle
    functionality for the PSO optimization visualization.
    
    Attributes:
        parent: The TemplatePage instance that owns this manager
        pso_viz: The PSOVisualizerWidget instance (when active)
    """
    
    def __init__(self, parent: 'TemplatePage'):
        """Initialize PSO UI Manager.
        
        Args:
            parent: The TemplatePage instance that owns this manager
        """
        self.parent = parent
        self.pso_viz: Optional[QWidget] = None
        self._hidden_cad_widget: Optional[QWidget] = None
        self._hidden_pso_widget: Optional[QWidget] = None
        self._pso_viz_widget: Optional[QWidget] = None
        self._last_pso_iter: int = -1
        self._pso_data_for_replay = None
    
    def is_plate_girder_optimized(self) -> bool:
        """Check if current module is Plate Girder with Optimized design type.
        
        Returns:
            True if Plate Girder module with Optimized design type selected
        """
        try:
            module_name = self.parent.backend.module_name()
            is_plate_girder = module_name.upper() == "PLATE GIRDER"
            
            if not is_plate_girder:
                return False
            
            # Read design type from the actual input widget (combobox)
            design_type = 'Unknown'
            if hasattr(self.parent, 'input_dock') and self.parent.input_dock:
                design_type_widget = self.parent.input_dock.input_widget.findChild(
                    QComboBox, 'Total.Design_Type'
                )
                if design_type_widget:
                    design_type = design_type_widget.currentText()
            
            return design_type == 'Optimized'
        except Exception:
            return False
    
    def start_visualization(self, data: dict) -> bool:
        """Start PSO optimization with real-time 3D visualization.
        
        Uses a background thread for optimization so UI updates in real-time.
        PSO widget replaces CAD widget in the splitter layout directly.
        
        Args:
            data: Design input data dictionary
            
        Returns:
            True if visualization started successfully, False otherwise
        """
        # Cleanup any previous visualization first
        self.cleanup()
        
        # Restore the initial horizontal splitter layout
        self._restore_initial_layout()
        
        try:
            from osdag_core.design_type.plate_girder.visualization.pso_visualizer import (
                PSOVisualizerWidget
            )
        except ImportError as e:
            print(f"[WARNING] PSO Visualization not available: {e}")
            return False
        
        # Build complete design dictionary
        option_list = self.parent.backend.input_values()
        for data_key_tuple in self.parent.backend.customized_input():
            data_key = data_key_tuple[0] + "_customized"
            if data_key in data.keys() and len(data_key_tuple) == 4:
                data[data_key] = [data_values for data_values in data[data_key]
                                  if data_values not in data_key_tuple[2]]
        
        # Populate design_inputs
        self.parent.design_fn(option_list, data, self.parent.backend)
        
        # VALIDATION CHECK: Prevent starting visualization if inputs are invalid
        # This mirrors the check in template_page.py's common_function_for_save_and_design
        error = self.parent.backend.func_for_validation(self.parent.design_inputs)
        status = self.parent.backend.design_status
        
        if status is False or error is not None:
             print("[DEBUG] PSO Validation Failed - Returning to standard design flow")
             # Returning False causes template_page to call _run_standard_design
             # which will handle the error display and logging
             return False
        
        # Create visualization widget
        try:
            # Create PSO viz popup window (fixed size, stays on top)
            self.pso_viz = PSOVisualizerWidget(None, max_iterations=100)
            
            # Show as popup window - CAD widget stays visible underneath
            self.pso_viz.show()
            
            # Center popup on main window
            if self.parent.window():
                main_geom = self.parent.window().geometry()
                popup_geom = self.pso_viz.geometry()
                x = main_geom.x() + (main_geom.width() - popup_geom.width()) // 2
                y = main_geom.y() + (main_geom.height() - popup_geom.height()) // 2
                self.pso_viz.move(x, y)
            
            # Store reference for toggle
            self._pso_viz_widget = self.pso_viz
            
            # Connect close signal to cleanup
            self.pso_viz.switch_to_cad.connect(self._on_popup_closed)
            
            # Throttle state for UI updates
            self._last_pso_iter = -1
            
            # Callback for real-time updates (throttled to once per iteration)
            def viz_callback(depth, ur, weight, iteration, particle_idx, position=None, variables=None, lb=None, ub=None):
                if self.pso_viz:
                    self.pso_viz.add_particle_data(depth, ur, weight, iteration, particle_idx, position, variables, lb, ub)
                    # Update graph and cross-section once per iteration (not per particle)
                    # Must manually flush buffer and update canvas since timer can't fire during sync optimization
                    if iteration != self._last_pso_iter:
                        self._last_pso_iter = iteration
                        # Flush the particle data buffer
                        self.pso_viz._flush_buffer()
                        # Force synchronous canvas redraw (not draw_idle which may be deferred)
                        self.pso_viz._update_canvas_immediate()
                        # Process Qt events to actually render the update
                        safe_processEvents()
            
            self.parent.backend._viz_callback = viz_callback
            
            # Force UI update before starting design (safe version)
            safe_processEvents()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[WARNING] Failed to create visualization widget: {e}")
            self.parent.cad_widget.show()
            return False
        
        # Disable input dock during optimization
        if hasattr(self.parent, 'input_dock'):
            self.parent.input_dock.setEnabled(False)
        
        # Output dock stays visible throughout PSO - no hide/show needed
        
        # Run design SYNCHRONOUSLY on main thread (required for OpenGL safety)
        # The viz_callback includes processEvents() to update UI in real-time
        try:
            self.parent.common_function_for_save_and_design(
                self.parent.backend, data, "Design"
            )
        finally:
            if hasattr(self.parent, 'input_dock'):
                self.parent.input_dock.setEnabled(True)
        
        # CRITICAL: Sync final design data to visualizer (after adjustments like rounding)
        # This ensures the visualization shows the same values as the Output Dock
        if self.pso_viz and hasattr(self.parent, 'backend'):
            backend = self.parent.backend
            try:
                # Get final adjusted values from backend
                final_d = getattr(backend, 'total_depth', 0)
                final_tw = getattr(backend, 'web_thickness', 0)
                final_bf_top = getattr(backend, 'top_flange_width', 0)
                final_bf_bot = getattr(backend, 'bottom_flange_width', 0)
                final_tf_top = getattr(backend, 'top_flange_thickness', 0)
                final_tf_bot = getattr(backend, 'bottom_flange_thickness', 0)
                final_ur = getattr(backend, 'result_UR', 0) or 0
                
                # Calculate final weight
                area_mm2 = (final_tf_top * final_bf_top) + (final_tf_bot * final_bf_bot) + \
                           (final_tw * (final_d - final_tf_top - final_tf_bot))
                area_m2 = area_mm2 / 1e6
                length_m = getattr(backend, 'length', 0) / 1000
                final_weight = area_m2 * 7850 * length_m
                
                # Use the data processor lock for thread safety
                dp = self.pso_viz.data_processor
                with dp.lock:
                    # Build position vector matching the EXISTING variable_names from PSO
                    existing_names = dp.variable_names or []
                    
                    # Map from variable name to backend value
                    var_to_value = {
                        'D': final_d, 'd': final_d,
                        'tw': final_tw,
                        'bf': final_bf_top, 'bf_top': final_bf_top, 'bf_bot': final_bf_bot,
                        'tf': final_tf_top, 'tf_top': final_tf_top, 'tf_bot': final_tf_bot,
                        'c': getattr(backend, 'c', 0) or 0,
                        't_stiff': getattr(backend, 'IntStiffThickness', 0) or 0
                    }
                    
                    # Build position vector in same order as PSO variable_names
                    if existing_names:
                        final_position = [var_to_value.get(name, 0) for name in existing_names]
                    else:
                        # Fallback: simple symmetric girder layout
                        final_position = [final_d, final_tw, final_bf_top, final_tf_top]
                        dp.variable_names = ['D', 'tw', 'bf', 'tf']
                    
                    # Update best data
                    dp.best_weight = final_weight
                    dp.best_pos = (final_d, final_ur, final_weight)
                    dp.best_position_vector = final_position
                        
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"[WARNING] Failed to sync final data: {e}")
        
        # Mark PSO visualization as complete
        if self.pso_viz:
            self.pso_viz.set_complete()
        
        # Auto-close popup after 1.5 second delay
        QTimer.singleShot(1500, self._close_popup_and_render)
        
        # Log message about Alt+G to see graph (after delay)
        def log_alt_g_message():
            if hasattr(self.parent, 'backend') and hasattr(self.parent.backend, 'logger'):
                self.parent.backend.logger.info(
                    "Optimization complete. Press Alt+G to view the optimization graph."
                )
        QTimer.singleShot(1500, log_alt_g_message)
        
        # Enable toggle action
        if hasattr(self.parent, 'toggle_opt_action'):
            self.parent.toggle_opt_action.setEnabled(True)
        
        return True
    
    def _on_popup_closed(self):
        """Handle popup close without regenerating model (user closed manually)."""
        # Just update the reference - don't trigger model regen
        if self.pso_viz:
            self._hidden_pso_widget = self.pso_viz
            # Don't delete - user might want to toggle back
        self.pso_viz = None
    
    def _close_popup_and_render(self):
        """Close popup and trigger 3D model generation."""
        if self.pso_viz:
            self._hidden_pso_widget = self.pso_viz
            self.pso_viz.hide()
            self.pso_viz = None
        
        # Trigger 3D model generation
        if hasattr(self.parent, '_render_3d_result'):
            self.parent._render_3d_result(self.parent.backend.design_status, self.parent.backend)
    
    def restore_cad_from_pso(self, regenerate_model=False):
        """Close PSO popup window (CAD is already visible).
        
        Args:
            regenerate_model: If True, triggers 3D model generation
        """
        # Hide the popup window, store for later toggle
        if self.pso_viz:
            self.pso_viz.hide()
            self._hidden_pso_widget = self.pso_viz
            self.pso_viz = None
        
        # Trigger 3D model generation if requested
        if regenerate_model:
            print("[DEBUG] Triggering 3D model generation")
            if hasattr(self.parent, '_render_3d_result'):
                self.parent._render_3d_result(self.parent.backend.design_status, self.parent.backend)

    
    def show_pso_from_cad(self) -> bool:
        """Show PSO visualization popup window.
        
        Returns:
            True if popup was shown, False if no PSO widget available
        """
        # Only works if we have a hidden PSO widget
        if not self._hidden_pso_widget:
            return False
        
        # Show the popup window
        self.pso_viz = self._hidden_pso_widget
        self._hidden_pso_widget = None
        self.pso_viz.show()
        
        # Center on main window
        if self.parent.window():
            main_geom = self.parent.window().geometry()
            popup_geom = self.pso_viz.geometry()
            x = main_geom.x() + (main_geom.width() - popup_geom.width()) // 2
            y = main_geom.y() + (main_geom.height() - popup_geom.height()) // 2
            self.pso_viz.move(x, y)
        
        return True
    
    def toggle_view(self):
        """Toggle PSO visualization popup window visibility.
        
        Called by Alt+G keyboard shortcut.
        """
        # Check if PSO popup is currently visible
        if self.pso_viz and self.pso_viz.isVisible():
            # PSO is visible, hide it
            self.pso_viz.hide()
            self._hidden_pso_widget = self.pso_viz
            self.pso_viz = None
        else:
            # PSO is hidden, try to show it
            self.show_pso_from_cad()
    
    def cleanup(self):
        """Clean up PSO visualization resources safely.
        
        Simply closes popup window and clears references.
        """
        # First, clear the callback to prevent any more updates
        if hasattr(self.parent, 'backend') and hasattr(self.parent.backend, '_viz_callback'):
            self.parent.backend._viz_callback = None
        
        # Cleanup visible PSO popup
        if self.pso_viz:
            try:
                self.pso_viz.cleanup()
            except Exception:
                pass
            
            try:
                self.pso_viz.hide()
                self.pso_viz.deleteLater()
            except Exception:
                pass
            
            self.pso_viz = None
        
        # Cleanup hidden PSO widget
        if self._hidden_pso_widget:
            try:
                self._hidden_pso_widget.cleanup()
            except Exception:
                pass
            
            try:
                self._hidden_pso_widget.hide()
                self._hidden_pso_widget.deleteLater()
            except Exception:
                pass
            
            self._hidden_pso_widget = None
        
        # Clear widget references
        self._pso_viz_widget = None
        self._pso_data_for_replay = None
        self._last_pso_iter = -1
    
    def _restore_initial_layout(self):
        """Restore the initial horizontal splitter layout for Plate Girder module.
        
        This ensures proper splitter sizing when pressing Design.
        Keeps all docks visible - PSO graph displays in central area without layout changes.
        Preserves the horizontal splitter sizes so output dock maintains its width.
        """
        try:
            # Ensure input dock is visible and enabled
            if hasattr(self.parent, 'input_dock') and self.parent.input_dock:
                self.parent.input_dock.show()
                self.parent.input_dock.setEnabled(True)
                # Unlock input dock for editing during PSO
                if hasattr(self.parent.input_dock, 'toggle_lock'):
                    self.parent.input_dock.toggle_lock(set_locked_state=False)
            
            # Ensure output dock stays visible (no changes to layout)
            if hasattr(self.parent, 'output_dock') and self.parent.output_dock:
                self.parent.output_dock.show()
            
            # Hide dock indicator labels since docks are visible
            if hasattr(self.parent, 'input_dock_label'):
                self.parent.input_dock_label.setVisible(False)
            if hasattr(self.parent, 'output_dock_label'):
                self.parent.output_dock_label.setVisible(False)
            
            # Preserve horizontal splitter sizes - like CAD viewing area behavior
            # This ensures output dock maintains its width during PSO visualization
            if hasattr(self.parent, 'splitter') and self.parent.splitter:
                splitter = self.parent.splitter
                current_sizes = splitter.sizes()
                
                # Only adjust if splitter has 3 widgets (input, central, output)
                if len(current_sizes) == 3 and sum(current_sizes) > 0:
                    # Get preferred dock widths
                    input_w = self.parent.input_dock.sizeHint().width() if self.parent.input_dock.isVisible() else 0
                    output_w = self.parent.output_dock.sizeHint().width() if self.parent.output_dock.isVisible() else 0
                    
                    total_w = splitter.width()
                    if total_w > 0:
                        # Calculate central area width (remaining after docks)
                        central_w = max(0, total_w - input_w - output_w)
                        splitter.setSizes([input_w, central_w, output_w])
                        splitter.refresh()
            
        except Exception as e:
            print(f"[WARNING] Failed to restore initial layout: {e}")

    
    def on_pso_complete(self, data, success: bool):
        """Handle PSO optimization completion (legacy method).
        
        Args:
            data: Optimization result data
            success: Whether optimization was successful
        """
        # Switch to CAD view
        if self.pso_viz:
            self.pso_viz.hide()
        if hasattr(self.parent, 'cad_widget') and self.parent.cad_widget:
            self.parent.cad_widget.show()
        
        # Enable toggle
        if hasattr(self.parent, 'toggle_opt_action'):
            self.parent.toggle_opt_action.setEnabled(True)
