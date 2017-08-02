__author__      = "Alex Mucci"
__copyright__   = "Copyright 2017 UK"
__license__     = """
 
"""
import pandas as pd
import numpy as np
import folium
import sys
sys.path.append('E:\Transit_Casa\Alex\Scripts')
import Muni_Estimates_day as muni
import Map_Function as map

TS_INFILE= "E:/Transit-Casa-Alex/Input/Bus Performence/sfmuni_monthly_ts.h5"
OUTFILE_START = 'E:\Transit-Casa-Alex/'
TABLE = 'stop_day'
MONTH1 = '2009-10-01'
MONTH2 = '2009-11-01'
MONTH3 = '2009-12-01'
MONTH4 = '2016-10-01'
MONTH5 = '2016-11-01'
MONTH6 = '2016-12-01'
COLMN_NAME = 'ON'
TRANSIT_START09 = 'E:/Transit-Casa-Alex/Mapping Data/2009/'
TRANSIT_START16 = 'E:/Transit-Casa-Alex/Mapping Data/2016/'
BUFFERS = ['Tenth','Quarter','Third']

def get_names_avg(colmn_name):
    """
    function that creates the names used later in the script
    
    colmn_name = the name of the data field (column name)
    """
    colmn_name_base = 'AVG' + '_09'
    colmn_name_future = 'AVG' + '_16'
    colmn_per_str = colmn_name + '_P_DIFF_STR'
    colmn_per = colmn_name + '_P_DIFF'
    colmn_diff = colmn_name + '_DIFF'
    return colmn_name_base, colmn_name_future, colmn_per_str, colmn_per, colmn_diff
    
def make_table(hdffile,table,MONTH1,MONTH2,MONTH3):
    """
    pulls and merges the given tables together into one output table from a given h5 file
    
    
    hdffile = string with the h5 file path
    table = string with the desired table 
    output = string with the name of the output dataframe
    MONTH 1-3 = string telling the months that need to be pulled
    """
    
    store = pd.HDFStore(hdffile)
    df = store.get(TABLE)
    df1 = df[df['MONTH'] == MONTH1]
    df2 = df[df['MONTH'] == MONTH2]
    df3 = df[df['MONTH'] == MONTH3]
    
    df_merge = pd.merge(pd.merge(df1,df2,how = 'outer',on='STOP_ID',suffixes = ('_10','_11')),df3,how = 'outer',on='STOP_ID')
    df_final = pd.DataFrame(columns = ['STOP_ID','ON_10','ON_11','ON_12', 'STOP_NAME_10', 'STOP_NAME_11', 'STOP_NAME_12','STOP_LAT','STOP_LON'])
    
# I am assuming that if I am pulling from the same dataframe that the stop id and LAT/LON will be in the same order as the ON columns
    df_final['ON_10'] = df_merge['ON_10']
    df_final['ON_11'] = df_merge['ON_11']
    df_final['ON_12'] = df_merge['ON']
    df_final['STOP_NAME_10'] = df_merge['STOPNAME_10']
    df_final['STOP_NAME_11'] = df_merge['STOPNAME_11']
    df_final['STOP_NAME_12'] = df_merge['STOPNAME']
    
#average the number of ONs and take the first name given to each stop (September's Name)
    df_final['STOP_NAME'] = df_final['STOP_NAME_10']
    df_final['AVG'] = df_final[['ON_10','ON_11','ON_12']].mean(axis = 1)
    
    df_final['STOP_ID'] = df_merge['STOP_ID']
    df_final['STOP_LAT'] = df_merge.apply(lambda row: map.choose_right_latlon(row['STOP_LAT_10'], row['STOP_LAT']), axis=1)
    df_final['STOP_LON'] = df_merge.apply(lambda row: map.choose_right_latlon(row['STOP_LON_10'], row['STOP_LON']), axis=1)
    return df_final
    
if __name__ == "__main__":
    print('Making the Tables!')
    
#make the 09 and 16 tables
    df09 = make_table(TS_INFILE,TABLE, MONTH1, MONTH2, MONTH3) 
    df16 = make_table(TS_INFILE,TABLE, MONTH4, MONTH5, MONTH6)  
    
#merge the 09 and 16 tables    
    df = pd.merge(df09,df16,how = 'outer',on = 'STOP_ID',suffixes = ('_09','_16'))
    
#set the lattitude and longitude of the stops to a central value (i.e. maybe one is month has it missing)
    df['LAT'] = df.apply(lambda row: map.choose_right_latlon(row['STOP_LAT_09'], row['STOP_LAT_16']), axis=1)
    df['LON'] = df.apply(lambda row: map.choose_right_latlon(row['STOP_LON_09'], row['STOP_LON_16']), axis=1)
    
    
    print('Calculating the Difference Columns!')
#set all of the names that will be used later in the script 
    (colmn_name_base, colmn_name_future, colmn_per_str, colmn_per, colmn_diff) = get_names_avg(COLMN_NAME)
    df[colmn_diff] = df[colmn_name_future] - df[colmn_name_base]
    df[colmn_per] = ((df[colmn_name_future] - df[colmn_name_base])/df[colmn_name_base])*100
    df[colmn_per_str] = df[colmn_per].astype(str) + '%'
    show_list = ['STOP_ID',colmn_per,colmn_diff,colmn_name_base,colmn_name_future]

    print('Mapping the Bus Data!')
#issues with colmn_values being skewed severly towards the minimum so all radius sizes will be similar (could increase step size to show more of a change)
    map.map(colmn_name_base,colmn_name_future,colmn_per,colmn_per_str,colmn_diff,df,show_list,OUTFILE_START,TABLE,COLMN_NAME,map.color,map.radius,BUFFERS,TRANSIT_START09,TRANSIT_START16)
    print('ALL DONE!! TIME FOR AN IPA!!!')
