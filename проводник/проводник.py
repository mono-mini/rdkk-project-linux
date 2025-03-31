#!/usr/bin/env python

import os
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, Frame, messagebox, Button, Label, Entry, Text
from PIL import Image, ImageTk
import pygame
import vlc
import zipfile
import tarfile
import threading
import subprocess
import shutil  # Импортируем shutil для перемещения файлов

def play_image(image_path):
    try:
        image = Image.open(image_path)
        image.show()
    except Exception as e:
        messagebox.showerror("Ошибка отображения изображения", str(e))

def play_sound(sound_file):
    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
    except Exception as e:
        messagebox.showerror("Ошибка воспроизведения", str(e))
    finally:
        pygame.mixer.quit()

def play_video(video_path):
    try:
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(video_path)
        player.set_media(media)
        player.play()

        video_window = tk.Toplevel()
        video_window.title("Видеоплеер")
        width, height = 800, 600
        video_window.geometry(f"{width}x{height}")

        def update():
            if player.get_state() in [vlc.State.Ended, vlc.State.Error]:
                video_window.destroy()
            else:
                video_window.after(100, update)

        update()
        video_window.protocol("WM_DELETE_WINDOW", lambda: player.stop() or video_window.destroy())

    except Exception as e:
        messagebox.showerror("Ошибка воспроизведения видео", str(e))

def play_text(text_file):
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.read()
        messagebox.showinfo("Текстовый файл", text)
    except Exception as e:
        messagebox.showerror("Ошибка отображения текстового файла", str(e))

def edit_text_file(text_file):
    def save_file():
        try:
            with open(text_file, 'w', encoding='utf-8') as file:
                file.write(text_area.get("1.0", tk.END))
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка сохранения файла", str(e))

    edit_window = tk.Toplevel()
    edit_window.title("Редактирование текстового файла")

    text_area = Text(edit_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH)

    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.read()
            text_area.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Ошибка открытия файла", str(e))

    save_button = Button(edit_window, text="Сохранить", command=save_file)
    save_button.pack()

def extract_archive(archive_path):
    try:
        extract_path = os.path.join(os.path.dirname(archive_path), "extracted")
        os.makedirs(extract_path, exist_ok=True)

        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
        elif archive_path.endswith('.tar'):
            with tarfile.open(archive_path, 'r') as tar_ref:
                tar_ref.extractall(extract_path)

        messagebox.showinfo("Архив", f"Архив извлечен в: {extract_path}")
    except Exception as e:
        messagebox.showerror("Ошибка извлечения архива", str(e))

