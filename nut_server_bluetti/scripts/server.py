import asyncio
import logging

from ..adapter.dummy_adapter import DummyAdapter
from ..servers.nut_server import NutServer


async def start_async():
    adapter = DummyAdapter()
    server = NutServer(adapter)
    await server.start()


def start():
    """Entrypoint."""
    logging.basicConfig()

    asyncio.run(start_async())

    print("done")
