import argparse
import asyncio
import logging
from typing import List

from nut_base_server import NutServer
from bluetti_bt_lib import build_device, FieldName

from .bluetti_adapter import BluettiAdapter

REQUIRED_FIELDS = [
    FieldName.DEVICE_TYPE.value,
    FieldName.BATTERY_SOC.value,
    FieldName.AC_INPUT_VOLTAGE.value,
    FieldName.AC_INPUT_POWER.value,
    FieldName.AC_OUTPUT_POWER.value,
]

def is_supported(t: str) -> bool:
    device = build_device(t + "123456789")
    if device is None:
        return False
    field_names: List[str] = []

    for f in device.fields:
        field_names.append(f.name)

    return all([f in field_names for f in REQUIRED_FIELDS])


async def start_async(address: str, t: str, encryption: bool, interval: int):
    adapter = BluettiAdapter(address, t, encryption, interval)
    server = NutServer(adapter)
    await server.start()


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(description="NUT Server for bluetti powerstation")
    parser.add_argument("-m", "--mac", type=str, help="Mac-address of the powerstation")
    parser.add_argument(
        "-t", "--type", type=str, help="Type of the powerstation (AC70 f.ex.)"
    )
    parser.add_argument(
        "-e", "--encryption", type=bool, help="Add this if encryption is needed"
    )
    parser.add_argument(
        "-i", "--interval", type=int, help="Set the polling interval in seconds. Defaults to 20"
    )
    args = parser.parse_args()

    if args.mac is None or args.type is None:
        parser.print_help()
        return
    
    if not is_supported(args.type):
        print("This powerstation is not supported (missing fields)")
        return

    logging.basicConfig()

    interval = 20

    if args.interval is not None:
        interval = args.interval

    print(f"Polling interval: {interval}s")

    asyncio.run(start_async(args.mac, args.type, args.encryption, interval))

    print("done")
