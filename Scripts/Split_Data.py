import geopandas as gp
import pandas as pd
import datetime
import numpy as np


BUFFERS = ['E:\Transit-Casa-Share\Data/Buffers_Tenth_GCS.shp',
'E:\Transit-Casa-Share\Data/Buffers_Quarter_GCS.shp',
'E:\Transit-Casa-Share\Data/Buffers_Third_GCS.shp']

BLOCKS = 'E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Blocks/Combined_Counties.shp'
OUTFILE_CSV = 'Split_Buffers.shp'
OUTFILE_SHP = 'Split_Buffers.csv'

def blocks_area(blocks, year):
    """
    function to calculate the area (in acres) of census blocks 
    
    blocks = shapefile with all of the census blocks 
    
    """
    
    
    if year == 2000:
            blocks['AREA'] = blocks['ALAND00']*0.000247105

    elif year == 2010:
        blocks['AREA'] = blocks['ALAND10']*0.000247105
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
        identity.crs = {'init' :'epsg:4326'}
        
    #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        stateplane = identity.to_crs(epsg = '2227')
        
    #convert ft^2 to acres
        stateplane['SPLIT_AREA'] = stateplane.area*2.29568e-5
        stateplane['SPLIT_RATIO'] = stateplane['SPLIT_AREA']/stateplane['AREA']
       
        data = stateplane[stateplane['STOP_ID'] == stop]
        
        final_buffers = final_buffers.append(data)
        count = count+1
        end = datetime.datetime.now()
        time = end - start

        print(str(count) + ' buffer(s) took ' + str((time.seconds/60)) + ' minutes')
    return final_buffers
    

if __name__ == "__main__":

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