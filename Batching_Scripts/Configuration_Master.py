# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:45:19 2024

@author: Ben Jolly
"""

import sys
import os

# Resolve paths relative to this script's own location, not the current working directory -
# Generalised_Clapp_v2.py and Histograms_v2_2.py live right next to this file.
script_dir = os.path.dirname(os.path.abspath(__file__))


def ask_yes_no(prompt):
    """Prompts for a Y/N answer; returns True/False, or None for anything else."""
    answer = input(prompt).strip().upper()
    if answer == 'Y':
        return True
    if answer == 'N':
        return False
    return None


print('\n====================================================================\n')
print("\t\tConfigurational Analysis - v1.0 (2024)\n")
print("\t   Developed by: Benjamin E. Jolly; Lewis R. Owen\n")
print("\t\t    University of Sheffield, UK\n")
print("====================================================================\n")

gen_dict = ask_yes_no("Generate Configurational Dictionary files? (Y/N):\t")

if gen_dict is None:
    print("\nInvalid input.")
else:
    if gen_dict:
        with open(os.path.join(script_dir, "Generalised_Clapp_v2.py")) as a:
            exec(a.read())

    run_hist = ask_yes_no('\nCalculate Enhancement Factors and generate Histograms? (Y/N):\t')

    if run_hist is None:
        print("\nInvalid input.")
    elif run_hist:
        with open(os.path.join(script_dir, "Histograms_v2_2.py")) as c:
            exec(c.read())


print("\n--------------End---------------\n\n")
