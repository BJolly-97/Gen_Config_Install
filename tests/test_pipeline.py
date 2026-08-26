"""
End-to-end regression test for the Clapp configurational-analysis pipeline.

Runs dict -> config -> vis against a synthetic Pm-3m (full cubic point group) test
structure with two co-sited species (Fe/Ni, merged via the lattice-site-equivalence
mechanism into one disordered sub-lattice) and asserts each stage completes without
raising and produces the expected output files.

This exists because most of the crash bugs found while overhauling this codebase were
only found by actually running the pipeline end-to-end - static review and isolated
reproduction missed several of them.
"""

import shutil
from pathlib import Path

import pytest

from gen_config import dictionary, histograms, visualiser

FIXTURES = Path(__file__).parent / "fixtures"


def _feed_input(monkeypatch, answers):
    """Makes input() return each of `answers` in turn, ignoring the prompt text."""
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(it))


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    shutil.copy(FIXTURES / "FeNi.cif", tmp_path / "FeNi.cif")
    shutil.copy(FIXTURES / "FeNi_config.rmc6f", tmp_path / "FeNi_config.rmc6f")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_dict_generates_expected_files(workdir, monkeypatch):
    _feed_input(monkeypatch, ["FeNi.cif", "Y", "0,1", "N"])

    dictionary.main()

    for suffix in [".cellpos", ".initsub", ".finsub", ".basis0", ".sym0", ".cfgdict0", ".binom0"]:
        assert (workdir / f"FeNi{suffix}").exists(), f"dict did not produce FeNi{suffix}"

    finsub = (workdir / "FeNi.finsub").read_text()
    assert "Fe/Ni" in finsub, "the two co-sited species should have been merged into one Fe/Ni sub-lattice"


def test_config_runs_against_dict_output(workdir, monkeypatch):
    _feed_input(monkeypatch, ["FeNi.cif", "Y", "0,1", "N"])
    dictionary.main()

    _feed_input(monkeypatch, [".", "0", "FeNi_config.rmc6f"])
    histograms.main()

    for suffix in ["_sub0.clapp", "_sub0_EF.clapp", "_mb.rmc6f"]:
        assert (workdir / f"FeNi_config{suffix}").exists(), f"config did not produce FeNi_config{suffix}"

    ef_lines = (workdir / "FeNi_config_sub0_EF.clapp").read_text().splitlines()
    assert any(line.strip() for line in ef_lines[5:]), "enhancement factor file has no data rows"


def test_vis_runs_against_dict_output(workdir, monkeypatch):
    _feed_input(monkeypatch, ["FeNi.cif", "Y", "0,1", "N"])
    dictionary.main()

    # Ask for a configuration label that's guaranteed to exist (the most-common one, CC 1),
    # then decline to continue so the loop exits on the first pass.
    _feed_input(monkeypatch, [".", "0", "1", "N"])
    visualiser.main()  # should complete without raising
