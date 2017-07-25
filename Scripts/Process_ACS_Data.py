import pandas as pd
import numpy as np
import geopandas as gp

YEAR = 2015
MODE = 'MUNI Rail'
#Note that for different years the file paths must be changed

#Table file paths for the 2009 data 
S101_09 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2009/S0101/ACS_09_5YR_S0101_with_ann.csv'
DP04_09 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2009/DP04/ACS_09_5YR_DP5YR4_with_ann.csv'
DP03_09 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2009/DP03/ACS_09_5YR_DP5YR3_with_ann.csv'
B08119_09 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2009/B08119/ACS_09_5YR_B08119_with_ann.csv'
STOPS_09 = 'E:/Transit-Casa-Alex/Input/Bus_Stops/2009/Bus_Stops_2009.shp'

# Table paths for the 2015 data
S101_15 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/San Francisco/S0101/ACS_15_5YR_S0101_with_ann.csv'
DP04_15 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/San Francisco/DP04/ACS_15_5YR_DP04_with_ann.csv'
DP03_15 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/San Francisco/DP03/ACS_15_5YR_DP03_with_ann.csv'
B08119_15 = 'E:/Transit-Casa-Alex/Input/ACS 5 Year Estimates/Census Tracts/2015/San Francisco/B08119/ACS_15_5YR_B08119_with_ann.csv'


STOPS_09 = 'E:/Transit-Casa-Alex/MUNI Rail/Input/Rail Stops/MUNI_Rail_Stops_2009.shp'
#used the 2016 bus stops because that is the year we are interested in. The acs data was only available for 2015.
STOPS_15 = 'E:/Transit-Casa-Alex/MUNI Rail/Input/Rail Stops/MUNI_Rail_Stops_2016.shp'

#Cenus tract Shapefile paths
SF15 = 'E:/Transit-Casa-Alex/Input/2010 Cenusus Shapefiles/Census Tracts/2015/San Francisco/SF_2015.shp'
SM15 = 'E:/Transit-Casa-Alex/Input/2010 Cenusus Shapefiles/Census Tracts/2015/San Mateo/SM_2015.shp'

SF09 = 'E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Tracts/06_CALIFORNIA/06075_San_Francisco_County/tl_2009_06075_tract00.shp'
SM09 = 'E:/Transit-Casa-Alex/Input/2000 Census Shapefiles/2000 Census Tracts/06_CALIFORNIA/06081_San_Mateo_County/tl_2009_06081_tract00.shp'

#Columns to keep in the end. Needed to tidy up the data fields. These are for 2009.

