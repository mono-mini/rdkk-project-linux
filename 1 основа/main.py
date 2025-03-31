#!/usr/bin/python
import os
import subprocess
import threading
import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import requests

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 12341))
        self.server_socket.listen(10)

    def start(self):
        client_socket, client_address = self.server_socket.accept()
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')

                # Check if the exit command is received
            if data == "exit":
                quit()  # Exit the loop if exit command is received

                # Write data to files
            with open("name.txt", "w") as file:
                file.write(data)

            start_server()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the client socket
            client_socket.close()

def start_server():
    try:
        # Check if the file "name.txt" exists
        with open("name.txt", "r") as file:
            c = file.read()
            b = c.split("|")
            print(b)
    except FileNotFoundError:
        # Start the server in a new thread if the file does not exist
        server_thread = threading.Thread(target=Server().start)
        server_thread.start()
        subprocess.run(["python", "name.py"])
        while True:
            try:
                with open("name.txt", "r") as file:
                    a = file.read()
                    if a:
                        b = a.split("|")
                        print(b)
                        break  # Exit the loop if data is read successfully
            except FileNotFoundError:
                pass

    os.chdir("./../2 основа")
    subprocess.run(["python", "main2.py"])

class Content(BoxLayout):
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.orientation = 'vertical'

class MainApp(App):
    def build(self):
        return Content()

if __name__ == "__main__":
    start_server()  # Ensure the server starts before the app
    app = MainApp()
    app.run()
