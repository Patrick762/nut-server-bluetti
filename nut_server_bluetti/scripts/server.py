import asyncio
import logging

from ..servers.nut_server import NutServer


async def start_async():
    server = NutServer()
    await server.start()


def start():
    """Entrypoint."""
    logging.basicConfig()

    asyncio.run(start_async())

    print("done")
