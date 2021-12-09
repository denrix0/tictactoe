import socket
import json
import sys

class Client:
    def __init__(self) -> None:
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.soc = socket.socket()
        host = sys.argv[1] if sys.argv[1] else 'localhost'
        port = 5555
        print('Waiting for connection response')
        try:
            self.soc.connect((host, port))
        except socket.error as e:
            print(str(e))

    def send_update(self, pos):
        self.soc.send(str.encode(json.dumps(pos)))
        self.soc.recv(1024)

    def periodic_update(self):
        self.soc.send('hi'.encode())
        res = self.soc.recv(1024).decode('utf-8')
        print(res)
        try:
            res = json.loads(res)
            return res
        except ValueError:
            pass
            

import tkinter

tk = tkinter.Tk()
client = Client()

board = client.board


tk.title("GAME")
tk.geometry("110x150")
tk.resizable(0, 0)

btns = []
btn_labels = [tkinter.StringVar() for i in range(9)]

def b_clicked(btn):
    client.send_update(btn_labels.index(btn))

def p_update():
    sym = client.periodic_update()
    if (sym is not None):
        for i in range(9):
            btn_labels[i].set(sym['board'][i])
        txt.set(sym['status'])
    tk.after(1000, p_update)

row = 0
col = 0
for i in range(9):
        if col==3: row += 1
        if i in (3, 6): col = 0 
        btns.append(tkinter.Button(tk, bg='white', fg='black', height=2, width=4, textvariable=btn_labels[i]))
        btns[i].config(command=lambda btn=btn_labels[i]: b_clicked(btn))
        btns[i].grid(row=row, column=col)
        col += 1

txt = tkinter.StringVar()

txt.set('')

tkinter.Label(textvariable=txt).grid(row=4, columnspan=3)

tk.after(50, p_update)

tk.mainloop()