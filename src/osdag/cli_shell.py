import click
import yaml
import click_repl
import sys
import os
#import readline
import re




base_dir = r"D:\Internship\My Forked Clone for CLI\Osdag\src\osdag"
file_path = os.path.join(base_dir, "osdagMainPage.py")


###############################       ALL FUNCTIONS        ################################

############## 1 ) MODULE VALIDATION AND VERIFICATION #########################
VALID_MODULES = ["Fin Plate Connection."]


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




VALID_MODULES = detect_imported_modules()  # Auto-update detected modules

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

if __name__ == '__main__':
    cli()

