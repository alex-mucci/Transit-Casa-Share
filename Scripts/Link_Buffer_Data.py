import pandas as pd
import geopandas as gp

BUFFERS = ['Tenth','Quarter','Third']
YEARS = ['2009','2016']

PATH_START = 'E:/Transit-Casa-Alex/Output/Final Data/'
OUTFILE_START = 'E:/Transit-Casa-Alex/Output/Modeling'



def link_buffer_data(acs,bus,park,trans,census,comp,edd):
    """
    function to link all of the buffer data together. Starts with the bus dataframe so that only the stops that have ridership data are kept.
    
    acs = dataframe with acs data 
    bus = dataframe with bus data
    park = dataframe with parking data
    trans = dataframe with competing transit dataframe
    census = dataframe with census block data
    comp = dataframe with competing stops data
    census = geodataframe with edd data
    
    """
    df = pd.merge(bus,acs,how = 'left', on = 'STOP_ID')
    df = pd.merge(df,park,how = 'left',on = 'STOP_ID',suffixes = ('','_a'))
    df = pd.merge(df,trans,how = 'left',on = 'STOP_ID',suffixes = ('','_b'))
    df = pd.merge(df,census,how = 'left',on = 'STOP_ID',suffixes = ('','_c'))
    df = pd.merge(df,comp,how = 'left',on = 'STOP_ID',suffixes = ('','_d'))
    df = pd.merge(df,edd,how = 'left',on = 'STOP_ID',suffixes = ('','_e'))
    
    return df
    
    
if __name__ == "__main__":
    for year in YEARS:
        path = PATH_START + year
        acs_path = path + '/ACS_DATA.csv'
        bus_path = path + '/Bus Performance Data.csv'
        park_path = path + '/Parking_Demand.csv'
        
        acs = pd.read_csv(acs_path)
        acs = acs.drop('Unnamed: 0',axis = 1)
        bus = pd.read_csv(bus_path)
        bus = bus.drop('Unnamed: 0',axis = 1)
        park = pd.read_csv(park_path)
        park = park.drop('Unnamed: 0',axis = 1)
    
        for buffer in BUFFERS:
            trans_path = path + '/Competing Transit Buffers/' + buffer + '_Competing_Transit.csv'
            census_path = path + '/Census Block Buffers/' + buffer + '_Census_Block_Estimation_File.csv'
            comp_path = path + '/Competing Stops Buffers/' + buffer + '_Comp_Bus_Stops.csv'
            edd_path = path + '/EDD Buffers/' + buffer + '_EDD.shp'
            
            
            trans = pd.read_csv(trans_path)
            trans = trans.drop('Unnamed: 0',axis = 1)
            census = pd.read_csv(census_path)
            census = census.drop('Unnamed: 0',axis = 1)
            comp = pd.read_csv(comp_path)
            comp = comp.drop('Unnamed: 0',axis = 1)
            edd = gp.read_file(edd_path)



            #merge all of the data together
            data = link_buffer_data(acs,bus,park,trans,census,comp,edd)
            
            outfile_csv = OUTFILE_START + '/' + year + '/' + buffer + '_Data.csv'
            outfile_shp = OUTFILE_START + buffer + '_Data.shp'
            
            #write the table to a csv 
            data.to_csv(outfile_csv)
            
            
            #later need to find a way to save a shapefile of the data too, so that it is easy to overlay on a map in ArcGIS and verify the data
            
            #data = edd[['STOP_ID','geometry']].merge(data, on = 'STOP_ID', how = 'left')
            #data = gp.GeoDataFrame(data,crs = edd.crs,geometry = 'geometry_x')
            #data.to_file(outfile_shp, driver = 'ESRI Shapefile')
            
    print('ALL DONE TIME FOR A BEER!')