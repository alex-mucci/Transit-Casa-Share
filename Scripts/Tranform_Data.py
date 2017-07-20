import pandas as pd


drop = ['Unnamed: 0',
'STOP_LAT_x',
'STOP_LON_x',
'STOP_LAT_y',
'STOP_LON_y',
'geometry',
'index_right',
'ALAND00',
'AWATER00',
'COUNTYFP00',
'CTIDFP00',
'NAME00',
'TRACTCE00',
'Id',
'Id2',
'Geography',
'geometry_a',
'geometry_e',
'geometry_f',
'STOP_LAT',
'STOP_LON',
'FID_1']


change = ['Average Hourly Price',
'Count_',
'EDHLTH_RAC_SCALED',
'EDHLTH_WAC_SCALED',
'EMP_RAC_SCALED',
'EMP_WAC_SCALED',
'HOUSING_09_SCALED',
'LEISER_RAC_SCALED',
'LEISER_WAC_SCALED',
'OTHER_RAC_SCALED',
'OTHER_WAC_SCALED',
'PER_HH_0VEH',
'PER_INCOME_0-15',
'PER_INCOME_100+',
'PER_INCOME_15-50',
'PER_INCOME_50-100',
'PRICE12HR',
'PRICE1HR',
'PRICE2HR',
'PRICE3HR',
'PRICE4HR',
'PRICEDAY',
'PRICEDAYDISCOUNT',
'RETAIL_RAC_SCALED',
'RETAIL_WAC_SCALED',
'Workers_16_And_Over_Mean_Travel_Time_To_Work_(Minutes)',
'parking_rate']

changes = ['PARK_HOURLY_AVG_ON',
'TRANSBAY',
'EDHLTH_RAC_DEN',
'EDHLTH_WAC_DEN',
'EMP_RAC_DEN',
'EMP_WAC_DEN',
'HOUSING_09_DEN',
'LEISER_RAC_DEN',
'LEISER_WAC_DEN',
'OTHER_RAC_DEN',
'OTHER_WAC_DEN',
'SHR_HH_0VEH',
'SHR_INCOME_0_15',
'SHR_INCOME_100P',
'SHR_INCOME_15_50',
'SHR_INCOME_50_100',
'PARK_12_HR_OFF_PUB',
'PARK_1_HR_OFF_PUB',
'PARK_2_HR_OFF_PUB',
'PARK_3_HR_OFF_PUB',
'PARK_4_HR_OFF_PUB',
'PARK_DAY_OFF_PUB',
'PARK_DAY_DISCOUNT_OFF_PUB',
'RETAIL_RAC_DEN',
'RETAIL_WAC_DEN',
'AVG_TT_TO_WORK_MINUTES',
'PARKING_RATE_OFF_RESIDENTIAL']



change = ['BART_FROMS','BART_TOS','MUNI_RAIL_ALIGHTINGS','MUNI_RAIL_BOARDINGS','CALTRAIN_OFF','CALTRAIN_ON','NUM_BUS_STOPS']

check = ['EMP_WAC_DEN','LEISER_RAC_DEN','LEISER_WAC_DEN','OTHER_RAC_DEN','OTHER_WAC_DEN','RETAIL_RAC_DEN','RETAIL_WAC_DEN','ON']

