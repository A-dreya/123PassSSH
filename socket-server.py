#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(clients)
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    print(client)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the game!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    ready = 0;

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{start}", "utf8"):
        	print(name + msg.decode("utf-8"))
        	for p in players:
        		print("p:" + p)
        		if name == p:
        			client.send(bytes("You already confirmed. Waiting for other players", "utf8"))
        			ready = 1
        			break
        		else:
        			continue
        	if ready == 0:
        		players.append(name)
        	print(players)
        	if len(players) >= 3 and len(players) == len(clients):
        		start_game()
        	elif len(players) < 3:
        		broadcast(bytes("There must be at least 3 players to start game. Currently there are " + str(len(players)), "utf8"))
        	else:
        		broadcast(bytes("Waiting for other players to confirm. "+ str(len(players)) +"/" + str(len(clients)) + " are confirmed", "utf8"))
        elif msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def start_game():
	broadcast(bytes("The game has started", "utf8"))

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
players = []
addresses = {}

HOST = ''
PORT = int(input())
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()