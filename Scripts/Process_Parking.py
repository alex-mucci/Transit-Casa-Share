import pandas as pd
import geopandas as gp
import numpy as np

keep = ['Shape_Area', 'geometry','cen_x', 'cen_y', 'MAZ', 'Average Hourly Price',
       'parking_rate', 'PRICE1HR', 'PRICE2HR', 'PRICE3HR', 'PRICE4HR',
       'PRICE12HR', 'PRICEDAY', 'PRICEDAYDISCOUNT']
       
keep2 = ['STOP_ID', 'geometry','Average Hourly Price', 'parking_rate',
       'PRICE1HR', 'PRICE2HR', 'PRICE3HR', 'PRICE4HR', 'PRICE12HR', 'PRICEDAY',
       'PRICEDAYDISCOUNT']

on_park = pd.read_csv('E:\Transit-Casa-Alex\Input\Parking\Demand/On Street Parking Demand.csv')
off_park = pd.read_csv('E:\Transit-Casa-Alex\Input\Parking\Demand/Off Street Parking Demand.csv')
off_res = pd.read_csv('E:\Transit-Casa-Alex\Input\Parking\Demand/Off Street Residential Parking Demand.csv')
maz = gp.read_file('E:/Transit-Casa-Alex/Input/Parking/TAZ39785.shp')
stops = gp.read_file('E:/Transit-Casa-Alex/Input/Bus_Stops/Bus_Stops_USft.shp')


def clean_row(row):
    if row == -99:
        row = np.nan
    else:
        row = row
    return row
    
    
    
    
on_park['Average Hourly Price'] = on_park['Average Hourly Price'].apply(lambda row: clean_row(row))
off_res = off_res.groupby(by = 'MAZ',as_index = False).mean()
on_park = on_park.groupby(by = 'MAZ',as_index = False).mean()
off_park = off_park.groupby(by = 'MAZ',as_index = False).mean()


demand = on_park.merge(off_res,how = 'outer',on = 'MAZ').merge(off_park,how = 'outer',on = 'MAZ')
final = maz.merge(demand,how = 'right',left_on='MAZ_ORIGIN',right_on = 'MAZ')

final2 = final[keep]
final2 = gp.GeoDataFrame(final2)


stops = stops.to_crs(maz.crs)
parking = gp.sjoin(stops,maz,how = 'left', op = 'intersects')
parking_demand = pd.merge(parking,demand, how = 'left',left_on = 'MAZ_ORIGIN',right_on = 'MAZ')
parking_demand = parking_demand[keep2]

parking_demand.to_csv('E:\Transit-Casa-Alex\Output\Parking Demand/Parking_Demand.csv')
parking_demand_geo = gp.GeoDataFrame(parking_demand)
parking_demand_geo.to_file('E:\Transit-Casa-Alex\Output\Parking Demand/Parking_Demand.shp')