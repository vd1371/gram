# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
import numpy as np
sys.path.insert(0,'..')
from indicators.Indicator import Indicator
from utils.GlobalVariables import *

class SPR(Indicator):
    # SPR indicator: https://www.mql5.com/en/code/7065
    # the code is written based on the discription in mql5 website

    def __init__(self, period = 14):
            super(SPR, self).__init__()
            self.period = period

    def calculate(self, df):
        '''
        returns the values of Spear's rank correlation
        :param: period
        :return: the SPR values a a panda series

        '''
        def srd(values):
            # this function calculates the sum of squared rank-different
            ranking = values.rank()
            diff = ranking - 1 - range(len(values))
            return sum(diff**2)
        df['SRD'] = df[CLOSE].rolling(self.period).apply(srd, raw = False)
        SPR = 1 - 6*df['SRD']/(self.period*(self.period**2-1))

        # For testing
        #df['SPR(14)'] = SPR
        #df.to_csv("../test_reports/SPR_test/SPR14.csv")

        df.drop(columns=['SRD'], inplace = True)

        return SPR


if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_SPR = SPR(14)
	my_SPR.calculate(df)
