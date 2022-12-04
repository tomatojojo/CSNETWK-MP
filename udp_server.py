
import socket
import sys
import json

connected = True

param_incom_cmd = {"command":"ret_code", "code_no": 201}
unknown_cmd = {"command":"ret_code", "code_no": 301}
accepted_cmd = {"command":"ret_code", "code_no": 401}
user_unreg_cmd = {"command":"ret_code", "code_no": 501}
user_exists_cmd = {"command":"ret_code", "code_no": 502}

users = []

#Set variables for listening address and listening port
listening_address='127.0.0.1'
listening_port=7190

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
print ("\nStarting up on %s port %d" %(listening_address, listening_port))
sock.bind((listening_address, listening_port)) 

print ('\nWaiting Connection')

while connected:
    #waiting for data to arrive
    data, address = sock.recvfrom(1024)
    data = data.decode("utf-8")
    command = json.loads(data)
  
    if command['command'] == "register":
       #it returns code_no:401 
       if command['username'] not in users:
          print(f"{command['username']} joined the message board!")
          users.append(command['username'])
          print(f"Users in Message Board: {users}")
          accepted_command = json.dumps(accepted_cmd)
          sock.sendto(bytes(accepted_command, "utf-8"), address)
          connected = True
       
       #it returns code_no:502
       else:
          user_exists = json.dumps(user_exists_cmd)
          sock.sendto(bytes(user_exists, "utf-8"), address)
          connected = True

    elif command['command'] == "deregister":
      
       #it returns code_no:501
       if command['username'] not in users:
          user_unreg = json.dumps(user_unreg_cmd)
          sock.sendto(bytes(user_unreg, "utf-8"), address)
          connected = True
      
       #it returns code_no:401
       else:
          print(f"{command['username']} left the message board!")
          users.remove(command['username'])
          print(f"Users in Message Board: {users}")
          accepted_command = json.dumps(accepted_cmd)
          sock.sendto(bytes(accepted_command, "utf-8"), address)
          connected = True

       #server will disconnect if users are empty
       if users == []:
          print("Disconnecting Server")
          connected = False

    elif command['command'] == "msg":
       #it returns code_no:501
       if command['username'] not in users:
          user_unreg = json.dumps(user_unreg_cmd)
          sock.sendto(bytes(user_unreg, "utf-8"), address)
          connected = True
        
       #it returns code_no:401
       else:
          accepted_command = json.dumps(accepted_cmd)
          sock.sendto(bytes(accepted_command, "utf-8"), address)
          print(f"From {command['username']}: {command['message']}")
          connected = True

    #it returns code_no:301
    else:
       unknown_command = json.dumps(unknown_cmd)
       sock.sendto(bytes(unknown_command, "UTF-8"), address)
       connected = True
   
print('Server Disconnected')
sock.close()

