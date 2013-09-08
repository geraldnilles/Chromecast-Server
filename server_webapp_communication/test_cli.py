#--------------------
# Test CLI
#
# This is a tool for manually sending commands through the WS Proxy
#-------------------


import socket,sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",40404))
s.settimeout(5)

s.sendall(sys.argv[1])

print s.recv(1024)

