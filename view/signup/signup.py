# this is the signup screen where you create a new account on the application
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class SignupScreenView(Screen):
    def select_work_area(self):
        self.data = [
            {
                "viewclass": "OneLineListItem",
                "text": "Admin",
                "on_release": lambda x="Example 1": self.update_work_area("Admin")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Usher",
                "on_release": lambda x="Example 1": self.update_work_area("Usher")
            },
        ]

        self.work_area_menu = MDDropdownMenu(
            caller=self.ids.work_area,
            items=self.data,
            width_mult=3
        )
        self.work_area_menu.open()

    def update_work_area(self, data):
        self.ids.user_Work.text = data
        self.work_area_menu.dismiss()
