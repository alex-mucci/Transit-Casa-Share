import pandas as pd
import numpy as np
import geopandas as gp


CENSUS_BLOCK_SHAPEFILE_START = 'E:/Transit-Casa-Alex/Input/2010 Census Blocks/'    
WAC_INFILE = 'E:/Transit-Casa-Alex/Input/LEHD Census Blocks/WAC/Original/ca_wac_S000_JT00_2009.csv'
RAC_INFILE = 'E:/Transit-Casa-Alex/Input/LEHD Census Blocks/RAC/Original/ca_rac_S000_JT00_2009.csv'

#eventually have a shapefile of the entire state and select out only the counties of interest
COUNTYFIPS = ['075','081']
OUTFILE_START = 'E:\Transit-Casa-Alex\Input\LEHD Census Blocks\San Mateo COUNTY/' 
OUTFILE_SHAPE_START = 'E:\Transit-Casa-Alex\Input\LEHD Census Blocks\San Mateo COUNTY/' 

DROP_LEHD_RAC = ['C000', 
    'CA01', 
    'CA02', 
    'CA03', 
    'CE01', 
    'CE02',
    'CE03',
    'CNS01',
    'CNS02',
    'CNS03',
    'CNS04',
    'CNS05',
    'CNS06',
    'CNS07',
    'CNS08',
    'CNS09',
    'CNS10',
    'CNS11',
    'CNS12',
    'CNS13',
    'CNS14',
    'CNS15',
    'CNS16',
    'CNS17',
    'CNS18',
    'CNS19',
    'CNS20',
    'CR01',
    'CR02',
    'CR03',
    'CR04',
    'CR05',
    'CR07',
    'CT01',
    'CT02',
    'CD01',
    'CD02',
    'CD03',
    'CD04',
    'CS01',
    'CS02']
  
#LEHD columns to drop out   
DROP_LEHD_WAC = ['C000', 
    'CA01', 
    'CA02', 
    'CA03', 
    'CE01', 
    'CE02',
    'CE03',
    'CNS01',
    'CNS02',
    'CNS03',
    'CNS04',
    'CNS05',
    'CNS06',
    'CNS07',
    'CNS08',
    'CNS09',
    'CNS10',
    'CNS11',
    'CNS12',
    'CNS13',
    'CNS14',
    'CNS15',
    'CNS16',
    'CNS17',
    'CNS18',
    'CNS19',
    'CNS20',
    'CR01',
    'CR02',
    'CR03',
    'CR04',
    'CR05',
    'CR07',
    'CT01',
    'CT02',
    'CD01',
    'CD02',
    'CD03',
    'CD04',
    'CS01',
    'CS02',
    'CFA01',
    'CFA02',
    'CFA03',
    'CFA04',
    'CFA05',
    'CFS01',
    'CFS02',
    'CFS03',
    'CFS04',
    'CFS05']
    
#census columns to drop out
DROP_CENSUS = ['INTPTLAT10',
'INTPTLON10',
'MTFCC10',
'NAME10',
'STATEFP10',
'TRACTCE10',
'UACE10',
'UATYP10',
'UR10',
'FUNCSTAT10']


def drop_columns(drop_list,df):
    """
    drops out unnecessary columns out of a dataframe 
    
    drop_list = list of columns to drop out of the dataframe
    df = dataframe that the columns will be dropped out of
    """
    for column in drop_list:
        df = df.drop(column,axis = 1)
    return df
        
def clean_lodes(df):
    """
    aggregates employment industries into specific categories
    
    
    df = lodes (wac or rac) data frame 
    """
    
    df['EMP'] = df['C000']
    df['RETAIL'] = df['CNS07']
    df['EDHLTH'] = df['CNS15'] + df['CNS16']
    df['LEISER'] = df['CNS17'] + df['CNS18']
    df['OTHER'] = df['EMP'] - df['RETAIL'] - df['EDHLTH'] - df['LEISER']



if __name__ == "__main__":

    for fips in COUNTYFIPS:
        OUTFILE = OUTFILE_START + fips + '_Employment.csv'
        OUTFILE_SHAPE = OUTFILE_SHAPE_START +  fips + '_Employment.shp'
        CENSUS_BLOCK_SHAPEFILE = CENSUS_BLOCK_SHAPEFILE_START + fips + '/tl_2010_06' + fips + '_tabblock10.shp'
        
    #read in the required files
        blocks = gp.read_file(CENSUS_BLOCK_SHAPEFILE)
        rac = pd.read_csv(RAC_INFILE)
        wac = pd.read_csv(WAC_INFILE)
        
    #set the employment categories
        clean_lodes(wac)
        clean_lodes(rac)
        
    #drop out all of the unnecessary columns
        rac = drop_columns(DROP_LEHD_RAC,rac)
        wac = drop_columns(DROP_LEHD_WAC,wac)
        
        #change the geoid column from a string to an int
        blocks['GEOID10'] = blocks.GEOID10.apply(lambda row: int(row))
    #merge all of the datasets together
        df = pd.merge(blocks,wac,how = 'left',left_on = 'GEOID10',right_on = 'w_geocode')
        df = pd.merge(df,rac,how = 'left',left_on = 'GEOID10',right_on = 'h_geocode',suffixes =('_WAC','_RAC'))
        
        #eventually will need to select by county see comment above next to County FIPS constant 
      #  df = df[df['COUNTYFP10'] == COUNTYFIPS ]
      
    #write the dataframe to a csv
        df.to_csv(OUTFILE)
        
        #write a shapefile of the data 
        shape = gp.GeoDataFrame(df)
        shape.to_file(OUTFILE_SHAPE, driver = 'ESRI Shapefile')
        print('ALL DONE TIME FOR A BEER')