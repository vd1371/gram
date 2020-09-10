# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pprint

from data.FXDataLoader import Pair
from trader.BaseTrader import BaseTrader
from trader.Trade import Trade
from indicators.ATR import ATR
from decision_models.CoinToss import CoinToss

class MatrixTrader(BaseTrader):

	# The trade's method of this class will iterate over rows
	# it predicts one row at a time

	def __init__(self,main_pair, aux_pair, balance = 10000, risk = 0.02, spread = 3, should_trailing_stop = True, timeframe = '1D', atr_multiplier_trailing = 1):

		super(MatrixTrader, self).__init__(main_pair.name)

		self.main_pair = main_pair
		self.aux_pair = aux_pair
		self.balance = balance
		self.risk = risk
		self.spread = spread/10000 if not 'JPY' in self.main_pair.name else spread/100
		self.should_trailing_stop = should_trailing_stop
		self.atr_multiplier_trailing = atr_multiplier_trailing

		if timeframe == '1D':
			self.df = main_pair.get_1D()
			self.df_aux = aux_pair.get_1D()
		elif timeframe == '4H':
			self.df = main_pair.get_4H()
			self.df_aux = aux_pair.get_4H()
		elif timeframe == '1H':
			self.df = main_pair.get_1H()
			self.df_aux = aux_pair.get_1H()

		self.atr = ATR(14).calculate(self.df)
		
	def simulate(self, signals, clsoing_signal = None, should_draw = True, should_analyze = True, should_save = True):
		# Report should be dataframe of all trades consisiting the trades' reports
		# Trades' report is a dictionary. You may find it in the Trade class in the same folder
		# total_profit is the sum of all trades' profits

		# Initializing the the required parameters
		in_trade = False
		trade_list = []
		total_profits = 0
		balance = self.balance

		# iterating over indices
		for index, next_index in zip(signals.index[:-1], signals.index[1:]):
		
			# Knowing the signal at the current time
			signal = signals[index]

			# check if we have an open trade
			if in_trade:
				
				# See if we have encountered an opposite signal
				if not isinstance (clsoing_signal, pd.Series):
					opposite_signal = trade.trade_type * signal < 0
				else:
					opposite_signal = trade.trade_type * clsoing_signal[index] < 0

				# Close the trade with opposite signal
				if opposite_signal:

					in_trade = False

					# Check if we have closed the trade_1 yet or not
					if trade.trade_1_open:
						trade.set_closing_info_1(closing_time = index,
												main_closing_price = self.df.loc[index, CLOSE],
									 			aux_closing_price = self.df_aux.loc[index, CLOSE],
									 			closing_reason = 'opposite_signal')
					# Closing the trade_2
					trade.set_closing_info_2(closing_time = index,
											main_closing_price = self.df.loc[index, CLOSE],
								 			aux_closing_price = self.df_aux.loc[index, CLOSE],
								 			closing_reason = 'opposite_signal')

					profit, balance = trade.evaluate()
					trade_list.append(trade.get_report())
					total_profits += profit

				else:

					for time, moment_row in self.main_pair.get_5M().loc[index:next_index].iterrows():
						
						# check stoplosses
						cross_sl1 = ((trade.trade_type is SHORT and moment_row[CLOSE] > trade.stop_loss1) or
							    (trade.trade_type is LONG and moment_row[CLOSE] < trade.stop_loss1))

						cross_sl2 = ((trade.trade_type is SHORT and moment_row[CLOSE] > trade.stop_loss2) or
							    (trade.trade_type is LONG and moment_row[CLOSE] < trade.stop_loss2))

						if cross_sl2:
							in_trade = False
							if trade_1_open:
								trade.set_closing_info_1(closing_time = time,
											 main_closing_price = trade.stop_loss1,
											 aux_closing_price = -1,
											 closing_reason = 'stop_loss')

							trade.set_closing_info_2(closing_time = time,
											 main_closing_price = trade.stop_loss2,
											 aux_closing_price = -1,
											 closing_reason = 'stop_loss')
							
							profit, balance = trade.evaluate()
							trade_list.append(trade.get_report())
							total_profits += profit
							break
							    
						if cross_sl1:
							trade.set_closing_info_1(closing_time = time,
											 main_closing_price = trade.stop_loss1,
											 aux_closing_price = -1,
											 closing_reason = 'stop_loss')
						# check take profit
						crossTP = ((trade.trade_type is SHORT and moment_row[CLOSE] < trade.take_profit) or
							   (trade.trade_type is LONG and moment_row[CLOSE] > trade.take_profit))

						if crossTP:
							trade.set_closing_info_1(closing_time = time,
											 main_closing_price = trade.stop_loss1,
											 aux_closing_price = -1,
											 closing_reason = 'take_profit')

				# check pelle                        
				if trade.trade_type is LONG and self.df.loc[index, CLOSE] > trade.pelle_price:
					trade.stop_loss2 = trade.pelle_price - self.atr_multiplier_trailing * self.atr[index]
					trade.pelle_price = trade.pelle_price + self.atr_multiplier_trailing * self.atr[index]
				
				if trade.trade_type is SHORT and self.df.loc[index, CLOSE] < trade.pelle_price:
					trade.stop_loss2 = trade.pelle_price + self.atr_multiplier_trailing * self.atr[index]
					trade.pelle_price = trade.pelle_price - self.atr_multiplier_trailing * self.atr[index]


			
			if not in_trade and pd.notna(self.atr[index]) and (signal == 1 or signal == -1):

				trade_type = signal
				in_trade = True
				trade = Trade(self.main_pair.name, self.aux_pair.name)
				trade.set_opening_info(opening_time = next_index,
						 main_open_price = self.df[OPEN][next_index],
						 aux_open_price = self.df[OPEN][next_index],
						 trade_type = trade_type,
						 balance = balance,
						 ATR = self.atr[index],
						 risk = self.risk,
						 stop_loss1=  self.df[OPEN][next_index] - trade_type * 1.5 * self.atr[index],
						 stop_loss2 = self.df[OPEN][next_index] - trade_type * 1.5 * self.atr[index],
						 pelle_price = self.df[OPEN][next_index] + trade_type * self.atr[index],
						 take_profit = self.df[OPEN][next_index] + trade_type * self.atr[index],
						 spread = self.spread)

		self.report = pd.DataFrame(trade_list)

		print (self.report)

		if should_draw: self.draw_graph(should_show = True)
		if should_analyze: self.analyze_trades(verbose = True)
		if should_save: self.save_trade_history()

		return total_profits
		



