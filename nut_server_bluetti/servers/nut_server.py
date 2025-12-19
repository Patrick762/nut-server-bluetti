"""Base nut server."""

import asyncio
from enum import Enum

from ..adapter import BaseAdapter
from .errors import NutError, build_nut_error
from .nut_commands import NUT_COMMANDS_RE, NutCommand


class NutServer:
    def __init__(self, adapter: BaseAdapter, host: str = "0.0.0.0", port: int = 3493):
        self.adapter = adapter
        self.host = host
        self.port = port

    async def start(self):
        server = await asyncio.start_server(
            self._handle_connection, self.host, self.port
        )
        async with server:
            await server.serve_forever()

    async def _handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        print("New connection")
        while True:
            try:
                buffer = await reader.readuntil()
                data = buffer.decode()

                if not data:
                    break

                print(f"-> {repr(data)}")
                result = self._handle_command(data)
                print(f"<- {repr(result)}")
                writer.write(f"{result}\n".encode())
                writer.write_eof()
            except:
                print("Error")
                break

        writer.close()

    def _handle_command(self, command: str) -> str:
        regexed = NUT_COMMANDS_RE.match(command)

        cw = regexed.group("cw")
        ca = regexed.group("ca")
        args = regexed.group("a")

        if (cw is None and ca is None) or (ca is not None and args is None):
            return build_nut_error(NutError.UnknownCommand)

        if cw is not None:
            parsed = NutCommand(cw)

        if ca is not None:
            parsed = NutCommand(ca)

        match (parsed):
            case NutCommand.GetNumlogins:
                return self._get_numlogins(args)
            case NutCommand.GetUpsdesc:
                return self._get_upsdesc(args)
            case NutCommand.GetVar:
                return self._get_var(args)
            case NutCommand.GetType:
                return self._get_type(args)
            case NutCommand.ListUps:
                return self._list_ups()
            case NutCommand.ListVar:
                return self._list_var(args)

        return build_nut_error(NutError.FeatureNotSupported)

    def _get_numlogins(self, args: str) -> str:
        if args != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        return "\n".join(
            [
                f"NUMLOGINS {args} {str(self.adapter.numlogins())}",
            ]
        )

    def _get_upsdesc(self, args: str) -> str:
        if args != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        return "\n".join(
            [
                f'UPSDESC {args} "{self.adapter.description}"',
            ]
        )

    def _get_var(self, args: str) -> str:
        splitted = args.split(" ")

        if len(splitted) != 2:
            return build_nut_error(NutError.InvalidArgument)

        if splitted[0] != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        value = None

        if splitted[1] in self.adapter.static_vars.keys():
            value = self.adapter.static_vars[splitted[1]].value

        dynamic = self.adapter.get_values()
        if splitted[1] in dynamic.keys():
            value = dynamic[splitted[1]].value

        if value is None:
            return build_nut_error(NutError.VarNotSupported)

        return f'VAR {self.adapter.name} {splitted[1]} "{value}"'

    def _get_type(self, args: str) -> str:
        splitted = args.split(" ")

        if len(splitted) != 2:
            return build_nut_error(NutError.InvalidArgument)

        if splitted[0] != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        value = None
        vType = None

        if splitted[1] in self.adapter.static_vars.keys():
            value = self.adapter.static_vars[splitted[1]].value
            vType = self.adapter.static_vars[splitted[1]].vType

        dynamic = self.adapter.get_values()
        if splitted[1] in dynamic.keys():
            value = dynamic[splitted[1]].value
            vType = dynamic[splitted[1]].vType

        if value is None:
            return build_nut_error(NutError.VarNotSupported)

        # detect var type if not set
        if vType is None:
            if isinstance(value, str):
                vType = "STRING:30"
            if isinstance(value, int) or isinstance(value, float):
                vType = "NUMBER"
            if isinstance(value, Enum):
                vType = "ENUM"

        return f'VAR {self.adapter.name} {splitted[1]} "{vType}"'

    def _list_ups(self) -> str:
        return "\n".join(
            [
                "BEGIN LIST UPS",
                f'UPS {self.adapter.name} "{self.adapter.description}"',
                "END LIST UPS",
            ]
        )

    def _build_var_list(self) -> list[str]:
        variables = self.adapter.static_vars
        variables.update(self.adapter.get_values())

        return [
            f'VAR {self.adapter.name} {key} "{value.value}"'
            for [key, value] in variables.items()
        ]

    def _list_var(self, args: str) -> str:
        if args != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        variables = self._build_var_list()

        return "\n".join(
            [f"BEGIN LIST VAR {args}"] + variables + [f"END LIST VAR {args}"]
        )
