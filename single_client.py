import socket, threading
nickname = input("Choose your nickname: ")

IP = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((IP, 8000))

def receive():
    while True:
        try: 
            message = server.recv(1024)
            if message == 'NICKNAME':
                server.send(nickname)
            else:
                print(message)
        except:
            print("An error occured")
            server.close()
            break