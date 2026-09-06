# Legacy entry points

Before this project became an installable package, it was a set of loose scripts
run by filename (`Histograms_v2_2.py`, `Configuration_Master.py`, …) and a couple
of `.bat` helpers. Everything they did now lives in `src/gen_config/` and is driven
by the single `gen-config` command (see the top-level [README](../README.md)).

These files are kept **only** so existing scripts, notes, and muscle memory that
point at those exact names keep working. They are thin wrappers - each one just
imports and calls the real implementation:

| Legacy file | Replacement |
| --- | --- |
| `exe/Generalised_Clapp_v2.py`, `Batching_Scripts/Generalised_Clapp_v2.py` | `gen-config dict` |
| `exe/Histograms_v2_2.py`, `Batching_Scripts/Histograms_v2_2.py` | `gen-config config` |
| `exe/Visualiser.py` | `gen-config vis` |
| `Batching_Scripts/Configuration_Master.py` | `python -m gen_config.batch` (or `gen-config config --rmc6f-glob ...`) |
| `Batching_Scripts/Requirements.bat` | `pip install -e .`, or any launcher in the repo root |

They require the package to be installed first (`pip install -e .` from the repo
root). New work should use `gen-config` directly; this directory will be removed
in a future release.
