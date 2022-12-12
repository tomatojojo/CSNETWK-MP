import socket
import json
import queue


bufferSize  = 1024
handles = []
port_address = []
if_registered = []
serverIPAdd = "127.0.0.1"
serverPortNum = 12345

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("UDP server up and listening")
# Bind to address and ip
UDPServerSocket.bind((serverIPAdd, serverPortNum))

def convertEmoji(check_message):
    emoji_message = str(check_message).split()
    emojiList = {
        ":heart" : "💚",
        ":laugh" : "😂",
        ":surprised" : "😮",
        ":sad" : "😢",
        ":angry" : "😠",
        ":thumbsup": "👍"
    }
    # test = ' '.join(str(emojiList.get(word, word)) for word in emoji_message)
    # print(test)
    return ' '.join(str(emojiList.get(word, word)) for word in emoji_message)


while True:
    try:
        data, address = UDPServerSocket.recvfrom(bufferSize)
    except:
        pass
    finally:
        encoded_data = data.decode("utf-8")
        json_data = json.loads(encoded_data)
        print("Received message: ", data, "\n from ", address)
        print(json_data)
        print(encoded_data)
        if json_data["command"] == "join":
            handles.append("")
            port_address.append(address)
            if_registered.append(False)
            bytesToSend = str.encode("Connection to the Message Board Server is successful!")
            UDPServerSocket.sendto(bytesToSend, address)
            '''
            command = bytes(json.dumps({"command": "join"}), "utf-8")
            '''
        elif json_data["command"] == "register":
            index = port_address.index(address)
            if if_registered[index] == False:
                if json_data["handle"] in handles:
                    bytesToSend = str.encode("Error: Registration failed. Handle or alias already exists.")
                    UDPServerSocket.sendto(bytesToSend, address)
                else:
                    name = json_data["handle"]
                    handles[index] = name
                    if_registered[index] = True
                    print(handles)
                    print(port_address)
                    for pa in port_address:
                        print(pa)
                        index_receiver = port_address.index(pa)
                        if if_registered[index_receiver] == True:
                            welcome = "Welcome " + name +"!"
                            welcome_bytes = str.encode(welcome)
                            UDPServerSocket.sendto(welcome_bytes, pa)
            else:
                bytesToSend = str.encode("You have already registered")
                UDPServerSocket.sendto(bytesToSend, address)          
        elif json_data["command"] == "leave":
            try:
                index = port_address.index(address)
                if_registered.pop(index)
                handles.pop(index)
                port_address.pop(index)
                print(handles)
                print(port_address)
                print(if_registered)
                leave_message = "Connection closed. Thank you!"
                leave_message_bytes = str.encode(leave_message)
                UDPServerSocket.sendto(leave_message, address)
            except:
                leave_message = "Connection closed. Thank you!"
                leave_message_bytes = str.encode(leave_message)
                UDPServerSocket.sendto(leave_message_bytes, address)     
        elif json_data["command"] == "error":
            error_message = json_data["message"]
            error_message_bytes = str.encode(error_message)
            UDPServerSocket.sendto(error_message_bytes, address)

        elif json_data["command"] == "msg":
            index_registered = port_address.index(address)
            if if_registered[index_registered] == True:
                if json_data['handle'] in handles:
                    receiver = json_data['handle']
                    index = handles.index(receiver)
                    destination_address = port_address[index]

                    index2 = port_address.index(address)
                    sender = handles[index2]
                    sender_message = ("[From " + sender + "]: " + convertEmoji(json_data["message"]))
                    receiver_message = ("[To " + receiver + "]: " + convertEmoji(json_data["message"]))
                    sender_message_bytes = str.encode(sender_message)
                    receiver_message_bytes = str.encode(receiver_message)
                    #sender
                    UDPServerSocket.sendto(sender_message_bytes, destination_address)
                    #receiver 
                    UDPServerSocket.sendto(receiver_message_bytes, address)
                else:
                    error_message = "Error: Handle or alias not found."
                    error_message_bytes = str.encode(error_message)
                    UDPServerSocket.sendto(error_message_bytes, address)
            else:
                error_message = "Please register to the server first before sending a message to another client"
                error_message_bytes = str.encode(error_message)
                UDPServerSocket.sendto(error_message_bytes, address)
        elif json_data["command"] == "all":
            index_registered = port_address.index(address)
            if if_registered[index_registered] == True:
                index2 = port_address.index(address)
                sender = handles[index2]
                for pa in port_address:
                    index_receiver = port_address.index(pa)
                    if if_registered[index_receiver] == True:
                        all_msg = sender + ": " + convertEmoji(json_data["message"])
                        all_msg_bytes = str.encode(all_msg)
                        UDPServerSocket.sendto(all_msg_bytes, pa)
            else:
                error_message = "Please register to the server first before sending a message to another client"
                error_message_bytes = str.encode(error_message)
                UDPServerSocket.sendto(error_message_bytes, address)
        elif json_data["command"] == "multicast":
            index_registered = port_address.index(address)
            if  if_registered[index_registered] == True:
                handdles_list = json_data["handle"]
                x = 0
                highest = json_data["numhandles"]
                for x in range(highest):
                    if handdles_list[x] in handles:
                        receiver = handdles_list[x]
                        index = handles.index(receiver)
                        destination_address = port_address[index]

                        index2 = port_address.index(address)
                        sender = handles[index2]
                        sender_message = ("[From " + sender + "]: " + convertEmoji(json_data["message"]))
                        receiver_message = ("[To " + receiver + "]: " + convertEmoji(json_data["message"]))
                        sender_message_bytes = str.encode(sender_message)
                        receiver_message_bytes = str.encode(receiver_message)
                        #sender
                        UDPServerSocket.sendto(sender_message_bytes, destination_address)
                        #receiver 
                        UDPServerSocket.sendto(receiver_message_bytes, address)
                    else:
                        error_message = handdles_list[x] + " is not found"
                        error_message_bytes = str.encode(error_message)
                        UDPServerSocket.sendto(error_message_bytes, address)
            else:
                error_message = "Please register to the server first before sending a message to another client"
                error_message_bytes = str.encode(error_message)
                UDPServerSocket.sendto(error_message_bytes, address)
            


                
                    
                    
                



