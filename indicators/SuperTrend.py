# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *
from indicators.ATR import ATR

class SuperTrend(Indicator):
	# SuperTrend indicator
    # The formula was taken from https://www.tradinformed.com/calculate-supertrend-indicator-using-excel/#formulas
	# actually there is a video in the website which explains completely
    
    def __init__(self, period = 10, multiplier = 3):
        super(SuperTrend, self).__init__()
        self.period = period
        self.multiplier = multiplier

    def calculate(self, df):
        '''
		returns the values of supertrend
		:param: period: the period of the supertrend which is also used for the atr inside it
        :multiplier: its a constant which is set by the user
		:return: the SuperTrend values as a panda series
        '''
        my_atr = ATR(self.period)
        df['atr'] = my_atr.calculate(df)
        
        # Compute basic upper and lower bands
        df['basic_ub'] = (df[HIGH] + df[LOW]) / 2 + self.multiplier * df['atr']
        df['basic_lb'] = (df[HIGH] + df[LOW]) / 2 - self.multiplier * df['atr']
        
        # Compute final upper and lower bands
        df['final_ub'] = 0.00
        df['final_lb'] = 0.00
        for i in range(self.period, len(df)):
            df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i - 1] or df[CLOSE].iat[i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[i - 1]
            df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i - 1] or df[CLOSE].iat[i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[i - 1]
      
        # Set the Supertrend value
        df['SuperTrend'] = 0.00
        for i in range(self.period, len(df)):
            df['SuperTrend'].iat[i] = df['final_ub'].iat[i] if df['SuperTrend'].iat[i - 1] == df['final_ub'].iat[i - 1] and df[CLOSE].iat[i] <= df['final_ub'].iat[i] else \
                                      df['final_lb'].iat[i] if df['SuperTrend'].iat[i - 1] == df['final_ub'].iat[i - 1] and df[CLOSE].iat[i] >  df['final_ub'].iat[i] else \
                                      df['final_lb'].iat[i] if df['SuperTrend'].iat[i - 1] == df['final_lb'].iat[i - 1] and df[CLOSE].iat[i] >= df['final_lb'].iat[i] else \
                                      df['final_ub'].iat[i] if df['SuperTrend'].iat[i - 1] == df['final_lb'].iat[i - 1] and df[CLOSE].iat[i] <  df['final_lb'].iat[i] else 0.00 
     
        out_series = df['SuperTrend']
        df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb', 'SuperTrend'], inplace=True, axis=1)
        
		# For testing
        '''
        df['SuperTrend10'] = out_series
        df.to_csv("../test_reports/SuperTrend_test/SuperTrend10.csv")
        '''
        return out_series

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_SuperTrend = SuperTrend(10)
	my_SuperTrend.calculate(df)
