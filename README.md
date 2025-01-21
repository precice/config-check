# preCICE Config Checker

A library that checks a preCICE configuration file for logical errors.

**How does this differ from [precice-tools check](https://precice.org/tooling-builtin.html)?** This checker only checks the
configuration for logical errors.

> [!NOTE]
> This checker assumes that `precice-tools check` has already been executed without an error on the configuration file.<br>
> Otherwise, the behavior of this checker is undefined.

## Requirements

- Python 3.12
- Pip
- Git for cloning the repository
- [precice-config-graph Library](https://github.com/precice-forschungsprojekt/config-graph). This will be installed during the Installation step below.

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
You need to force re-install the `precice_config_graph`-dependency on new versions, since it is downloaded directly from GitHub. To do so, run:
```bash
pip install --ignore-installed .
```

## Project Structure

```
config-checker
├── .github, .idea, etc…
│
├── docs                       # Documentation on rules and the inner workings of this checker
│
├── preciceconfigchecker       # Main library files
│   ├── rules                  # All rules that are checked by this utility
│   │   ├── ...
│   │   └── examples           # Exemplary implementations of rules to test output format 
│   │       └── ...
│   │
│   ├── test-xml-files         # Configuration files to test rules 
│   │   └── ...
│   │
│   ├── cli.py                 # Main entrypoint for this checker
│   ├── color.py               # Definition of colors for CLI output
│   ├── rule.py                # Class of a rule and logic to check all rules
│   ├── severity.py            # Enum for specifying severity of output
│   └── violation.py           # Class of a violation
│
│
├── .gitignore, LICENSE, README.md
│
├── pyproject.toml             # Project configuration (dependencies etc.)
└── shell.nix                  # Dependencies for anyone using NixOS / the nix-package manager. Should be replaced by a flake in the future.
```

## Checking a preCICE config

To check a preCICE configuration file for logical errors, run the following within the root of this repository:

```bash
python preciceconfigchecker/cli.py "/path/to/precice-config.xml"
```

If you want more information about the checks that were performed and their results, use

```bash
python preciceconfigchecker/cli.py "/path/to/precice-config.xml" --debug
```