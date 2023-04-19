import socket, threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

nicknames = []
addresses = []

def receive():
    while True:
        client, address = server.accept()
        #ask for nickname to each client
        nicknames.append(nickname)
        addresses.append(address)
        