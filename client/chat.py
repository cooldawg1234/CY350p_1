import socket
import time

address = 'localhost'
port = 12000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cs:
    cs.connect((address, port))
    cs.settimeout(1)