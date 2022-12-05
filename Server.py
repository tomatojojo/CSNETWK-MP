import socket
import json
import queue

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
handles = []
address = []
messages = queue.Queue()
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

while True:
    try:
        data, address = UDPServerSocket.recvfrom(bufferSize)
    except:
        pass
    finally:
        json_data = json.loads(data.decode("utf-8"))
        print("Received message: ", data, "\n from ", address)
        if json_data["command"] == "/join":
            command = bytes(json.dumps({"command": "join"}), "utf-8")
            UDPServerSocket.sendto(command, address)
        if json_data["command"] == "/register":
            if json_data["handle"] in handles:
                command = bytes(json.dumps({"command": "error", "message": "Error: Registration failed. Handle or alias already exists."}), "utf-8")
            else:
                pass #will change

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
