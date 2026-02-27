# Osdag CLI Tool

A command-line interface for Osdag structural engineering design software.

## Installation

```bash
pip install -e .
```

## Usage

The Osdag CLI tool provides several commands for processing design files and generating reports:

### Process Design

Process an OSI file, run design calculations, show output values, and generate a design report:

```bash
osdag-cli process-design [-i input_file.osi] [-o output_directory] [-v]
```

Options:

- `-i, --input-file`: Path to the OSI input file (optional, will prompt if not provided)
- `-o, --output-dir`: Directory to save the design report (optional)
- `-v, --verbose`: Enable verbose output

### Show Design Output

Process an OSI file, run design calculations, and show output values without generating a report:

```bash
osdag-cli show-design-output [-i input_file.osi]
```

Options:

- `-i, --input-file`: Path to the OSI file (optional, will prompt if not provided)

### Custom Design

Run design calculations directly using a custom implementation (currently supports only Fin Plate Connection):

```bash
osdag-cli custom-design [-i input_file.osi]
```

Options:

- `-i, --input-file`: Path to the OSI file (optional, will prompt if not provided)

This command implements a more direct design calculation approach that may be more reliable for certain modules.

### Debug Module

Analyze a module, show its methods and inheritance hierarchy:

```bash
osdag-cli debug-module [-i input_file.osi]
```

Options:

- `-i, --input-file`: Path to the OSI input file (optional, will prompt if not provided)

### Show Content

Parse and display the content of an OSI file:

```bash
osdag-cli show-content [-i input_file.osi]
```

Options:

- `-i, --input-file`: Path to the OSI input file (optional, will prompt if not provided)

### List Modules

List all valid module names:

```bash
osdag-cli list-modules
```

### Interactive Shell

Start an interactive shell to run multiple commands:

```bash
osdag-cli shell
```

In shell mode, you can run any of the above commands without the `osdag-cli` prefix. Use `exit` or `quit` to exit the shell.

## Examples

1. Process a design file and generate a report in the specified directory:

```bash
osdag-cli process-design -i examples/fin_plate.osi -o ./reports
```

2. Process a design file with verbose output:

```bash
osdag-cli process-design -i examples/fin_plate.osi -o ./reports -v
```

3. Show design output values without generating a report:

```bash
osdag-cli show-design-output -i examples/fin_plate.osi
```

4. Debug a module to see its methods and attributes:

```bash
osdag-cli debug-module -i examples/fin_plate.osi
```

5. View all supported modules:

```bash
osdag-cli list-modules
```

6. Start an interactive shell:

```bash
osdag-cli shell
```

Then within the shell:

```
> process-design
> list-modules
> exit
```

7. Try the custom design implementation for a Fin Plate Connection:

```bash
osdag-cli custom-design -i examples/fin_plate.osi
```
