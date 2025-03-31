#!/usr/bin/env python
import subprocess
import tkinter as tk
from tkinter import messagebox, Button, Entry
import os
import socket
import requests

path = "./../rdkkplay.client/скачаное"


class MyScrollApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("tas")
        self.root.geometry("400x300")

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.root, yscrollcommand=scrollbar.set)
        self.listbox.pack(fill="both", expand=True)

        scrollbar.config(command=self.listbox.yview)

        # Adding items from the specified directory to the list
        self.populate_listbox()

        # Binding the selection event
        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)

        # Start the periodic refresh
        self.refresh_listbox()

        self.root.mainloop()

    def populate_listbox(self):
        # Clear the current listbox
        self.listbox.delete(0, tk.END)
        try:
            # List all files in the specified directory
            files = os.listdir(path)
            for file in files:
                self.listbox.insert(tk.END, file)
            self.listbox.insert(tk.END, "toma")
            self.listbox.insert(tk.END, "kolcula")
            self.listbox.insert(tk.END, "mefa")
            self.listbox.insert(tk.END, "briz")
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Directory not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_listbox(self):
        self.populate_listbox()
        # Schedule the next refresh after 5000 milliseconds (5 seconds)
        self.root.after(5000, self.refresh_listbox)

    def on_item_select(self, event):
        # Get the index of the selected item
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)

            # Check if the selected item is "toma"
            if selected_item == "toma":
                self.run_script()
            elif selected_item == "kolcula":
                self.open_kolcula_window()
            elif selected_item == "mefa":
                self.open_mefa_window()
            elif selected_item == "briz":
                os.chdir("./../браузер")
                subprocess.Popen(["python", "1.py"])
            else:
                if selected_item.endswith(".py"):
                    subprocess.Popen(["python", os.path.join(path, selected_item)])
                elif selected_item.endswith(".cpp"):
                    subprocess.Popen(
                        [
                            "g++",
                            os.path.join(path, selected_item),
                            "-o",
                            os.path.splitext(selected_item)[0],
                        ]
                    )
                elif selected_item.endswith(".js"):
                    subprocess.Popen(["node", os.path.join(path, selected_item)])
                elif selected_item.endswith(".java"):
                    subprocess.Popen(["javac", os.path.join(path, selected_item)])
                elif selected_item.endswith(".exe"):
                    subprocess.Popen(["wine", os.path.join(path, selected_item)])
                elif selected_item.endswith(".c"):
                    subprocess.Popen(
                        [
                            "gcc",
                            os.path.join(path, selected_item),
                            "-o",
                            os.path.splitext(selected_item)[0],
                        ]
                    )
                elif selected_item.endswith(".html", ".htm"):
                    try:
                        subprocess.Popen(["firefox", os.path.join(path, selected_item)])
                    except FileNotFoundError:
                        try:
                            subprocess.Popen(
                                ["google-chrome", os.path.join(path, selected_item)]
                            )
                        except FileNotFoundError:
                            try:
                                subprocess.Popen(
                                    ["opera", os.path.join(path, selected_item)]
                                )
                            except FileNotFoundError:
                                messagebox.showerror("Error", "No web browser found.")

    def run_script(self):
        try:
            os.chdir("./../rdkkplay.client")
            subprocess.Popen(["python", "2.py"])
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Directory or file not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_mefa_window(self):
        os.chdir("./../проводник")
        subprocess.Popen(["python", "проводник.py"])

    def open_kolcula_window(self):
        kolcula_window = tk.Toplevel(self.root)
        kolcula_window.title("kolcula")
        kolcula_window.geometry("300x400")

        self.entry = Entry(
            kolcula_window,
            width=16,
            font=("Arial", 24),
            bd=5,
            insertwidth=4,
            bg="powder blue",
            justify="right",
        )
        self.entry.grid(row=0, column=0, columnspan=4)

        # Button layout
        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            "C",
            "=",
            "+",
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            Button(
                kolcula_window,
                text=button,
                padx=20,
                pady=20,
                font=("Arial", 18),
                command=lambda b=button: self.on_button_click(b),
            ).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_button_click(self, char):
        if char == "C":
            self.entry.delete(0, tk.END)
        elif char == "=":
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                messagebox.showerror("Error", "Invalid Input")
                self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, char)

MyScrollApp()
