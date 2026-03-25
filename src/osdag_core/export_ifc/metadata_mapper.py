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

    def assign_standard_qto(self, ifc_element, qto_name, quantities_dict):
        """
        Creates and assigns an IfcElementQuantity set for BOQ extraction.
        """
        quantities = []
        for name, data in quantities_dict.items():
            qty_type = data.get('type')
            val = float(data.get('value', 0.0))
            if qty_type == 'Length':
                qty = self.ifc_file.createIfcQuantityLength(name, name, None, val, None) if self.exporter.schema == "IFC4" else self.ifc_file.createIfcQuantityLength(name, name, None, val)
            elif qty_type == 'Area':
                qty = self.ifc_file.createIfcQuantityArea(name, name, None, val, None) if self.exporter.schema == "IFC4" else self.ifc_file.createIfcQuantityArea(name, name, None, val)
            elif qty_type == 'Volume':
                qty = self.ifc_file.createIfcQuantityVolume(name, name, None, val, None) if self.exporter.schema == "IFC4" else self.ifc_file.createIfcQuantityVolume(name, name, None, val)
            elif qty_type == 'Weight':
                qty = self.ifc_file.createIfcQuantityWeight(name, name, None, val, None) if self.exporter.schema == "IFC4" else self.ifc_file.createIfcQuantityWeight(name, name, None, val)
            elif qty_type == 'Count':
                qty = self.ifc_file.createIfcQuantityCount(name, name, None, int(val), None) if self.exporter.schema == "IFC4" else self.ifc_file.createIfcQuantityCount(name, name, None, int(val))
            else:
                continue
            quantities.append(qty)

        if not quantities: return None

        element_qty = self.ifc_file.createIfcElementQuantity(
            GlobalId=self.exporter.generate_guid(),
            OwnerHistory=self.exporter.owner_history,
            Name=qto_name,
            MethodOfMeasurement="Custom",
            Quantities=quantities
        )

        self.ifc_file.createIfcRelDefinesByProperties(
            GlobalId=self.exporter.generate_guid(),
            OwnerHistory=self.exporter.owner_history,
            RelatingPropertyDefinition=element_qty,
            RelatedObjects=[ifc_element]
        )
        return element_qty

    def assign_member_boq(self, ifc_element, osdag_obj, metadata=None):
        common_props = {}
        if hasattr(osdag_obj, 'material'): common_props['Material'] = str(osdag_obj.material)
        
        designation = str(getattr(osdag_obj, 'designation', '')).strip()
        
        # Fallback to the global metadata dictionary if the model geometry string was scrubbed
        if not designation and metadata:
            name = getattr(osdag_obj, 'ifc_name', '')
            if 'Column' in name:
                designation = metadata.get('Supporting_Profile') or metadata.get('Column_Profile') or metadata.get('Profile') or metadata.get('Section_Profile', '')
            else:
                designation = metadata.get('Supported_Profile') or metadata.get('Beam_Profile') or metadata.get('Profile') or metadata.get('Section_Profile', '')
                
        if designation: common_props['Reference'] = designation
        if common_props: self.assign_standard_pset(ifc_element, "Pset_BeamCommon", common_props)

        qto = {}
        length = float(getattr(osdag_obj, 'length', getattr(osdag_obj, 'L', getattr(osdag_obj, 'H', 0))))
        if length > 0: qto['Length'] = {'type': 'Length', 'value': length}
        
        area = 0.0
        mass_per_m = 0.0
        
        # Phase 2: Native Database Extraction
        if designation:
            try:
                from .database_connector import fetch_profile_data
                db_data = fetch_profile_data(designation, getattr(osdag_obj, '_class_name', ''))
                if db_data:
                    area = float(db_data.get('Area', 0)) * 100  # DB Area is in cm^2, convert to mm^2
                    mass_per_m = float(db_data.get('Mass', 0))
            except ImportError:
                pass


        if area > 0:
            qto['CrossSectionArea'] = {'type': 'Area', 'value': area / 1e6}
            vol = (area * length) / 1e9
            qto['NetVolume'] = {'type': 'Volume', 'value': vol}
            
            if mass_per_m > 0:
                qto['NetWeight'] = {'type': 'Weight', 'value': mass_per_m * (length / 1000.0)}
            else:
                qto['NetWeight'] = {'type': 'Weight', 'value': vol * 7850}
            
        if qto: self.assign_standard_qto(ifc_element, "Qto_BeamBaseQuantities", qto)

    def assign_plate_boq(self, ifc_element, osdag_obj):
        common_props = {}
        if hasattr(osdag_obj, 'material'): common_props['Material'] = str(osdag_obj.material)
        if common_props: self.assign_standard_pset(ifc_element, "Pset_PlateCommon", common_props)

        qto = {}
        # Robustly discover plate dimensions by gathering all possible length/width attributes
        dim_candidates = []
        for attr in ['L', 'length', 'W', 'width', 'H', 'height', 'B', 'Hst', 'Lst', 'A']:
            val = float(getattr(osdag_obj, attr, 0))
            if val > 0: dim_candidates.append(val)
            
        dim_candidates.sort(reverse=True)
        L = dim_candidates[0] if len(dim_candidates) > 0 else 0
        W = dim_candidates[1] if len(dim_candidates) > 1 else L
        
        T = float(getattr(osdag_obj, 'T', getattr(osdag_obj, 't', getattr(osdag_obj, 'thickness', getattr(osdag_obj, 'Tst', getattr(osdag_obj, 'tw', 0))))))
        
        if L > 0: qto['Length'] = {'type': 'Length', 'value': L}
        if W > 0: qto['Width'] = {'type': 'Length', 'value': W}
        if T > 0: qto['Depth'] = {'type': 'Length', 'value': T}
        
        area = L * W
        
        obj_class = getattr(osdag_obj, '_class_name', '')
        try:
            if obj_class == "GassetPlate":
                g_L = float(getattr(osdag_obj, 'L', 0))
                g_H = float(getattr(osdag_obj, 'H', 0))
                degree = float(getattr(osdag_obj, 'degree', 0))
                import math
                if g_L > 0 and g_H > 0:
                    area = (g_H + g_L * math.tan(math.radians(degree))) * g_L
            elif obj_class == "Stiffener_CAD":
                s_Lst = float(getattr(osdag_obj, 'Lst', 0))
                s_Hst = float(getattr(osdag_obj, 'Hst', 0))
                if s_Lst > 25 and s_Hst > 25:
                    area = (s_Lst * s_Hst) - 0.5 * (s_Lst - 25) * (s_Hst - 25)
        except Exception:
            pass
            
        if area > 0:
            qto['GrossArea'] = {'type': 'Area', 'value': area / 1e6}
            vol = (area * T) / 1e9
            qto['NetVolume'] = {'type': 'Volume', 'value': vol}
            qto['NetWeight'] = {'type': 'Weight', 'value': vol * 7850}
            
        if qto: self.assign_standard_qto(ifc_element, "Qto_PlateBaseQuantities", qto)

    def assign_fastener_boq(self, ifc_element, osdag_obj, fastener_type):
        common_props = {}
        if hasattr(osdag_obj, 'type'): common_props['Type'] = str(osdag_obj.type)
        
        grade = str(getattr(osdag_obj, 'property_class', getattr(osdag_obj, 'grade', '')))
        if grade: common_props['Grade'] = grade
        
        # DB lookup for Bolt fy and fu
        if "Bolt" in fastener_type and grade:
            try:
                from .database_connector import fetch_bolt_data
                db_data = fetch_bolt_data(grade)
                if db_data:
                    if 'fy' in db_data: common_props['YieldStrength'] = float(db_data['fy'])
                    if 'fu' in db_data: common_props['UltimateStrength'] = float(db_data['fu'])
            except ImportError:
                pass

        if common_props: self.assign_standard_pset(ifc_element, "Pset_FastenerCommon", common_props)

        qto = {}
        dia = float(getattr(osdag_obj, 'd', getattr(osdag_obj, 'D', getattr(osdag_obj, 'diameter', 0))))
        length = float(getattr(osdag_obj, 'l', getattr(osdag_obj, 'L', getattr(osdag_obj, 'H', getattr(osdag_obj, 'length', 0)))))
        
        if dia > 0: qto['Diameter'] = {'type': 'Length', 'value': dia}
        if length > 0: qto['Length'] = {'type': 'Length', 'value': length}
        qto['Count'] = {'type': 'Count', 'value': 1}
        
        if "Bolt" in fastener_type and dia > 0 and length > 0:
            import math
            vol = (math.pi * (dia/2)**2 * length) / 1e9
            qto['NetWeight'] = {'type': 'Weight', 'value': vol * 7850}
            
        self.assign_standard_qto(ifc_element, "Qto_FastenerBaseQuantities", qto)

    def assign_weld_boq(self, ifc_element, osdag_obj):
        common_props = {}
        obj_class = getattr(osdag_obj, '_class_name', '')
        if hasattr(osdag_obj, 'type'): 
            common_props['WeldType'] = str(osdag_obj.type)
        else:
            if "Fillet" in obj_class: common_props['WeldType'] = "Fillet"
            elif "Groove" in obj_class: common_props['WeldType'] = "Groove"
        
        if hasattr(osdag_obj, 'strength'): common_props['Grade'] = str(osdag_obj.strength)
        
        if common_props: self.assign_standard_pset(ifc_element, "Pset_WeldCommon", common_props)

        qto = {}
        L = float(getattr(osdag_obj, 'L', getattr(osdag_obj, 'h', getattr(osdag_obj, 'length', 0))))
        size = float(getattr(osdag_obj, 'b', getattr(osdag_obj, 'W', getattr(osdag_obj, 'size', getattr(osdag_obj, 'T', 0)))))
        
        if L > 0: qto['Length'] = {'type': 'Length', 'value': L}
        if size > 0: qto['Depth'] = {'type': 'Length', 'value': size}
        
        if qto: self.assign_standard_qto(ifc_element, "Qto_WeldBaseQuantities", qto)
