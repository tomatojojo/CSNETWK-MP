import socket

localIP = "127.0.0.1"
localPort = 3000
bufferSize = 4096
serverMessage = "Hello World"
bytesCount = str.encode(serverMessage)

socketUDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socketUDP.bind((localIP, localPort))

print("UDP Server is online")

while(True):
    bytesAddress = socketUDP.recvfrom(bufferSize)
    message = bytesAddress[0]
    address = bytesAddress[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP ="Client IP Address;{}".format(address)

    print(clientMsg)
    print(clientIP)

    socketUDP.sendto(bytesCount, address)