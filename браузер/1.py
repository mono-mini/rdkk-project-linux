#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl
from PyQt5 import QtGui

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("rdkk briz")
        self.setWindowIcon(QtGui.QIcon('icon.svg'))
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()

        # Создаем профиль для браузера, который будет хранить куки и данные сессии
        self.profile = QWebEngineProfile.defaultProfile()

        # Создание браузера с использованием профиля
        self.webpage = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.webpage)

        self.browser.setUrl(QUrl("http://www.google.com"))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Создание кнопки "Home"
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.navigate_home)

        # Создание горизонтального layout для кнопки и url_bar
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.home_button)
        h_layout.addWidget(self.url_bar)

        self.layout = QVBoxLayout()
        self.layout.addLayout(h_layout)  # Добавляем горизонтальный layout
        self.layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))  # Устанавливаем домашнюю страницу

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())