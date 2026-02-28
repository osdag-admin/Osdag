import ifcopenshell
import time

class MetadataMapper:
    """
    Handles the attachment of buildingSMART Property Sets (Psets) 
    and custom Osdag Data to IFC entities for LOD 500 lifecycle tracking.
    """
    
    def __init__(self, ifc_exporter):
        """
        :param ifc_exporter: The OsdagIfcExporter instance managing the file.
        """
        self.exporter = ifc_exporter
        self.ifc_file = ifc_exporter.ifc_file

    def assign_standard_pset(self, ifc_element, pset_name, properties_dict):
        """
        Creates and assigns a standard Property Set (e.g., Pset_BeamCommon)
        to the given IFC element.
        """
        properties = []
        for name, value in properties_dict.items():
            if isinstance(value, float):
                prop = self.ifc_file.createIfcPropertySingleValue(name, name, self.ifc_file.createIfcReal(value), None)
            elif isinstance(value, int):
                prop = self.ifc_file.createIfcPropertySingleValue(name, name, self.ifc_file.createIfcInteger(value), None)
            elif isinstance(value, bool):
                prop = self.ifc_file.createIfcPropertySingleValue(name, name, self.ifc_file.createIfcBoolean(value), None)
            else:
                prop = self.ifc_file.createIfcPropertySingleValue(name, name, self.ifc_file.createIfcLabel(str(value)), None)
            properties.append(prop)

        pset = self.ifc_file.createIfcPropertySet(
            GlobalId=self.exporter.generate_guid(),
            OwnerHistory=self.exporter.owner_history,
            Name=pset_name,
            HasProperties=properties
        )

        self.ifc_file.createIfcRelDefinesByProperties(
            GlobalId=self.exporter.generate_guid(),
            OwnerHistory=self.exporter.owner_history,
            RelatingPropertyDefinition=pset,
            RelatedObjects=[ifc_element]
        )
        return pset

    def assign_osdag_design_data(self, ifc_element, osdag_obj, applied_forces=None, capacities=None):
        """
        Extracts structural capacities, forces, and material data from 
        the Osdag underlying object and assigns it to Pset_OsdagDesignData.
        """
        # We simulate extraction by expecting a dictionary or pulling from osdag_obj
        props = {}
        if hasattr(osdag_obj, 'material'):
            props['MaterialGrade'] = str(osdag_obj.material)
        if hasattr(osdag_obj, 'designation'):
            props['SectionProfile'] = str(osdag_obj.designation)
            
        if applied_forces:
            props.update(applied_forces)
        if capacities:
            props.update(capacities)

        props['DesignCode'] = 'IS 800:2007'
        props['ExportTime'] = time.strftime("%Y-%m-%d %H:%M:%S")

        self.assign_standard_pset(ifc_element, "Pset_OsdagDesignData", props)

    def create_element_assembly(self, assembly_name, elements, assembly_type="CONNECTION"):
        """
        Groups multiple IFC elements (e.g., bolts, nuts, plates) 
        into an IfcElementAssembly for spatial hierarchy.
        """
        assembly = self.ifc_file.createIfcElementAssembly(
            GlobalId=self.exporter.generate_guid(),
            OwnerHistory=self.exporter.owner_history,
            Name=assembly_name,
            ObjectType=assembly_type,
            PredefinedType="USERDEFINED"
        )
        
        # Link children elements to the assembly
        self.ifc_file.createIfcRelAggregates(
            GlobalId=self.exporter.generate_guid(),
            OwnerHistory=self.exporter.owner_history,
            RelatingObject=assembly,
            RelatedObjects=elements
        )
        return assembly
