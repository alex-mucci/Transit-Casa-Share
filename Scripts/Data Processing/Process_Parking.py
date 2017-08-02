import pandas as pd
import geopandas as gp
import numpy as np

KEEP = ['Shape_Area', 'geometry','cen_x', 'cen_y', 'MAZ', 'Average Hourly Price',
       'parking_rate', 'PRICE1HR', 'PRICE2HR', 'PRICE3HR', 'PRICE4HR',
       'PRICE12HR', 'PRICEDAY', 'PRICEDAYDISCOUNT']
       
KEEP2 = ['STOP_ID', 'geometry','Average Hourly Price', 'parking_rate',
       'PRICE1HR', 'PRICE2HR', 'PRICE3HR', 'PRICE4HR', 'PRICE12HR', 'PRICEDAY',
       'PRICEDAYDISCOUNT']
       
YEARS = [2009,2016]

ON_PARK_PATH = 'E:\Transit-Casa-Alex\Input\Parking\Demand/On Street Parking Demand.csv'
OFF_PARK_PATH = 'E:\Transit-Casa-Alex\Input\Parking\Demand/Off Street Parking Demand.csv'
OFF_RES_PATH = 'E:\Transit-Casa-Alex\Input\Parking\Demand/Off Street Residential Parking Demand.csv'
MAZ_PATH = 'E:/Transit-Casa-Alex/Input/Parking/TAZ39785.shp'

STOPS_START = 'E:/Transit-Casa-Alex/MUNI Rail/Input/Rail Stops/MUNI_Rail_Stops_'
STOPS_END = '.shp'

MODE = 'MUNI Rail'



def clean_row(row):
    if row == -99:
        row = np.nan
    else:
        row = row
    return row

    
    

if __name__ == "__main__":
    for year in YEARS:
        print('Processing year ' + str(year))
        
        on_park = pd.read_csv(ON_PARK_PATH)
        off_park = pd.read_csv(OFF_PARK_PATH)
        off_res = pd.read_csv(OFF_RES_PATH)
        maz = gp.read_file(MAZ_PATH)

        stops_path = STOPS_START + str(year) + STOPS_END
        stops = gp.read_file(stops_path)
        stops.crs = {'init':'epsg:4326'}
        
            
        on_park['Average Hourly Price'] = on_park['Average Hourly Price'].apply(lambda row: clean_row(row))
        off_res = off_res.groupby(by = 'MAZ',as_index = False).mean()
        on_park = on_park.groupby(by = 'MAZ',as_index = False).mean()
        off_park = off_park.groupby(by = 'MAZ',as_index = False).mean()


        demand = on_park.merge(off_res,how = 'outer',on = 'MAZ').merge(off_park,how = 'outer',on = 'MAZ')
        final = maz.merge(demand,how = 'right',left_on='MAZ_ORIGIN',right_on = 'MAZ')

        final2 = final[KEEP]
        final2 = gp.GeoDataFrame(final2)

        maz = maz.to_crs(stops.crs)
        parking = gp.sjoin(stops,maz,how = 'left', op = 'intersects')
        parking_demand = pd.merge(parking,demand, how = 'left',left_on = 'MAZ_ORIGIN',right_on = 'MAZ')
        parking_demand = parking_demand[KEEP2]

        parking_demand.to_csv('E:/Transit-Casa-Alex/' + MODE + '/Output/Parking Demand/' + str(year) + '_Parking_Demand.csv')
        parking_demand_geo = gp.GeoDataFrame(parking_demand)
        parking_demand_geo.to_file('E:/Transit-Casa-Alex/' + MODE + '/Output/Parking Demand/' + str(year) + '_Parking_Demand.shp')
        
    print('TOO EASY!')