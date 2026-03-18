import ifcopenshell
import ifcopenshell.guid
import uuid
import time

class OsdagIfcExporter:
    """
    Main generator class for exporting Osdag 3D models to IFC format.
    Maintains the file structure, project hierarchy, and orchestrates the mappers.
    """

    def __init__(self, filename="Osdag_Model.ifc", schema="IFC2X3"):
        """
        Initialize the IFC exporter.
        :param filename: Output path for the IFC file.
        :param schema: IFC schema to use ('IFC2X3' or 'IFC4').
        """
        self.filename = filename
        self.schema = schema
        
        # Initialize an empty IFC file with the chosen schema
        self.ifc_file = ifcopenshell.file(schema=self.schema)
        
        # IFC Header Setup
        self.setup_header()
        
        # Initialize Project Hierarchy
        self.project = None
        self.site = None
        self.building = None
        self.storey = None
        self.setup_project_hierarchy()
        
        # Initialize Mappers
        from .geometry_mapper import GeometryMapper
        from .metadata_mapper import MetadataMapper
        self.geom_mapper = GeometryMapper(self)
        self.meta_mapper = MetadataMapper(self)

    def generate_guid(self, osdag_id=None):
        """
        Generates a 22-character IFC standard GUID.
        If an osdag_id is provided, it can be used to generate a deterministic GUID.
        """
        if osdag_id is not None:
            # Deterministic GUID based on the element's unique Osdag ID
            # Use uuid5 with a namespace to consistently get the same uuid for the same ID
            namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
            element_uuid = uuid.uuid5(namespace, str(osdag_id))
            # Pack uuid to IFC base64
            guid = ifcopenshell.guid.compress(element_uuid.hex)
        else:
            # Random GUID
            guid = ifcopenshell.guid.new()
        return guid

    def setup_header(self):
        """Set up the IFC file header metadata."""
        owner_history = self.ifc_file.createIfcOwnerHistory()
        # To be populated fully in metadata_mapper if needed, but a basic one is required
        # IfcPerson: IFC2X3 uses 'Id', IFC4 renamed it to 'Identification'
        if self.schema == "IFC4":
            person = self.ifc_file.createIfcPerson(
                Identification="OsdagUser", FamilyName="User"
            )
            org = self.ifc_file.createIfcOrganization(
                Identification="Osdag", Name="Osdag"
            )
        else:  # IFC2X3
            person = self.ifc_file.createIfcPerson(
                Id="OsdagUser", FamilyName="User"
            )
            org = self.ifc_file.createIfcOrganization(
                Id="Osdag", Name="Osdag"
            )
        person_and_org = self.ifc_file.createIfcPersonAndOrganization(ThePerson=person, TheOrganization=org)
        
        app = self.ifc_file.createIfcApplication(
            ApplicationDeveloper=org,
            Version="1.0",
            ApplicationFullName="Osdag Structural Design",
            ApplicationIdentifier="OSDAG"
        )
        
        self.owner_history = self.ifc_file.createIfcOwnerHistory(
            OwningUser=person_and_org,
            OwningApplication=app,
            ChangeAction="ADDED",
            CreationDate=int(time.time())
        )

    def setup_project_hierarchy(self):
        """Create the Project -> Site -> Building -> Storey hierarchy."""
        
        # Create Units
        length_unit = self.ifc_file.createIfcSIUnit(
            UnitType="LENGTHUNIT",
            Prefix="MILLI",
            Name="METRE"
        )
        angle_unit = self.ifc_file.createIfcSIUnit(
            UnitType="PLANEANGLEUNIT",
            Name="RADIAN"
        )
        unit_assignment = self.ifc_file.createIfcUnitAssignment(
            Units=[length_unit, angle_unit]
        )
        
        # Create Project
        self.project = self.ifc_file.createIfcProject(
            GlobalId=self.generate_guid("osdag_project"),
            OwnerHistory=self.owner_history,
            Name="Osdag Connection Design",
            RepresentationContexts=self._create_contexts(),
            UnitsInContext=unit_assignment
        )
        
        # Create Site
        self.site = self.ifc_file.createIfcSite(
            GlobalId=self.generate_guid("osdag_site"),
            OwnerHistory=self.owner_history,
            Name="Site",
            CompositionType="COMPLEX"
        )
        self.ifc_file.createIfcRelAggregates(
            GlobalId=self.generate_guid(),
            OwnerHistory=self.owner_history,
            RelatingObject=self.project,
            RelatedObjects=[self.site]
        )
        
        # Create Building
        self.building = self.ifc_file.createIfcBuilding(
            GlobalId=self.generate_guid("osdag_building"),
            OwnerHistory=self.owner_history,
            Name="Building",
            CompositionType="COMPLEX"
        )
        self.ifc_file.createIfcRelAggregates(
            GlobalId=self.generate_guid(),
            OwnerHistory=self.owner_history,
            RelatingObject=self.site,
            RelatedObjects=[self.building]
        )
        
        # Create Storey
        self.storey = self.ifc_file.createIfcBuildingStorey(
            GlobalId=self.generate_guid("osdag_storey"),
            OwnerHistory=self.owner_history,
            Name="Level 1",
            CompositionType="COMPLEX",
            Elevation=0.0
        )
        self.ifc_file.createIfcRelAggregates(
            GlobalId=self.generate_guid(),
            OwnerHistory=self.owner_history,
            RelatingObject=self.building,
            RelatedObjects=[self.storey]
        )

    def _create_contexts(self):
        """Creates representation contexts for 3D modeling."""
        # 3D Context
        context3d = self.ifc_file.createIfcGeometricRepresentationContext(
            ContextType="Model",
            CoordinateSpaceDimension=3,
            Precision=1e-5,
            WorldCoordinateSystem=self._create_placement(),
            TrueNorth=self._create_direction((0.0, 1.0, 0.0))
        )
        return [context3d]

    def _create_placement(self, point=(0.0, 0.0, 0.0), dir_z=(0.0, 0.0, 1.0), dir_x=(1.0, 0.0, 0.0)):
        """Helper to create Local Placement."""
        point_ifc = self.ifc_file.createIfcCartesianPoint(list(point))
        axis = self.ifc_file.createIfcDirection(list(dir_z))
        ref_dir = self.ifc_file.createIfcDirection(list(dir_x))
        axis2placement = self.ifc_file.createIfcAxis2Placement3D(Location=point_ifc, Axis=axis, RefDirection=ref_dir)
        return axis2placement

    def _create_direction(self, dir_tuple):
        """Helper to create a direction."""
        return self.ifc_file.createIfcDirection(list(dir_tuple))

    def save(self):
        """Save the IFC file to disk."""
        self.ifc_file.write(self.filename)
        print(f"IFC file successfully saved to {self.filename}")

    def export_connection(self, connection_id, members, plates, bolts, welds=None, metadata=None, others=None):
        """
        Orchestrates the export of an entire Osdag structural connection.
        
        :param connection_id: Unique string identifier for the connection
        :param members: List of Osdag parameterized section objects (e.g. ISection, RHS)
        :param plates: List of Osdag Plate objects
        :param bolts: List of Osdag Bolt/Nut/Washer objects
        :param welds: Optional list of Osdag Weld objects
        :param metadata: Optional dictionary containing design loads, status and material metadata
        :param others: Optional list of non-steel elements (Civil foundation, Grout, etc.)
        """
        print(f"Starting IFC LOD 500 export for connection: {connection_id}")
        
        ifc_elements = []

        # 1. Map Members (Beams, Columns)
        for member in members:
            solid = self.geom_mapper.map_extruded_solid(member)
            if solid:
                # Determine element type
                m_name = getattr(member, 'ifc_name', 'Steel Member')
                if 'Column' in m_name:
                    ifc_element = self.ifc_file.createIfcColumn(
                        GlobalId=self.generate_guid(),
                        OwnerHistory=self.owner_history,
                        Name=m_name,
                        Representation=self._create_shape_representation(solid)
                    )
                else: 
                    ifc_element = self.ifc_file.createIfcBeam(
                        GlobalId=self.generate_guid(),
                        OwnerHistory=self.owner_history,
                        Name=m_name,
                        Representation=self._create_shape_representation(solid)
                    )
                self.meta_mapper.assign_osdag_design_data(ifc_element, member)
                ifc_elements.append(ifc_element)
                
        # 2. Map Plates & Apply Boolean Cuts from Bolts
        for plate in plates:
            plate_solid = self.geom_mapper.map_extruded_solid(plate)
            if not plate_solid:
                continue
                
            ifc_plate = self.ifc_file.createIfcPlate(
                GlobalId=self.generate_guid(),
                OwnerHistory=self.owner_history,
                Name=getattr(plate, 'ifc_name', "Connection Plate"),
                Representation=self._create_shape_representation(plate_solid)
            )
            
            # Apply exact boolean cuts for every bolt passing through (LOD 500)
            for fastener in bolts:
                if fastener.__class__.__name__ == 'Bolt':
                    try:
                        origin = getattr(fastener, 'origin', None) or getattr(fastener, 'sec_origin', None)
                        shaft_dir = getattr(fastener, 'shaftDir', None) or getattr(fastener, 'uDir', None)
                        R = getattr(fastener, 'R', None)
                        H = getattr(fastener, 'H', None)
                        if origin is not None and shaft_dir is not None and R is not None and H is not None:
                            opening = self.geom_mapper.create_opening_element(origin, shaft_dir, R, H)
                            self.geom_mapper.perform_boolean_cut(ifc_plate, opening)
                    except Exception:
                        pass
                
            self.meta_mapper.assign_osdag_design_data(ifc_plate, plate)
            ifc_elements.append(ifc_plate)

        # 3. Map Fasteners (Bolts, Nuts, Washers) via Instancing
        for bolt in bolts:
            mapped_item = self.geom_mapper.map_fastener(bolt)
            if mapped_item:
                ifc_fastener = self.ifc_file.createIfcFastener(
                    GlobalId=self.generate_guid(),
                    OwnerHistory=self.owner_history,
                    Name="Bolt Assembly",
                    Representation=self._create_shape_representation(mapped_item, rep_type="MappedRepresentation")
                )
                ifc_elements.append(ifc_fastener)

        # 4. Map Welds as Fasteners
        if welds:
            for weld in welds:
                weld_solid = self.geom_mapper.map_weld(weld)
                if weld_solid:
                    ifc_weld = self.ifc_file.createIfcFastener(
                        GlobalId=self.generate_guid(),
                        OwnerHistory=self.owner_history,
                        Name=getattr(weld, 'designation', 'Weld Joint'),
                        ObjectType="WELD",
                        Representation=self._create_shape_representation(weld_solid, rep_type="SweptSolid")
                    )
                    self.meta_mapper.assign_osdag_design_data(ifc_weld, weld)
                    ifc_elements.append(ifc_weld)

        # 5. Map Others (Concrete, Grout) as BuildingElementProxies
        if others:
            for other_item in others:
                other_solid = self.geom_mapper.map_extruded_solid(other_item)
                if other_solid:
                    name = getattr(other_item, '_class_name', other_item.__class__.__name__)
                    ifc_other = self.ifc_file.createIfcBuildingElementProxy(
                        GlobalId=self.generate_guid(),
                        OwnerHistory=self.owner_history,
                        Name=name,
                        Representation=self._create_shape_representation(other_solid, rep_type="SweptSolid")
                    )
                    ifc_elements.append(ifc_other)

        # 6. Group all elements into an IfcElementAssembly and link to Storey
        assembly = self.meta_mapper.create_element_assembly(f"Connection_{connection_id}", ifc_elements)
        
        # Attach the non-geometric structural design metadata to the Root Assembly
        if metadata:
            self.meta_mapper.assign_standard_pset(assembly, "Pset_OsdagDesignData", metadata)
        
        self.ifc_file.createIfcRelContainedInSpatialStructure(
            GlobalId=self.generate_guid(),
            OwnerHistory=self.owner_history,
            RelatingStructure=self.storey,
            RelatedElements=[assembly]
        )
        
        print("Export orchestration completed.")

    def _create_shape_representation(self, geometric_item, rep_type="SweptSolid"):
        """Helper to wrap a solid/mapped item in an IfcProductDefinitionShape."""
        rep = self.ifc_file.createIfcShapeRepresentation(
            ContextOfItems=self.project.RepresentationContexts[0],
            RepresentationIdentifier="Body",
            RepresentationType=rep_type,
            Items=[geometric_item]
        )
        return self.ifc_file.createIfcProductDefinitionShape(Representations=[rep])
