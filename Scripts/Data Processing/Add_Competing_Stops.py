import pandas as pd
import geopandas as gp

MODE = 'MUNI Rail'
STOPS_START = 'E:/Transit-Casa-Alex/Input/Bus_Stops/'
STOPS_END = '/Post-Deleted_Stops/Bus_Stops.shp'

BUFFERS_START  = 'E:/Transit-Casa-Alex/Output/Buffers/'
BUFFERS_ENDS = ['/Tenth/Buffers_Tenth_GCS.shp', '/Third/Buffers_Third_GCS.shp', '/Quarter/Buffers_Quarter_GCS.shp']

YEARS = [2009,2016]

if __name__ == "__main__":

    for year in YEARS:
        print('Working on year ' + str(year))
        
        for buffers_ends in BUFFERS_ENDS:
            print('Processing Buffer ' + buffers_ends)
            
            stops_path = STOPS_START + str(year) + STOPS_END
            stops = gp.read_file(stops_path)
            
            buffer_path = BUFFERS_START + str(year) + buffers_ends
            buffer = gp.read_file(buffer_path)

            buffer.crs = {'init':'epsg:4269'}
            stops.crs = {'init':'epsg:4326'}
            stops = stops.to_crs(buffer.crs)


            joined = gp.sjoin(buffer[['STOP_ID','geometry']],stops[['STOP_LAT','STOP_LON','geometry']],how = 'left')

            comp = joined[['STOP_ID','geometry']].groupby(by = 'STOP_ID',as_index = False).count()
            comp.columns=['STOP_ID','NUM_BUS_STOPS']
            comp.NUM_BUS_STOPS = comp.NUM_BUS_STOPS - 1
            
            
            if buffers_ends == BUFFERS_ENDS[0]:
                comp.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' + str(year) + '/Competing Stops Buffers/Tenth_Comp_Bus_Stops.csv')
            
            elif buffers_ends == BUFFERS_ENDS[1]:
                comp.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' + str(year) + '/Competing Stops Buffers/Third_Comp_Bus_Stops.csv')
            
            elif buffers_ends == BUFFERS_ENDS[2]:
                comp.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' + str(year) + '/Competing Stops Buffers/Quarter_Comp_Bus_Stops.csv')
    
    print('Competition only Makes you Better!')