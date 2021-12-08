import socket
import os
from _thread import *

class Board:
    def __init__(self) -> None:
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

    def set_board_box(self, sym, pos):
        self.board[pos[0], pos[1]] = sym

    def win_check(self):
        b = self.board
        for sym in ['X', 'Y']:
            return (
                (b[0][0] == sym and b[0][1] == sym and b[0][2] == sym) or
                (b[1][0] == sym and b[1][1] == sym and b[1][2] == sym) or
                (b[2][0] == sym and b[2][1] == sym and b[2][2] == sym) or
                (b[0][0] == sym and b[1][0] == sym and b[2][0] == sym) or
                (b[0][1] == sym and b[1][1] == sym and b[2][1] == sym) or
                (b[0][2] == sym and b[1][2] == sym and b[2][2] == sym) or
                (b[0][0] == sym and b[1][1] == sym and b[2][2] == sym) or
                (b[0][2] == sym and b[1][1] == sym and b[2][0] == sym))

class GameSever:
    def __init__(self) -> None:
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

    def main(self):
        soc = socket.socket()
        host = "localhost"
        port = 5555

        thread_count = 0

        try:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.bind((host, port))
        except socket.error as e:
            print(str(e))

        print("Socket is listening...")
        soc.listen(5)

        try:
            while True:
                client, address = soc.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                start_new_thread(self.multi_threaded_client, (client, ))
                thread_count += 1
                print('Thread Number: ' + str(thread_count))
        except KeyboardInterrupt:
            pass
            
        soc.close()

    def multi_threaded_client(self, conn):
        conn.send(str.encode('Server is working:'))
        while True:
            data = conn.recv(5555)
            response = 'Server message: ' + data.decode('utf-8')
            if not data:
                break
            conn.sendall(str.encode(response))
        conn.close()

if __name__ == "__main__":
    server = GameSever()
    server.main()