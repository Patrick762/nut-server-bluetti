from . import BaseAdapter, NutVariable


class DummyAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            "name",
            "Description",
            {
                "device.mfr": NutVariable("device.mfr", "Manufacturer", "STRING:12"),
                "device.model": NutVariable("device.model", "Model", "STRING:5"),
            },
        )

    def numlogins(self) -> int:
        return 0
