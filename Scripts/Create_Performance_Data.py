import pandas as pd


TABLE = 'rs_day'
H5INFILE = 'E:/Transit-Casa-Alex/Input/Bus Performence/sfmuni_monthly_ts.h5'
MONTHS = ['2016-10-01','2016-11-01','2016-12-01']
YEAR = 2016


if __name__ == "__main__":
    store = pd.HDFStore(H5INFILE)
    df = store.select(TABLE,where = "'MONTH' == MONTHS & 'ROUTE_TYPE' == 3")

    df.to_csv('E:/Transit-Casa-Alex/Output/Final Data/' + str(YEAR) + '/Bus_Performance_Data_' + TABLE + '.csv')
    
    print('Finished!')