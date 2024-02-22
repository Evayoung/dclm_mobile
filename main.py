# Thank You, Jesus!
import os
import pickle
import threading
from datetime import datetime
import asyncio
from plyer import vibrator

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox

from utility_.backend import *
from utility_.validator import Validate
from view.attendance.attendance import AttendanceScreenView
from view.counter.counter import CounterScreenView

# import all other added screens here
from view.home.home import HomeScreenView
from view.login.login import LoginScreenView
from view.record.record import RecordScreenView
from view.settings.setting import SettingsScreenView
from view.signup.signup import SignupScreenView
from view.splash.splash import SplashScreenView
from view.viewdata.viewdata import ViewdataScreenView
from view.workers.workers import WorkersScreenView

Builder.load_file("view/splash/splash.kv")

# Window.size = (400, 700)
# Window.size = (350, 660)

# color schema
colors = {
    "Teal": {
        "200": "#010140",
        "500": "#010140",
        "700": "#010140",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#FFFFFF",
        "Background": "#E6E6E6",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}


class URLOperator(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, text, second, img, status, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.secondary_text = second
        self.ids.img.source = img
        if status == "Present":
            self.ids.check.active = True
        else:
            self.ids.check.active = False

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)


class RightCheckbox(IRightBody, MDCheckbox):
    pass


class SubmitData(MDBoxLayout):
    p_domain = StringProperty()
    p_type = StringProperty()
    l_name = StringProperty()
    l_id = StringProperty()


class GetWorker(MDBoxLayout):
    def __init__(self, id_, fullname, location, email, units, **kwargs):
        super().__init__(**kwargs)
        self.ids.user_id.text = id_
        self.ids.fullname.text = fullname
        self.ids.location_id.text = location
        self.ids.email.text = email
        self.ids.units.text = units


class AttendanceSetup(MDBoxLayout):
    def __init__(self, get_all, gender, units, loc_id, **kwargs):
        super().__init__(**kwargs)
        if get_all:
            self.ids.all_workers.active = True

        if loc_id:
            self.ids.check_location.active = True
            self.ids.by_location.text = loc_id

        if gender:
            self.ids.check_gender.active = True
            self.ids.by_gender.text = gender

        if units:
            self.ids.check_units.active = True
            self.ids.by_units.text = units

    def use_id(self, checkbox, value):
        if value:
            self.ids.by_location.readonly = False
        else:
            self.ids.by_location.readonly = True
            self.ids.by_location.text = ''

    def use_gender(self, checkbox, value):
        if value:
            self.ids.by_gender.readonly = False
        else:
            self.ids.by_gender.readonly = True
            self.ids.by_gender.text = ''

    def use_units(self, checkbox, value):
        if value:
            self.ids.by_units.readonly = False
        else:
            self.ids.by_units.readonly = True
            self.ids.by_units.text = ''


class ShowPending(MDBoxLayout):
    def __init__(self, id_, fullname, location, email, units, **kwargs):
        super().__init__(**kwargs)
        self.ids.user_id.text = id_
        self.ids.fullname.text = fullname
        self.ids.location_id.text = location
        self.ids.email.text = email
        self.ids.units.text = units


class EditCount(MDBoxLayout):
    a = NumericProperty()
    b = NumericProperty()
    c = NumericProperty()
    d = NumericProperty()
    e = NumericProperty()
    f = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.a.text = str(self.a)
        self.ids.b.text = str(self.b)
        self.ids.c.text = str(self.c)
        self.ids.d.text = str(self.d)
        self.ids.e.text = str(self.e)
        self.ids.f.text = str(self.f)


class SetupReg(MDFloatLayout):
    validate = Validate()
    p_domain = StringProperty()
    p_type = StringProperty()
    p_level = StringProperty()
    l_id = StringProperty()
    valid = False

    def validate_id(self, instance, value):
        level = self.ids["p_level"].text

        if level == "National":
            if not self.validate.validate_national(value):
                self.ids.error.color = "red"
                self.ids.error.text = "Entry is not a valid National ID"
                self.ids.id_in.md_bg_color = "#F7DCDC"
                self.ids.p_id.foreground_color = "red"
                self.handle_button()
                return

        if level == "State":
            if not self.validate.validate_state(value):
                self.ids.error.color = "red"
                self.ids.error.text = "Entry is not a valid State ID"
                self.ids.id_in.md_bg_color = "#F7DCDC"
                self.ids.p_id.foreground_color = "red"
                self.handle_button()
                return

        if level == "Region":
            if not self.validate.validate_region(value):
                self.ids.error.color = "red"
                self.ids.error.text = "Entry is not a valid Region ID"
                self.ids.id_in.md_bg_color = "#F7DCDC"
                self.ids.p_id.foreground_color = "red"
                self.handle_button()
                return

        if level == "Group":
            if not self.validate.validate_group(value):
                self.ids.error.color = "red"
                self.ids.error.text = "Entry is not a valid Group ID"
                self.ids.id_in.md_bg_color = "#F7DCDC"
                self.ids.p_id.foreground_color = "red"
                self.handle_button()
                return

        if level == "Location":
            if not self.validate.validate_location(value):
                self.ids.error.color = "red"
                self.ids.error.text = "Entry is not a valid Location ID"
                self.ids.id_in.md_bg_color = "#F7DCDC"
                self.ids.p_id.foreground_color = "red"
                self.handle_button()
                return

        self.ids.id_in.md_bg_color = app.theme_cls.bg_normal
        self.ids.error.text = ""
        self.ids.p_id.foreground_color = app.theme_cls.primary_color
        self.ids.submit_btn.disabled = False
        self.ids.submit_btn.md_bg_color = app.theme_cls.primary_color

    def handle_button(self):
        self.ids.submit_btn.disabled = True
        self.ids.submit_btn.md_bg_color = "#262645"

    def reset_error_lbl(self, *args):
        self.ids.error.text = ""
        self.ids.error.color = "green"

    def confirm_saved(self):
        self.ids.error.text = "Data Saved successfully!"
        self.ids.error.color = "green"
        Clock.schedule_once(self.reset_error_lbl, 2)

    def program_domain_dropdown(self):
        self.data = [
            {
                "viewclass": "OneLineListItem",
                "text": "Crusade Programs",
                "on_release": lambda x="Example 1": self.update_domain("Crusade Programs")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Retreat Programs",
                "on_release": lambda x="Example 1": self.update_domain("Retreat Programs")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Weekly Programs",
                "on_release": lambda x="Example 1": self.update_domain("Weekly Programs")
            }
        ]

        self.program_domain_drop = MDDropdownMenu(
            caller=self.ids.p_dom,
            items=self.data,
            width_mult=3
        )
        self.program_domain_drop.open()

    def update_domain(self, data):
        self.ids.p_domain.text = data
        self.program_domain_drop.dismiss()

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
        prog_type = self.ids.p_domain.text

        if prog_type == 'Crusade Programs':
            self.program_type = self.data[0]

        if prog_type == 'Retreat Programs':
            self.program_type = self.data[1]

        if prog_type == 'Weekly Programs':
            self.program_type = self.data[2]

        self.program_type_drop = MDDropdownMenu(
            caller=self.ids.p_typ,
            items=self.program_type,
            width_mult=3
        )
        self.program_type_drop.open()

    def update_type(self, data):
        if data == 'Special Program':
            self.ids.p_type.readonly = False
            self.ids.p_type.text = ''
        else:
            self.ids.p_type.readonly = True
            self.ids.p_type.text = data
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
                "text": "State",
                "on_release": lambda x="Example 1": self.update_level("State")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Region",
                "on_release": lambda x="Example 1": self.update_level("Region")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Group",
                "on_release": lambda x="Example 1": self.update_level("Group")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Location",
                "on_release": lambda x="Example 1": self.update_level("Location")
            }
        ]

        self.program_level_drop = MDDropdownMenu(
            caller=self.ids.level,
            items=self.program_level,
            width_mult=3
        )
        self.program_level_drop.open()

    def update_level(self, data):
        self.ids.p_level.text = data
        self.ids.p_id.text = ""
        self.program_level_drop.dismiss()


