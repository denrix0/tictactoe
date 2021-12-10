from twisted.internet import reactor, tksupport
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

import json
import tkinter

class Client(Protocol):
    def __init__(self):
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        tk = tkinter.Tk()
        self.tk_interface = TkInterface(tk, self.board, self.send_data)
        tksupport.install(tk)

    def dataReceived(self, data):
        data = json.loads(data.decode())
        self.tk_interface.p_update(data)

    def send_data(self, data):
        self.transport.write(str(data).encode())

class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return Client()

class TkInterface:
    def __init__(self, tk, board, board_update):
        self.tk = tk
        self.board = board
        self.tk.title("GAME")
        self.tk.geometry("110x150")
        self.tk.resizable(0, 0)
        self.btns = []
        self.board_update = board_update
        self.main()

    def b_clicked(self, btn):
        self.board_update(self.btn_labels.index(btn))

    def p_update(self, pkg):
        if (pkg is not None):
            for i in range(9):
                self.btn_labels[i].set(pkg['board'][i])
            self.txt.set(pkg['status'])

    def main(self):
        self.btn_labels = [tkinter.StringVar() for i in range(9)]

        row = 0
        col = 0

        for i in range(9):
                if col==3: row += 1
                if i in (3, 6): col = 0 
                self.btns.append(tkinter.Button(self.tk, bg='white', fg='black', height=2, width=4, textvariable=self.btn_labels[i]))
                self.btns[i].config(command=lambda btn=self.btn_labels[i]: self.b_clicked(btn))
                self.btns[i].grid(row=row, column=col)
                col += 1

        self.txt = tkinter.StringVar()
        self.txt.set('')

        tkinter.Label(textvariable=self.txt).grid(row=4, columnspan=3)


if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 2000)
    endpoint.connect(ClientFactory())
    reactor.run()