# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class SVS_Trend_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SVS_Trend_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['SVS_Trend_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[features > 0, 'SVS_Trend_FT'] = LONG
		df.loc[features < 0, 'SVS_Trend_FT'] = SHORT

		# make everything clean
		out_series = df['SVS_Trend_FT']
		df.drop(columns=['SVS_Trend_FT'], inplace = True)

		# For test
		# df['SVS'] = features
		# df['SVS_transformed'] = out_series
		# df.to_csv("../test_reports/SVS_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.SVS_Trend import SVS_Trend
	ind = SVS_Trend(14, 5)
	ind_values = ind.calculate(df)

	# Transforming the Features
	ind_transformed = SVS_Trend_FT().transform(df, ind_values)

	print (ind_transformed)


