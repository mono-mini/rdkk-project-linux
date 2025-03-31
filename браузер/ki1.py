#!/usr/bin/env python
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.webview import WebView  # Убедитесь, что у вас установлен kivy_garden.xcamera

class Browser(BoxLayout):
    def __init__(self, **kwargs):
        super(Browser, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # URL bar
        self.url_bar = TextInput(size_hint_y=None, height=40)
        self.url_bar.bind(on_text_validate=self.navigate_to_url)

        # Home button
        self.home_button = Button(text='Home', size_hint_y=None, height=40)
        self.home_button.bind(on_press=self.navigate_home)

        # WebView
        self.browser = WebView(url='http://www.google.com')

        # Layout
        self.add_widget(self.url_bar)
        self.add_widget(self.home_button)
        self.add_widget(self.browser)

    def navigate_to_url(self, instance):
        url = self.url_bar.text
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.url = url

    def navigate_home(self, instance):
        self.browser.url = 'http://www.google.com'  # Устанавливаем домашнюю страницу

class BrowserApp(App):
    def build(self):
        return Browser()

if __name__ == '__main__':
    BrowserApp().run()