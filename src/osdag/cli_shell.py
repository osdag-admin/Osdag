import click
import yaml
import click_repl
import sys
import os
#import readline
import re
from .Common import (
    TYPE_COMBOBOX, TYPE_COMBOBOX_CUSTOMIZED, TYPE_TEXTBOX,
    KEY_DISP_FINPLATE, KEY_DISP_ENDPLATE, KEY_DISP_CLEATANGLE,
    KEY_DISP_SEATED_ANGLE, KEY_DISP_COLUMNCOVERPLATE,
    KEY_DISP_COLUMNCOVERPLATEWELD, KEY_DISP_BEAMCOVERPLATE,
    KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_BB_EP_SPLICE,
    KEY_DISP_COLUMNENDPLATE, KEY_DISP_BASE_PLATE,
    KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED
)
from .design_type.connection.fin_plate_connection import FinPlateConnection
from .design_type.connection.end_plate_connection import EndPlateConnection
from .design_type.connection.cleat_angle_connection import CleatAngleConnection
from .design_type.connection.seated_angle_connection import SeatedAngleConnection
from .design_type.connection.column_cover_plate import ColumnCoverPlate
from .design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from .design_type.connection.beam_cover_plate import BeamCoverPlate
from .design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from .design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
from .design_type.connection.column_end_plate import ColumnEndPlate
from .design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from .design_type.connection.base_plate_connection import BasePlateConnection
from .design_type.tension_member.tension_bolted import Tension_bolted
from .design_type.tension_member.tension_welded import Tension_welded




base_dir = r"D:\Internship\My Forked Clone for CLI\Osdag\src\osdag"
file_path = os.path.join(base_dir, "osdagMainPage.py")


###############################       ALL FUNCTIONS        ################################

############## 1 ) MODULE VALIDATION AND VERIFICATION #########################
VALID_MODULES = ["Fin Plate Connection","End Plate Connection"]


def validate_module_name(module_name):
    if module_name.lower() in [mod.lower() for mod in VALID_MODULES]:  # Case-insensitive check
        return True
    else:
        raise ValueError(f"Invalid module name: {module_name}.")

############## 2 ) AUTO MODULE DETECTION #########################

def detect_imported_modules():
    """Auto-detect imported modules in osdagMainPage.py and filter relevant ones."""
    # file_path = r"D:\Internship\My Forked Clone for CLI\Osdag\src\osdag\osdagMainPage.py"  
    pattern = re.compile(r'^(?:from)\s+([\w\.]+)(?:\s+import\s+([\w\*, ]+))?')

    relevant_modules = set()
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                match = pattern.match(line.strip())
                if match:
                    module_path = match.group(1)  # Full module path
                    imports = match.group(2)  # Extracts specific imports (like FinPlateConnection)

                    if imports:
                        # If specific imports exist, extract and store them
                        for item in imports.split(","):
                            item = item.strip()
                            if item and item != "*":  # Ignore wildcard imports
                                relevant_modules.add(item)
                    else:
                        # Otherwise, store the full module name if no specific imports
                        relevant_modules.add(module_path)

    return sorted(relevant_modules)




# VALID_MODULES = detect_imported_modules()  # Auto-update detected modules

#################################              END OF ALL FUNCTIONS     ##################################




##################################      START ALL COMMANDS             ####################################




@click.group()
def cli():
    """Osdag CLI tool with interactive shell"""
    pass

@cli.command()
def shell():
    """Start the interactive shell"""
    #os.environ["CLICK_REPL_PROMPT"] = "osdag> "
    click.echo("Entering Osdag shell. Type '--help' for commands.")
    from click import Context
    ctx = Context(cli)
    click_repl.repl(ctx)


@cli.command()
@click.option('-i', '--input-file', required=True, type=click.Path(exists=True), help='Input YAML file path')
def find_module(input_file):
    """Find and extract the Module line from a YAML file."""
    with open(input_file, 'r') as file:
        for line in file:
            if line.strip().startswith('Module:'):
                module_name = line.split('Module:')[1].strip()
                try:
                    validate_module_name(module_name)
                    click.echo(f"Found module: {module_name}")
                except ValueError as e:
                    print(e)

        #         return
        # click.echo("No Module line found in the file")

@cli.command()
@click.option('-i', '--input-file', required=True, type=click.Path(exists=True), help='Input YAML file path')
def parse_yaml(input_file):
    """Parse and display the entire YAML file content."""
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)
        click.echo(data)


################################## TESTING FUNCTIONS ONLY #################################

