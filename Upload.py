from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import themed_tk
import socket as skt
import time
import os

class Upload():
    def __init__(self, username):
        self.seperator = "<<SEPERATOR>>"
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.socket.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
        self.buffer_size = 1024
        self.server = "192.168.43.25"
        self.username = username
        self.port = 5555
        self.socket.connect((self.server, self.port))

    def send_username_filesize(self):
        for i in self.files_list:
            file_name = i.split("/")[-1]
            cur_dir = i.replace(f"/{file_name}", "")
            os.chdir(cur_dir)
            file_size = os.path.getsize(file_name)
            file_and_username = file_name + self.seperator + self.username + self.seperator + str(file_size) + self.seperator
            self.socket.send(file_and_username.encode())
            self.send_files(file_size, file_name)
    
    def send_files(self, file_size, file_name):
        with open(file_name, "rb") as f:
            for _ in range(file_size):
                bytes_read = f.read(self.buffer_size)
                total_sent = 0
                if not bytes_read:
                    break

                self.socket.sendall(bytes_read)
                total_sent += self.buffer_size
        if total_sent == file_size:
            print("True")
        messagebox.showinfo("Success", "Files sent Succesfully.")
        self.browse_window.destroy()
    
    def selected_file(self):
        self.files_list = []
        self.files_list += filedialog.askopenfilenames(initialdir = "/", title = "select files to send.")
        self.browse_btn.configure(text = "Send Files", command = self.send_username_filesize)

    def browse_files(self):
        self.browse_window = themed_tk.ThemedTk(theme="keramik",className=" BROWSE FILES")
        self.browse_window.geometry("200x100")
        self.browse_window.config(bg = "#000000")

        self.browse_btn = Button(self.browse_window, text = "Browse ",command = self.selected_file)
        self.browse_btn.place(x = 70, y = 20,height=50)

        self.browse_window.resizable(0, 0)
        self.browse_window.mainloop()

