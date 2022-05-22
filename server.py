import socket
import pickle
from typing import Tuple, List
import threading
from _thread import start_new_thread
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime


@dataclass
class Message:
    """
    Dataclass to hold the attributes of a message
    """

    content: str
    author: Tuple[str, int]
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self):
        return self.content


class Server:
    """
    Groups the functionality to host a chatroom where suitable clients could connect
    """

    def __init__(self, host, port, member_count):
        self.HOST: str = host
        self.PORT: int = port
        self.SERVER: socket  # Instance of the server socket
        self.MEMBER_COUNT: int = member_count  # Number of members server listen
        self.CLIENTS: List[socket] = []  # List of all clients connected
        self.BANNED_IP: List[str] = []  # Ip banned from the chat

    def broadcast(self, message: Message):
        """
        Helper function to send message to all the clients connected on the server
        :return: None
        """

        for client in self.CLIENTS:
            obj = pickle.dumps(message)
            client.send(obj)

    def recive_messages(self, client, address):
        """
        Helper function to listen to the client and broadcast the message to all the other clients
        :return: None
        """

        while True:
            try:
                res = client.recv(1024).decode()
                message = Message(res, address)
                self.broadcast(message)

            except ConnectionResetError:
                print(f"{address[0]}:{address[1]} has left the chat")
                client.close()
                self.CLIENTS.remove(client)
                break

            except ConnectionAbortedError:
                print(f"{address[0]}:{address[1]} has left the chat")
                client.close()
                self.CLIENTS.remove(client)
                break

    def add_members(self):
        """
        Helper function to connect clients to the server
        :return: None
        """

        while True:
            client, address = self.SERVER.accept()

            if address in self.BANNED_IP:
                client.send(
                    bytes("Refused to connect - Your ip is blacklisted", "utf-8")
                )
                client.close()
                continue

            start_new_thread(self.recive_messages, (client, address))
            print(f"{address[0]}:{address[1]} joined the chat!")
            self.CLIENTS.append(client)

    def host_chat(self):
        """
        Function to host a server for multiple clients to connect
        :return: None
        """

        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind((self.HOST, self.PORT))
        print(f"Server started at Ip: {self.HOST}\t Port: {self.PORT}")

        self.SERVER.listen(self.MEMBER_COUNT)
        print("Waiting for connections...")

        thread1 = threading.Thread(target=self.add_members)
        thread1.start()


def main():
    host = input("Enter an ip to host the chatroom: ")
    port = int(input("Enter port number: "))
    member_count = int(input("Enter the number of members for the server to listen: "))

    s = Server(host, port, member_count)
    s.host_chat()


if __name__ == "__main__":
    main()
