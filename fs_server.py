import socket, threading
import msgpack

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

nicknames = []
addresses = []

def handle(client):
    while True:
        try:
            req = client.recv(1024)
            req = msgpack.unpackb(req, raw=False)
            message = req['payload']
            if(message == 'CONNECT'):
                res = {'type': 'server_req', 'payload': 'DESTINATION'}
                res = msgpack.packb(res, use_bin_type=True)
                client.send(res)
            
        except:


def receive():
    while True:
        client, address = server.accept()
        #ask for nickname to each client
        req = {'type': 'server_req', 'payload': 'USERNAME'}
        req = msgpack.packb(req, use_bin_type=True)
        client.send(req)
        res = client.recv(1024)
        res = msgpack.unpackb(res, raw = False)
        nickname = res['payload']
        nicknames.append(nickname)
        addresses.append(str(address))
        print('Nickname is {}'.format(nickname))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
receive()