log_change = ['PARK_12_HR_OFF_PUB',
'BIKE_BOARDINGS',
'BIKE_ALIGHTINGS',
'BIKE_AVG',     
'PARK_1_HR_OFF_PUB',
'PARK_2_HR_OFF_PUB',
'PARK_3_HR_OFF_PUB',
'PARK_4_HR_OFF_PUB',
'AVG_BART',
'AVG_HH_SIZE',
'AVG_TT_TO_WORK_MINUTES',
'BART_FROMS',
'BART_TOS',
'CALTRAIN_AVG',
'CALTRAIN_OFF',
'CALTRAIN_ON',
'CAPACITY',
'CROWDED',
'CROWDHOURS',
'PARK_DAY_DISCOUNT_OFF_PUB',
'PARK_DAY_OFF_PUB',
'DWELL',
'DWELL_S',
'EDD_EMP',
'EDHLTH_RAC_DEN',
'EDHLTH_WAC_DEN',
'EMP_RAC_DEN',
'EMP_WAC_DEN',
'FARE',
'FREQ_S',
'FULLFARE_REV',
'HEADWAY_S',
'HH_DEN_ACS',
'PARK_HOURLY_AVG_ON',
'HOUSING_09_DEN',
'HU_DEN_ACS',
'LEISER_RAC_DEN',
'LEISER_WAC_DEN',
'MUNI_RAIL_ALIGHTINGS',
'MUNI_RAIL_AVG',
'MUNI_RAIL_BOARDINGS',
'NUM_BUS_STOPS',
'OCC_RATE',
'OFF',
'ON',
'ONTIME5',
'OTHER_RAC_DEN',
'OTHER_WAC_DEN',
'PARKING_RATE_OFF_RESIDENTIAL',
'PASSDELAY_ARR',
'PASSDELAY_DEP',
'PASSHOURS',
'PASSMILES',
'POP_DEN_ACS',
'RDBRDNGS',
'RETAIL_RAC_DEN',
'RETAIL_WAC_DEN',
'RUNSPEED',
'RUNSPEED_S',
'RUNTIME',
'RUNTIME_S',
'SHR_HH_0VEH',
'SHR_INCOME_0_15',
'SHR_INCOME_100P',
'SHR_INCOME_15_50',
'SHR_INCOME_50_100',
'TOTSPEED',
'TOTSPEED_S',
'TOTTIME',
'TOTTIME_S',
'Total_Housing_Units',
'Total_Pop',
'VAC_RATE',
'VC',
'WAITHOURS']


OUTFILE =

def rename_column(old_columns,new_columns,df):
    num = len(old_columns)
    count = 0
    while count < num:
        df[new_columns[count]] = df[old_columns[count]]
        df = df.drop(old_columns[count],axis = 1)
        
        count = count + 1
    return df
    
    
def check(value):
    if value == 'N':
        value = ''
    else:
        value = value
    return value
    
    

estimate = pd.read_csv('E:/Transit-Casa-Alex/Output/Modeling/2009/Tenth_Data_rs_day.csv',thousands = ',')
estimate['FREQ_S'] = 1 / (estimate['HEADWAY_S'] / 60.0)
estimate['NUM_BUS_STOPS'] = estimate['NUM_BUS_STOPS'] - 1

estimate.RUNSPEED = estimate.RUNSPEED.clip(upper = 40)
estimate.RUNSPEED = estimate.TOTSPEED.clip(upper = 40)

estimate = estimate.drop(drop,axis = 1)

for column in change:
    estimate[column] = estimate[column].fillna(0)
    

    
estimate = rename_column(change,changes,estimate)


estimate['EXCLUDE'] = 0
count = 0
for column in check:
    while count < len(estimate[column]):
        if np.isnan(estimate[column][count]):
                print('Got One')
                estimate['EXCLUDE'][count] = 1
        count = count + 1
        
        
data = estimate[estimate['EXCLUDE'] == 0].

data['AVG_RIDE'] = (data.ON + data.OFF)/2
data['LOG_RIDERS'] = np.log(data.AVG_RIDE + 1)

data['AVG_BART'] = (data['BART_FROMS']+data['BART_TOS'])/2
data['CALTRAIN_AVG'] = (data.CALTRAIN_OFF + data.CALTRAIN_ON)/2
data['MUNI_RAIL_AVG'] = (data.MUNI_RAIL_ALIGHTINGS + data.MUNI_RAIL_BOARDINGS)/2
data['BIKE_AVG'] = (data.BIKE_ALIGHTINGS + data.BIKE_BOARDINGS)/2

for column in log_change:
    data[column + '_LOG'] = data[column].apply(lambda value: np.log(value + 1))
    
data.AVG_TT_TO_WORK_MINUTES = data.AVG_TT_TO_WORK_MINUTES.convert_objects(convert_numeric = True)

data['DIST_FROM_LAST_STOP'] = data['SERVMILES_S'] / (data['FREQ_S']*24)

data['DIST_FROM_LAST_STOP_LOG'] = data['DIST_FROM_LAST_STOP'].apply(lambda value: np.log(value + 1))

data['SERVMILES_S_LOG'] = data['SERVMILES_S'].apply(lambda x : np.log(x + 1))
    
data['EOL_SOL'] = data['EOL'] + data['SOL']

data.to_csv(OUTFILE)