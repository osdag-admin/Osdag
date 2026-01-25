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
            # Create PSO viz widget
            self.pso_viz = PSOVisualizerWidget(None, max_iterations=100)
            
            # Hide CAD widget completely
            self.parent.cad_widget.hide()
            
            # Remove cad_widget from splitter temporarily
            self.parent.cad_widget.setParent(None)
            
            # Insert PSO viz at index 0
            self.parent.cad_log_splitter.insertWidget(0, self.pso_viz)
            self.pso_viz.show()
            
            # Store CAD widget for later restoration  
            self._hidden_cad_widget = self.parent.cad_widget
            
            # Set splitter sizes: [viz, logs]
            total_height = self.parent.cad_log_splitter.height()
            if total_height > 0:
                viz_h = int(total_height * 6 / 7)
                log_h = total_height - viz_h
                self.parent.cad_log_splitter.setSizes([viz_h, log_h])
            
            # Ensure log dock is visible
            if hasattr(self.parent, 'logs_dock') and self.parent.logs_dock:
                self.parent.logs_dock.show()
                
            # Store reference for toggle
            self._pso_viz_widget = self.pso_viz
            
            # Connect toggle
            self.pso_viz.switch_to_cad.connect(self.restore_cad_from_pso)
            
            # Throttle state for UI updates
            self._last_pso_iter = -1
            
            # Callback for real-time updates (throttled to once per iteration)
            def viz_callback(depth, ur, weight, iteration, particle_idx, position=None, variables=None, lb=None, ub=None):
                if self.pso_viz:
                    self.pso_viz.add_particle_data(depth, ur, weight, iteration, particle_idx, position, variables, lb, ub)
                    # Only process events once per iteration (not per particle!)
                    if iteration != self._last_pso_iter:
                        self._last_pso_iter = iteration
                        QApplication.processEvents()
            
            self.parent.backend._viz_callback = viz_callback
            
            # Force UI update before starting design
            QApplication.processEvents()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[WARNING] Failed to create visualization widget: {e}")
            self.parent.cad_widget.show()
            return False
        
        # Disable input dock during optimization
        if hasattr(self.parent, 'input_dock'):
            self.parent.input_dock.setEnabled(False)
        
        # Hide output dock during optimization
        if hasattr(self.parent, 'output_dock'):
            self.parent.output_dock.hide()
        
        # Run design SYNCHRONOUSLY on main thread (required for OpenGL safety)
        # The viz_callback includes processEvents() to update UI in real-time
        try:
            self.parent.common_function_for_save_and_design(
                self.parent.backend, data, "Design"
            )
        finally:
            if hasattr(self.parent, 'input_dock'):
                self.parent.input_dock.setEnabled(True)
        
        # Show output dock after optimization
        if hasattr(self.parent, 'output_dock'):
            self.parent.output_dock.show()
        
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
        
        # Auto-switch to CAD view after 1.5 second delay
        # Pass regenerate_model=True to trigger 3D model generation now that CAD widget will be restored
        QTimer.singleShot(1500, lambda: self.restore_cad_from_pso(regenerate_model=True))
        
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
    
    def restore_cad_from_pso(self, regenerate_model=False):
        """Swap from PSO visualization to CAD widget.
        
        Properly removes PSO from splitter before inserting CAD.
        
        Args:
            regenerate_model: If True, triggers 3D model generation (used effectively after optimization)
        """
        # FIRST: Remove PSO viz from splitter (store for later toggle)
        if self.pso_viz:
            self.pso_viz.hide()
            self.pso_viz.setParent(None)  # Remove from splitter
            self._hidden_pso_widget = self.pso_viz
        
        # THEN: Restore CAD widget to splitter at index 0
        if self._hidden_cad_widget:
            self.parent.cad_log_splitter.insertWidget(0, self._hidden_cad_widget)
            self._hidden_cad_widget.show()
            self.parent.cad_widget = self._hidden_cad_widget
            self._hidden_cad_widget = None
        elif hasattr(self.parent, 'cad_widget') and self.parent.cad_widget:
            # CAD is still in splitter, just show it
            self.parent.cad_widget.show()
        
        # Ensure logs dock is visible
        if hasattr(self.parent, 'logs_dock') and self.parent.logs_dock:
            self.parent.logs_dock.show()
        
        # Reset splitter sizes for 2 widgets: [cad, logs]
        total_height = self.parent.cad_log_splitter.height()
        if total_height > 0:
            cad_h = int(total_height * 6 / 7)
            log_h = total_height - cad_h
            self.parent.cad_log_splitter.setSizes([cad_h, log_h])

        # Trigger 3D model generation if requested
        if regenerate_model:
            print("[DEBUG] Triggering delayed 3D model generation (post-PSO restoration)")
            # Use the new helper method in template_page
            if hasattr(self.parent, '_render_3d_result'):
                self.parent._render_3d_result(self.parent.backend.design_status, self.parent.backend)

    
    def show_pso_from_cad(self) -> bool:
        """Swap from CAD widget to PSO visualization.
        
        Properly removes CAD from splitter before inserting PSO.
        
        Returns:
            True if swap was successful, False if no PSO widget available
        """
        # Only works if we have a hidden PSO widget
        if not self._hidden_pso_widget:
            return False
        
        # FIRST: Remove CAD from splitter (store for later toggle)
        if hasattr(self.parent, 'cad_widget') and self.parent.cad_widget:
            self.parent.cad_widget.hide()
            self.parent.cad_widget.setParent(None)  # Remove from splitter
            self._hidden_cad_widget = self.parent.cad_widget
        
        # THEN: Insert PSO at index 0
        self.parent.cad_log_splitter.insertWidget(0, self._hidden_pso_widget)
        self._hidden_pso_widget.show()
        self._pso_viz_widget = self._hidden_pso_widget
        self.pso_viz = self._hidden_pso_widget  # Update main reference
        self._hidden_pso_widget = None
        
        # Ensure logs dock is visible
        if hasattr(self.parent, 'logs_dock') and self.parent.logs_dock:
            self.parent.logs_dock.show()
        
        # Set splitter sizes for 2 widgets: [pso, logs]
        total_height = self.parent.cad_log_splitter.height()
        if total_height > 0:
            viz_h = int(total_height * 6 / 7)
            log_h = total_height - viz_h
            self.parent.cad_log_splitter.setSizes([viz_h, log_h])
        
        return True
    
    def toggle_view(self):
        """Toggle between PSO visualization and CAD view.
        
        Bidirectional toggle that preserves both widgets.
        Called by Alt+G keyboard shortcut.
        """
        # Check if PSO is visible
        pso_visible = False
        if self.pso_viz and self.pso_viz.isVisible():
            pso_visible = True
        elif self._pso_viz_widget and self._pso_viz_widget.isVisible():
            pso_visible = True
        
        if pso_visible:
            # PSO is visible, switch to CAD
            self.restore_cad_from_pso()
        else:
            # CAD is visible, try to switch to PSO
            if not self.show_pso_from_cad():
                # No PSO widget available, ensure CAD is shown
                if hasattr(self.parent, 'cad_widget') and self.parent.cad_widget:
                    self.parent.cad_widget.show()
    
    def cleanup(self):
        """Clean up PSO visualization resources safely.
        
        Prevents heap corruption by properly stopping timers,
        removing widgets from parents, and clearing references.
        """
        # First, clear the callback to prevent any more updates
        if hasattr(self.parent, 'backend') and hasattr(self.parent.backend, '_viz_callback'):
            self.parent.backend._viz_callback = None
        
        # Cleanup visualization widget
        if self.pso_viz:
            try:
                # Stop all timers first
                self.pso_viz.cleanup()
            except Exception:
                pass
            
            try:
                # Hide and remove from parent
                self.pso_viz.hide()
                self.pso_viz.setParent(None)
            except Exception:
                pass
            
            # NOTE: DO NOT call QApplication.processEvents() here!
            # It causes OpenGL race conditions that corrupt memory.
            
            try:
                # Schedule for deletion
                self.pso_viz.deleteLater()
            except Exception:
                pass
            
            # Clear references
            self.pso_viz = None
        
        # Clear widget references
        self._pso_viz_widget = None
        self._hidden_pso_widget = None
        
        # Clear replay data
        self._pso_data_for_replay = None
        
        # IMPORTANT: Restore hidden CAD widget if it was removed from splitter
        try:
            if self._hidden_cad_widget:
                # CAD widget was removed from splitter, restore it
                self.parent.cad_log_splitter.insertWidget(0, self._hidden_cad_widget)
                self._hidden_cad_widget.show()
                self.parent.cad_widget = self._hidden_cad_widget
                self._hidden_cad_widget = None
            elif hasattr(self.parent, 'cad_widget') and self.parent.cad_widget:
                # CAD widget is still in splitter, just show it
                self.parent.cad_widget.show()
            
            # Ensure logs dock is visible
            if hasattr(self.parent, 'logs_dock') and self.parent.logs_dock:
                self.parent.logs_dock.show()
            
            if hasattr(self.parent, 'cad_log_splitter'):
                total_height = self.parent.cad_log_splitter.height()
                if total_height > 0:
                    cad_h = int(total_height * 6 / 7)
                    log_h = total_height - cad_h
                    self.parent.cad_log_splitter.setSizes([cad_h, log_h])
                    self.parent.cad_log_splitter.setStretchFactor(0, 6)
                    self.parent.cad_log_splitter.setStretchFactor(1, 1)
        except Exception:
            pass
        
        # Reset throttle variable for next design run
        self._last_pso_iter = -1
        
        # NOTE: DO NOT call QApplication.processEvents() here!
        # It causes OpenGL race conditions that corrupt memory.
    
    def _restore_initial_layout(self):
        """Restore the initial horizontal splitter layout for Plate Girder module.
        
        This ensures the input dock retains its original narrow width when
        pressing Design multiple times. Only affects horizontal splitter,
        not the vertical CAD/logs splitter.
        """
        try:
            # Show input dock with original width
            if hasattr(self.parent, 'input_dock') and self.parent.input_dock:
                self.parent.input_dock.show()
                self.parent.input_dock.setEnabled(True)
                # Unlock input dock for editing during PSO
                if hasattr(self.parent.input_dock, 'toggle_lock'):
                    self.parent.input_dock.toggle_lock(set_locked_state=False)
            
            # Hide input dock indicator label
            if hasattr(self.parent, 'input_dock_label'):
                self.parent.input_dock_label.setVisible(False)
            
            # Hide output dock during PSO optimization
            if hasattr(self.parent, 'output_dock') and self.parent.output_dock:
                self.parent.output_dock.hide()
            
            # Show output dock indicator label
            if hasattr(self.parent, 'output_dock_label'):
                self.parent.output_dock_label.setVisible(True)
            
            # Restore splitter sizes: [input_dock, central, output_dock=0]
            if hasattr(self.parent, 'splitter') and self.parent.splitter:
                # Use stored default width or sizeHint
                input_width = getattr(self.parent, '_input_dock_default_width', None)
                if input_width is None:
                    input_width = (
                        self.parent.input_dock.sizeHint().width() 
                        if self.parent.input_dock else 320
                    )
                
                total_width = self.parent.splitter.width()
                if total_width <= 0:
                    total_width = self.parent.width()
                
                # Layout: [input_dock, central_widget, output_dock=0]
                center_width = max(0, total_width - input_width)
                target_sizes = [input_width, center_width, 0]
                
                self.parent.splitter.setSizes(target_sizes)
                try:
                    self.parent.splitter.refresh()
                except Exception:
                    pass
                self.parent.splitter.update()
            
            # Update dock control icons
            self.parent.input_dock_active = True
            self.parent.output_dock_active = False
            self.parent.update_docking_icons(input_is_active=True, output_is_active=False)
            
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
