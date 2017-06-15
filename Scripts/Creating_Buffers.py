import geopandas
import geopandas.tools as tools
import pandas as pd
import csv as csv
import pandas as pd
import numpy as np
from shapely.geometry import Point

HDFFILE_PATH = "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"
MONTH1 = '2016-10-01'
MONTH2 = '2016-12-01'
BUFFER_SIZES = [1760,1320,528]


#could not add in stop names for now, but may want to do that in the future

def grab_stops(hdffile_path): 
    """
    function that pulls out all 3,744 bus stop IDs and Lat/Lons 
    
    hdffile_path = path to the H5 file
    """
    
    store = pd.HDFStore(hdffile_path)
    df = store.select('stop_day', columns = ['STOP_LAT','STOP_LON','STOP_ID'])
    mask = (df['MONTH'] >= MONTH1) & (df['MONTH'] <= MONTH2)
    df = df.loc[mask]
    df = df.groupby('STOP_ID',as_index = False).mean()
    
    return df
    
def LatLon_to_point(df):
    """
    function that converts Lat/Lon columns into a point feature geometry
    
    df = dataframe with Lat/Lon columns
    """
    
    df['geometry'] = df.apply(lambda x: Point((float(x.STOP_LON), float(x.STOP_LAT))), axis=1)
    stops = gp.GeoDataFrame(df, geometry='geometry', crs = {'init':'epsg:4326'})
    
    return stops
    


def make_buffers(stops,buffer_size):
    """
    function that creates a buffer around a point feature. Make sure that the projection is in stateplane, may need ARCGIS for this. 
    NAD 1983 GCS for Lat/Lon (for defining projection, if needed) and California Zone 3 for state plane. 
   
    stops_df = dataframe with bus stops and a geometry column
    buffer_outfile = path to where the buffers shapefile is saved
    buffer_size = the size of the buffer (in feet) that is created
    
    """
    
    buffer = stops.copy()
    buffer = buffer.to_crs({'init':'epsg 6420'})
    buffer.geometry = buffer.buffer(buffer_size)
    print(buffer.crs)
   
   
    
if __name__ == "__main__":
    df = grab_stops("E:/Transit_Casa/Output/sfmuni_monthly_ts.h5")
    df2.to_csv('E:/Transit-Casa-Alex/Input/Bus_Stops/Bus_Stops.csv')
    
    stops = LatLon_to_point(df)
    stops.to_file('E:/Transit-Casa-Alex/Input/Bus_Stops/Bus_Stops.shp', driver='ESRI Shapefile')
    
    for buffer_size in BUFFER_SIZES:
        buffers = make_buffers(stops,buffer_size)
        
        
        if buffer_size == 1760:
            buffers.to_file('E:/Transit-Casa-Alex/Output/Buffers/Quarter_Buffers.shp',driver='ESRI Shapefile')
        elif buffer_size == 1320:
            buffers.to_file('E:/Transit-Casa-Alex/Output/Buffers/Third_Buffers.shp',driver='ESRI Shapefile')
        elif buffer_size == 528:
            buffers.to_file('E:/Transit-Casa-Alex/Output/Buffers/Tenth_Buffers.shp',driver='ESRI Shapefile')
        else:
            print('Bad Buffer Size!')