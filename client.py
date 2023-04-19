import socket, threading
nickname = input("Choose your nickname: ")
IP = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((IP, 8000))

def receive():
    while True:
        try:
            message = server.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                server.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured")
            server.close()
            break

def write():
    while True:
        message = input('')
        server.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()