"""
Created on 7 August 2018
@author: Isaac Wong
@email: isaacwongsiushing@gmail.com

The script and all the code within is licensed under GNU GENERAL PUBLIC LICENSE
"""

import os
import sys

import numpy as np
import pandas as pd
from skimage.measure import label

if __name__ == "__main__":
    root_path = sys.argv[1] # The folder storing data.csv
    num_control = int(sys.argv[2]) # The number of control you measured
    sd_thresh = sys.argv[3].split() # The threshold of number of sd from the mean

    # Create a result directory if no result directory is found
    result_path = os.path.join(root_path, 'Results')
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    df = pd.read_csv(os.path.join(root_path, 'data.csv'), index_col=0) # Take in the data.csv from parsing the csv file

    # Calculate the average of mean of each control recording
    mean = 0
    for i in range(num_control):
        col_name = df.columns[i]
        mean += df[col_name].mean()
    mean = mean / num_control

    # Calculate the average of sd of each control recording
    sd = 0
    for i in range(num_control):
        col_name = df.columns[i]
        sd += df[col_name].std()
    sd = sd / num_control

    data_list = []

    for item in sd_thresh: # Loop through the sd value for the threshold

        item = float(item) # Turning string into float for the value

        peak_profiles = [item, ] # Initializing a list that will store the peak
        
        threshold = mean + item * sd # Calculate the threshold
        df_threshed = df - threshold # Mask the data with threshold

        #df_threshed.to_csv(os.path.join(result_path, 'raw_data(thresh-mean+{}sd).csv'.format(item))) # Save the thresholded data
        
        df_threshed[df_threshed <= 0] = 0 # Mask any data point below threshold as zero
        
        for col in df_threshed.columns: # Loop through all columns in the data

            temp_arr = label(df_threshed[col].as_matrix()) # Label any contiguous data as a single patch
            num_peak = np.max(temp_arr) # Find the number of peak counted
            peak_profiles.append(num_peak)
        
        data_list.append(peak_profiles)

    if len(sd_thresh) == 1:
        data_list = np.array(data_list, dtype=np.int64).reshape((1, len(peak_profiles)))
    else:
        data_list = np.array(data_list, dtype=np.int64)

        # Save the peak profile
    np.savetxt(os.path.join(result_path, 'peak_count.csv'), \
           data_list, delimiter=',')