KEEP09 = ['ALAND00', 'AWATER00', 'COUNTYFP00', 'CTIDFP00', 'NAME00', 'TRACTCE00', 'geometry', 'Id',
       'Id2', 'Geography','Total; Estimate; Total population', 'Number; Estimate; HOUSING OCCUPANCY - Total housing units', 'Number; Estimate; COMMUTING TO WORK - Workers 16 years and over - Mean travel time to work (minutes)', 
       'VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
RENAME09 = ['ALAND00', 'AWATER00', 'COUNTYFP00', 'CTIDFP00', 'NAME00', 'TRACTCE00', 'geometry', 'Id',
       'Id2', 'Geography', 'Total_Pop', 'Total_Housing_Units','Workers_16_And_Over_Mean_Travel_Time_To_Work_(Minutes)','VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
          
          
# same as before but for 2015
KEEP15 = ['ALAND', 'AWATER', 'COUNTYFP', 'NAME', 'TRACTCE', 'geometry', 'Id',
       'Id2', 'Geography','Total; Estimate; Total population', 'Estimate; HOUSING OCCUPANCY - Total housing units', 
       'VAC_RATE', 'OCC_RATE', 'PER_INCOME_0-15','PER_INCOME_15-50', 'PER_INCOME_50-100', 'PER_INCOME_100+', 'AVG_HH_SIZE', 'PER_HH_0VEH','POP_DEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']
       
RENAME15 = ['ALAND', 'AWATER', 'COUNTYFP', 'NAME', 'TRACTCE', 'geometry', 'Id',
       'Id2', 'Geography', 'POP_ACS', 'HU_ACS','VAC_RATE', 'OCC_RATE', 'INC_0_15','INC_15_50', 'INC_50_100', 'INC_100P', 'HH_SIZE', 'HH_0VEH','POPDEN_ACS', 'HH_DEN_ACS', 'HU_DEN_ACS']




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

    # eventually need to change the percents (PER) to shares (SHR) because they are decimals not percents. 
    if year == 2009:
        
        df['PER_INCOME_0-15'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - Less than $10,000'] +
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $10,000 to $14,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_15-50'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $15,000 to $24,999'] +
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $25,000 to $34,999']+
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $35,000 to $49,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_50-100'] = (df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $50,000 to $74,999'] + 
        df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households - $75,000 to $99,999'])/df['Number; Estimate; INCOME AND BENEFITS (IN 2009 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_100+']= 1-df['PER_INCOME_50-100'] - df['PER_INCOME_15-50'] - df['PER_INCOME_0-15']
        
        
    elif year == 2015:
        df['PER_INCOME_0-15'] = (df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - Less than $10,000'] +
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $10,000 to $14,999'])/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_15-50'] = (df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $15,000 to $24,999'] +
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $25,000 to $34,999']+
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $35,000 to $49,999'])/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_50-100'] = (df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $50,000 to $74,999'] + 
        df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households - $75,000 to $99,999'])/df['Estimate; INCOME AND BENEFITS (IN 2015 INFLATION-ADJUSTED DOLLARS) - Total households']
        
        df['PER_INCOME_100+']= 1-df['PER_INCOME_50-100'] - df['PER_INCOME_15-50'] - df['PER_INCOME_0-15']
    
    else:
        print('This year has not been formatted yet')
  

    
def acs_household_calc(df):
    """
    function that calculates the household data fields 
    
    df = acs dataframe
    """

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

    

def acs_density_calc(df):
    """
    function that calculates population, household, and housing unit densities
    
    df = acs dataframe
    """

    
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
    stops_path = file path to the bus stop point feature shapefile
    """
    
    acs = acs_df
    bus_stops = gp.read_file(stops_path, crs = 'crs')
    acs.crs = bus_stops.crs
    data = gp.sjoin(bus_stops,acs,how = 'left',op = 'intersects')

    return data

    

    
if __name__ == "__main__":
    
    year = YEAR
    
    print('Reading in the Files!')
    
    if year == 2009:
        S101 = S101_09
        DP04 = DP04_09
        DP03 = DP03_09
        B08119 = B08119_09
        
        stops = STOPS_09
    
    elif year == 2015:
        S101 = S101_15
        DP04 = DP04_15
        DP03 = DP03_15
        B08119 = B08119_15
        
        stops = STOPS_15
    
    else:
        print('This year has not been formatted yet')
    
    #read in all of the tables
    s1 = pd.read_csv(S101,skiprows = 1)
    d4 = pd.read_csv(DP04,skiprows = 1)
    d3 = pd.read_csv(DP03,skiprows =1)
    b8 = pd.read_csv(B08119,skiprows = 1)
    
    print('Mashing the ACS tables together!')
    #merge all of the tables (use outer in case there is missing tracts in a table)
    df = pd.merge(s1,d4,how = 'outer', on = ['Id','Id2','Geography'],suffixes = ('_S0101','_DP04'))
    df = pd.merge(df,d3,how = 'outer', on = ['Id','Id2','Geography'],suffixes = ('','_DP03'))
    df = pd.merge(df,b8,how = 'outer', on = ['Id','Id2','Geography'],suffixes = ('','_B08119'))

    
    #read each counties census tract shapefile
    if year == 2009:
        sf = gp.read_file(SF09,crs = 'crs')
        sm = gp.read_file(SM09,crs = 'crs')
        
    elif year == 2015:
        sf = gp.read_file(SF15,crs = 'crs')
        sm = gp.read_file(SM15,crs = 'crs')
        
    else:
        print('This year has not been formatted yet')

    
    #combine the shapefiles to attach the acs data 
    tracts = sf.append(sm)
    
    
    #change the unique identifier to an int so that the acs data can be merged in
    print('Giving the Data Geometry! :)')
    
    if year < 2010:
        tracts['CTIDFP00'] = tracts.CTIDFP00.apply(lambda row: int(row))
        tracts_data = pd.merge(tracts,df,how = 'left',left_on = 'CTIDFP00',right_on = 'Id2')
    else:
        tracts['GEOID'] = tracts.GEOID.apply(lambda row: int(row))
        tracts_data = pd.merge(tracts,df,how = 'left',left_on = 'GEOID',right_on = 'Id2')
  
    
    #drop the margin of errors
    tracts_data = drop_margins(17,tracts_data)
    
    print('Calculating Awesome Variables!!')
    #perform the data calculations
    acs_income_calc(tracts_data)
    acs_household_calc(tracts_data)
    acs_density_calc(tracts_data)
    

    if year == 2009:
        # pull out the columns that are of interest
        tracts_keep = pd.DataFrame()
        for column in KEEP09:
            tracts_keep[column] = tracts_data[column]
        tracts_keep.columns = RENAME09
        
    elif year == 2015:
        # pull out the columns that are of interest
        tracts_keep = pd.DataFrame()
        for column in KEEP15:
            tracts_keep[column] = tracts_data[column]
        tracts_keep.columns = RENAME15
        
    else:   
        print('This year has not been formatted yet')
        
    print('Writting the files.....Almost Done!')
    
        
    #intersect the buffers with the census tracts and average if multiple tracts intersect, then link the data back to the buffers 
    acs = intersect_acs_buffers(tracts_keep,stops)
    
    
    #write to a csv file 
    acs.to_csv('E:/Transit-Casa-Alex/' + MODE + '/Output/Demographic (ACS)/' + str(year) + '/ACS_DATA.csv')
    
    #write to a shapefile 
    acs.to_file('E:/Transit-Casa-Alex/' + MODE + '/Output\Demographic (ACS)/' + str(year) + '/Bus_Stops_ACS.shp',driver = 'ESRI Shapefile')

    print('ALL DONE TIME FOR A BEER!')
    