import geopandas as gp
import pandas as pd
import datetime
import numpy as np

<<<<<<< HEAD
#set which buffer shapefiles that are going to be processed
BUFFERS = ['E:\Transit-Casa-Alex\Output\Buffers\Tenth/Buffers_Tenth_GCS.shp',
'E:\Transit-Casa-Alex\Output\Buffers\Quarter/Buffers_Quarter_GCS.shp',
'E:\Transit-Casa-Alex\Output\Buffers\Third/Buffers_Third_GCS.shp']

#change the paths to do a different set of census blocks or to save the output in a different directory
BLOCKS = 'E:/Transit-Casa-Alex/Output/Census Block Data/2009/Census_Block_Data.shp'
OUTFILE_CSV = ['Split_Buffers_Tenth.shp', 'Split_Buffers_Quarter.shp', 'Split_Buffers_Third.shp']
OUTFILE_SHP = ['Split_Buffers_Tenth.csv', 'Split_Buffers_Quarter.csv', 'Split_Buffers_Third.csv']

YEAR = 2010
=======

BUFFERS = ['E:\Transit-Casa-Share\Data/Buffers_Tenth_GCS.shp',
'E:\Transit-Casa-Share\Data/Buffers_Quarter_GCS.shp',
'E:\Transit-Casa-Share\Data/Buffers_Third_GCS.shp']

BLOCKS = 'E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Blocks/Combined_Counties.shp'
OUTFILE_CSV = 'Split_Buffers.shp'
OUTFILE_SHP = 'Split_Buffers.csv'

>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
def blocks_area(blocks, year):
    """
    function to calculate the area (in acres) of census blocks 
    
    blocks = shapefile with all of the census blocks 
    
    """
    
    
    if year == 2000:
            blocks['AREA'] = blocks['ALAND00']*0.000247105

    elif year == 2010:
<<<<<<< HEAD

        blocks['AREA_x'] = blocks['ALAND10_x']*0.0000229568
        blocks['AREA_y'] = blocks['ALAND10_y']*0.000247105
    return blocks
    
def clean_area_(blocks):
=======
        blocks['AREA'] = blocks['ALAND10']*0.000247105
    return blocks
    
def clean_area(blocks):
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
    """
    San Mateo and San Francisco have two different names for their area columns. This function sets the areas to one column name, ALAND00.
    
    blocks = census blocks dataframe with area columns 
    
   """
<<<<<<< HEAD
=======
   
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
    if blocks['ALAND00'] == 0:
        blocks['ALAND00'] = blocks['ALAND']
    else:
        blocks['ALAND00'] = blocks['ALAND00']
    return blocks['ALAND00']    
<<<<<<< HEAD
        

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
        
=======

>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
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
<<<<<<< HEAD

    #select out the census blocks that intersect the buffer
        blocks_select = gp.sjoin(blocks,buffer,how = 'inner',op = 'intersects')
       
        
    #identity keeps only the left geodataframe and splits it based on the right geodataframe
        identity = gp.overlay(buffer,blocks_select,how = 'identity')
        identity.crs = {'init' :'epsg:4269'}
        
    #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        stateplane = identity.to_crs(epsg = '6420')
        
    #convert ft^2 to acres
        stateplane['SPLIT_AREA'] = stateplane.area*0.0000229568
=======
        
    #select out the census blocks that intersect the buffer
        blocks_select = gp.sjoin(blocks,buffer,how = 'inner',op = 'intersects')
        
    #identity keeps only the left geodataframe and splits it based on the right geodataframe
        identity = gp.overlay(buffer,blocks_select,how = 'identity')
        identity.crs = {'init' :'epsg:4326'}
        
    #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        stateplane = identity.to_crs(epsg = '2227')
        
    #convert ft^2 to acres
        stateplane['SPLIT_AREA'] = stateplane.area*2.29568e-5
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
        stateplane['SPLIT_RATIO'] = stateplane['SPLIT_AREA']/stateplane['AREA']
       
        data = stateplane[stateplane['STOP_ID'] == stop]
        
        final_buffers = final_buffers.append(data)
        count = count+1
        end = datetime.datetime.now()
        time = end - start

        print(str(count) + ' buffer(s) took ' + str((time.seconds/60)) + ' minutes')
    return final_buffers
    

if __name__ == "__main__":
<<<<<<< HEAD
    count = 0

    for buffers in BUFFERS:
        print('Started New Buffer Titled: ' + buffers)


        buffers = gp.read_file(buffers)
        blocks = gp.read_file(BLOCKS)
      
        blocks.crs = {'init':'epsg:4269'}
        blocks = blocks.to_crs(buffers.crs)
        #print(blocks.crs)
        #print(buffers.crs)
        if YEAR == 2000:
            # this formats the area column of the two counties so that they are the same name
            blocks['ALAND00'] = blocks.apply(lambda row: clean_area00(row),axis = 1)
            
        elif YEAR == 2010:
            # calculate the area of the cenusus blocks (in acres)
            blocks = blocks_area(blocks,YEAR)
            blocks['AREA'] = blocks.apply(lambda row: clean_area_column(row),axis = 1)
            
            # function that intersects the census blocks with the buffers and calculates ratio of the split area over the original block area
            split_buffers = intersect(buffers,blocks)
            
           #write the intersected tenth-mile buffers to a csv and shapefile
            split_buffers.to_file(str(YEAR)+ '_' + OUTFILE_CSV[count])
            split_buffers.to_csv(str(YEAR) + '_' + OUTFILE_SHP[count])
            
            count = count + 1
        else:
            print('bad year')
    print('ALL DONE TIME FOR SOME HALO!!!')
=======

    for buffers in BUFFERS:
        print('Started New Buffer Titled: ' + buffers)
        buffers = gp.read_file(buffers)
        blocks = gp.read_file(BLOCKS)
        
        # this formats the area column of the two counties so that they are the same name
        blocks['ALAND00'] = blocks.apply(lambda row: clean_area(row),axis = 1)
        
        blocks = blocks_area(blocks,2000)
        split_buffers = intersect(buffers,blocks)
       
        split_buffers.to_file(OUTFILE_CSV)
        split_buffers.to_csv(OUTFILE_SHP)
        print('ALL DONE TIME FOR SOME HALO!!!')
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
