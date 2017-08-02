import geopandas as gp
import geopandas.tools as tools
import pandas as pd
import csv as csv
import pandas as pd
import numpy as np
from shapely.geometry import Point


BUFFER_SIZES = [1760,1320,528]
YEARS = [2009,2016]
STOPS_PATH09 = 'E:/Transit-Casa-Alex/MUNI Rail/Input/Rail Stops Performance Data/MUNI_Rail_Stops_2009.shp'
STOPS_PATH16 = 'E:/Transit-Casa-Alex/MUNI Rail/Input/Rail Stops Performance Data/MUNI_Rail_Stops_2016.shp'
MODE = 'MUNI Rail'

def make_buffers(stops_df,buffer_size):

    """
    function that creates a buffer around a point feature. Make sure that the projection is in stateplane, may need ARCGIS for this. 
    NAD 1983 GCS for Lat/Lon (for defining projection, if needed) and California Zone 3 for state plane. 
   
    stops_df = dataframe with bus stops and a geometry column
    buffer_outfile = path to where the buffers shapefile is saved
    buffer_size = the size of the buffer (in feet) that is created
    
    """
    
    buffer = stops.copy()
    buffer = buffer.to_crs({'init':'epsg:6420'})
    buffer.geometry = buffer.buffer(buffer_size)
    
    return buffer
   
 
if __name__ == "__main__":

    
    for year in YEARS:
        print('Reading in the Files!')
        
        if year == 2009:
            stops = STOPS_PATH09
            
        elif year == 2016:
            stops = STOPS_PATH16
        
        
        else:
            print('Bad Year')
            
        stops = gp.read_file(stops)    
        for buffer_size in BUFFER_SIZES:
            print('Creating HUGE ' + str(buffer_size) + ' buffers')
            
            stops.crs = {'init':'epsg:4269'}

            stops = stops.drop_duplicates(subset = 'STOP_ID')
                      
            buffers = make_buffers(stops,buffer_size)
            
            if buffer_size == 1760:
                buffers.to_csv('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Quarter.csv')
            elif buffer_size == 1320:
                buffers.to_csv('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Third.csv')
            elif buffer_size == 528:
                buffers.to_csv('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Tenth.csv')
            else:
                print('Bad Buffer Size!')
            
            buffers = buffers.to_crs({'init':'epsg:4269'})
   

            if buffer_size == 1760:
                buffers.to_file('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Quarter_GCS.shp',driver='ESRI Shapefile')
                buffers.to_file('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Quarter_GCS.shp',driver='ESRI Shapefile')
            elif buffer_size == 1320:
                buffers.to_file('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Third_GCS.shp',driver='ESRI Shapefile')
            elif buffer_size == 528:
                buffers.to_file('E:/Transit-Casa-Alex/' + MODE +'/Output/Buffers/' + str(year) + '/Buffers_Tenth_GCS.shp',driver='ESRI Shapefile')
            else:
                print('Bad Buffer Size!')
        print('JUST MADE THIS CODE GREAT AGAIN!')
