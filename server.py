import socket
from _thread import *
from board import Board
import json
import sys

class GameSever:
    def __init__(self) -> None:
        self.board = Board()
        self.clients = []

    def main(self):
        soc = socket.socket()
        host = sys.argv[1] if sys.argv[1] else 'localhost'
        port = 5555

        self.thread_count = 0

        try:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.bind((host, port))
        except socket.error as e:
            print(str(e))

        print("Socket is listening...")
        soc.listen(2)

        while True:
            client, address = soc.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))

            start_new_thread(self.multi_threaded_client, (client, ))
            self.thread_count += 1
            print('Thread Number: ' + str(self.thread_count))      

    def multi_threaded_client(self, conn):
        cid = conn.fileno()
        self.clients.append(cid)

        while True:
            response = '000'
            data = conn.recv(5555).decode('utf-8')

            if data=='hi':
                response = json.dumps(self.board.get_gameinfo())
            else:
                if len(self.clients) == 2:
                    if (cid == self.clients[self.board.turn]):
                        self.board.click_check(int(data))

            print(self.board.board)
            conn.sendall(response.encode())

if __name__ == "__main__":
    server = GameSever()
    server.main()