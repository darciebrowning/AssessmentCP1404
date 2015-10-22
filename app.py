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

    #def __init__(self, trip):
        #self.trip = trip

    def build(self):
        Window.size = (350, 700)
        self.title = 'Bills Budget Adventures Currency Calculator'
        self.root = Builder.load_file('gui.kv')
        self.country_names = sorted(results.keys())
        self.current_country = self.country_names[0]
        #self.current_country()
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

    # def current_location(self):
    #     date_string = (datetime.date.today().strftime("%Y/%m/%d"))
    #     location = trip.Details.current_country(date_string)
    #     self.root.ids.current_location.text = 'Current Location:\n' + location

    def current_date(self):
        date_today = datetime.date.today().strftime("%Y/%m/%d")
        self.root.ids.date_today.text = 'Today is:\n' + date_today

    def button_pressed(self):
        pass

CurrencyApp().run()