# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class AroonHorn_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(AroonHorn_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['AroonHorn_FT'] = np.zeros(len(df))

		# Parsing the features
		AroonHorn_up = features[0]
		AroonHorn_down = features[1]

		# Interpreting the values
		df.loc[AroonHorn_up > AroonHorn_down, 'AroonHorn_FT'] = LONG
		df.loc[AroonHorn_up < AroonHorn_down, 'AroonHorn_FT'] = SHORT

		# make everything clean
		out_series = df['AroonHorn_FT']
		df.drop(columns=['AroonHorn_FT'], inplace = True)

		# For test
		# df['AroonHorn_up'] = features[0]
		# df['AroonHorn_down'] = features[1]
		# df['AroonHorn(20)_transformed'] = out_series
		# df.to_csv("../test_reports/Aroon_test/AroonHorn20_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.AroonHorn import AroonHorn
	aroon_horn = AroonHorn(20)
	aroon_horn_values = aroon_horn.calculate(df)

	# Transforming the Features
	aroon_horn_transformed = AroonHorn_FT().transform(df, aroon_horn_values)

	print (aroon_horn_transformed)