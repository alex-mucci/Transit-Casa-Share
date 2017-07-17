import pandas as pd
import geopandas as gp
import numpy as np
from shapely.geometry import Point

YEARS = [2009,2016]

BART09_PATH = 'E:/Transit-Casa-Alex/Output/BART/2009/BART_Intra_SF_Ridership.csv'
BART16_PATH = 'E:/Transit-Casa-Alex/Output/BART/2016/BART_Intra_SF_Ridership.csv'
BART_STATIONS_PATH = 'E:/Transit-Casa-Alex/Output/BART/Stations/SF-SM_BART_Stations.shp'
BART_RENAME = ['STOP_ID', 'geometry', 'BART_FROMS', 'BART_TOS']


CAL09_PATH = 'E:/Transit-Casa-Alex/Output/CalTrain/2009/CalTrain_Ridership.csv'
CAL16_PATH = 'E:/Transit-Casa-Alex/Output/CalTrain/2016/CalTrain_Ridership.csv'
CAL_STATIONS_PATH = 'E:/Transit-Casa-Alex/Output/CalTrain/SF_Caltrain_Stations.shp'
CAL_RENAME = ['STOP_ID', 'geometry','CALTRAIN_ON', 'CALTRAIN_OFF']

MUNI09_PATH = 'E:/Transit-Casa-Alex/Output/Processed MUNI Rail/2009_MUNI_Rail.shp'
MUNI16_PATH = 'E:/Transit-Casa-Alex/Output/Processed MUNI Rail/2016_MUNI_Rail.csv'
MUNI_RENAME = ['STOP_ID','geometry','MUNI_RAIL_BOARDINGS','MUNI_RAIL_ALIGHTINGS']


BIKE16_PATH = 'E:/Transit-Casa-Alex/Input/Bay Area Bike Share/bike_ridership.shp'
BIKE_KEEP = ['STOP_ID', 'geometry', 'Alightings', 'Boardings', 'Dockcount']
BIKE_RENAME = ['STOP_ID', 'geometry', 'BIKE_ALIGHTINGS', 'BIKE_BOARDINGS', 'BIKE_DOCKCOUNT']

BUFFERS_START = 'E:/Transit-Casa-Alex/Output/Buffers/'
BUFFER_ENDS = ['/Tenth/Buffers_Tenth_GCS.shp','/Quarter/Buffers_Quarter_GCS.shp','/Third/Buffers_Third_GCS.shp']


#this was ran before and so for this script the output of this function is used instead of using the function, but I have the code used to create them before below. It is for creating the 2009 stops
def create_stops():

    store = pd.HDFStore('E:\Transit_Casa\Output/gtfs1.h5')
    df = store.get('sfmuni')
    rail_stops = df[df['ROUTE_TYPE'] == 0]
    stops = rail_stops[['STOP_ID','STOP_LAT','STOP_LON','MONTH']]
    stops09 = stops[stops['MONTH'].isin(pd.date_range(start = '2009-01-01',end = '2009-12-31'))]
    stops09 = stops09[['STOP_ID','STOP_LAT','STOP_LON']].groupby(by = 'STOP_ID',as_index = False).mean()
    muni09_merged = pd.merge(stops09,muni09, on = 'STOP_ID',how = 'right')
    muni09_merged['geometry'] = [Point(xy) for xy in zip(muni09_merged.STOP_LON, muni09_merged.STOP_LAT)]
    muni09_geo = gp.GeoDataFrame(muni09_merged)
    muni09_geo.crs = {'init':'epsg:4326'}
    
    
