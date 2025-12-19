from dataclasses import dataclass
from enum import Enum


@dataclass
class NutVariable:
    name: str
    value: str | int | float | Enum
    vType: str | None = None


class BaseAdapter:
    def __init__(
        self, name: str, description: str, static_vars: dict[str, NutVariable] = {}
    ):
        self.name = name
        self.description = description
        self.static_vars = static_vars

    def numlogins(self) -> int:
        raise NotImplementedError()

    def get_values(self) -> dict[str, NutVariable]:
        return {}
