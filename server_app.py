import socket
import json

# Create an empty list to store current logged in users (object)
curr_users = [] 

# Set variables for listening address, listening port, buffer size, 
# template for user object, and if the message is for everyone

# 192.168.X.X is risky
listening_addr = "127.128.0.1"
listening_port = 12345
bffr_size  = 1024
def_tmp = {
  "handle": None,
  "ip_addr": None,
  "port": 0
}
msg_all = False
# is_server_running = True

# Create a UDP socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to address and port
UDPServerSocket.bind((listening_addr,listening_port))

# Resets the default template for the client address info
def reset_def_tmp():
  global def_tmp
  def_tmp = {
  "handle": None,
  "ip_addr": None,
  "port": 0
  }

# Start listening for incoming datagrams
# This function is responsible for joining the server
def join_server(req) :
  global curr_users
  # TO-DO: Can't join once currently joined
  if is_joined_server() == False:
    curr_users.append(def_tmp)
    print("all users:",curr_users)
  return server_res("joined"), None

# This function is responsible for knowing whether a user has already joined the server
def is_joined_server(): 
  global curr_users
  for user in curr_users:
    if user["ip_addr"] == def_tmp["ip_addr"] and user["port"] == def_tmp["port"]: return True
  return False

# This function is responsible for knowing whether a user is already registered, or if a user already have an alias
def is_registered(handle):
  global curr_users
  for user in curr_users:
    if user["handle"] == handle:
      return True

    if user["ip_addr"] == def_tmp["ip_addr"] and user["port"] == def_tmp["port"]: # For checking if current user from packet had already joined
      if user["handle"] is not None: # Checking if user already have a handle (Cannot change handle once already registered)
        return True
      else:
        return False
  return False

# This function is responsible for registering a handle
def reg_user(req):
  global curr_users
  if is_joined_server():
    # Checks if handle already exists
    if is_registered(req["handle"]): 
      return server_res("handle_exists"), None

    # Registers the handle if it doesn't exist
    for user in curr_users:
      if user["ip_addr"] == def_tmp["ip_addr"]:
        user["handle"] = req["handle"]
        print("registered handle:", user)
        tmp = server_res("registered", req=req), None
        # Message upon successful registration of a handle
        return tmp
  return server_res("err_joining"), None

# This function is responsible for sending the message to all registered handles
def send_msg_all(req):
  global msg_all
  if is_joined_server():
    try:
      # Check if requesting handle is registered
      if is_registered(req["handle"]): 
        msg_all = True
        return server_res("msg_sent_all", req=req), server_res("msg_rcvd", req=req)
      return server_res("not_registered"), None      
    except KeyError:
      return server_res("incomplete_command"), None
  return server_res("err_joining"), None

# This function is responsible for sending the message to a specific handle
def send_msg_direct(req):
  global curr_users, msg_all
  if is_joined_server():
    try:
      # Check if requesting handle and receipient handle are both registered
      if is_registered(req["handle"]) and is_registered(req["handle_receipient"]): 
        msg_all = False
        return server_res("msg_sent_direct", req=req), server_res("msg_rcvd", req=req)
      return server_res("not_registered"), None
    except KeyError:
        return server_res("incomplete_command"), None
  return server_res("err_joining"), None

# This function is responsible for leaving the server
def leave_server(req) :
  global curr_users
  if is_joined_server():
    for user in curr_users:
      if user["ip_addr"] == req["ip_addr"]:
        curr_users.remove(user["ip_addr"])
    return server_res("disconnect"), None
  return server_res("err_disconnecting"), None

# This function is responsible for returning the message responses given an event
def server_res(key, req=None):
    # Return codes Dictionary
    #print("KEYS_REQ", key, req)
    # if req has dict value
    if req is not None:
      if key == "registered": # Successfully registered handle
        return "Welcome, {0}!".format(req["handle"])
      elif key == "msg_sent_direct": # Message upon successful sending of a direct message
        return "[To {0}]: {1}".format(req["handle_recipient"], req["message"])
      elif key == "msg_sent_all": # Message upon successful sending of a message to all
        return "{0}: {1}".format(req["handle"], req["message"])
      elif key == "msg_rcvd": # Message upon successful receipt of a direct message
        return "[From {0}:] {1}".format(req["handle"], req["message"])

    # if req is default value (None)
    else:
      responses = {
          "joined": "Connection to the Message Board Server is successful!", # Message upon successful connection to the server
          #NOTE: "err_joining" CHECK SHOULD BE DONE AT CLIENT SIDE
          "err_joining": "Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", # Message upon unsuccessful connection to the server due to the server not running or incorrect IP and Port combination
          "not_registered": "Error: Handle or alias not found.", # Message upon unsuccessful sending of a direct message
          "handle_exists": "Error: Registration failed. Handle or alias already exists.", # Handle already exists
          "disconnect": "Connection closed. Thank you!", # Message upon successful disconnection to the server
          #NOTE: "err_disconnecting" CHECK SHOULD BE DONE AT CLIENT SIDE
          "err_disconnecting": "Error: Disconnection failed. Please connect to the server first.", # Message upon unsuccessful disconnection to the server due to not currently being connected
          #NOTE: "incomplete_command" and "unknown_command" probably done at client side
          "incomplete_command": "Error: Command parameters do not match or is not allowed.", # Incorrect or invalid command parameters
          "unknown_command": "Error: Command not found." # Invalid command syntax
      }
      return responses[key]

# Function for processing request commands
def process_req(req):
  # Available commands
  commands = {
    "join": join_server,
    "register": reg_user,
    "all": send_msg_all,
    "msg": send_msg_direct,
    "leave": leave_server
  }
  try:
    # Get the command that needs to be executed
    res = commands.get(req["command"])
    
    # Execute command and return the response
    return res(req)

  except KeyError:
    #print("incomplete_command")
    return server_res("incomplete_command")
  except TypeError:
    #print("unknown_command")
    return server_res("unknown_command")




# START LISTENING FOR REQUESTS
while True:
  reset_def_tmp()

  # Waiting for data to arrive, this is a blocking function
  data,address = UDPServerSocket.recvfrom(bffr_size)

  # Checks if received data contains something
  if data:
    try:
      print("received:", data, ",", address)
      # Load the JSON string request from
      # connecting client to a Dictionary object
      request = json.loads(data.decode("utf-8"))

      # Load current IP address and Port of client to dict
      def_tmp["ip_addr"] = address[0]
      def_tmp["port"] = address[1]

      # Process the request from connecting client
      response_sent, response_rcvd = process_req(request)

      # Convert response to JSON string
      res_json_sent = json.dumps(response_sent)
      res_json_rcvd = json.dumps(response_rcvd)

      # Send return message to connecting client
      sent = UDPServerSocket.sendto(bytes(res_json_sent,"utf-8"), address)
      # Send message to recipient client
      if res_json_rcvd is not None and msg_all:
        for user in curr_users:
          if(user["handle"] != request["handle"]):
            UDPServerSocket.sendto(bytes(res_json_rcvd,"utf-8"), (user["ip_addr"], user["port"]))
      else:
        for user in curr_users:
          if(user["handle"] == request["handle"]): 
            address_recipient = (user["ip_addr"], user["port"])
        UDPServerSocket.sendto(bytes(res_json_rcvd,"utf-8"), address_recipient)
    except:
      continue

# TO-DO: Clarify no need for backslash right