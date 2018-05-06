#!/usr/bin/env python3
# Chat Server
# brady maxwell 177245IVCM

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import linesep

clients = {}
clientAddresses = {}
host = ''
port = 33333
bufferSize = 256
serverAddress = (host, port)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(serverAddress)

# handle client setup
def newClientRequest():
    while True:
        client, clientAdder = SERVER.accept()

        client.send(bytes("Welcome to BEM Chat! " + "\n" +
                          "Enter your name: ", "utf8"))
        clientAddresses[client] = clientAdder
        #print(clientAddresses)
        print("%s:%s has connected.\n" % clientAdder)
        Thread(target=handleClient, args=(client,)).start()

def handleClient(client):  # Takes client socket as argument.
    #hadle a client connection
    name = client.recv(bufferSize).decode("utf8")
    welcome = 'Welcome %s! \n' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!\n" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(bufferSize)
        if msg != bytes("{KillSocket}", "utf8"):
            broadcast(msg, name+": ")
            print(name, msg)
        else:
            client.close()
            print("%s disconnected")
            print("removing " + clients[client])
            del clients[client]
            broadcast(bytes("%s has left the chat.\n" % name, "utf8"))
            break

def broadcast(msg, prefix=""):  # prefix is for name identification.
    # broadcast recieved messages to other connected clients
     for sock in clients:

        sock.send(bytes(prefix, "utf8")+msg )

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Server starting...\n")
    print("Waiting for chat clients to connect...\n")
    ACCEPT_THREAD = Thread(target=newClientRequest)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
