import sys
import datetime

sys.path.append('C:\Workspace\SOURCE\sf_taxi\sfdata_wrangler')

from SFMuniDataHelper import SFMuniDataHelper
from TransitReporter import TransitReporter

MULTIMODAL_REPORT_XLSFILE = "E:\Transit_Casa\Alex\Output\Performence Report/MultiModalReport.xlsx"
DEMAND_REPORT_XLSFILE = "E:\Transit_Casa\Alex\Output\Performence Report/DriversOfDemandReport.xlsx"
MUNI_REPORT_XLSFILE = "E:\Transit_Casa\Alex\Output\Performence Report/MuniPerformanceReport.xlsx"
REPORT_ROUTEPLOTS = "E:\Transit_Casa\Alex\Output\Performence Report/RoutePlots"
GTFS_OUTFILE = "E:\Transit_Casa\Alex\Output\PerformanceReports/gtfs.h5"
DEMAND_OUTFILE = "E:\Transit_Casa\Alex\Output\Performence Report/drivers_of_demand.h5"
MONTHLY_TRIP_OUTFILE = "E:\Transit_Casa\Output/sfmuni_monthly_trip.h5"
MONTHLY_TS_OUTFILE   = "E:\Transit_Casa\Output/sfmuni_monthly_ts.h5"
MULTIMODAL_OUTFILE = "E:\Transit_Casa\Alex\Output\Performence Report/multimodal.h5"




#change these and then run for all time of days

MONTH1 = '2009-09-01'
MONTH2 = '2013-09-01'
TOD = ['0300-0559', '0600-0859','0900-1359','1400-1559','1600-1859','1900-2159','2200-0259','Daily']
#ROUTESHORTNAME is a string
ROUTESHORTNAME = '3'
#DIRECTION is an integer
DIRECTION = 0
#DOW is an integer
DOW = 1



startTime = datetime.datetime.now()   
                
reporter = TransitReporter(trip_file=MONTHLY_TRIP_OUTFILE, 
                                  ts_file=MONTHLY_TS_OUTFILE, 
                                  demand_file=DEMAND_OUTFILE,
                                  gtfs_file=GTFS_OUTFILE, 
                                  multimodal_file=MULTIMODAL_OUTFILE)
for tod in TOD:        
    reporter.createRoutePlot(REPORT_ROUTEPLOTS, 
                                 months=('2009-09-01', '2013-09-01'), 
                                 dow=DOW, 
                                 tod=tod, 
                                 route_short_name=ROUTESHORTNAME, 
                                 dir=DIRECTION)

        
    print ('Finished performance reports in ', (datetime.datetime.now() - startTime) )

print ('Run complete!  Time for a pint!')