# preCICE Config Checker

A library that checks a preCICE configuration file for logical errors.

**How does this differ from [precice-tools](https://precice.org/tooling-builtin.html)?** This checker only checks the
configuration for logical errors.

> [!NOTE]
> This checker assumes that `precice-tools check` has already been executed without an error on the configuration file.<br> 
> Otherwise, the behavior of this checker is undefined.

## Requirements

- Python 3.12
- Pip
- Git for cloning the repository
- precice-config-graph

## Installation

1. Clone this repository:
```bash
git clone https://github.com/precice-forschungsprojekt/config-checker
cd config-checker
```
2. Create a new Python Virtual Environment (optional, but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install required dependencies:
```bash
pip install .
```

## Project Structure

```
config-checker
├── .github, .idea, etc…
│
├── preciceconfigchecker       # Main library files
│   ├── rules                  # All rules that get checked by the checker
│   │   ├── ...
│   │   └── examples           # Exemplary implementations of rules to test output format 
│   │       └── ...
│   │
│   ├── test-xml-files         # Configuration files to test rules 
│   │   └── ...
│   │
│   ├── cli.py                 # Call this script to test a provided config file for logical errors
│   ├── color.py               # Definition of colors for output 
│   ├── rule.py                # Template for implementing rules
│   ├── severity.py            # Enum for severity of output
│   └── violation.py           # Template for implementing violations
│
│
├── .gitignore, LICENSE, README.md
│
├── pyproject.toml             # Project configuration (dependencies etc.)
└── shell.nix                  # Dependencies for anyone using NixOS / the nix-package manager. Should be replaced by a flake in the future.
```

## Using in your project

This library is not yet published to any package registry. Nonetheless, it can still be imported into your pyproject.toml like so:

```toml
# …
dependencies = [
    "preciceconfigchecker @ git+https://github.com/precice-forschungsprojekt/config-checker.git",
    # …
]
# …
```

Then, run `pip install .` in your project. TODO ?

[TODO]

If new versions of dependencies have been released, try `pip install --ignore installed .` to update your project.

## Checking a preCICE config

To check a preCICE configuration file for logical errors, run  

```bash
python preciceconfigchecker/cli.py "/path/to/precice-config.xml"
```

If you want more information about the checks that were performed and their results, use

```bash
python preciceconfigchecker/cli.py "/path/to/precice-config.xml" --debug
```

## Documentation

In the future, we will document how this checker works!
