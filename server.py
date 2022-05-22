import socket
import pickle
from typing import Tuple, List
import threading
from _thread import start_new_thread
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt, IntPrompt


@dataclass
class Message:
    """
    Dataclass to hold the attributes of a message
    """

    content: str
    author: Tuple[str, int]
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"[bold][underline][{self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}] [magenta]{self.author[0]}:{self.author[1]}[/][/][/] {self.content}"


class Server:
    """
    Groups the functionality to host a chatroom where suitable clients could connect
    """

    def __init__(self, host, port, member_count, console):
        self.HOST: str = host
        self.PORT: int = port
        self.SERVER: socket  # Instance of the server socket
        self.MEMBER_COUNT: int = member_count  # Number of members server listen
        self.CLIENTS: List[socket] = []  # List of all clients connected
        self.CONSOLE: Console = console  # Sandard output screen
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
                self.CLIENTS.remove(client)
                client.close()

                self.CONSOLE.print(
                    f"{address[0]}:{address[1]} has left the chat", style="error"
                )
                self.broadcast(f"{address[0]}:{address[1]} has left the chat")
                break

            except ConnectionAbortedError:
                self.CLIENTS.remove(client)
                client.close()

                self.CONSOLE.print(
                    f"{address[0]}:{address[1]} has left the chat",
                    style="error",
                )
                self.broadcast(f"{address[0]}:{address[1]} has left the chat")
                break

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

            start_new_thread(self.recive_messages, (client, address))
            self.CONSOLE.print(
                f"{address[0]}:{address[1]} joined the chat!", style="success"
            )
            self.broadcast(f"{address[0]}:{address[1]} joined the chat!")
            self.CLIENTS.append(client)

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
