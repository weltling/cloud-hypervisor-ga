import unittest
import sys
import os
import platform
import subprocess
from mock import patch
sys.path.insert(1, sys.path[0] + "/../src/guest_agent")
from guest_agent import GuestAgent # noqa E402


def mock_vsock_listener(self):
    pass


def mock_init(self):
    self.command = None


class TestAgentMethods(unittest.TestCase):

    # Test execute
    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_guest_sync(self):
        ga = GuestAgent()
        input = {"execute": "guest-sync", "arguments": {"id": 1234}}
        expected = {'return': ga.guest_sync(1234)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_create_user_no_other_args(self):
        ga = GuestAgent()
        input = {"execute": "guest-sync", "arguments": {"id": 1234}}
        expected = {'return': ga.guest_sync(1234)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_create_user_only_home(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        input = {"execute": "create-user",
                 "arguments": {"username": user_name,
                               "create-home": True}}
        expected = {'return': ga.create_user(user_name, create_home=True)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_create_user_only_one_group(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        user_group = "kvm"
        input = {"execute": "create-user",
                 "arguments": {"username": user_name,
                               "groups": user_group}}
        expected = {'return': ga.create_user(user_name, groups=user_group)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_create_user_many_groups(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        user_group = ["kvm", "libvirt"]
        input = {"execute": "create-user",
                 "arguments": {"username": user_name,
                               "groups": user_group}}
        expected = {'return': ga.create_user(user_name, groups=user_group)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_create_user_group_and_home(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        user_group = "kvm"
        input = {"execute": "create-user",
                 "arguments": {"username": user_name,
                               "groups": user_group,
                               "create-home": True}}
        expected = {'return':
                    ga.create_user(user_name,
                                   groups=user_group,
                                   create_home=True)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_get_osinfo(self):
        ga = GuestAgent()
        input = {'execute': "get-osinfo"}
        result = ga.execute_qmp(input)
        expected = {'return': ga.get_osinfo()}
        self.assertDictEqual(expected, result)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_execute_deploy_ssh_pubkey(self):
        ga = GuestAgent()
        ssh_key = "test ssk key"
        user_name = "anothertestuser"
        input = {'execute': "deploy-ssh-pubkey",
                 "arguments": {"username": user_name, "ssh-key": ssh_key}}
        result = ga.execute_qmp(input)
        expected = {'return': ga.deploy_ssh_pubkey(user_name, ssh_key)}
        self.assertDictEqual(expected, result)


class TestAgentCommands(unittest.TestCase):

    # test guest-sync
    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_guest_sync(self):
        ga = GuestAgent()
        expected = 1234
        res = ga.guest_sync(1234)
        self.assertEqual(expected, res)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_create_user_no_other_args(self):
        ga = GuestAgent()
        user_name = "testuser"
        ga.create_user(user_name)
        f = open("/etc/passwd", "r")
        matched_users = set(line[:len(user_name)] for line in f.read().split())
        self.assertTrue(user_name in matched_users)
        os.system("sudo userdel -r testuser")

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_create_user_only_home(self):
        os.system("userdel -r testuser")
        ga = GuestAgent()
        user_name = "testuser"
        user_home = True
        ga.create_user(user_name, create_home=user_home)
        user_entries = open("/etc/passwd").read().split()

        for entry in user_entries:
            entry_items = entry.split(":")
            if entry_items[0] == user_name:
                self.assertTrue(entry_items[5] == "/home/{}".format(user_name))
                break
        else:
            raise ValueError("user not found")

        os.system("userdel -r testuser")

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_create_user_only_one_group(self):
        os.system("userdel testuser")
        ga = GuestAgent()
        test_group = "testgroup"
        test_user = "testuser"
        os.system("groupadd testgroup")
        ga.create_user(test_user, groups=test_group)
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        self.assertTrue(test_group in groups)
        os.system("userdel testuser")

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_create_user_many_groups(self):
        ga = GuestAgent()
        test_groups = ["testgroup1", "testgroup2", "testgroup3"]
        test_user = "testuser"
        os.system("userdel testuser")
        os.system("groupadd {}".format(test_groups[0]))
        os.system("groupadd {}".format(test_groups[1]))
        os.system("groupadd {}".format(test_groups[2]))
        ga.create_user(test_user, groups=test_groups)
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        for group in test_groups:
            self.assertTrue(group in groups)
        os.system("userdel testuser")

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_create_user_group_and_home(self):
        ga = GuestAgent()
        user_name = "testuser"
        test_home = True
        test_groups = ["testgroup1", "testgroup2", "testgroup3"]

        os.system("userdel -r testuser")
        os.system("groupadd {}".format(test_groups[0]))
        os.system("groupadd {}".format(test_groups[1]))
        os.system("groupadd {}".format(test_groups[2]))

        ga.create_user(user_name, create_home=test_home, groups=test_groups)

        # Find groups
        ps = subprocess.Popen(('groups', user_name),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        for group in test_groups:
            self.assertTrue(group in groups)

        # Find home directory
        user_entries = open("/etc/passwd").read().split()

        for entry in user_entries:
            entry_items = entry.split(":")
            if entry_items[0] == user_name:
                self.assertTrue(entry_items[5] == "/home/{}".format(user_name))
                break
        else:
            raise ValueError("user not found")
        os.system("userdel -r testuser")

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_get_osinfo(self):
        ga = GuestAgent()
        info = platform.freedesktop_os_release()
        uname_info = os.uname()
        expected = {}
        expected["kernel-release"] = uname_info.release
        expected["kernel-version"] = uname_info.version
        expected["machine"] = uname_info.machine
        expected["name"] = info["NAME"]
        expected["pretty-name"] = info["PRETTY_NAME"]
        expected["version"] = info["VERSION"]
        expected["version-id"] = info["VERSION_ID"]

        result = ga.get_osinfo()
        self.assertDictEqual(expected, result)

    @patch.object(GuestAgent, 'vsock_listener', mock_vsock_listener)
    @patch.object(GuestAgent, '__init__', mock_init)
    def test_deploy_ssh_pubkey(self):
        ga = GuestAgent()
        ssh_key = "sshkeytest"
        ssh_user = "testuser"
        os.system("useradd {}".format(ssh_user))
        ga.deploy_ssh_pubkey(ssh_user, ssh_key)
        f = open("/home/{}/.ssh/authorized_keys".format(ssh_user)).read()

        self.assertTrue(ssh_key in f)


if __name__ == '__main__':
    unittest.main()
