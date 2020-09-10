# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class FDI_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(FDI_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['FDI_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[features < 1.5, 'FDI_FT'] = TRADE
		df.loc[features > 1.5, 'FDI_FT'] = WAIT

		# make everything clean
		out_series = df['FDI_FT']
		df.drop(columns=['FDI_FT'], inplace = True)

		# For test
		#df['FDI(14)'] = features
		#df['FDI(14)_transformed'] = out_series
		#df.to_csv("../test_reports/FDI_test/FDI(14)_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.FDI import FDI
	fdi = FDI(14, CLOSE)
	fdi_values = fdi.calculate(df)

	# Transforming the Features
	fdi_transformed = FDI_FT().transform(df, fdi_values)

	print (fdi_transformed)


