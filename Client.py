import socket
import json
import threading
import re
'''
msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
'''
join_command = {"command": "join"}
leave_command = {"command": "leave"}
register_command = {"command": "register", "handle": "handle"}
all_message_command = {"command": "all", "message": "message"}
direct_message_command = {"command": "msg", "handle": "handle", "message": "message"}
error_command = {"command": "error", "message": "message"}

bufferSize = 1024
joined = False
registered = False

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def helperCall():
    print("\nList of Commands: ")
    print("/join <server ip addr> <port>    - connects to the server ")
    print("/leave                           - leaves the chat ")
    print("/register <handle>               - set a handle or a nickname ")
    print("/all                             - messages all clients connected in the server ")
    print("/msg <handle>                    - messages to another client privately rather than all clients ")
    print("/?                               - list of commands ")

def receive_join():
    while True:
        try:
            data = UDPClientSocket.recvfrom(1024)
            #json_data = json.loads(data.decode("utf-8"))
            print("Connection to the Message Board Server is successful!") 
            return True
        except:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.") 
            return False
        
def receive():
    while True:
            data= UDPClientSocket.recvfrom(1024)
            json_data = json.loads(data.decode("utf-8"))
            if json_data["command"] == "error":
                print(json_data["error"])
            else:
                print("")



while joined == False:
    command = input("Enter /join <ip adress> <portnum> to join a server \n")
    command = command.split()
    if command[0] == "/join":
        ip_adress = command[1]
        try:
            host = int(command[2])
            UDPClientSocket.sendto(bytes(json.dumps(join_command), "utf-8"), (ip_adress, host))
        except:
            pass
        joined = receive_join()
    elif command[0] == "/?":
        helperCall()
    elif command[0] =="/leave":
        print("Error: Disconnection failed. Please connect to the server first.")
    elif command[0] =="/register":
        print("Please connect to the server first before creating a handle")
    elif command[0] =="/all" or command[0] =="/msg":
        print("Please connect to the server first before sending a message")

t1 = threading.Thread(target=receive)
t1.start()

while joined and not registered:
    command = input("Enter /register <handle> to join a server \n")
    numwords = len(re.findall(r'\w+', command))
    print(numwords)
    command = command.split()
    if command[0] == "/register":
        if numwords >= 3:
            print("Only input the very first name")
        else:
            register_command["handle"] = command[1]
            UDPClientSocket.sendto(bytes(json.dumps(register_command), "utf-8"), (ip_adress, host))
            
    

