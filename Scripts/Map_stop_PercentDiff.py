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


TS_INFILE= "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"
OUTFILE_START = 'E:\Transit_Casa\Alex\C_Drive\Maps/'
TABLE = 'stop_day'
MONTH1 = '2009-09-01'
MONTH2 = '2013-09-01'
#may want to write a function in the future to return a list of column names to show, based on the constants given

#make sure you change the show list for each column 
COLMN_NAME = 'ON'

def get_names(colmn_name):
    COLMN_NAME_BASE = colmn_name + '_09'
    COLMN_NAME_FUTURE = colmn_name +'_13'
    COLMN_PER_STR = colmn_name + '_P_DIFF_STR'
    COLMN_PER = colmn_name + '_P_DIFF'
    COLMN_DIFF = colmn_name + '_DIFF'
    return COLMN_NAME_BASE, COLMN_NAME_FUTURE, COLMN_PER_STR, COLMN_PER, COLMN_DIFF
    
    
def get_day(hdffile,table,month1, month2):
    """
    function to pull out two months from the given h5 file and merge them together
    
    hdffile = string path to the h5 file
    table = table that you want to pull from the h5 file
    month1 = the base month you want to pull
    month2 = the future month you want to pull
     
    """
    
    store = pd.HDFStore(hdffile)
    df = store.get(table)
    
    df1 = df[df['MONTH'] == month1]
    df2 = df[df['MONTH'] == month2]
    
#the stop tables had stop_id as their unique identifier and required a different key when merging
    if table == 'stop_day':
# merge the two months for easy comparison of values (outer so that all stops are preserved, nan is filled in for missing stops)
        df = pd.merge(df1,df2, how = 'outer', on = ['DOW', 'AGENCY_ID', 'STOP_ID'], suffixes = ['_09','_13'])
    
    else: 
        df = pd.merge(df1,df2, how = 'outer', on = ['DOW', 'AGENCY_ID', 'ROUTE_SHORT_NAME', 'DIR', 'SEQ'], suffixes = ['_09','_13'])
    
#sort the columns alphabetically to easily compare values
    df = df.reindex_axis(sorted(df.columns), axis=1)
    return df
    
def choose_right_latlon(val1, val2): 
    """
    function to make sure that a lattitude and longitude is given when there is missing values
    """
    if np.isnan(val1): 
        return val2
    else: 
        return val1

def color(colmn_per):
    """
    function to set the color based on the percent difference
    
    coln_per = percent difference value 
    
   
    """
    # if the change is infinity, it means the base is zero.
    # make it equal to the darkest color green
    if np.isinf(colmn_per) == True:
        col='#003300'        
         
    
    # continue to regular values
    elif int(colmn_per) in range (-10000000, -500):
        col='#cc0000'
    elif int(colmn_per) in range (-500, -100):
        col='#ff0000'
    elif int(colmn_per) in range(-100,-75):
        col='#ff3333'
    elif int(colmn_per) in range(-75,-50):
        col='#ff4d4d'
    elif int(colmn_per) in range(-50,-25):
        col='#ff6666'
    elif int(colmn_per) in range(-25,-10):
        col='#ff8080'
    elif int(colmn_per) in range(-10,-5):
        col='#ff9999'
    elif int(colmn_per) in range(-5,5):
        col='DarkGray'
    elif int(colmn_per) in range(5,10):
        col= '#80ff80'
    elif int(colmn_per) in range(10,25):
        col= '#4dff4d'
    elif int(colmn_per) in range(25,50):
        col='#1aff1a'
    elif int(colmn_per) in range(50,75):
        col='#00e600'
    elif int(colmn_per) in range(75,100):
        col='#00b300'
    elif int(colmn_per) in range(100,500):
        col='#008000'
    elif int(colmn_per) in range(500,10000000):
        col='#006600'
    else:
        col='Black'
    return col

def radius(colmn_value):  
        """
        function to set the radius based on the column value (absolute difference)
        
        colmn_value = int value of interest
        """
        if np.isnan(colmn_value):
            rad = 3    
        elif abs(int(colmn_value)) in range(0,10):
            rad = 3
        elif abs(int(colmn_value)) in range(10,25):
            rad = 5
        elif abs(int(colmn_value)) in range(25,100):
            rad = 7
        elif abs(int(colmn_value)) in range(100,500):
            rad = 12
        elif abs(int(colmn_value)) in range(500,1000):
            rad = 18
        elif abs(int(colmn_value)) in range(500,30000000):
            rad = 24
        else:
            print('bad radius1')
            print(colmn_value)
            rad=500
        return rad
        


