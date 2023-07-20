import os
import platform
import socket
import struct
import fcntl
import json

class GuestAgent:
    def __init__(self):
        '''
        Initialize the guest agent to be in a listening state
        '''
        self.command = None
        while True:
            self.vsock_listener()

    def vsock_listener(self):
        with open("/dev/vsock", "rb") as fd:
            r = fcntl.ioctl(fd, socket.IOCTL_VM_SOCKETS_GET_LOCAL_CID, "    ")
            CID = struct.unpack("I", r)[0]


        PORT = 1234

        s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        s.settimeout(None)
        s.bind((CID, PORT))
        s.listen()

        (conn, (remote_cid, remote_port)) = s.accept()
        buf = None
        while True:
            buf = conn.recv(128)
            if not buf:
                break
            print(buf)
            buf = json.loads(buf.decode('utf-8'))
            print("Received: \n{}".format(buf))
            # print(type(buf))
            break

        response = str(self.execute_qmp(buf))
        conn.send(response.encode())
        conn.close()

    def execute_qmp(self, qmp_command):
        '''
        Calls the function associated with the qmp command provided.
        Parses the QMP command to also input correct arguments to function.
        If the command does not exist, raise" an error.
        '''
        ret = None
        command = qmp_command['execute']
        self.command = command
        if 'arguments' in qmp_command:
            arguments = qmp_command['arguments']

        if command == "guest-sync":
            ret = self.guest_sync(arguments["id"])
        elif command == "create-user":
            if 'create-home' in arguments:
                if 'groups' in arguments:
                    ret = self.create_user(arguments['username'], groups=arguments['groups'], create_home=arguments['create-home'])
                else:
                    ret = self.create_user(arguments['username'], create_home=arguments['create-home'])
            elif 'groups' in arguments:
                ret = self.create_user(arguments['username'], groups=arguments['groups'])
            else:
                ret = self.create_user(arguments['username'])

        elif command == "get-osinfo":
            ret = self.get_osinfo()
        elif command == "deploy-ssh-pubkey":
            ret = self.deploy_ssh_pubkey(arguments["username"], arguments["ssh-key"])
        else:
            raise Exception("Command {} not recognized".format(command))
        
        return {'return': ret}

    def guest_sync(self, num):
        '''
        Return the number passed to the guest agent
        '''
        return num

    def create_user(self, username, groups=None, create_home=False):
        '''
        Create a user with the provided username. If groups and home provided,
        include the user in those groups and with that home directory
        '''
        ret_val = [False, False]
        home = ""
        groups_in = ""
        if create_home:
            home = "-m "
            ret_val[0] = True
        if groups is not None:
            ret_val[1] = True
            if isinstance(groups, list):
                groups_in = "--groups " + ",".join(groups) + " "
            elif isinstance(groups, str):
                groups_in = "--groups {} ".format(groups)
                
        cmd = "useradd {}{}{}".format(home, groups_in, username)
        os.system(cmd)
        return ret_val
    
    def get_osinfo(self):
        '''
        gets info about the os on which the guest is running.
        Info includes kernel release, kernel version, machine, id and name.
        '''
        info = platform.freedesktop_os_release()
        uname_info = os.uname()
        os_info = {}
        os_info["kernel-release"] = uname_info.release
        os_info["kernel-version"] = uname_info.version
        os_info["machine"] = uname_info.machine
        os_info["name"] = info["NAME"]
        os_info["prtty-name"] = info["PRETTY_NAME"]
        os_info["version"] = info["VERSION"]
        os_info["version-id"] = info["VERSION_ID"]

        return os_info

    def deploy_ssh_pubkey(self, username, ssh_key):
        '''
        add an authroized ssh key to a given user account
        '''
        path = '/home/{}/.ssh/'.format(username)
        if not os.path.exists(path):
            os.makedirs(path)

        filename = 'authorized_keys'
        if not os.path.exists(os.path.join(path, filename)):
            f = open(os.path.join(path, filename), 'w')
        else:
            f = open(os.path.join(path, filename), 'a')

        f.write("\n" + ssh_key + "\n")

        return 0

    def send_response(self, qmp_response):
        '''
        send the response in qmp format back to the host VM
        '''
        raise NotImplementedError


if __name__ == '__main__':
    GuestAgent()
