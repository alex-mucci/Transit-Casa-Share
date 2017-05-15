import geopandas as gp
import pandas as pd
import datetime
import numpy as np


BUFFERS = gp.read_file('E:/Transit-Casa-Alex/Output/Buffers/Tenth/Buffers/Buffers_Tenth_GCS.shp')
BLOCKS = gp.read_file('E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Blocks/Combined_Counties.shp')
OUTFILE_CSV = 'Split_Buffers.shp'
OUTFILE_SHP = 'Split_Buffers.csv'

def blocks_area(blocks, year):
    """
    function to calculate the area (in acres) of census blocks 
    
    blocks = shapefile with all of the census blocks 
    
    """
    if year == 2000:
        blocks['AREA'] = blocks['ALAND']*0.000247105
    elif year == 2010:
        blocks['AREA'] = blocks['ALAND10']*0.000247105
    return blocks
    
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
    
    for stop in stops.STOP_ID.unique():
    #select out one of the buffers to intersect
        buffer = buffers[buffers['STOP_ID'] == stop]
        
    #identity keeps only the left geodataframe and splits it based on the right geodataframe
        identity = gp.overlay(buffer,blocks,how = 'identity')
        identity.crs = {'init' :'epsg:4326'}
        
    #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        stateplane = identity.to_crs(epsg = '2227')
        
    #convert ft^2 to acres
        stateplane['SPLIT_AREA'] = stateplane.area*2.29568e-5
        stateplane['SPLIT_RATIO'] = stateplane['SPLIT_AREA']/stateplane['AREA']
       
        data = stateplane[stateplane['stop'] == stop]
        
        final_buffers = final_buffers.append(data)
        count = count+1
        end = datetime.datetime.now()
        time = start - end
        
        print(str(count) + ' buffer(s) took' + str(time) + ' minutes')
    return final_buffers
    

if __name__ == "__main__":

    blocks = blocks_area(BLOCKS)
    split_buffers = intersect(BUFFERS,blocks)
   
    split_buffers.to_file(OUTFILE_CSV)
    split_buffers.to_csv(OUTFILE_SHP)