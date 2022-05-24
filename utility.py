from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """
    Dataclass to hold the attributes of a message
    """

    content: str
    username: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"[bold][underline][{self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}] [magenta]{self.username}[/][/][/] {self.content}"
