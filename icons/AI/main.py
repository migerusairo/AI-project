import datetime

import pyttsx3
import speech_recognition as sr
from firebase import firebase
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar

# ----------------------------------------------------------------------------------------------------------------------

Window.size = (325, 670)
Window.radius = [30, 30, 30, 30]
# ----------------------------------------------------------------------------------------------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('pitch', 100)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# ----------------------------------------------------------------------------------------------------------------------
class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 14


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 14


class TCUAdvisor(MDApp):
    def build(self):

        global screen
        screen = ScreenManager(transition=SlideTransition(duration=.8))
        screen.add_widget(Builder.load_file("Introduction.kv"))
        screen.add_widget(Builder.load_file("Introduction1.kv"))
        screen.add_widget(Builder.load_file("Login.kv"))
        screen.add_widget(Builder.load_file("Register.kv"))
        screen.add_widget(Builder.load_file("Admin.kv"))
        screen.add_widget(Builder.load_file("Admin-screen.kv"))
        screen.add_widget(Builder.load_file("Welcome-screen.kv"))
        screen.add_widget(Builder.load_file("Home-screen.kv"))
        screen.add_widget(Builder.load_file("Message-screen.kv"))
        screen.add_widget(Builder.load_file("Notification-screen.kv"))
        screen.add_widget(Builder.load_file("About.kv"))
        screen.add_widget(Builder.load_file("Profile-screen.kv"))
        return screen

    def profile(self):
        button = MDIconButton(icon="assets/TCUlogo.jpg")
        layout = BoxLayout(orientation='vertical', pos_hint={"center_x": .93, "center_y": .51})
        layout.add_widget(button)

        screen.get_screen('Home-screen').add_widget(layout)

    # ----------------------------------------------------------------------------------------------------------------------
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def response(self, *args):

        firebase_app = firebase.FirebaseApplication('https://test-e079c-default-rtdb.firebaseio.com/', None)
        botresponse = firebase_app.get('aidb-72811-default-rtdb/bot_response', '')

        for x in botresponse.keys():
            if botresponse[x]['Command'] == command:
                response = botresponse[x]['Response']
                screen.get_screen('Message-screen').chat_list.add_widget(Response(text=response, size_hint_x=.75))
                self.speak(response)

    def send(self):
        global size, halign, command
        if screen.get_screen('Message-screen').text_input != "":
            command = screen.get_screen('Message-screen').text_input.text
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))
            Clock.schedule_once(self.response, 1)
            screen.get_screen('Message-screen').text_input.text = ""

    def take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))
            Clock.schedule_once(self.response, 1)
            screen.get_screen('Message-screen').text_input.text = ""

        except Exception as e:
            print(e)
            screen.get_screen('Message-screen').chat_list.add_widget(
                Command(text="I didnt understand", size_hint_x=size, halign=halign))
            return "None"
        return command

    def add_new_response(self, command, new_response):
        if any(field == "" for field in [command, new_response]):
            Snackbar(text="Please fill out all fields!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
        else:
            firebase_app = firebase.FirebaseApplication('https://test-e079c-default-rtdb.firebaseio.com/', None)
            data = {
                'Command': command,
                'Response': new_response
            }
            result = firebase_app.post('aidb-72811-default-rtdb/bot_response', data)

            self.clear_admin_fields()

            Snackbar(text="Updated Successfully!",
                     font_size='12sp',
                     snackbar_x="10dp",
                     snackbar_y="10dp",
                     pos_hint={'center_x': 0.5, 'center_y': 0.9},
                     radius=[15, 15, 15, 15],
                     size_hint_x=(Window.width - (dp(75) * 2)) / Window.width,
                     bg_color=(0, 255, 0, 1),
                     ).open()

    def register(self, name, stud_id, yr_course, section, password):
        if any(field == "" for field in [name, stud_id, yr_course, section, password]):
            Snackbar(text="Please fill out all fields!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
        else:
            firebase_app = firebase.FirebaseApplication('https://test-e079c-default-rtdb.firebaseio.com/', None)
            data = {
                'Name': name,
                'Student ID': stud_id,
                'Year & Course': yr_course,
                'Section': section,
                'Password': password
            }

            result = firebase_app.post('aidb-72811-default-rtdb/User', data)

            self.clear_registration_fields()
            self.speak("Registered successfully!, please Log In your Account!")
            self.root.current = 'Login'

    # Clearing Inputs-------------------------------------------------------------------------------------------------------
    def clear_admin_fields(self):
        screen = self.root.get_screen('Admin-screen')
        screen.ids.command.text = ""
        screen.ids.new_response.text = ""

    def clear_registration_fields(self):
        screen = self.root.get_screen('Register')
        screen.ids.name.text = ""
        screen.ids.stud_id.text = ""
        screen.ids.yr_course.text = ""
        screen.ids.section.text = ""
        screen.ids.password.text = ""

    def clear_admin_login_fields(self):
        screen = self.root.get_screen('Admin')
        screen.ids.admin_id.text = ""
        screen.ids.admin_password.text = ""

    def clear_user_login_fields(self, ):
        screen = self.root.get_screen('Login')
        screen.ids.stud_id.text = ""
        screen.ids.password.text = ""

    # Admin & User Login----------------------------------------------------------------------------------------------------

    def user_login(self, stud_id, password):
        if not stud_id:
            self.speak("Please enter your Student ID!")
            return
        if not password:
            self.speak("Please enter your Password!")
            return

        firebase_app = firebase.FirebaseApplication('https://test-e079c-default-rtdb.firebaseio.com/', None)
        result = firebase_app.get('aidb-72811-default-rtdb/User', '')

        for i in result.keys():
            if result[i]['Student ID'] == stud_id:
                if result[i]['Password'] == password:

                    self.speak("Logged In successfully!")
                    self.clear_user_login_fields()
                    self.root.current = 'Welcome-screen'

                    print(result[i]['Name'])
                    print(result[i]['Student ID'])
                    print(result[i]['Section'])
                    print(result[i]['Year & Course'])

                    return

        for i in result.keys():
            if result[i]['Student ID'] != stud_id:
                if result[i]['Password'] != password:
                    self.speak("Invalid Student ID or Password!")
                    return

        for i in result.keys():
            if result[i]['Student ID'] == stud_id:
                if result[i]['Password'] != password:
                    self.speak("Invalid Student ID or Password!")
                    return

        for i in result.keys():
            if result[i]['Student ID'] != stud_id:
                if result[i]['Password'] == password:
                    self.speak("Invalid Student ID or Password!")
                    return

    def admin_login(self, admin_id, admin_password):
        if not admin_id:
            self.speak("Please input your Admin ID!")
            return

        if not admin_password:
            self.speak("Please input your Admin Password!")
            return

        firebase_app = firebase.FirebaseApplication('https://test-e079c-default-rtdb.firebaseio.com/', None)
        result = firebase_app.get('aidb-72811-default-rtdb/Admin', '')

        for i in result.keys():
            if result[i]['Admin ID'] == admin_id:
                if result[i]['Admin Password'] == admin_password:
                    self.speak("Admin Logged In Successfully!")

                    self.clear_admin_login_fields()
                    self.root.current = 'Admin-screen'
                    return

        for i in result.keys():
            if result[i]['Admin ID'] != admin_id:
                if result[i]['Admin Password'] != admin_password:
                    self.speak("Invalid Admin ID or Password!")
                    return

    def forgot_password(self):
        self.speak("Contact admin to retrieve your account")

    # Admin & User Logout---------------------------------------------------------------------------------------------------

    def user_logout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()
        self.root.current = 'Login'

    def admin_logout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()
        self.root.current = 'Admin'

    # other functions-------------------------------------------------------------------------------------------------------
    def wish_sign_in(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning!, Welcome to T C U Artificial Intelligence. Please Sign in your Account.")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!, Welcome to T C U Artificial Intelligence. Please Sign in your Account.")
        else:
            self.speak("Good Evening!, Welcome to T C U Artificial Intelligence. Please Sign in your Account.")

    def on_touch(self, instance):
        pass

    def on_start(self):
        self.profile()
        Clock.schedule_once(self.start, 0)

    def start(self, *args):
        self.root.current = "Login"


if __name__ == "__main__":
    TCUAdvisor().run()
