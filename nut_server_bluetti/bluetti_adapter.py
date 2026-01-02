import asyncio

from nut_definitions import NutVariable, DeviceType, UpsStatus
from bluetti_bt_lib import build_device, DeviceReader, FieldName
from nut_base_server import BaseAdapter


class BluettiAdapter(BaseAdapter):
    def __init__(self, mac: str, dType: str, use_encryption: bool, interval):
        super().__init__(
            "powerstation",
            "Powerstation",
            [
                NutVariable.device_mfr("Bluetti"),
                NutVariable.device_type(DeviceType.Ups),
            ],
        )
        self.mac = mac
        self.dType = dType
        self.use_encryption = use_encryption
        self.interval = interval

        self.lock = asyncio.Lock()
        self.data: dict | None = {}

        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.periodic())

    def numlogins(self) -> int:
        return 0

    async def _get_values(self) -> list[NutVariable]:
        await self.lock.acquire()

        model = self.data.get(FieldName.DEVICE_TYPE.value)
        soc = self.data.get(FieldName.BATTERY_SOC.value)
        vin = self.data.get(FieldName.AC_INPUT_VOLTAGE.value)
        pwr_in = self.data.get(FieldName.AC_INPUT_POWER.value)
        pwr_out = self.data.get(FieldName.AC_OUTPUT_POWER.value)

        self.lock.release()

        if (
            model is None
            or soc is None
            or vin is None
            or pwr_in is None
            or pwr_out is None
        ):
            return []

        ups_status = []

        if vin > 50:
            ups_status.append(UpsStatus.Online)
        else:
            ups_status.append(UpsStatus.OnBattery)

        if pwr_in > 0:
            ups_status.append(UpsStatus.Charging)

        if pwr_out > 0 and vin < 50:
            ups_status.append(UpsStatus.Discharging)

        return [
            NutVariable.device_model(model),
            NutVariable.ups_status(ups_status),
            NutVariable.battery_charge(soc),
            NutVariable.ups_realpower(pwr_out),
        ]

    async def periodic(self):
        device = build_device(self.dType + "123456789")
        reader = DeviceReader(self.mac, device, asyncio.Future)
        tmp = {}

        while True:
            print("START POLLING")
            tmp = await reader.read()
            print("END POLLING")
            async with self.lock:
                self.data = tmp
            await asyncio.sleep(self.interval)
