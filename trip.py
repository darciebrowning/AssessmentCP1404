__author__ = 'Darcie'
"""
Takes details about a users trip and records them in a list, contains a number of formatting functions.

Trip. Created by Darcie Browning, October 2015
"""

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
        """Appends the appropriate currency symbol to the dollar amount"""
        amount = '{1:.2f}'.format(amount)
        str(amount)
        return amount

    def __str__(self, details):
        """Returns a string of the tuple country details passed in"""
        string_details = str(details)
        string_details = string_details.split("'")
        details = string_details[1] + " " + string_details[3] + " " + string_details [5]
        return details


class Details:

    def __init__(self, locations):
        """Create a list for the locations visited to be stored in."""
        self.locations = []

    def add(self, country_name, start_date, end_date):
        """Takes the location, the start date and the end date and appends to the locations list"""
        start_date = "{%Y}/{%m}/{%d}". format(start_date[0], start_date[1], start_date[2])
        end_date = "{%Y}/{%m}/{%d}".format(end_date[0], end_date[1], end_date[2])

        self.locations.append((country_name, start_date, end_date))

    def current_country(self, date_string):
        """Checks if the current date is between a countries start and end dates"""
        try:
            for location in self.locations:
                if location[1] <= date_string <= location[2]:
                    return location[0]

        except ValueError:
            return

    def is_empty(self):
        """Checks if there is locations in the list"""
        if not self.locations[0]:
            return False
        else:
            return True


#details = ('Germany', 'EUR', '€')
#date_string = datetime.date.today().strftime("%Y/%m/%d")
