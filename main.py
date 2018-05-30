import pandas as pd
import math


class Anuity(object):

	# def __init__(self, amount=10000.0, interest_rate=0.07, periods=26, date='10/10/2010'):
	# 	self.amount = amount
	# 	self.interest_rate = interest_rate
	# 	self.monthy_rate = interest_rate / 12.0
	# 	self.periods = periods
	# 	self.date = date

	def __init__(self):
		self.amount = None
		self.interest_rate = None
		self.monthy_rate = None
		self.periods = None
		self.date = None

	def get_info(self):
		while True:
			try:
				self.amount = float(input("Loan amount: "))
				self.interest_rate = float(input("Annual interest rate: "))
				self.periods = int(input("Count of payments: "))
				self.date = input("Date (DD/MM/YYYY): ")
				self.monthy_rate = self.interest_rate / 12.0 / 100
				break
			except:
				pass

	def get_full_amount(self):
		return self.amount * math.pow(1.0 + (self.monthy_rate, self.periods))

	def get_total_payment(self, remaining):
		return (self.monthy_rate * remaining) / (1 - math.pow(1 + self.monthy_rate, -self.periods))

	def calculate(self):
		self.get_info()

		dates = pd.date_range(start=self.date,
			 				  periods=self.periods,
			 				  freq=pd.DateOffset(months=1))

		total = self.get_total_payment(self.amount)
		interest = self.amount * self.monthy_rate
		principal = total - interest

		initial = {
			'Payment #': pd.Series(range(1, self.periods + 1)),
			'Payment date': dates,
			'Remaining amount': self.amount,
			'Principal payment': principal,
			'Interest payment': interest,
			'Total payment': total,
			'Interest rate': self.interest_rate,
		}

		df = pd.DataFrame(data=initial)

		for index, row in df[1:].iterrows():
			df.loc[index, 'Remaining amount'] = df.loc[index - 1, 'Remaining amount'] - df.loc[index - 1, 'Principal payment']
			df.loc[index, 'Interest payment'] = df.loc[index, 'Remaining amount'] * self.monthy_rate
			df.loc[index, 'Principal payment'] = df.loc[index, 'Total payment'] - df.loc[index, 'Interest payment']

		df = df[['Payment #', 'Payment date', 'Remaining amount', 'Principal payment', 'Interest payment', 'Total payment', 'Interest rate']]
		df = df.round(2)

		print(df)
		self.store(df)
		
	def store(self, df):
		df.to_csv('ataskaita.csv', index=False)


if __name__ == '__main__':
	Anuity().calculate()