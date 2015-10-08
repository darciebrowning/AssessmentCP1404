__author__ = 'Darcie'
import currency
import datetime


class Error(Exception):
    pass


class Country:

    def __init__(self, name, currency_code, currency_symbol):
        self.name = name
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol

    def format_currency(self, amount):
        amount = '{1:.2f}'.format(amount)
        str(amount)
        return amount

    def __str__(self, details):
        pass

class Details:

    def __init__(self, locations):
        """Create a list for the locations visited to be stored in."""
        self.locations = []

    def add(self, country_name, start_date, end_date):

        start_date = "{}/{}/{}". format(start_date[0], start_date[1], start_date[2])
        end_date = "{}/{}/{}".format(end_date[0], end_date[1], end_date[2])

        self.locations.append((country_name, start_date, end_date))

    def current_country(self, date_string):

        for location in self.locations:
            if date_string >= location[1] and date_string <= location[2]:
                return location[0]

    def is_empty(self):

        if self.locations[0] == []:
            return False
        else:
            return True



date_string = datetime.date.today().strftime("%Y/%m/%d")
