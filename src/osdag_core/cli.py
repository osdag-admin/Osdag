from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection
from osdag_core.design_type.connection.cleat_angle_connection import CleatAngleConnection
from osdag_core.design_type.connection.seated_angle_connection import SeatedAngleConnection
from osdag_core.design_type.connection.end_plate_connection import EndPlateConnection
from osdag_core.design_type.connection.base_plate_connection import BasePlateConnection
from osdag_core.design_type.connection.beam_cover_plate import BeamCoverPlate
from osdag_core.design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from osdag_core.design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from osdag_core.design_type.tension_member.tension_bolted import Tension_bolted
from osdag_core.design_type.tension_member.tension_welded import Tension_welded
from osdag_core.design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
from osdag_core.design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from osdag_core.design_type.connection.column_cover_plate import ColumnCoverPlate
from osdag_core.design_type.connection.column_end_plate import ColumnEndPlate
from osdag_core.design_type.compression_member.compression import Compression
from osdag_core.design_type.main import Main
from osdag_core.Common import TYPE_TEXTBOX, TYPE_OUT_BUTTON
from osdag_core.Common import (
    # Shear Connection
    KEY_DISP_FINPLATE,
    KEY_DISP_ENDPLATE,
    KEY_DISP_CLEATANGLE,
    KEY_DISP_SEATED_ANGLE,

    # Base Plate Connection
    KEY_DISP_BASE_PLATE,

    # Moment Connection
    KEY_DISP_BEAMCOVERPLATE,
    KEY_DISP_COLUMNCOVERPLATE,
    KEY_DISP_BEAMCOVERPLATEWELD,
    KEY_DISP_COLUMNCOVERPLATEWELD,
    KEY_DISP_BB_EP_SPLICE,
    KEY_DISP_COLUMNENDPLATE,
    KEY_DISP_BCENDPLATE,

    # Tension Member
    KEY_DISP_TENSION_BOLTED,
    KEY_DISP_TENSION_WELDED,

    # Compression Member
    KEY_DISP_COMPRESSION

)


available_modules = {
    KEY_DISP_BASE_PLATE:BasePlateConnection, 
    KEY_DISP_BEAMCOVERPLATE:BeamCoverPlate, 
    KEY_DISP_CLEATANGLE:CleatAngleConnection,
    KEY_DISP_COLUMNCOVERPLATE:ColumnCoverPlate, 
    KEY_DISP_COLUMNENDPLATE:ColumnEndPlate, 
    KEY_DISP_ENDPLATE:EndPlateConnection,
    KEY_DISP_FINPLATE:FinPlateConnection, 
    KEY_DISP_SEATED_ANGLE:SeatedAngleConnection, 
    KEY_DISP_TENSION_BOLTED:Tension_bolted,
    KEY_DISP_TENSION_WELDED:Tension_welded, 
    KEY_DISP_COMPRESSION:Compression, 
    KEY_DISP_BEAMCOVERPLATEWELD:BeamCoverPlateWeld,
    KEY_DISP_COLUMNCOVERPLATEWELD:ColumnCoverPlateWeld, 
    KEY_DISP_BB_EP_SPLICE:BeamBeamEndPlateSplice,
    KEY_DISP_BCENDPLATE:BeamColumnEndPlate,
}

from pathlib import Path
import yaml, click
import pandas as pd

def _print_result(out_dict:dict):
    print("="*100)
    for key, value in out_dict.items():
        print(f"|| {key}: {value}")
    print("="*100)

def _get_design_dictionary(osi_path:Path) -> dict:
    """return the design dictionary from an OSI file."""
    with open(osi_path, 'r') as file:
        return yaml.safe_load(file)
    
def _get_output_dictionary(module_class:Main) -> dict:
    """return the output dictionary for the design"""
    status = module_class.design_status
    out_list = module_class.output_values(module_class, status)
    out_dict = {"Parameter": "Value"}
    for option in out_list:
        if option[0] is not None and option[2] == TYPE_TEXTBOX:
            out_dict[option[0]] = option[3]
        if option[2] == TYPE_OUT_BUTTON:
            tup = option[3]
            fn = tup[1]
            for item in fn(module_class, status):
                lable = item[0]
                value = item[3]
                if lable!=None and value!=None:
                    out_dict[lable] = value
    return out_dict


