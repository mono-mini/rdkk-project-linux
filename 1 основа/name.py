#!/usr/bin/env python
import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock

class Container(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text='mena'))
        self.text1 = TextInput(multiline=False)
        self.add_widget(self.text1)

        self.add_widget(Label(text='zamen'))
        self.text2 = TextInput(multiline=False)
        self.add_widget(self.text2)

        self.add_widget(Label(text='vgo'))
        self.text3 = TextInput(multiline=False)
        self.add_widget(self.text3)

        self.add_widget(Button(text='>>>', on_press=self.submit))

    def submit(self, instance):
        # Start a new thread for sending data
        threading.Thread(target=self.send_data).start()

    def send_data(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 12341))  # Replace with your server's IP and port

            # Send data as a single message
            message = f"{self.text1.text}|{self.text2.text}|{self.text3.text}"
            client_socket.send(message.encode('utf-8'))

            # Schedule the success message to be shown on the main thread
            Clock.schedule_once(lambda dt: self.show_popup("Success", "Data sent successfully!"))

            # Clear input fields
            Clock.schedule_once(lambda dt: self.clear_inputs())

        except Exception as e:
            # Schedule the error message to be shown on the main thread
            Clock.schedule_once(lambda dt: self.show_popup("Error", str(e)))
        finally:
            client_socket.close()  # Close the socket after sending data

    def clear_inputs(self):
        self.text1.text = ''
        self.text2.text = ''
        self.text3.text = ''

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class MainApp(App):
    def build(self):
        return Container()

if __name__ == "__main__":
    MainApp().run()