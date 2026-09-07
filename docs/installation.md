# Installation

`clapp-jolly` requires **Python 3.9 or newer**. It depends only on `numpy`, `pandas`,
`matplotlib` and `tqdm`, all of which install as wheels on Windows, macOS and Linux.

## From PyPI

```bash
pip install clapp-jolly
```

For an isolated install of just the command-line tool (recommended if you only want to
*run* it, not import it):

```bash
pipx install clapp-jolly
# or
uv tool install clapp-jolly
```

## From source

```bash
git clone https://github.com/BJolly-97/Gen_Config_Install
cd Gen_Config_Install
pip install -e ".[dev]"
```

## Docker

A headless image (published to GHCR on each release) runs the `dict` and `config`
commands with no Python install on the host — useful for reproducible batch runs on a
cluster or in CI. Mount your working directory at `/data`:

```bash
docker run --rm -v "$PWD:/data" ghcr.io/bjolly-97/clapp-jolly \
    config --dict-dir . --sublattice 0 --rmc6f run.rmc6f
```

The interactive `vis` viewer and the desktop GUI need a display and are not usable from
the container.

## What you get

A single command, **`gen-config`**. The importable package is `gen_config`:

```python
from gen_config import dictionary, histograms, visualiser
```

The pre-package script names (`Histograms_v2_2.py`, `Configuration_Master.py`, …) still
exist as thin wrappers under `legacy/`, purely so old scripts keep working.

## The GUI

`gen-config gui` opens a desktop GUI (Dictionary / Analysis / Visualiser tabs). It needs
Tkinter:

- **Windows / macOS** — bundled with the python.org installer.
- **Linux** — install separately, e.g. `sudo apt install python3-tk`.
- **macOS system Python** often ships an old, buggy Tk; prefer the python.org build or
  `brew install python-tk`.

## Launcher scripts

The repository root has double-click launcher scripts for users who would rather not
touch a terminal — they create a local virtual environment and install into it on first
run. Once `clapp-jolly` is on PyPI, `pipx install` is the simpler cross-platform route.
