import pandas as pd
import numpy as np
import geopandas as gp

<<<<<<< HEAD
YEAR = 2015

#Note that for different years the file paths must be changed

#Table file paths
S101 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/California/S0101/ACS_15_5YR_S0101_with_ann.csv'
DP04 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/California/DP04/ACS_15_5YR_DP04_with_ann.csv'
DP03 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/California/DP03/ACS_15_5YR_DP03_with_ann.csv'
B08119 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/California/B08119/ACS_15_5YR_B08119_with_ann.csv'

#Buffers path
STOPS_PATH = 'E:/Transit-Casa-Alex/Input/Bus_Stops/Bus_Stops.shp'

#Cenus tract Shapefile paths
SF = 'E:/Transit-Casa-Alex/Input/2010 Cenusus Shapefiles/Census Tracts/2015/San Francisco/SF_2015.shp'
SM = 'E:/Transit-Casa-Alex/Input/2010 Cenusus Shapefiles/Census Tracts/2015/San Mateo/SM_2015.shp'

#Data fields to keep in the end

keep09 = ['ALAND00', 'AWATER00', 'COUNTYFP00', 'CTIDFP00', 'NAME00', 'TRACTCE00', 'geometry', 'Id',
       'Id2', 'Geography','Total; Estimate; Total population', 'Number; Estimate; HOUSING OCCUPANCY - Total housing units', 'Number; Estimate; COMMUTING TO WORK - Workers 16 years and over - Mean travel time to work (minutes)', 
       'VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
rename09 = ['ALAND00', 'AWATER00', 'COUNTYFP00', 'CTIDFP00', 'NAME00', 'TRACTCE00', 'geometry', 'Id',
       'Id2', 'Geography', 'Total_Pop', 'Total_Housing_Units','Workers_16_And_Over_Mean_Travel_Time_To_Work_(Minutes)','VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
       
keep15 = ['ALAND', 'AWATER', 'COUNTYFP', 'NAME', 'TRACTCE', 'geometry', 'Id',
       'Id2', 'Geography','Total; Estimate; Total population', 'Estimate; HOUSING OCCUPANCY - Total housing units', 
       'VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
       
rename15 = ['ALAND', 'AWATER', 'COUNTYFP', 'NAME', 'TRACTCE', 'geometry', 'Id',
       'Id2', 'Geography', 'POP_ACS', 'HU_ACS','VAC_RATE', 'OCC_RATE', 'INC_0_15','INC_15_50', 'INC_50_100', 'INC_100P', 'HH_SIZE', 'HH_0VEH','POPDEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
=======
#Table file paths
S101 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/2009/S0101/ACS_09_5YR_S0101_with_ann.csv'
DP04 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/2009/DP04/ACS_09_5YR_DP5YR4_with_ann.csv'
DP03 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/2009/DP03/ACS_09_5YR_DP5YR3_with_ann.csv'
B08119 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/2009/B08119/ACS_09_5YR_B08119_with_ann.csv'

#Buffers path
BUFFERS_PATH = 'E:/Transit-Casa-Alex/Output/Buffers/Tenth/Buffers/Buffers_Tenth_GCS.shp'

#Cenus tract Shapefile paths
SF = 'E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Tracts/06_CALIFORNIA/06075_San_Francisco_County/tl_2009_06075_tract00.shp'
SM = 'E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Tracts/06_CALIFORNIA/06081_San_Mateo_County/tl_2009_06081_tract00.shp'

#Data fields to keep in the end

keep = ['ALAND00', 'AWATER00', 'COUNTYFP00', 'CTIDFP00', 'NAME00', 'TRACTCE00', 'geometry', 'Id',
       'Id2', 'Geography','Total; Estimate; Total population', 'Number; Estimate; HOUSING OCCUPANCY - Total housing units', 'Number; Estimate; COMMUTING TO WORK - Workers 16 years and over - Mean travel time to work (minutes)', 
       'VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
rename = ['ALAND00', 'AWATER00', 'COUNTYFP00', 'CTIDFP00', 'NAME00', 'TRACTCE00', 'geometry', 'Id',
       'Id2', 'Geography', 'Total_Pop', 'Total_Housing_Units','Workers_16_And_Over_Mean_Travel_Time_To_Work_(Minutes)','VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
   

def drop_margins(start_column,df):
    """
    function to drop out the margin of errors from the acs dataset 
    
    start_column = the column number with the first margin of errors
    df = the acs dataframe
    
    """
    
    i = start_column
    columns = df.columns
    while i< len(columns):
        df = df.drop(columns[i],axis = 1)
        i = i + 2
    return df
        
def acs_income_calc(df):
    """
    funtion that categorizes the acs income data into ranges that match previous research. (0-15k, 15-50k,50-100k, and 100+)
    
    df = acs dataframe
    """
    
<<<<<<< HEAD
    # eventually need to change the percents (PER) to shares (SHR) because they are decimals not percents. 
    if year == 2009:
        
        df['PER_INCOME_0-15'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - Less than $10,000'] +
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $10,000 to $14,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_15-50'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $15,000 to $24,999'] +
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $25,000 to $34,999']+
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $35,000 to $49,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_50-100'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $50,000 to $74,999'] + 
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $75,000 to $99,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        
    elif year == 2015:
        df['PER_INCOME_0-15'] = (df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - Less than $10,000'] +
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $10,000 to $14,999'])/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_15-50'] = (df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $15,000 to $24,999'] +
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $25,000 to $34,999']+
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $35,000 to $49,999'])/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_50-100'] = (df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $50,000 to $74,999'] + 
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $75,000 to $99,999'])/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']
    
    else:
        print('This year has not been formatted yet')
    
    df['PER_INCOME_100+']= 1-df['PER_INCOME_50-100'] - df['PER_INCOME_15-50'] - df['PER_INCOME_0-15']



=======
    df['PER_INCOME_0-15'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - Less than $10,000'] +
    df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $10,000 to $14,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
    
    df['PER_INCOME_15-50'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $15,000 to $24,999'] +
    df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $25,000 to $34,999']+
    df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $35,000 to $49,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
    
    df['PER_INCOME_50-100'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $50,000 to $74,999'] + 
    df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $75,000 to $99,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
    
    df['PER_INCOME_100+']= 1-df['PER_INCOME_50-100'] - df['PER_INCOME_15-50'] - df['PER_INCOME_0-15']

>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
def acs_household_calc(df):
    """
    function that calculates the household data fields 
    
    df = acs dataframe
    """
<<<<<<< HEAD
    if year == 2009:
    
        df['VAC_RATE'] = df['Number; Estimate; HOUSING OCCUPANCY - Total housing units - Vacant housing units']/df['Number; Estimate; HOUSING OCCUPANCY - Total housing units']
        
        df['OCC_RATE'] = 1-df['VAC_RATE']
        
        df['AVG_HH_SIZE'] = df['Total; Estimate; Total population']/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']  
        
        df['PER_HH_0VEH'] = df['Number; Estimate; VEHICLES AVAILABLE - Occupied housing units - No vehicles available']/df['Number; Estimate; HOUSING OCCUPANCY - Total housing units - Occupied housing units']
    
    elif year == 2015:
        df['VAC_RATE'] = df['Estimate; HOUSING OCCUPANCY - Total housing units - Vacant housing units']/df['Estimate; HOUSING OCCUPANCY - Total housing units']
        
        df['OCC_RATE'] = 1-df['VAC_RATE']
        
        df['AVG_HH_SIZE'] = df['Total; Estimate; Total population']/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']  
        
        df['PER_HH_0VEH'] = df['Estimate; VEHICLES AVAILABLE - Occupied housing units - No vehicles available']/df['Estimate; HOUSING OCCUPANCY - Total housing units - Occupied housing units']
    
    else:
        print('This year has not been formatted yet')

=======
    df['VAC_RATE'] = df['Number; Estimate; HOUSING OCCUPANCY - Total housing units - Vacant housing units']/df['Number; Estimate; HOUSING OCCUPANCY - Total housing units']
    
    df['OCC_RATE'] = 1-df['VAC_RATE']
    
    df['AVG_HH_SIZE'] = df['Total; Estimate; Total population']/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']  
    
    df['PER_HH_0VEH'] = df['Number; Estimate; VEHICLES AVAILABLE - Occupied housing units - No vehicles available']/df['Number; Estimate; HOUSING OCCUPANCY - Total housing units - Occupied housing units']
    
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
def acs_density_calc(df):
    """
    function that calculates population, household, and housing unit densities
    
    df = acs dataframe
    """
<<<<<<< HEAD
    
    if year == 2009:
        df['POP_DEN_ACS'] = df['Total; Estimate; Total population']/df['ALAND00']/0.000247105
        df['HH_DEN_ACS'] = df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']/df['ALAND00']/0.000247105   
        df['HU_DEN_ACS'] = df['Number; Estimate; HOUSING OCCUPANCY - Total housing units']/df['ALAND00']/0.000247105   
    
    elif year == 2015:
        df['POP_DEN_ACS'] = df['Total; Estimate; Total population']/df['ALAND']/0.000247105
        df['HH_DEN_ACS'] = df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']/df['ALAND']/0.000247105   
        df['HU_DEN_ACS'] = df['Estimate; HOUSING OCCUPANCY - Total housing units']/df['ALAND']/0.000247105   
    
    else:
        print('This year has not been formatted yet')

def intersect_acs_buffers(acs_df,stops_path):
    """
    function to intersect acs tract data with the bus stop point features. 
    
    acs_df = dataframe containing the acs data (by census tract)
    buffers_path = file path to the bus stop point feature shapefile
    """
    
    acs = acs_df
    bus_stops = gp.read_file(stops_path, crs = 'crs')
    acs.crs = bus_stops.crs
    data = gp.sjoin(bus_stops,acs,how = 'left',op = 'intersects')

    return data

    
if __name__ == "__main__":
    
    year = YEAR
=======
    df['POP_DEN_ACS'] = df['Total; Estimate; Total population']/df['ALAND00']/0.000247105
    df['HH_DEN_ACS'] = df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']/df['ALAND00']/0.000247105   
    df['HU_DEN_ACS'] = df['Number; Estimate; HOUSING OCCUPANCY - Total housing units']/df['ALAND00']/0.000247105   

def intersect_acs_buffers(acs_df,buffers_path):
    """
    function to intersect acs tract data with the bus stop buffers. Note: When multiple census tracts intersect with a buffer the average of the data field is taken. 
    
    acs_df = dataframe containing the acs data (by census tract)
    buffers_path = file path to the buffers shapefile
    """
    
    acs = acs_df
    buffers = gp.read_file(buffers_path, crs = 'crs')
    acs.crs = buffers.crs

    data = gp.sjoin(buffers,acs,how = 'left',op = 'intersects')
    
    acs = data[['POP_ACS', 'HU_ACS',
       'TT_To_Work', 'VAC_RATE', 'OCC_RATE',
       'INC_0_15', 'INC_15_50', 'INC_50_100', 'INC_100P',
       'HH_SIZE', 'HH_0VEH', 'POPDEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS','STOP_ID']].groupby(by = 'STOP_ID',as_index = False).mean()

    buffers_acs = pd.merge(buffers,acs,on= 'STOP_ID',how = 'left')
    return buffers_acs

    
if __name__ == "__main__":
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
    #read in all of the tables
    s1 = pd.read_csv(S101,skiprows = 1)
    d4 = pd.read_csv(DP04,skiprows = 1)
    d3 = pd.read_csv(DP03,skiprows =1)
    b8 = pd.read_csv(B08119,skiprows = 1)
    
    
    #merge all of the tables (use outer in case there is missing tracts in a table)
    df = pd.merge(s1,d4,how = 'outer', on = ['Id','Id2','Geography'],suffixes = ('_S0101','_DP04'))
    df = pd.merge(df,d3,how = 'outer', on = ['Id','Id2','Geography'],suffixes = ('','_DP03'))
    df = pd.merge(df,b8,how = 'outer', on = ['Id','Id2','Geography'],suffixes = ('','_B08119'))

    
    #read each counties census tract shapefile
    sf = gp.read_file(SF,crs = 'crs')
    sm = gp.read_file(SM,crs = 'crs')
    
    
    #combine the shapefiles to attach the acs data 
    tracts = sf.append(sm)
    
    
    #change the unique identifier to an int so that the acs data can be merged in
<<<<<<< HEAD
    if year < 2010:
        tracts['CTIDFP00'] = tracts.CTIDFP10.apply(lambda row: int(row))
        tracts_data = pd.merge(tracts,df,how = 'left',left_on = 'CTIDFP00',right_on = 'Id2')
    else:
        tracts['GEOID'] = tracts.GEOID.apply(lambda row: int(row))
        tracts_data = pd.merge(tracts,df,how = 'left',left_on = 'GEOID',right_on = 'Id2')
  
    
    #drop the margin of errors
    tracts_data = drop_margins(17,tracts_data)

=======
    tracts['CTIDFP00'] = tracts.CTIDFP00.apply(lambda row: int(row))
    tracts_data = pd.merge(tracts,df,how = 'left',left_on = 'CTIDFP00',right_on = 'Id2')
    
    
    #drop the margin of errors
    tracts_data = drop_margins(17,tracts_data)
    
    
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
    #perform the data calculations
    acs_income_calc(tracts_data)
    acs_household_calc(tracts_data)
    acs_density_calc(tracts_data)
    
<<<<<<< HEAD
    if year == 2009:
        # pull out the columns that are of interest
        tracts_keep = pd.DataFrame()
        for column in keep09:
            tracts_keep[column] = tracts_data[column]
        tracts_keep.columns = rename09
        
    elif year == 2015:
        # pull out the columns that are of interest
        tracts_keep = pd.DataFrame()
        for column in keep15:
            tracts_keep[column] = tracts_data[column]
        tracts_keep.columns = rename15
        
    else:   
        print('This year has not been formatted yet')
        
    
    
        
    #intersect the buffers with the census tracts and average if multiple tracts intersect, then link the data back to the buffers 
    acs = intersect_acs_buffers(tracts_keep,STOPS_PATH)
    
    
    #write to a csv file 
    acs.to_csv('E:/Transit-Casa-Alex/Output/Demographic (ACS)/2015/ACS_DATA.csv')
    
    #write to a shapefile 
    acs.to_file('E:/Transit-Casa-Alex/Output\Demographic (ACS)/2015/Bus_Stops_ACS.shp',driver = 'ESRI Shapefile')
=======
    
    # pull out the columns that are of interest
    tracts_keep = pd.DataFrame()
    for column in keep:
        tracts_keep[column] = tracts_data[column]
    tracts_keep.columns = rename
    
    #intersect the buffers with the census tracts and average if multiple tracts intersect, then link the data back to the buffers 
    buffers_acs = intersect_acs_buffers(tracts_keep,BUFFERS_PATH)
    
    
    #write to a csv file 
    buffers_acs.to_csv('E:\Transit-Casa-Alex\Output\Buffers\Tenth\Buffers_ACS/Buffers_ACS.csv')
    
    #write to a shapefile 
    buffers_acs.to_file('E:\Transit-Casa-Alex\Output\Buffers\Tenth\Buffers_ACS/Buffers_ACS.shp',driver = 'ESRI Shapefile')
>>>>>>> 6e43ba4dca69e340b79d1a3d9b929f6bae11c8f8
    
    print('ALL DONE TIME FOR A BEER!')
    