__author__      = "Alex Mucci"
__copyright__   = "Copyright 2017 UK"
__license__     = """
    This file is part of .
    
    Come up with my version of what is below:
    
    
    sfdata_wrangler is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    sfdata_wrangler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with sfdata_wrangler.  If not, see <http://www.gnu.org/licenses/>.
"""
import csv as csv
import pandas as pd
import matplotlib.pyplot as plt
from pylab import savefig

#call the script with python 'script name' .py (python 3.5)

#set the constants for the data "input" file and where to write the outfile
TS_INFILE_START     = "E:\Transit_Casa\Alex\C_Drive\MuniEstimation/"
OUTFILE_START = 'E:\Transit_Casa\Alex\C_Drive\MuniPlots/'
TABLE = 'stop_tod'
X = 'ON_09'
Y = 'ON_13'
LIMIT = 100

def get_plot(tod,file,table,x,y,limit):
    """

    Write a comment here about the arguments and what it returns. 
    """
    
    file = file + tod + '_' + table + '.csv'
    df = pd.read_csv(file)
    outfile = OUTFILE_START + tod + '_' + table +'.png'
    fig = df.plot.scatter(x = x, y = y, xlim = [0,limit], ylim = [0,limit])
    savefig(outfile)
    
if __name__ == "__main__":
    tods = ['0300-0559', '0600-0859', '0900-1359', '1400-1559', '1600-1859', '1900-2159', '2200-0259']
        
    for tod in tods: 
        print('Running TOD: ' + tod)
        get_plot(tod,TS_INFILE_START,TABLE, X, Y,LIMIT)   
    
    print('All done!')