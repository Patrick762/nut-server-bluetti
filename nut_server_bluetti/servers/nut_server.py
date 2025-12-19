"""Base nut server."""

import asyncio

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
        error_response = "ERROR"

        regexed = NUT_COMMANDS_RE.match(command)

        cw = regexed.group("cw")
        ca = regexed.group("ca")
        args = regexed.group("a")

        if (cw is None and ca is None) or (ca is not None and args is None):
            return error_response

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

            # Get desc
            # Get cmddesc
            # Get tracking

            case NutCommand.ListUps:
                return self._list_ups()
            case NutCommand.ListVar:
                return self._list_var(args)

            # List rw
            # List cmd
            # List enum
            # List range
            # List client

            # Set var
            # Set tracking

            # Instcmd

            # Logout
            # Login

            # Primary

            # FSD

            # Password

            # Username

            # StartTls

            # Help
            # Ver
            # Netver

        return error_response

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

        if splitted[1] in self.adapter.static_vars.keys():
            return f'VAR {self.adapter.name} {splitted[1]} "{self.adapter.static_vars[splitted[1]].value}"'

        # TODO Get from dynamic
        return build_nut_error(NutError.VarNotSupported)

    def _get_type(self, args: str) -> str:
        splitted = args.split(" ")

        if len(splitted) != 2:
            return build_nut_error(NutError.InvalidArgument)

        if splitted[0] != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        if splitted[1] in self.adapter.static_vars.keys():
            return f'VAR {self.adapter.name} {splitted[1]} "{self.adapter.static_vars[splitted[1]].vType}"'

        # TODO Get from dynamic
        return build_nut_error(NutError.VarNotSupported)

    def _list_ups(self) -> str:
        return "\n".join(
            [
                "BEGIN LIST UPS",
                f'UPS {self.adapter.name} "{self.adapter.description}"',
                "END LIST UPS",
            ]
        )

    def _build_var_list(self) -> list[str]:
        return [
            f"VAR {self.adapter.name} {key} {value.value}"
            for [key, value] in self.adapter.static_vars.items()
        ]

    def _list_var(self, args: str) -> str:
        if args != self.adapter.name:
            return build_nut_error(NutError.UnknownUps)

        variables = self._build_var_list()

        return "\n".join(
            [f"BEGIN LIST VAR {args}"] + variables + [f"END LIST VAR {args}"]
        )
