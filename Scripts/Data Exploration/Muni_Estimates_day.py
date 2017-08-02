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

#call the script with python 'script name' .py (python 3.5)

#set the constants for the data "input" file and where to write the outfile
TS_INFILE     = "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"
OUTFILE_START = 'E:\Transit_Casa\Alex\C_Drive\MuniEstimation_'
TABLE = 'stop_day'
MONTH1 = '2009-09-01'
MONTH2 = '2013-09-01'

#function splitting a file by time of day and pulling two months out for comparison (for daily totals)

def get_day(hdffile,TABLE,month1, month2):
    """

    Write a comment here about the arguments and what it returns. 
    """
    
    store = pd.HDFStore(hdffile)
    df = store.get(TABLE)
    outfile = OUTFILE_START + TABLE +'.csv'
    
    df1 = df[df['MONTH'] == month1]
    df2 = df[df['MONTH'] == month2]
    
   #the stop tables had stop_id as their unique identifier and required a different key when merging
    if TABLE == 'stop_day':
    # merge the two months for easy comparison of values (outer so that all stops are preserved, nan is filled in for missing stops)
        df = pd.merge(df1,df2, how = 'outer', on = ['DOW', 'AGENCY_ID', 'STOP_ID'], suffixes = ['_09','_13'])
    
    else: 
        df = pd.merge(df1,df2, how = 'outer', on = ['DOW', 'AGENCY_ID', 'ROUTE_SHORT_NAME', 'DIR', 'SEQ'], suffixes = ['_09','_13'])
    
    #sort the columns alphabetically to easily compare values
    df = df.reindex_axis(sorted(df.columns), axis=1)

    #write to the given csv file, set chunksize to prevent memory error
    df.to_csv(outfile, chunksize = 10000)

    
if __name__ == "__main__":
    get_day(TS_INFILE,TABLE, MONTH1, MONTH2) 
    print('All done!')
