import pandas as pd
import numpy as np
import folium
import sys
sys.path.append('E:\Transit_Casa\Alex\Scripts')
import Muni_Estimates_day as muni

from Map_Function import color
from Map_Function import radius 
from Map_Function import choose_right_latlon

INFILE09 = 'E:/Transit-Casa-Alex/Output/Modeling/2009/Diff_Mapping_Data.csv'
INFILE16 = 'E:/Transit-Casa-Alex/Output/Modeling/2016/Diff_Mapping_Data.csv'

OUTFILE = 'E:/Transit-Casa-Alex/Output/Modeling/Growth_Diff_Map.html'



def map(stop_id,base,future,colmn_per,colmn_per_str,colmn_diff,df,col_func,rad_func,lat,lon):
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
                  tiles='cartodbpositron',
                  control_scale = True)
   
   #sets the layers up so that marks can be added to it (NEED TO CHANGE WHEN THE DATA IM MAPPING CHANGES!!!)
    missing_both_group = folium.FeatureGroup(name = 'Stops With Missing Data')
    good_group = folium.FeatureGroup(name ='Ridership Growth Difference (Modeled Growth - Observed Growth)')
    
    for name, row in df.iterrows():
        #make all of the stops missing in both years purple with a radius of 20 
        if np.isnan(row[base]) & np.isnan(row[future]):
            html= """ <h2> STOP """ + str(row[stop_id]) + """  </h2>             
            <p> 
            2009 Name: Missing  <br>
            2016 Name: Missing </p> 
            <p> 
            Percent Difference: N/A <br>             
            Difference: N/A </p>             
            <p>  
            2009 Value: Missing   <br>             
            2016 Value: Missing </p> """
            
            iframe = folium.IFrame(html=html, width=300, height=150)
            pop_up = folium.Popup(iframe, max_width=2650)
            
            folium.CircleMarker([row[lat], row[lon]], 
                                    color='Purple',
                                     fill_color='Purple', 
                                     radius= 5,
                                     fill_opacity = 0.3, popup=pop_up).add_to(missing_both_group)


                                     
                                     
#when both stops have a value of 0 then the percent difference is calculated as a nan and causes issues with the color and radius function
#since the change is 0 (0 to 0) we set the color and radius equal to what it would have been set by the radius and color function (Dark Grey and a radius of 3 map units)                                 
        elif row[future] == 0 and row[base] == 0:
           # if pd.isnull(row['STOP_NAME_09']):
                #row['STOP_NAME_09'] = 'Missing '
            #elif pd.isnull(row['STOP_NAME_16']):
                #row['STOP_NAME_16'] = 'Missing '
           
            html="""
            <h2> STOP """ + str(row[stop_id]) + """  </h2>
            <p> 
            2009 Name: """ + row['STOPNAME_09'] + """  <br>
            <br>
            2016 Name: """ + row['STOPNAME_16'] + """ </p> 
            <p> 
            Percent Difference: 0% <br>
            Difference: """ + str(round(row[colmn_diff])) + """ </p>
            <p> 
            Observed Change: """ + str(round(row[base])) + """ <br>
            Modeled Change: """ + str(round(row[future])) + """ </p> """
            
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
                
            #if pd.isnull(row['STOP_NAME_09']):
                #row['STOP_NAME_09'] = 'Missing '
            #elif pd.isnull(row['STOP_NAME_16']):
                #row['STOP_NAME_16'] = 'Missing '
            
            
            html="""
            <h2> STOP: """ + str(row[stop_id]) + """  </h2>
            <p> 
            2009 Name: """ + row['STOPNAME_09'] + """  <br>
            <br>
            2016 Name: """ + row['STOPNAME_16'] + """ </p> 
            <p> 
            Percent Difference: """ + str(round(row[colmn_per])) + """%
            <br>
            Difference: """ + str(round(row[colmn_diff])) + """
            </p>
            <p>
            Observed Change: """ + str(round(row[base])) + """
            <br>
            Modeled Change: """ + str(round(row[future])) + """
            </p>"""
            
            iframe = folium.IFrame(html=html, width=300, height=150)
            pop_up = folium.Popup(iframe, max_width=2650)
            
            folium.CircleMarker([row[lat], row[lon]], 
                                     color=col_func(row[colmn_per]), 
                                     fill_color=col_func(row[colmn_per]), 
                                     radius=rad_func(row[colmn_diff]),
                                     fill_opacity = 0.3, popup=pop_up).add_to(good_group)
                                         
                                         

    missing_both_group.add_to(mapa)
    good_group.add_to(mapa)
    folium.LayerControl().add_to(mapa)

    return mapa
    
    
if __name__ == "__main__":
    
    df09 = pd.read_csv(INFILE09,index_col = 0)
    df16 = pd.read_csv(INFILE16,index_col = 0)
    
    df = pd.merge(df09,df16, how = 'inner', on = 'STOP_ID',suffixes = ('_09','_16'))
    
    
    df['LAT'] = df.apply(lambda row: choose_right_latlon(row['STOP_LAT_09'], row['STOP_LAT_16']), axis=1)
    df['LON'] = df.apply(lambda row: choose_right_latlon(row['STOP_LON_09'], row['STOP_LON_16']), axis=1)
    
    df['DIFF_OBS'] = df.AVG_RIDE_16 - df.AVG_RIDE_09
    df['DIFF_MOD'] = df.PRED_AVG_RIDERSHIP_16 - df.PRED_AVG_RIDERSHIP_09
    df['GROWTH_DIFF'] = df.DIFF_MOD - df.DIFF_OBS
    df['GROWTH_PDIFF'] = (df['GROWTH_DIFF']/np.absolute(df['DIFF_OBS']))*100

    
    
    df['COLUMN_PER_STR'] = df['GROWTH_PDIFF'].apply(lambda x : str(x) + '%')
    print('Mapping Your Differences!')
    mapa = map('STOP_ID','DIFF_OBS','DIFF_MOD','GROWTH_PDIFF','COLUMN_PER_STR','GROWTH_DIFF',df,color,radius,'LAT','LON')
    print('Settling Your Differences!!')
    mapa.save(OUTFILE)
    print('Time for some Panda Express!')
    
    