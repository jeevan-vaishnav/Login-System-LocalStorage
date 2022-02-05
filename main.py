from ast import Try
from calendar import month
from gc import callbacks
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.pickers import MDDatePicker


class WelcomeScreen(Screen):
    pass


class UsernameScreen(Screen):
    pass


class DOBScreen(Screen):
    pass


class MainScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(UsernameScreen(name='usernamescreen'))
sm.add_widget(DOBScreen(name="dob"))
sm.add_widget(MainScreen(name='mainscreen'))


class NewApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Lime"
        return Builder.load_file('main.kv')

    # Cheking user function
    def check_username(self):
        self.username_text = self.root.get_screen(
            'usernamescreen').ids.username_text_filed.text

        username_check_false = True

        try:
            int(self.username_text)
        except:
            username_check_false: False

        if username_check_false == False or self.username_text.split() == []:

            cancel_btn_username_dialoge = MDFlatButton(
                text="Retry", on_release=self.close_username_dialog)
            self.dialog = MDDialog(
                title="Invalid Username", text="Please input a valid username ", size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialoge])
            self.dialog.open()
        else:
            # self.button_enable()
            self.root.get_screen(
                'usernamescreen').ids.disabled_button.disabled = False

    # Close the dial button

    def close_username_dialog(self, object):
        self.dialog.dismiss()

    def showDate_Picker(self):
        date_dialog = MDDatePicker(year=1999, month=1, day=1,)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_cancel(self, instance, value):
        self.root.get_screen("dob").ids.datepicker.text = f"Select Date"

    def on_save(self, instance, value, date_range):
        self.dob = value
        self.root.get_screen("dob").ids.datepicker.text = str(self.dob)
        self.root.get_screen('dob').ids.second_disbaled.disabled = False
        # String OF data
        self.store.put('userInfo', name=self.username_text, dob=str(self.dob))
        self.username_changer()

    def username_changer(self):

        self.root.get_screen(
            'mainscreen').ids.profile_Name.text = f"Welcome {self.store.get('userInfo')['name']}"

    def on_start(self):
        self.store = JsonStore('userprofile.json')
        try:
            if self.store.get('userInfo')['name'] != "":
                self.username_changer()
                self.root.get_screen(
                    'mainscreen').manager.current = "mainscreen"
        except KeyError:
            self.root.get_screen(
                'welcomescreen').manager.current = "welcomescreen"


NewApp().run()
