from dataclasses import dataclass


@dataclass
class NutVariable:
    name: str
    value: str
    vType: str


class BaseAdapter:
    def __init__(
        self, name: str, description: str, static_vars: dict[str, NutVariable] = {}
    ):
        self.name = name
        self.description = description
        self.static_vars = static_vars

    def numlogins(self) -> int:
        raise NotImplementedError()
