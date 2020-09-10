# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class TEMA_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(TEMA_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['TEMA_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[df[CLOSE] > features, 'TEMA_FT'] = LONG
		df.loc[df[CLOSE] < features, 'TEMA_FT'] = SHORT

		# make everything clean
		out_series = df['TEMA_FT']
		df.drop(columns=['TEMA_FT'], inplace = True)

		# For test
		# df['TEMA(20)'] = features
		# df['TEMA(20)_transformed'] = out_series
		# df.to_csv("../test_reports/TEMA_test/TEMA20_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.TEMA import TEMA
	TEMA = TEMA(20, CLOSE)
	tema_values = TEMA.calculate(df)

	# Transforming the Features
	tema_transformed = TEMA_FT().transform(df, tema_values)

	print (tema_transformed)


