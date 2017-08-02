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
MONTH2 = '2016-09-01'
#may want to write a function in the future to return a list of column names to show, based on the constants given

#make sure you change the show list for each column 
COLMN_NAME = 'ON'

def get_names(colmn_name):
    COLMN_NAME_BASE = colmn_name + '_09'
    COLMN_NAME_FUTURE = colmn_name +'_16'
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
        print('Bad Color')
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
        elif abs(int(colmn_value)) in range(1000,30000000):
            rad = 24
        else:
            print('Bad Radius')
            print(colmn_value)
            rad=150
        return rad
        


#function to add marks to the map 
def map(base,future,colmn_per,colmn_per_str,colmn_diff,df,show_list,outfile_start,table,colmn_name,col_func,rad_func,BUFFERS,TRANSIT_START09,TRANSIT_START16):
    """
    function to map all of the stops and add popups to them showing the various values
    
    base = name of the column for base values of interest example: 2009
    future = name of the column for future values of interest example: 2013
    colmn_per = name of the column for percent difference between the base and future values
    colmn_per_str = string of percent difference so that the percentage sign is included (%)
    colmn_diff = name of the column for absolute difference between the base and future values
    df = dataframe that houses all of the values
    show_list = list of strings that will be shown in the pop up
    outfile_start = the folder you want to save the map to
    table = the table you want to pull out of the h5 file
    colmn_name = the name of the data field (column of df) that you are interested in 
    col_func = function to set the color of the dots 
    rad_func = function to set the radius of the dots
    """


    #sets the map zoomed into san fran with a scale bar
    mapa = folium.Map([37.765, -122.45],
                  zoom_start=13,
                  tiles='openstreetmap',
                  control_scale = True)
   
   #sets the layers up so that marks can be added to it (NEED TO CHANGE WHEN THE DATA IM MAPPING CHANGES!!!)
    missing09_group = folium.FeatureGroup(name = 'Stops with Missing Boardings in 2009')
    missing16_group = folium.FeatureGroup(name = 'Stops with Missing Boardings in 2016')
    missing_both_group = folium.FeatureGroup(name = 'Stops with Missing Boardings in Both Years')
    good_group = folium.FeatureGroup(name = 'Bus Stops with Complete Boardings')
    
    missing_both = 0
    missing09 = 0
    missing16 = 0
    good = 0
    
    for name, row in df.iterrows():
        #make all of the stops missing in both years purple with a radius of 20 
        if np.isnan(row[base]) & np.isnan(row[future]):
            html= """ <h2> STOP """ + str(row[show_list[0]]) + """  </h2>             
            <p> 
            2009 Name: Missing  <br>
            2016 Name: Missing </p> 
            <p> 
            Percent Difference: N/A <br>             
            Difference: N/A </p>             
            <p>    2009 Value: Missing   <br>             
            2016 Value: Missing </p> """
            
            iframe = folium.IFrame(html=html, width=300, height=150)
            pop_up = folium.Popup(iframe, max_width=2650)
            
            folium.CircleMarker([row["LAT"], row["LON"]], 
                                    color='Purple',
                                     fill_color='Purple', 
                                     radius= 5,
                                     fill_opacity = 0.3, popup=pop_up).add_to(missing_both_group)

            missing_both = missing_both + 1


        # make all of the bus stops missing in 2009 sea green             
        elif np.isnan(row[base]) == True: 
             
            if pd.isnull(row['STOP_NAME_16']):
                row['STOP_NAME_16'] = 'Missing '
            else:
                html= """ <h2> STOP """ + str(row[show_list[0]]) + """  </h2>             
                <p> 
                2009 Name: Missing  <br>
                2016 Name: """ + row['STOP_NAME_16'] + """ </p> 
                <p> 
                Percent Difference: N/A <br>             
                Difference: N/A </p>             
                <p>    2009 Value: Missing   <br>             
                2016 Value: """ + str(round(row[show_list[4]])) + """ </p> """
                
                iframe = folium.IFrame(html=html, width=300, height=150)
                pop_up = folium.Popup(iframe, max_width=2650)
                
                folium.CircleMarker([row["LAT"], row["LON"]], 
                                        color='#3CB371',
                                         fill_color='#3CB371', 
                                         radius=rad_func(row[future]),
                                         fill_opacity = 0.3, popup=pop_up).add_to(missing09_group)
                
                missing09 = missing09 + 1
                                     
    # make all of the bus stops missing in 2016 maroon                             
        elif np.isnan(row[future]) == True: 

            if pd.isnull(row['STOP_NAME_09']):
                row['STOP_NAME_09'] = 'Missing '
            else:    
                html="""
                <h2> STOP """ + str(row[show_list[0]]) + """  </h2>
                <p> 
                2009 Name: """ + row['STOP_NAME_09'] + """  <br>
                2016 Name: Missing </p> 
                <p> 
                Percent Difference: N/A <br>
                Difference: N/A </p>
                <p> 
                2009 Value: """ + str(round(row[show_list[3]])) + """ <br>
                2016 Value: Missing </p>"""
                
                iframe = folium.IFrame(html=html, width=300, height=150)
                pop_up = folium.Popup(iframe, max_width=2650)

                folium.CircleMarker([row["LAT"], row["LON"]], 
                                         color='#800000',
                                         fill_color='#800000', 
                                         radius=rad_func(row[base]),
                                         fill_opacity = 0.3, popup=pop_up).add_to(missing16_group)
                                         
                                     
                missing16 = missing16 + 1
                
