import socket, threading
import msgpack

IP = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP, 8000))

def receive():
    while True:
        try:
            req = server.recv(1024)
            req_obj = msgpack.unpackb(req, raw=False)
            if req_obj['type'] == 'server_req':
                if req_obj['payload'] == 'USERNAME':
                    username = input('Enter your Username: ')
                    res = {'type': 'server_res', 'payload': username}
                    res = msgpack.packb(res, use_bin_type=True)
                    server.send(res)
                elif req_obj['payload'] == 'DESTINATION':
                    destination = input('Enter username to connect with: ')
                    res = {'type': 'server_res', 'payload': destination}
                    res = msgpack.packb(res, use_bin_type=True)
                    server.send(res)
            
        except:
            #errors
            print("An error occured")
            server.close()
            break

def write():
    while True:
        message = input('')
        req = {'type': 'client_req', 'payload': message}
        req = msgpack.packb(req, use_bin_type=True)
        server.send(req)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()