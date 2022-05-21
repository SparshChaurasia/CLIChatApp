from server import Message

import socket
import pickle
from threading import Thread


class Client:
    """
    A client to connect to an established chat server
    """

    def __init__(self):
        self.CLIENT: socket

    def print_message(self, message):
        """
        Helper function to print message
        :return: None
        """

        print(
            f"[{message.timestamp}] {message.author[0]}:{message.author[1]}> {message.content}"
        )

    def recieve_message(self):
        """
        Helper function to recieve messages from the server
        :return: None
        """

        while True:
            res = self.CLIENT.recv(1024)

            if not res:
                continue

            message = pickle.loads(res)
            self.print_message(message)

    def send_message(self):
        """
        Helper function to send messages to server
        :return: None
        """

        while True:
            message = input("> ")
            self.CLIENT.send(bytes(message, "utf-8"))

    def join_chat(self, host, port):
        """
        Function to connect to a server; recieve and send messages
        :return: None
        """
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENT.connect((host, port))
        print(f"Connected to server Ip: {host}\t Port: {port}")

        thread1 = Thread(target=self.recieve_message)
        thread1.start()

        thread2 = Thread(target=self.send_message)
        thread2.start()


def main():
    host = input("Enter host ip to connect: ")
    port = int(input("Enter host port number: "))

    c = Client()
    c.join_chat(host, port)


if __name__ == "__main__":
    main()
