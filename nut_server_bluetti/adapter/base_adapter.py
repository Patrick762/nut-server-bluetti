from ..definitions import NutVariable


class BaseAdapter:
    def __init__(
        self, name: str, description: str, static_vars: list[NutVariable] = []
    ):
        self.name = name
        self.description = description
        self.static_vars = static_vars

    def _get_nut_variable(self, name: str) -> NutVariable | None:
        """DO NOT OVERRIDE!"""
        all_vars = self.static_vars + self._get_values()
        found = [f for f in all_vars if f.name == name]
        if len(found) == 0:
            return None
        return found[-1]

    def get_variable_value(self, name: str) -> str | None:
        """DO NOT OVERRIDE!"""
        variable = self._get_nut_variable(name)
        if variable is None:
            return None
        return variable.value

    def get_all_variables(self) -> list[NutVariable]:
        """DO NOT OVERRIDE!"""
        return self.static_vars + self._get_values()

    def get_variable_type(self, name: str) -> str | None:
        """DO NOT OVERRIDE!"""
        variable = self._get_nut_variable(name)
        if variable is None:
            return None
        return variable.vType

    def numlogins(self) -> int:
        raise NotImplementedError()

    def _get_values(self) -> list[NutVariable]:
        return []
