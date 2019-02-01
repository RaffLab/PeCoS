# Peak Counting Spectroscopy (PeCoS)
This directory contains two python scripts, namely "parse_fcs.py" and "thresh_fcs.py". "parse_fcs.py" parses through files with ".fcs" extension and combines them into a single ".csv" file. "thresh_fcs.py" finds the threshold from the control recordings of the aforementioned file with ".csv" extension and obtains the peak count after threshold subtraction.

## Getting Started

These instructions will provide you with a copy of the project up and running on your local machine for development and testing purposes. It was developed in macOS Sierra Version 10.12.6 but similar logic may well apply to other systems.

### Installation

Please install anaconda python 2.7 version from [anaconda website](https://www.anaconda.com/download/#macos). Dependencies include scikit-image version 0.13.0, numpy version 1.13.3, and pandas version 0.21.0. The guideline to install dependecies is in [anaconda package management](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html).

## Running and testing the program

### Download the example files

Download the files "A_01.fcs", "A_02.fcs", "A_03.fcs", "B_01.fcs", "B_02.fcs", and "B_03.fcs" from the "Demo" folder in this repository. Save them on your Desktop. Create a new folder called 'Demo'. Place them in the 'Demo' folder of your local machine.

Assuming your terminal is still open and your current directory is "Desktop". Type:  
```
git clone https://github.com/SiuShingWong/FCS-for-low-abundance-protein.git
```

### Running and testing the program
Close all terminal windows. Open terminal again and type:  
```
cd Desktop/FCS-for-low-abundance-protein
```
Press **Enter**, then type:  
```
python parse_fcs.py "/Users/your_user_name_of_computer/Desktop/Demo" 1
```
The command is in the format of **python parse_fcs.py argument_1 argument_2**.

The arguments:

| Name | Description |
| :--- | :-------------------------------------------------------------------------------------------- |
| argument_1 | The location to **.fcs** files. It should be a string enclosed by "". |
| argument_2 | The number of recordings per **.fcs** file |
  
To identify the wanted threshold for background subtraction (that results in less than 5 peaks per control recording), multiple thresholds that vary in "Mean + n*SD" can be subtracted simultaneously by running the following command in the same terminal:  
```
python thresh_fcs.py "/Users/your_user_name_of_computer/Desktop/Demo" 3 "1 2 3 4 5 6 7 8 9 10"
```

The above command has the format of **python thresh_fcs.py argument_1 argument_2 argument_3**.

The arguments:
  
| Name | Description |
| :--- | :-------------------------------------------------------------------------------------------- |
| argument_1 | The location to **data.csv** file generated from the previous command. It should be a string enclosed by "". |
| argument_2 | A positive number specifies the number of control recording used. |
| argument_3 | The number of standard deviations away from the mean that are additionally subtracted. It expects a string of number separated by space and enclosed by "". | 
  
The program will create a folder called **Results** in the "Demo" folder which will contain a **peak_count.csv** file. The number in the first column describes the number of added standard deviations, every following column the peak count of a recording after threshold subtraction (in alphabetical order of the folder).   

### Usage and naming conventions
- Ensure that the number of control recording is correct. If there are 2 control '.fcs' files and each file contains 3 recordings, the total number should be 3*2 = 6. 
- Ensure that all ".fcs" files in the same directory have the same number of recordings per file.
- Ensure that the name of the control is smaller than all other ".fcs" files in the folder. In our case, "A" is always smaller than "B", which determines the "A" series as our control.

## Authors
**Isaac Wong** @ Raff Lab  
email: isaacwongsiushing@gmail.com

## Publication
The script was used in XXX

## Acknowledgements
- Thomas Steinacker for kickstarting the project, providing the theoretical perspectives of PeCoS, reviewing this documentation, and testing the code
- Felix Zhou for testing the code
- Everyone from the Raff Lab
- Sir William Dunn School of Pathology
- Balliol College
- Clarendon Fund
- Cancer Research UK

## License
This project is licensed under MIT LICENSE
