from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from ttkthemes import themed_tk
from tkinter import ttk
from winsound import *
import winsound
import socket as skt
import threading
from Upload import *
from Download import *

class chat_room():
    def __init__(self):
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.socket.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
        self.server = '192.168.43.25'
        self.buffer_size = 4096

    def disconnect(self):
        winsound.Beep(2000, 300)
        response = messagebox.askyesnocancel("Disconnect", "Do You Want To Disconnect and Save the chat logs.")
        if response:
            chatlog = self.chatbox.get("1.0", END)
            if not os.path.isdir("Chat-Logs"):
                os.mkdir("Chat-Logs")
            chatlog_path = os.path.join("Chat-Logs", f"chatlog_{self.username}_{self.port}")
            chatlog_file = open(chatlog_path, "w")
            chatlog_file.write(chatlog)
            self.socket.send(f"\n{self.username} has been disconnected.\n".encode("utf-8"))
            self.socket.close()
        elif response == None:
            return
        else:
            self.socket.close()

    def initializing(self):
        self.address = (self.server, self.port)
        self.socket.connect(self.address)
        self.socket.send(self.username.encode("utf-8"))
        initial_msg = self.receive_msg()
        rcv = threading.Thread(target = self.update_chatbox)
        rcv.start()
        return initial_msg

    def update_chatbox(self):
        while True:
            try:
                msg = self.receive_msg()
                self.chatbox.configure(state = NORMAL)
                self.chatbox.insert(END, msg)
                self.chatbox.configure(state = DISABLED)
            except:
                self.disconnect()
                break

    def receive_msg(self):
        self.recvd_msg = self.socket.recv(self.buffer_size)
        return self.recvd_msg.decode("utf-8")
    
    def forward_msg_function(self, msg_to_send):
        self.msg_send = msg_to_send
        self.msg.delete(0, END)
        send = threading.Thread(target = self.send_message)
        send.start()

    def send_message(self):
        while True:
            message = (f"{self.username} :: {self.msg_send}")
            self.socket.send(message.encode("utf-8"))
            break
    
    def send_clicked(self):
        send_obj = Upload(self.username)
        send_obj.browse_files()
    
    def download_clicked(self):
        download_obj = Download()
        download_obj.download_form()
        
    def connect(self, username, port, server_type):
        self.username = username
        self.port = port
        self.server_type = server_type

        init_msg = self.initializing()

        root2 = themed_tk.ThemedTk(theme="itft1",className=' WINDOW')
        root2.geometry("500x500")
        root2.config(bg = "#ccefff")

        self.chatbox = Text(root2, width = 38, height = 27, state = DISABLED)
        self.chatbox.place(x = 10, y = 20)

        scollbar = Scrollbar(root2, orient = VERTICAL, command = self.chatbox.yview)
        scollbar.place(x = 305 , y = 20, height = 440)
        self.chatbox.config(yscrollcommand = scollbar.set)

        self.chatbox.configure(state = NORMAL)
        self.chatbox.insert(END, str(init_msg))
        self.chatbox.configure(state = DISABLED)
        
        self.msg = Entry(root2, width = 40)
        self.msg.place(x = 10, y = 460, height = 25)

        self.frwd = Button(root2, text = "SEND", command = lambda: self.forward_msg_function(self.msg.get()))
        self.frwd.place(x = 260, y = 460, width = 60)

        photo3 = PhotoImage(file = r"Resources\iupload.png")
        uplabel=Label(root2,image= photo3)
        uplabel.place(x=360,y=25)

        self.send = Button(root2, text = "UPLOAD", command = self.send_clicked)
        self.send.place(x = 350, y = 95, height = 40, width = 100)

        photo1 = PhotoImage(file = r"Resources\idownload.png")
        downlabel=Label(root2,image= photo1)
        downlabel.place(x=360,y=170)
        
        self.recieve = Button(root2, text = "DOWNLOAD", command = self.download_clicked)
        self.recieve.place(x = 350, y = 235, height = 40, width = 100)

        photo2=PhotoImage(file = r"Resources\disconnected.png")
        disconlabel=Label(root2,image=photo2)
        disconlabel.place(x=360,y=315)

        self.disconnect_btn = Button(root2, text = "DISCONNECT", command = self.disconnect)
        self.disconnect_btn.place(x = 350, y = 380, height = 40, width = 100)

        root2.resizable(0, 0)
        root2.mainloop()
