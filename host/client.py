import socket

PORT = 1234

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/ch.vsock")
s.send("CONNECT {}\nHello, world!".format(PORT).encode('utf-8'))

buf = s.recv(64)
buf = buf.decode('utf-8')
print(buf)
s.close()
