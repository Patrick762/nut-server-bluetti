import unittest

from nut_server_bluetti.servers.nut_commands import NUT_COMMANDS_RE


class TestCommandParser(unittest.TestCase):
    def test_list_ups(self):
        result = NUT_COMMANDS_RE.match("LIST UPS")

        self.assertEqual(result.group("cw"), "LIST UPS")

    def test_list_var(self):
        result = NUT_COMMANDS_RE.match("LIST VAR myUps")

        self.assertEqual(result.group("ca"), "LIST VAR")
        self.assertEqual(result.group("a"), "myUps")
