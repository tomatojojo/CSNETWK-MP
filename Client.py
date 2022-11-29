import socket
import threading
import random

joined = false;


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





msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 3000)
bufferSize          = 4096


UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)


msg = "Message from Server {}".format(msgFromServer[0])

print(msg)

'''
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
    if message == "!q":
        print("Left the chat...")
        exit()
        
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", 3000))
'''