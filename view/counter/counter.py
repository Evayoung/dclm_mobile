# this is the application counter screen home
from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker


class CounterScreenView(Screen):

    # program_output
    def program_type_dropdown(self):
        self.data = [
            [
                {
                    "viewclass": "OneLineListItem",
                    "text": "Global Crusade",
                    "on_release": lambda x="Example 1": self.update_type('Global Crusade')
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Minister's Conference",
                    "on_release": lambda x="Example 1": self.update_type("Minister's Conference")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Impact Academy",
                    "on_release": lambda x="Example 1": self.update_type("Impact Academy")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Sunday Worship",
                    "on_release": lambda x="Example 1": self.update_type("Sunday Worship")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Special Program",
                    "on_release": lambda x="Example 1": self.update_type("Special Program")
                }
            ],
            [
                {
                    "viewclass": "OneLineListItem",
                    "text": "Morning Message",
                    "on_release": lambda x="Example 1": self.update_type('Morning Message')
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Bible Teaching",
                    "on_release": lambda x="Example 1": self.update_type("Bible Teaching")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Bible Study",
                    "on_release": lambda x="Example 1": self.update_type("Bible Study")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Seminar",
                    "on_release": lambda x="Example 1": self.update_type("Seminar")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Authentic Christianity",
                    "on_release": lambda x="Example 1": self.update_type("Authentic Christianity")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Reality",
                    "on_release": lambda x="Example 1": self.update_type("Reality")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Breakthrough Series",
                    "on_release": lambda x="Example 1": self.update_type("Breakthrough Series")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Revival Session",
                    "on_release": lambda x="Example 1": self.update_type("Revival Session")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Special Program",
                    "on_release": lambda x="Example 1": self.update_type("Special Program")
                }
            ],
            [
                {
                    "viewclass": "OneLineListItem",
                    "text": "Sunday Worship",
                    "on_release": lambda x="Example 1": self.update_type('Sunday Worship')
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Monday Bible Study",
                    "on_release": lambda x="Example 1": self.update_type("Monday Bible Study")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Thursday Revival",
                    "on_release": lambda x="Example 1": self.update_type("Thursday Revival")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Leader's Meeting",
                    "on_release": lambda x="Example 1": self.update_type("Leader's Meeting")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Worker's Meeting",
                    "on_release": lambda x="Example 1": self.update_type("Worker's Meeting")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Combine Service",
                    "on_release": lambda x="Example 1": self.update_type("Combine Service")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Conference",
                    "on_release": lambda x="Example 1": self.update_type("Conference")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Worker's Retreat",
                    "on_release": lambda x="Example 1": self.update_type("Worker's Retreat")
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Special Program",
                    "on_release": lambda x="Example 1": self.update_type("Special Program")
                }
            ]
        ]
        self.program_type = ''
        prog_type = self.ids.counter_title.text

        if prog_type == 'Crusade':
            self.program_type = self.data[0]

        if prog_type == 'Retreat':
            self.program_type = self.data[1]

        if prog_type == 'Programs':
            self.program_type = self.data[2]

        self.program_type_drop = MDDropdownMenu(
            caller=self.ids.select_type,
            items=self.program_type,
            width_mult=3
        )
        self.program_type_drop.open()

    def update_type(self, data):
        if data == 'Special Program':
            self.ids.program_output.readonly = False
            self.ids.program_output.text = ''
        else:
            self.ids.program_output.readonly = True
            self.ids.program_output.text = data
        self.program_type_drop.dismiss()

    def show_program_level(self):  # drop down to select the user role
        self.program_level = [
            {
                "viewclass": "OneLineListItem",
                "text": "National",
                "on_release": lambda x="Example 1": self.update_level("National")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Zonal",
                "on_release": lambda x="Example 1": self.update_level("Zonal")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "State",
                "on_release": lambda x="Example 1": self.update_level("State")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Region",
                "on_release": lambda x="Example 1": self.update_level("Region")
            }
        ]

        self.program_level_drop = MDDropdownMenu(
            caller=self.ids.level,
            items=self.program_level,
            width_mult=3
        )
        self.program_level_drop.open()

    def update_level(self, data):
        self.ids.level.text = data
        self.program_level_drop.dismiss()

    def show_program_type(self):
        self.program_list = []


    def show_date_picker(self):
        self.program_date = [
            {
                "viewclass": "OneLineListItem",
                "text": "Current Date",
                "on_release": lambda x="Example 1": self.current_date()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Custom Date",
                "on_release": lambda x="Example 1": self.custom_date()
            }
        ]

        self.program_date_drop = MDDropdownMenu(
            caller=self.ids.date_picker,
            items=self.program_date,
            width_mult=3
        )
        self.program_date_drop.open()

    # def current_date(self, *args):
    #     self.ids['set_date'].readonly = True
    #     today2 = datetime.today()
    #     dat = today2.strftime("%Y-%d-%b")
    #     self.ids['set_date'].text = dat
    #     self.program_date_drop.dismiss()

    def current_date(self, *args):
        self.ids['set_date'].readonly = True
        today = datetime.today()
        dat = today.strftime("%Y-%m-%d")
        self.ids['set_date'].text = dat
        self.program_date_drop.dismiss()

    def custom_date(self, *args):
        self.ids.set_date.readonly = False
        # self.ids['set_date'].readyonly = False
        self.ids.set_date.text = ''
        self.program_date_drop.dismiss()

