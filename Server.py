import socket
import json
import queue

#Json Commands
join_command = {"command": "join"}
leave_command = {"command": "leave"}
register_command = {"command": "register", "handle": "handle"}
all_message_command = {"command": "all", "message": "message"}
direct_message_command = {"command": "msg", "handle": "handle", "message": "message"}
error_command = {"command": "error", "message": "message"}

bufferSize  = 1024
handles = []
port_address = []
messages = queue.Queue()
serverIPAdd = "127.0.0.1"
serverPortNum = 12345

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("UDP server up and listening")
# Bind to address and ip
UDPServerSocket.bind((serverIPAdd, serverPortNum))
#pass client message as param for this func (change word and clientMessage since they are just placeholders)
def emotes(clientMessage):
    emote = {
        ":heart" : "❤️",
        ":laugh" : "😂",
        ":surprised" : "😮",
        ":sad" : "😔",
        ":angry" : "😠"
    }

    return ' '.join(str(emote.get(word, word)) for word in clientMessage)


while True:
    try:
        data, address = UDPServerSocket.recvfrom(bufferSize)
    except:
        pass
    finally:
        json_data = json.loads(data.decode("utf-8"))
        print("Received message: ", data, "\n from ", address)
        if json_data["command"] == "join":
            bytesToSend = str.encode("Connection to the Message Board Server is successful!")
            UDPServerSocket.sendto(bytesToSend, address)
            '''
            command = bytes(json.dumps({"command": "join"}), "utf-8")
            '''
        elif json_data["command"] == "register":
            if json_data["handle"] in handles:
                bytesToSend = str.encode("Error: Registration failed. Handle or alias already exists.")
                UDPServerSocket.sendto(bytesToSend, address)
            else:
                handles.append(json_data["handle"])
                port_address.append(address)
                name = json_data["handle"]
                print(handles)
                print(port_address)
                for pa in port_address:
                    welcome = "Welcome " + name +"!"
                    welcome_bytes = str.encode(welcome)
                    UDPServerSocket.sendto(welcome_bytes, pa)
        elif json_data["command"] == "leave":
            try:
                index = port_address.index(address)
                handles.pop(index)
                port_address.pop(index)
                print(handles)
                print(port_address)
            except:
                pass
                
                    
                    
                


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
