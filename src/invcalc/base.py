"""Module with the base models."""

class Portfolio():
    """"""

    def __init__(self, cash=0):
        self.cash = cash
        self.assets = {}

    def forecast(self, years):
        """"""
        for asset in self.assets.values():
            asset.mature(years)
            self.cash += asset.withdraw()
        return self.value

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
        self.profit += (self.equity * self.div_yield)**years

class Investment(Asset):
    """"""

    def __init__(self, funding, inv_yield: float):
        super().__init__(funding)
        self.inv_yield = inv_yield

    def mature(self, years):
        self.equity += (self.equity * self.inv_yield)**years