class MyToggleButton(MDRectangleFlatIconButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_normal = self.theme_cls.bg_normal
        self.md_bg_color = self.theme_cls.bg_normal


class CardItem(MDCard):
    def __init__(self, id_, program, date, pics, **kwargs):
        super().__init__(**kwargs)
        self.ids.data_id.text = id_
        self.ids.program.text = program
        self.ids.date.text = date
        self.ids.picture.source = pics


class Category(MDCard):
    pass


class CountSummary(MDFloatLayout):
    pass


class WindowManager(ScreenManager):
    pass


class DCLMCounter(MDApp):
    # url = "https://dclm-server.onrender.com"
    state = StringProperty("stop")
    validate = Validate()
    navigator = []
    logout_dialog = None
    reset_dialog = None
    countItem_Dialog = None
    setUp_Dialog = None
    edit_count_Dialog = None
    confirm_submit_Dialog = None
    worker_details_dialog = None
    attendance_setup_dialog = None
    admin_dialog = None
    confirm_get_worker = None
    menu_drop = None
    check_offline_data = True

    # these values are for data identification and customization
    program_domain = None
    program_type = None
    program_level = None
    program_id = None
    convert_type = None

    login = False
    submit = False
    url_dialog = None
    edit_url = False

    gen_animate = True
    access_token = ''
    author = ''

    worker_on = None
    location_id_ = None
    gender_ = None
    unit_ = None
    internet = True
    pending = 0
    submitted_count = 0
    not_submitted_count = 0
    marked_data = []
    a, b, c, d, e, f, g = 0, 0, 0, 0, 0, 0, 0

    def build(self):
        ''' Initializes the Application
        and returns the root widget'''
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.accent_hue = '200'
        self.title = "DCLM Counter"
        self.wm = WindowManager(transition=FadeTransition())
        threading.Thread(target=self.load_screens, daemon=True).start()
        # Clock.schedule_once(self.load_screens, 5)

        screens = [
            SplashScreenView(name='splash'),
            SignupScreenView(name='signup'),
            LoginScreenView(name='login'),
            HomeScreenView(name='home'),
            CounterScreenView(name='counter'),
            RecordScreenView(name='record'),
            ViewdataScreenView(name='pending'),
            AttendanceScreenView(name='attendance'),
            SettingsScreenView(name='settings'),
            WorkersScreenView(name='workers')

        ]

        # add all screen class to the ScreenManager
        for screen in screens:
            self.wm.add_widget(screen)

        return self.wm

    def on_start(self):
        Window.softinput_mode = "below_target"
        Window.bind(on_keyboard=self.back_button)
        # self.create_pickle_file()
        self.administer_setup()
        self.call_config()
        # self.change_pics()
        Clock.schedule_once(self.load_remember_me, 1)
        Clock.schedule_once(self.update_pending, 1)

    def change_screen(self, screen):
        """Change screen using the window manager."""
        self.wm.current = screen

    def update_pending(self, *args):
        try:
            res1 = get_counts()
            res2 = get_registration()
            data = len(res1) + len(res2)
            if data != 0:
                self.pending = data
                self.counter_update()
        except Exception as e:
            pass

        if self.pending:
            self.wm.screens[3].ids['pending_data_count'].text = str(self.pending)

    def vibrate_now(self, *args):
        # pass
        vibrator.vibrate(time=0.1)

    # ===================== this functions update labels or widget within the application interface ===================
    def update_counter_title(self, title):
        self.wm.screens[0].ids['counter_title'].text = title

    # ======================================== this creates the home menu list ========================================
    #     pics = ["images/lm.png", "images/mbs.png", "images/trh.png", "images/sws.png", "images/wm.png"]

    def menu_dropdown(self):  # drop down to select the user role
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "SetUp",
                "on_release": lambda x="Example 1": self.setup_program_dialog()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "About Developer",
                "on_release": lambda x="Example 3": self.call_page("settings")

            }
        ]

        self.menu_drop = MDDropdownMenu(
            caller=self.wm.screens[3].ids.menu_btn,
            items=self.menu_list,
            width_mult=3,
            elevation=1,

        )
        self.menu_drop.open()

    def call_page(self, data):
        self.change_screen(data)
        self.menu_drop.dismiss()

    # ===============================================> Confirm user logout <===========================================
    def confirm_logout_dialog(self, *args):
        if not self.logout_dialog:
            self.logout_dialog = MDDialog(
                text="You are settings to logout?",
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.cancel_logout_dialog,
                    ),

                    MDFlatButton(
                        text="Confirm",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.confirm_logout,
                    )
                ]
            )
        self.logout_dialog.open()

    def cancel_logout_dialog(self, *args):
        self.logout_dialog.dismiss()

    def confirm_logout(self, *args):
        # self.wm.screens[2].ids['user_passwrd'].text = ""
        self.logout_dialog.dismiss()
        self.indicate_login(2, 'login_btn')
        # self.wm.screens[2].ids['login_btn'].disabled = False
        self.change_screen('login')

    # =======================================> list count item dialog box <============================================
    def view_count_dialog(self, *args):
        if not self.countItem_Dialog:
            self.countItem_Dialog = MDDialog(
                type="custom",
                content_cls=CountSummary(),
                size_hint=(.9, .8),
                elevation=0,
                md_bg_color="white",
                padding=[0],
                buttons=[
                    MDFlatButton(
                        text="Close",
                        padding=0,
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.close_count_view,
                    )
                ]
            )
        self.countItem_Dialog.open()

    def close_count_view(self, *args):
        self.countItem_Dialog.dismiss()

    # =======================================> setup Attendance for workers <==========================================
    def attendance_set_dialog(self, *args):
        self.load_filter_data()
        if not self.attendance_setup_dialog:
            self.attendance_setup_dialog = MDDialog(
                auto_dismiss=False,
                title='Search parameter',
                type="custom",
                content_cls=AttendanceSetup(self.worker_on, self.gender_, self.unit_, self.location_id_),
                elevation=0,
                md_bg_color="white",
                padding=[0]
            )
        self.attendance_setup_dialog.open()

    def close_attendance_setup(self, *args):
        if self.attendance_setup_dialog:
            self.attendance_setup_dialog.dismiss()
            self.attendance_setup_dialog = None

    def confirm_get_workers(self):
        if self.internet:
            response = search_workers_by_params(get_all=True)
            if not response:
                self.attendance_set_dialog()
            else:
                if not self.confirm_get_worker:
                    self.confirm_get_dialog = MDDialog(
                        auto_dismiss=False,
                        text="Attendance in the local database will be lost if you change settings?",
                        buttons=[
                            MDFlatButton(
                                text="Back",
                                theme_text_color="Custom",
                                text_color=app.theme_cls.primary_color,
                                on_release=self.close_confirm_get,
                            ),

                            MDFlatButton(
                                text="Continue",
                                theme_text_color="Custom",
                                text_color=app.theme_cls.primary_color,
                                on_release=self.continue_get_workers,
                            )
                        ]
                    )
                    self.confirm_get_dialog.open()
                    # self.confirm_get_dialog.
                else:
                    toast("This is available in internet mode only")

    def close_confirm_get(self, *args):
        self.confirm_get_dialog.dismiss()

    def continue_get_workers(self, *args):
        self.confirm_get_dialog.dismiss()
        delete_all_taken_attendance()
        self.update_attendance_count()
        self.attendance_set_dialog()

    # =======================================> setup program dialog box <==============================================
    def setup_program_dialog(self, *args):
        if self.menu_drop:
            self.menu_drop.dismiss()
            self.menu_drop = None

        if not self.setUp_Dialog:
            self.setUp_Dialog = MDDialog(
                title='Setup Program',
                type="custom",
                content_cls=SetupReg(p_domain=self.program_domain, p_type=self.program_type,
                                     p_level=self.program_level,
                                     l_id=self.program_id),
                size_hint=(.9, .8),
                elevation=0,
                md_bg_color="white",
                padding=[0],
            )
        self.setUp_Dialog.open()

    def close_setup_dialog(self, *args):
        self.setUp_Dialog.dismiss()

    def save_setup(self, domain, type_, level, pid):
        directory = "app_data"
        filename = "location_setup.pkl"
        updated_data = {"program_domain": domain,
                        "program_type": type_,
                        "program_level": level,
                        "location_id": pid
                        }

        existing_data = self.read_pickle_file(directory, filename)
        if existing_data is not None:
            existing_data.update(updated_data)
            filepath = os.path.join(directory, filename)
            with open(filepath, "wb") as file:
                pickle.dump(existing_data, file)

        self.administer_setup()

    # =======================================> setup program dialog box <==============================================
    def edit_count_dialog(self, *args):
        if not self.edit_count_Dialog:
            self.edit_count_Dialog = MDDialog(
                title='Edit Count',
                type="custom",
                content_cls=EditCount(a=self.a, b=self.b, c=self.c, d=self.d, e=self.e, f=self.f),
                size_hint=(.85, .8),
                elevation=0,
                md_bg_color="white",
                padding=[0],
            )
        self.edit_count_Dialog.open()

    def close_edit_dialog(self, *args):
        self.edit_count_Dialog.dismiss()
        self.edit_count_Dialog = None

    def save_edited(self, a, b, c, d, e, f):
        self.a, self.b, self.c, self.d, self.e, self.f = int(a), int(b), int(c), int(d), int(e), int(f)
        self.wm.screens[4].ids["adult_male"].text = a
        self.wm.screens[4].ids["adult_female"].text = b
        self.wm.screens[4].ids["youth_male"].text = c
        self.wm.screens[4].ids["youth_female"].text = d
        self.wm.screens[4].ids["boys"].text = e
        self.wm.screens[4].ids["girls"].text = f
        self.add_count()

    # =======================================> Confirm Submit data Dialog <============================================
    def confirm_submit_dialog(self, *args):
        date = self.wm.screens[4].ids["set_date"].text
        if not self.g:
            toast("You can't submit an empty count")
            return
        if (self.program_domain or self.program_type or self.program_level or self.program_id) == '':
            toast("Please set the location identities")
            return

        if not date:
            toast("Please set the date")
            return
        if not self.confirm_submit_Dialog:
            self.confirm_submit_Dialog = MDDialog(
                title='Submit with these data?',
                type="custom",
                content_cls=SubmitData(p_domain=self.program_domain, p_type=self.program_type,
                                       l_name=self.program_level,
                                       l_id=self.program_id),
                size_hint=(.9, .8),
                elevation=0,
                md_bg_color="white",
                padding=[0],
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.cancel_submit_dialog,
                    ),

                    MDFlatButton(
                        text="Proceed",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.submit_count,
                    )
                ]
            )
        self.confirm_submit_Dialog.open()

    def cancel_submit_dialog(self, *args):
        self.confirm_submit_Dialog.dismiss()
        self.confirm_submit_Dialog = None

    # ============================================> confirm reset counter (counter) <==================================
    def confirm_reset_dialog(self, *args):
        if not self.reset_dialog:
            self.reset_dialog = MDDialog(
                text="You are settings to clear all Counts?",
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.cancel_reset_dialog,
                    ),

                    MDFlatButton(
                        text="Confirm",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.proceed_reset_logout,
                    )
                ]
            )
        self.reset_dialog.open()

    def cancel_reset_dialog(self, *args):
        self.reset_dialog.dismiss()

    def proceed_reset_logout(self, *args):
        self.reset_dialog.dismiss()
        self.reset_counter()

    # ===============================================> Confirm user logout <===========================================
    def check_admin_dialog(self, data):
        self.change_screen("workers")
        self.add_screen_2list("home")

    def close_admin_dialog(self, *args):
        self.admin_dialog.dismiss()

    # this region is where the pickle file and all other document files for serialization of the application will reside
    # ==================================================================================================================
    def create_directory(self, directory):
        os.makedirs(directory)

    # this creates a serializing file to save the application program setup

    def create_pickle_file(self):
        directory = "app_data"
        if not os.path.exists(directory):
            filename = 'location_setup.pkl'
            data = {"program_domain": "",
                    "program_type": "",
                    "program_level": "",
                    "location_id": ""
                    }
            self.create_directory(directory)

            filepath = os.path.join(directory, filename)
            with open(filepath, "wb") as file:
                pickle.dump(data, file)

    # this is often called to deserialize the application setup
    def read_pickle_file(self, directory, filename):
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as file:
                loaded_data = pickle.load(file)
                return loaded_data
        else:
            toast(f"File '{filepath}' not found.")
            # print(f"File '{filepath}' not found.")
            return None

    def administer_setup(self):
        directory = "app_data"
        filename = "location_setup.pkl"
        loaded_data = self.read_pickle_file(directory, filename)
        self.program_domain = loaded_data["program_domain"]
        self.program_type = loaded_data["program_type"]
        self.program_level = loaded_data["program_level"]
        self.program_id = loaded_data["location_id"]
        self.home_display_setup()

    def call_config(self):
        # Load endpoint from the JSON file at startup
        with open("app_data/config.json", "r") as config_file:
            loaded_data = json.load(config_file)

        main_endpoint = loaded_data.get("main_endpoint")
        set_server_url(main_endpoint)
        self.wm.screens[8].ids['api_url'].text = main_endpoint

        # https://dclm-server.onrender.com

    def app_config_file(self, data):
        # Save endpoint to a JSON file
        endpoint_data = {"main_endpoint": data}
        with open("app_data/config.json", "w") as config_file:
            json.dump(endpoint_data, config_file)

        self.call_config()

    def home_display_setup(self):
        self.wm.screens[3].ids['program_domain'].text = self.program_domain
        self.wm.screens[3].ids['program_type'].text = self.program_type
        self.wm.screens[3].ids['program_level'].text = self.program_level
        self.wm.screens[3].ids['location_id'].text = self.program_id

    def add_salvation(self, instance, value):
        if value is True:
            self.convert_type = "Salvation"
        else:
            self.convert_type = None

    def add_restitution(self, instance, value):
        if value is True:
            self.convert_type = "Restitution"
        else:
            self.convert_type = None

    # #################################################################################################################
    def show_worker_details(self, the_list_item):
        if not self.worker_details_dialog:
            details = fetch_details(the_list_item)
            self.worker_details_dialog = MDDialog(
                auto_dismiss=False,
                title="Worker details",
                type="custom",
                content_cls=GetWorker(id_=details[6], fullname=details[7], location=details[13], email=details[10],
                                      units=details[11]),
                md_bg_color="white"

            )
        self.worker_details_dialog.open()

    def close_worker_details(self, *args):
        self.worker_details_dialog.dismiss()
        self.worker_details_dialog = None

    # ########################################### Edit url ############################################################

    def show_url_editor(self):
        if not self.edit_url:
            self.edit_url = True
            if not self.url_dialog:
                # details = fetch_details(the_list_item)
                self.url_dialog = MDDialog(
                    title="Warning!",
                    md_bg_color="white",

                    text="Editing this URL can cause the app to misbehave and you will not be able to connect to the "
                         "central server anymore \n\nContinue anyways?",
                    buttons=[
                        MDFlatButton(
                            text="Cancel",
                            theme_text_color="Custom",
                            text_color=app.theme_cls.primary_color,
                            on_release=self.cancel_url_dialog,
                        ),

                        MDFlatButton(
                            text="Continue",
                            theme_text_color="Custom",
                            text_color=app.theme_cls.primary_color,
                            on_release=self.continue_url_dialog,
                        )
                    ]
                )
            self.url_dialog.open()
        else:
            url_update = self.wm.screens[8].ids['api_url'].text
            self.app_config_file(url_update)
            self.edit_url = False
            self.wm.screens[8].ids['edit_url_btn'].text = "Edit"
            self.wm.screens[8].ids['api_url'].password = True
            self.wm.screens[8].ids['api_url'].readonly = True

    def continue_url_dialog(self, *args):
        self.wm.screens[8].ids['api_url'].password = False
        self.wm.screens[8].ids['api_url'].readonly = False
        self.url_dialog.dismiss()
        self.url_dialog = None
        self.wm.screens[8].ids['edit_url_btn'].text = "Save"

    def cancel_url_dialog(self, *args):
        self.url_dialog.dismiss()
        self.url_dialog = None
        self.edit_url = False

    # def enforce_widget(self):

    # ===================================== update count data as clicked ==============================================

    def add_count(self):
        self.g = self.a + self.b + self.c + self.d + self.e + self.f
        self.wm.screens[4].ids["counter"].text = str(self.g)

    def adult_male(self):
        self.a += 1
        self.wm.screens[4].ids["adult_male"].text = str(self.a)
        self.add_count()

    def adult_female(self):
        self.b += 1
        self.wm.screens[4].ids["adult_female"].text = str(self.b)
        self.add_count()

    def youth_male(self):
        self.c += 1
        self.wm.screens[4].ids["youth_male"].text = str(self.c)
        self.add_count()

    def youth_female(self):
        self.d += 1
        self.wm.screens[4].ids["youth_female"].text = str(self.d)
        self.add_count()

    def boys(self):
        self.e += 1
        self.wm.screens[4].ids["boys"].text = str(self.e)
        self.add_count()

    def girls(self):
        self.f += 1
        self.wm.screens[4].ids["girls"].text = str(self.f)
        self.add_count()

    def reset_counter(self):
        self.a, self.b, self.c, self.d, self.e, self.f, self.g = 0, 0, 0, 0, 0, 0, 0
        self.wm.screens[4].ids["adult_male"].text = "0"
        self.wm.screens[4].ids["adult_female"].text = "0"
        self.wm.screens[4].ids["youth_male"].text = "0"
        self.wm.screens[4].ids["youth_female"].text = "0"
        self.wm.screens[4].ids["boys"].text = "0"
        self.wm.screens[4].ids["girls"].text = "0"
        self.wm.screens[4].ids["counter"].text = "0"

    # =================================================================================================================
    #                                   SUBMIT COUNT DATA FROM COUNTER
    # =================================================================================================================

    # def add_note(self, ):

    def indicate_save_data(self, screen, widget):
        button = self.wm.screens[screen].ids[f'{widget}']
        if self.submit:
            button.text = "Sending..."
            button.md_bg_color = "#3F3F66"
        else:
            button.text = "Save"
            button.md_bg_color = app.theme_cls.primary_color

    def submit_count(self, *args):
        self.confirm_submit_Dialog.dismiss()
        if all(field.strip() for field in
               (self.program_domain, self.program_type, self.program_level, self.program_id)):
            payload = {
                "program_domain": self.program_domain,
                "program_type": self.program_type,
                "location": self.program_level,
                "location_id": self.program_id,
                "date": self.wm.screens[4].ids["set_date"].text,
                "adult_male": self.a,
                "adult_female": self.b,
                "youth_male": self.c,
                "youth_female": self.d,
                "boys": self.e,
                "girls": self.f,
                "total": self.g,
                "author": self.author
            }
            if self.internet:
                Clock.schedule_once(lambda x: self.create_count(payload, self.access_token), 2)
                self.submit = True
                self.indicate_save_data(4, "save_count")
            else:
                Clock.schedule_once(lambda x: self.send_offline_db(payload), 2)

    def create_count(self, payload, token):
        try:

            count = create_counts(payload, token)
            if count.status_code == 201:  # Check the status code directly
                self.reset_counter()
                toast("Data Saved Successfully!")
                self.submit = False
                self.indicate_save_data(4, "save_count")
            if count.status_code == 500:
                toast("Error ")
                self.submit = False
                self.indicate_save_data(4, "save_count")
        except requests.RequestException as e:
            # print(f"Error creating user: {e}")
            self.send_offline_db(payload)
            self.submit = False
            self.indicate_save_data(4, "save_count")
            toast(f"Could not submit data, \n Data saved locally")

    def send_offline_db(self, payload):

        counts = insert_offline_count(payload)

        if counts:
            self.reset_counter()
            toast("Data Saved locally!")
            self.pending += 1
            self.update_pending()

        else:
            toast("Data could not be saved")

    def clear_reg_form(self, data):
        """ CLEAR FORM FIELD AFTER REGISTRATION OR WHEN THE EMAIL BOX IS EDITED"""
        if data:
            self.wm.screens[1].ids["user_id"].text = ""
            self.wm.screens[1].ids["user_name"].text = ""
            self.wm.screens[1].ids["user_phone"].text = ""
            self.wm.screens[1].ids["location_id"].text = ""
            self.wm.screens[1].ids["user_email"].text = ""
            self.wm.screens[1].ids["user_password"].text = ""
        else:
            self.wm.screens[1].ids["user_id"].text = ""
            self.wm.screens[1].ids["user_name"].text = ""
            self.wm.screens[1].ids["user_phone"].text = ""
            self.wm.screens[1].ids["location_id"].text = ""
            self.wm.screens[1].ids["user_password"].text = ""

    # """*** SERVER COMMUNICATION THROUGH THE BACKEND ***"""

    # #################################################################################################################
    #                                               CREATE NEW USER
    # #################################################################################################################
    def create_user_account(self, loc_id, name, phone, email, password, user_id):
        # Validate payload fields before creating the user
        if all(field.strip() for field in (loc_id, name, phone, email, password, user_id)):
            admin_type = self.assign_role(user_id)
            payload = {
                "user_id": user_id,
                "location_id": loc_id,
                "name": name,
                "phone": phone,
                "email": email,
                "password": password,
                "role": admin_type,
            }

            Clock.schedule_once(lambda x: self.create_now(payload), 2)
        else:
            toast("Please set a user password")

    def assign_role(self, id_):
        if "USR" in id_:
            return "Usher"

        elif "RER" in id_:
            return "Regular"

        elif "GER" in id_:
            return "General Coordinator"

        elif "ASR" in id_:
            return "Associate Coordinator"

        elif "GRR" in id_:
            return "Group Coordinator"

        elif "RIR" in id_:
            return "Regional Coordinator"

    def create_now(self, payload):
        try:
            app.state = "start"
            user = create_user(payload)
            if user.status_code == 201:  # Check the status code directly
                self.clear_reg_form(True)
                app.state = "stop"
                toast("User successfully created!")
            if user.status_code == 500:
                app.state = "stop"
                toast("Email already exist")
                app.state = "stop"
        except requests.RequestException as e:
            # print(f"Error creating user: {e}")
            toast(f"Error! could not create user, please try again")
            app.state = "stop"

    # #################################################################################################################
    #                                           GET USER DETAILS
    # #################################################################################################################

    def get_user_details(self, data):
        """ Get user details using the user email """
        if data != '':
            payload = data
            threading.Thread(target=self.call_generate, args=(payload,), daemon=True).start()
        else:
            toast('Please provide user email!')
            return

    def call_generate(self, payload):
        # Clock.schedule_once(self.update_ui, 0)  # Schedule UI update immediately

        try:
            response = get_details(payload)
            if response.status_code == 404:
                toast("User not found!")
            elif response.status_code == 200:
                user_data = response.json()
                # Update the Ui
                Clock.schedule_once(lambda x: self.update_ui(user_data), 0)
            else:
                toast("Error fetching user details.")
        except requests.RequestException as e:
            toast(f"Error processing requests: {e}")

    def update_ui(self, response):
        """ Updates UI elements with retrieved user data """

        if response:
            self.wm.screens[1].ids["user_id"].text = response.get("user_id", "")
            self.wm.screens[1].ids["user_name"].text = response.get("name", "")
            self.wm.screens[1].ids["user_phone"].text = response.get("phone", "")
            self.wm.screens[1].ids["location_id"].text = response.get("location_id", "")

    # ################################################################################################################
    #                                               LOGIN USER
    # ################################################################################################################

    def indicate_login(self, screen, name):
        button = self.wm.screens[screen].ids[f'{name}']

        if self.login:
            button.text = "loading..."
            button.md_bg_color = '#3F3F66'
            button.disabled = True
        else:
            # Revert button appearance when login is not in progress
            button.disabled = False
            button.text = "Login"
            button.md_bg_color = app.theme_cls.primary_color

    def update_offline(self, checkbox, value):
        self.vibrate_now()
        if value:
            self.internet = True
        else:
            self.internet = False

    def do_login(self, user_email, user_password):
        if (user_email and user_password) != "":
            payload = {
                'username': user_email,
                'password': user_password
            }

            if self.internet:
                self.login = True
                self.indicate_login(2, "login_btn")
                threading.Thread(target=self.pass_login_data, args=(payload,), daemon=True).start()
                # Clock.schedule_once(lambda x: self.pass_login_data(payload), 2)
            else:
                Clock.schedule_once(lambda x: self.pass_offline_data(payload), 1)

        else:
            toast('Please fill all field')

    def pass_offline_data(self, payload):
        """ ** this is called when the user uses the app in the offline mode ** """
        try:
            response = offline_login(payload)
            if response:
                data = {
                    "user_name": response[2],
                    "user_id": response[1],
                    "user_role": response[4]
                }
                self.change_screen("home")
                self.update_view(data)
            else:
                toast("Please use internet if this is your first login on the app")
        except requests.RequestException as e:
            toast("Please connect your internet, credentials not found")
            # print(e)

    def pass_login_data(self, payload):
        try:

            response = login_user(payload)

            if response.status_code == 200:  # Check the status code directly
                access_token = response.json().get('access_token')
                Clock.schedule_once(lambda x: insert_user(response.json()), 0)

                data = {
                    "user_name": response.json().get('user_name'),
                    "user_id": response.json().get('user_id'),
                    "user_role": response.json().get('user_role')
                }

                self.access_token = access_token
                self.author = response.json().get('user_id')

                Clock.schedule_once(lambda x: self.update_view(data), 0)
                Clock.schedule_once(lambda x: self.change_screen("home"), 0)
                self.remember_me()
                self.login = False

            else:
                self.login = False
                Clock.schedule_once(lambda x: self.indicate_login(2, "login_btn"), 0)
                Clock.schedule_once(lambda x: toast("Login failed! Please check credentials"), 0)

        except requests.RequestException as e:
            self.login = False
            Clock.schedule_once(lambda x: self.indicate_login(2, "login_btn"), 0)
            Clock.schedule_once(lambda x: toast("Connection error! Please check your network."), 0)
            app.state = "stop"

    def update_view(self, data):
        self.wm.screens[3].ids['user_id'].text = data["user_id"]
        self.wm.screens[3].ids['user_nam'].text = data['user_name']
        self.wm.screens[3].ids['user_typ'].text = data['user_role']

    # #################################################################################################################
    #                                       HANDLE WORKERS ATTENDANCE
    # #################################################################################################################
    attendance = []

    def mark(self, check, the_list_item):
        if check.active:
            self.vibrate_now()
            date_ = datetime.today()
            dat = date_.strftime("%Y-%m-%d")
            self.update_details(self.program_domain, self.program_type, self.program_level, self.program_id, dat,
                                "Present", the_list_item.secondary_text)
            # self.attendance.append(the_list_item.secondary_text)
            insert_attendance_count(the_list_item.secondary_text)
            self.update_attendance_count()
            toast(f"{the_list_item.secondary_text} is added to attendance.")
        else:
            self.update_details('', '', '', '', '',
                                "", the_list_item.secondary_text)
            # self.attendance.remove(the_list_item.secondary_text)
            delete_an_attendance(the_list_item.secondary_text)
            self.update_attendance_count()
            toast(f"{the_list_item.secondary_text} was removed from attendance.")

    def update_attendance_count(self):
        attendance = fetch_attendance_count()
        self.wm.screens[7].ids['total_attendance'].text = str(len(attendance))

    def update_details(self, program_domain, program_type, location, location_id, date, status, worker_id):
        update_attendance(program_domain, program_type, location, location_id, date, status, worker_id)

    # #################################################################################################################
    #                                   Load all workers data for attendance
    # #################################################################################################################
    def load_filter_data(self, *args):
        path = "app_data/worker_filter.json"
        data = self.load_json_files(path)
        if data:
            self.location_id_ = data['location_id']
            self.gender_ = data['gender']
            self.unit_ = data['unit']
            self.worker_on = data['get_all']

    def load_json_files(self, json_path):
        try:
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            return False

    def set_worker_data(self, by_location, by_gender, by_units, all_workers):
        json_path = "app_data/worker_filter.json"
        get_all = None
        if all_workers.active:
            get_all = True
        else:
            get_all = False

        filter_worker = {
            "get_all": get_all,
            "location_id": by_location.text,
            "gender": by_gender.text,
            "unit": by_units.text
        }
        self.create_worker_filter(filter_worker, json_path)
        self.load_filter_data()

        # if not (self.location_id_ or self.gender_ or self.unit_ or self.worker_on):
        #     return False
        # else:
        Clock.schedule_once(lambda x: delete_all_attendance(), 0)
        threading.Thread(target=self.load_data_gradually, daemon=True).start()

    def get_all_workers_data(self):
        if self.internet:
            if all(field.strip() for field in
                   (self.program_domain, self.program_type, self.program_level, self.program_id)):
                # response = search_workers_by_params(get_all=True)
                # if not response:
                threading.Thread(target=self.load_data_gradually, daemon=True).start()

            else:
                toast("Please setup program parameter. can't load workers")
        else:
            toast("This can not be used in offline mode")

    def clear_attendance_widget(self, *args):
        mdlist = self.wm.screens[7].ids['worker_list']
        mdlist.clear_widgets()

    def remember_me(self):
        """ this function helps to save the user login credentials for next time 'remember me' is ticked """
        user_mail = self.wm.screens[2].ids['user_login'].text
        user_password = self.wm.screens[2].ids['user_password'].text
        json_path = "app_data/remember_me.json"
        if self.wm.screens[2].ids['remember'].active:
            value = True
        else:
            value = False
        data = {
            "email": user_mail,
            "password": user_password,
            "remember_me": value
        }
        self.create_worker_filter(data, json_path)

    def load_remember_me(self, *args):
        try:
            with open("app_data/remember_me.json", 'r') as json_file:
                data = json.load(json_file)
            if data['remember_me']:
                self.wm.screens[2].ids['remember'].active = True
                self.wm.screens[2].ids['user_login'].text = data['email']
                self.wm.screens[2].ids['user_password'].text = data['password']
        except FileNotFoundError:
            return False

    def create_worker_filter(self, data, json_path):
        """ Create a JSON file with the given data. """
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def load_data_gradually(self, *args):
        try:
            data = get_workers(self.access_token, self.worker_on, self.location_id_, self.gender_, self.unit_)
            if data.status_code == 200 and data != []:
                Clock.schedule_once(lambda x: self.pass_locally(data), 0)

        except requests.RequestException as e:
            toast(f"Error! {e}")

    def pass_locally(self, data):
        self.clear_attendance_widget()
        for i in data.json():
            payload = {
                'program_domain': '',
                'program_type': '',
                'location': '',
                'location_id': '',
                'date': '',
                'worker_id': i.get('user_id'),
                'name': i.get('name'),
                'gender': i.get('gender'),
                'contact': i.get('phone'),
                'email': i.get('email'),
                'unit': i.get('unit'),
                'church_id': i.get('location_id'),
                'local_church': i.get('location'),
                'status': ''
            }
            # print(payload)
            try:
                insert_attendance(payload)
            except Exception as e:
                print(e)

        # Clock.schedule_once(lambda x: self.get_workers_back, 0)

    def get_workers_back(self, *args):
        self.clear_attendance_widget()
        try:
            img = None
            response = search_workers_by_params(get_all=True)
            for j in response:

                if j[8] == "Male":
                    img = "images/brother.png"

                if j[8] == "Female":
                    img = "images/sister.png"

                name = str(j[7])
                worker_id = str(j[6])
                status = j[14]

                self.add_item_to_view(name, worker_id, img, status)
            self.update_attendance_count()
        except requests.RequestException as e:
            toast(f"Error! {e}")

    def add_item_to_view(self, name, id_, img, status):
        mdlist = self.wm.screens[7].ids['worker_list']
        item = ListItemWithCheckbox(name, id_, img, status)
        mdlist.add_widget(item)

    def prep_worker_attendance(self):
        if all(field.strip() for field in
               (self.program_domain, self.program_type, self.program_level, self.program_id)):
            try:
                attendance = search_workers_by_params(get_all=True)
                threading.Thread(target=self.create_attendance, args=(attendance,), daemon=True).start()
                # Clock.schedule_once(lambda x: self.create_attendance(attendance), 2)
            except Exception as e:
                print(e)

        else:
            toast("Parameters to submit data not set, please click setup")

    def create_attendance(self, attendance):
        for data in attendance:
            if data[14] != "":
                payload = {
                    'program_domain': data[1],
                    'program_type': data[2],
                    'location': data[3],
                    'location_id': data[4],
                    'date': data[5],
                    'worker_id': data[6],
                    'name': data[7],
                    'gender': data[8],
                    'contact': data[9],
                    'email': data[10],
                    'unit': data[11],
                    'church_id': data[12],
                    'local_church': data[13],
                    'status': data[14]
                }
                self.do_attendance_submit(payload, data[6])
                # Clock.schedule_once(lambda x: self.do_attendance_submit(payload, data[6]), 0)

        if self.submitted_count > 0:
            Clock.schedule_once(lambda x: toast(f"{self.submitted_count} data submitted!"), 0)

        else:
            Clock.schedule_once(lambda x: toast(f"{self.not_submitted_count} attendance not submitted!"), 0)

    def do_attendance_submit(self, payload, data):
        try:
            response = submit_worker_attendance(payload, self.access_token)
            if response.status_code == 201:
                Clock.schedule_once(lambda x: search_workers_by_params(get_all=True), 0)
                Clock.schedule_once(lambda x: delete_one_attendance(data), 0)
                Clock.schedule_once(lambda x: self.find_item(data), 0)
                Clock.schedule_once(lambda x: delete_an_attendance(data), 0)
                Clock.schedule_once(lambda x: self.update_attendance_count(), 0)
                self.submitted_count += 1
                return response

        except requests.RequestException as e:
            self.not_submitted_count += 1

    def find_item(self, worker_id):
        mdlist = self.wm.screens[7].ids['worker_list']
        for i in mdlist.children:
            if i.secondary_text == worker_id:
                mdlist.remove_widget(i)

    # #################################################################################################################
    #                      GET EITHER COUNTS DATA, REGISTRATION DATA OR ALL THE DATA OFFLINE
    # #################################################################################################################

    def get_all_counts(self, checkbox, value):
        if value:
            self.counter_update()
        else:
            pass

    def get_all_reg(self, checkbox, value):
        if value:
            self.registration_update()
        else:
            pass

    def counter_update(self):
        response = get_counts()
        self.wm.screens[6].ids['pending_item_list'].clear_widgets()
        self.marked_data.clear()
        self.add_all_mark()
        for i in response:
            self.wm.screens[6].ids['pending_item_list'].add_widget(CardItem(id_=str(i[0]), program=i[2], date=i[5],
                                                                            pics='images/counts.png'))

    def registration_update(self):
        response = get_registration()
        self.wm.screens[6].ids['pending_item_list'].clear_widgets()
        self.marked_data.clear()
        self.add_all_mark()
        for i in response:
            self.wm.screens[6].ids['pending_item_list'].add_widget(CardItem(id_=str(i[0]), program=i[2], date=i[5],
                                                                            pics='images/reg.png'))

    def update_marked(self, check, data_id):
        if check.active:
            self.marked_data.append(data_id.text)
            self.add_all_mark()

        else:
            self.marked_data.remove(data_id.text)
            self.add_all_mark()

    def add_all_mark(self):
        count = len(self.marked_data)
        if count > 0:
            self.wm.screens[6].ids['total_marked'].text = str(count)
        else:
            self.wm.screens[6].ids['total_marked'].text = '0'

    def get_and_post_data(self, counts, reg):
        if self.internet:
            if counts.active:
                for i in self.marked_data:
                    data = select_each_count(i)
                    self.re_submit_counts(data, i)

            if reg.active:
                for j in self.marked_data:
                    data = select_each_reg(j)
                    self.resubmit_reg(data, j)
        else:
            toast("Please Log in again and mark Internet to send data")

    # #################################################################################################################
    #                           RE-SUBMIT DATA SAVED LOCALLY
    # #################################################################################################################
    def resubmit_reg(self, data, id_):
        payload = {
            "program_domain": data[1],
            "program_type": data[2],
            "location": data[3],
            "location_id": data[4],
            "date": data[5],
            "reg_type": data[6],
            "name": data[7],
            "gender": data[8],
            "phone": data[9],
            "home_address": data[10],
            "marital_status": data[11],
            "social_group": data[12],
            "social_status": data[13],
            "status_address": data[14],
            "level": data[15],
            "salvation_type": data[16],
            "invited_by": data[17],
            "author": data[18]
        }

        try:
            response = create_online_con_record(payload, self.access_token)
            if response.status_code == 201:
                toast("Data Successfully Submitted!")
                delete_registration(id_)
                self.registration_update()
                self.update_pending()
        except requests.RequestException as e:
            toast("Error, data not submitted!")

    def re_submit_counts(self, data, id_):
        payload = {
            "program_domain": data[1],
            "program_type": data[2],
            "location": data[3],
            "location_id": data[4],
            "date": data[5],
            "adult_male": data[6],
            "adult_female": data[7],
            "youth_male": data[8],
            "youth_female": data[9],
            "boys": data[10],
            "girls": data[11],
            "total": data[12],
            "author": data[13]
        }

        try:
            response = create_counts(payload, self.access_token)
            if response.status_code == 201:
                toast("Data Successfully Submitted!")
                delete_counts(id_)
                self.counter_update()
                self.update_pending()
        except requests.RequestException as e:
            toast("Error, data not submitted!")

    # #################################################################################################################

    def on_state(self, instance, value):
        {
            "start": self.wm.screens[1].ids['gen_progress'].start,
            "stop": self.wm.screens[1].ids['gen_progress'].stop,
        }.get(value)()

    # #################################################################################################################
    #                                       CONVERT / INVITEE DATA SUBMISSION LOGIC
    # #################################################################################################################
    def submit_form(self, name, gender, address, marital, social, job, j_address, level, inviter, phone, c_type, date):
        self.reg_type = ""
        if all(field.strip() for field in (name, gender, address, social, job, j_address, phone, c_type, date)):
            if self.wm.screens[5].ids['convert_click'].active:
                self.reg_type = "Convert"

            elif self.wm.screens[5].ids['invitee_click'].active:
                self.reg_type = "Invitee"

            else:
                toast("Please Select Convert or Invitee")
                return

            payload = {
                "program_domain": self.program_domain,
                "program_type": self.program_type,
                "location": self.program_level,
                "location_id": self.program_id,
                "date": date,
                "reg_type": self.reg_type,
                "name": name,
                "gender": gender,
                "phone": phone,
                "home_address": address,
                "marital_status": marital,
                "social_group": social,
                "social_status": job,
                "status_address": j_address,
                "level": level,
                "salvation_type": c_type,
                "invited_by": inviter,
                "author": self.author
            }

            if self.internet:
                self.submit = True
                self.indicate_save_data(5, "save_form")
                Clock.schedule_once(lambda x: self.pass_convert_to_db(payload), 2)
            else:
                Clock.schedule_once(lambda x: self.send_offline(payload), 2)

        else:
            toast("Please fill necessary filed before submitting")

    def pass_convert_to_db(self, payload):
        try:
            response = create_online_con_record(payload, self.access_token)
            if response.status_code == 201:
                toast("Data Saved Successfully!")
                self.submit = False
                self.indicate_save_data(5, "save_form")
        except requests.RequestException as e:
            self.submit = False
            self.indicate_save_data(5, "save_form")
            self.send_offline(payload)

    def send_offline(self, payload):
        insert_convert_offline(payload["program_domain"], payload["program_type"], payload["location"],
                               payload["location_id"], payload["date"], payload["reg_type"], payload["name"],
                               payload["gender"], payload["phone"], payload["home_address"], payload["marital_status"],
                               payload["social_group"], payload["social_status"], payload["status_address"],
                               payload["level"], payload["salvation_type"], payload["invited_by"], payload["author"])
        self.pending += 1
        self.update_pending()
        toast("Data Saved offline")

    # #################################################################################################################
    #                                       CONVERT / INVITEE DATA SUBMISSION LOGIC
    # #################################################################################################################
    def reset_worker_form(self):
        self.wm.screens[9].ids.worker_id.text = ""
        self.wm.screens[9].ids.full_name.text = ""
        self.wm.screens[9].ids.location_name.text = ""
        self.wm.screens[9].ids.gender.text = ""
        self.wm.screens[9].ids.phone_number.text = ""
        self.wm.screens[9].ids.email.text = ""
        self.wm.screens[9].ids.address.text = ""
        self.wm.screens[9].ids.occupation.text = ""
        self.wm.screens[9].ids.marital_status.text = ""
        self.wm.screens[9].ids.work_area.text = ""
        self.wm.screens[9].ids.worker_location_id.text = ""
        self.wm.screens[9].ids.worker_type.text = ""

    def generate_worker_id(self, location_id, worker_type):
        if (location_id and worker_type) != "":
            if worker_type == "Regional Coordinator":
                worker_type = "Rigional Coordinator"
            payload = {
                "location_id": location_id,
                "admin": worker_type
            }
            Clock.schedule_once(lambda x: self.get_worker_id(payload), 2)
            # threading.Thread(target=self.get_worker_id(payload), daemon=True).start()

    def get_worker_id(self, payload):
        try:
            response = generate_worker_id(payload)
            if response.status_code == 201:
                # print()
                self.wm.screens[9].ids.worker_id.text = response.json()
        except requests.RequestException as e:
            toast("Error! Worker could not be created.")

    def submit_worker_reg(self, worker_id, worker_location_id, location_name, full_name, gender, phone_number, email,
                          address, occupation, marital_status, work_area):

        if all(field.strip() for field in (
                worker_id, worker_location_id, location_name, full_name, gender, phone_number, address, marital_status,
                work_area)):
            payload = {
                "user_id": worker_id,
                "location_id": worker_location_id,
                "location": location_name,
                "name": full_name,
                "gender": gender,
                "phone": phone_number,
                "email": email,
                "address": address,
                "occupation": occupation,
                "marital_status": marital_status,
                "unit": work_area
            }
            Clock.schedule_once(lambda x: self.send_worker(payload), 2)

        else:
            toast("Please ever necessary field")

    def send_worker(self, payload):
        try:
            response = create_new_worker(payload)
            if response.status_code == 201:
                self.reset_worker_form()
                toast("Data Saved Successfully!")
        except requests.RequestException as e:
            toast("Error! Worker could not be created.")

    # #################################################################################################################
    #                                               OFFLINE DATABASE CONNECTION
    # #################################################################################################################

    def get_offline_search(self, data):
        mdlist = self.wm.screens[7].ids['worker_list']
        mdlist.clear_widgets()
        response = search_workers_by_params(name=data)
        if response:
            img = ''
            for j in response:
                if j[8] == "Male":
                    img = "images/brother.png"

                if j[8] == "Female":
                    img = "images/sister.png"

                name = str(j[7])
                user_id = str(j[6])
                status = j[14]
                # print(name)
                self.add_item_to_view(name, user_id, img, status)

    # =======================================> this controls the back button <=========================================
    def add_screen_2list(self, view):
        self.navigator.append(view)

    def remove_screen_4rm_list(self, *args):
        if self.navigator:
            self.navigator.pop()

    def back_button(self, window, key, *largs):
        if key == 27:
            data = self.navigator
            try:
                self.change_screen(data[-1])
                self.remove_screen_4rm_list()
            except Exception as e:
                app.stop()
            return True

    def load_screens(self, *args):
        Builder.load_file("view/login/login.kv")
        Builder.load_file("view/signup/signup.kv")
        Builder.load_file("view/home/home.kv")
        Builder.load_file("view/counter/counter.kv")
        Builder.load_file("view/record/record.kv")
        Builder.load_file("view/viewdata/viewdata.kv")
        Builder.load_file("view/attendance/attendance.kv")
        Builder.load_file("view/workers/workers.kv")
        Builder.load_file("view/settings/setting.kv")
        Builder.load_file("view/widgets/card_item.kv")
        Builder.load_file("view/widgets/attendance_setup.kv")
        Builder.load_file("view/widgets/count_summary.kv")
        Builder.load_file("view/widgets/setup_reg.kv")
        Builder.load_file("view/widgets/edit_count.kv")
        Builder.load_file("view/widgets/submit_data.kv")
        Builder.load_file("view/widgets/attendance_list.kv")
        Builder.load_file("view/widgets/get_workers.kv")
        Builder.load_file("view/widgets/get_app_apiurl.kv")

    def create_local_db(self):
        self.create_pickle_file()
        create_worker()
        create_attendance()
        create_offline_count()
        create_offline_convert()
        create_user_log()
        create_attendance_count()
        create_program_setup()


