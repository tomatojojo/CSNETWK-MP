
import socket
import sys
import json

connected = True

#JSON Commands
register_cmd = {"command":"register", "username":"username"}
deregister_cmd = {"command":"deregister", "username":"username"}
message_cmd = {"command":"msg", "username":"username", "message":"this is my message"}

#Set variables for server address and destination port
server_host = input("\nEnter Server Host: ")
dest_port = int(input("\nEnter Destination Port: "))

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while connected:
    username = input("\nEnter Preferred Username: ")
    register_cmd['username'] = username
    register = json.dumps(register_cmd)
    sock.sendto(bytes(register, "utf-8"), (server_host, dest_port))
    print("Registered Successfully!\n")

    
    data, server = sock.recvfrom(1024)
    data = data.decode("utf-8")  
    command = json.loads(data)

    if command['command'] == "ret_code":
       if command['code_no'] == 401:
          messaging = True
          while messaging:
              message = input("Enter Message[bye = Disconnect]: ")
        
              if message != "bye":
                 message_cmd['message'] = message
                 message_cmd['username'] = username
                 msg = json.dumps(message_cmd)
                 sock.sendto(bytes(msg,"utf-8"), (server_host, dest_port))

                 data, server = sock.recvfrom(1024)
                 data = data.decode("utf-8")
                 command = json.loads(data)
                 if command['code_no'] == 501:
                    print("Server Timeout!")
                    messaging = False
                    connected = False

                 elif command['code_no'] == 401:
                    messaging = True

              else:
                 deregister_cmd['username'] = username
                 deregister = json.dumps(deregister_cmd)
                 sock.sendto(bytes(deregister, "utf-8"), (server_host, dest_port))
                 messaging = False
                 connected = False
       
       elif command['code_no'] == 502:
          print("Username Already Exists!")
          print("Please Enter New Username!")
          connected = True        

       elif command['code_no'] == 301:
          print("Command Unknown!")
          connected = False

#close socket
print ('Disconnected')
sock.close()
