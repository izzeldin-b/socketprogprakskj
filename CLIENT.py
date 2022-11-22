import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from datetime import datetime
port = 1234
host = '127.0.0.1'

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.title('Group 1 - Messenger')
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "What is your name?", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title('Group 1 - Messenger')
        self.win.configure(bg="ivory2")

        self.chat_label = tkinter.Label(self.win, text="Messenger", bg="ivory2", foreground='cornsilk4')
        self.chat_label.config(font=("Arial bold", 20))
        self.chat_label.pack(padx=20, pady=10, anchor='w')

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, borderwidth=0)
        self.text_area.pack(padx=20, pady=0)
        self.text_area.config(state='disabled')

        self.input_area = tkinter.Text(self.win, height=2, width=60, borderwidth=0)
        self.input_area.pack(padx=20, pady=10, anchor='w')

        self.send_button = tkinter.Button(self.win, text="SEND", command=self.write, borderwidth=0, bg='cornsilk3', foreground='white', width=8, height=1)
        self.send_button.config(font=("Arial bold", 16))
        self.send_button.pack(padx=20, pady=10, anchor='w')     

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.text_area.config(state='normal')
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self.text_area.insert('end', "["+current_time+"] ""You: "+self.input_area.get('1.0', 'end'))
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send((self.nickname.encode('utf-8')))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        now = datetime.now()
                        current_time = now.strftime("%H:%M")
                        self.text_area.insert('end', "["+current_time+"] "+message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(host, port)
