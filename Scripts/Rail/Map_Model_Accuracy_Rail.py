import pandas as pd
import numpy as np
import folium
import sys
sys.path.append('E:\Transit_Casa\Alex\Scripts')
import Muni_Estimates_day as muni

from Map_Function import color
from Map_Function import radius 


INFILE_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Modeling/'
INFILE_END = '/Diff_Mapping_Data_Post_Process.csv'
OUTFILE_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Modeling/'
OUTFILE_END = '/Diff_Map.html'


YEAR = 2016



def map(stop_id,stop_name,housing_name,modeled,observed,colmn_per,colmn_per_str,colmn_diff,df,col_func,rad_func,lat,lon):
    """
    function to map all of the stops and add popups to them showing the various values
    
    modeled = name of the column for modeled values of interest
    observed = name of the column for observed values of interest
    colmn_per = name of the column for percent difference between the modeled and observed
    colmn_per_str = string of percent difference so that the percentage sign is included (%)
    colmn_diff = name of the column for absolute difference between the modeled and observed values
    df = dataframe that houses all of the values
    col_func = function to set the color of the markers 
    rad_func = function to set the radius of the markers
    lat = column name containing the latitudes of the stops
    lon = column name containing the longitudes of the stops 
    
    """


    #sets the map zoomed into san fran with a scale bar
    mapa = folium.Map([37.765, -122.45],
                  zoom_start=13,
                  tiles='cartodbpositron',
                  control_scale = True)
   
   #sets the layers up so that marks can be added to it (NEED TO CHANGE WHEN THE DATA IM MAPPING CHANGES!!!)

    good_group = folium.FeatureGroup(name = 'Modeled vs. Observed Average Ridership (Tenth-Mile & Buffer Route Stop Data)')
    
    for name, row in df.iterrows():

        #takes care of a bug when there is a stop name in one year but not the other and a bug of having an infinite percent difference when the base year is zero 
        if row[observed] == 0:
            row[observed] = 0.00001              
            row[colmn_per] = ((row[modeled] - row[observed])/row[observed])*100
            
        else:
            row[observed] = row[observed]
        html="""
        <h2> STOP: """ + str(row[stop_id]) + """  </h2>
        <p> 
        Stop Name: """ + row[stop_name] + """  <br>
        </p> 
        <p> 
        Percent Difference: """ + str(round(row[colmn_per])) + """%
        <br>
        Difference: """ + str(round(row[colmn_diff])) + """
        </p>
        <p>
        Modeled Value: """ + str(round(row[modeled])) + """
        <br>
        Observed Value: """ + str(round(row[observed])) + """
        </p>
        <br>
        <h3> VALUES </h3> 
        Employment (Log): """ + str(row['EDD_EMP_LOG']) + """ <br>
        Frequency (Log): """ + str(row['FREQ_S_LOG']) + """ <br>
        EOL_SOL (Dummy): """ + str(row['EOL_SOL']) + """ <br>
        Housing Density (Log): """ + str(row[housing_name]) + """ <br>
        BART Ridership (Log): """ + str(row['AVG_BART_LOG']) + """ <br>
        Close Stop (Dummy): """ + str(row['CLOSE_STOP']) + """ <br>
        MUNI Bus Ridership: """ + str(row['MUNI_BUS_AVG']) + """ <br>
        </p>"""
        
        iframe = folium.IFrame(html=html, width=300, height=150)
        pop_up = folium.Popup(iframe, max_width=2650)
        
        folium.CircleMarker([row[lat], row[lon]], 
                                 color=col_func(row[colmn_per]), 
                                 fill_color=col_func(row[colmn_per]), 
                                 radius=rad_func(row[colmn_diff]),
                                 fill_opacity = 0.3, popup=pop_up).add_to(good_group)
                                     
                                     

    good_group.add_to(mapa)
    
    return mapa
    
    
if __name__ == "__main__":
    if YEAR == 2009:
        stop_name = 'STOP'
        housing_name = 'HOUSING_09_DEN_LOG'
    elif YEAR == 2016:
        stop_name = 'STOP NAME'
        housing_name = 'HOUSING_16_DEN_LOG'
    else:
        print('Bad Year')
        
    df = pd.read_csv(INFILE_START + str(YEAR) + INFILE_END,index_col = 0)
    df = df.dropna()
    df['COLUMN_PER_STR'] = df['PDIFF_AVG_RIDE'].apply(lambda x : str(x) + '%')
    print('Mapping Your Differences!')
    mapa = map('STOP_ID',stop_name,housing_name,'PRED_AVG_RIDERSHIP','AVG_RIDE','PDIFF_AVG_RIDE','COLUMN_PER_STR','DIFF_AVG_RIDE',df,color,radius,'STOP_LAT','STOP_LON')
    print('Settling Your Differences!!')
    mapa.save(OUTFILE_START + str(YEAR) + OUTFILE_END)
    print('Time for some Panda Express!')
    
    