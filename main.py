from tkinter import *
import socket as skt
import threading
from Chat_room import *
from tkinter.ttk import *
from ttkthemes import themed_tk 
from PIL import Image, ImageTk

def connect():
    gui_obj = chat_room()
    username_str, port_int, server_type = username.get(), int(port.get()), var1.get()
    root1.destroy()
    gui_obj.connect(username_str, port_int, server_type)
    
root1 = themed_tk.ThemedTk(theme="radiance")
root1.geometry("400x300")
root1.config(bg = "#e6e6e6")

Label(root1, text = " USERNAME: ").place(x = 80, y = 32)
username = Entry(root1)
username.place(x = 180, y = 30)

Label(root1, text = "PORT:").place(x = 130, y = 82)
port = Entry(root1)
port.place(x = 180, y = 80)

var1 = IntVar()

single = Radiobutton(root1, text = "PRIVATE", variable = var1, value = 1)
single.place(x = 80, y = 120)

multiple = Radiobutton(root1, text = "MULTIPLE", variable = var1, value = 2)
multiple.place(x = 180, y = 120)

photo = PhotoImage(file = r"Resources\\connect.png")
photoimage = photo.subsample(2,3)

connect_btn = Button(root1, text = ' CONNECT ', image = photoimage,compound = LEFT, command = connect)
connect_btn.place(x = 90, y = 160) 

root1.resizable(0, 0)
root1.mainloop()