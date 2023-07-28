import socket
import argparse

PORT = 1234

# Collect JSON string from command line
parser = argparse.ArgumentParser()
parser.add_argument("command", help="""the command you wish to send to the guest agent.
                            Must be fomatted in QEMU Monitor Protocol(QMP)""")
json_string = parser.parse_args().command
print(json_string)

# Connect to UNIX socket to send raw data
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/ch.vsock")
s.sendall("CONNECT {}\n{}".format(PORT, json_string).encode('utf-8'))

# Recieve guest response and parse
ok_buf = s.recv(64)
buf2 = s.recv(64)
ok_buf = ok_buf.decode('utf-8')
buf2 = buf2.decode('utf-8')
print(ok_buf)
print(buf2)
s.close()
