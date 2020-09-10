# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class Drive(Indicator):
	# Drive indicator with the number of 2040 in the indicator list
    # the link of the indicator is https://www.mql5.com/en/code/9460
	
    def __init__(self, period = 16):
        super(Drive, self).__init__()
        self.period = period

    def calculate(self, df):
        '''
        returns the value of two lines which names are Up and Down
        :param: period: the priod of lines
        : the 
        :return: the Up and Down vlues as panda series
        '''
        df['Up'] = ((df[HIGH] - df[OPEN]) + (df[CLOSE] - df[LOW]))/2
        df['Down'] = ((df[OPEN] - df[LOW]) + (df[HIGH] - df[CLOSE]))/2
        out_series_up = df['Up'].rolling(window = self.period).mean()
        out_series_down = df['Down'].rolling(window = self.period).mean()
        df.drop(columns=['Up', 'Down'], inplace = True)

		# For testing
        # df['Drive(20)-UP'] = out_series_up
        # df['Drive(20)-DOWN'] = out_series_down
        # df.to_csv("../test_reports/Drive_test/Drive20.csv")

        return out_series_up,out_series_down

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_Drive = Drive(20)
	my_Drive.calculate(df)
	print (df)