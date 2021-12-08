import socket

class Client:
    def __init__(self) -> None:
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

    def main(self):
        soc = socket.socket()
        host = 'localhost'
        port = 5555

        print('Waiting for connection response')
        try:
            soc.connect((host, port))
        except socket.error as e:
            print(str(e))
        
        res = soc.recv(1024)

        while True:
            msg = input("Message: ")
            soc.send(str.encode(msg))
            res = soc.recv(1024)
            print(res.decode('utf-8'))
        soc.close()

if __name__ == "__main__":
    client = Client()
    client.main()