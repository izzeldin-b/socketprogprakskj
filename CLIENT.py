import socket
import threading
port = 1234
SIZE = 4096
FORMAT = 'utf-8'
disconnectmsg = '!dissconect'


def getmsg(client):
    while True :
        print(client.recv(SIZE).decode(FORMAT))
        global status
        status = True
        if status == False :
            break

client = socket.socket()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', port))
    print('client connected')
    threading._start_new_thread(getmsg, (client, ))
    while True :
        status = True
        msg = input()
        client.send(msg.encode())
        if msg == disconnectmsg :
            status = False
            client.close()
            break
            

    


if __name__ == '__main__':
    main()
