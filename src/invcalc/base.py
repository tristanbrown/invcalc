"""Module with the base models."""
from copy import deepcopy

from invcalc.time import Calendar

class Portfolio():
    """"""

    def __init__(self, cash=0):
        self.cash = cash
        self.assets = {}
        self.distributions = {}
        self.calendar = Calendar()

    def add(self, asset, name):
        self.assets[name] = asset

    def invest(self, percent: float, name):
        self.distributions[name] = percent

    def distribute(self, amount):
        remaining = amount
        for name, percent in self.distributions.items():
            portion = amount * percent
            self.assets[name].deposit(portion)
            # print(f"Deposited ${portion} in {name}.")
            # print(f"{name} now worth ${self.assets[name].value}.")
            remaining -= portion
        self.cash += remaining
        # print(f"Deposited ${remaining} in cash.")

    def mature(self, years):
        """"""
        events = self.calendar.advance(years * 12)
        for event in events:
            profit = 0
            for name, asset in self.assets.items():
                if asset.period in event:
                    asset.capitalize()
                    # print(f"Received ${asset.profit} from {name}.")
                    profit += asset.withdraw()
            self.distribute(profit)
        return self.value

    def forecast(self, years):
        """"""
        temporary = deepcopy(self)
        result = temporary.mature(years)
        return result

    @property
    def value(self):
        returns = sum([asset.value for asset in self.assets.values()])
        return self.cash + returns

class Asset():
    """"""

    def __init__(self, funding=0):
        self.equity = funding
        self.profit = 0
        self.period = None

    def withdraw(self):
        curr_profit = self.profit
        self.profit = 0
        return curr_profit

    def deposit(self, funding):
        self.equity += funding

    @property
    def value(self):
        return self.equity + self.profit

class Income(Asset):
    """"""

    def __init__(self, salary: float):
        super().__init__()
        self.period = 'monthly'
        self.salary = salary

    def capitalize(self):
        self.profit += self.salary / 12

class Dividend(Asset):
    """"""

    def __init__(self, funding, div_yield: float):
        super().__init__(funding)
        self.period = 'quarterly'
        self.div_yield = div_yield

    def capitalize(self):
        self.profit += self.equity * self.div_yield / 4

class Investment(Asset):
    """"""

    def __init__(self, funding, inv_yield: float):
        super().__init__(funding)
        self.period = 'monthly'
        self.inv_yield = inv_yield

    def capitalize(self):
        self.equity += self.equity * self.inv_yield / 12
