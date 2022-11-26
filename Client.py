import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000,9000)))

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

client.sendto(f"Online Tag: {name}".encode(), ("localhost", 3000))

while True:
    message = input("")
    if message == "!leave":
        print("Left the chat...")
        exit()
        
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", 3000))

# msgFromClient       = "Hello UDP Server"
# bytesToSend         = str.encode(msgFromClient)
# serverAddressPort   = ("127.0.0.1", 3000)
# bufferSize          = 4096


# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)


# msg = "Message from Server {}".format(msgFromServer[0])

# print(msg)