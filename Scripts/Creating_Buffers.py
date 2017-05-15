import geopandas
import geopandas.tools as tools
import pandas as pd
import csv as csv
import pandas as pd
import numpy as np
from shapely.geometry import Point

HDFFILE_PATH = "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"

#could not add in stop names for now, but may want to do that in the future

def grab_stops(hdffile_path): 
    """
    function that pulls out all 3,744 bus stop IDs and Lat/Lons 
    
    hdffile_path = path to the H5 file
    """
    
    store = pd.HDFStore(hdffile_path)
    df = store.select('stop_day', columns = ['STOP_LAT','STOP_LON','STOP_ID'])
    df = df.groupby('STOP_ID').mean()
    #df2 = store.select('stop_day',columns = ['STOP_ID','STOPNAME'], where = 'MONTH=09-1-2009')

    
def LatLon_to_point(df):
    """
    function that converts Lat/Lon columns into a point feature geometry
    
    df = dataframe with Lat/Lon columns
    """
    
df['geometry'] = df.apply(lambda x: Point((float(x.STOP_LON), float(x.STOP_LAT))), axis=1)
stops = gp.GeoDataFrame(df, geometry='geometry', crs = df.crs = "+init=epsg:4326")
stops.to_crs(
stops.to_file('Bus_Stops.shp', driver='ESRI Shapefile')


def make_buffers(stops_df,buffer_outfile,buffer_size):
    """
    function that creates a buffer around a point feature. Make sure that the projection is in stateplane, may need ARCGIS for this. 
    NAD 1983 GCS for Lat/Lon (for defining projection, if needed) and California Zone 3 for state plane. 
   
    stops_df = dataframe with bus stops and a geometry column
    buffer_outfile = path to where the buffers shapefile is saved
    buffer_size = the size of the buffer (in feet) that is created
    
    """
    
    buffer = stops.copy()
    buffer.geometry = stops.buffer(buffer_size)
    buffer.to_file(buffer_outfile, driver='ESRI Shapefile')