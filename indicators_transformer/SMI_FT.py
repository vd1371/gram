# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class SMI_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SMI_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['SMI_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[features > 0, 'SMI_FT'] = LONG
		df.loc[features < 0, 'SMI_FT'] = SHORT

		# make everything clean
		out_series = df['SMI_FT']
		df.drop(columns=['SMI_FT'], inplace = True)

		# For test
		#df['SMI(14)'] = features
		#df['SMI(14)_transformed'] = out_series
		#df.to_csv("../test_reports/SMI_test/SMI14_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.SMI import SMI
	smi = SMI(14 , 3)
	smi_values = smi.calculate(df)

	# Transforming the Features
	smi_transformed = SMI_FT().transform(df, smi_values)

	print (smi_transformed)


