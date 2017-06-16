import pandas as pd
import geopandas as gp

SPLIT_BUFFER_PATHS = ['E:/Transit-Casa-Alex/Output/Buffers/Split Buffers/2010_Split_Buffers_Tenth.shp',
'E:/Transit-Casa-Alex/Output/Buffers/Split Buffers/2010_Split_Buffers_Quarter.shp', 
'E:/Transit-Casa-Alex/Output/Buffers/Split Buffers/2010_Split_Buffers_Third.shp']

KEEP = ['EDHLTH_RAC_SCALED', 'EDHLTH_WAC_SCALED',
       'EMP_RAC_SCALED', 'EMP_WAC_SCALED', 'LEISER_RAC_SCALED',
       'LEISER_WAC_SCALED', 'OTHER_RAC_SCALED', 'OTHER_WAC_SCALED',
       'RETAIL_RAC_SCALED', 'RETAIL_WAC_SCALED', 'POP10_SCALED',
       'HOUSING10_SCALED','STOP_ID']
       
SCALE_LIST = ['EDHLTH_RAC', 'EDHLTH_WAC',
       'EMP_RAC', 'EMP_WAC', 'LEISER_RAC',
       'LEISER_WAC', 'OTHER_RAC', 'OTHER_WAC',
       'RETAIL_RAC', 'RETAIL_WAC', 'POP10',
       'HOUSING10']
       
       
def scale(scale_list,df,keep):
    """
    function that scales a list of columns by a specified column (SPLIT_RATIO) and selects out columns of interest.
    
    scale_list = a list of column names that need to be scaled (string)
    df = dataframe that contains the columns needing to be scaled and a scaler-column (SPLIT_RATIO)
    keep = a list of columns that are of interest at the end. Filters out the unscalled columns. 
    
    """
    for column in scale_list:
        name = column + '_SCALED'
        df[name] = df[column]*df['SPLIT_RATIO']

    df2 = df[keep].groupby(by = 'STOP_ID',as_index = False).sum()
    return df2





if __name__ == "__main__":
    for buffer in SPLIT_BUFFER_PATHS:
        print('Processing buffer ' + str(buffer))
        split = gp.read_file(buffer)
        split_scaled = scale(SCALE_LIST, split, KEEP)
        split_scaled.to_csv('E:/Transit-Casa-Alex/Output/Census_Block_Estimation_File.csv')
    print('ALL DONE TIME FOR MONTY PYTHON!')