def _save_to_csv(output_dictionary:dict, output_file:str):
    """save the output dictionary to a csv file"""
    df = pd.DataFrame(output_dictionary.items())
    df.to_csv(output_file, index=False, header=None)

def _save_to_pdf(module_class:Main, output_file:Path):
    """save the output dictionary to a pdf file"""
    popup_summary = {
            'ProfileSummary': {
            'CompanyName': 'LoremIpsum', 
            'CompanyLogo': '', 
            'Group/TeamName': 'LoremIpsum', 
            'Designer': 'LoremIpsum'
        }, 
        'ProjectTitle': 'Fossee', 
        'Subtitle': '', 
        'JobNumber': '123', 
        'AdditionalComments': 'No comments', 
        'Client': 'LoremIpsum', 
        'input_filename': f'{output_file}', 
        'does_design_exist': True, 
        'logger_messages': ''
        }
    module_class.save_design(module_class, popup_summary)



def run_module(*args, **kargs) -> dict:
    """Run the module specified in the OSI file located at osi_path."""
    osi_path = kargs["input_path"] if len(kargs) > 0 else None
    op_type = kargs["op_type"] if len(kargs) > 1 else "print_result"
    output_path = kargs["output_path"] if len(kargs) > 2 else None

    result = {
        "success": False,
        "operation": op_type,
        "input": str(osi_path) if osi_path else None,
        "output": None,
        "data": None,
        "errors": [],
    }

    if osi_path is None:
        result["errors"].append("No input file provided.")
        print(result)
        return result
    
    osi_path = Path(osi_path) if osi_path else None
    output_path = Path(output_path) if output_path else None
    if not osi_path.exists():
        result["errors"].append(f"File not found: {osi_path}")
        print(result)
        return result
    
    design_dict = _get_design_dictionary(osi_path)
    module_name = design_dict.get("Module")
    if not module_name:
        result["errors"].append("Module not specified.")
        print(result)
        return result

    module_class = available_modules.get(module_name)
    if not module_class:
        result["errors"].append(f"Not a valid module class: {module_name}")
        print(result)
        return result
    
    input_filename = osi_path.stem
    output_filename = output_path.stem if output_path else None
    if not output_path:
        output_folder_path = osi_path.parent / "Outputs" / f"{module_class.__name__}"
    else:
        output_folder_path = output_path.parent / f"{module_class.__name__}"
    output_folder_path.mkdir(parents=True, exist_ok=True)
    output_file = output_folder_path / f"{output_filename if output_filename else input_filename}"

    module_class.set_osdaglogger(None)
    val_errors = module_class.func_for_validation(module_class, design_dict)

    if val_errors:
        result["errors"].extend(val_errors)
        print(result)
        return result

    out_dict = _get_output_dictionary(module_class)
    result["data"] = out_dict
    if op_type == "save_csv":
        try:
            _save_to_csv(out_dict, str(output_file) + ".csv")
            result["success"] = True
            result["output"] = str(output_file)
        except Exception as e:
            result["success"] = False
            result["errors"].append(f"Failed to save CSV: {e}")

    elif op_type == "save_pdf":
        try:
            _save_to_pdf(module_class, output_file)
            result["success"] = True
            result["output"] = str(output_file)
        except Exception as e:
            result["success"] = False
            result["errors"].append(f"Failed to save PDF: {e}")

    elif op_type == "print_result":
        try:
            result["success"] = True
            click.echo(_print_result(out_dict=out_dict))
        except Exception as e:
            result["success"] = False
            result["errors"].append(f"Failed to get result: {e}")

    else:
        result["errors"].append(f"Unsupported op_type: {op_type}")

    if len(result["errors"]) > 0:
        print(result)
    
    return result
