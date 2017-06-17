import pandas as pd
import geopandas as gp

#The file paths for the bart files
BART_RIDERSHIP_PATH = 'E:\Transit-Casa-Alex\Input\BART\Bart_Ridership.csv'
BART_STATIONS_PATH = 'E:\Transit-Casa-Alex\Input\BART\Stations\San Francisco/BART_SF_13.shp'
BART_CSV_OUTFILE = 'E:\Transit-Casa-Alex\Output\BART\BART_Ridership.csv'
BART_SHP_OUTFILE = 'E:\Transit-Casa-Alex\Output\BART\BART_Ridership.shp'

#the file paths for the caltrain files
CALTRAIN_RIDERSHIP_PATH = 'E:\Transit-Casa-Alex\Input\Rail Commuter Routes (CalTrain)/CalTrain_Ridership.csv'
CALTRAIN_STATIONS_PATH = 'E:\Transit-Casa-Alex\Input\Rail Commuter Routes (CalTrain)\Stations\San Francisco/RR_Commuter_Sta_13_SF.shp'
CALTRAIN_CSV_OUTFILE = 'E:\Transit-Casa-Alex\Output\CalTrain/CalTrain_Ridership.csv'
CALTRAIN_SHP_OUTFILE = 'E:\Transit-Casa-Alex\Output\CalTrain/CalTrain_Ridership.shp'



if __name__ == "__main__":

    #read in the bart ridership csv and stations shapefile
    bart = pd.read_csv(BART_RIDERSHIP_PATH)
    bart_stations = gp.read_file(BART_STATIONS_PATH,crs = 'crs')
    
    #stations are in the same order so they can be set in this way which gives a unique identifies to link the two tables together with
    bart_stations['Station'] = bart['Station']
    
    #read in the caltrain ridership csv and stations shapefile
    cal = pd.read_csv(CALTRAIN_RIDERSHIP_PATH)
    cal_stations = gp.read_file(CALTRAIN_STATIONS_PATH, crs = 'crs')
    
    bart_merge = pd.merge(bart, bart_stations,how = 'outer', on = 'Station')
    bart_merge.to_csv(BART_CSV_OUTFILE)
    bart_merge_geo = gp.GeoDataFrame(bart_merge)
    bart_merge_geo.to_file(BART_SHP_OUTFILE, driver = 'ESRI Shapefile')
    
    
    cal_merge = pd.merge(cal,cal_stations,how = 'outer',on = 'STATION')
    cal_merge.to_csv(CALTRAIN_CSV_OUTFILE)
    cal_merge_geo = gp.GeoDataFrame(cal_merge)
    cal_merge_geo.to_file(CALTRAIN_SHP_OUTFILE,driver = 'ESRI Shapefile')
    
    print('ALL DONE TIME FOR MONTY PYTHON!')