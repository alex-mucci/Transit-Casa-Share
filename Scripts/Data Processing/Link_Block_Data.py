import pandas as pd
import geopandas as gp
import numpy as np


YEAR = 2016
CENSUS_DATA_START = 'E:/Transit-Casa-Alex/Output/Housing Units/' 
CENSUS_DATA_END = '/SF_Housing.shp'

LEHD_DATA_START = 'E:/Transit-Casa-Alex/Output/LEHD/'
LEHD_DATA_START = 'E:/Transit-Casa-Alex/Output/LEHD/'
LEHD_DATA_END = '/SF_Employment.csv'

CSV_OUTFILE = 'E:/Transit-Casa-Alex/Output/Census Block Data/Census_Block_Data.csv'
SHP_OUTFILE = 'E:/Transit-Casa-Alex/Output/Census Block Data/Census_Block_Data.shp'

KEEP = 'BLOCKID10','HOUSING16','BLOCK_ID','EDHLTH_RAC_1','EMP_WAC_16'

def link_census_data(pop,emp):
    """
    function that links the lehd census block data with the population/housing unit census block data
    
    pop = population/housing unit census block dataframe
    emp = LEHD census block dataframe
    """
    
    pop.crs = {'init':'epsg:4269'}
    pop = pop.to_crs({'init' : 'epsg:6420'})
    pop['ALAND10'] = pop['geometry'].area

    pop.BLOCKID10 = pop.BLOCKID10.astype(float)

    df = pop.merge(emp, how = 'left', left_on = 'BLOCKID10', right_on = 'BLOCK_ID')

    return df
    
    #this function is not used, but I was planning on using it and see it as something useful and worth keeping moving forward. 
    
def clean_id(row,clean1,clean2,id):
    """
    This is a function to clean missing values from two columns. Example: if a census block id column has missing values in one id but does have an id in another (after a merge) then this will
    select the column with the non-missing Block ID. 
    
    row = a row of a dataframe passed to this function using the .apply(lambda row: function(row)) method
    clean1 = one of the column names that is to be checked
    clean2 = the other column name to be checked
    id = the column that you want the non-missing values to go to 
    
    """
    if np.isnan(row[clean1]):
        row[id] = row[clean2]
        
    elif np.isnan(row[clean1]) & np.isnan(row[clean2]):
        print('bad row')
        
    else:
        row[id] = row[clean1] 
    return row[id]
    

def create_geo(df):
    """
    function that takes a df and creates a geodataframe
    
    df = dataframe with a geometry column
    """
    
    geo = gp.GeoDataFrame(df,geometry = 'geometry_x')
    geo.crs = {'init' : 'epsg:6420'}
    geo = geo.to_crs({'init': 'epsg:4269'})
    
    return geo
    
if __name__ == "__main__":
    year = YEAR
    print('Reading in the Files!')

    pop_path = CENSUS_DATA_START + str(year) + CENSUS_DATA_END
    emp_path = LEHD_DATA_START + str(year) + LEHD_DATA_END
    
    pop = gp.read_file(pop_path)
    emp = pd.read_csv(emp_path)
    
    print('Linking the Census Data Together!')
    df = link_census_data(pop,emp)
    
    print('Creating and Saving the Geodataframe!')
    geo = create_geo(df)
    

    df.to_csv(CSV_OUTFILE)
    geo.to_file(SHP_OUTFILE,driver = 'ESRI Shapefile')
    
    print('TOO EASY!')