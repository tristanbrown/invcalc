"""Time management for the fiscal year."""
import pandas as pd

class Calendar():
    """Reports the time intervals of the fiscal year."""
    periods = {
            # 'daily': 365.25,
            # 'weekly': 52.179,
            # 'biweekly': 52.179 / 2,
            'monthly': 12,
            'quarterly': 4,
            'yearly': 1,
        }

    def __init__(self):
        first_year = []
        sequences = {name: self.period_to_sequence(period) for name, period in self.periods.items()}
        index = sequences['monthly'].copy()
        for month in index:
            events = set()
            for name, intervals in sequences.items():
                if month >= intervals[0]:
                    events.add(name)
                    intervals.pop(0)
            first_year.append(events)
        self.first_year = pd.Series(first_year, index=index)
        self.first_year.index = self.first_year.index.astype('int64')
        self.now = 0

    @staticmethod
    def period_to_sequence(period):
        return [n / period * 12 for n in range(1, 1 + int(period))]

    def advance(self, months):
        """Move the calendar forward a given number of months.
        Returns all intervening events
        """
        extra_years = int((self.now + months) // 12 - self.year)
        all_years = self.full_year.copy()
        for i in range(extra_years):
            next_index = self.full_year.index + (i + 1) * 12
            next_year = pd.Series(list(self.full_year), index=next_index)
            all_years = all_years.append(next_year)
        full_interval = all_years.loc[self.now + 1:self.now + months]
        self.now += months
        return full_interval
    
    @property
    def year(self):
        return self.now // 12

    @property
    def full_year(self):
        curr_index = self.first_year.index + self.year * 12
        return pd.Series(list(self.first_year), index=curr_index)
