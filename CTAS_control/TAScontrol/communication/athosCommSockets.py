import socket

zsamoHOST = '192.168.0.102'
zsamoPORT = 4973

global zsamoSocket

zsamoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
zsamoSocket.connect((zsamoHOST, zsamoPORT))