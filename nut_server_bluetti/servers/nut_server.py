"""Base nut server to extend."""

import asyncio

from .nut_commands import NUT_COMMANDS_RE, NutCommand


class NutServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 3493):
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

                # TODO handle exit requests
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
            case NutCommand.ListUps:
                return self._list_ups()
            case NutCommand.ListVar:
                return self._list_var(args)

        return error_response

    def _list_ups(self) -> str:
        return "\n".join(
            [
                "BEGIN LIST UPS",
                'UPS eb3a "Bluetti EB3A"',
                "END LIST UPS",
            ]
        )

    def _list_var(self, args: str) -> str:
        return "\n".join(
            [
                f"BEGIN LIST VAR {args}",
                f'VAR {args} device.mfr "Bluetti"',
                f'VAR {args} device.model "EB3A"',
                f"END LIST VAR {args}",
            ]
        )
