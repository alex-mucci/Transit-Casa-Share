import pandas as pd
import geopandas as gp
import numpy as np


BART09_PATH = 'E:/Transit-Casa-Alex/Output/BART/2009/BART_Ridership.csv'
BART16_PATH = 'E:/Transit-Casa-Alex/Output/BART/2016/BART_Ridership.csv'
BART_STATIONS_PATH = 'E:/Transit-Casa-Alex/Output/BART/SF-SM_BART_Stations.shp'
BART_RENAME = ['STOP_ID', 'geometry', 'BART_FROMS', 'BART_TOS']


CAL09_PATH = 'E:/Transit-Casa-Alex/Output/CalTrain/2009/CalTrain_Ridership.csv'
CAL16_PATH = 'E:/Transit-Casa-Alex/Output/CalTrain/2016/CalTrain_Ridership.csv'
CAL_STATIONS_PATH = 'E:/Transit-Casa-Alex/Output/CalTrain/SF_Caltrain_Stations.shp'
CAL_RENAME = ['STOP_ID', 'geometry','CALTRAIN_ON', 'CAL_TRAIN_OFF']


BIKE16_PATH = 'E:/Transit-Casa-Alex/Input/Bay Area Bike Share/bike_ridership.shp'
BIKE_KEEP = ['STOP_ID', 'geometry', 'Alightings', 'Boardings', 'Dockcount']

BUFFERS = ['E:/Transit-Casa-Alex/Output/Buffers/Tenth/Buffers/Buffers_Tenth_GCS.shp',
           'E:/Transit-Casa-Alex/Output/Buffers/Quarter/Buffers_Quarter_GCS.shp',
           'E:/Transit-Casa-Alex/Output/Buffers/Third/Buffers_Third_GCS.shp']


if __name__ == "__main__":
    count = 0
    for buffer in BUFFERS:
        print('Attaching data to ' + ' buffer ' + 'buffers)
        buffer = gp.read_file(buffer)
        bart_sta = gp.read_file(BART_STATIONS_PATH)
        for year in YEARS:
            if year == 2009:
                bart = pd.read_csv(BART09_PATH)
                cal = pd.read_csv(CAL09_PATH)
            elif year == 2016:
                bart = pd.read_csv(BART16_PATH)
                cal = pd.read_csv(CAL16_PATH)
            
            bart = pd.merge(bart_sta[['STATION','geometry']],bart[['Froms','Tos','Station','STATION']],how = 'left',on = 'STATION')

            bart = gp.sjoin(buffer[['STOP_ID','geometry']],bart[['Froms','Tos','geometry']],how = 'left')
            bart = bart.drop('index_right',axis = 1)
            bart.columns =  BART_RENAME
           
            
            
            cal = pd.merge(cal_sta[['geometry','STATION']],cal[['STATION','ON','OFF']],on = 'STATION') 
            cal = gp.sjoin(buffer[['STOP_ID','geometry']],cal[['ON','OFF','geometry']],how = 'left')
            cal = cal.drop('index_right',axis = 1)
            cal.columns = CAL_RENAME
            
            
            
            muni =
            
            
            bike = gp.read_file('E:/Transit-Casa-Alex/Input/Bay Area Bike Share/bike_ridership.shp') 
            bike = gp.sjoin(buffers,bike,how = 'left')
            bike = bike[BIKE_KEEP]
            
            if year == 2009:
                #merge everything 2009 except bike because it is assumed to be 0
                
            elif yera == 2016:
                #merge all 2016 data together
            #name the combined competing transit file based on the buffer size it is associated with
            if count == 0:
                transit.to_csv('E:/Transit-Casa-Alex/Output/Buffer Data/Competing Transit Buffers/year/Tenth_Competing_Transit.csv')
            if count == 1:
                transit.to_csv('E:/Transit-Casa-Alex/Output/Buffer Data/Competing Transit Buffers/year/Third_Competing_Transit.csv')
            if count == 2:
                transit.to_csv('E:/Transit-Casa-Alex/Output/Buffer Data/Competing Transit Buffers/year/Quarter_Competing_Transit.csv')