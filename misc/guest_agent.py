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
        If the command does not exist, raise an error.

        '''
        raise NotImplementedError
    
    def guest_sync(num):
        '''
        Return the number passed to the guest agent
        '''
        raise NotImplementedError
    
    def send_response(qmp_response):
        '''
        send the response in qmp format back to the host VM
        '''
        raise NotImplementedError


if __name__ == '__main__':
    pass