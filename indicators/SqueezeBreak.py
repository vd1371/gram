# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class SqueezeBreak(Indicator):
	# Squeeze break volume indicator
	# https://www.mql5.com/en/code/8840
	
	def __init__(self, boll_period = 14, keltner_period = 20):
		super(SqueezeBreak, self).__init__()
		self.boll_period = boll_period
		self.keltner_period = keltner_period
	
	def calculate(self, df):
		'''
		returns the values of the squuze break
		:param: period: the period of the squuze break indicator indicator
		:return: the squeeze break indicator values as a panda series
		'''

		# Keltner bands are ema +- 2*ATR

		# So first we need to calculate ATR
		df['HIGH-LOW'] = df[HIGH] - df[LOW]
		df['LOW-LASTCLOSE'] = abs(df[LOW]-df[CLOSE].shift(1))
		df['HIGH-LASTCLOSE'] = abs(df[HIGH]-df[CLOSE].shift(1))
		df['TR'] = df[['HIGH-LOW','LOW-LASTCLOSE','HIGH-LASTCLOSE']].max(axis=1)
		atr = df['TR'].rolling(window = self.keltner_period).mean()
		df.drop(['TR', 'HIGH-LOW','LOW-LASTCLOSE','HIGH-LASTCLOSE'],inplace=True, axis=1)
		
		# Let's create keltner band
		keltner_mid = df[CLOSE].ewm(span = self.keltner_period).mean()
		keltner_upper = keltner_mid + 2*atr
		keltner_lower = keltner_mid + 2*atr
		
		# Bollinger bands are SMA(price) +- 2*stdev (prices)
		std = df[CLOSE].rolling(window = self.boll_period).std()
		boll_mid = df[CLOSE].rolling(window = self.boll_period).mean()
		boll_upper = boll_mid + 2*std
		boll_lower = boll_mid - 2*std

		# Squeeze break is essentially the difference between the boll_upper and the keltner_uppre
		squeeze_break = 2*(boll_upper-keltner_upper)

		# For testing
		# df['SqueezeBreak(20)'] = squeeze_break
		# df.to_csv("../test_reports/SqueezeBreak20.csv")

		return squeeze_break

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_Squueze = SqueezeBreak(20, 20)
	my_Squueze.calculate(df)