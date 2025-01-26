import click
import os

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def determine_module(file_path):
    """
    Reads a plain text file line by line, extracts the 'Module' field,
    and determines the module type.
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Check if the line contains the 'Module' field
                if line.startswith("Module:"):
                    # Extract and print the module name
                    module_name = line.split(':', 1)[1].strip()
                    click.echo(f"Module: {module_name}")
                    return
        click.echo("Error: 'Module' field not found in the file.")
    except Exception as e:
        click.echo(f"Error processing file: {e}")

if __name__ == "__main__":
    determine_module()
