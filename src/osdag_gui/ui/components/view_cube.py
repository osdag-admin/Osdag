"""
Chamfered View Cube - Pure Python implementation using OCC geometry.
Provides 26 interactive regions: 6 faces, 8 corners, 12 edges.
"""
from typing import Dict, Optional
from dataclasses import dataclass
import math

from PySide6.QtCore import QObject, Signal

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepFilletAPI import BRepFillet_MakeChamfer
from OCC.Core.BRepPrim import BRepPrim_MakeBox
from OCC.Core.gp import (
    gp_Pnt,
    gp_Dir,
    gp_Ax3,
    gp_Trsf,
)
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Solid
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_WHITE,
    Quantity_NOC_CYAN,
    Quantity_NOC_MAGENTA,
)
from OCC.Core.Prs3d import Prs3d_Drawer


@dataclass
class ViewDirection:
    """Represents a view direction with name and transformation."""
    name: str
    direction: gp_Dir
    rotation: Optional[gp_Trsf] = None


class ChamferedViewCube(QObject):
    """
    Creates a chamfered (beveled) cube geometry for view navigation.
    
    The cube has:
    - 6 main faces (Top, Bottom, Front, Back, Left, Right)
    - 8 corner regions
    - 12 edge regions
    
    Each region can be clicked to set the corresponding view.
    """
    
    # Standard view directions
    VIEWS = {
        # Face views
        "front": ViewDirection("Front", gp_Dir(0, 0, 1)),
        "back": ViewDirection("Back", gp_Dir(0, 0, -1)),
        "top": ViewDirection("Top", gp_Dir(0, 1, 0)),
        "bottom": ViewDirection("Bottom", gp_Dir(0, -1, 0)),
        "right": ViewDirection("Right", gp_Dir(1, 0, 0)),
        "left": ViewDirection("Left", gp_Dir(-1, 0, 0)),
        
        # Corner views (isometric-style)
        "front_top_right": ViewDirection("Front Top Right", gp_Dir(1, 1, 1)),
        "front_top_left": ViewDirection("Front Top Left", gp_Dir(-1, 1, 1)),
        "front_bottom_right": ViewDirection("Front Bottom Right", gp_Dir(1, -1, 1)),
        "front_bottom_left": ViewDirection("Front Bottom Left", gp_Dir(-1, -1, 1)),
        "back_top_right": ViewDirection("Back Top Right", gp_Dir(1, 1, -1)),
        "back_top_left": ViewDirection("Back Top Left", gp_Dir(-1, 1, -1)),
        "back_bottom_right": ViewDirection("Back Bottom Right", gp_Dir(1, -1, -1)),
        "back_bottom_left": ViewDirection("Back Bottom Left", gp_Dir(-1, -1, -1)),
        
        # Edge views
        "front_top": ViewDirection("Front Top", gp_Dir(0, 1, 1)),
        "front_bottom": ViewDirection("Front Bottom", gp_Dir(0, -1, 1)),
        "front_right": ViewDirection("Front Right", gp_Dir(1, 0, 1)),
        "front_left": ViewDirection("Front Left", gp_Dir(-1, 0, 1)),
        "back_top": ViewDirection("Back Top", gp_Dir(0, 1, -1)),
        "back_bottom": ViewDirection("Back Bottom", gp_Dir(0, -1, -1)),
        "back_right": ViewDirection("Back Right", gp_Dir(1, 0, -1)),
        "back_left": ViewDirection("Back Left", gp_Dir(-1, 0, -1)),
        "top_right": ViewDirection("Top Right", gp_Dir(1, 1, 0)),
        "top_left": ViewDirection("Top Left", gp_Dir(-1, 1, 0)),
        "bottom_right": ViewDirection("Bottom Right", gp_Dir(1, -1, 0)),
        "bottom_left": ViewDirection("Bottom Left", gp_Dir(-1, -1, 0)),
    }
    
    view_selected = Signal(str)  # Emits view name when clicked
    
    def __init__(
        self,
        size: float = 45.0,
        chamfer_radius: float = 8.0,
        parent: Optional[QObject] = None
    ):
        super().__init__(parent)
        self.size = size
        self.chamfer_radius = chamfer_radius
        self._half_size = size / 2.0
        
        # Cache for AIS shapes
        self._main_cube_shape: Optional[TopoDS_Solid] = None
        self._chamfered_cube_shape: Optional[TopoDS_Solid] = None
        self._ais_shapes: Dict[str, AIS_Shape] = {}
        
        # Colors
        self._default_color = Quantity_Color(Quantity_NOC_WHITE)
        self._highlight_color = Quantity_Color(Quantity_NOC_CYAN)
        self._hover_color = Quantity_Color(Quantity_NOC_MAGENTA)
        
        self._build_geometry()
    
    def _build_geometry(self) -> None:
        """Build the chamfered cube geometry."""
        # Create basic box
        box_maker = BRepPrim_MakeBox(
            gp_Pnt(-self._half_size, -self._half_size, -self._half_size),
            self.size, self.size, self.size
        )
        self._main_cube_shape = box_maker.Solid()
        
        # Apply chamfer (bevel) to all edges
        self._chamfered_cube_shape = self._apply_chamfer(
            self._main_cube_shape, 
            self.chamfer_radius
        )
    
    def _apply_chamfer(
        self, 
        shape: TopoDS_Solid, 
        radius: float
    ) -> TopoDS_Solid:
        """
        Apply chamfer (bevel) to all edges of the solid.
        This creates the characteristic beveled edges of the view cube.
        """
        try:
            # Get all edges from the solid
            from OCC.Core.TopExp import TopExp_Explorer
            from OCC.Core.TopAbs import TopAbs_EDGE
            
            edges = []
            exp = TopExp_Explorer(shape, TopAbs_EDGE)
            while exp.More():
                edges.append(exp.Current())
                exp.Next()
            
            if not edges:
                return shape
            
            # Create chamfer operation
            fillet = BRepFillet_MakeChamfer(shape)
            
            # Add all edges with the same chamfer distance
            for edge in edges:
                fillet.Add(radius, edge)
            
            return fillet.Solid()
            
        except Exception as e:
            print(f"Chamfer failed, using basic cube: {e}")
            return shape
    
    def get_shape(self) -> TopoDS_Solid:
        """Get the chamfered cube shape."""
        if self._chamfered_cube_shape is None:
            self._build_geometry()
        return self._chamfered_cube_shape
    
    def get_ais_shape(self, name: str) -> AIS_Shape:
        """
        Get or create an AIS_Shape for a specific view region.
        
        Args:
            name: View name (e.g., 'front', 'front_top_right', 'front_top')
            
        Returns:
            AIS_Shape that can be displayed in the viewer
        """
        if name in self._ais_shapes:
            return self._ais_shapes[name]
        
        # Get the view direction
        if name not in self.VIEWS:
            raise ValueError(f"Unknown view: {name}")
        
        view_info = self.VIEWS[name]
        
        # Create transformed shape for this view
        shape = self._create_view_shape(name, view_info)
        
        # Create AIS object
        ais_shape = AIS_Shape(shape)
        
        # Set appearance
        drawer = Prs3d_Drawer()
        drawer.SetColor(self._default_color)
        ais_shape.SetAttributes(drawer)
        
        # Store in cache
        self._ais_shapes[name] = ais_shape
        
        return ais_shape
    
    def _create_view_shape(
        self, 
        name: str, 
        view_info: ViewDirection
    ) -> TopoDS_Shape:
        """
        Create a transformed shape for a specific view.
        
        The shape is oriented to face the camera in the corresponding view.
        """
        # Get base shape
        base_shape = self.get_shape()
        
        # Calculate rotation to align with view direction
        # Default view is +Z (front)
        default_dir = gp_Dir(0, 0, 1)
        target_dir = view_info.direction
        
        # Create rotation transformation
        trsf = gp_Trsf()
        
        # Calculate rotation axis and angle using quaternion-like approach
        axis = default_dir.Crossed(target_dir)
        
        if axis.Magnitude() < 1e-10:
            # Directions are parallel or opposite
            if default_dir.IsOpposite(target_dir, 1e-10):
                # 180 degree rotation around X axis
                trsf.SetRotation(gp_Ax3(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.pi)
        else:
            # General case - rotate around cross product axis
            axis.Normalize()
            angle = default_dir.Angle(target_dir)
            trsf.SetRotation(gp_Ax3(gp_Pnt(0, 0, 0), axis), angle)
        
        # Apply transformation
        builder = BRepBuilderAPI_Transform(base_shape, trsf, True)
        return builder.Shape()
    
    def get_all_ais_shapes(self) -> Dict[str, AIS_Shape]:
        """Get all AIS shapes for the view cube."""
        for name in self.VIEWS:
            if name not in self._ais_shapes:
                self.get_ais_shape(name)
        return self._ais_shapes
    
    def set_highlight(self, name: str, highlight: bool = True) -> None:
        """Set highlight state for a specific view."""
        if name in self._ais_shapes:
            ais_shape = self._ais_shapes[name]
            if highlight:
                drawer = Prs3d_Drawer()
                drawer.SetColor(self._highlight_color)
                ais_shape.SetHilightAttributes(drawer)
            else:
                ais_shape.ClearHilight()
    
    def get_view_from_click(
        self, 
        x: int, 
        y: int, 
        viewer
    ) -> Optional[str]:
        """
        Determine which view was clicked based on screen coordinates.
        
        Args:
            x, y: Screen coordinates
            viewer: The OCC 3D viewer
            
        Returns:
            View name or None if no valid view clicked
        """
        if not viewer or not viewer.context:
            return None
        
        try:
            viewer.context.MoveTo(x, y, viewer.view, True)
            
            if viewer.context.HasDetected():
                detected = viewer.context.DetectedInteractive()
                
                # Check if any of our shapes was detected
                for name, ais_shape in self._ais_shapes.items():
                    if detected == ais_shape:
                        return name
            
            return None
            
        except Exception as e:
            print(f"Error detecting view click: {e}")
            return None
    
    def reset(self) -> None:
        """Clear cached shapes."""
        self._ais_shapes.clear()
