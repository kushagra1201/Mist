import socket
import threading
import select
import msgpack

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sockets_list = [server_socket]

def receive_msg(client_socket):
    message_type = client_socket.recv(1024).decode('utf-8')
    if not len(message_type):
        raise Exception(msg='Client closed the connection')
    elif message_type not in ('n', 'r'):
        raise Exception(msg='Invalid message type in header')
    else:
        message_len = int(client_socket.recv(1024).decode('utf-8'))
        return {'type': message_type, 'uname': client_socket.recv(1024)}

def read_handler(notified_socket: socket.socket):
    global clients
    global sockets_list
    if notified_socket == server_socket:
        client_socket, client_addr = server_socket.accept()
        try:
            user_data = receive_msg(client_socket)
            if user_data['type'] == 'n':
                sockets_list.append(client_socket)
                clients[user_data['uname']] = client_addr
                print(f"Accepted new connection from {client_addr[0]}:{client_addr[1]} username: {user_data['uname']}")
            else:
                print(f"Bad request from {client_addr}")
        except Exception as e:
            print(f"Exception: {e.msg}")
            return
    else:
        try:
            request = receive_msg(notified_socket)
            if request['type'] == 'r':
                response_data = clients.get(request['uname'])
                if response_data is not None:
                    data: bytes = msgpack.packb(response_data)
                    notified_socket.send(data)
                else:
                    print('Username {request['uname']} not found')
                    return
            else:
                print(f'Bad request from {notified_socket.getpeername()}')
                return
        except Exception as e:
            sockets_list.remove(notified_socket)
            for uname, addr in clients.items:
                if addr == notified_socket.getpeername():
                    del clients[uname]
                    break
            print(f"Exception: {e.msg}")
            return

while True:
    read_sockets: list[socket.socket]
    exception_sockets: list[socket.socket]

    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list) # this refers to the sockets which are readable, writable or have any exceptions 
    for notified_socket in read_sockets:
        thread = threading.Thread(target=read_handler, args=(notified_socket,))
        thread.start()

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]