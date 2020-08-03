import socket
#from TAScontrol.user_commands.commands import rallh



#statusHOST = '148.6.120.29'    # The address of the status host
statusHOST = '192.168.0.102'
statusPORT = 4973
#commandHOST = '148.6.120.29'   # The address of the command host
commandHOST = '192.168.0.102'
commandPORT = 4975

global statusSocket
global commandSocket

statusSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
statusSocket.connect((statusHOST, statusPORT))

commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
commandSocket.connect((commandHOST, commandPORT))

#rallh()