if __name__ == "__main__":
    # check_screen()
    app = DCLMCounter()
    app.create_local_db()
    app.run()

# BB868980

"""
Valid properties of MDDropDown ['background_color', 'border_margin', 'caller', 'center', 'center_x', 'center_y', 
'children', 
'cls', 'device_ios', 'disabled', 'elevation', 'header_cls', 'height', 'hor_growth', 'ids', 'items', 'max_height', 
'motion_filter', 'opacity', 'opening_time', 'opening_transition', 'opposite_colors', 'parent', 'pos', 'pos_hint', 
'position', 'radius', 'right', 'size', 'size_hint', 'size_hint_max', 'size_hint_max_x', 'size_hint_max_y', 
'size_hint_min', 'size_hint_min_x', 'size_hint_min_y', 'size_hint_x', 'size_hint_y', 'theme_cls', 'top', 
'ver_growth', 'widget_style', 'width', 'width_mult', 'x', 'y']

Valid properties of MDDialog ['_anim_alpha', '_anim_duration', '_is_open', '_scale_x', '_scale_y', '_scroll_height', 
'_spacer_top', '_window', 'anchor_x', 'anchor_y', 'attach_to', 'auto_dismiss', 'background', 'background_color', 
'border', 'buttons', 'center', 'center_x', 'center_y', 'children', 'cls', 'content_cls', 'device_ios', 'disabled', 
'elevation', 'height', 'ids', 'items', 'md_bg_color', 'motion_filter', 'opacity', 'opposite_colors', 'overlay_color', 
'padding', 'parent', 'pos', 'pos_hint', 'radius', 'right', 'shadow_color', 'shadow_offset', 'shadow_radius', 
'shadow_softness', 'shadow_softness_size', 'size', 'size_hint', 'size_hint_max', 'size_hint_max_x', 
'size_hint_max_y', 'size_hint_min', 'size_hint_min_x', 'size_hint_min_y', 'size_hint_x', 'size_hint_y', 'text', 
'theme_cls', 'title', 'top', 'type', 'widget_pos', 'widget_style', 'width', 'width_offset', 'x', 'y']

"""
