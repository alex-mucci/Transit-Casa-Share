import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gp
import sys


H5_INFILE = "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"
BASE_START_DATE = '2009-01-01'
BASE_END_DATE = '2009-12-01'
FUTURE_START_DATE = '2013-01-01'
FUTURE_END_DATE = '2013-12-01'
DIRECTIONS = [1,0]


def create_heatmap(df,direction):
    """
    function to create a heatmap of a route given a pivot table with time (TOD) as the columns and 
    stopnames as the row index
    
    df = dataframe of route 
    direction = direction of the route (1 or 0 for inbound and outbound)
    """
    
    plt.figure(figsize =(10, 10))
    if direction == 1:
        plt.title('INBOUND')
        plt.tight_layout()
        Heatmap = sns.heatmap(df, robust = True, cmap = 'RdYlGn',fmt = '.1f',annot = False,
                              linecolor = 'black',linewidth = 0.1,cbar = True,square = False, 
                              xticklabels = True, yticklabels = True)
    elif direction == 0:
        plt.title('OUTBOUND')
        plt.tight_layout()
        Heatmap = sns.heatmap(df, robust = True, cmap = 'RdYlGn',fmt = '.1f',annot = False,
                              linecolor = 'black',linewidth = 0.1,cbar = True,square = False, 
                              xticklabels = True, yticklabels = True)

    else:
        print('Bad Direction!')

    return Heatmap
 

if __name__ == "__main__":
    # read in the monthly route stops table
    store = pd.HDFStore(H5_INFILE)
    bus = store.get('rs_tod')
    
    #select out the months that are of interest
    bus09 = bus[bus["MONTH"].isin(pd.date_range(BASE_START_DATE,BASE_END_DATE))]
    bus13 = bus[bus['MONTH'].isin(pd.date_range(FUTURE_START_DATE,FUTURE_END_DATE))]
    
    #merge the two dataframes to calculate a difference between the two date ranges (years)
    bus_diff = pd.merge(bus09,bus13,how = 'inner',on =['DOW','TOD','AGENCY_ID','ROUTE_SHORT_NAME','DIR','SEQ'],suffixes = ('_09','_13'))
    bus_diff['LOAD_DIFF'] = bus_diff['LOAD_DEP_13'] - bus_diff['LOAD_DEP_09']
    bus_diff['LOAD_PDIFF'] = (bus_diff['LOAD_DEP_13'] - bus_diff['LOAD_DEP_09'])/bus_diff['LOAD_DEP_09']
    
    bus_dfs = [bus09,bus13,bus_diff]
    count = 0 
    
    for bus_df in bus_dfs:
        print('Started new heatmaps dataframe')
        #run through all of the directions (inbound and outbound)
        for direction in DIRECTIONS:
            dir_df = bus_df[bus_df['DIR'] == direction]
            if count != 2:
                pivot = dir_df.pivot_table(values = 'LOAD_DEP',index = 'ROUTE_SHORT_NAME',
                                      columns = 'TOD',aggfunc = 'sum',margins = False, fill_value = 0)
        #create the heatmap  
                heatmap = create_heatmap(pivot,direction)
                figure = heatmap.get_figure()
                
         #save the heatmap 
                if count == 0:
                    figure.savefig('E:/Transit-Casa-Alex/Output/HeatMaps/'  + '2009 ' +  '_Direction_' +
                    str(direction) + '.jpg',bbox_inches='tight')
                elif count == 1:
                    figure.savefig('E:/Transit-Casa-Alex/Output/HeatMaps/'  + ' 2013 ' + '_Direction_' +
                    str(direction) + '.jpg',bbox_inches='tight')
                else:
                    print('Something is wrong')
            else:
                        
                #create a similar pivot table as before, but instead use sequence becasue stop names may 
                #change between years
                pivot = dir_df.pivot_table(values = 'LOAD_DIFF',index = 'ROUTE_SHORT_NAME',
                                      columns = 'TOD',aggfunc = 'sum',margins = False, fill_value = 0)
                pivot2 = dir_df.pivot_table(values = 'LOAD_PDIFF',index = 'ROUTE_SHORT_NAME',
                                      columns = 'TOD',aggfunc = 'sum',margins = False, fill_value = 0)                      
                heatmap = create_heatmap(pivot,direction)
                heatmap2 = create_heatmap(pivot2,direction)
                
        #save the heatmap 
                figure = heatmap.get_figure()
                figure2 = heatmap2.get_figure()
                figure.savefig('E:/Transit-Casa-Alex/Output/HeatMaps/'  + 'Diff ' + '_Direction_' +
                str(direction) + '.jpg',bbox_inches='tight')
                figure2.savefig('E:/Transit-Casa-Alex/Output/HeatMaps/'  + 'PDiff ' + '_Direction_' +
                str(direction) + '.jpg',bbox_inches='tight')
           
          
            
        plt.close('all')
        count = count + 1        
            
                
    print('ALL DONE TIME FOR HALO!')
        