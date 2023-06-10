import socket
import threading
import select
import msgpack

IP = socket.gethostbyname(socket.gethostname())
PORT = 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sockets_list = [server_socket]

