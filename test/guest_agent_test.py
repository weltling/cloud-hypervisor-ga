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
        ga = GuestAgent()
        input = {"execute": "guest-sync", "arguments": {"id": 1234}}
        expected = {'return': ga.guest_sync(1234)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_create_user_no_other_args(self):
        ga = GuestAgent()
        input = {"execute": "guest-sync", "arguments": {"id": 1234}}
        expected = {'return': ga.guest_sync(1234)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_create_user_only_home(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        input = {"execute": "create-user", "arguments": {"username": user_name, "create-home": True}}
        expected = {'return': ga.create_user(user_name, create_home=True)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_create_user_only_one_group(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        user_group = "kvm"
        input = {"execute": "create-user", "arguments": {"username": user_name, "groups": user_group}}
        expected = {'return': ga.create_user(user_name, groups=user_group)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_create_user_many_groups(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        user_group = ["kvm", "libvirt"]
        input = {"execute": "create-user", "arguments": {"username": user_name, "groups": user_group}}
        expected = {'return': ga.create_user(user_name, groups=user_group)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_create_user_group_and_home(self):
        ga = GuestAgent()
        user_name = "testtestuser"
        user_group = "kvm"
        input = {"execute": "create-user", "arguments": {"username": user_name, "groups": user_group, "create-home": True}}
        expected = {'return': ga.create_user(user_name, groups=user_group, create_home=True)}
        res = ga.execute_qmp(input)
        self.assertDictEqual(expected, res)

    def test_execute_get_osinfo(self):
        ga = GuestAgent()
        input = {'execute': "get-osinfo"}
        result = ga.execute_qmp(input)
        expected = {'return': ga.get_osinfo()}
        self.assertDictEqual(expected, result)

    def test_execute_deploy_ssh_pubkey(self):
        ga = GuestAgent()
        ssh_key = "test ssk key"
        user_name = "anothertestuser"
        input = {'execute': "deploy-ssh-pubkey", "arguments": {"username": user_name, "ssh-key": ssh_key}}
        result = ga.execute_qmp(input)
        expected = {'return': ga.deploy_ssh_pubkey(user_name, ssh_key)}
        self.assertDictEqual(expected, result)


class TestAgentCommands(unittest.TestCase):

    # test guest-sync
    def test_guest_sync(self):
        ga = GuestAgent()
        expected = 1234
        res = ga.guest_sync(1234)
        self.assertEqual(expected, res)

    def test_create_user_no_other_args(self):
        ga = GuestAgent()
        user_name = "testuser"
        ga.create_user(user_name)

        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        try:
            output = subprocess.check_output(('grep', 'testuser'),
                                             stdin=ps.stdout)
        except subprocess.CalledProcessError:
            self.debug("User not found")
        ps.wait()

        matched_users = set(l[:len(user_name)] for l in output.decode().split())
        self.assertTrue(user_name in matched_users)
        os.system("sudo userdel -r testuser")

    def test_create_user_only_home(self):
        ga = GuestAgent()
        user_name = "testuser"
        user_home = True
        ga.create_user(user_name, create_home=user_home)

        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        try:
            output = subprocess.check_output(('grep', "/home/{}".format(user_name)),
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

        matched_users = set(l[:len(user_name)] for l in output.decode().split())
        self.assertTrue(user_name in matched_users)
        os.system("sudo userdel -r testuser")

    def test_create_user_only_one_group(self):
        ga = GuestAgent()
        test_group = "libvirt"
        test_user = "testuser"
        ga.create_user(test_user, groups=test_group)
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        self.assertTrue(test_group in groups)
        os.system("sudo userdel testuser")

    def test_create_user_many_groups(self):
        ga = GuestAgent()
        test_groups = ["libvirt", "kvm", "sambashare"]
        test_user = "testuser"
        ga.create_user(test_user, groups=test_groups)
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        for group in test_groups:
            self.assertTrue(group in groups)
        os.system("sudo userdel testuser")

    def test_create_user_group_and_home(self):
        ga = GuestAgent()
        test_groups = ["libvirt", "kvm", "sambashare"]
        test_user = "testuser"
        test_home = True
        ga.create_user(test_user, create_home=test_home, groups=test_groups)

        # Find groups
        ps = subprocess.Popen(('groups', test_user),
                              stdout=subprocess.PIPE).stdout.read()
        groups = set(ps.decode()[:-1].split()[2:])
        for group in test_groups:
            self.assertTrue(group in groups)

        # Find home directory
        ps = subprocess.Popen(('less', '/etc/passwd'), stdout=subprocess.PIPE)
        try:
            subprocess.check_output(('grep', "/home/{}".format(test_user)),
                                    stdin=ps.stdout)
            ps.wait()
        except subprocess.CalledProcessError:
            self.debug("Home directory not found")
        os.system("sudo userdel testuser")

    def test_get_osinfo(self):
        ga = GuestAgent()
        info = platform.freedesktop_os_release()
        uname_info = os.uname()
        expected = {}
        expected["kernel-release"] = uname_info.release
        expected["kernel-version"] = uname_info.version
        expected["machine"] = uname_info.machine
        expected["name"] = info["NAME"]
        expected["prtty-name"] = info["PRETTY_NAME"]
        expected["version"] = info["VERSION"]
        expected["version-id"] = info["VERSION_ID"]

        result = ga.get_osinfo()
        self.assertDictEqual(expected, result)

    def test_deploy_ssh_pubkey(self):
        ga = GuestAgent()
        ssh_key = "ssh key test"
        ssh_user = "anothertestuser"
        ga.deploy_ssh_pubkey(ssh_user, ssh_key)
        f = open("/home/{}/.ssh/authorized_keys".format(ssh_user))
        self.assertTrue(ssh_key in f)


if __name__ == '__main__':
    unittest.main()
