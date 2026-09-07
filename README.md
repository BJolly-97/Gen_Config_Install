# Gen-Config

[![CI](https://github.com/BJolly-97/Gen_Config_Install/actions/workflows/ci.yml/badge.svg)](https://github.com/BJolly-97/Gen_Config_Install/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%20%E2%80%93%203.13-blue)

**A Generalised Tool for the Analysis of Atomic Configurations in Crystalline Materials**

This tool has been created for the quantification of chemical short-range order in the large-box models produced by
[RMCProfile](https://rmcprofile.pages.ornl.gov/), through the computation of statistical
*enhancement factors* (β) for local atomic configurations. The framework outlined here redefines and generalises the
method of **[P. C. Clapp, *Atomic Configurations in Binary Alloys*, Phys. Rev. B **4**, 255 (1971)](https://doi.org/10.1103/PhysRevB.4.255)**
— originally limited to binary primitive/FCC/BCC crystals — to **any crystal
structure with any number of elements**.

** Bugs, general usability concerns, or any further queries should therefore be reported/forwarded to Dr. Ben Jolly (b.e.jolly@sheffield.ac.uk) or Dr. Lewis Owen (lewis.owen@sheffield.ac.uk).**

The original code files for the package can be found in a separate public repo: https://github.com/BJolly-97/Gen_Config/tree/main . These files are preserved to ensure usability (including the original launchers) and to provide the original versions as untouched by Claude/agents.

<p align="center">
  <img src="docs/assets/example-histogram.png" alt="Enhancement-factor histogram for an Fe/Ni solid solution" width="520">
</p>

> **Input format:** currently reads RMCProfile `.rmc6f` configuration files and `.cif`
> structures only.

## Installation

```bash
pip install clapp-jolly
```

or, for an isolated command-line install:

```bash
pipx install clapp-jolly        # or:  uv tool install clapp-jolly
```
NB: pipx is its own installation tool used to download software packages in isolated environments. If intending to use pipx for this package, please refer to pipx installation guides.

From a clone, for development:

```bash
pip install -e ".[dev]"
```

Or run the headless CLI with no Python install via Docker:

```bash
docker run --rm -v "$PWD:/data" ghcr.io/bjolly-97/clapp-jolly config --dict-dir . --sublattice 0 --rmc6f run.rmc6f
```

Either way you get one command, **`gen-config`**. (The importable package is
`gen_config`; the pre-package script names live in [`legacy/`](legacy/).)

## Quickstart

Using the bundled [`examples/FeNi/`](examples/FeNi/):

```bash
cd examples/FeNi

# 1. Build the structure dictionaries (merge Fe + Ni into one disordered sub-lattice)
gen-config dict --cif FeNi.cif --equivalence 0,1

# 2. Enhancement-factor analysis of one configuration
gen-config config --dict-dir . --sublattice 0 --rmc6f FeNi_solid_solution.rmc6f

# 3. Visualise Clapp configurations 1 and 12 in 3D
gen-config vis --dict-dir . --sublattice 0 --config 1,12
```

Step 2 writes `*_sub0_EF.clapp` (the enhancement factors) and the `*_EF*.png`
histograms shown above, alongside the input file.

Run `gen-config` with no arguments for an interactive menu instead.

## Usage

`gen-config` has three subcommands, each usable interactively (prompts) or scripted
(flags):

| Command | Purpose |
| --- | --- |
| `gen-config dict` | Generate the per-structure dictionary files from a `.cif` |
| `gen-config config` | Run the enhancement-factor analysis for one or many `.rmc6f` files |
| `gen-config vis` | Plot Clapp configurations for a sub-lattice in 3D |

Batch a whole directory in one process (one bad file doesn't abort the run):

```bash
gen-config config --dict-dir . --sublattice 0 --rmc6f-glob "configs/*.rmc6f"
```

Full command reference, the interactive workflow, and a description of every output
file are in **[the documentation](docs/index.md)**.

## Development

```bash
pip install -e ".[dev]"
pre-commit install
pytest
```

See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md). CI runs `ruff` plus the test
suite on Linux/macOS/Windows × Python 3.9/3.11/3.13.

## Citing

If you use this software, please cite both the software (see
[`.github/CITATION.cff`](.github/CITATION.cff)) and the Clapp 1971 paper linked above.

## License

[MIT](LICENSE) © Benjamin E. Jolly and Lewis R. Owen, University of Sheffield.

Questions: Dr. Ben Jolly (b.e.jolly@sheffield.ac.uk), Dr. Lewis Owen (lewis.owen@sheffield.ac.uk).
