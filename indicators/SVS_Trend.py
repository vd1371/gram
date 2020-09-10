# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class SVS_Trend(Indicator):
	# SVS-Trend indicator with the number of 1988 in the indicator list
    # the link of the indicator is https://www.mql5.com/en/code/7260

	
    def __init__(self, period_1 = 4, period_2 = 8):
        super(SVS_Trend, self).__init__()
        self.period_1 = period_1
        self.period_2 = period_2

    def calculate(self, df):
        '''
        returns the value of subtraction of twe weighted SMAs
        the original indicator has other lines in it but because it's a C0 indicator
        I just calculated the first line value
        :param: Two parameters for the SMA calculation is needed
        :return: the subtraction vlues as panda series
        '''
        df['weighted_price'] = (df[HIGH] + df[LOW] + df[CLOSE] + df[CLOSE])/4
        SMA_period_1 = df['weighted_price'].rolling(window = self.period_1).mean()
        SMA_period_2 = df['weighted_price'].rolling(window = self.period_2).mean()
        out_series = SMA_period_1 - SMA_period_2

        # dropping added columns
        df.drop(columns = ['weighted_price'], inplace = True)
        
		
		# For testing
        '''
        df['SVS_Trend'] = out_series
        
        df.to_csv("../test_reports/SVS_Trend_test/SVS_Trend.csv")
		'''
        return out_series

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_SVS_Trend = SVS_Trend()
	my_SVS_Trend.calculate(df)