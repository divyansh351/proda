import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 5000


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        msg = tkinter.Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring(
            "Nickname", "Please Choose a Nickname", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(
            self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Monaco", 8))
        self.chat_label.pack(padx=10, pady=3)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(state="disabled", font=("Monaco", 11))
        self.text_area.pack(padx=10, pady=3)

        self.msg_label = tkinter.Label(
            self.win, text="Message: ", bg="lightgray")
        self.msg_label.config(font=("Monaco", 8))
        self.msg_label.pack(padx=10, pady=3)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.config(font=("Monaco", 11))
        self.input_area.pack(padx=10, pady=3)

        self.send_button = tkinter.Button(
            self.win, text="Send", command=self.write)
        self.send_button.config(font=("Monaco", 8))
        self.send_button.pack(padx=10, pady=3)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


client = Client(HOST, PORT)
