#!/usr/bin/env python
import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox, QLineEdit

class AppStore(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('toma')

        layout = QVBoxLayout()

        self.upload_button = QPushButton('Загрузить приложение или архив')
        self.upload_button.clicked.connect(self.upload_app_or_folder)
        layout.addWidget(self.upload_button)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Поиск приложений...')
        self.search_input.textChanged.connect(self.filter_apps)
        layout.addWidget(self.search_input)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.refresh_button = QPushButton('Обновить список приложений')
        self.refresh_button.clicked.connect(self.refresh_apps)
        layout.addWidget(self.refresh_button)

        self.download_button = QPushButton('Скачать приложение')
        self.download_button.clicked.connect(self.download_app)
        layout.addWidget(self.download_button)

        self.setLayout(layout)
        self.apps = []  # Инициализация списка приложений
        self.refresh_apps()

    def upload_app_or_folder(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите архив для загрузки", "", "Архивные файлы (*.zip *.tar *.tar.gz);;Все файлы (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'rb') as file:
                    # Загрузка архивного файла
                    response = requests.post('http://127.0.0.1:5001/upload', files={'file': (os.path.basename(file_name), file)})
                QMessageBox.information(self, 'Статус загрузки', response.json().get('message', 'Ошибка загрузки'))
                self.refresh_apps()  # Обновить список приложений после загрузки
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка загрузки', str(e))

    def refresh_apps(self):
        try:
            response = requests.get('http://127.0.0.1:5001/apps')
            if response.status_code == 200:
                self.list_widget.clear()
                self.apps = response.json()  # Сохранить список приложений
                self.list_widget.addItems(self.apps)
            else:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось получить список приложений')
        except Exception as e:
            QMessageBox.warning(self, 'Сетевая ошибка', str(e))

    def filter_apps(self):
        search_text = self.search_input.text().lower()
        filtered_apps = [app for app in self.apps if search_text in app.lower()]
        self.list_widget.clear()
        self.list_widget.addItems(filtered_apps)

    def download_app(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            filename = selected_item.text()
            try:
                response = requests.get(f'http://127.0.0.1:5001/download/{filename}')
                if response.status_code == 200:
                    downloads_folder = os.path.join(os.path.expanduser(""), "скачаное")  # Изменено на "Загрузки"
                    os.makedirs(downloads_folder, exist_ok=True)  # Создать директорию, если она не существует
                    file_path = os.path.join(downloads_folder, filename)

                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Статус загрузки', f'{filename} успешно загружен в {downloads_folder}')
                else:
                    QMessageBox.warning(self, 'Ошибка загрузки', 'Не удалось скачать файл')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка загрузки', str(e))
        else:
            QMessageBox.warning(self, 'Ошибка выбора', 'Пожалуйста, выберите файл для загрузки')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppStore()
    ex.show()
    sys.exit(app.exec_())
