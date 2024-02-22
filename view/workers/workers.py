from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class WorkersScreenView(Screen):
    def show_admin_levels(self):
        self.admin_levels = [
            {
                "viewclass": "OneLineListItem",
                "text": "Usher",
                "on_release": lambda x="Example 1": self.pass_admin("Usher")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Regular",
                "on_release": lambda x="Example 1": self.pass_admin("Regular")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "General Coordinator",
                "on_release": lambda x="Example 1": self.pass_admin("General Coordinator")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Associate Coordinator",
                "on_release": lambda x="Example 1": self.pass_admin("Associate Coordinator")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Group Coordinator",
                "on_release": lambda x="Example 1": self.pass_admin("Group Coordinator")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Regional Coordinator",
                "on_release": lambda x="Example 1": self.pass_admin("Regional Coordinator")
            }
        ]

        self.worker_reg_drop = MDDropdownMenu(
            caller=self.ids.select_admin_type,
            items=self.admin_levels,
            width_mult=3
        )
        self.worker_reg_drop.open()

    def pass_admin(self, data):
        self.ids.worker_type.text = data
        self.worker_reg_drop.dismiss()

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
            caller=self.ids.gender_btn,
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
            caller=self.ids.marital_status_btn,
            items=self.status_list,
            size_hint_max_y=.09,
            width_mult=3
        )
        self.marital_drop.open()

    def update_marital_status(self, data):
        self.ids.marital_status.text = data
        self.marital_drop.dismiss()

"""
{
  "location_id": "string",
  "admin": "string"
}

{
  "user_id": "string",
  "location_id": "string",
  "location": "string",
  "name": "string",
  "gender": "string",
  "phone": "string",
  "email": "user@example.com",
  "address": "string",
  "occupation": "string",
  "marital_status": "string",
  "unit": "string",
  "created_at": "2024-02-16T14:20:06.688Z"
}
"""