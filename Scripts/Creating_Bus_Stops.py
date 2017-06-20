import pandas as pd
import geopandas
import numpy as np
from shapely.geometry import Point




HDF_INFILE = "E:/Transit_Casa/Output/sfmuni_monthly_ts.h5"
MONTH1 = '2016-09-01'
MONTH2 = '2016-12-31'

CSV_OUTFILE = 'E:/Transit-Casa-Alex/Input/Bus_Stops/bus stops_2016.csv'
SHP_OUTFILE = 'E:/Transit-Casa-Alex/Input/Bus_Stops/2016Bus_Stops_2016.shp'

hdffile = HDF_INFILE
store = pd.HDFStore(hdffile)

df = store.select('stop_day', columns = ['STOP_LAT','STOP_LON','STOP_ID','STOPNAME','MONTH'])

df = df[df['MONTH'].isin(pd.date_range(MONTH1,MONTH2))]

df = df.groupby(by = 'STOP_ID', as_index = False).mean()

df.to_csv(CSV_OUTFILE)

df['geometry'] = df.apply(lambda x: Point((float(x.STOP_LON), float(x.STOP_LAT))), axis=1)
stops = gp.GeoDataFrame(df, geometry='geometry')

stops.to_file(SHP_OUTFILE, driver='ESRI Shapefile',crs = {'init':'epsg:4326'})
