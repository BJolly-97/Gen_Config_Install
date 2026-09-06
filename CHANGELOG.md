# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `LICENSE` (MIT), `CHANGELOG.md`, and `CITATION.cff`.
- Full packaging metadata in `pyproject.toml` (classifiers, keywords, project URLs,
  PEP 639 license declaration).
- macOS/Linux launcher (`Configurational_Analysis.command` / `.sh`) that builds a
  self-contained virtual environment on first run, so it never installs into a
  system-managed Python.
- Regression test covering 9-column, bare-10-column and bracketed-10-column
  `.rmc6f` layouts.
- Continuous integration (GitHub Actions): `ruff` lint + format check, `pytest`
  with coverage on Linux/macOS/Windows × Python 3.9/3.11/3.13, and a package
  build + `twine check`.
- `pre-commit` config, Dependabot, and `CONTRIBUTING.md`.

### Changed
- Renamed the distribution to `clapp-jolly` (the import package stays `gen_config`
  and the command stays `gen-config`).
- Moved the pre-package compatibility wrappers (`exe/`, `Batching_Scripts/`) into
  `legacy/` with an explanatory README.
- Applied `ruff format` across the codebase (whitespace/layout only; recorded in
  `.git-blame-ignore-revs`).

### Fixed
- `config` now reads `.rmc6f` files whose `Atoms:` section omits the optional
  site-label column (9-column layout); previously every field was read one column
  to the left and the run crashed.
- Enhancement-factor histograms label the y-axis with β, not Ψ.

## [1.0.0] - 2024

First packaged release. The previously loose analysis scripts became an installable
Python package (`src/gen_config/`) exposing a single `gen-config` command with
`dict`, `config`, `vis` and `gui` subcommands, interactive and scripted/batch
modes, a desktop GUI, and an end-to-end regression test suite.
