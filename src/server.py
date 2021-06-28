import socket
from typing import Tuple


class Server:
    MAX_CLIENTS = 5

    def __init__(self, ipAddress: str, port: str) -> None:
        self.clients: dict[str, socket.SocketIO] = dict()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ipAddress, port))
        self.server.listen(self.MAX_CLIENTS)

    def accept(self) -> Tuple[socket.SocketIO, socket.AddressInfo]:
        connection, address = self.server.accept()
        self.clients[address] = connection
        return connection, address

    def broadcast(self, address: str, message: str) -> None:
        for addr, client in self.clients.items():
            if addr != address:
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    client.close()
                    del self.clients[address]

    def remove(self, client: str):
        del self.clients[client]
