# this is the login in class screen of the application

from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class LoginScreenView(Screen):
    def select_admin_type(self):
        self.data = [
            {
                "viewclass": "OneLineListItem",
                "text": "Admin",
                "on_release": lambda x="Example 1": self.update_admin_type("Admin")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Usher",
                "on_release": lambda x="Example 1": self.update_admin_type("Usher")
            },
        ]

        self.adminn_type = MDDropdownMenu(
            caller=self.ids.admin_type,
            items=self.data,
            width_mult=3
        )
        self.adminn_type.open()

    def update_admin_type(self, data):
        self.ids.user_type.text = data
        self.adminn_type.dismiss()
