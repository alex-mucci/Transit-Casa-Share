import pandas as pd
import geopandas as gp

START_BUFFER_PATHS = ['E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/','E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/', 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/']

YEAR = 2009

MODE = 'MUNI Rail'

KEEP09 = ['EDHLTH_RAC_SCALED', 'EDHLTH_WAC_SCALED',
       'EMP_RAC_SCALED', 'EMP_WAC_SCALED', 'LEISER_RAC_SCALED',
       'LEISER_WAC_SCALED', 'OTHER_RAC_SCALED', 'OTHER_WAC_SCALED',
       'RETAIL_RAC_SCALED', 'RETAIL_WAC_SCALED',
       'HOUSING_09_SCALED','STOP_ID']
       
SCALE_LIST09 = ['EDHLTH_RAC', 'EDHLTH_WAC',
       'EMP_RAC', 'EMP_WAC', 'LEISER_RAC',
       'LEISER_WAC', 'OTHER_RAC', 'OTHER_WAC',
       'RETAIL_RAC', 'RETAIL_WAC',
       'HOUSING_09']
 
KEEP16 = ['EDHLTH_RAC_SCALED', 'EDHLTH_WAC_SCALED',
       'EMP_RAC_SCALED', 'EMP_WAC_SCALED', 'LEISER_RAC_SCALED',
       'LEISER_WAC_SCALED', 'OTHER_RAC_SCALED', 'OTHER_WAC_SCALED',
       'RETAIL_RAC_SCALED', 'RETAIL_WAC_SCALED',
       'HOUSING16_SCALED','STOP_ID']
       
SCALE_LIST16 = ['EDHLTH_RAC', 'EDHLTH_WAC',
       'EMP_RAC', 'EMP_WAC', 'LEISER_RAC',
       'LEISER_WAC', 'OTHER_RAC', 'OTHER_WAC',
       'RETAIL_RAC', 'RETAIL_WAC','HOUSING16'] 
       
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
    year = YEAR
    
    buffers = [START_BUFFER_PATHS[0] + str(year) + '/Split Buffers/Split_Buffers_Tenth.csv',START_BUFFER_PATHS[1] + str(year) + '/Split Buffers/Split_Buffers_Quarter.csv',
               START_BUFFER_PATHS[2] + str(year) + '/Split Buffers/Split_Buffers_Third.csv']
               
    for buffer in buffers:
        print('Processing buffer ' + str(buffer))
        
        year = YEAR
        
        if year == 2009:
            scale_list = SCALE_LIST09
            keep = KEEP09
            
        elif year == 2016:
            scale_list = SCALE_LIST16
            keep = KEEP16
        
        else:
            print('This year has not been formatted!')
        
        print('Reading in the files!')
        
        split = pd.read_csv(buffer)
        
        print('Scaling the Data!')
        split_scaled = scale(scale_list, split, keep)
        
        print('Saving all Files!')
        
        if buffer == buffers[0]:
            split_scaled.to_csv('E:/Transit-Casa-Alex/' + MODE + '/Output/Tenth_Census_Block_Estimation_File.csv')
        
        elif buffer == buffers[1]:
            split_scaled.to_csv('E:/Transit-Casa-Alex/' + MODE + '/Output/Third_Census_Block_Estimation_File.csv')
        
        elif buffer == buffers[2]:
            split_scaled.to_csv('E:/Transit-Casa-Alex/' + MODE + '/Output/Quarter_Census_Block_Estimation_File.csv')
    print('ALL DONE TIME FOR MONTY PYTHON!')