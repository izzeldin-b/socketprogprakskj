import socket
import threading
port = 1234
SIZE = 4096
FORMAT = 'utf-8'
disconnectmsg = '!dissconect'

clientlist = []

def client_handle(conn, addr) :
    connection = True
    while connection :
        msg = conn.recv(SIZE)
        if msg == disconnectmsg :
            connection = False
        sendmes(msg, conn)
    conn.close()

def sendmes(msg, connect) :
    msgsend = 'message recived : '
    for clients in clientlist:
        if clients != connect :
            clients.send(msgsend.encode(FORMAT))
            clients.send(msg)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server is starting')
    server.bind(('127.0.0.1', port))
    server.listen()
    print(f'server is listing on port {port}')
    while True :
        conn, addr = server.accept()
        thread = threading.Thread(target= client_handle, args= (conn, addr))
        thread.start()
        clientlist.append(conn)
        print(f'the number of active connection is {threading.active_count() - 1}')
    server.close()


if __name__ == "__main__":
    main()

