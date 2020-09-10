# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

import pprint as pp

class Trade(object):
	# This class will be used in the traders to record the trades's information

	def __init__(self, main_pair_name, aux_pair_name):
		super(Trade, self).__init__()
		assert isinstance(main_pair_name, str)
		assert isinstance(aux_pair_name, str)

		self.main_pair_name = main_pair_name
		self.aux_pair_name = aux_pair_name

	def set_opening_info(self, opening_time , main_open_price, aux_open_price,
                             trade_type, balance, ATR, risk, stop_loss1,
                             stop_loss2,pelle_price,take_profit, spread):
		self.opening_time = opening_time
		self.main_opening_price = main_open_price + trade_type * spread
		self.aux_opening_price = aux_open_price
		self.risk = risk
		self.balance = balance
		self.trade_type = trade_type
		self.stop_loss1 = stop_loss1
		self.stop_loss2 = stop_loss2
		self.pelle_price = pelle_price
		self.take_profit = take_profit
		# Set the pip  value
		if self.main_pair_name[-3:] == 'USD':
			self.pip_value = 10
		elif self.aux_pair_name[-3:] == 'USD':
			self.pip_value = 10 / aux_open_price
		elif self.aux_pair_name[:3] == 'USD':
			self.pip_value = 10 * aux_open_price

		self.trade_1_open = True
		self.trade_2_open = True

		'''
		Trade size and Risk:

		Example: We have an account with 3000 USD balance, and the ATR at the openning time is 0.0080
		We want to trade EUR/USD, GBP/CAD, and USD/CAD
		At the openning EUR/USD = 1.1, GBP/CAD = 2.1, USD/CAD = 2.2

		stop_loss = 1.5 ATR (when you want to open the trade) * 10,000 = 120
		risk = 2% (constant) * balance = 60 USD
		pip_value = risk / stop_loss = 60 USD/120 = 0.5 USD/pip

		General Function:
		trade_size = (pip_value * exchange_rate to the currency pair denomenator) * 10,000

		for EUR/USD:
		trade_size = (0.5 USD/pip * 1 USD/USD ) * 10,000

		for GBP/CAD:
		trade_size = (0.5 USD/pip *  (1CAD/2.2USD) ) * 10,000

		for USD/CAD:
		trade_size = (0.5 USD/pip * (1CAD/2.2USD)) * 10,000

		Obviously for any pair with JPY all the 10,000 will change to 100
		'''
		modifier = 10000 if not 'JPY' in self.main_pair_name else 100
		pip_value = risk * balance / (1.5 * ATR * modifier)

		if self.main_pair_name[-3:] == 'USD':
			self.trade_size = pip_value * modifier
		elif self.aux_pair_name[-3:] == 'USD':
			self.trade_size = pip_value * modifier / aux_opening_price
		elif self.aux_pair_name[-3:] != 'USD':
			self.trade_size = pip_value * modifier * aux_opening_price
		else:
			raise ValueError ("Something is wrong with the trade size calculation")

		self.closing_time_1 = 'not_assigned'
		self.main_closing_price_1 = 'not_assigned'
		self.aux_closing_price_1 = 'not_assigned'
		self.closing_reason_1 = 'not_assigned'
		self.closing_time_2 = 'not_assigned'
		self.main_closing_price_2 = 'not_assigned'
		self.aux_closing_price_2 = 'not_assigned'
		self.closing_reason_2 = 'not_assigned'
		self.closing_balance = 'not_assigned'
		self.profit = 'not_assigned'

	def set_closing_info_1(self, closing_time, main_closing_price,
                               aux_closing_price, closing_reason):
		self.closing_time_1 = closing_time
		self.main_closing_price_1 = main_closing_price
		self.aux_closing_price_1 = aux_closing_price
		self.closing_reason_1 = closing_reason
		self.trade_1_open = False

	def set_closing_info_2(self, closing_time, main_closing_price, aux_closing_price, closing_reason):
		self.closing_time_2 = closing_time
		self.main_closing_price_2 = main_closing_price
		self.aux_closing_price_2 = aux_closing_price
		self.closing_reason_2 = closing_reason
		self.trade_2_open = False

	def evaluate(self):
                
		self.profit = self.trade_type*self.trade_size/2  * ((self.main_closing_price_1-self.main_opening_price)+ \
																			(self.main_closing_price_2-self.main_opening_price))
		self.closing_balance = self.balance + self.profit

		return self.profit, self.closing_balance

	def get_report(self):
		dic = {
		'type': self.trade_type,
		'opening_time': self.opening_time,
		'main_opening_price': self.main_opening_price,
		'aux_opening_price': self.aux_opening_price,
		'closing_time_1': self.closing_time_1,
		'main_closing_price_1': self.main_closing_price_1,
		'aux_closing_price_1': self.aux_closing_price_1,
		'reason_1': self.closing_reason_1,
		'closing_time_2': self.closing_time_2,
		'main_closing_price_2': self.main_closing_price_2,
		'aux_closing_price_2': self.aux_closing_price_2,
		'reason_2': self.closing_reason_2,
		'balance': self.balance,
		'closing_balance': self.closing_balance,
		'risk': self.risk,
		'trade_size': self.trade_size,
		'profit': self.profit
		}
		return dic

if __name__ == '__main__':
	1
