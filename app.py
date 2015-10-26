__author__ = 'Darcie'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty
import datetime
from currency import *
from trip import *


class CurrencyApp(App):
    current_country = StringProperty()
    country_names = ListProperty()

    # def __init__(self, trip_details):
    #     super(CurrencyApp, self).__init__()
    #     self.trip_details = trip_details

    def build(self):
        Window.size = (350, 700)
        self.title = 'Bills Budget Adventures Currency Calculator'
        self.root = Builder.load_file('gui.kv')
        self.country_names = sorted(results.keys())
        self.current_country = self.country_names[0]
        self.current_location()
        self.home_country()
        self.current_date()
        return self.root

    def change_state(self, country_names):
        self.root.ids.foreign_amount.text = 'converted number here'
        foreign_country_code = get_details(country_names)
        print "changed to", country_names

    def home_country(self):
        input_file = open('config.txt', encoding='utf-8')
        line = input_file.readline()
        self.root.ids.home_country.text = line

    def current_location(self):
        date_string = datetime.date.today().strftime("%Y/%m/%d")
        location_file = open('config.txt')
        location = location_file.readline()[1:]
        details = Details()

        for line in location_file:
            line = line.strip('\n').split(',')
            country_name, start_date, end_date = line[0], line[1], line[2]
            details.add(country_name, start_date, end_date)
        location_file.close()

        current_country = details.current_country(date_string)
        self.root.ids.current_location.text = 'Current trip location is:\n' + current_country

    def current_date(self):
        date_today = datetime.date.today().strftime("%Y/%m/%d")
        self.root.ids.date_today.text = 'Today is:\n' + date_today

    def button_pressed(self):
        # country_name = self.root.ids.home_country.text
        # amount = self.valid()
        # home_currency = (get_details(self.root.ids.home_country.text))
        #
        # #location_currency = str(get_details(self.root.ids.country_selection.text))
        # conversion_result = convert(amount,home_currency,location_currency)
        # self.root.ids.home_amount.text = str(conversion_result)

    def valid(self):
        try:
            value = float(self.root.ids.foreign_amount.text)
            return value

        except ValueError:
            print("This amount is not valid.")
            return 0
CurrencyApp().run()