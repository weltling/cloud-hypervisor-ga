import unittest
from qemu.qmp import Message
import sys
sys.path.insert(1, "../src/guest_agent")
from guest_agent import GuestAgent

class TestAgentMethods(unittest.TestCase):

    # Test execute
    def test_execute_guest_sync(self):
        input = {"execute": "guest-sync", "arguments": {"id": 1234}}
        expected = GuestAgent.guest_sync(1234)
        res = GuestAgent.guest_sync(1234)
        self.assertDictEqual(dict(expected), res)


class TestAgentCommands(unittest.TestCase):

    # test guest-sync
    def test_guest_sync(self):
        expected = 1234
        res = GuestAgent.guest_sync(1234)
        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()