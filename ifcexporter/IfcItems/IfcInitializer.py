import os
import glob
import time 
import json
import tempfile
import numpy as np
import ifcopenshell as ifcops
import ifcopenshell.geom as ifcgeom
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools

# GLOBAL

O = (0., 0., 0.)
X = (1., 0., 0.)
Y = (0., 1., 0.)
Z = (0., 0., 1.)

i = np.array([1,0,0])
j = np.array([0,1,0])
k = np.array([0,0,1])

def temp_brep(prism, name):
    fname = "ifcexporter/Temp/" + name + ".brep"
    breptools.Write(prism, fname)

#MAIN class

class IfcObject():
    def __init__(self, ifcfile = None, **kwgs):
        if ifcfile == None:
            self.create_ifcfile(**kwgs)
        else:
            self.ifcfile = ifcfile
            self.extract_data_from_ifctemplate()

    def create_ifcfile(self, **kwgs):
        self.time = time.time()
        self.CONFIG = {
            "filename": "Default" + ".ifc",
            "timestamp": self.time,
            "timestring": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.time)),
            "creator": "Mukunth A G",
            "organization": "IIT Bombay",
            "application": "IfcOpenShell", 
            "application_version": "0.7.0-1b1fd1e6",
            "project_globalid": ifcops.guid.new(), 
            "project_name": "Project Osdag",
        }
        self.CONFIG.update(kwgs)
        locals().update(self.CONFIG)

        self.template = """ISO-10303-21;
        HEADER;
        FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
        FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
        FILE_SCHEMA(('IFC2X3'));
        ENDSEC;
        DATA;
        #1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
        #2=IFCORGANIZATION($,'%(organization)s',$,$,$);
        #3=IFCPERSONANDORGANIZATION(#1,#2,$);
        #4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
        #5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
        #6=IFCDIRECTION((1.,0.,0.));
        #7=IFCDIRECTION((0.,1.,0.));
        #8=IFCDIRECTION((0.,0.,1.));
        #9=IFCCARTESIANPOINT((0.,0.,0.));
        #10=IFCAXIS2PLACEMENT3D(#9,#8,#6);
        #11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#10,#7);
        #12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
        #13=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
        #14=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
        #15=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
        #16=IFCSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);
        #17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
        #18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
        #19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
        #20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
        ENDSEC;
        END-ISO-10303-21;
        """ % locals()

        self.ifcfile = self.make_file()
        self.extract_data_from_ifctemplate()
        self.create_initial_heirarchy()
    
    def make_file(self):
        _, temp_filename = tempfile.mkstemp(suffix=".ifc")
        with open(temp_filename, "w") as f:
            f.write(self.template)
        ifcfile = ifcops.open(temp_filename)
        return ifcfile 
    
    def extract_data_from_ifctemplate(self):
        self.owner_history = self.ifcfile.by_id(5)
        self.Xdir = self.ifcfile.by_id(6)
        self.Ydir = self.ifcfile.by_id(7)
        self.Zdir = self.ifcfile.by_id(8)
        self.ori = self.ifcfile.by_id(9)
        self.g_placement = self.ifcfile.by_id(10)
        self.context = self.ifcfile.by_id(11)
        self.project = self.ifcfile.by_id(20)

    def create_initial_heirarchy(self):
        self.create_ifcsite()
        self.create_ifcbuilding()
        self.create_ifcbuildingstorey()
        self.create_ifcrelaggregates()
    
    def create_ifcsite(self):
        self.site_placement = self.ifcfile.createIfcLocalPlacement(PlacementRelTo = None, RelativePlacement = self.g_placement)
        self.site_data = {
            "GlobalId": self.guid(),
            "OwnerHistory": self.owner_history,
            "Name": "Site",
            "ObjectPlacement": self.site_placement,
            "CompositionType": "ELEMENT"
        }
        self.site = self.ifcfile.createIfcSite(**self.site_data)

    def create_ifcbuilding(self):
        self.building_placement = self.ifcfile.createIfcLocalPlacement(PlacementRelTo = self.site_placement)
        self.building_data = {
            "GlobalId": self.guid(),
            "OwnerHistory": self.owner_history,
            "Name": "Building",
            "CompositionType": "ELEMENT"
        }
        self.building = self.ifcfile.createIfcBuilding(**self.building_data)

    def create_ifcbuildingstorey(self, elevation = 0, name = "Ground", description = "Ground Level"):
        self.ground_storey_placement = self.ifcfile.createIfcLocalPlacement(PlacementRelTo = self.building_placement)
        self.buildingstorey_data = {
            "GlobalId": self.guid(),
            "OwnerHistory": self.owner_history,
            "Name": name,
            "Description": description,
            "CompositionType": "ELEMENT",
            "Elevation": elevation
        }
        self.ground_storey = self.ifcfile.createIfcBuildingStorey(**self.buildingstorey_data)
        self.ifcfile.ground_storey_placement = self.ground_storey_placement
        self.ifcfile.ground_storey = self.ground_storey

    def create_ifcrelaggregates(self):
        self.ifcfile.createIfcRelAggregates(self.guid(), self.owner_history, "Building Container", "Ground level to Building", self.building, [self.ground_storey])
        self.ifcfile.createIfcRelAggregates(self.guid(), self.owner_history, "Site Container", "Building to Site", self.site, [self.building])
        self.ifcfile.createIfcRelAggregates(self.guid(), self.owner_history, "Project Container", "Site to Project", self.project, [self.site])
    
    def create_ifcpoint(self, point):
        point = self.to_tuple(point)
        if point == O:
            point = self.ori
        else:
            point = self.ifcfile.createIfcCartesianPoint(point)
        return point
    
    def create_ifcdir(self, dir):
        dir = self.to_tuple(dir)
        if dir == X: 
            dir = self.Xdir
        elif dir == Y: 
            dir = self.Ydir
        elif dir == Z: 
            dir = self.Zdir
        else:
            dir = self.ifcfile.createIfcDirection(dir)
        return dir

    def create_ifcaxis2placement(self, point = O, uDir = X, wDir = Z):
        point = self.create_ifcpoint(point)
        wDir = self.create_ifcdir(wDir)
        uDir = self.create_ifcdir(uDir)
        axis2placement = self.ifcfile.createIfcAxis2Placement3D(point, wDir, uDir)
        return axis2placement

    def create_ifclocalplacement(self, point = O, uDir = X, wDir = Z, relative_to = None):
        axis2placement = self.create_ifcaxis2placement(point, uDir, wDir)
        ifclocalplacement2 = self.ifcfile.createIfcLocalPlacement(relative_to, axis2placement)
        return ifclocalplacement2

    def create_ifcpolyline(self,  point_list):
        ifcpts = []
        for point in point_list:
            point = self.create_ifcpoint(point)
            ifcpts.append(point)
        polyline = self.ifcfile.createIfcPolyLine(ifcpts)
        return polyline

    def create_ifcarbitraryclosedprofiledef(self,  point_list, name = None):
        polyline = self.create_ifcpolyline(point_list)
        ifcclosedprofile = self.ifcfile.createIfcArbitraryClosedProfileDef("AREA", name, polyline)
        return ifcclosedprofile

    def create_product_representation(self, extruded_body):
        shape_representation = self.ifcfile.createIfcShapeRepresentation(self.context, "Body", "SweptSolid", [extruded_body])
        product_representation = self.ifcfile.createIfcProductDefinitionShape(Representations = [shape_representation])
        return product_representation

    def place(self, location = [O, X, Z], relative_to = None):
        if relative_to == None:
            relative_to = self.ground_storey_placement
        point = location[0]
        uDir = location[1]
        wDir = location[2]
        return self.create_ifclocalplacement(point, uDir, wDir, relative_to)
    
    def place_ifcelement_in_storey(self, ifcelement, storey):
        params = {
            "GlobalId": self.guid(),
            "OwnerHistory": self.owner_history,
            "RelatedElements": [ifcelement],
            "RelatingStructure": storey
        }
        self.ifcfile.createIfcRelContainedInSpatialStructure(**params)

    def assign_storey(self, ifcobj, storey):
        if storey == None:
            self.place_ifcelement_in_storey(ifcobj, self.ifcfile.ground_storey)
        else:
            self.place_ifcelement_in_storey(ifcobj, storey)

    def assign_Pset(self, ifcobj, Pset_name, props):
        ifc_prop_single_values = []
        for k, v in props.items():
            v = str(v)
            psv = self.ifcfile.createIfcPropertySingleValue(k, None, self.ifcfile.createIfcText(v), None)
            ifc_prop_single_values.append(psv)
        Pset = self.ifcfile.createIfcPropertySet(
            self.guid(), 
            self.owner_history,
            Pset_name,
            None,
            ifc_prop_single_values
        )
        self.ifcfile.createIfcRelDefinesByProperties(
            self.guid(), 
            self.owner_history,
            None,
            None,
            [ifcobj],
            Pset
        )
    
    def write_ifcfile(self, directory = "Samples"):
        """
        Only for testing, use ifc_write_to_path instead
        """
        filename = self.CONFIG.get("filename")
        self.ifcfile.write(directory + "/" + filename)
    
    def ifc_write_to_path(self, path):
        self.ifcfile.write(path)

    def display_ifc_geometry(self):
        ifcgeom.utils.initialize_display()
        settings = ifcgeom.settings(USE_PYTHON_OPENCASCADE=True)
        for item in ifcgeom.iterate(
            settings, self.ifcfile, exclude=["IfcSpace", "IfcOpeningElement"]
        ):
            ifcgeom.utils.display_shape(item)
        ifcgeom.utils.main_loop()
        
    def clear_Temp(self):
        files = glob.glob('ifcexporter/Temp/*')
        for f in files:
            os.remove(f)
    
    def read_brep(self, fname):
        shape = TopoDS_Shape()
        builder = BRep_Builder()
        breptools.Read(shape, fname, builder)
        return shape
    
    def get_rep(self, name):
        fname = "ifcexporter/Temp/" + name + ".brep"
        shape = self.read_brep(fname)
        representation = ifcgeom.tesselate(self.ifcfile.schema, shape, 1.)
        self.ifcfile.add(representation)
        return representation

    def guid(self):
        return ifcops.guid.new()
    
    def ifc2np(self, ifcpoint):
        return np.array(ifcpoint)[0]

    def to_tuple(self, ifc_or_np):
        if isinstance(ifc_or_np, ifcops.entity_instance):
            ifc_or_np = self.ifc2np(ifc_or_np)
        tup = tuple([float(e) for e in ifc_or_np])
        return tup