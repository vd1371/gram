# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class SPR_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SPR_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['SPR_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[features > 0 , 'SPR_FT'] = LONG
		df.loc[features < 0 , 'SPR_FT'] = SHORT

		# make everything clean
		out_series = df['SPR_FT']
		df.drop(columns=['SPR_FT'], inplace = True)

		# For test
		#df['SPR(14)'] = features
		#df['SPR(14)_transformed'] = out_series
		#df.to_csv("../test_reports/SPR_test/SPR14_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.SPR import SPR
	spr = SPR(14)
	spr_values = spr.calculate(df)

	# Transforming the Features
	spr_transformed = SPR_FT().transform(df, spr_values)

	print (spr_transformed)


