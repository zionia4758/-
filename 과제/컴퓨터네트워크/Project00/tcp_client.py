import socket

HOST='127.0.0.1'
PORT=4779
BUFFER=4096

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
sock.send('Hello,tcpServer!'.encode())

recv=sock.recv(BUFFER)
print('[tcpServer said]: %s'%recv.decode())
sock.close()
