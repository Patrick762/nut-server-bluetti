import random

from . import BaseAdapter
from ..definitions import NutVariable, DeviceType, UpsStatus


class DummyAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            "name",
            "Description",
            [
                NutVariable.device_mfr("Manufacturer"),
                NutVariable.device_model("Model"),
                NutVariable.device_type(DeviceType.Ups),
            ],
        )

    def numlogins(self) -> int:
        return 0

    def _get_values(self) -> list[NutVariable]:
        return [
            NutVariable.ups_status([UpsStatus.Online]),
            NutVariable.battery_charge(random.randint(50, 100)),
        ]