def view_archive_contents(archive_path):
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                contents = zip_ref.namelist()
        elif archive_path.endswith('.tar'):
            with tarfile.open(archive_path, 'r') as tar_ref:
                contents = tar_ref.getnames()
        else:
            messagebox.showerror("Ошибка", "Неподдерживаемый формат архива.")
            return

        contents_window = tk.Toplevel()
        contents_window.title("Содержимое архива")
        listbox = Listbox(contents_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        for item in contents:
            listbox.insert(tk.END, item)

    except Exception as e:
        messagebox.showerror("Ошибка просмотра архива", str(e))

def play_ispolnitelnyy(ispolnitelnyy_path):
    try:
        subprocess.Popen(ispolnitelnyy_path, check=True)
    except Exception as e:
        messagebox.showerror("Ошибка запуска исполняемого файла", str(e))

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Проводник")

        self.frame = Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = Label(self.frame, text="Содержимое директории:")
        self.label.pack()

        self.listbox = Listbox(self.frame, selectmode=tk.MULTIPLE)  # Allow multiple selection
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<Double-Button-1>', self.open_item)

        self.history = []
        self.load_directory(os.path.expanduser("~"))

        self.root.bind('<Control-o>', self.open_directory)

        self.search_entry = Entry(self.root)
        self.search_entry.pack(side=tk.TOP, fill=tk.X)
        self.search_entry.bind('<Return>', self.search_files)

        self.search_button = Button(self.root, text="Поиск", command=self.search_files)
        self.search_button.pack(side=tk.TOP)

        self.back_button = Button(self.root, text="Назад", command=self.go_back)
        self.back_button.pack(side=tk.LEFT)

        self.delete_button = Button(self.root, text="Удалить", command=self.delete_file)
        self.delete_button.pack(side=tk.LEFT)

        self.edit_properties_button = Button(self.root, text="Свойства", command=self.edit_file_properties)
        self.edit_properties_button.pack(side=tk.LEFT)

        self.create_text_file_button = Button(self.root, text="Создать текстовый файл", command=self.create_text_file)
        self.create_text_file_button.pack(side=tk.LEFT)

        self.create_archive_button = Button(self.root, text="Создать архив", command=self.create_archive)
        self.create_archive_button.pack(side=tk.LEFT)

        self.extract_button = Button(self.root, text="Распаковать", command=self.extract_selected_archive)
        self.extract_button.pack(side=tk.LEFT)

        self.move_button = Button(self.root, text="Переместить", command=self.move_file)
        self.move_button.pack(side=tk.LEFT)

    def move_file(self):
            selected_indices = self.listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Предупреждение", "Выберите файлы для перемещения.")
                return

            destination_directory = filedialog.askdirectory(title="Выберите папку назначения")
            if not destination_directory:
                return

            for index in selected_indices:
                selected_item = self.listbox.get(index)
                full_path = os.path.join(self.current_path, selected_item)

                try:
                    shutil.move(full_path, destination_directory)
                    messagebox.showinfo("Успех", f"Файл '{selected_item}' перемещен в '{destination_directory}'.")
                except Exception as e:
                    messagebox.showerror("Ошибка перемещения файла", str(e))

            self.load_directory(self.current_path)  # Обновляем список файлов


    def load_directory(self, path):
        self.listbox.delete(0, tk.END)
        try:
            if self.history and self.history[-1] != path:
                self.history.append(path)
            elif not self.history:
                self.history.append(path)

            for item in os.listdir(path):
                self.listbox.insert(tk.END, item)
            self.current_path = path
            self.label.config(text=f"Содержимое директории: {path}")
        except PermissionError:
            messagebox.showerror("Ошибка", "Нет доступа к этой папке.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Папка не найдена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def create_text_file(self):
        def save_new_file():
            new_file_name = new_file_entry.get()
            if not new_file_name.endswith('.txt'):
                new_file_name += '.txt'
            new_file_path = os.path.join(self.current_path, new_file_name)
            try:
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write("")  # Создаем пустой файл
                messagebox.showinfo("Успех", f"Файл '{new_file_name}' создан.")
                new_file_window.destroy()
                self.load_directory(self.current_path)  # Обновляем список файлов
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        new_file_window = tk.Toplevel(self.root)
        new_file_window.title("Создание текстового файла")

        Label(new_file_window, text="Введите имя файла:").pack()
        new_file_entry = Entry(new_file_window)
        new_file_entry.pack()

        save_button = Button(new_file_window, text="Создать", command=save_new_file)
        save_button.pack()

    def create_archive(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Предупреждение", "Выберите файлы для архивации.")
            return

        archive_name = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip"), ("TAR files", "*.tar")])
        if not archive_name:
            return

        try:
            if archive_name.endswith('.zip'):
                with zipfile.ZipFile(archive_name, 'w') as zipf:
                    for index in selected_indices:
                        file_name = self.listbox.get(index)
                        full_path = os.path.join(self.current_path, file_name)
                        zipf.write(full_path, arcname=file_name)
                messagebox.showinfo("Успех", f"Архив '{archive_name}' создан.")
            elif archive_name.endswith('.tar'):
                with tarfile.open(archive_name, 'w') as tarf:
                    for index in selected_indices:
                        file_name = self.listbox.get(index)
                        full_path = os.path.join(self.current_path, file_name)
                        tarf.add(full_path, arcname=file_name)
                messagebox.showinfo("Успех", f"Архив '{archive_name}' создан.")
            else:
                messagebox.showerror("Ошибка", "Неподдерживаемый формат архива.")
        except Exception as e:
            messagebox.showerror("Ошибка создания архива", str(e))

    def extract_selected_archive(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Предупреждение", "Выберите архив для распаковки.")
            return

        for index in selected_indices:
            selected_item = self.listbox.get(index)
            full_path = os.path.join(self.current_path, selected_item)

            if full_path.endswith(('.zip', '.tar')):
                extract_archive(full_path)

    def edit_file_properties(self):
        try:
            selected_indices = self.listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Предупреждение", "Выберите файл для редактирования свойств.")
                return

            selected_item = self.listbox.get(selected_indices[0])
            full_path = os.path.join(self.current_path, selected_item)

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Изменение свойств файла")

            Label(edit_window, text="Имя файла:").pack()
            name_entry = Entry(edit_window)
            name_entry.pack()
            name_entry.insert(0, selected_item)

            Label(edit_window, text="Расширение файла:").pack()
            extension_entry = Entry(edit_window)
            extension_entry.pack()
            extension_entry.insert(0, os.path.splitext(selected_item)[1][1:])  # Убираем точку

            Label(edit_window, text="Полный путь:").pack()
            full_path_label = Label(edit_window, text=full_path)
            full_path_label.pack()

            Label(edit_window, text="Размер файла в байтах:").pack()
            size_label = Label(edit_window, text=os.path.getsize(full_path))
            size_label.pack()

            Label(edit_window, text="Дата изменения файла:").pack()
            modified_label = Label(edit_window, text=os.path.getmtime(full_path))
            modified_label.pack()

            Label(edit_window, text="Атрибуты файла:").pack()
            attributes_label = Label(edit_window, text=os.stat(full_path).st_mode)
            attributes_label.pack()

            Label(edit_window, text="Тип файла:").pack()
            type_label = Label(edit_window, text=os.path.isfile(full_path))
            type_label.pack()

            def save_changes():
                new_name = name_entry.get()
                new_extension = extension_entry.get()
                new_full_path = os.path.join(self.current_path, new_name + ('.' + new_extension if new_extension else ''))

                if os.path.exists(new_full_path):
                    messagebox.showerror("Ошибка", "Файл с таким именем уже существует.")
                    return

                os.rename(full_path, new_full_path)
                edit_window.destroy()
                self.load_directory(self.current_path)

            save_button = Button(edit_window, text="Сохранить", command=save_changes)
            save_button.pack()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def open_item(self, event):
        selected_indices = self.listbox.curselection()
        for index in selected_indices:
            selected_item = self.listbox.get(index)
            full_path = os.path.join(self.current_path, selected_item)

            if os.path.isdir(full_path):
                self.load_directory(full_path)
            else:
                try:
                    if full_path.endswith(('.wav', '.mp3')):
                        threading.Thread(target=play_sound, args=(full_path,)).start()
                    elif full_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        self.show_image(full_path)
                    elif full_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                        threading.Thread(target=play_video, args=(full_path,)).start()
                    elif full_path.lower().endswith('.txt'):
                        edit_text_file(full_path)  # Открываем файл для редактирования
                    elif full_path.lower().endswith(('.zip', '.tar')):  # Архивы
                        view_archive_contents(full_path)  # Просмотр содержимого архива
                    elif full_path.lower().endswith(('.py')):
                        subprocess.Popen(['python', full_path])
                    elif full_path.lower().endswith(('.cpp')):
                        subprocess.Popen(['g++', full_path])  # Исправлено на g++
                    elif full_path.lower().endswith(('.c')):
                        subprocess.Popen(['gcc', full_path])
                    elif full_path.lower().endswith(('.java')):
                        subprocess.Popen(['java', full_path])
                    elif full_path.lower().endswith(('.html', '.htm')):
                        try:
                            subprocess.Popen(['firefox', full_path])
                        except Exception:
                            try:
                                subprocess.Popen(['google-chrome', full_path])
                            except Exception:
                                pass
                    elif full_path.lower().endswith(('.pdf')):
                        subprocess.Popen(['evince', full_path])
                    elif full_path.lower().endswith(('.doc', '.docx')):
                        subprocess.Popen(['libreoffice', full_path])
                    elif full_path.lower().endswith(('.xls', '.xlsx')):
                        subprocess.Popen(['libreoffice', full_path])
                    elif full_path.lower().endswith(('.js')):
                        subprocess.Popen(['node', full_path])
                    elif full_path.lower().endswith(('.tmp', '.log')):
                        pass
                    elif full_path.lower().endswith(('.exe')):
                        try:
                            subprocess.Popen(['wine', full_path])
                        except Exception:
                            pass
                    else:
                        pass
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

    def show_image(self, image_path):
        image_window = tk.Toplevel(self.root)
        image_window.title("Изображение")

        img = Image.open(image_path)
        img.thumbnail((600, 300))
        photo = ImageTk.PhotoImage(img)

        label = Label(image_window, image=photo)
        label.image = photo
        label.pack()

        close_button = Button(image_window, text="Закрыть", command=image_window.destroy)
        close_button.pack()

    def open_directory(self, event=None):
        directory = filedialog.askdirectory()
        if directory:
            self.load_directory(directory)

    def go_back(self, event=None):
        if len(self.history) > 1:
            self.history.pop()
            previous_path = self.history[-1]
            self.load_directory(previous_path)

    def search_files(self, event=None):
        query = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        if query:
            try:
                for item in os.listdir(self.current_path):
                    if query in item.lower():
                        self.listbox.insert(tk.END, item)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def delete_file(self):
        try:
            selected_indices = self.listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Предупреждение", "Выберите файл для удаления.")
                return

            for index in selected_indices:
                selected_item = self.listbox.get(index)
                full_path = os.path.join(self.current_path, selected_item)

                if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить '{selected_item}'?"):
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                    else:
                        messagebox.showerror("Ошибка", "Выбранный элемент не является файлом.")
            self.load_directory(self.current_path)  # Обновляем список файлов
        except Exception as e:
            messagebox.showerror("Ошибка удаления", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    explorer = FileExplorer(root)
    root.mainloop()
