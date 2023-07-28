import socket
import struct
import fcntl
import json


with open("/dev/vsock", "rb") as fd:
    r = fcntl.ioctl(fd, socket.IOCTL_VM_SOCKETS_GET_LOCAL_CID, "    ")
    CID = struct.unpack("I", r)[0]


PORT = 1234

s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
s.settimeout(None)
s.bind((CID, PORT))
s.listen()

(conn, (remote_cid, remote_port)) = s.accept()

while True:
    buf = conn.recv(4096)
    if not buf:
        break
    buf = json.loads(buf.decode('utf-8'))
    print("Received: \n{}".format(buf))
    print(type(buf))
    break

response = "hello from server"
conn.send(response.encode())
conn.close()
