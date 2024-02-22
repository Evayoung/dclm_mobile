# this is the screen where invitee and convert details will be recorded
from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class RecordScreenView(Screen):
    def __init__(self, **kwargs):
        super(RecordScreenView, self).__init__(**kwargs)

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

    def current_date(self, *args):
        self.ids['date'].readonly = True
        # today2 = datetime.today()
        # dat = today2.strftime("%b-%d-%Y")
        today2 = datetime.today()
        dat = today2.strftime("%Y-%m-%d")
        self.ids['date'].text = dat
        self.program_date_drop.dismiss()

    def custom_date(self, *args):
        self.ids.date.readonly = False
        # self.ids['date'].readyonly = False
        self.ids.date.text = ''
        self.program_date_drop.dismiss()

    def select_gender(self):
        self.gender_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Male",
                "on_release": lambda x="Example 1": self.update_gender("Male")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Female",
                "on_release": lambda x="Example 1": self.update_gender("Female")
            }
        ]

        self.gender_drop = MDDropdownMenu(
            caller=self.ids.gender_group,
            items=self.gender_list,
            size_hint_max_y=.09,
            width_mult=3
        )
        self.gender_drop.open()

    def update_gender(self, data):
        self.ids.gender.text = data
        self.gender_drop.dismiss()

    def select_marital_status(self):
        self.status_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Single",
                "on_release": lambda x="Example 1": self.update_marital_status("Single")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Married",
                "on_release": lambda x="Example 1": self.update_marital_status("Married")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Divorce",
                "on_release": lambda x="Example 1": self.update_marital_status("Divorce")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Widow",
                "on_release": lambda x="Example 1": self.update_marital_status("Widow")
            }
        ]

        self.marital_drop = MDDropdownMenu(
            caller=self.ids.marital_status,
            items=self.status_list,
            size_hint_max_y=.09,
            width_mult=3
        )
        self.marital_drop.open()

    def update_marital_status(self, data):
        self.ids.marital.text = data
        self.marital_drop.dismiss()

    def select_social_group(self):
        self.group_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Adult",
                "on_release": lambda x="Example 1": self.update_group("Adulte")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Youth",
                "on_release": lambda x="Example 1": self.update_group("Youth")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Children",
                "on_release": lambda x="Example 1": self.update_group("Children")
            }
        ]

        self.group_drop = MDDropdownMenu(
            caller=self.ids.social_group,
            items=self.group_list,
            size_hint_max_y=.09,
            width_mult=3
        )
        self.group_drop.open()

    def update_group(self, data):
        self.ids.social.text = data
        self.group_drop.dismiss()

    def show_convert_type(self):
        self.convert_data = [
            {
                "viewclass": "OneLineListItem",
                "text": "Salvation",
                "on_release": lambda x="Example 1": self.update_convert_type("Salvation")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Restitution",
                "on_release": lambda x="Example 1": self.update_convert_type("Restitution")
            }
        ]

        self.convert_type_drop = MDDropdownMenu(
            caller=self.ids.c_type,
            items=self.convert_data,
            width_mult=3
        )
        self.convert_type_drop.open()

    def update_convert_type(self, data):
        self.ids.c_type.text = data
        self.convert_type_drop.dismiss()

    def reset_form(self):
        self.ids.f_name.text = ""
        self.ids.gender.text = ""
        self.ids.address.text = ""
        self.ids.marital.text = ""
        self.ids.social.text = ""
        self.ids.job.text = ""
        self.ids.j_address.text = ""
        self.ids.level.text = ""
        self.ids.inviter.text = ""
        self.ids.date.text = ""
        self.ids.c_type.text = "Type"
        if self.ids.convert_click.active:
            self.ids.convert_click.active = False

        if self.ids.invitee_click.active:
            self.ids.invitee_click.active = False
