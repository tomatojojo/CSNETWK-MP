import socket
import threading
import random
import json

join_command = {"command": "join"}
leave_command = {"command": "leave"}
register_command = {"command": "register", "handle": "handle"}
all_message_command = {"command": "all", "message": "message"}
direct_message_command = {"command": "msg", "handle": "handle", "message": "message"}
error_command = {"command": "error", "message": "message"}

BUFFER_SIZE = 1024
connectIP = None
connectPort = None

joined = False

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def helperCall():
    print("\nList of Commands: ")
    print("/join <server ip addr> <port>    - connects to the server ")
    print("/leave                           - leaves the chat ")
    print("/register <handle>               - set a handle or a nickname ")
    print("/all                             - messages all clients connected in the server ")
    print("/msg <handle>                    - messages to another client privately rather than all clients ")
    print("/?                               - list of commands ")

def clientReceiver():
    while True:
        try:
            receiveMessage = UDPClientSocket.recvfrom(BUFFER_SIZE)[0].decode()
            receiver = json.loads(receiveMessage)

            if(receiver["command"] == "join"):
                print("Connection to the Message Board Server is successful.")

            elif(receiver["command"] == "leave"):
                print("Connection closed. Thank you.")

            elif(receiver["command"] == "register"):
                print("Welcome " + "insert handle here")

            elif(receiver["command"] == "msg"):
                print("idk")
            else:
                print("error", "Unrecognized command format")
            

        except:
            pass




while not joined:
    command = input()
    command = command.split()
    if command[0] == "/join":
        try:
            ip_adress = command[1]
            host = int(command[2])
            UDPClientSocket.sendto(bytes(json.dumps(join_command), "utf-8"), (ip_adress, host))

            joined = True

        except socket.gaierror:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

    elif command[0] == "/?":
        helperCall()

