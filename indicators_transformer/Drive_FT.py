# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class Drive_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(Drive_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['Drive_FT'] = np.zeros(len(df))

		# Parsing the features
		drive_up = features[0]
		drive_down = features[1]

		# Interpreting the values
		df.loc[drive_up > drive_down, 'Drive_FT'] = LONG
		df.loc[drive_up < drive_down, 'Drive_FT'] = SHORT

		# make everything clean
		out_series = df['Drive_FT']
		df.drop(columns=['Drive_FT'], inplace = True)

		# For test
		# df['Drive_up'] = features[0]
		# df['Drive_down'] = features[1]
		# df['Drive(20)_transformed'] = out_series
		# df.to_csv("../test_reports/Drive_test/Drive20_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.Drive import Drive
	Drive = Drive(20)
	drive_values = Drive.calculate(df)

	# Transforming the Features
	drive_transformed = Drive_FT().transform(df, drive_values)

	print (drive_transformed)


