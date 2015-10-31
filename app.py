__author__ = 'Darcie'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty
import datetime
from currency import *
from trip import *
import os.path


class CurrencyApp(App):
    current_country = StringProperty()
    country_names = ListProperty()

    def __init__(self):
        super(CurrencyApp, self).__init__()
        self.trip_details = Details()

    def build(self):
        Window.size = (350, 700)
        self.title = 'Bills Budget Adventures Currency Calculator'
        self.root = Builder.load_file('gui.kv')
        self.status_bar_update()
        self.countries_available()
        self.current_location()
        self.home_country()
        self.current_date()
        return self.root

    def change_state(self, country_names):
        self.root.ids.foreign_amount.text = ''
        foreign_country_code = get_details(country_names)
        print "changed to", country_names

    def home_country(self):
        """Searches the config.txt file (first line) to get home country"""
        input_file = open('config.txt', encoding='utf-8')
        line = input_file.readline()
        self.root.ids.home_country.text = line

    def current_location(self):
        """Gets the current trip location based on the current date"""
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

    def currency_convert_pressed(self):
        """
        If text entered into home country feild
        run convert function and output to foreign country field

        else if text changed in foreign country feild
        run convert function and output to home country field
        """

    def status_bar_update(self):
        try:
            os.path.exists('config.txt')
            config_file = open ('config.txt', encoding='utf-8')
            config_file = config_file.readlines()[1:]
            lines = str(config_file)

            count = lines.count('/')
            count2 = lines.count(',')

            if count >= 4 and count2 >= 2:
                self.root.ids.status.text = "Trip details accepted"

            else:
                self.root.ids.status.text = "Trip details not valid"
        except:
            if not os.path.exists('config.txt'):
                self.root.ids.status.text = "Trip file not found"


    # def button_pressed(self):
    #     country_name = str(self.root.ids.home_country.text).strip('\n')
    #     amount = self.valid()
    #     home_currency = str(get_details(country_name)).strip('\'').split('\'')[3]
    #
    #     print(home_currency)
    #
    #     try:
    #         country_name = str(self.root.ids.country_selection.text)
    #         location_currency = (get_details(country_name))
    #         location_currency = str(location_currency).strip('\'').split('\'')[3]
    #         converted_value = convert(amount, home_currency, location_currency)
    #         self.root.ids.home_amount.text = str(converted_value)
    #
    #     except ValueError:
    #         print("This amount is not valid.")

    def valid(self):
        try:
            value = float(self.root.ids.foreign_amount.text)
            return value

        except ValueError:
            print("This amount is not valid.")
            return 0


    def countries_available(self):
        config_file = open('config.txt', encoding='utf-8')
        config_file = config_file.readlines() [1:]
        countries = []
        for content in config_file:
            content = str(content).split(',')[0]
            countries.append(content)
        d = dict.fromkeys(countries)
        self.root.ids.country_selection.values = d


CurrencyApp().run()