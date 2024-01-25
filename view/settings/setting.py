# this screen view gives details settings the developer company of the application
from kivy.uix.screenmanager import Screen


class SettingsScreenView(Screen):

    def see_api(self,instance, value):
        if value:
            self.ids.api_url.password = True
        else:
            self.ids.api_url.password = False
