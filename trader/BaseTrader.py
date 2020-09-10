# Adding parent directory to the PYTHONPATH
import sys, os
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from utils.AwesomeLogger import Logger


import logging
from datetime import datetime
import matplotlib.pyplot as plt
import itertools
import numpy as np
import pprint


class BaseTrader(object):
	# Base class for creating trader agents
	# This is a very rough idea, it must be completed in the future
	def __init__(self, pair_name= 'UNSPECIFIED'):
		super(BaseTrader, self).__init__()

		# This is the name of the report folder, all reports including graphs, analysis, etc. will be saved under this name
		self.name = pair_name + "-" + str(datetime.now())[:-10].replace(":", "-")

		# Creating the report directory
		self.report_dir = f"../test_reports/Report-{self.name}"
		if not os.path.exists(self.report_dir):
			os.makedirs(self.report_dir)

		# Crearing logger
		logging_address = os.path.join(self.report_dir, 'Report.log')
		self.log = Logger(logger_name = 'AwesomeLogger', address = logging_address , mode='a',
							level = logging.DEBUG,
							console_level = logging.WARNING,
							file_level = logging.DEBUG)

	def draw_graph(self, should_show = False):
		# This method must draw a graph based on the report of the trades
		balances = self.report['closing_balance']

		plt.plot(self.report.index, balances)
		plt.xlabel("Closing time of trades")
		plt.ylabel("balances")
		plt.title(self.name)
		plt.grid(True)
		plt.savefig(os.path.join(self.report_dir, 'Balance.png'))
		if should_show: plt.show()
		plt.close()

	def analyze_trades(self, verbose = False):
		# This method should analyze the trades and save them as a report
		# This report should use logging
		# Total trades opened and closed in the simulation

		# Finding the short and long positions
		df = self.report.copy()

		long_positions = len(df[df['type'] > 0])
		short_positions = len(df[df['type'] < 0])

		win_trades = self.report[self.report['profit'] > 0]
		loss_trades = self.report[self.report['profit'] < 0]

		total_trades = len(self.report)
		n_profit_trades = len(df[df['profit'] > 0])
		n_loss_trades = len(df[df['profit'] < 0])

		total_net_profit = df['profit'].sum()
		gross_profit = df['profit'][df['profit'] > 0].sum()
		gross_loss = df['profit'][df['profit'] < 0].sum()

		expected_payoff = total_net_profit/total_trades
		profit_factor = abs(gross_profit/gross_loss)

		largest_profit_trade = win_trades['profit'].max()
		largest_loss_trade = loss_trades['profit'].min()
		average_profit_trade = win_trades['profit'].mean()
		average_loss_trade = loss_trades['profit'].mean()

		cons_wins, cons_loss = 0, 0
		for k, g in itertools.groupby(df['profit'].astype('float64'), key=lambda n: n>0):

			temp_len = len([val for val in g])
			if k and temp_len > cons_wins:
				cons_wins = temp_len
			elif not k and temp_len > cons_loss:
				cons_loss = temp_len

		# Finding the maximum drawdown
		maximums = np.maximum.accumulate(df['profit'])
		maximum_drawdown = np.max(1 - df['profit']/maximums)

		analysis_report = {'total_trades':total_trades,
							'n_profit_trades': n_profit_trades,
							'n_loss_trades': n_loss_trades,
							'total_net_profit': round(total_net_profit, 3),
							'gross_profit': round(gross_profit, 3),
							'gross_loss': round(gross_loss, 3),
							'expected_payoff': round(expected_payoff, 3),
							'profit_factor': round(profit_factor, 3),
							'largest_profit_trade': round(largest_profit_trade, 3),
							'largest_loss_trade': round(largest_loss_trade, 3),
							'average_profit_trade': round(average_profit_trade, 3),
							'average_loss_trade': round(average_loss_trade, 3),
							'cons_wins': cons_wins,
							'cons_loss': cons_loss}

		self.log.info(pprint.pformat(analysis_report))

		if verbose: pprint.pprint(analysis_report)

		return analysis_report


	def save_trade_history(self):
		# This method saves the report created by the trader in a csv file
		# The file should be similar to the MT4 trade history
		self.report.to_csv(os.path.join(self.report_dir, 'Trades_History.csv'))


if __name__ == '__main__':

	# For testing the methods
	import pandas as pd
	df = pd.read_csv('TestForBaseTrader.csv', index_col =0)

	def date_parser_1(date_as_str):
		# For the case index: 5/12/1993 0:00
		# There might be other cases so I named it date_parser_1
		return datetime.strptime(date_as_str, "%m/%d/%Y %H:%M")

	df['opening_time'].apply(date_parser_1)
	df['closing_time'].apply(date_parser_1)

	myBaseTrader = BaseTrader()
	myBaseTrader.report = df

	myBaseTrader.draw_graph()
	myBaseTrader.save_trade_history()
	myBaseTrader.analyze_trades()







