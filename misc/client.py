import socket
import qmp_formatter
from client_parser import build_parser

cmd = build_parser()
print(cmd)
PORT = 1234
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/ch.vsock")
s.send("CONNECT {}\n{}".format(PORT, cmd).encode('utf-8'))

buf1 = s.recv(4096)
buf2 = s.recv(4096).decode('utf-8')
print(buf2)