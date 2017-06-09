import pandas as pd
import geopandas as gp
import geocoder 
from shapely.geometry import Point

YEARS = [2012,2013,2014]
HOUSING_CSV_BASE = 'E:\Transit-Casa-Alex\Input\Housing Inventory/'
CENSUS_BLOCKS = 'E:/Transit-Casa-Alex/Input/2010 Cenusus Shapefiles/2010 Census Blocks/075/tl_2010_06075_tabblock10.shp'

def combine_address(row):
    address = str(row['STDADDRESS']) + ' San Francisco, CA'
    return address


def set_geometry(df):

    df['LAT'] = df['ADDRESS'].apply(lambda value: geocoder.google(value).lat)
    df['LON'] = df['ADDRESS'].apply(lambda value:  geocoder.google(value).lng)
    print(df['LAT'])
    df['geometry'] = [Point(xy) for xy in zip(df.LON, df.LAT)]
    return df


def attach_changes(changes,blocks):
    changes.crs = blocks.crs

    df = gp.sjoin(changes,blocks, how= 'left')
    df = df[['NETUNITS','GEOID10']].groupby(by = 'GEOID10',as_index = False).sum()
    return df


if __name__ == "__main__":

    for year in YEARS:
        changes = pd.read_csv(HOUSING_CSV_BASE + str(year) + '_Housing_Inventory.csv')
        blocks = gp.read_file(CENSUS_BLOCKS)
        print('Processing Year ' + str(year))
        if year == 2012:
            changes['STDADDRESS'].loc[73] = '1864 8TH AV' 
            changes['ADDRESS'] = changes.apply(lambda row: combine_address(row),axis = 1)
            changes = set_geometry(changes)
            
            changes = gp.GeoDataFrame(changes)
            changes.to_file( 'E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_housing_units_change.shp',driver = 'ESRI Shapefile')
            
            df = attach_changes(changes,blocks)
            df.to_csv('E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_HU_Changes.csv')
            print('Completed Year ' + str(year))

        else:
            changes['ADDRESS'] = changes.apply(lambda row: combine_address(row),axis = 1)
            
            changes = set_geometry(changes)
            
            changes = gp.GeoDataFrame(changes)
            changes.to_file( 'E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_housing_units_change.shp',driver = 'ESRI Shapefile')
            
            df = attach_changes(changes,blocks)
            df.to_csv('E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_HU_Changes.csv')
            print('Completed Year ' + str(year))
