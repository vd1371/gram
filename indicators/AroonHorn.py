# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
import numpy as np
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class AroonHorn(Indicator):
	# AroonHorn indicator: https://www.mql5.com/en/code/8399
	# https://www.investopedia.com/ask/answers/112814/what-aroon-indicator-formula-and-how-indicator-calculated.asp
	
	def __init__(self, period = 14):
		super(AroonHorn, self).__init__()
		self.period = period

	def calculate(self, df):
		'''
		returns the values of Aroon horn
		:param: period
		:return: the AroonHorn values as two panda series

		Aroon_Up = ((period-number_of_periods_since_highest_high)/period)*100 = ((argmin(highest_high)-1)/period)*100
		but since Aroon_up must be between 0 and 100, inclusive, I think the period must be (period-1)

		Similar foraroon down
		'''
		df['Aroon_Up'] = (df[HIGH].rolling(self.period).apply(np.argmax, raw=True))/(self.period-1)*100
		df['Aroon_Down'] = (df[LOW].rolling(self.period).apply(np.argmin, raw= True))/(self.period-1)*100

		aroon_up = df['Aroon_Up']
		aroon_down = df['Aroon_Down']

		# For testing
		# df.to_csv("../test_reports/Aroon_test/Aroon14.csv")

		df.drop(columns=['Aroon_Up', 'Aroon_Down'])

		return aroon_up, aroon_down


if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	
	my_AH = AroonHorn(14)
	print (my_AH.calculate(df))
