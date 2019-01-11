"""
Created on 8 August 2018
@author: Isaac Wong
@email: isaacwongsiushing@gmail.com

The script and all the code within is licensed under GNU GENERAL PUBLIC LICENSE
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def fuse_near_peak(col, threshold=3):
    """ Read binary pd.Series and close the gap between nearby 1s with distance less that or equal to 3.

    The function was borrowed directly from a MaxU answer from 
    https://datascience.stackexchange.com/questions/20587/find-the-consecutive-zeros-in-a-dataframe-and-do-a-conditional-replacement
    The explanation of the code is provided

    Args:
        col: pd.Series with 1 and 0
        threshold: int

    Returns:
        col: pd.Series with 1 and 0 with the gap between 1s which is under the threshold is closed
    """
    mask = col.groupby((col != col.shift()).cumsum()).transform('count').lt(threshold)
    mask &= col.eq(0)
    col.update(col.loc[mask].replace(0,1))
    return col

sd_thresh=8 # A threshold constructed by the number of standard deviation above the mean
fused = 5 # Maximum step between the adjacent peak
padding = 10 # Number of padding around a peark
want_fig = False

if __name__ == "__main__":

    # Parse the argument from the command line and store them in several variables
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', dest='directory', help='directory of data.csv', type=str, required=True)
    parser.add_argument('-c', dest='num_control', help='number of control recordings', type=int, required=True)
    parser.add_argument('-sd', dest='sd_thresh', help='standard deviation away from the mean (default: 8.0)', type=float, required=False)
    parser.add_argument('-fu', dest='fused', help='step of fusing two near peak (default: 5)', type=int, required=False)
    parser.add_argument('-pd', dest='padding', help='padding around peak (default: 10)', type=int, required=False)
    parser.add_argument('-fg', dest='want_fig', help='If the user would save the figure (default: False)', type=bool, required=False)

    arg = parser.parse_args()

    root_path = arg.directory # The path which contain the image information
    num_control = arg.num_control # The first few files in the directory which serves as control

    # The arguments were explained above.
    if arg.sd_thresh:
        sd_thresh = arg.sd_thresh
    if arg.fused:
        fused = arg.fused
    if arg.padding:
        padding = arg.padding
    if arg.want_fig:
        want_fig = arg.want_fig

    # Create result path in the directory
    result_path = os.path.join(root_path, 'Results')
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    df = pd.read_csv(os.path.join(root_path, 'data.csv'), index_col=0) # Read a pd.DataFrame that called data.csv

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


    threshold = mean + sd_thresh * sd # Calculate the threshold
    df_threshed = df - threshold # Mask the data with threshold

    df_threshed[df_threshed <= 0] = 0 # Convert any point below threshold into 0
    df_threshed[df_threshed > 0] = 1 # Convert any point above threshold into 1
    df_fused = df_threshed.apply(fuse_near_peak, threshold=5) # Apply the peak fusion function to df_threshed in each column

    fcs_data = [] # a list to store the peak information

    for col in df.columns: # Loop through each columns
        
        arr_origin = df[col].as_matrix() # Convert the original column into a 1D np.array
        arr_mask = df_fused[col].as_matrix() # Convert the thresholded column into a 1D np.array
        
        index = np.where(arr_mask == 1) # Find all the location where there is a fused peak

        for i in index[0]: # Loop through all location
            # Some logic towards the start and end of an array
            # The idea is to convert every surrounding of a peak in padding distance into 1
            if i < padding:
                arr_mask[:i] = 1
                arr_mask[i:i + padding] = 1
            elif i + padding + 1 > arr_mask.shape[0]:
                arr_mask[i - padding:i] = 1
                arr_mask[i:] = 1
            else:
                arr_mask[i - padding:i] = 1
                arr_mask[i:i + padding] = 1
                
        index = np.where(arr_mask == 1)[0] # Find the location of the renewed 1s
        fcs_joined = arr_origin[index].tolist() # Convert the sliced array which contains peak into a list
        
        fcs_data.append(fcs_joined) # Append the information into the list

    # This block of code is to find the length of the longest list 
    longest = len(fcs_data[0])
    for data in fcs_data:
        if len(data) > longest:
            longest = len(data)
    time_index = np.arange(0, longest*0.001, 0.001)

    # Pad the end of shorter list with np.nan so that they have the same length as longest array
    fcs_data_saved = []
    for data in fcs_data:
        temp = list(data)
        if len(temp) < longest:
            temp.extend([np.nan]*(longest - len(temp)))
        fcs_data_saved.append(temp)

    # Save the joined peak as csv
    fcs_data_saved = np.array(fcs_data_saved).T
    df_saved = pd.DataFrame(fcs_data_saved, index=time_index)
    df_saved.to_csv(os.path.join(result_path, 'data_joined-peak_fused{0}_padding{1}.csv'.format(fused, padding)))

    # For handling if user would like to save the joined fcs peaks
    if want_fig:

        fig_path = os.path.join(result_path, 'Figure_joined-peak_fused{0}_padding{1}'.format(fused, padding))
        if not os.path.exists(fig_path):
            os.mkdir(fig_path)

        i = 0
        for data in fcs_data:
            fig = plt.figure()
            plt.plot(data)
            fig.savefig(os.path.join(fig_path,'data_{0}_joined-peak_fused{1}_padding{2}.png'.format(i, fused, padding)))
            plt.close(fig)
            i += 1 