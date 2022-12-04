import socket
import threading
import queue
import json


localIP = "127.0.0.1"
localPort = 3000
bufferSize = 1024
serverMessage = "Hello World"
bytesCount = str.encode(serverMessage)

socketUDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socketUDP.bind((localIP, localPort))
threading.Thread(target=receive)

print("UDP Server is online")
print("Waiting for client...")

def serverUnicast():
    serverSocket.sendto(receiveMessage, address)

while(True):
    bytesAddress, clientSend = socketUDP.recvfrom(bufferSize)
    messageDecode = bytesAddress.decode()
    message = bytesAddress[0]
    address = bytesAddress[1]

    clientMsg = "Message from Client: {}".format(message)
    clientIP ="Client IP Address: {}".format(address)

    print(clientMsg)
    print(clientIP)

    messageJson = json.loads(messageDecode)

    
    # if(messageJson["command"] == "/join"):
    #     if(inputs[0] == "/join"):
    #         messageInputs = {
    #             "command": inputs[0],
    #         }


    socketUDP.sendto(bytesCount, address)


'''
messages = queue.Queue()
clients = []

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server.bind(("localhost", 3000))

def receive():
    while True:
        try:
            message, address= server.recvfrom(2048)
            messages.put((message, address))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, address = messages.get()
            print(message.decode())
            if address not in clients:
                clients.append(address)
            for client in clients:
                try:
                    if message.decode().startswith("Online Tag:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
'''
