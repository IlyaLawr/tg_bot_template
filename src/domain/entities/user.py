from dataclasses import dataclass


@dataclass
class User:
    client_id: int
    username: str
    access: bool = False
