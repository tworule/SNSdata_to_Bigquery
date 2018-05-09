import sys
import pandas
sys.stdout.flush()

df = pandas.DataFrame({'date' : [0,1]})
pandas.DataFrame.to_gbq(df, 'SNS_data.first_test', 'datamingo', if_exists = 'append', chunksize = 10000, verbose = True)