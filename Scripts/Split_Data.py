import geopandas as gp
import pandas as pd
import datetime
import numpy as np

#set which buffer shapefiles that are going to be processed
BUFFERS_START = ['E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/' , 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/', 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/']
BUFFERS_START = ['E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/' , 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/', 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/']

#change the paths to do a different set of census blocks or to save the output in a different directory
BLOCKS_START = 'E:/Transit-Casa-Alex/Output/Census Block Data/'
BLOCKS_END = '/Census_Block_Data.shp'

OUTFILE_CSV_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/'
OUTFILE_SHP_START = 'E:/Transit-Casa-Alex/MUNI Rail/Output/Buffers/'
OUTFILE_CSV_END = ['/Split Buffers/Split_Buffers_Tenth.csv', '/Split Buffers/Split_Buffers_Quarter.csv', '/Split Buffers/Split_Buffers_Third.csv']
OUTFILE_SHP_END = ['/Split Buffers/Split_Buffers_Tenth.shp', '/Split Buffers/Split_Buffers_Quarter.shp', '/Split Buffers/Split_Buffers_Third.shp']

YEARS = [2016]

def blocks_area(blocks):
    """
    function to calculate the area (in acres) of census blocks 
    
    blocks = shapefile with all of the census blocks 
    
    """

    blocks['AREA_x'] = blocks['ALAND10_x']*0.0000229568
    blocks['AREA_y'] = blocks['ALAND10_y']*0.000247105
    return blocks

    
def clean_area(blocks):

    """
    San Mateo and San Francisco have two different names for their area columns. This function sets the areas to one column name, ALAND00.
    
    blocks = census blocks dataframe with area columns 
    
   """

    if blocks['ALAND00'] == 0:
        blocks['ALAND00'] = blocks['ALAND']
    else:
        blocks['ALAND00'] = blocks['ALAND00']
    return blocks['ALAND00']    

        

def clean_area_column(row):
    """
    function to clean the area column. There are two data sets; one being the 2010 pop/housing and the other being the LEHD data. The pop/housing data has better coverage, but didnt have area pre-calculated. LEHD data does have area pre-calculated. LEHD block areas are used unless it is missing, where the user-calculated areas for pop/housing blocks are used.

    row = using the apply method with lambda allows python to iterate through the rows of a dataframe. This takes in one of the rows. 
    
    Example: df['new_column'] = df.apply(lambda row: function(row))
    """
    if np.isnan(row['AREA_y']):
        area = row['AREA_x']
    else:
        area = row['AREA_x']
    return area
        

def intersect(buffers,blocks):
    """
    function to intersect buffers with census blocks and calculate the portion of area that the original census block is within the buffer
    
    buffers = shapefile with all of the buffers
    blocks = shapefile with all of the census blocks
    
    """
    #loop through the buffers one stop at a time
    final_buffers = pd.DataFrame()
    count = 0
    
    #set the start time to check how long it takes to intersect one buffer
    start = datetime.datetime.now()
    
    for stop in buffers.STOP_ID.unique():
    #select out one of the buffers to intersect
        buffer = buffers[buffers['STOP_ID'] == stop]

    #select out the census blocks that intersect the buffer
        blocks_select = gp.sjoin(blocks,buffer,how = 'inner',op = 'intersects')
       

    #identity keeps only the left geodataframe and splits it based on the right geodataframe
        identity = gp.overlay(buffer,blocks_select,how = 'identity')
        identity.crs = {'init' :'epsg:4269'}
        
    #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        stateplane = identity.to_crs(epsg = '6420')
        
    #convert ft^2 to acres
        stateplane['SPLIT_AREA'] = stateplane.area*0.0000229568


        stateplane['SPLIT_RATIO'] = stateplane['SPLIT_AREA']/stateplane['AREA']
       
        data = stateplane[stateplane['STOP_ID'] == stop]
        
        final_buffers = final_buffers.append(data)
        count = count+1
        end = datetime.datetime.now()
        time = end - start

        print(str(count) + ' buffer(s) took ' + str((time.seconds/60)) + ' minutes')
    return final_buffers
    

if __name__ == "__main__":
    for y in YEARS:
        
        count = 0
        year = y
        buffers_paths = [BUFFERS_START[0] + str(year) + '/Tenth/Buffers_Tenth_GCS.shp', BUFFERS_START[1] + str(year) +'/Quarter/Buffers_Quarter_GCS.shp', 
                   BUFFERS_START[2] + str(year) + '/Third/Buffers_Third_GCS.shp',]
        blocks_path = BLOCKS_START + str(year) + BLOCKS_END
        
        for buffers_path in buffers_paths:
            print('Started New Buffer Titled: ' + buffers_path)


            buffers = gp.read_file(buffers_path)
            blocks = gp.read_file(blocks_path)
            buffers.crs = {'init':'epsg:4269'}
            blocks.crs = {'init':'epsg:4269'}

                
            # calculate the area of the cenusus blocks (in acres)
            blocks = blocks_area(blocks)
            blocks['AREA'] = blocks.apply(lambda row: clean_area_column(row),axis = 1)
           
            # function that intersects the census blocks with the buffers and calculates ratio of the split area over the original block area
            split_buffers = intersect(buffers,blocks)
            
           #write the intersected tenth-mile buffers to a csv and shapefile
            split_buffers.to_file(OUTFILE_SHP_START + str(year) + OUTFILE_SHP_END[count])
            split_buffers.to_csv(OUTFILE_CSV_START + str(year) + OUTFILE_CSV_END[count])
            
            count = count + 1

                
                
    print('ALL DONE TIME FOR SOME HALO!!!')

