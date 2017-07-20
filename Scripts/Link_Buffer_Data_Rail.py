import pandas as pd
import geopandas as gp
import numpy as np
BUFFERS = ['Tenth','Quarter','Third']
YEARS = ['2009','2016']

PATH_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Final Data/'
OUTFILE_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Modeling'


def link_buffer_data(acs,rail,park,trans,census,comp,edd,transbay):
    """
    function to link all of the buffer data together. Starts with the rail dataframe so that only the stops that have ridership data are kept.
    
    acs = dataframe with acs data 
    rail = dataframe with rail data
    park = dataframe with parking data
    trans = dataframe with competing transit dataframe
    census = dataframe with census block data
    comp = dataframe with competing stops data
    census = geodataframe with edd data
    
    """
    
    df = pd.merge(rail,acs,how = 'left', on = 'STOP_ID')
    df = pd.merge(df,park,how = 'left',on = 'STOP_ID',suffixes = ('','_a'))
    df = pd.merge(df,trans,how = 'left',on = 'STOP_ID',suffixes = ('','_b'))
    df = pd.merge(df,census,how = 'left',on = 'STOP_ID',suffixes = ('','_c'))
    df = pd.merge(df,comp,how = 'left',on = 'STOP_ID',suffixes = ('','_d'))    
    df = pd.merge(df,transbay,how = 'left',on = 'STOP_ID',suffixes = ('','_e'))
    df = pd.merge(df,edd, how = 'left', left_on = 'STOP_ID',right_on = 'STOP_ID', suffixes = ('','_f'))
    return df
    
    
if __name__ == "__main__":
    for year in YEARS:
        path = PATH_START + year
        acs_path = path + '/ACS_DATA.csv'
        rail_path = path + '/MUNI_Rail_Stops_' + year + '.csv'
        park_path = path + '/' + year + '_Parking_Demand.csv'
        
        acs = pd.read_csv(acs_path)
        acs = acs.drop('Unnamed: 0',axis = 1)
        rail = pd.read_csv(rail_path)
        rail = rail.drop('Unnamed: 0',axis = 1)
        park = pd.read_csv(park_path)
        park = park.drop('Unnamed: 0',axis = 1)
    
        for buffer in BUFFERS:
            trans_path = path + '/Competing Transit Buffers/' + buffer + '_Competing_Transit.csv'
            census_path = path + '/Census Block Buffers/' + buffer + '_Census_Block_Estimation_File.csv'
            comp_path = path + '/Competing Stops Buffers/' + buffer + '_Comp_Bus_Stops.csv'
            edd_path = path + '/EDD Buffers/' + buffer + '_EDD.shp'
            transbay_path = path + '/Transbay Buffers/Buffers_Transbay_' + buffer + '.shp'
            
            trans = pd.read_csv(trans_path)
            trans = trans.drop('Unnamed: 0',axis = 1)
            census = pd.read_csv(census_path)
            census = census.drop('Unnamed: 0',axis = 1)
            comp = pd.read_csv(comp_path)
            comp = comp.drop('Unnamed: 0',axis = 1)
            edd = gp.read_file(edd_path)
            transbay = gp.read_file(transbay_path)

            edd.STOP_ID = edd.STOP_ID.convert_objects(convert_numeric = True)
            transbay.STOP_ID = transbay.STOP_ID.convert_objects(convert_numeric = True)
            
            #merge all of the data together
            data = link_buffer_data(acs,rail,park,trans,census,comp,edd,transbay)
            
            outfile_csv = OUTFILE_START + '/' + year + '/' + buffer + '_Data.csv'
            outfile_shp = OUTFILE_START + buffer + '_Data.shp'
            
            #write the table to a csv 
            data.to_csv(outfile_csv)
            
            
            #later need to find a way to save a shapefile of the data too, so that it is easy to overlay on a map in ArcGIS and verify the data
            
            #data = edd[['STOP_ID','geometry']].merge(data, on = 'STOP_ID', how = 'left')
            #data = gp.GeoDataFrame(data,crs = edd.crs,geometry = 'geometry_x')
            #data.to_file(outfile_shp, driver = 'ESRI Shapefile')
            
    print('ALL DONE TIME FOR A BEER!')