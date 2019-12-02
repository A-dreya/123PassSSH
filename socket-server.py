#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from random import choice

def randomize_deck(client_cnt, hands):  #generates player hands
    print("randomize_deck") #detection
    
    deck = []

    #generates cards to be used
    for i in range(1,len(clients)+1):
        if i == 1:
            deck.append("DA")
            deck.append("HA")
            deck.append("SA")
            deck.append("CA")
        elif i == 11:
            deck.append("DJ")
            deck.append("HJ")
            deck.append("SJ")
            deck.append("CJ")
        elif i == 12:
            deck.append("DQ")
            deck.append("HQ")
            deck.append("SQ")
            deck.append("CQ")
        elif i == 13:
            deck.append("DK")
            deck.append("HK")
            deck.append("SK")
            deck.append("CK")
        else:
            deck.append("D"+str(i))
            deck.append("H"+str(i))
            deck.append("S"+str(i))
            deck.append("C"+str(i))
    
    #groups chosen cards into fours
    for i in range(client_cnt):
        hand = []
        for j in range(4):
            card = choice(deck)
            hand.append(card)
            deck.remove(card)
        hands.append(tuple(hand[:]))
        hand.clear()
    print(str(hands))


def mainMenu(client): #main menu format
	client.send(bytes("\n======================================================\n ooo   oooo   oooo    oooooo   ooooo    ooooo  ooooo\no oo  o  oo      oo   oo    o oo    o  ooo    ooo\n  oo    oo    ooo     oooooo  ooooooo   oooo   oooo\n  oo   oo        oo   oo      oo    o     ooo    ooo\nooooo oooooo  oooo    oo      oo    o  ooooo  ooooo\n======================================================\n[{start}] Enter\n[{help}] Instructions\n[{quit}] Exit", "utf8"))

def instructions(client): #main menu format
    client.send(bytes("\n======================================================\n\nThis 1 2 3 pass cmd game simulates the real life card game.\n\nTo enter the game, you must input \"{start}.\" The game will\nstart once there are at least 3 players, and all players in\nthe lobby has all input \"{start}\"\n\nAfter the cards are distributed, the cards will immediately\nstart, counting down form 1 to 3. In that time span, you must\nalready input the card you wish to pass. If you fail to do so,\nthen the game will just randomly choose which card to pass from\nyour deck.\n\nThis game will continue until someone completes a rank. If you\nthink you have completed a rank, type the command \" {down} .\"\nIf it turns out you do have a complete rank, then you are\nthe Winner, and the game ends.\n\n======================================================\n[{start}] Enter Game\n[{quit}] Exit", "utf8"))


def accept_incoming_connections():
    print("accept_incoming_connections")
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(clients)
        print("%s:%s has connected." % client_address)
        client.send(bytes("Enter Player name: \t", "utf8"))
        addresses[client] = client_address
        client_cards[client] = []
        Thread(target=handle_client, args=(client,)).start()

def card_distrib():
    print("card_distrib")
    randomize_deck(len(clients), hands)
    cnt = 0
    for client in clients:
        client_cards[client] = hands[cnt]
        cnt+=1
    for client in client_cards:
        cards = ''
        for i in range(len(client_cards[client])):
            # print((client_cards[client])[i])
            if i == 0:
                temp = str(client_cards[client][i])
                cards = cards + temp
            else:
                temp = str(client_cards[client][i])
                cards = cards + ', ' + temp
        print(str(clients[client])+':'+cards)
        client.send(bytes("\n======================================================\nHere are your cards: " + cards+"\n======================================================\n", "utf8"))
        # print(client_cards[client])

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    print("handle_client")

    name = client.recv(BUFSIZ).decode("utf8")
    print(client)
    welcome = 'Welcome %s!' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the game!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    ready = 0;
    mainMenu(client)

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{start}", "utf8"):
            print(name + msg.decode("utf-8"))
            for p in players:
                print("p:" + p)
                if name == p:
                    client.send(bytes("\n======================================================\nYou already confirmed. Waiting for other players\n======================================================\n", "utf8"))
                    ready = 1
                    break
                else:
                    continue
            if ready == 0:
                players.append(name)
            print(players)
            if len(players) >= 3 and len(players) == len(clients):
                start_game(client)

            elif len(players) < 3:
                broadcast(bytes("\n======================================================\n" + name + " has confirmed. There must be at least 3 players to start game. Currently there are " + str(len(players)), "utf8"))
            else:
                broadcast(bytes("\n======================================================\n" + name + " has confirmed. Waiting for other players to confirm. "+ str(len(players)) +"/" + str(len(clients)) + " are confirmed", "utf8"))
        elif msg == bytes("{help}", "utf8"):
            instructions(client)
            continue
        elif msg != bytes("{quit}", "utf8"):
            continue
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def start_game(client):
    print("start_game")
    broadcast(bytes("\n======================================================\nThe game has started. Cards are being distributed\n======================================================\n", "utf8"))
    card_distrib()
    client.send(bytes("Pass in Three seconds", "utf8"))

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    print("broadcast")

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
client_cards = {}
players = []
hands = []
addresses = {}

HOST = ''
PORT = int(input("Enter game port: "))
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
