__author__ = 'Darcie'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty
import datetime
import time
from currency import *
from trip import *
import os.path
from kivy.uix.textinput import TextInput

home_amount = TextInput.multiline=False
foreign_amount = TextInput.multiline=False

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
        """Displays the current date today"""
        date_today = datetime.date.today().strftime("%Y/%m/%d")
        self.root.ids.date_today.text = 'Today is:\n' + date_today

    def status_bar_update(self):
        """Updates the status bar of any errors loading the config file"""
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

    # def on_text(self, instance, value)
    #     textinput = TextInput
    #     textinput._bind_keyboard(on_text_validate=on_text)


    def button_pressed(self):

        try:
            country_name = str(self.root.ids.home_country.text).strip('\n')
            home_currency = str(get_details(country_name)).strip('\'').split('\'')[3]
            foreign_country = self.root.ids.country_selection.text
            foreign_currency = str(get_details(foreign_country)).strip('\'').split('\'')[3]
            conversion_rate = convert(1,home_currency,foreign_currency)

            update_time = (time.strftime("%H:%M:%S"))
            self.root.ids.status.text = str('Last updated at ') + update_time
            return conversion_rate

        except:
            current_country_default = self.root.ids.current_location.text [26:]
            self.root.ids.country_selection.text = current_country_default

            update_time = (time.strftime("%H:%M:%S"))
            self.root.ids.status.text = str('Last updated at ') + update_time

    def valid(self):
        try:
            value = float(self.root.ids.foreign_amount.text)
            return value

        except ValueError:
            print("This amount is not valid.")
            return 0


    def countries_available(self):
        """Sets countries available in the spinner"""
        config_file = open('config.txt', encoding='utf-8')
        config_file = config_file.readlines() [1:]
        countries = []
        for content in config_file:
            content = str(content).split(',')[0]
            countries.append(content)
        d = dict.fromkeys(countries)
        self.root.ids.country_selection.values = d


CurrencyApp().run()