if __name__ == '__main__':

	GBPUSD_data = Pair(GBPUSD)
	matrix_trader = MatrixTrader(GBPUSD_data, GBPUSD_data, timeframe = '1D')
	
	# dm = CoinToss()
	# features = pd.DataFrame(np.random.rand(len(GBPUSD_data.get_1D()), 5), index = GBPUSD_data.get_1D().index)
	# signals = pd.Series(dm.decide(features), features.index)


	# Trying to immitate VP
	from indicators_transformer.EMA_FT import EMA_FT
	from indicators_transformer.SqueezeBreak_FT import SqueezeBreak_FT
	from indicators_transformer.AroonHorn_FT import AroonHorn_FT
	from indicators_transformer.SMI_FT import SMI_FT

	from indicators.EMA import EMA
	from indicators.SqueezeBreak import SqueezeBreak
	from indicators.AroonHorn import AroonHorn
	from indicators.SMI import SMI

	df = GBPUSD_data.get_1D()

	baseline = EMA_FT().transform(df, EMA(14, CLOSE).calculate(df))
	volume = SqueezeBreak_FT().transform(df, SqueezeBreak(14, 14).calculate(df))
	ind1 = AroonHorn_FT().transform(df, AroonHorn(20).calculate(df))
	ind2 = SMI_FT().transform(df, SMI(14 , 3).calculate(df))

	signals = pd.concat([baseline, volume, ind1, ind2], axis = 1)
	signals_dic = {}
	for index, row in signals.iterrows():
		if row[0] == 1 and row[1] == 1 and row[2] == 1 and row[3] == 1:
			signals_dic[index] = 1
		elif row[0] == -1 and row[1] == 1 and row[2] == -1 and row[3] == -1:
			signals_dic[index] = -1
		else:
			signals_dic[index] = 0
	
	signals = pd.Series(signals_dic)
	print ("Features are ready")

	matrix_trader.simulate(signals, ind1)




