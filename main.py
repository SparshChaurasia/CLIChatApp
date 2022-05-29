import sys

import server
import client

from rich.console import Console
from rich.prompt import Prompt


def main():
    console = Console()
    console.print(
        "[bold magenta]Welcome to Point Chat![/]\n"
        "An open-source comand line utility to chat anonymously with people\n"
        "[bold magenta]GitHub:[/] github.com/SparshChaurasia/PointChat\n\n"
        "[bold magenta]Features:[/]\n"
        " * Text chat\n"
        " * Emojis using emoji markup language\n\n"
        "[bold magenta]How to use:[/]\n"
        " 1) Host a chat server to join on localhost or your public ip\n"
        " 2) Join the chat server using that ip\n"
    )

    option = Prompt.ask(
        "Select one option", show_choices=True, choices=["host", "join"]
    )
    console.print()

    if option == "host":
        server.main()
    else:
        client.main()


if __name__ == "__main__":
    main()