#function to add marks to the map 
def map(base,future,colmn_per,colmn_diff,colmn_per_str,df,show_list,outfile_start,table,colmn_name,col_func,rad_func):
    """
    function to map all of the stops and add popups to them showing the various values
    
    base = name of the column for base values of interest example: 2009
    future = name of the column for future values of interest example: 2013
    colmn_per = name of the column for percent difference between the base and future values
    colmn_diff = name of the column for absolute difference between the base and future values
    colmn_per_str = the string values of colmn_per
    df = dataframe that houses all of the values
    show_list = list of strings that will be shown in the pop up
    outfile_start = the folder you want to save the map to
    table = the table you want to pull out of the h5 file
    colmn_name = the name of the data field (column of df) that you are interested in 
    col_func = function to set the color of the dots 
    rad_func = function to set the radius of the dots
    """
    #sets the map zoomed into san fran with a scale bar
    mapa = folium.Map([37.775, -122.4813333],
                  zoom_start=13,
                  tiles='cartodbpositron',
                  control_scale = True)
   
   #sets the layers up so that marks can be added to it
    missing_group = folium.FeatureGroup(name = 'Stops with missing data')
    good_group = folium.FeatureGroup(name = 'Stops that passed')

    for name, row in df.iterrows():
            # make all of the bus stops missing in 2009 sea green  (Also includes the ones missing in both, because it is the first if read in)                           
        if np.isnan(row[base]) == True: 
                popup_string =  'Stop ID: '+str(row[show_list[0]])+ '\n' +  '     Percent Difference: ' + str(row[colmn_per]) + '\n' + '    Difference: ' + str(row[colmn_diff]) +'     2009 value: ' + str(row[show_list[3]]) + '\n' +    '2013 value: ' + str(row[show_list[4]])
                folium.CircleMarker([row["LAT"], row["LON"]], 
                                    color='#3CB371',
                                     fill_color='#3CB371', 
                                     radius=rad_func(row[future]),
                                     fill_opacity = 0.3, popup=popup_string).add_to(missing_group)
    # make all of the bus stops missing in 2013 maroon                             
        elif np.isnan(row[future]) == True: 
                popup_string =  'Stop ID: '+str(row[show_list[0]])+ '\n' +  '     Percent Difference: ' + str(row[colmn_per]) + '\n' + '    Difference: ' + str(row[colmn_diff]) +'     2009 value: ' + str(row[show_list[3]]) + '     2013 value: ' + str(row[show_list[4]])
                folium.CircleMarker([row["LAT"], row["LON"]], 
                                     color='#800000',
                                     fill_color='#800000', 
                                     radius=rad_func(row[base]),
                                     fill_opacity = 0.3, popup=popup_string).add_to(missing_group)   
#when both stops have a value of 0 then the percent difference is calculated as a nan and causes issues with the color and radius function
#since the change is 0 (0 to 0) we set the color and radius equal to what it would have been set by the radius and color function (Dark Grey and a radius of 3 map units)                                 
        elif row[future] == 0 and row[base] == 0:
            popup_string =  'Stop ID: '+str(row[show_list[0]])+ '\n' +  '     Percent Difference: ' + str(row[colmn_per]) + '\n' + '    Difference: ' + str(row[colmn_diff]) +'     2009 value: ' + str(row[show_list[3]]) + '     2013 value: ' + str(row[show_list[4]])
            folium.CircleMarker([row["LAT"], row["LON"]], 
                                     color='DarkGray',
                                     fill_color='DarkGray', 
                                     radius= 3,
                                     fill_opacity = 0.3, popup=popup_string).add_to(good_group) 
    #based on percent difference map the bus stop ranging from dark green (high % gain) to light green (medium % gain) to grey (low % gain/loss) to light red (low % loss) to dark red (high % loss)  
        else:
            popup_string =  'Stop ID: '+str(row[show_list[0]])+ '\n' +  '     Percent Difference: ' + str(round(row[colmn_per],2)) + '\n' + '    Difference: ' + str(round(row[colmn_diff],2)) + '\n' +'     2009 value: '+ '\n' + str(round(row[show_list[3]],2)) + '\n' + '     2013 value: ' + str(round(row[show_list[4]],2))
            folium.CircleMarker([row["LAT"], row["LON"]], 
                                     color=col_func(row[colmn_per]), 
                                     fill_color=col_func(row[colmn_per]), 
                                     radius=rad_func(row[colmn_diff]),
                                     fill_opacity = 0.3, popup=popup_string).add_to(good_group)
      

    missing_group.add_to(mapa)
    good_group.add_to(mapa)
    folium.LayerControl().add_to(mapa)
    outfile = outfile_start +table + '_' + colmn_name + '.html'
    mapa.save(outfile)
    
#start here if the script is called into the command prompt
if __name__ == "__main__":

#pull from the h5 file the two months of interest

    df = get_day(TS_INFILE,TABLE, MONTH1, MONTH2) 
#set the lattitude and longitude of the stops to a central value (i.e. maybe one is month has it missing)
    df['LAT'] = df.apply(lambda row: choose_right_latlon(row['STOP_LAT_09'], row['STOP_LAT_13']), axis=1)
    df['LON'] = df.apply(lambda row: choose_right_latlon(row['STOP_LON_09'], row['STOP_LON_13']), axis=1)
    
#set all of the names that are used later in the script
    (colmn_name_base, colmn_name_future, colmn_per_str, colmn_per, colmn_diff) = get_names(COLMN_NAME)
    
#calculate the percent and absolute difference
    df[colmn_diff] = df[colmn_name_future] - df[colmn_name_base]    
    df[colmn_per] = ((df[colmn_name_future] - df[colmn_name_base])/df[colmn_name_base])*100
    df[colmn_per_str] = df[colmn_per].astype(str) + '%'
    
#set the list of values that will be shown in the pop up when you click on a stop
    show_list = ['STOP_ID',colmn_per,colmn_diff,colmn_name_base,colmn_name_future]
    
#map all of the stops 
    map(colmn_name_base,colmn_name_future,colmn_per,colmn_diff,colmn_name_future,df,show_list,OUTFILE_START,TABLE,COLMN_NAME,color,radius)
    print('ALL DONE!! TIME FOR A BEER!!!')