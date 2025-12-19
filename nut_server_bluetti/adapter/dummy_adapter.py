import random
from . import BaseAdapter, NutVariable


class DummyAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            "name",
            "Description",
            {
                "device.mfr": NutVariable("device.mfr", "Manufacturer"),
                "device.model": NutVariable("device.model", "Model"),
            },
        )

    def numlogins(self) -> int:
        return 0

    def get_values(self) -> dict[str, NutVariable]:
        return {
            "battery.charge": NutVariable("battery.charge", random.randint(50, 100)),
            "output.voltage": NutVariable("output.voltage", random.randint(1, 999)),
        }
