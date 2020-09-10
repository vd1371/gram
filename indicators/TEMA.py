# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class TEMA(Indicator):
	# Triple exponential moving average indicator
	# https://www.investopedia.com/terms/t/triple-exponential-moving-average.asp
	# TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
	
	def __init__(self, period = 14, on = CLOSE):
		super(TEMA, self).__init__()
		self.period = period
		self.on = on

	def calculate(self, df):
		'''
		returns the values of the simple moving average
		:param: period: the period of the EMA indicator
		:param: on: close, open, HLC/3
		:return: the TEMA values as a panda series
		'''
		if self.on == HLC_3: df[HLC_3] = (df[HIGH] + df[LOW] + df[CLOSE])/3
		
		df[f'EMA-{self.period}'] = df[self.on].ewm(span = self.period).mean()
		df['EMA2'] = df[f'EMA-{self.period}'].ewm(span = self.period).mean()
		df['EMA3'] = df['EMA2'].ewm(span = self.period).mean()
		out_series = 3*df[f'EMA-{self.period}'] - 3*df['EMA2'] + df['EMA3']

		# Dropping added columns
		if self.on == HLC_3: df.drop(columns = [HLC_3])
		df.drop(columns = [f'EMA-{self.period}', 'EMA2', 'EMA3'], inplace = True)
		
		# For testing
# 		df['TEMA(14)'] = out_series
# 		df.to_csv("../test_reports/TEMA_test/TEMA14.csv")
		
		return out_series
		
		
		

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_TEMA = TEMA(14, CLOSE)
	print (my_TEMA.calculate(df))
	print (df)