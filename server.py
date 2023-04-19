import socket, threading
IP = socket.gethostbyname(socket.gethostname())

port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, port))
server.listen()

clients = []
nicknames = []
addresses = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            message_content = message.decode('ascii')
            if message_content[:4] == 'SEND':
                print(addresses)
                client.send(addresses[nicknames.index(message_content[5:])].encode('ascii'))
            else:
            # message = nicknames[(clients.index(client))] + ': ' + message_content
            # message.encode('ascii')
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print('Connected with {}'.format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        addresses.append(str(address))
        print('Nickname is {}'.format(nickname))
        broadcast('{} joined'.format(nickname).encode('ascii'))
        client.send('Connected to server'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()