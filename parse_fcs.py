"""
Created on 2 August 2018
@author: Isaac Wong
@email: isaacwongsiushing@gmail.com

The script and all the code within is licensed under GNU GENERAL PUBLIC LICENSE
"""

import re 
import os
import sys

import numpy as np
import pandas as pd

if __name__ == "__main__":

    root_path = sys.argv[1] # The folder storing all fcs data
    num_recordings = int(sys.argv[2]) # Specify the number of recordings per fcs file

    fcs_data = [] # List storing all recordings

    fnames = sorted([os.path.join(root_path, f) for f in os.listdir(root_path) if f.endswith('.fcs')]) # List of files in the root path
    start = [False for i in range(num_recordings)] # List of boolean specifying the start and end of a recording

    for fname in fnames: # Loop of all files

        print "Processing {}".format(fname)

        temp_data = [[] for i in range(num_recordings)] # Initialize a list of list containing recordings per file
        start_clone = list(start) # Clone the start list
        
        with open(fname) as f:
            for line in f: # Loop over all lines in a fcs file
#===================================================================================
#               Major logic part
#===================================================================================             
                for i in range(num_recordings):
                    if len(re.findall('^\t?BEGIN FcsEntry{}'.format(i + 1), line)) > 0: # Regular expression to find the start of a recording
                        start_clone[i] = True

                if len(re.findall('^\t\t\tCorrelationArraySize', line)) > 0: # Regular expression to find the end of a recording
                    for i in range(num_recordings):
                        start_clone[i] = False
                        
                for i in range(num_recordings): # Read the line that contains timestamp and the peak information
                    if start_clone[i]:
                        if len(re.findall('\t\t\t\d+', line)) > 0:
                            t = float(line.split('\t')[3]) # Time
                            m = float(line.split('\t')[4]) # Peak
                            temp_data[i].append([t, m])
                            
            f.close()
            
            for i in range(num_recordings):
                temp_data[i] = np.array(temp_data[i]) # Convert each reacording into a numpy array
            
        for i in range(num_recordings):
            fcs_data.append(temp_data[i])

#===================================================================================
#   Ensure each recording is of the same length by appending np.nan
#===================================================================================   
    longest = fcs_data[0].shape[0]
    time_index = fcs_data[0][:, 0]

    for data in fcs_data:
        if data.shape[0] > longest:
            longest = data.shape[0] # The length of the longest recording
            time_index = data[:,0] # The longest time index

    fcs_data_saved = []
    for data in fcs_data:
        temp = data[:, 1].tolist()
        if len(temp) < longest:
            temp.extend([np.nan]*(longest - len(temp)))
        fcs_data_saved.append(temp)

#===================================================================================
#   Save data into csv file
#===================================================================================  
    fcs_data_saved = np.array(fcs_data_saved).T
    df = pd.DataFrame(fcs_data_saved, index=time_index)
    df.to_csv(os.path.join(root_path, 'data.csv'))