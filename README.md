# Project-1-Pandas
Overview

This code is used to clean and format a dataset containing information about shark attacks. Once cleaned/reformatted, the data is used to produce visualizations supporting/disproving my hypotheses.

Data Cleaning
The code begins by removing unwanted columns and rows with incomplete data from the original dataset. The data is then filtered to only include certain shark species. The index of the data is set to the 'Case Number' column and the date and time columns are cleaned and reformatted. The code also adds a new column called 'Hemisphere' that categorizes each location as being in the Northern or Southern hemisphere.

Exporting the cleaned data
Finally, the cleaned dataset is exported as a new CSV file called attack_clean.csv which can be found in the data folder. This cleaned dataset can be used for further analysis and exploration.

Requirements
This code was written in Python, using the pandas library for data manipulation. To run this code, you will need to have pandas and Python installed on your machine. The original dataset attacks.csv should also be in the same directory as the code file.

Usage
You can run this code by opening it in your Python environment and running it. The cleaned dataset will be saved in the data folder as attack_clean.csv.
