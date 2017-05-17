import pandas as pd
import geopandas as gp
import sys
sys.path.append('E:\Transit-Casa-Alex\Scripts')
import Clean_Lodes

#Path to competing bus stops buffer data
TRANS_PATH = 'E:\Transit-Casa-Alex\Output\Buffers\Tenth\Competing Treansit Buffers/Competing_Transit.csv'


#Path to the acs buffer data csv file
ACS_PATH = 'E:\Transit-Casa-Alex\Output\Buffers\Tenth\Buffers_ACS/Buffers_ACS.csv'

#Path to the LEHD and Census buffer data csv file
LEHD_PATH = 'E:/Transit-Casa-Alex/Output/Buffers/Tenth/Census Data Buffers/Normalized to per Acre/Census_Buffers_Acres.csv'

#Path to the Bus performance data H5 file
BUS_PATH = 'E:/Transit_Casa/Output/sfmuni_monthly_ts.h5'

#Date Range of bus data that needs to be pulled 
DATE_RANGE = '2009-01-01', '2009-12-01'

#Outfile path to write the merge table to a csv
OUTFILE = 'E:\Transit-Casa-Alex\Output\Modeling/Buffer10_Data.csv'

DROP_LIST = ['STOP_LAT_y', 'STOP_LON_y','Unnamed: 0','ORIG_FID','BUFF_DIST_y','geometry_y',
        'STOP_LAT_x', 'STOP_LON_x','BUFF_DIST','ALAND10']

def link_buffer_data(acs,lehd,bus,trans):
    df = pd.merge(bus,acs,how = 'left', on = 'STOP_ID')
    df = pd.merge(df,lehd,how = 'left',on = 'STOP_ID',suffixes = ('','_y'))
    return df
    
    
if __name__ == "__main__":
    
    #read in the data
    acs = pd.read_csv(ACS_PATH)
    lehd = pd.read_csv(LEHD_PATH)
    trans = pd.read_csv(TRANS_PATH)
    
    #in the future: will need to change the data range if I am running this for other time periods
    store = pd.HDFStore(BUS_PATH)
    bus = store.get('stop_day')
    bus = bus[bus["MONTH"].isin(pd.date_range('2009-01-01', '2009-12-01'))]

    #drop out the random unnamed column (old index maybe)
    lehd = lehd.drop('Unnamed: 0', axis = 1)
    
    #merge all of the data together
    data = link_buffer_data(acs,lehd,bus,trans)
    
    #drop out the extra columns that are not of interest
    Clean_Lodes.drop_columns(DROP_LIST,data)
    
    #write the table to a csv 
    data.to_csv(OUTFILE)
    
    print('ALL DONE TIME FOR A BEER!')