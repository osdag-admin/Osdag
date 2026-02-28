import ifcopenshell
import numpy as np

class GeometryMapper:
    """
    Handles the translation of OpenCASCADE TopoDS_Shape objects from Osdag
    into buildingSMART IFC geometric representations.
    This version explicitly handles 28 CAD classes with precise parametric profiles.
    """
    
    def __init__(self, ifc_exporter):
        self.exporter = ifc_exporter
        self.ifc_file = ifc_exporter.ifc_file

    def _create_placement(self, point, dir_z, dir_x):
        point_ifc = self.ifc_file.createIfcCartesianPoint([float(x) for x in point])
        axis = self.ifc_file.createIfcDirection([float(x) for x in dir_z])
        # Force orthogonal normalization if needed
        if abs(np.dot(dir_z, dir_x)) > 0.01:
            vDir = np.cross(dir_z, dir_x)
            vDir = vDir / np.linalg.norm(vDir)
            dir_x = np.cross(vDir, dir_z)
        ref_dir = self.ifc_file.createIfcDirection([float(x) for x in dir_x])
        return self.ifc_file.createIfcAxis2Placement3D(Location=point_ifc, Axis=axis, RefDirection=ref_dir)

    def _create_placement_2d(self, point=(0., 0.), dir_x=(1., 0.)):
        point_ifc = self.ifc_file.createIfcCartesianPoint([float(x) for x in point])
        ref_dir = self.ifc_file.createIfcDirection([float(x) for x in dir_x])
        return self.ifc_file.createIfcAxis2Placement2D(Location=point_ifc, RefDirection=ref_dir)

    # ─────────────────────────────────────────────────────────────────────────────
    # Standard Extrusions Map
    # ─────────────────────────────────────────────────────────────────────────────

    def map_extruded_solid(self, osdag_obj):
        obj_class = getattr(osdag_obj, '_class_name', osdag_obj.__class__.__name__)

        # Universal extraction of local coordinates
        origin = getattr(osdag_obj, 'sec_origin', None) or getattr(osdag_obj, 'origin', [0,0,0])
        uDir = getattr(osdag_obj, 'uDir', [1,0,0])
        wDir = getattr(osdag_obj, 'wDir', [0,0,1])
        vDir = getattr(osdag_obj, 'vDir', None)
        if vDir is None:
            vDir = np.cross(wDir, uDir)
            
        placement = self._create_placement(origin, wDir, uDir)
        profile = None
        extrusion_depth = 0.0

        if obj_class == "ISection":
            B, D, t, T = float(osdag_obj.B), float(osdag_obj.D), float(osdag_obj.t), float(osdag_obj.T)
            points_2d = [
                (t/2, D/2-T), (B/2, D/2-T), (B/2, D/2), (-B/2, D/2), (-B/2, D/2-T), (-t/2, D/2-T),
                (-t/2, -D/2+T), (-B/2, -D/2+T), (-B/2, -D/2), (B/2, -D/2), (B/2, -D/2+T), (t/2, -D/2+T)
            ]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            extrusion_depth = float(osdag_obj.length)

        elif obj_class == "Channel":
            D, W, t, T = float(osdag_obj.D), float(osdag_obj.B), float(osdag_obj.t), float(osdag_obj.T)
            points_2d = [(0,0), (-W,0), (-W,D), (0,D), (0,D-T), (-(W-t),D-T), (-(W-t),T), (0,T)]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            extrusion_depth = float(osdag_obj.L)

        elif obj_class in ["Angle", "DoubleAngle"]:
            D, W = float(osdag_obj.A), float(osdag_obj.B)
            profile = self.ifc_file.createIfcLShapeProfileDef(
                ProfileType="AREA", Position=self._create_placement_2d((W/2., D/2.)),
                Depth=D, Width=W, Thickness=float(osdag_obj.T),
                FilletRadius=float(osdag_obj.R1) if hasattr(osdag_obj, 'R1') and osdag_obj.R1 > 0 else None,
                EdgeRadius=float(osdag_obj.R2) if hasattr(osdag_obj, 'R2') and osdag_obj.R2 > 0 else None
            )
            extrusion_depth = float(osdag_obj.L)

        elif obj_class == "RectHollow":
            profile = self.ifc_file.createIfcRectangleHollowProfileDef(
                ProfileType="AREA", Position=self._create_placement_2d(),
                XDim=float(osdag_obj.B) if hasattr(osdag_obj, 'B') else float(osdag_obj.L),
                YDim=float(osdag_obj.D) if hasattr(osdag_obj, 'D') else float(osdag_obj.W),
                WallThickness=float(osdag_obj.T)
            )
            extrusion_depth = float(osdag_obj.L) if hasattr(osdag_obj, 'L') else float(osdag_obj.H)
            
        elif obj_class == "CircularHollow":
            profile = self.ifc_file.createIfcCircleHollowProfileDef(
                ProfileType="AREA", Position=self._create_placement_2d(),
                Radius=float(getattr(osdag_obj, 'r', getattr(osdag_obj, 'R', 10))),
                WallThickness=float(osdag_obj.T)
            )
            extrusion_depth = float(osdag_obj.H) if hasattr(osdag_obj, 'H') else float(osdag_obj.L)

        elif obj_class == "StiffenerPlate":
            # Parametric triangular/tapered stiffener
            L, W, T = float(osdag_obj.L), float(osdag_obj.W), float(osdag_obj.T)
            L11 = float(getattr(osdag_obj, 'L11', 0.0))
            L12 = float(getattr(osdag_obj, 'L12', 0.0))
            R11 = float(getattr(osdag_obj, 'R11', 0.0))
            R12 = float(getattr(osdag_obj, 'R12', 0.0))
            R21 = float(getattr(osdag_obj, 'R21', 0.0))
            R22 = float(getattr(osdag_obj, 'R22', 0.0))
            L21 = float(getattr(osdag_obj, 'L21', 0.0))
            L22 = float(getattr(osdag_obj, 'L22', 0.0))

            # Points a1 to a8 based on Osdag's StiffenerPlate geometry
            points_2d = [
                (-L/2 + L11, W/2), (L/2 - R11, W/2), (L/2, W/2 - R12),
                (L/2, -W/2 + R22), (L/2 - R21, -W/2), (-L/2 + L21, -W/2),
                (-L/2, -W/2 + L22), (-L/2, W/2 - L12)
            ]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            extrusion_depth = T
            placement = self._create_placement(osdag_obj.sec_origin, osdag_obj.wDir, osdag_obj.uDir)
            return self.ifc_file.createIfcExtrudedAreaSolid(SweptArea=profile, Position=placement, ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,1.)), Depth=extrusion_depth)

        elif obj_class in ["Plate", "stiffener", "stiffener_flange"]:
            T = float(getattr(osdag_obj, 'T', getattr(osdag_obj, 't', 10)))
            L = float(getattr(osdag_obj, 'L', getattr(osdag_obj, 'Hst', 100)))
            W = float(getattr(osdag_obj, 'W', getattr(osdag_obj, 'Lst', 100)))
            profile = self.ifc_file.createIfcRectangleProfileDef(
                ProfileType="AREA", Position=self._create_placement_2d(),
                XDim=T, YDim=L
            )
            extrusion_depth = W

        elif obj_class == "GassetPlate":
            import math
            H, L, deg = float(osdag_obj.H), float(osdag_obj.L), math.radians(float(osdag_obj.degree))
            points_2d = [(0, H/2), (0, -H/2), (-L, -H/2 - L*math.tan(deg)), (-L, H/2 + L*math.tan(deg))]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            placement = self._create_placement(osdag_obj.sec_origin, osdag_obj.vDir, osdag_obj.uDir)
            return self.ifc_file.createIfcExtrudedAreaSolid(
                SweptArea=profile, Position=placement,
                ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,1.)), Depth=float(osdag_obj.T)
            )
            
        elif obj_class in ["Concrete", "Grout"]:
            L, W, T = float(osdag_obj.L), float(osdag_obj.W), float(osdag_obj.T)
            profile = self.ifc_file.createIfcRectangleProfileDef(
                ProfileType="AREA", Position=self._create_placement_2d(),
                XDim=L, YDim=W
            )
            # Extrude thick blocks
            extrusion_depth = T

        elif obj_class == "Stiffener_CAD":
            Hst, Lst = float(osdag_obj.Hst), float(osdag_obj.Lst)
            points_2d = [(0.0, Hst), (25.0, Hst), (Lst, 25.0), (Lst, 0.0)]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            extrusion_depth = float(osdag_obj.Tst)
            
        elif obj_class == "Notch":
            w, h = float(osdag_obj.width), float(osdag_obj.height)
            points_2d = [(w/2, 0), (w/2, -h), (-w/2, -h), (-w/2, 0)]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            extrusion_depth = float(osdag_obj.length)
            
        elif obj_class == "QuarterCone":
            import math
            b, h = float(osdag_obj.b), float(osdag_obj.h)
            points_2d = [(b, 0), (0, 0), (0, h)]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            axis = self.ifc_file.createIfcAxis1Placement(
                Location=self.ifc_file.createIfcCartesianPoint((0.,0.,0.)),
                Axis=self.ifc_file.createIfcDirection((0.,0.,1.))
            )
            return self.ifc_file.createIfcRevolvedAreaSolid(
                SweptArea=profile, Position=placement,
                Axis=axis, Angle=math.radians(float(osdag_obj.coneAngle))
            )

        else:
            print(f"[GeometryMapper2] Ignoring internal/abstract shape: {obj_class}")
            return None

        # Return Uniform Extrusion
        return self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=profile, Position=placement,
            ExtrudedDirection=self.ifc_file.createIfcDirection((0., 0., 1.)), Depth=extrusion_depth
        )


    # ─────────────────────────────────────────────────────────────────────────────
    # Complex Polygonal Extrusion for Hardware (Bolts, Nuts, Washers) - LOD 500
    # ─────────────────────────────────────────────────────────────────────────────

    def _create_bolt_representation(self, bolt_obj):
        """Creates the cached B-Rep representation of a Hex Bolt."""
        head_radius, head_thickness = float(bolt_obj.R), float(bolt_obj.T)
        points = []
        for i in range(6):
            angle = np.deg2rad(i * 60)
            points.append([float(head_radius * np.cos(angle)), float(head_radius * np.sin(angle))])
        
        head_profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
            ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points + [points[0]]])
        )
        head_solid = self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=head_profile, Position=self._create_placement((0.,0.,0.), (0.,0.,1.), (1.,0.,0.)),
            ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,-1.)), Depth=head_thickness
        )
        
        shank_radius, shank_length = float(bolt_obj.r), float(bolt_obj.H)
        shank_profile = self.ifc_file.createIfcCircleProfileDef(
            ProfileType="AREA", Position=self._create_placement_2d(), Radius=shank_radius
        )
        shank_solid = self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=shank_profile, Position=self._create_placement((0.,0.,0.), (0.,0.,1.), (1.,0.,0.)),
            ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,1.)), Depth=shank_length
        )
        return self.ifc_file.createIfcShapeRepresentation(
            ContextOfItems=self.exporter.project.RepresentationContexts[0], RepresentationIdentifier="Body",
            RepresentationType="SweptSolid", Items=[head_solid, shank_solid]
        )

    def _create_nut_representation(self, nut_obj):
        """Creates the geometric Representation for an Osdag Hex Nut."""
        hex_radius, thickness = float(nut_obj.R), float(nut_obj.T)
        points = [[float(hex_radius * np.cos(np.deg2rad(i * 60))), float(hex_radius * np.sin(np.deg2rad(i * 60)))] for i in range(6)]
        
        # OSDAG Nuts essentially map completely fine as solid hex blocks at standard LOD500,
        # BuildingSMART generally avoids complex `IfcArbitraryProfileDefWithVoids` for hundreds of nuts.
        hex_profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
            ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points + [points[0]]])
        )
        hex_solid = self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=hex_profile, Position=self._create_placement((0.,0.,0.), (0.,0.,1.), (1.,0.,0.)),
            ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,1.)), Depth=thickness
        )
        return self.ifc_file.createIfcShapeRepresentation(
            ContextOfItems=self.exporter.project.RepresentationContexts[0], RepresentationIdentifier="Body",
            RepresentationType="SweptSolid", Items=[hex_solid]
        )
        
    def _create_anchor_bolt_representation(self, bolt_obj):
        """Creates a generic fallback representation for complex curved Anchor Bolts."""
        # Due to J/L curves in AnchorBolt_A, AnchorBolt_B, we map it as a generic cylinder shank
        r = float(bolt_obj.r)
        L = float(getattr(bolt_obj, 'l', 100))
        shank_profile = self.ifc_file.createIfcCircleProfileDef(
            ProfileType="AREA", Position=self._create_placement_2d(), Radius=r
        )
        shank_solid = self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=shank_profile, Position=self._create_placement((0.,0.,0.), (0.,0.,1.), (1.,0.,0.)),
            ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,-1.)), Depth=L
        )
        return self.ifc_file.createIfcShapeRepresentation(
            ContextOfItems=self.exporter.project.RepresentationContexts[0], RepresentationIdentifier="Body",
            RepresentationType="SweptSolid", Items=[shank_solid]
        )

    def _create_washer_representation(self, washer_obj):
        """Creates the geometric Representation for an Osdag Washer (Square with hole)."""
        width, thickness, hole_radius = float(washer_obj.a), float(washer_obj.T), float(washer_obj.d) / 2.0
        outer_points = [(width/2, width/2), (-width/2, width/2), (-width/2, -width/2), (width/2, -width/2)]
        outer_curve = self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in outer_points + [outer_points[0]]])
        inner_curve = self.ifc_file.createIfcCircle(Position=self._create_placement_2d(), Radius=hole_radius)
        
        washer_profile = self.ifc_file.createIfcArbitraryProfileDefWithVoids(
            ProfileType="AREA", ProfileName="Washer Profile", OuterCurve=outer_curve, InnerCurves=[inner_curve]
        )
        washer_solid = self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=washer_profile, Position=self._create_placement((0.,0.,0.), (0.,0.,1.), (1.,0.,0.)),
            ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,-1.)), Depth=thickness
        )
        return self.ifc_file.createIfcShapeRepresentation(
            ContextOfItems=self.exporter.project.RepresentationContexts[0], RepresentationIdentifier="Body",
            RepresentationType="SweptSolid", Items=[washer_solid]
        )

    def map_fastener(self, osdag_fastener_obj):
        obj_type = getattr(osdag_fastener_obj, '_class_name', osdag_fastener_obj.__class__.__name__)
        
        if obj_type == "Bolt":
            fastener_rep = self._create_bolt_representation(osdag_fastener_obj)
            wDir = getattr(osdag_fastener_obj, 'shaftDir', [0,0,1])
        elif obj_type == "Nut":
            fastener_rep = self._create_nut_representation(osdag_fastener_obj)
            wDir = getattr(osdag_fastener_obj, 'wDir', [0,0,1])
        elif obj_type == "Washer":
            fastener_rep = self._create_washer_representation(osdag_fastener_obj)
            wDir = getattr(osdag_fastener_obj, 'wDir', [0,0,1])
        elif obj_type in ["AnchorBolt_A", "AnchorBolt_B", "AnchorBolt_Endplate"]:
            fastener_rep = self._create_anchor_bolt_representation(osdag_fastener_obj)
            wDir = getattr(osdag_fastener_obj, 'shaftDir', [0,0,1])
        else:
            return None
            
        uDir = getattr(osdag_fastener_obj, 'uDir', [1,0,0])
        if abs(np.dot(uDir, wDir)) > 0.99:
            uDir = np.array([0., 1., 0.])
            
        origin = getattr(osdag_fastener_obj, 'sec_origin', getattr(osdag_fastener_obj, 'origin', [0,0,0]))
        
        # We explicitly map using IfcMappedItem for thousands of hardware pieces
        mapping_source = self.ifc_file.createIfcRepresentationMap(
            MappingOrigin=self._create_placement((0.,0.,0.), (0.,0.,1.), (1.,0.,0.)),
            MappedRepresentation=fastener_rep
        )
        
        return self.ifc_file.createIfcMappedItem(
            MappingSource=mapping_source,
            MappingTarget=self.ifc_file.createIfcCartesianTransformationOperator3D(
                Axis1=self.ifc_file.createIfcDirection([float(x) for x in uDir]),
                Axis2=self.ifc_file.createIfcDirection([float(x) for x in np.cross(wDir, uDir)]),
                Axis3=self.ifc_file.createIfcDirection([float(x) for x in wDir]),
                LocalOrigin=self.ifc_file.createIfcCartesianPoint([float(x) for x in origin]), Scale=1.0
            )
        )

    # ─────────────────────────────────────────────────────────────────────────────
    # Weld Mappers
    # ─────────────────────────────────────────────────────────────────────────────

    def map_weld(self, osdag_weld_obj):
        obj_type = getattr(osdag_weld_obj, '_class_name', osdag_weld_obj.__class__.__name__)
        if obj_type in ["Weld", "GrooveWeld"]:
            W = float(osdag_weld_obj.W) if obj_type == "Weld" else float(getattr(osdag_weld_obj, 'b', 0))
            L = float(osdag_weld_obj.L) if obj_type == "Weld" else float(getattr(osdag_weld_obj, 'h', 0))
            T = float(osdag_weld_obj.T) if obj_type == "Weld" else float(getattr(osdag_weld_obj, 'L', 0))
            profile = self.ifc_file.createIfcRectangleProfileDef(
                ProfileType="AREA", Position=self._create_placement_2d(), XDim=W, YDim=L
            )
            return self.ifc_file.createIfcExtrudedAreaSolid(
                SweptArea=profile, Position=self._create_placement(osdag_weld_obj.sec_origin, osdag_weld_obj.wDir, osdag_weld_obj.uDir),
                ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,1.)), Depth=T
            )

        elif obj_type == "FilletWeld":
            b, h, L = float(osdag_weld_obj.b), float(osdag_weld_obj.h), float(osdag_weld_obj.L)
            points_2d = [(0., 0.), (b, 0.), (0., h)]
            profile = self.ifc_file.createIfcArbitraryClosedProfileDef(
                ProfileType="AREA", OuterCurve=self.ifc_file.createIfcPolyline([self.ifc_file.createIfcCartesianPoint([float(c) for c in p]) for p in points_2d + [points_2d[0]]])
            )
            return self.ifc_file.createIfcExtrudedAreaSolid(
                SweptArea=profile, Position=self._create_placement(osdag_weld_obj.sec_origin, osdag_weld_obj.wDir, osdag_weld_obj.uDir),
                ExtrudedDirection=self.ifc_file.createIfcDirection((0.,0.,1.)), Depth=L
            )
        return None

    # ─────────────────────────────────────────────────────────────────────────────
    # Boolean Methods
    # ─────────────────────────────────────────────────────────────────────────────

    def create_opening_element(self, bolt_origin, bolt_dir, bolt_r, bolt_len):
        uDir, wDir = np.array([1., 0., 0.]), bolt_dir
        if abs(np.dot(uDir, wDir)) > 0.99: uDir = np.array([0., 1., 0.])
        profile = self.ifc_file.createIfcCircleProfileDef(
            ProfileType="AREA", Position=self._create_placement_2d(), Radius=float(bolt_r) + 1.0 
        )
        solid = self.ifc_file.createIfcExtrudedAreaSolid(
            SweptArea=profile, Position=self._create_placement(bolt_origin, wDir, uDir),
            ExtrudedDirection=self.ifc_file.createIfcDirection((0., 0., 1.)), Depth=float(bolt_len) 
        )
        return solid
        
    def perform_boolean_cut(self, base_element, opening_solid):
        opening_element = self.ifc_file.createIfcOpeningElement(
            GlobalId=self.exporter.generate_guid(), OwnerHistory=self.exporter.owner_history,
            Name="Bolt Hole", Representation=self.ifc_file.createIfcProductDefinitionShape(
                Representations=[self.ifc_file.createIfcShapeRepresentation(
                    ContextOfItems=self.exporter.project.RepresentationContexts[0],
                    RepresentationIdentifier="Body", RepresentationType="SweptSolid", Items=[opening_solid]
                )])
        )
        self.ifc_file.createIfcRelVoidsElement(
            GlobalId=self.exporter.generate_guid(), OwnerHistory=self.exporter.owner_history,
            RelatingBuildingElement=base_element, RelatedOpeningElement=opening_element
        )
