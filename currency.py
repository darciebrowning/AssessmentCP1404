__author__ = 'Darcie'
import web_utility
from trip import *

def convert(amount, home_currency_code, location_currency_code):
    """This function generates the URL string for the contries the user wishes to convert and returns the unformatted version of the conversion"""

    url_string = ("https://www.google.com/finance/converter?a= {} &from= {}  &to= {}".format(amount, home_currency_code, location_currency_code))
    result = web_utility.load_page(url_string)
    result = (result[result.index('result'):])
    #TODO put in exception to equal - 1

    split_result = result.split(">") [2]
    amount = split_result.split(" ") [0]
    return amount


def get_details(country_name):
    """This function takes the country name, searches the currency_details text file to find a match and returns the
    corresponding currency details as a tuple, otherwise if a match isn't found it returns an empty tuple"""

    # open the currency_details file for use
    file = open('currency_details.txt', mode='r')
    lines = file.readlines()

    # Loop through the lines file until the matching country name is found and return line.
    for details in lines:
        if country_name in details:
            details = tuple(list(details.strip('\n').split(',')))
            return details

    #close the file
    file.close()
    return ()


# Get details for the users home country
country_name = input("Enter your Country name: ")
home_currency_code = get_details(country_name) [1]


# Get details for the country the visitor is converting to
country_name = input("Enter the country you would like to convert to: ")
location_currency_code = get_details(country_name) [1]


# Get the amount the user would like to convert
amount = input("Enter the value you would like to convert: ")

# pass values to the convert function and run it
convert(amount, home_currency_code, location_currency_code)

# Pass amount to format currency to be formatted.
Country.format_currency(amount)