@cli.command()
def list_modules():
    ##"""List all detected modules."""
    click.echo("Detected Modules:")
    modules = detect_imported_modules()
    # print("Filtered Modules:")
    for module in modules:
        print(f"- {module}")



################################# END OF TESTING FUNCTIONS ###########################


@cli.command()
def exit():
    ##"""Exit the Osdag shell."""
    click.echo("Exiting Osdag shell.")
    os._exit(0)

@cli.command()
def quit():
    ##"""Exit the Osdag shell."""
    click.echo("Exiting Osdag shell.")
    os._exit(0)

def parse_osi_file(input_file):
    """Parse an OSI file and extract values in the same format as the GUI.
    
    Args:
        input_file (str): Path to the OSI file
        
    Returns:
        dict: Dictionary containing the design inputs in the same format as the GUI
    """
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)
    
    # Extract module name
    module = data.get('Module')
    if not module:
        raise ValueError("No Module specified in OSI file")
        
    # Get the appropriate module class
    module_class = get_module_class(module)
    if not module_class:
        raise ValueError(f"Unknown module {module}")
        
    # Create module instance to get input definitions
    module_instance = module_class()
    
    # Get input definitions from module
    input_definitions = module_instance.input_values()
    
    # Create design inputs dictionary
    design_inputs = {}
    
    # Process each input definition
    for input_def in input_definitions:
        key = input_def[0]  # Input key
        input_type = input_def[2]  # Input type (combobox, textbox, etc.)
        
        if key is None:  # Skip titles and other non-input elements
            continue
            
        if key not in data:
            continue
            
        value = data[key]
        
        # Handle different input types
        if input_type == TYPE_COMBOBOX:
            # For combobox, validate against allowed values
            allowed_values = input_def[3]  # List of allowed values
            if value not in allowed_values:
                raise ValueError(f"Invalid value '{value}' for {key}. Must be one of: {allowed_values}")
            design_inputs[key] = value
            
        elif input_type == TYPE_COMBOBOX_CUSTOMIZED:
            # For customized combobox, handle special cases
            if key == 'Member.Designation':
                # Handle section designation specially
                design_inputs[key] = value
            else:
                # For other customized inputs, validate against allowed values
                allowed_values = input_def[3]
                if value not in allowed_values:
                    raise ValueError(f"Invalid value '{value}' for {key}. Must be one of: {allowed_values}")
                design_inputs[key] = value
                
        elif input_type == TYPE_TEXTBOX:
            # For textbox, just store the value
            design_inputs[key] = str(value)
            
        else:
            # For other types, store as is
            design_inputs[key] = value
            
    return design_inputs, module

@cli.command()
@click.option('-i', '--input-file', required=True, type=click.Path(exists=True), help='Input OSI file path')
def process_design(input_file):
    """Process an OSI file and run design calculations."""
    try:
        # Parse the OSI file
        design_inputs, module = parse_osi_file(input_file)
        
        # Get the appropriate module class
        module_class = get_module_class(module)
        if not module_class:
            click.echo(f"Error: Unknown module {module}")
            return
            
        # Create module instance and set inputs
        module_instance = module_class()
        module_instance.set_input_values(design_inputs)
        
        # Run design calculations
        module_instance.trial_design()
        
        # Get output values
        output_values = module_instance.get_output_values()
        
        # Display results
        click.echo("\nDesign Results:")
        for key, value in output_values.items():
            click.echo(f"{key}: {value}")
            
    except Exception as e:
        click.echo(f"Error processing design: {str(e)}")

def get_module_class(module_name):
    """Get the appropriate module class based on module name."""
    module_map = {
        'Fin Plate Connection': FinPlateConnection,
        'End Plate Connection': EndPlateConnection,
        'Cleat Angle Connection': CleatAngleConnection,
        'Seated Angle Connection': SeatedAngleConnection,
        'Column Cover Plate': ColumnCoverPlate,
        'Column Cover Plate Weld': ColumnCoverPlateWeld,
        'Beam Cover Plate': BeamCoverPlate,
        'Beam Cover Plate Weld': BeamCoverPlateWeld,
        'Beam-Beam End Plate Splice': BeamBeamEndPlateSplice,
        'Column End Plate': ColumnEndPlate,
        'Beam-Column End Plate': BeamColumnEndPlate,
        'Base Plate Connection': BasePlateConnection,
        'Tension Member Design - Bolted to End Gusset': Tension_bolted,
        'Tension Member Design - Welded to End Gusset': Tension_welded
    }
    return module_map.get(module_name)

if __name__ == '__main__':
    cli()