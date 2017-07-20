import geopandas as gp

BUFFERS_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/'
BUFFERS_ENDS = ['/Tenth/Buffers_Tenth_GCS.shp', '/Quarter/Buffers_Quarter_GCS.shp', '/Third/Buffers_Third_GCS.shp']
MODE = 'MUNI Rail'

# could not use the year variable because the 2016 edd data is actually for 2015. It is the most recent data that was available

EDD_PATH_START_09 = 'E:/Transit-Casa-Alex/Input/EDD/EDD_SF_JOBS_2009-2015/SF_JOBS_2009-2015/SF_JOBS_2009_Q4.shp'
EDD_PATH_START_16 = 'E:/Transit-Casa-Alex/Input/EDD/EDD_SF_JOBS_2009-2015/SF_JOBS_2009-2015/SF_JOBS_2015_Q4.shp'

YEARS = [2009,2016]


if __name__ == "__main__":
    for y in YEARS:
        print('Processing Year ' + str(y))
        
        year = y
        if year == 2009:
            qavg = 'Q4AVG'
            edd_path = EDD_PATH_START_09
            
        elif year == 2016:
            qavg = 'Q4_AVG'
            edd_path = EDD_PATH_START_16
            
        edd = gp.read_file(edd_path)

        for buffer in BUFFERS_ENDS:
            print('Processing Buffer ' + buffer + '!')
            
            buffers = gp.read_file(BUFFERS_START + str(year) + buffer)
            buffers.crs = {'init':'epsg:4269'}
            
            edd = edd.to_crs(buffers.crs)
            


            joined = gp.sjoin(buffers,edd[['geometry',qavg]],how = 'left')
            print('Doing Something Awesome!!!')
            joined_sum = joined[['geometry','STOP_ID',qavg]].groupby(by = 'STOP_ID',as_index = False).agg({'geometry':'first',qavg:'sum'})
            
            joined_sum['EDD_EMP'] = joined_sum[qavg]
            joined_sum = joined_sum.drop(qavg,axis = 1)
        
            joined_geo = gp.GeoDataFrame(joined_sum)
            joined_geo.crs = buffers.crs

            if buffer == BUFFERS_ENDS[0]:
                joined_geo.to_file('E:/Transit-Casa-Alex/' + MODE + '/Output/Final Data/' + str(year) + '/EDD Buffers/Tenth_EDD.shp',driver = 'ESRI Shapefile')
                
            elif buffer == BUFFERS_ENDS[1]:
                joined_geo.to_file('E:/Transit-Casa-Alex/' + MODE + '/Output/Final Data/' + str(year) + '/EDD Buffers/Quarter_EDD.shp',driver = 'ESRI Shapefile')
                
            elif buffer == BUFFERS_ENDS[2]:
                joined_geo.to_file('E:/Transit-Casa-Alex/' + MODE + '/Output/Final Data/' + str(year) + '/EDD Buffers/Third_EDD.shp',driver = 'ESRI Shapefile')
            else:
                print('Bad Buffer Path!')