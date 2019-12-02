#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
import threading
from random import choice
#import signal
import time
import sys, select
from multiprocessing import Process


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

def instructions(client): #instruction format
    client.send(bytes("\n======================================================\n\nThis 1 2 3 pass cmd game simulates the real life card game.\n\nTo enter the game, you must input \"{start}.\" The game will\nstart once there are at least 3 players, and all players in\nthe lobby has all input \"{start}\"\n\nAfter the cards are distributed, the cards will immediately\nstart, counting down form 1 to 3. In that time span, you must\nalready input the card you wish to pass. If you fail to do so,\nthen the game will just randomly choose which card to pass from\nyour deck.\n\nThis game will continue until someone completes a rank. If you\nthink you have completed a rank, type the command \" {down} .\"\nIf it turns out you do have a complete rank, then you are\nthe Winner, and the game ends.\n\n======================================================\n[{start}] Enter Game\n[{quit}] Exit", "utf8"))


def accept_incoming_connections(): #Sets up handling for incoming clients.
    print("accept_incoming_connections")

    while True:
        client, client_address = SERVER.accept()
        print(clients)
        print("%s:%s has connected." % client_address)
        client.send(bytes("\n======================================================\nEnter Player name below:", "utf8"))
        addresses[client] = client_address
        client_cards[client] = []
        threading.Thread(target=handle_client, args=(client,)).start()

def card_distrib(): #distributes the generated hands
    print("card_distrib")

    randomize_deck(len(clients), hands)
    
    cnt = 0
    
    for client in clients:
        client_cards[client] = hands[cnt]
        cnt+=1
    
    for client in client_cards:
        cards = ''
        for i in range(len(client_cards[client])):
            if i == 0:
                temp = str(client_cards[client][i])
                cards = cards + temp
            else:
                temp = str(client_cards[client][i])
                cards = cards + ', ' + temp
        print(str(clients[client])+':'+cards)
        client.send(bytes("\n======================================================\nHere are your cards: " + cards+"\n======================================================\n", "utf8"))

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
                start_game()

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

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    print("broadcast")

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def handle_time(client):
   count = 0
   while count <= 3:
      time.sleep(2)
      count += 1
      client.send(bytes(str(count) + "... ", "utf8"))
      if count == 3:
        print("in")
        allowed = 1
        return

def handle_pass(client):
    '''signal.alarm(TIMEOUT)
    s = input_t(client)
    # disable the alarm after success
    signal.alarm(0)
    client.send(bytes("You typed"+ s, "utf8"))'''
    client.send(bytes("You have three seconds to pass!","utf8"))
    t1 = Process(target=handle_time, args=(client,))
    t1.start()
    #i, o, e = select.select( [sys.stdin], [], [], 10 )
    while allowed != 1:
        print("in- allowed")
        inp = client.recv(BUFSIZ).decode("utf8")
        print(inp)

    print(allowed)
    if inp!="":
        print("meep")
        client.send(bytes("You said"+ inp, "utf8"))
    else:
        client.send(bytes("You said nothing!","utf8"))

    t1.terminate()
    t1.join()

def start_game():
    print("start_game")
    broadcast(bytes("\n======================================================\nThe game has started. Cards are being distributed\n======================================================\n", "utf8"))
    
    card_distrib()
    
    for client in clients:
        print(client)
        client.send(bytes("Pass in the count of three...", "utf8"))
        threading.Thread(target=handle_pass, args=(client,)).start()
        



TIMEOUT = 5
passed = {}
clients = {}
client_cards = {}
players = []
hands = []
addresses = {}
allowed = 0

HOST = ''
PORT = int(input("Enter game port: "))
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
