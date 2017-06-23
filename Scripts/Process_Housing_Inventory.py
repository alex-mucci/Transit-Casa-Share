import pandas as pd
import geopandas as gp
import geocoder
import numpy as np
from shapely.geometry import Point

YEARS = [2009]
HOUSING_CSV_BASE = 'E:\Transit-Casa-Alex\Input\Housing Inventory/'
CENSUS_BLOCKS = 'E:/Transit-Casa-Alex/Input/2010 Cenusus Shapefiles/2010 Census Blocks/075/tl_2010_06075_tabblock10.shp'

def combine_address(row):
    """
    A function to combine a street address with a city and state (San Francisco, California), so that it can be geocoded using the google API.
    
    row = using the apply method with lambda allows python to iterate through the rows of a dataframe. This takes in one of the rows. 
    
    Example: df['new_column'] = df.apply(lambda row: function(row))
    """
    
    address = str(row['STDADDRESS']) + ' San Francisco, CA'
    return address


def geocode(df,year):
    """
    A funtion that sets the geometry column of a dataframe by geocoding street addresses.
    
    df = dataframe with a column that contains street addresses (ADDRESS)
    """
    #this tests if I have reached the query limit
    print(geocoder.google(df['ADDRESS'][0]))
    
    if year == 2015:
        df['LAT'] = df['Y']
        df['LON'] = df['X']
        
    elif year != 2015:    
        df['LAT'] = df['ADDRESS'].apply(lambda value: geocoder.google(value).lat)
        df['LON'] = df['ADDRESS'].apply(lambda value: geocoder.google(value).lng)
        
    df['geometry'] = [Point(xy) for xy in zip(df.LON, df.LAT)]
    
    return df


def attach_changes(changes,blocks):
    """
    Spatially intersects point features with census blocks and groups the changes, to get total changes for each census block.
    
    changes = geodataframe containing point features with a column containing changes (NETUNITS).
    blocks = geodataframe containing census blocks (polygons) 
    """
    df = gp.sjoin(blocks,changes, how = 'left')
    df = df[['NETUNITS','GEOID10','geometry']].groupby(by = 'GEOID10',as_index = False).agg({'geometry':'first','NETUNITS':'sum'})
    return df


if __name__ == "__main__":
    df2 = gp.GeoDataFrame()
    change_final = gp.GeoDataFrame()
    for year in YEARS:
        changes = pd.read_csv(HOUSING_CSV_BASE + str(year) + '_Housing_Inventory.csv')
        blocks = gp.read_file(CENSUS_BLOCKS)
        print('Processing Year ' + str(year))
        

        if year == 2009:
            print(changes['STREET'].loc[157])
            changes['STREET'].loc[157] = '8TH'
            changes['STDADDRESS'] = changes.apply(lambda row: str(row['NUMBER']) + ' '+ str(row['STREET']) + ' ' + str(row['ST_TYPE']), axis = 1)
            
        elif year == 2011:
            print(changes['STRDADDRESS'].loc[108])
            changes['STRDADDRESS'].loc[108] = '638 8TH AV'
            changes['STDADDRESS'] = changes['STRDADDRESS']
            
        elif year == 2012:
            print(changes['STDADDRESS'].loc[73])
            changes['STDADDRESS'].loc[73] = '1864 8TH AV' 
            
        elif year == 2013:
            print(changes['STDADDRESS'].loc[46])
            print(changes['STDADDRESS'].loc[118])
            print(changes['STDADDRESS'].loc[119])
            changes['STDADDRESS'].loc[46] = '1391 8TH AV'
            changes['STDADDRESS'].loc[118] = '1222 8TH AV'
            changes['STDADDRESS'].loc[119] = '1222 8TH AV'
        elif year == 2014:
            
            changes['STDADDRESS'] = changes['STDADD']   
            
        elif year == 2015:
            changes['STDADDRESS'] = changes['Address']
             
        else:
            print('Bad Year!')
        
        changes['ADDRESS'] = changes.apply(lambda row: combine_address(row),axis = 1)
        changes = geocode(changes,year)
        
        #had to filter out rows that had missing/bad addresses which produced unusable lat longs
       
        drop = changes[np.isnan(changes['LAT']) | np.isnan(changes['LON'])]
        print(drop)
        #changes = changes.drop(drop.index,axis = 0)
        
        changes = gp.GeoDataFrame(changes)
        changes.crs = {'init':'epsg:4326'}
        changes = changes.to_crs({'init':'epsg:4269'})
        
        change_final = change_final.append(changes)
        
        
        changes.to_file( 'E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_housing_units_change.shp',driver = 'ESRI Shapefile')
    df = attach_changes(changes,blocks)
    df.to_csv('E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_HU_Changes.csv')
    df = gp.GeoDataFrame(df)
    df2 = df2.append(df)
    df2.to_file('E:\Transit-Casa-Alex\Output\Housing Inventory/' + str(year) + '_housing_units_change.shp',driver = 'ESRI Shapefile')
    change_final.to_file('E:\Transit-Casa-Alex\Output\Housing Inventory/Net_Change_'+ str(year) + '.shp',driver = 'ESRI Shapefile')
    change_final.to_file('E:\Transit-Casa-Alex\Output\Housing Inventory/Net_Change_'+ str(year) + '.shp',driver = 'ESRI Shapefile')
    print('Completed Year ' + str(year))

        
            