if __name__ == "__main__":
    
    bart_sta = gp.read_file(BART_STATIONS_PATH)
    cal_sta = gp.read_file('E:/Transit-Casa-Alex/Output/CalTrain/SF_Caltrain_Stations.shp')
    for year in YEARS:

            

        
        for buffer_end in BUFFER_ENDS:
            print('Attaching data to ' + ' buffer ' + str(buffer_end))
            buffer_path = BUFFERS_START + str(year) + buffer_end
            buffers = gp.read_file(buffer_path)
            buffers.crs = {'init':'epsg:4269'}

            print('For year ' + str(year))
            if year == 2009:
                bart = pd.read_csv(BART09_PATH)
                cal = pd.read_csv(CAL09_PATH)
                muni = gp.read_file(MUNI09_PATH)
                
            elif year == 2016:
                bart = pd.read_csv(BART16_PATH)
                cal = pd.read_csv(CAL16_PATH)
                muni = pd.read_csv(MUNI16_PATH)
                muni['geometry'] = [Point(xy) for xy in zip(muni.Longitude, muni.Latitude)]
                muni = gp.GeoDataFrame(muni)
                
                
                
            bart = pd.merge(bart_sta[['STATION','geometry']],bart[['Froms','Tos','Station','STATION']],how = 'left',on = 'STATION')

            bart = gp.sjoin(buffers[['STOP_ID','geometry']],bart[['Froms','Tos','geometry']],how = 'left')
            bart = bart.drop('index_right',axis = 1)
            bart.columns =  BART_RENAME
            bart = bart.groupby(by = 'STOP_ID',as_index = False).agg({'BART_FROMS':'sum','BART_TOS':'sum','geometry':'first'})
            
            
           
            
            
            cal = pd.merge(cal_sta[['geometry','STATION']],cal[['STATION','ON','OFF']],on = 'STATION') 
            cal = gp.sjoin(buffers[['STOP_ID','geometry']],cal[['ON','OFF','geometry']],how = 'left')
            cal = cal.drop('index_right',axis = 1)
            cal.columns = CAL_RENAME
            cal = cal.groupby(by = 'STOP_ID',as_index = False).agg({'geometry':'first','CALTRAIN_ON':'sum','CALTRAIN_OFF':'sum'})
            
            
            muni.crs = {'init':'epsg:4269'}
            muni = gp.sjoin(buffers[['STOP_ID','geometry']],muni[['Boardings','Alightings','geometry']],how = 'left')
            muni.Boardings = muni.Boardings.convert_objects(convert_numeric = True)
            muni.Alightings = muni.Alightings.convert_objects(convert_numeric = True)
            muni = muni.drop('index_right',axis = 1)
            muni.columns = MUNI_RENAME
            muni = muni.groupby(by = 'STOP_ID',as_index = False).agg({'geometry':'first','MUNI_RAIL_BOARDINGS':'sum','MUNI_RAIL_ALIGHTINGS':'sum'})
           
            
            
            bike = gp.read_file('E:/Transit-Casa-Alex/Input/Bay Area Bike Share/bike_ridership.shp') 
            bike = gp.sjoin(buffers,bike,how = 'left')
            bike = bike[BIKE_KEEP]
            bike.columns = BIKE_RENAME
            
            bike = bike.groupby(by = 'STOP_ID',as_index = False).agg({'geometry':'first','BIKE_DOCKCOUNT':'sum','BIKE_BOARDINGS':'sum','BIKE_ALIGHTINGS':'sum'})
            
            
            #eventually add in competing bus stops for both years 
            
            if year == 2009:
                #merge everything that is for 2009 except bike share ridership because it is assumed to be 0
                bart = bart.drop('geometry',axis = 1)
                transit = bart.merge(cal.drop('geometry',axis =1),on = 'STOP_ID',how = 'outer').merge(muni.drop('geometry',axis = 1),on = 'STOP_ID',how = 'outer').merge(bike.drop('geometry',axis = 1), on = 'STOP_ID',how = 'outer')
            
            elif year == 2016:
                #merge all 2016 data together
                bart = bart.drop('geometry',axis = 1)
                transit = bart.merge(cal.drop('geometry',axis = 1),on = 'STOP_ID',how = 'outer').merge(muni.drop('geometry',axis =1),on = 'STOP_ID',how = 'outer').merge(bike.drop('geometry',axis = 1), on = 'STOP_ID',how = 'outer')

            #name the combined competing transit file based on the buffer size it is associated with
            if buffer_end == BUFFER_ENDS[0]:
                print('Finished Tenth')
                transit.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' +str(year) + '/Competing Transit Buffers/Tenth_Competing_Transit.csv')
            if buffer_end == BUFFER_ENDS[1]:
                print('Finished Third')
                transit.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' +str(year) + '/Competing Transit Buffers/Third_Competing_Transit.csv')
            if buffer_end == BUFFER_ENDS[2]:
                print('Finished Quarter')
                transit.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' +str(year) + '/Competing Transit Buffers/Quarter_Competing_Transit.csv')
            
    print('ALL DONE TIME FOR SOME HALO!!')