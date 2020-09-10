# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class ATR(Indicator):
	# Average True Range (ATR) indicator
    # The formula was taken from https://www.investopedia.com/terms/a/atr.asp
	
    def __init__(self, period = 14):
        super(ATR, self).__init__()
        self.period = period

    def calculate(self, df):
        '''
		returns the values of ATR
		:param: period: the period of the ATR
		:return: the ATR values as a panda series
        '''
        df['HIGH-LOW'] = df[HIGH] - df[LOW]
        df['LOW-LASTCLOSE'] = abs(df[LOW]-df[CLOSE].shift(1))
        df['HIGH-LASTCLOSE'] = abs(df[HIGH]-df[CLOSE].shift(1))
        df['TR'] = df[['HIGH-LOW','LOW-LASTCLOSE','HIGH-LASTCLOSE']].max(axis=1)
        out_series = df['TR'].rolling(window = self.period).mean()
        df.drop(['TR', 'HIGH-LOW','LOW-LASTCLOSE','HIGH-LASTCLOSE'],inplace=True, axis=1)
        
		# For testing
        '''
        df['ATR(14)'] = out_series
        df.to_csv("../test_reports/ATR_test/ATR_14.csv")
        '''
        return out_series

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_ATR = ATR(14)
	my_ATR.calculate(df)
