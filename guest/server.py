import socket
import struct
import fcntl

with open("/dev/vsock", "rb") as fd:
    r = fcntl.ioctl(fd, socket.IOCTL_VM_SOCKETS_GET_LOCAL_CID, "    ")
    CID = struct.unpack("I", r)[0]
    #print("Local CID: {}".format(CID))

PORT = 1234

s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
s.settimeout(None)
s.bind((CID, PORT))
s.listen()

(conn, (remote_cid, remote_port)) = s.accept()

#print(f"Connection opened by cid={remote_cid} port={remote_port}")

while True:
    buf = conn.recv(64)
    if not buf:
        break
    buf = buf.decode('utf-8')
    print("Received: {}".format(buf))
