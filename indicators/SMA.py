# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class SMA(Indicator):
	# Simple moving average indicator
	
	def __init__(self, period = 14, on = CLOSE):
		super(SMA, self).__init__()
		self.period = period
		self.on = on

	def calculate(self, df):
		'''
		returns the values of the simple moving average
		:param: period: the period of the SMA indicator
		:param: on: close, open, HLC/3
		:return: the SMA values as a panda series
		'''
		if self.on == HLC_3: df[HLC_3] = (df[HIGH] + df[LOW] + df[CLOSE])/3
		out_series = df[self.on].rolling(window = self.period).mean()
		if self.on == HLC_3: df.drop(columns=[HLC_3], inplace = True)
		
		# For testing
		'''
		df['SMA(20)'] = out_series
		df.to_csv("../test_reports/SMA_test/SMA20.csv")
		'''
		return out_series

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_SMA = SMA(20, CLOSE)
	my_SMA.calculate(df)
	print ('Done')