import socket
import sys
import json
import re
from threading import Thread

# ---------- Global Variables ----------

# For storing the handle of
# the client side's current user
curr_server = {
  'server_ip' : None,
  'server_port' : 0
}

helpMSG = """
/join <server_ip_add> <port>\t:\tTo connect to the server application
/leave\t\t\t\t:\tTo disconnect to the server application
/register <handle>\t\t:\tTo register a unique handle or alias
/all <message>\t\t\t:\tTo send message to all
/msg <handle> <message>\t\t:\tTo send direct message to a single handle
"""

errorMSG = {
  "err_joining": "Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.",
  "err_disconnecting": "Error: Disconnection failed. Please connect to the server first.",
  "incomplete_command": "Error: Command parameters do not match or is not allowed.",
  "unknown_command": "Error: Command not found."
}

curr_command = None

buffer_size = 1024

# ---------- Functions ----------

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receiveMsg():
  while True:
      try:
          data,address = udp_socket.recvfrom(buffer_size)
          print(json.loads(data))
      except OSError as error:
          continue

# This function gets the command from client
def get_command():
  global curr_command
  curr_command = input().split(" ") #Enter command

# This functions return True if the IPV4 address is valid, else it is false
def valid_IP(addr):
  try:
    socket.inet_aton(addr)
    return [0<=int(x)<256 for x in re.split('\.',re.match(r'^\d+\.\d+\.\d+\.\d+$',addr).group(0))].count(True) == 4
  except socket.error:
    return False
  except Exception:
    return False

# This functions checks if the port# in 'str' format is valid
def valid_Port(port):
  try:
    conv = int(port)
    if conv >= 0 and conv <= 65536:
      return True
    else:
      return False
  except ValueError:
    return False

def client_res():
  if curr_command[0] == "/register":
    if len(curr_command) == 2:
      return {"command": "register", "handle": curr_command[1]}
    else:
      return errorMSG['incomplete_command']

  elif curr_command[0] == "/all":
    if len(curr_command) == 2:
      return {"command": "all", "message": curr_command[1]}
    else:
      return errorMSG['incomplete_command']

  elif curr_command[0] == "/msg":
    if len(curr_command) == 3:
      return {"command": "msg", "handle": curr_command[1], "message": curr_command[2]}
    else:
      return errorMSG['incomplete_command']

  elif curr_command[0] == "/join":
    if len(curr_command) == 3 and valid_IP(curr_command[1]) is True and valid_Port(curr_command[2]):
      curr_server['server_ip'] = curr_command[1]
      curr_server['server_port'] = int(curr_command[2])
      return {"command": "join"}
    else:
      return errorMSG['incomplete_command']

  elif curr_command[0] == "/leave":
    if len(curr_command) == 1:
      return {"command": "leave"}
    else:
      return errorMSG['incomplete_command']

  elif curr_command[0] == "/?":
    return helpMSG

  else:
    return errorMSG['unknown_command']


# This function is for leaving the server
def leave_server():
  global curr_command, curr_user
  try:
    request = {
      "command": "leave".format(curr_command[0]), # leave
    }
    # Parse join request into JSON string
    request_json = json.dumps(request)
    # Send JSON string as bytes to the server
    sent = udp_socket.sendto(bytes(request_json,"utf-8"), (curr_user["server_ip"],curr_user["dest_port"]))
    data, server = udp_socket.recvfrom(1024)
    print(data)
    if data == "Connection closed. Thank you!":
      udp_socket.close()
      
      curr_server["server_ip"] = None
      curr_server["server_port"] = 0
  except:
    print("Error: Disconnection failed. Please connect to the server first.")

print("Type \"/?\" to request command help to output all Input Syntax commands for references ")

while True:
  get_command()
  command = client_res()
  t = False

  if type(command) is str:  #if command is an error message
    print(command)
  else:
    to_send = bytes(json.dumps(command), "utf-8")
    
    if curr_server["server_ip"] is not None or curr_command[0] == "/join":
      srv_addr = (curr_server['server_ip'], curr_server['server_port'])
      try:
        udp_socket.sendto(to_send, srv_addr)
        if t is False:
          receiveMsgThread = Thread(target=receiveMsg)
          receiveMsgThread.start()
          t = True
      except PermissionError as pe:
        print(pe)
      except OSError as oe:
        print(oe)