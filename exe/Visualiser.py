# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 13:18:40 2024

@author: CDT3
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#%%

print('\n====================================================================\n')
print("\t\tConfigurational Analysis - v1.0 (2024)\n")
print("\t\t Graphical Configuration Visualiser\n")
print("\t   Developed by: Benjamin E. Jolly; Lewis R. Owen\n")
print("\t\t    University of Sheffield, UK\n")
print("====================================================================\n")

filepath = input("Input Directory:\t")
filepath = filepath.strip('"')

sublattice_labels = None
for stemname in os.listdir(filepath):
    if stemname.endswith('.finsub'):
        sublattice_labels = stemname

if sublattice_labels is None:
    raise FileNotFoundError(f"No '.finsub' file found in '{filepath}'. Run 'dict' first to generate the dictionary files.")

sublab_file = open(os.path.join(filepath, sublattice_labels), "r")
sublab_read = sublab_file.readlines()
sublab_file.close()

sublab = pd.DataFrame(sublab_read)

exit_cond=0

while exit_cond == 0:
    print("\nEnter desired sublattice for analysis (e.g. 0):\n")
    for i in range(len(sublab)):
        print(sublab.loc[i,0])
    
    sub_num = str(input())
    
    basis_ext = None
    clapp_ext = None

    # Loop through files in the folder
    for stemname in os.listdir(filepath):
        if stemname.endswith(".basis"+sub_num):
            basis_ext = stemname
        if stemname.endswith(".cfgdict"+sub_num):
            clapp_ext = stemname

    if basis_ext is None or clapp_ext is None:
        raise FileNotFoundError(f"No '.basis{sub_num}'/'.cfgdict{sub_num}' files found in '{filepath}' for sub-lattice {sub_num}.")

    basis = open(os.path.join(filepath, basis_ext), "r")
    
    line_read = basis.readlines()
    
    basis.close()
    
    lines = line_read.copy()
    
    del lines[0:2]
    del lines[-1]
    
    basis_df = pd.DataFrame(lines)
    
    basis_df = basis_df[0].str.split('\\s+', expand = True)
    basis_df.drop([0, 4, 5], axis=1, inplace=True)
    basis_df.rename(columns={1:'x', 2:'y', 3:'z',5:'Atom No.'}, inplace=True)


    #%%

    config_dict = open(os.path.join(filepath, clapp_ext), "r")
    config_read = config_dict.readlines()
    
    config_dict.close()
    
    config_df = pd.DataFrame(config_read)
    
    config_df = config_df[0].str.split('\\s+', expand = True)
    
    input_config_list = input("\nInput desired configuration(s) (NB: For multiple configuration plots, separate values using commas.):\t")
    input_config = input_config_list.split(',')
    
    for z in range(len(input_config)):
        input_dec = None
        for n in range(len(config_df)):
            if config_df[1][n] == input_config[z]:
                input_dec = int(config_df[0][n])
                break

        if input_dec is None:
            print(f"\nConfiguration label '{input_config[z]}' not found for this sub-lattice - skipping.")
            continue

        #%%

        #input_dec = int(input("Decimal Number of Configuration from Dictionary:"))

        input_bin = bin(input_dec)
        
        full_bin = input_bin[2:].zfill(len(basis_df))
        
        full_bin = list(full_bin)
        bin_df = pd.DataFrame(full_bin)
        bin_df.rename(columns={0:'Bin'}, inplace=True)
        
        Plotting_df = pd.concat([basis_df, bin_df], axis=1)
        
        axes = [1,1,1]
        data = np.ones(axes)
        data = data*0.5
        
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        
        for i in range(len(Plotting_df)):
            if Plotting_df['Bin'][i] == '1':
                ax.scatter(float(Plotting_df['x'].iloc[i]), float(Plotting_df['y'].iloc[i]), float(Plotting_df['z'].iloc[i]), color='r', s=500)
            elif Plotting_df['Bin'][i] == '0':
                ax.scatter(float(Plotting_df['x'].iloc[i]), float(Plotting_df['y'].iloc[i]), float(Plotting_df['z'].iloc[i]), color='black', s=500)
        
        
        ax.scatter(0,0,0, marker='X', color='black', s=150)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("C"+input_config[z])
        
        plt.show()

    A = input('\nContinue with visualisation for selected sublattice? (Y/N)\n').strip().upper()
    if A == 'Y':
        pass
    elif A == 'N':
        exit_cond+=1
    else:
        print('\nInvalid Input.\n')
        exit_cond+=1

print("\n--------------End---------------\n\n")
    
    


