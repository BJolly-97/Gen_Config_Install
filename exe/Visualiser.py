"""Thin compatibility wrapper - the real implementation now lives in gen_config.visualiser.

Requires the package to be installed first: run `pip install -e .` from the repo root
(the launcher scripts do this for you), or install gen_config normally.
"""
from gen_config.visualiser import main

if __name__ == "__main__":
    main()
