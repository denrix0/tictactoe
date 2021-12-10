import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from game.board import Board

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

import json


class GameSever(Protocol):

    def __init__(self, board):
        self.board = board

    def connectionMade(self):
        print("New client")
        ServerFactory.clients.append(self)
        print(ServerFactory.clients)

    def dataReceived(self, data):
        if (ServerFactory.clients.index(self) == self.board.turn):
            self.board.click_check(int(data.decode()))
        for client in ServerFactory.clients:
            client.transport.write(json.dumps(self.board.get_gameinfo()).encode())

    def connectionLost(self, reason):
        ServerFactory.clients.remove(self)


class ServerFactory(ServFactory):
    clients = []

    def __init__(self):
        self.board = Board()

    def buildProtocol(self, addr):
        if len(ServerFactory.clients) <= 2:
            return GameSever(self.board)


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 2000)
    endpoint.listen(ServerFactory())
    reactor.run()