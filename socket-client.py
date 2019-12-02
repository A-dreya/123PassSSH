#!/usr/bin/env python3

from socket import *
from threading import Thread
from os import system, name 
from time import sleep 
  
#clears the command prompt every other turn
def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear') 

def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if msg == "{quit}":
            client_socket.close()
            break
        if not msg:
            break
        print(msg)


def send():
    while True:
    	msg = input()
    	#clear()
    	client_socket.send(bytes(msg, "utf8"))
    	if msg == "{quit}":
    		break


HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = input('Enter port: ')
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()