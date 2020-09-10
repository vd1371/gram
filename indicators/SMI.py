import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *


class SMI(Indicator):
        # Stochastic Momentum Index
        # the calculation is based on https://www.barchart.com/trader/help/studies/stoch_mom.php
        def __init__(self, period = 14, smoothing_period = 3):
                super(SMI, self).__init__()
                self.period = period
                self.smoothing_period = smoothing_period

        def calculate(self, df):
                '''
                returns the values of the stochastic momentum index
                :param: period: the period of the SMI indicator
                :param: smoothing_period: the smoothing period 
                :return: the SMI values as a panda series
                '''

                hig_max = df[HIGH].rolling(window = self.period).max()
                low_min = df[LOW].rolling(window = self.period).min()
                # center of low to high range
                center = (hig_max + low_min) / 2 
                #subtract distance of Current Close from the Center of the Range.
                dist2center = df[CLOSE] - center
                # smooth distance to center with an exponential moving average
                dist2center_smoothed = dist2center.ewm(span = self.smoothing_period).mean() 
                dist2center_smoothed2 = dist2center_smoothed.ewm(span = self.smoothing_period).mean()
                range_price = hig_max - low_min
                # smooth range with an exponential moving average
                range_smoothed = range_price.ewm(span = self.smoothing_period).mean() 
                range_smoothed2 = range_smoothed.ewm(span = self.smoothing_period).mean()/2
                out_series = dist2center_smoothed2/range_smoothed2*100

                return out_series
	
if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_SMI = SMI(period = 14, smoothing_period = 3)
	df['SMI(14,3)'] = my_SMI.calculate(df)
	df.to_csv("SMI_test.csv")
