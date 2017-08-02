import pandas as pd
import geopandas as gp
import numpy as np
from shapely.geometry import Point

HDFFILE_PATH_09 = "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"
MONTHS_09 = ['2009-10-01','2009-11-01','2009-12-01']
TABLE_09 = 'stop_day'
COLUMNS_09 = ['STOP_ID','STOP_LAT','STOP_LON']

HDFFILE_PATH_16 = "E:/sfdata_wrangler2/out/gtfs.h5"
MONTHS_16 = ['2016-08-13T00:00:00.000000000']
TABLE_16 = 'sfmuni'
COLUMNS_16 = ['STOP_ID','STOP_LAT','STOP_LON','ROUTE_TYPE','DOW','AGENCY_ID']
YEAR = 2016
MODE = 0


def grab_stops(hdffile_path,months,table,columns,year, mode): 
    """
    function that pulls out all 3,744 bus stop IDs and Lat/Lons 
    
    hdffile_path = path to the H5 file
    
    months = list of months you want to pull out of the H5 file
    
    mode = the route type number to select out a specific mode (0 = Rail, 1 =  , 3 = Bus, 5 = Cable Car)
    """
    df_out = pd.DataFrame()
    store = pd.HDFStore(hdffile_path)
    for m in months: 
        print(m)
        df = store.select(table,where="MONTH=m")
        
        df_out = df_out.append(df[columns])
        
   #used the gtfs for 2016 and needed to filter out the data to only include busses operating during the week. 2009 data was already filtered
    if year == 2016:
        df_out = df_out[(df_out['AGENCY_ID'] == 'SFMTA') & (df_out['ROUTE_TYPE'] == mode) & (df_out['DOW'] == 1)]
    elif year == 2009:
        df_out = df_out
        
    df_out = df_out.groupby('STOP_ID',as_index = False).mean()
    print(len(df_out))
    return df_out
    
def LatLon_to_point(df):
    """
    function that converts Lat/Lon columns into a point feature geometry
    
    df = dataframe with Lat/Lon columns
    """
    
    df['geometry'] = df.apply(lambda x: Point((float(x.STOP_LON), float(x.STOP_LAT))), axis=1)
    stops = gp.GeoDataFrame(df, geometry='geometry', crs = {'init':'epsg:4326'})
    
    return stops
    

    
    
if __name__ == "__main__":
    year = YEAR
    
    if year == 2009:
        hdf = HDFFILE_PATH_09
        months = MONTHS_09
        table = TABLE_09
        columns = COLUMNS_09
        
    elif year == 2016:
        hdf = HDFFILE_PATH_16
        months = MONTHS_16
        table = TABLE_16
        columns = COLUMNS_16
    else:
        print('This year has not been formatted yet')
        
    print('Reading in the Files!')
    df = grab_stops(hdf,months,table,columns,year,MODE)
    
 
    if MODE == 3:
        df.to_csv('E:/Transit-Casa-Alex/Input/Bus_Stops/' + str(year) + '/Bus_Stops.csv')
        
        print('Creating Tremendous Point Features!')
        stops = LatLon_to_point(df)
        stops.to_file('E:/Transit-Casa-Alex/Input/Bus_Stops/' + str(year) + '/Bus_Stops.shp', driver='ESRI Shapefile')
    
    elif MODE === 0:
        df.to_csv('E:/Transit-Casa-Alex/Input/Rail Stops/' + str(year) + '/Rail_Stops.csv')
        
        print('Creating Tremendous Point Features!')
        stops = LatLon_to_point(df)
        stops.to_file('E:/Transit-Casa-Alex/Input/Rail Stops/' + str(year) + '/Rail_Stops.shp', driver='ESRI Shapefile')
    
    print('TOO EASY!')
    
    
