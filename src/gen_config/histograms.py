# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:17:37 2024

@author: CDT3
"""

import pandas as pd
import numpy as np
import sys
from tqdm import tqdm
import os 
import re
import copy

#%%
    
def diff_eq(avgd, asym):
    
    for i in range(len(avgd)):
        dum_list = []
        for j in range(len(asym)):
            
            chi = np.sqrt( ( avgd[1].iloc[i] - asym[0].iloc[j] )**2 + ( avgd[2].iloc[i] - asym[1].iloc[j] )**2 + ( avgd[3].iloc[i] - asym[2].iloc[j] )**2  )
            dum_list.append(chi)
        
        avgd.loc[i, 1] = asym[0].iloc[dum_list.index(min(dum_list))]
        avgd.loc[i, 2] = asym[1].iloc[dum_list.index(min(dum_list))]
        avgd.loc[i, 3] = asym[2].iloc[dum_list.index(min(dum_list))]
            


def main():
    print('\n====================================================================\n')
    print("\t\tConfigurational Analysis - v1.0 (2024)\n")
    print("\t   Developed by: Benjamin E. Jolly; Lewis R. Owen\n")
    print("\t\t    University of Sheffield, UK\n")
    print("====================================================================\n")

    #%%Collect relevant files and convert to dataframes

    filepath = input("Input Dictionaries Directory:\t")
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

    print("\nEnter desired sublattice for analysis (e.g. 0):\n")
    for i in range(len(sublab)):
        print(sublab.loc[i,0])

    sub_num = str(input())

    basis_ext = None
    binom_ext = None
    clapp_ext = None

    # Loop through files in the folder
    for stemname in os.listdir(filepath):
        if stemname.endswith(".basis"+sub_num):
            basis_ext = stemname
        if stemname.endswith(".binom"+sub_num):
            binom_ext = stemname
        if stemname.endswith(".cfgdict"+sub_num):
            clapp_ext = stemname

    if basis_ext is None or binom_ext is None or clapp_ext is None:
        raise FileNotFoundError(f"No '.basis{sub_num}'/'.binom{sub_num}'/'.cfgdict{sub_num}' files found in '{filepath}' for sub-lattice {sub_num}.")

    #%%

    sublab = sublab[0].str.split('\t',expand=True)
    sublab[1] = sublab[1].astype(object)  # column 1 ends up holding a list per row below - .loc[i, col] = <list> doesn't reliably store a list as one cell (pandas tries to broadcast it instead), so this uses .at[] further down as well
    for i in range(len(sublab)):
        sublab.loc[i,1] = sublab.loc[i,1].replace('\n', '')

    for i in range(len(sublab)):
        parts = sublab.loc[i,1].split('/')

    # Extract only the letters from each part
        sub_atoms = [re.findall(r'[A-Za-z]+', part)[0] for part in parts]
        sublab.at[i,1] = sub_atoms

    #%%

    basis = open(os.path.join(filepath, basis_ext), "r")
    basis_line_read = basis.readlines()
    basis.close()
    basis_lines = basis_line_read.copy()

    binom = open(os.path.join(filepath, binom_ext), "r")
    binom_line_read = binom.readlines()
    binom.close()
    binom_lines = binom_line_read.copy()

    config = open(os.path.join(filepath, clapp_ext), "r")
    config_line_read = config.readlines()
    config.close()
    config_lines = config_line_read.copy()

    basis_df = pd.DataFrame(basis_lines)
    binom_df = pd.DataFrame(binom_lines)
    config_df = pd.DataFrame(config_lines)


    #%%Adjust the basis set dataframe for use

    basis_df.drop([0,1,len(basis_df)-1], inplace=True)
    basis_df.reset_index(inplace=True)
    basis_df.drop(['index'], axis=1,inplace=True)

    basis_df = basis_df[0].str.split(r'\s+', expand=True)
    basis_df.drop([0,4,5], axis=1, inplace=True)
    basis_df.columns = range(basis_df.shape[1])


    #%%Adjust remaining dataframes

    binom_df = binom_df[0].str.split(r'\s+', expand=True)
    binom_df.drop([3], axis=1, inplace=True)

    config_df = config_df[0].str.split(r'\s+', expand=True)
    config_df.drop([2], axis=1, inplace=True)

    #%%Convert dataframes to numeric

    basis_df = basis_df.astype(float)
    binom_df = binom_df.astype(int)
    config_df = config_df.astype(int)

    #%%

    asym_file = None
    for stemname in os.listdir(filepath):
        if stemname.endswith(".cellpos"):
            asym_file = os.path.join(filepath, stemname)

    if asym_file is None:
        raise FileNotFoundError(f"No '.cellpos' file found in '{filepath}'. Run 'dict' first to generate the dictionary files.")

    asym_file = asym_file.strip('"')

    asym = open(asym_file, "r")
    asym_line_read = asym.readlines()
    asym.close()
    asym_lines = asym_line_read.copy()

    asym_df = pd.DataFrame(asym_lines)
    asym_df = asym_df[0].str.split(",", expand=True)
    asym_df.drop_duplicates(inplace=True)
    asym_df = asym_df.astype(float)


    #%%
    ###################################################
    #### DEFINING FUNCTIONS
    ###################################################
    def matrix_to_string(matrix, header=None):
     	# NEXT LINES TAKEN FROM WEB - They create a nice table output for the data
        if type(header) is list:
            header = tuple(header)
        lengths = []
        if header:
            for column in header:
                lengths.append(len(column))
        for row in matrix:
            for column in row:
                i = row.index(column)
                column = str(column)
                cl = len(column)
                try:
                    ml = lengths[i]
                    if cl > ml:
                        lengths[i] = cl
                except IndexError:
                    lengths.append(cl)
        lengths = tuple(lengths)
        format_string = ""
        for length in lengths:
            format_string += "%-" + str(length) + "s "
        format_string += "\n"
        matrix_str = ""
        if header:
            matrix_str += format_string % header
        for row in matrix:
            matrix_str += format_string % tuple(row)
        return matrix_str


    def modulo_sep(numb,base,comp):
     	# Separates a normal integer into its base components (for a given base and number of components)
     	A=[]
     	num_work=numb
     	while num_work > 0:
             rem = num_work % base
             num_work = (num_work - rem)/base
             A.insert(0,rem)
     	while len(A) < comp:
             A.insert(0,0)
     	return A
    def modulo_comb(set,base,comp):
     	# Recombines a separated base into a normal integer
     	num=0
     	for n in range(len(set)):
             num+=set[n]*(base**(comp-1-n))
     	return num
    def reduce_comp(A,B):
     	# Allows for a numbers to be made equivalent to each other
     	# A is the original set
     	# B is the equivalency
     	A1=[]
     	for n in A:
             A1.append(B[n])
     	return A1
    ####################################################
    #%%

    ####################
    ####   START CODE
    ####################
    #filename = input( "Filename (including .ext):	")

    filename= input("\nSelect .rmc6f file path (incl. extension):\t")
    filename = filename.strip('"')
    filenamex=filename.split(".")

    # These lines set-up the initial matrices that will be used
    atoms = []
    raw = []
    coordinates = []

    ####################
    ####   Read RMC file
    ####################

    if filenamex[-1]=="rmc6f":
     	#### Loads information from .rmc6f file
     
         filename_stem=filename.replace("."+str(filenamex[-1]),"")
         print("Path is "+str(filename_stem))
         raw_file=[]
         xyzac = open(filename)
         lines = xyzac.readlines()
         for n in lines:
             raw_file.append(n.split())
     	####
         at_labels=[]
         N_ats=[]
         U=[]
         CD=[]
         start_no=0
     	#### These are selecting the data lines from the header
         for n in range(30):
             if 'types' in raw_file[n]:
                 if 'atoms:' in raw_file[n]:
                     no_types=int(raw_file[n][-1])
                 else:
                     for n1 in range(no_types):
                         at_labels.append(raw_file[n][-no_types+n1])
             elif 'each' in raw_file[n]:
                 for n1 in range(no_types):
                     N_ats.append(int(raw_file[n][-no_types+n1]))
             elif 'Supercell' in raw_file[n]:
                 for n1 in range(2,5,1):
                     U.append(int(raw_file[n][n1]))
             elif 'Cell' in raw_file[n]:
                 for n1 in range(2,8,1):
                     CD.append(float(raw_file[n][n1]))
             elif 'Atoms:' in raw_file[n]:
                 start_no+=n+1
         LP_a = CD[0]/U[0]
         LP_b = CD[1]/U[1]
         LP_c = CD[2]/U[2]
     	######
     	# Prints file info in running window
         print("\nRMC6F INFO")
         print("No of atom types = "+str(no_types))
         print("Atom Types = "+str(at_labels))
         print("No. of atoms = "+str(N_ats))
         print("No. of unit cells = "+str(U))
         print("Cell dimensions = "+str(CD))
         print("Lattice parameters = "+str(LP_a)+" "+str(LP_b)+" "+str(LP_c))
     	######
     	# Reads the data in the file
         for n in range(start_no,len(raw_file),1):
             raw.append([float(raw_file[n][3]), float(raw_file[n][4]), float(raw_file[n][5])])
             #coordinates.append([round((float(raw_file[n][3]) - 0.5) * 2 * U[0],0), round((float(raw_file[n][4]) - 0.5) * 2 * U[1],0), round((float(raw_file[n][5]) - 0.5) * 2 * U[2],0)])
             coordinates.append([float(raw_file[n][3]), float(raw_file[n][4]), float(raw_file[n][5])])
             atoms.append(at_labels.index(raw_file[n][1]))
    else:
     	print("Don't recognise filetype, so have to stop...")
     	exit()


    #%%

    ##  Store atoms as separate dataframe?

    ########################
    ####### CALCULATION
    ########################

    #%% 	
    #These lines create the dictionary of atom coordinates in the configuration, from which we can reference the 12 nn

    for i in range(len(raw_file)):
        if 'Atoms:' in raw_file[i]:
            a_c_i = i
        

    master_df_main =pd.DataFrame(raw_file[a_c_i+1:])
    master_df_main.drop([0,2], axis=1, inplace=True)
    master_df_main.columns=range(master_df_main.shape[1])

    label_to_index = {label: j for j, label in enumerate(at_labels)}
    master_df_main[0] = master_df_main[0].map(label_to_index)

    for i in [0,4,5,6,7]:
        master_df_main[i]=master_df_main[i].astype(int)
    for i in [1,2,3]:
        master_df_main[i]=master_df_main[i].astype(float)
    

    #%%

    master_df = copy.deepcopy(master_df_main)
    sub_num = int(sub_num)

    uniq_types = sorted(master_df[0].unique())

    index_nums = []

    for i in range(len(sublab.loc[sub_num,1])):
        index_nums.append(at_labels.index(sublab.loc[sub_num,1][i]))

    master_df = master_df[master_df[0].isin(index_nums)]
    master_df.reset_index(inplace=True)
    master_df.drop(['index'], axis=1,inplace=True)

    #%%

    uniq_types2 = sorted(master_df[0].unique())

    if len(uniq_types2) == 1:
        print('\n\nSub-lattice '+str(sub_num)+' contains a single atomic species. Configurational analysis is therefore deemed trivial, and is halted.\n')
        sys.exit()

    #%% Re-mapping atom types on sub-lattices

    mapping = {old: new for new, old in enumerate(uniq_types2)}
    inv_mapping = {new: old for old, new in mapping.items()}  # to recover original at_labels index later (e.g. for the _mb.rmc6f writer)

    # Apply the mapping to relabel the column
    master_df[0] = master_df[0].map(mapping)

    
    #%%Calculations

    for i in [1,2,3]:
        master_df[i+7]=0
        master_df[i+7]+=(master_df[i]*U[i-1])-master_df[i+4]

    # Wrap into the principal range around the atom's assigned home unit cell. An atom whose
    # RMC-fitted (displaced) position crosses a periodic boundary relative to its recorded
    # reference cell can come out of the subtraction above near +-1 instead of near 0; wrapping
    # to the nearest integer preserves the true small displacement instead of discarding it
    # (previously: `if disp > 1: disp = 0`, a one-sided clamp that zeroed the value outright and
    # never handled the equivalent undershoot below 0).
    for i in [1,2,3]:
        master_df[i+7] = master_df[i+7] - master_df[i+7].round()


    #%%Averaging the offsite displacements to find ideal lattice positions

    vals_list = sorted(master_df[4].unique())
    avgd_df = master_df.groupby([4])[[8,9,10]].mean().reset_index()
    avgd_df.columns=range(avgd_df.shape[1])
    for i in [1,2,3]:
        avgd_df[i] = round(avgd_df[i], 4)

    #%%#This section takes the averaged lattice positions, from the section above, and compares them to the asymmetric unit cell taken from the configurational code

    diff_eq(avgd_df, asym_df)

    #%%#Creates the 'fine supercell coordinates'

    for i in tqdm(range(len(master_df)), desc="Generating supercell coordinates for selected sub-lattice"):
        for j in range(len(avgd_df)):
            if master_df[4].loc[i] == avgd_df[0].iloc[j]:
                master_df.loc[i, 8] = master_df[5].iloc[i]+avgd_df[1].iloc[j]
                master_df.loc[i, 9] = master_df[6].iloc[i]+avgd_df[2].iloc[j]
                master_df.loc[i, 10] = master_df[7].iloc[i]+avgd_df[3].iloc[j]


    NN_list_df = master_df[[0,8,9,10]].copy()
    NN_list_df.columns=range(NN_list_df.shape[1])


    #%%

    NN_list_df[4] = None  # not "" - as of pandas 3.x that would create a strict string-dtype column, and this cell later holds a list (see the Modulo_comb section below)

    # Precompute combinations of NN_list_df columns 1, 2, and 3 into tuples for fast lookup
    NN_combined = list(zip(NN_list_df[1], NN_list_df[2], NN_list_df[3]))

    # Create a lookup map (dictionary) for faster matching
    lookup_dict = pd.Series(NN_list_df[0].values, index=NN_combined).to_dict()

    # Loop through rows of NN_list_df
    for i in tqdm(range(len(NN_list_df)), desc="Generating nearest neighbour atom-type lists"):
    
        # Get the current row's values from columns 1, 2, and 3
        dummy_list = NN_list_df.iloc[i, [1, 2, 3]].values
    
        # Add the current row values to the entire basis_df, applying it row-wise
        dummy_NN = basis_df.values + dummy_list  # Shape (12, 3) + (3,)
    
        for j in range(len(dummy_NN)):
            for k in [0,1,2]:
                if dummy_NN[j][k] >= U[k]:
                    dummy_NN[j][k]=dummy_NN[j][k]-U[k]
                elif dummy_NN[j][k] < 0.0:
                    dummy_NN[j][k]=dummy_NN[j][k]+U[k]
    
        # Convert the dummy_NN into tuples for comparison
        dummy_combined = list(zip(dummy_NN[:, 0], dummy_NN[:, 1], dummy_NN[:, 2]))
    
        # Find matching rows in NN_list_df using the lookup_dict
        NN_list = [lookup_dict[dummy_row] for dummy_row in dummy_combined if dummy_row in lookup_dict]
    
        # Store the matching results as a comma-separated string
        NN_list_df.at[i, 4] = ','.join(map(str, NN_list))

    #%%$Trying to deal with no. types issue

    ######################################

    no_types_new = master_df[0].nunique()

    ######################################

    
    #%%Performing the modulo_comb on the newly generated lists

    NN_list_df[5] = None  # not "" - this cell holds an int (see astype(int) below); "" would create a strict string-dtype column on pandas 3.x and reject the int assignment

    for i in tqdm(range(len(NN_list_df)), desc='Modulo_comb'):
        NN_list_df.at[i, 4] = list(NN_list_df.loc[i, 4])
        NN_list_df.at[i, 4] = [int(j) for j in NN_list_df.loc[i, 4] if j != ',']
        NN_list_df.at[i, 5] = modulo_comb(NN_list_df.loc[i, 4], no_types_new, len(basis_df)) ########ASSUMING AT THIS POINT YOU NEED THE TOTAL NUMBER OF ATOMS

    NN_list_df[5] =  NN_list_df[5].astype(int)


    #%%

    NN_list_df[6] = None  # not "" - this cell holds a list (see A1 below); "" would create a strict string-dtype column on pandas 3.x and reject the list assignment

    #Does the conversion from higher order configurations to binary Clapp configurations
    for n in tqdm(range(len(NN_list_df)), desc='Conversion from higher order configurations to binary configs:'):
     	A=[]
     	for m1 in range(1,(2**no_types_new)-1,1):
             red = modulo_sep(m1,2,no_types_new)
             new_comp = reduce_comp(NN_list_df[4].loc[n],red)
             new_comp_no = int(modulo_comb(new_comp,2,len(basis_df)))
             if red[NN_list_df[0].iloc[n]]==0:
                 A.append(config_df[1].iloc[new_comp_no])
             else:
                 A.append(-config_df[1].iloc[new_comp_no])
     	A1=[]	
     	for m2 in range(int(len(A)/2)):
             if A[m2]<=binom_df.loc[0,0]-1:
                 A1.append(A[len(A)-1-m2])
             else:
                 A1.append(A[m2])
     	NN_list_df.at[n, 6] = A1


    #%%

    #Makes the Clapp configurations histogram
    cond_num=int(((2**no_types_new)-2)/2)
    config_hist=[]


    for n in range(binom_df[0].iloc[0], binom_df[0].iloc[-1]+1,1):
     	A=[n]
     	for n1 in range(cond_num):
             A.append([0,0,0])
     	config_hist.append(A)

    #%%
    #Counts the binary Clapp configurations into the histogram
    for n in tqdm(range(len(NN_list_df)), desc='Counting binary configurations into the histogram:'):
     	#print n
     	for n1 in range(1,cond_num+1,1):
         
             a1=NN_list_df[6].iloc[n][n1-1]#n[3][n1-1]

             config_hist[a1-binom_df[0].iloc[0]][n1][2]+=1
             red = modulo_sep(n1,2,no_types_new)
             config_hist[int(a1-binom_df[0].iloc[0])][int(n1)][int(red[NN_list_df[0].iloc[n]])]+=1

    
    #%%


    #%%$Trying to deal with no. types issue

    ######################################

    #TYPES ISSUE ENDS HERE?

    ######################################


    #%%

    ##################################################################
    ######## THESE LINES CALCULATE THE ENHANCEMENT FACTORS
    ##################################################################


    #Calculates the EF for the configurations
    for m1 in range(cond_num): 
     	Na=0
     	Nb=0
     	Ntot=0
     	for n in range(len(config_hist)):
             Na+=config_hist[n][m1+1][0]
             Nb+=config_hist[n][m1+1][1]
             Ntot+=config_hist[n][m1+1][2]
     	for n in range(len(config_hist)):
             config_hist[n][m1+1].append(float(config_hist[n][m1+1][0])/Na)
             config_hist[n][m1+1].append(float(config_hist[n][m1+1][1])/Nb)
             config_hist[n][m1+1].append(float(config_hist[n][m1+1][2])/Ntot)
     	X_b=(float(Nb)/(float(Na)+float(Nb)))
     	X_a=1-X_b
     	##These lines calculate the binomial value for this specific case
     	for n in range(len(binom_df)):
    		#pB is the probability of finding the Clapp config around an atom of type B
             pB= (X_b**(len(basis_df)-binom_df[2].iloc[n]))*(X_a**(binom_df[2].iloc[n]))
    		#pA is the probability of finding the Clapp config around an atom of type A
             pA= (X_b**(binom_df[2].iloc[n]))*(X_a**(len(basis_df)-binom_df[2].iloc[n]))
             pint= (pB*X_b)+(pA*X_a)
    		#### Adds Binomial probability to occ in [6-8]
             config_hist[n][m1+1].append(pA*binom_df[1].iloc[n])
             config_hist[n][m1+1].append(pB*binom_df[1].iloc[n])
             config_hist[n][m1+1].append(pint*binom_df[1].iloc[n])
 	
     	##### Adds Binomial predicted number in [9-11]
     	for n in config_hist:
    		#print n
             n[m1+1].append(n[m1+1][6]*Na)
             n[m1+1].append(n[m1+1][7]*Nb)
             n[m1+1].append(n[m1+1][8]*Ntot)
     	#### Adds difference in number in [12-14]
     	#### Adds binomial stdev in [15-17]
     	for n in config_hist:
             n[m1+1].append(n[m1+1][0]-n[m1+1][9])
             n[m1+1].append(n[m1+1][1]-n[m1+1][10])
             n[m1+1].append(n[m1+1][2]-n[m1+1][11])
             n[m1+1].append((n[m1+1][9]*(1-n[m1+1][6]))**(0.5))
             n[m1+1].append((n[m1+1][10]*(1-n[m1+1][7]))**(0.5))
             n[m1+1].append((n[m1+1][11]*(1-n[m1+1][8]))**(0.5))
     	##### Adds EF in [18-20]
     	for n in config_hist:
             if n[0]==0:
                 n[m1+1].append(0)
                 n[m1+1].append(0)
                 n[m1+1].append(0)
             else:
                 n[m1+1].append(n[m1+1][12]/n[m1+1][15])
                 n[m1+1].append(n[m1+1][13]/n[m1+1][16])
                 n[m1+1].append(n[m1+1][14]/n[m1+1][17])
    		#print n

    #%%

    index_sort = sorted(index_nums)

    #############################
    ####### OUTPUTTING RESULTS - EF
    #############################

    ###########Move back code results here###############
    #This section generates a second .rmc6f file with all atoms located on their ideal lattice positions.

    mb_df = copy.deepcopy(master_df)
    for i in [1,2,3]:
        mb_df[i] = mb_df[i+7]
        del mb_df[i+7]


    inserts = [at_labels[inv_mapping[idx]] for idx in mb_df[0]]
            

    mb_df.insert(0, "NewCol", inserts)
    mb_df.columns = [int(i) for i in range(len(mb_df.columns))] 

    mb_df.index=mb_df.index+1

    for i in [2,3,4]:
        mb_df[i] = mb_df[i]/(U[i-2])

    outfile = open(filename_stem+"_mb.rmc6f", 'w')
    for i in range(a_c_i+1):
        outfile.write(lines[i])
    outfile.close()

    mb_df.to_string()
    with open(filename_stem+"_mb.rmc6f", mode='a') as f:
        f.write(mb_df.to_string(header=False))

    #%%

    #These lines create the _EF.clapp file with the Enhancement factor data in
    outfile = open (filename_stem+"_sub"+str(sub_num)+'_EF.clapp', 'w')
    outfile.write('Enhancement Factor\n\n')
    outfile.write('Original Filename: '+filename+'\n')
    for n in index_nums:
     	outfile.write('No. of '+at_labels[n]+' atoms'+'('+str(cond_num-n)+'):	'+str(N_ats[n])+'\n')
    outfile.write('No. of unit cells in x:	'+ str(U[0]) +'\n')
    outfile.write('No. of unit cells in y:	'+ str(U[1]) +'\n')
    outfile.write('No. of unit cells in z:	'+ str(U[2]) +'\n\n')
    # Make Column Header
    header=["CC"]
    for n in range(1,cond_num+1,1):
     	header.append(str(no_types_new)+'_'+str(n)+'n_A')
     	header.append(str(no_types_new)+'_'+str(n)+'n_B')
     	header.append(str(no_types_new)+'_'+str(n)+'n_Tot')
    for n in range(1,cond_num+1,1):
     	header.append(str(no_types_new)+'_'+str(n)+'EF_A')
     	header.append(str(no_types_new)+'_'+str(n)+'EF_B')
     	header.append(str(no_types_new)+'_'+str(n)+'EF_Tot')
    # Make body to output
    for_output=[]
    for n in config_hist:
     	A1=[]
     	A1.append(n[0])
     	for n1 in range(1,len(n)):
             A1.append(n[n1][0])
             A1.append(n[n1][1])
             A1.append(n[n1][2])
     	for n1 in range(1,len(n)):
             A1.append(n[n1][18])
             A1.append(n[n1][19])
             A1.append(n[n1][20])
     	for_output.append(A1)
    # Output body
    result = matrix_to_string(for_output, header)
    outfile.write(result)
    outfile.close ()

    #############################
    ####### OUTPUTTING RESULTS - CC Numbers
    #############################
    #These lines create the .clapp file heading
    outfile2 = open (filename_stem+"_sub"+str(sub_num)+'.clapp', 'w')
    outfile2.write('Clapp Configurations\n\n')
    outfile2.write('Original Filename: '+filename+'\n')

    for n in index_nums:
     	outfile2.write('No. of '+at_labels[n]+' atoms'+'('+str(cond_num-n)+'):	'+str(N_ats[n])+'\n')
    outfile2.write('No. of unit cells in x:	'+ str(U[0]) +'\n')
    outfile2.write('No. of unit cells in y:	'+ str(U[1]) +'\n')
    outfile2.write('No. of unit cells in z:	'+ str(U[2]) +'\n\n')
    # Make Column Header
    header2=["X","Y","Z","At"]
    header2.append(str(no_types_new)+'C')

    for n in range(1,cond_num+1,1):
     	header2.append(str(no_types_new)+'_'+str(n)+'C') 
    # Make body to output
    for_output2=[]

    for n in range(len(NN_list_df)):
     	A1=[]
     	for n1 in range(3):
             A1.append((NN_list_df[n1+1].iloc[n]/(U[n1])))
     	A1.append(NN_list_df[0].iloc[n])
     	A1.append(NN_list_df[5].iloc[n])
     	for n1 in range(len(NN_list_df[6].iloc[n])):
             A1.append(NN_list_df[6].iloc[n][n1])
     	for_output2.append(A1)
    # Output body
    result2 = matrix_to_string(for_output2, header2)
    outfile2.write(result2)
    outfile2.close ()


    ##############################
    ######## SAVE PLOTS
    ##############################
 	
    import matplotlib.pyplot as plt

    for m1 in range(cond_num):
     	xDATvalues=[]
     	yDATvalues=[]
     	xDATAvalues=[]
     	yDATAvalues=[]
     	xDATBvalues=[]
     	yDATBvalues=[]
     	for n1 in range(len(config_hist)):
             xDATvalues.append(config_hist[n1][0])
             yDATvalues.append(config_hist[n1][m1+1][20])
             xDATAvalues.append(config_hist[n1][0])
             yDATAvalues.append(config_hist[n1][m1+1][18])
             xDATBvalues.append(config_hist[n1][0])
             yDATBvalues.append(config_hist[n1][m1+1][19])
     	#print max(yDATvalues)
     	plt.bar(xDATvalues,yDATvalues,color='red')
     	plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATvalues)-0.5,max(yDATvalues)+0.5])
     	plt.axhline(y=3, color='black', linestyle='dashed', linewidth=1)
     	plt.axhline(y=-3, color='black', linestyle='dashed', linewidth=1)
     	plt.savefig(filename_stem+"_"+str(m1+1)+"C_sub"+str(sub_num)+"_EF.png")
     	#plt.show()
     	plt.close()
     	#
     	plt.bar(xDATAvalues,yDATAvalues,color='blue')
     	plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATAvalues)-0.5,max(yDATAvalues)+0.5])
     	plt.axhline(y=3, color='black', linestyle='dashed', linewidth=1)
     	plt.axhline(y=-3, color='black', linestyle='dashed', linewidth=1)
     	plt.savefig(filename_stem+"_"+str(m1+1)+"C_sub"+str(sub_num)+"_EF_A.png")
     	plt.close()
     	#
     	plt.bar(xDATBvalues,yDATBvalues,color='green')
     	plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATBvalues)-0.5,max(yDATBvalues)+0.5])
     	plt.axhline(y=3, color='black', linestyle='dashed', linewidth=1)
     	plt.axhline(y=-3, color='black', linestyle='dashed', linewidth=1)
     	plt.savefig(filename_stem+"_"+str(m1+1)+"C_sub"+str(sub_num)+"_EF_B.png")
     	plt.close()
     	#
     	plt.bar(xDATAvalues,yDATAvalues,color='blue')
     	plt.bar(xDATBvalues,yDATBvalues,color='green')
     	if max(yDATAvalues)>=max(yDATBvalues):
             if min(yDATAvalues)<=min(yDATBvalues):
                 plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATAvalues)-0.5,max(yDATAvalues)+0.5])
             else:
                 plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATBvalues)-0.5,max(yDATAvalues)+0.5])
     	else:
             if min(yDATAvalues)<=min(yDATBvalues):
                 plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATAvalues)-0.5,max(yDATBvalues)+0.5])
             else:
                 plt.axis([binom_df[0].iloc[0],binom_df[0].iloc[-1],min(yDATBvalues)-0.5,max(yDATBvalues)+0.5])
     	plt.axhline(y=3, color='black', linestyle='dashed', linewidth=1)
     	plt.axhline(y=-3, color='black', linestyle='dashed', linewidth=1)
     	plt.savefig(filename_stem+"_"+str(m1+1)+"C_sub"+str(sub_num)+"_EF_AB.png")
     	plt.close()

    print("\nConfigurational Analysis Complete.\n")

    print("\n--------------End---------------\n\n")
























if __name__ == "__main__":
    main()