#when both stops have a value of 0 then the percent difference is calculated as a nan and causes issues with the color and radius function
#since the change is 0 (0 to 0) we set the color and radius equal to what it would have been set by the radius and color function (Dark Grey and a radius of 3 map units)                                 
        elif row[future] == 0 and row[base] == 0:
            if pd.isnull(row['STOP_NAME_09']):
                row['STOP_NAME_09'] = 'Missing '
            elif pd.isnull(row['STOP_NAME_16']):
                row['STOP_NAME_16'] = 'Missing '
            else:
                html="""
                <h2> STOP """ + str(row[show_list[0]]) + """  </h2>
                <p> 
                2009 Name: """ + row['STOP_NAME_09'] + """  <br>
                <br>
                2016 Name: """ + row['STOP_NAME_16'] + """ </p> 
                <p> 
                Percent Difference: 0% <br>
                Difference: """ + str(round(row[colmn_diff])) + """ </p>
                <p> 2009 Value: """ + str(round(row['AVG_09'])) + """ <br>
                2016 Value: """ + str(round(row['AVG_16'])) + """ </p> """
                
                iframe = folium.IFrame(html=html, width=300, height=150)
                pop_up = folium.Popup(iframe, max_width=2650)
                
                folium.CircleMarker([row["LAT"], row["LON"]], 
                                         color='DarkGray',
                                         fill_color='DarkGray', 
                                         radius= 5,
                                         fill_opacity = 0.3, popup=pop_up).add_to(good_group) 

            
    #based on percent difference map the bus stop ranging from dark green (high % gain) to light green (medium % gain) to grey (low % gain/loss) to light red (low % loss) to dark red (high % loss)  
        else:
            #takes care of a bug when there is a stop name in one year but not the other and a bug of having an infinite percent difference when the base year is zero 
            if row[base] == 0:
                row[base] = 0.00001              
                row[colmn_per] = ((row[future] - row[base])/row[base])*100
                
            if pd.isnull(row['STOP_NAME_09']):
                row['STOP_NAME_09'] = 'Missing '
            elif pd.isnull(row['STOP_NAME_16']):
                row['STOP_NAME_16'] = 'Missing '
            else:
                count = 0
                html="""
                <h2> STOP: """ + str(row[show_list[0]]) + """  </h2>
                <p> 
                2009 Name: """ + row['STOP_NAME_09'] + """  <br>
                <br>
                2016 Name: """ + row['STOP_NAME_16'] + """ </p> 
                <p> 
                Percent Difference: """ + str(round(row[colmn_per])) + """%
                <br>
                Difference: """ + str(round(row[colmn_diff])) + """
                </p>
                <p>
                2009 Value: """ + str(round(row['AVG_09'])) + """
                <br>
                2016 Value: """ + str(round(row['AVG_16'])) + """
                </p>"""
                
                iframe = folium.IFrame(html=html, width=300, height=150)
                pop_up = folium.Popup(iframe, max_width=2650)
                
                folium.CircleMarker([row["LAT"], row["LON"]], 
                                         color=col_func(row[colmn_per]), 
                                         fill_color=col_func(row[colmn_per]), 
                                         radius=rad_func(row[colmn_diff]),
                                         fill_opacity = 0.3, popup=pop_up).add_to(good_group)
                                         
                
                good = good + 1
                
    print(str(missing09) + ' Stops Missing in 2009.')
    print(str(missing16) + ' Stops Missing in 2016.')
    print(str(missing_both) + ' Stops Missing in Both Years.')
    print(str(good) + ' Stops that are in Both Years.')
    
    missing09_group.add_to(mapa)
    missing16_group.add_to(mapa)
    missing_both_group.add_to(mapa)
    good_group.add_to(mapa)
   
    
    

    
    
    #This section is completely separate. To have the layer control work correctly all layers had to be added at the same time. 

    
    print('Processing Competing Transit!')
  
    buffer = 'Quarter'
    transit09 = pd.read_csv(TRANSIT_START09 + buffer + '_Mapping_Comp_Transit.csv', thousands = ',')
    transit16 = pd.read_csv(TRANSIT_START16 + buffer + '_Mapping_Comp_Transit.csv', thousands = ',')
    merged_transit = pd.merge(transit09,transit16,how = 'outer',on = 'STOP_ID',suffixes =('_09','_16'))
    merged_transit['STOP_ID'] = merged_transit['STOP_ID'].astype(str)
    transit = pd.merge(merged_transit, df[['STOP_ID','LAT','LON']],how = 'left',on = 'STOP_ID')
    
    #had to convert BART data from strings to integers
    
    transit['BART_FROMS_09'] = transit['BART_FROMS_09'].apply(lambda value: float(value))
    transit['BART_FROMS_16'] = transit['BART_FROMS_16'].apply(lambda value: float(value))
    
    transit['bart_diff'] = round(transit['BART_FROMS_09'] - transit['BART_FROMS_16'])
    transit['muni_diff'] = round(transit['MUNI_RAIL_BOARDINGS_09'] - transit['MUNI_RAIL_BOARDINGS_16'])
    transit['cal_diff'] = round(transit['CALTRAIN_ON_09'] - transit['CALTRAIN_ON_16'])
   
   
    quarter_group = folium.FeatureGroup(name = 'Competing Transit (Quarter-Mile Buffers)')
    for row in transit.iterrows():
        html ="""<h2> STOP: """ + str(row[1]['STOP_ID']) + """ </h2> <br>
        BART Difference: """ + str(row[1]['bart_diff']) + """ <br>
        MUNI Rail Difference: """ + str(row[1]['muni_diff']) + """ <br>
        CalTrain Difference: """ + str(row[1]['cal_diff']) + """ <br>
        <br>
        <br>
        2009 BART Boardings: """ + str(row[1]['BART_FROMS_09']) + """ <br>
        2009 CalTrain Boardings: """ + str(row[1]['CALTRAIN_ON_09']) + """ <br>
        2009 MUNI Rail Boardings: """ + str(row[1]['MUNI_RAIL_BOARDINGS_09']) + """ <br> 
        <br>
        2016 BART Boardings: """ + str(row[1]['BART_FROMS_16']) + """ <br>
        2016 CalTrain Boardings: """ + str(row[1]['CALTRAIN_OFF_16']) + """ <br>
        2016 MUNI Rail Boardings: """ + str(row[1]['MUNI_RAIL_BOARDINGS_16']) + """ <br> """ 
        iframe = folium.IFrame(html=html, width=300, height=150)
        pop_up = folium.Popup(iframe, max_width=2650)
    
        folium.CircleMarker([row[1]["LAT"], row[1]["LON"]], 
            color='#ffd2b3',
            fill_color='#ffd2b3', 
            radius= 5,
            fill_opacity = 0.3, popup=pop_up).add_to(quarter_group)
                 
                 
                 
                 
     #added in the bart stations here
    print('Adding BART Stations!')
    
    bart_group = folium.FeatureGroup(name = 'BART Stations')
    bart = pd.read_csv('E:/Transit-Casa-Alex/Output/BART/Map Data/Map_Data.csv',thousands = ',')
    
    for row in bart.iterrows():
        
        html ="""<h2> STOP: """ + str(row[1]['STATION']) + """ </h2> <br>
        BART Difference: """ + str(row[1]['FROM_DIFF']) + """ <br>
        BART Percent Difference: """ + row[1]['FROM_P_DIFF_STR'] + """
        <br>
        <br>
        2009 BART Boardings: """ + str(row[1]['Froms_09']) + """ <br>
        2016 BART Boardings: """ + str(row[1]['Froms_16'])
        
        iframe = folium.IFrame(html=html, width=300, height=150)
        pop_up = folium.Popup(iframe, max_width=2650)
    
        folium.CircleMarker([row[1]["LAT"], row[1]["LON"]], 
            color= col_func(row[1]['FROM_P_DIFF']),
            fill_color = col_func(row[1]['FROM_P_DIFF']), 
            radius= rad_func(row[1]['FROM_DIFF']),
            fill_opacity = 0.3, popup=pop_up).add_to(bart_group)
    
    
    
    
     #added in the MUNI Rail stations here. Only the stations that operate in both years are shown. (Drops out about 10 stops)
    print('Adding MUNI Rail Stations!')
    
    rail_group = folium.FeatureGroup(name = 'MUNI Rail Stations')
    rail = pd.read_csv('E:/Transit-Casa-Alex/Output/Processed MUNI Rail/MUNI_Rail_Map_Data.csv',thousands = ',')
    
    for row in rail.iterrows():
        
        html ="""<h2> STOP: """ + str(row[1]['STOP_ID']) + """ </h2> <br>
        Stop Name: """ +row[1]['STOP_NAME'] + """ <br>
        RAIL Difference: """ + str(row[1]['DIFF']) + """ <br>
        RAIL Percent Difference: """ + row[1]['P_DIFF_STR'] + """
        <br>
        <br>
        2009 RAIL Boardings: """ + str(int(row[1]['Boardings_09'])) + """ <br>
        2016 RAIL Boardings: """ + str(int(row[1]['Boardings_16']))
        
        iframe = folium.IFrame(html=html, width=300, height=150)
        pop_up = folium.Popup(iframe, max_width=2650)
        
        folium.CircleMarker([row[1]["LAT"], row[1]["LON"]], 
            color= col_func(row[1]['P_DIFF']),
            fill_color = col_func(row[1]['P_DIFF']), 
            radius= rad_func(row[1]['DIFF']),
            fill_opacity = 0.3, popup=pop_up).add_to(rail_group)   
    
    
    #leaving out the quater mile transit buffers because it causes the layer control to disappear and it isnt really needed
    rail_group.add_to(mapa)
    bart_group.add_to(mapa)
    #quarter_group.add_to(mapa)
    folium.TileLayer('cartodbpositron').add_to(mapa)
    
    folium.LayerControl().add_to(mapa)
    

    outfile = outfile_start +table + '_' + colmn_name + '.html'
    mapa.save(outfile)
    
    return mapa
    
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
    df[colmn_per_str] = str(df[colmn_per].astype(int)) + '%'
    
#set the list of values that will be shown in the pop up when you click on a stop
    show_list = ['STOP_ID',colmn_per,colmn_diff,colmn_name_base,colmn_name_future]
    
#map all of the stops 
    map(colmn_name_base,colmn_name_future,colmn_per,colmn_diff,colmn_name_future,df,show_list,OUTFILE_START,TABLE,COLMN_NAME,color,radius)
    print('ALL DONE!! TIME FOR A BEER!!!')