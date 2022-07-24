import ifcopenshell as ifcops
import pprint as pp
import sys

def get_attr(name):
        print(name + "\n")
        schema = ifcops.ifcopenshell_wrapper.schema_by_name("IFC2X3")
        ele = schema.declaration_by_name(name)
        pp.pprint(ele.all_attributes())

get_attr(str(sys.argv[1]))