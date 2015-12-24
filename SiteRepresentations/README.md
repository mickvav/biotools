# Disclaimer #

This small piece of code is intended to solve linear regression problems by numpy.linalg.lstsq method.
Usage:

`./model.py file.csv [Always1]

file.csv is assumed to be tab-delimited text, containing column names in first row and experiment name in first column.
Last two columns in row are for Kr and 1-Kr dependent variables, respectively.
All data from experiment name to Kr is assumed to be the values of independent variables.

Always1 - optional parameter, denoting whether we should add extra column, containing 1 in all rows, to original data. If it's added, Kr is represented in the results. 1-Kr otherwise. 
sudo apt-get install python3-numpy
