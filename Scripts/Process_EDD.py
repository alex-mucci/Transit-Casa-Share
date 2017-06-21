import geopandas as gp

BUFFERS = ['E:/Transit-Casa-Alex/Output/Buffers/Tenth/Buffers_Tenth_GCS.shp','E:/Transit-Casa-Alex/Output/Buffers/Quarter/Buffers_Quarter_GCS.shp','E:/Transit-Casa-Alex/Output/Buffers/Third/Buffers_Third_GCS.shp']
EDD_PATH = 'E:/Transit-Casa-Alex/Input/EDD/EDD_SF_JOBS_2009-2015/SF_JOBS_2009-2015/SF_JOBS_2015_Q4.shp'

YEAR = 2016


if __name__ == "__main__":
    edd = gp.read_file(EDD_PATH)
    year = YEAR
    for buffer in BUFFERS:
        print('Processing Buffer ' + buffer + '!')
        
        buffers = gp.read_file(buffer)
        edd = edd.to_crs(buffers.crs)
        
        if year == 2009:
            joined = gp.sjoin(buffers,edd[['geometry','Q4AVG']],how = 'left')
            
            print('Doing Something Awesome!!!')
            joined_sum = joined[['geometry','STOP_ID','Q4AVG']].groupby(by = 'STOP_ID',as_index = False).agg({'geometry':'first','Q4AVG':'sum'})
            joined_sum.columns = ['STOP_ID','geometry','EDD_EMP']
        
        elif year == 2016: 
            joined = gp.sjoin(buffers,edd[['geometry','Q4_AVG']],how = 'left')
            
            print('Doing Something Awesome!!!')
            joined_sum = joined[['geometry','STOP_ID','Q4_AVG']].groupby(by = 'STOP_ID',as_index = False).agg({'geometry':'first','Q4_AVG':'sum'})
            joined_sum.columns = ['STOP_ID','EDD_EMP','geometry']
        print(joined_sum)
        joined_geo = gp.GeoDataFrame(joined_sum)
        joined_geo.crs = buffers.crs

        if buffer == 'E:/Transit-Casa-Alex/Output/Buffers/Tenth/Buffers_Tenth_GCS.shp':
            joined_geo.to_file('E:/Transit-Casa-Alex/Output/Buffer Data/2016/EDD Buffers (2015)/Tenth_EDD.shp',driver = 'ESRI Shapefile')
            
        elif buffer == 'E:/Transit-Casa-Alex/Output/Buffers/Quarter/Buffers_Quarter_GCS.shp':
            joined_geo.to_file('E:/Transit-Casa-Alex/Output/Buffer Data/2016/EDD Buffers (2015)/Quarter_EDD.shp',driver = 'ESRI Shapefile')
            
        elif buffer == 'E:/Transit-Casa-Alex/Output/Buffers/Third/Buffers_Third_GCS.shp':
            joined_geo.to_file('E:/Transit-Casa-Alex/Output/Buffer Data/2016/EDD Buffers (2015)/Third_EDD.shp',driver = 'ESRI Shapefile')
        else:
            print('Bad Buffer Path!')