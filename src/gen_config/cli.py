# -*- coding: utf-8 -*-
"""
Interactive command-loop entry point.

Equivalent to the old Configurational_Analysis.bat / Configurational_Analysis_MacOS.sh
launchers, minus the dependency-install step (handled by `pip install` now).
"""

from gen_config import dictionary, histograms, visualiser


def main():
    while True:
        command = input(
            "> Enter command (i.e. dict (Configurational Dictionaries), "
            "config (Configurational Analysis), vis (Configuration Visualiser) "
            "or exit): "
        ).strip().lower()

        if command == "dict":
            dictionary.main()
        elif command == "config":
            histograms.main()
        elif command == "vis":
            visualiser.main()
        elif command == "exit":
            break
        else:
            print(f"Invalid command: {command}")


if __name__ == "__main__":
    main()
