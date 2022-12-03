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

'''
while not joined:
    command = input()
    command.split()
    if command[0] == "/join":
        if command[1] == "127.0.0.1":
            if command[2] =="3000":
                joined = True
            else:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        else:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
    elif command[0] == "/leave":
        print("Error: Disconnection failed. Please connect to the server first.")
    else:
        print("Error: Command not found.")
'''
while not joined:
    command = input()
    command = command.split()
    print("Enter command: ")
    if command[0] == "/join":
        try:
            ip_adress = command[1]
            host = int(command[2])
            UDPClientSocket.sendto(bytes(json.dumps(join_command), "utf-8"), (ip_adress, host))
        except:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        finally:
            #testing purposes to see if connected sa server
            msgFromClient       = "Hello UDP Server"
            bytesToSend         = str.encode(msgFromClient)
            serverAddressPort   = ("127.0.0.1", 3000)
            bufferSize          = 1024
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    elif command[0] == "/?":
        helperCall()
    elif command[0] == "/leave":
        print("Error: Disconnection failed. Please connect to the server first.")
    

    



    

        





msg = "Message from Server {}".format(msgFromServer[0])

print(msg)

'''
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000,9000))) #ig this is not needed? since the server is already binded and theres port numbers nman

name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(2048)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"Online Tag: {name}".encode(), ("localhost", 3000)) #localhost, 3000 should be in func so they can input custom IP and port number

while True:
    message = input("")
    if message == "!leave":
        print("Left the chat...")
        exit()
    elif message == "/?":
        helperCall()
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", 3000))
'''