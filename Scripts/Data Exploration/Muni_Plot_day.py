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
TS_INFILE_START     = "E:\Transit_Casa\Alex\C_Drive\MuniEstimation\MuniEstimation_"
OUTFILE_START = 'E:\Transit_Casa\Alex\C_Drive\MuniPlots/'
TABLE = 'stop_day'
X = 'ON_09'
Y = 'ON_13'
LIMIT = 500

def get_plot(file,table,x,y,limit):
    """

    Write a comment here about the arguments and what it returns. 
    """
    
    file = file + table + '.csv'
    df = pd.read_csv(file)
    outfile = OUTFILE_START + table +'.png'
    fig = df.plot.scatter(x = x, y = y, xlim = [0,limit], ylim = [0,limit])
    savefig(outfile)
    
if __name__ == "__main__":
    get_plot(TS_INFILE_START,TABLE, X, Y,LIMIT) 
    print('All done!')