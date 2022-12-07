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
global registered
registered = False

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def helperCall():
    print("\n---------------------------------------------------------------------------------------------------------")
    print("|   List of Commands:                |    Function                                                      |")
    print("|-------------------------------------------------------------------------------------------------------|")
    print("|   /join <server ip addr> <port>    |    connects to the server                                        |")
    print("|   /leave                           |    leaves the chat                                               |")
    print("|   /register <handle>               |    set a handle or a nickname                                    |")
    print("|   /all <message>                   |    messages all clients connected in the server                  |")
    print("|   /msg <handle> <message>          |    messages to another client privately rather than all clients  |")
    print("|   /?                               |    list of commands                                              |")
    print("---------------------------------------------------------------------------------------------------------")
    print("\n")

def receive_join():
    while True:
            try:
                data, _ = UDPClientSocket.recvfrom(1024)
                #json_data = json.loads(data.decode("utf-8"))
                data = data.decode()
                print(data) 
                return True
            except:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                return False
        
def receive():
        data, _ = UDPClientSocket.recvfrom(1024)
        data = data.decode()
        data_splitted = data.split()
        if data_splitted[0] == "Error:":
            print(data)
            if registered == False:
                registered = False
        elif data_splitted[0] == "Welcome!":
            print(data)
            if registered == False:
                registered = True
        else:
            print(data)
#senderResponse


while True:
    while joined == False:
        command = input("Enter /join <ip adress> <portnum> to join a server \n")
        numwords = len(command.split())
        print(numwords)
        command = command.split()
        if command[0] == "/join":
            if numwords != 3:
                print("Error: Command parameters do not match or is not allowed.")
            else:
                ip_adress = command[1]
                try:
                    host = int(command[2])
                    print("converted host")
                    UDPClientSocket.sendto(bytes(json.dumps(join_command), "utf-8"), (ip_adress, host))
                    print("json sent")
                    joined = receive_join()
                    print("joined")
                except:
                    print("Error: Command parameters do not match or is not allowed.")
                
        elif command[0] == "/?":
            if numwords > 1: 
                print("Error: Command parameters do not match or is not allowed.")
            else:
                helperCall()
        elif command[0] =="/leave":
            if numwords > 1: 
                print("Error: Command parameters do not match or is not allowed.")
            else:
                print("Error: Disconnection failed. Please connect to the server first.")
        elif command[0] =="/register":
            if numwords != 2:
                print("Error: Command parameters do not match or is not allowed.")
            else:
                print("Please connect to the server first before creating a handle")
        elif command[0] =="/all":
            if numwords < 2:
                print("Error: Command parameters do not match or is not allowed.")
            else:
                print("Please connect to the server first before sending a message")
        elif command[0] =="/msg":
            if numwords <= 2:
                print("Error: Command parameters do not match or is not allowed.")
            else:
                print("Please connect to the server first before sending a message")
        else:
            print("Error: Command not found.")

    t1 = threading.Thread(target=receive)
    t1.start()

    while joined and not registered:
        command = input("Enter /register <handle> to join a server \n")
        numwords = len(command.split())
        command = command.split()
        if command[0] == "/register":
            if numwords != 2:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                register_command["handle"] = command[1]
                UDPClientSocket.sendto(bytes(json.dumps(register_command), "utf-8"), (ip_adress, host))
        elif command[0] == "/leave":
            if numwords > 1:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                joined = False
                UDPClientSocket.sendto(bytes(json.dumps(leave_command), "utf-8"), (ip_adress, host))
        elif command[0] == "/join":
            if numwords > 1:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                error_command["message"] = "You have already joined the server"
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
        elif command[0] =="/all":
            if numwords < 2:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                error_command["message"] = "Please connect to the server first before sending a message to all"
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
        elif command[0] =="/msg":
            if numwords <= 2:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                error_command["message"] = "Please connect to the server first before sending a message to another client"
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
        elif command[0] == "/?":
            if numwords > 1: 
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                helperCall()
        else:
                error_command["message"] = "Error: Command not found."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))


    while joined and registered:
        command = input("Enter command: \n")
        numwords = len(command.split())
        command = command.split()

        if command[0] == "/leave":
            #insert serverPort and serverIP to None or 0
            if numwords > 1:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                joined = False
                registered = False
                UDPClientSocket.sendto(bytes(json.dumps(leave_command), "utf-8"), (ip_adress, host))
        elif command[0] == "/register":
            if numwords != 2:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                error_command["message"] = "Error: You have already registered"
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
        elif command[0] == "/join":
            if numwords > 1:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                error_command["message"] = "You have already joined the server"
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
        elif command[0] == "/all":
            if numwords < 2:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                all_message = ''.join(command[1:])
                all_message_command["message"] = all_message
                UDPClientSocket.sendto(bytes(json.dumps(all_message_command), "utf-8"), (ip_adress, host))
            #insert broadcast and pass its params here
            #broadcast()
        elif command[0] == "/msg":
            if numwords < 3:
                error_command["message"] = "Error: Command parameters do not match or is not allowed."
                UDPClientSocket.sendto(bytes(json.dumps(error_command), "utf-8"), (ip_adress, host))
            else:
                direct_message = ''.join(command[2:])
                direct_message_command['handle'] = command[1]
                direct_message_command['message'] = direct_message
                UDPClientSocket.sendto(bytes(json.dumps(direct_message_command), "utf-8"), (ip_adress, host))
            #insert unicast and pass its params here
            #unicast()
        #else assumes hindi nag type si user ng slash / command stuff
        elif command[0] == "/?":
            if numwords > 1: 
                print("Error: Command parameters do not match or is not allowed.")
            else:
                helperCall()
        else:
            print("Error: Please input a proper command or type '/?' to check the list of commands.")
        
        

'''
#pass params to this func
def broadcast():
    #adjust allMessage to the json stuff
    allMessage = "change me".encode()

    for address in allConnectionsList:
        if(address in registered and address != sender):
            #change server socket to whatever the server socket is called because idk if its the udpclientsocket
            serverSocket.sendto(allMessage, address)

    return allMessage

#pass params to this func
def unicast():
    #change receiverhandle and senderAddress
    if (receiverHandle in registered):
        receiver = registered(receiverHandle)
        sender = registered[senderAddress]

        receiverMessage = "(From " + str(sender) + ") " + clientMessage
        senderResponse = "(To " + str(receiver) + ") " + clientMessage

        receiverMessage.encode()
        senderResponse.encode()

        serverSocket.sendto(receiverMessage, receiver)
    else:
        senderResponse = "Error: Handle is not found in the server.".encode()

    return 
'''