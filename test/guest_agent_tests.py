import unittest
import sys
import os
import platform
import subprocess
sys.path.insert(1, sys.path[0] + "/../src/guest_agent")
from guest_agent import GuestAgent # noqa E402


class TestAgentMethods(unittest.TestCase):

    # Test execute
    def test_execute_guest_sync(self):
        input = {"execute": "guest-sync", "arguments": {"id": 1234}}
        expected = {'result': GuestAgent.guest_sync(1234)}
        res = GuestAgent.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_create_user_no_other_args(self):
        raise NotImplementedError

    def test_execute_create_user_only_home(self):
        raise NotImplementedError

    def test_execute_create_user_only_one_group(self):
        raise NotImplementedError

    def test_execute_create_user_many_groups(self):
        raise NotImplementedError

    def test_execute_create_user_group_and_home(self):
        raise NotImplementedError

    def test_execute_get_osinfo(self):
        input = {'execute': "get-osinfo"}
        result = GuestAgent.execute_qmp(input)
        expected = {'result': GuestAgent.get_osinfo()}
        self.assertDictEqual(expected, result)

    def test_execute_deploy_ssh_pubkey(self):
        raise NotImplementedError


class TestAgentCommands(unittest.TestCase):

    # test guest-sync
    def test_guest_sync(self):
        expected = 1234
        res = GuestAgent.guest_sync(1234)
        self.assertEqual(expected, res)

    def test_create_user_no_other_args(self):
        user_name = "testuser"
        GuestAgent.create_user(user_name)

        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        try:
            output = subprocess.check_output(('grep', 'testuser'),
                                             stdin=ps.stdout)
        except subprocess.CalledProcessError:
            self.debug("User not found")
        ps.wait()

        self.assertEqual(output.decode()[:len(user_name)], user_name)

    def test_create_user_only_home(self):
        user_name = "testuser"
        user_home = "/home/testuserhome"
        GuestAgent.create_user(user_name, home=user_home)

        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        try:
            output = subprocess.check_output(('grep', user_home),
                                             stdin=ps.stdout)
            ps.wait()
        except subprocess.CalledProcessError:
            self.debug("Home directory not found")

        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        ps.wait()
        try:
            output = subprocess.check_output(('grep', 'testuser'),
                                             stdin=ps.stdout)
        except subprocess.CalledProcessError:
            self.debug("User not found")

        self.assertEqual(output.decode()[:len(user_name)], user_name)

    def test_create_user_only_one_group(self):
        test_group = "testgroup"
        test_user = "testuser"
        GuestAgent.create_user(test_user, groups=test_group)
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        self.assertTrue(test_group in groups)

    def test_create_user_many_groups(self):
        test_groups = ["testgroup", "anothergroup", "thirdgroup"]
        test_user = "testuser"
        GuestAgent.create_user(test_user, groups=test_groups)
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        for group in test_groups:
            self.assertTrue(group in groups)

    def test_create_user_group_and_home(self):
        test_groups = ["testgroup", "anothergroup", "thirdgroup"]
        test_user = "testuser"
        test_home = "/home/testuserhome"
        GuestAgent.create_user(test_user, home=test_home, groups=test_groups)

        # Find groups
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        for group in test_groups:
            self.assertTrue(group in groups)

        # Find home directory
        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        try:
            subprocess.check_output(('grep', test_home),
                                    stdin=ps.stdout)
            ps.wait()
        except subprocess.CalledProcessError:
            self.debug("Home directory not found")

    def test_get_osinfo(self):
        info = platform.freedesktop_os_release()
        print(info)
        uname_info = os.uname()
        print(os.uname())
        expected = {}
        expected["kernel-release"] = uname_info.release
        expected["kernel-version"] = uname_info.version
        expected["machine"] = uname_info.machine
        expected["name"] = info["NAME"]
        expected["prtty-name"] = info["PRETTY_NAME"]
        expected["version"] = info["VERSION"]
        expected["version-id"] = info["VERSION_ID"]

        result = GuestAgent.get_osinfo()
        self.assertDictEqual(expected, result)

    def test_deploy_ssh_pubkey(self):
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
