"""Module with the base models."""
from copy import deepcopy

class Portfolio():
    """"""

    def __init__(self, cash=0):
        self.cash = cash
        self.assets = {}
        self.distributions = {}

    def add(self, asset, name):
        self.assets[name] = asset

    def invest(self, percent: float, name):
        self.distributions[name] = percent

    def distribute(self, amount):
        remaining = amount
        for name, percent in self.distributions.items():
            portion = amount * percent
            self.assets[name].deposit(portion)
            print(f"Deposited ${portion} in {name}.")
            print(f"{name} now worth ${self.assets[name].value}.")
            remaining -= portion
        self.cash += remaining
        print(f"Deposited ${remaining} in savings.")

    def mature(self, years):
        """"""
        profit = 0
        for name, asset in self.assets.items():
            asset.mature(years)
            print(f"Received ${asset.profit} from {name}.")
            profit += asset.withdraw()
        self.distribute(profit)
        return self.value

    def forecast(self, years, comp='monthly'):
        """"""
        original = deepcopy(self)
        comp_def = {
            'daily': 365,
            'weekly': 52,
            'biweekly': 26,
            'monthly': 12,
            'quarterly': 4,
            'yearly': 1,
        }
        period = comp_def[comp]
        interval = 1/period
        for _ in range(period * years):
            result = self.mature(interval)
        self.cash = original.cash
        self.assets = original.assets
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
        self.salary = salary

    def mature(self, years):
        self.profit = self.salary * years

class Dividend(Asset):
    """"""

    def __init__(self, funding, div_yield: float):
        super().__init__(funding)
        self.div_yield = div_yield

    def mature(self, years):
        self.profit += self.equity * (1 + self.div_yield)**years

class Investment(Asset):
    """"""

    def __init__(self, funding, inv_yield: float):
        super().__init__(funding)
        self.inv_yield = inv_yield

    def mature(self, years):
        self.equity += (self.equity * self.inv_yield)**years
