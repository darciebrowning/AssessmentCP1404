__author__ = 'Darcie'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import datetime
from currency import *
from trip import *
import time
import os.path
from kivy.uix.textinput import TextInput

home_amount = TextInput.multiline = False
foreign_amount = TextInput.multiline = False


class CurrencyApp(App):
    def __init__(self):
        super(CurrencyApp, self).__init__()
        self.trip_conversions = Details()

    def build(self):
        Window.size = (350, 700)
        self.title = 'Bills Budget Adventures Currency Calculator'
        self.root = Builder.load_file('gui.kv')
        self.set_trip_details()
        self.conversion_rates = {}
        self.button_pressed = self.button_pressed
        self.root.ids.foreign_amount.disabled = True
        self.root.ids.home_amount.disabled = True
        return self.root

    def change_state(self, country_names):
        self.root.ids.foreign_amount.text = ''
        foreign_country_code = get_details(country_names)
        print "changed to", country_names

    def set_trip_details(self):
        """Searches the config.txt file (first line) to get home country"""

        valid_details = get_all_details()
        input_file = open('config.txt', encoding='utf-8')
        line = input_file.readline().strip()
        self.home_country = line
        self.root.ids.home_country.text = line
        lines = input_file.readlines()
        trip_countries = []

        self.root.ids.status.text = "Trip details accepted"

        # trip countries
        for line in lines:
            parts = line.strip('\n').split(',')
            self.country_name = parts[0]
            self.start_date = parts[1]
            self.end_date = parts[2]
            # validate trip file
            if not os.path.exists('config.txt'):
                self.root.ids.status = "Config file not found"
            elif self.home_country not in valid_details.keys():
                self.root.ids.status.text = "Trip invalid:\n" + self.home_country
            elif self.country_name not in valid_details.keys():
                self.root.ids.status.text = "Trip invalid:\n" + self.country_name
            elif self.start_date > self.end_date:
                self.root.ids.status.text = "Trip invalid:\n"

            trip_countries.append(parts[0])
            try:
                self.trip_conversions.add(parts[0], parts[1], parts[2])
            except Error:
                self.root.ids.status.text = "Trip dates invalid\n" + self.start_date + "\n" + self.end_date
                self.root.ids.convert.disabled = True
                self.root.ids.country_selection.disabled = True

        if "Trip invalid:\n" in self.root.ids.status.text:
            self.root.ids.convert.disabled = True
            self.root.ids.country_selection.disabled = True

        # create no-value dictionary
        self.trip_locations_dict = dict.fromkeys(trip_countries)
        self.root.ids.country_selection.values = self.trip_locations_dict

        # set current country
        self.date = datetime.date.today().strftime("%Y/%m/%d")
        self.current_country = self.trip_conversions.current_country(self.date)
        self.root.ids.current_location.text = 'Current trip location is:\n' + self.current_country

        # set date
        date_today = datetime.date.today().strftime("%Y/%m/%d")
        self.root.ids.date_today.text = 'Today is:\n' + date_today

    def button_pressed(self):

        self.root.ids.foreign_amount.disabled = False
        self.root.ids.home_amount.disabled = False

        if not self.root.ids.country_selection.text:
            self.root.ids.country_selection.text = self.current_country

        home_country_code = get_details(self.home_country)[1]
        amount = 1

        for country in self.trip_locations_dict:
            details = get_details(country)[1]
            converted_value = convert(amount, home_country_code, details)
            self.trip_locations_dict[country] = (converted_value)

        update_time = (time.strftime("%H:%M:%S"))
        self.root.ids.status.text = str('Last updated at ') + update_time

    def convert_home_to_foreign(self):

        try:

            home_amount = float(self.root.ids.home_amount.text)
            foreign_country = self.root.ids.country_selection.text
            rate = self.trip_locations_dict[foreign_country]
            convert = home_amount * rate
            self.root.ids.foreign_amount.text = '{:,.2f}'.format(convert)

            home_country_details = get_details(self.home_country)
            foreign_country_details = get_details(self.root.ids.country_selection.text)

            try:
                self.root.ids.status.text = "From {} ({}) to {} ({})".format(home_country_details[1],
                                                                             home_country_details[2],
                                                                             foreign_country_details[1],
                                                                             foreign_country_details[2])
            except:
                # Mac encoding issues
                self.root.ids.status.text = "From {} to {} ".format(home_country_details[1], foreign_country_details[1])
        except ValueError:
            self.root.ids.status.text = "Invalid amount"

    def convert_foreign_to_home(self):

        try:
            home_amount = float(self.root.ids.foreign_amount.text)
            foreign_country = self.root.ids.country_selection.text
            rate = self.trip_locations_dict[foreign_country]
            convert = home_amount / rate
            self.root.ids.home_amount.text = '{:,.2f}'.format(convert)

            home_country_details = get_details(self.root.ids.country_selection.text)
            foreign_country_details = get_details(self.home_country)

            try:
                self.root.ids.status.text = "From {} ({}) to {} ({})".format(home_country_details[1],
                                                                             home_country_details[2],
                                                                             foreign_country_details[1],
                                                                             foreign_country_details[2])
            except:
                # Mac encoding issues
                self.root.ids.status.text = "From {} to {} ".format(home_country_details[1], foreign_country_details[1])
        except ValueError:
            self.root.ids.status.text = "Invalid amount"


CurrencyApp().run()
