from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from winsound import *
import winsound
import socket as skt
import time
import os

class Download():
    def __init__(self):
        self.seperator = "<<SEPERATOR>>"
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.socket.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
        self.buffer_size = 1024
        self.server = "192.168.43.25"
        self.port = 6666
        self.socket.connect((self.server, self.port))

    def downloading(self, dir_name, file_name):
        winsound.Beep(2000, 300)
        init_msg = dir_name + self.seperator + file_name
        self.socket.sendall(init_msg.encode())
        if not os.path.isdir("Downloads"):
            os.mkdir("Downloads")
        download_loc = os.path.join(os.getcwd(), "Downloads")
        download_loc = os.path.join(download_loc, file_name)
        with open(download_loc, "wb") as newfile: 
            while True:     
                bytes_recieved = self.socket.recv(self.buffer_size)
                if not bytes_recieved:
                    break
                newfile.write(bytes_recieved)

        self.form_win.destroy()

    def download_form(self):
        self.form_win = Tk(className = ' FORM')
        self.form_win.geometry("400x200")
        self.form_win.config(bg = '#295f2d')

        Label(self.form_win, text = "DIRECTORY NAME:", font = ('Times'), background = '#295f2d', foreground = '#ffe67c').place(x=30,y=30)
        dir_entry = Entry(self.form_win)
        dir_entry.place(x = 215, y = 33)

        Label(self.form_win, text = "FILE NAME:",font = ('Times'), background = '#295f2d', foreground = '#ffe67c').place(x = 100, y =70)
        file_name_entry = Entry(self.form_win)
        file_name_entry.place(x = 215, y = 73)

        #photo = PhotoImage(file = r"Resources\img.png")
       #photoimage = photo.subsample(2,2)

        style = Style()
        style.configure("My.TButton",  font = 'Montserrat', background = '#ffe67c', foreground = '#295f2d')

        down_btn = Button(self.form_win, text = "DOWNLOAD", style = "My.TButton", compound = TOP, command = lambda : self.downloading(dir_entry.get(), file_name_entry.get()))
        down_btn.place(x = 130, y = 120, height = 62)

        self.form_win.resizable(0, 0)
        self.form_win.mainloop()
