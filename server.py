from utility import Message

import socket
import random
import pickle
import threading
from _thread import start_new_thread
from typing import Tuple, List, Dict


from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt, IntPrompt


class Server:
    """
    Groups the functionality to host a chatroom where suitable clients could connect
    """

    def __init__(self, host, port, member_count, console):
        self.HOST: str = host
        self.PORT: int = port
        self.SERVER: socket  # Instance of the server socket
        self.MEMBER_COUNT: int = member_count  # Number of members server listen
        self.CONSOLE: Console = console  # Sandard output screen

        # Dictionary of all clients connected and their usernames
        self.CLIENTS: Dict[(str, socket)] = {}
        self.BANNED_IP: List[str] = []  # Ip banned from the chat

    def broadcast(self, message: Message):
        """
        Helper function to send message to all the clients connected on the server
        :return: None
        """

        for client in self.CLIENTS.values():
            obj = pickle.dumps(message)
            client.send(obj)

    def recive_messages(self, client, username):
        """
        Helper function to listen to the client and broadcast the message to all the other clients
        :return: None
        """

        while True:
            try:
                res = client.recv(1024).decode()
                res.strip()  # Remove all extra spaaces and new lines

                message = Message(res, username)
                self.broadcast(message)

            except ConnectionResetError:
                del self.CLIENTS[username]

                client.close()

                self.CONSOLE.print(f"{username!s} has left the chat", style="error")
                self.broadcast(f"{username!s} has left the chat")
                break

            except ConnectionAbortedError:
                del self.CLIENTS[username]

                client.close()

                self.CONSOLE.print(f"{username!s} has left the chat", style="error")
                self.broadcast(f"{username!s} has left the chat")
                break

    def genrate_username(self):
        """
        Helper function to generate a unique username
        :return: str
        """

        username = f"user{random.randrange(10000)}"
        while username in self.CLIENTS.keys():
            username = f"user{random.randrange(10000)}"

        return username

    def validate_username(self, username):
        """
        Helper function to check if the username is unique
        :return: bool
        """

        if username not in self.CLIENTS.keys():
            return True

    def add_members(self):
        """
        Helper function to connect clients to the server
        :return: None
        """

        while True:
            client, address = self.SERVER.accept()

            if address[0] in self.BANNED_IP:
                self.CONSOLE.print(
                    f"{address[0]} was denied connection to the server - Restricted user tried to join",
                    style="debug",
                )
                client.close()
                continue

            default_username = self.genrate_username()
            while True:
                message = Message(
                    f"Enter your username - suggestion: {default_username!s}", "Server"
                )
                obj = pickle.dumps(message)
                client.send(obj)

                try:
                    username = client.recv(1024).decode()
                    username.strip()
                except EOFError:
                    self.CONSOLE.print(
                        f"{address[0]}:{address[1]} failed to join",
                        style="error",
                    )

                if self.validate_username(username):
                    self.CLIENTS.update({username: client})
                    break

            start_new_thread(self.recive_messages, (client, username))

            self.CONSOLE.print(f"{username!s} joined the chat!", style="success")
            self.broadcast(f"{username!s} joined the chat!")

    def host_chat(self):
        """
        Function to host a server for multiple clients to connect
        :return: None
        """

        self.SERVER = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.SERVER.bind((self.HOST, self.PORT))
        self.CONSOLE.print(
            f"Server started at Ip: {self.HOST}\t Port: {self.PORT}", style="success"
        )

        self.SERVER.listen(self.MEMBER_COUNT)
        self.CONSOLE.print("Waiting for connections...", style="debug")

        thread1 = threading.Thread(target=self.add_members)
        thread1.start()


def main():
    custom_theme = Theme(
        {"success": "bold green", "error": "bold magenta", "debug": "bold white"}
    )

    console = Console(theme=custom_theme)

    host = Prompt.ask("Enter an ip to host the chatroom", default="localhost")
    port = IntPrompt.ask("Enter port number")
    member_count = IntPrompt.ask(
        "Enter the number of members server could connect", default=5
    )

    s = Server(host, port, member_count, console)
    s.host_chat()


if __name__ == "__main__":
    main()
