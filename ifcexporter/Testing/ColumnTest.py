from ifcexporter.IfcItems.IfcInitializer import *

class ColumnBase(IfcObject):
    """
    => A square shaped column base of square width "w" and height "h"

    => Creating a Local Coordinate System at (5,5,0) with Pure Translation (see figure below)

        Y
        ^
        |
        |
        |---------------(5.,5.,0.) => ColumnBase's LCS will be placed here
        |               |
        |               |
        |               |
        |               |
        |               |
        |--------------------------- > X  ==> Storey's LCS (Local Coordinate System)

    => Create LCS of base
    
    => Construct base Profile (By Creating another placement for 2D drawing, where IfcRectangleProfile is put to use)
    
    => Extrude base Profile
    
    => Create Product Representation (Here its just the extruded solid body, but this can be combined with some datum plane or axis)
    
    => Assign the product to Ifc element called "IfcColumn" with the created LCS
    
    => Place the IfcColumn in the ground storey
    """

    def __init__(self, base_params, **kwgs):
        super().__init__(**kwgs)

        bp = base_params
        self.base_location = bp.get("base_location")
        self.base_width = bp.get("base_width")
        self.base_height = bp.get("base_height")

        self.base_local_placement = self.create_ifclocalplacement(point = self.base_location, relative_to = self.storey_placement)
        base_profile = self.construct_base_profile2d()
        extruded_base = self.extrude_base_profile(base_profile)
        base_product_representation = self.create_product_representation(extruded_base)
        base_as_ifccolumn = self.base_product_as_ifccolumn(base_product_representation)
        self.place_ifcelement_in_storey(base_as_ifccolumn, self.ground_storey)

    def construct_base_profile2d(self):
        base_profile_placement = self.ifcfile.createIfcAxis2Placement2D(self.ori, self.Xdir)
        base_profile = self.ifcfile.createIfcRectangleProfileDef("AREA", "Column Base Profile", base_profile_placement, self.base_width, self.base_width)
        return base_profile
    
    def extrude_base_profile(self, base_profile):
        extruded_base = self.ifcfile.createIfcExtrudedAreaSolid(base_profile, self.g_placement, self.Zdir, self.base_height)
        return extruded_base
    
    def base_product_as_ifccolumn(self, base_product_representation):
        params = {
            "GlobalId": self.guid(),
            "Name": "Column Base",
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": self.base_local_placement,
            "Representation": base_product_representation
        }
        base_as_ifccolumn = self.ifcfile.createIfcColumn(**params)
        return base_as_ifccolumn

class Column(ColumnBase):
    """
    => A column with standard Ifc parameters see https://standards.buildingsmart.org/IFC/DEV/IFC4_3/RC1/HTML/schema/ifcprofileresource/lexical/ifcishapeprofiledef.htm 

    => Get base_height from base params for placing column's LCS (Local Coordinate System) 
    
    => Create LCS of Column
    
    => Construct Column Profile (By Creating another placement for 2D drawing, where Ifc "I" shaped profile is drawn)
    
    => Extrude Column Profile
    
    => Create Product Representation (Here its just the extruded solid body, but this can be combined with some datum plane or axis)
    
    => Assign the product to Ifc element called "IfcColumn" with the created LCS
    
    => Place the IfcColumn in the ground storey

    => NOTE: This class has poor discipline compared to the parent class
    """

    def __init__(self, column_params, base_params, **kwgs):
        self.column_params = column_params
        super().__init__(base_params, **kwgs)
        col_foot = float(base_params.get("base_height"))
        self.column_local_placement = self.create_ifclocalplacement(point = np.array([0.,0.,col_foot]), relative_to = self.base_local_placement)
        self.construct_column_profile2d()
        self.extrude_column_profile()
        self.column_product_representation = self.create_product_representation(self.extruded_column)
        self.column_product_as_ifccolumn()
        self.place_ifcelement_in_storey(self.column_as_ifccolumn, self.ground_storey)

    def construct_column_profile2d(self):
        self.column_profile_placement = self.ifcfile.createIfcAxis2Placement2D(self.ori, self.Xdir)
        self.col_height = self.column_params.get("ColumnHeight")
        self.column_params.pop("ColumnHeight")
        self.column_profile = self.ifcfile.createIfcIShapeProfileDef("AREA", "Column Profile", self.column_profile_placement, **self.column_params)
    
    def extrude_column_profile(self):
        self.extruded_column = self.ifcfile.createIfcExtrudedAreaSolid(self.column_profile, self.g_placement, self.Zdir, self.col_height)

    def column_product_as_ifccolumn(self):
        params = {
            "GlobalId": self.guid(),
            "Name": "Column",
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": self.column_local_placement,
            "Representation": self.column_product_representation
        }
        self.column_as_ifccolumn = self.ifcfile.createIfcColumn(**params)
        
column_params = {
    "OverallWidth": 0.6,
    "OverallDepth": 0.75,
    "WebThickness": 0.05,
    "FlangeThickness": 0.05,
    "FilletRadius": 0.05,
    "ColumnHeight": 5
}
import numpy as np
base_params = {
    "base_location": np.array([5., 5., 0.]),
    "base_width": 1.,
    "base_height": 1.5
}

column_obj = Column(column_params, base_params, filename = "ColumnTest.ifc")
column_obj.write_ifcfile()