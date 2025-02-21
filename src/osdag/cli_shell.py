import click
import yaml
import click_repl
import sys
import os
#import readline

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
                click.echo(f"Found module: {module_name}")
                return
        click.echo("No Module line found in the file")

@cli.command()
@click.option('-i', '--input-file', required=True, type=click.Path(exists=True), help='Input YAML file path')
def parse_yaml(input_file):
    """Parse and display the entire YAML file content."""
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)
        click.echo(data)

@cli.command()
def exit():
    """Exit the Osdag shell."""
    click.echo("Exiting Osdag shell.")
    os._exit(0)

@cli.command()
def quit():
    """Exit the Osdag shell."""
    click.echo("Exiting Osdag shell.")
    os._exit(0)

if __name__ == '__main__':
    cli()
