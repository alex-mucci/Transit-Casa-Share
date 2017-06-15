import pandas as pd
import geopandas as gp


CENSUS_DATA_PATH = 'E:/Transit-Casa-Alex/Input/2010 Population (Blocks)/Population_Houses_Blocks.shp'
LEHD_DATA_PATH = 'E:/Transit-Casa-Alex/Input\LEHD Census Blocks/2009/Combined Employment/Combined Employment.csv'

CSV_OUTFILE = 'E:/Transit-Casa-Alex/Output/Census Block Data/Census_Block_Data.csv'
SHP_OUTFILE = 'E:/Transit-Casa-Alex/Output/Census Block Data/Census_Block_Data.shp'

def link_census_data(pop,emp):
    """
    function that links the lehd census block data with the population/housing unit census block data
    
    pop = population/housing unit census block dataframe
    emp = LEHD census block dataframe
    """
    
    pop = pop.to_crs({'init' : 'epsg:6420'})
    pop['ALAND10'] = pop['geometry'].area

    pop.BLOCKID10 = pop.BLOCKID10.astype(float)
    df = pd.merge(pop,emp, how = 'outer', left_on = 'BLOCKID10',right_on = 'GEOID10')
    
    return df
    
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
    pop = gp.read_file(CENSUS_DATA_PATH)
    emp = pd.read_csv(LEHD_DATA_PATH)
    
    df = link_census_data(pop,emp)
    geo = create_geo(df)
    
    df.to_csv(CSV_OUTFILE)
    geo.to_file(SHP_OUTFILE,driver = 'ESRI Shapefile')
    
    print('TOO EASY!')