import socket
from  threading import Thread
import time
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
BUFFER_SIZE = 4096
clients = {}

def ftp():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd","lftpd",".",perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer((IP_ADDRESS, PORT),handler)
    ftp_server.serve_forever()

def handleClient():
    pass

def acceptConnections():
    global SERVER
    global clients

    while True:
        clients, addr = SERVER.accept()
        clients_name = clients.recv(4096).decode().lower()
        clients[clients_name] = {
            "clients"        : clients,
            "address"        : addr,
            "connected_with" : "",
            "file_name"      : "",
            "file_size"      : 4096
        }
        print(f'Connection established with {clients_name} : {addr}')

        thread = Thread(target= handleClient, agrs = (clients,clients_name,))
        thread.start()

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    global PORT
    global SERVER
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind({IP_ADDRESS,PORT})

    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...")
    print("\n")

    acceptConnections()

setup_thread = Thread(target=setup)
setup_thread.start()

ftp_thread = Thread(target=ftp)
ftp_thread.start()