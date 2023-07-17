class GuestAgent:
    def __init__(self):
        '''
        Initialize the guest agent to be in a listening state
        '''
        raise NotImplementedError

    def execute_qmp(qmp_command):
        '''
        Calls the function associated with the qmp command provided.
        Parses the QMP command to also input correct arguments to function.
        If the command does not exist, raise" an error.
        '''
        raise NotImplementedError

    def guest_sync(num):
        '''
        Return the number passed to the guest agent
        '''
        raise NotImplementedError

    def create_user(username, groups=None, home=None):
        '''
        Create a user with the provided username. If groups and home provided,
        include the user in those groups and with that home directory
        '''
        raise NotImplementedError

    def get_osinfo():
        '''
        gets info about the os on which the guest is running.
        Info includes kernel release, kernel version, machine, id and name.
        '''
        raise NotImplementedError

    def deploy_ssh_pubkey(username, ssh_key):
        '''
        add an authroized ssh key to a given user account
        '''
        raise NotImplementedError

    def send_response(qmp_response):
        '''
        send the response in qmp format back to the host VM
        '''
        raise NotImplementedError


if __name__ == '__main__':
    pass
