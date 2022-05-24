from utility import Message

import os
import socket
import pickle
from threading import Thread
from datetime import datetime

from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt, IntPrompt


class Client:
    """
    A client to connect to an established chat server
    """

    def __init__(self, console: Console):
        self.CLIENT: socket  # Instance of the client socket connnection
        self.CONSOLE = console  # Standard output screen

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
            self.CONSOLE.print(str(message))

    def send_message(self):
        """
        Helper function to send messages to server
        :return: None
        """

        while True:
            try:
                message = input()
            except KeyboardInterrupt:
                os._exit(1)
            except EOFError:
                os._exit(1)

            self.CLIENT.send(bytes(message, "utf-8"))

    def join_chat(self, host, port):
        """
        Function to connect to a server; recieve and send messages
        :return: None
        """

        self.CLIENT = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        try:
            self.CLIENT.connect((host, port))
        except ConnectionRefusedError:
            self.CONSOLE.print(
                "Failed to connect - Target machine refused to connect", style="error"
            )
            return
        except ConnectionResetError:
            self.CONSOLE.print(
                "Connnection reset - An existing connection was forcibly closed by the remote host",
                style="error",
            )
            return

        self.CONSOLE.print(
            f"Connected to server Ip: {host}\t Port: {port}", style="debug"
        )

        thread1 = Thread(target=self.recieve_message)
        thread1.start()

        thread2 = Thread(target=self.send_message)
        thread2.start()


def main():
    custom_theme = Theme(
        {"success": "bold green", "error": "bold magenta", "debug": "bold white"}
    )
    console = Console(theme=custom_theme)

    host = Prompt.ask("Enter host ip to connect", default="localhost")
    port = IntPrompt.ask("Enter host port number", default=9999)

    c = Client(console)
    c.join_chat(host, port)


if __name__ == "__main__":
    main()
