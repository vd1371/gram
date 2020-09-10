# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class I5_34_5(Indicator):
	# 5_34_5 indicator with the number of 199 in the indicator list
    # the link of the indicator is https://www.mql5.com/en/code/7727

	
    def __init__(self):
        super(I5_34_5, self).__init__()

    def calculate(self, df):
        '''
        returns the value of subtraction of the SMA(5) and SMA(34)
        the original indicator has another line in it but because it's a C0 indicator
        I just calculated the first line value
        :param: No parameter is needed
        :return: the subtraction vlues as panda series
        '''
        median = (df[HIGH] + df[LOW])/2
        SMA_34 = median.rolling(34).mean()
        SMA_5 = median.rolling(5).mean()
        out_series = SMA_5 - SMA_34
        
		
		# For testing
        # df['5_34_5'] = out_series
        # df.to_csv("../test_reports/5_34_5_test/5_34_5.csv")
        
        return out_series

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_I5_34_5 = I5_34_5()
	my_I5_34_5.calculate(df)