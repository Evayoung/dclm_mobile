# this class is the application home class
from kivy.uix.screenmanager import Screen
from datetime import datetime
from kivymd.uix.menu import MDDropdownMenu


class HomeScreenView(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        current_date = datetime.now()

        # Format the date as "Tuesday 24 January, 2024"
        formatted_date = current_date.strftime("%A %d %B, %Y")

        self.ids["today_date"].text = formatted_date

        if "Sunday" in formatted_date:
            self.ids['disp_pics'].source = 'images/sunday.png'
        elif "Monday" in formatted_date:
            self.ids['disp_pics'].source = 'images/monday.png'
        elif "Tuesday" in formatted_date:
            self.ids['disp_pics'].source = 'images/tuesday.png'
        elif "Thursday" in formatted_date:
            self.ids['disp_pics'].source = 'images/thursday.png'
        elif "Saturday" in formatted_date:
            self.ids['disp_pics'].source = 'images/saturday.png'
        else:
            self.ids['disp_pics'].source = 'images/regular.png'
