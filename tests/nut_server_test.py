import unittest

from nut_server_bluetti.adapter.dummy_adapter import DummyAdapter
from nut_server_bluetti.servers.nut_server import NutServer


class TestNutServer(unittest.TestCase):
    def _mock_adapter(self):
        return DummyAdapter()

    def _mock(self):
        return NutServer(self._mock_adapter())

    def test_build_var_list(self):
        server = self._mock()

        variables = server._build_var_list()

        self.assertIn("VAR name device.mfr Manufacturer", variables)
