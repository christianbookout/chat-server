#https://www.geeksforgeeks.org/simple-chat-room-using-python/
#https://realpython.com/python-sockets/
from datetime import datetime
import socket 
import sys 
import json
import threading
import pickle
from user import User
from message import Message
import channel
from os import path
#TODO 
#make ban work
#read banned ips from data.json
#make sure server can be terminated!!!
#make users able to start calls in a channel
#make users able to make their own username
#send user a message if the server is full
#run as daemon in the background
#put more try/excepts around so server will never crash
#finish the /help command
#implement a password system
#figure out whether or not i need to store peoples ip for banning
#add a reason to kicking/banning users
#add a mute feature
#switch from using pickle to just sending bytes
#change in channel.py from server.channels to passing in a variable 


file_extension = ".server"

user_data_file = "user_data" + file_extension
channels_file = "channels" + file_extension
banned_user_file = "bans" + file_extension

stayalive = True
listen_socket = None

#(users, connection)
connected_users = []
known_users = []
channels = []
banned_users = []

def users():
    return [i[0] for i in connected_users]

def connections():
    return [i[1] for i in connected_users]

# close all open sockets by using a classic strategy employed by governments worldwide!
def close_all_sockets():
    if listen_socket != None:
        listen_socket.close()
    for user in connected_users:
        user[1].shutdown(socket.SHUT_RDWR)
        user[1].close()

#bans a user's ip from joining the server
def ban(user):
    #print("banning " + connection + " dasdasd")
    #add user to banned list
    banned_users.append(user)
    remove_user(user)

#Disconnects user from the server
def kick(id):
    connected_user = [i for i in connected_users if str(i[0].id) == id]

    if len(connected_user) == 0:
        print("User with id " + id + " does not exist")
    
    connected_user = connected_user[0]

    remove_user(connected_user[0], connected_user[1])

#removes the connection between the server and the user
def remove_user(user, connection):
    print("Removing " + repr(user))
    if ((user, connection) in connected_users):
        connected_users.remove((user, connection))
    connection.close()

#stores messages into their respective channel and writes them to the channels file 
def store_message(message):
    message.channel.message_history.append(message)
    with open(channels_file, "wb") as file:
        pickle.dump(channels, file)

#broadcasts a message to all users connected to the server
def send_message(message):
    store_message(message)
    for (u, conn) in connected_users:
        try:
            conn.sendall(pickle.dumps(message))
        except:
            print("Error in broadcasting message! Removing " + u.username)
            remove_user(u, conn)

#creates a channel named title
def create_channel(title, is_public):
    channels.append(channel.Channel(title, is_public))
    with open(channels_file, "wb") as file:
        pickle.dump(channels, file)

#turns a string "true" or "false" into its respective bool
def bool(str):
    return str.lower() == "true"

#Receives input from the console, all actions that the server host can perform 
def server_input_thread():
    global stayalive
    while True:
        #try:
        inp = input()
        args = inp.split(" ")
        if len(args) == 0:
            continue
        if args[0].startswith("/"):
            if args[0] == "/exit":
            #    for connected_user in connected_users:
            #        remove_user(connected_user[0], connected_user[1])
                close_all_sockets()
                stayalive = False
                break
            elif args[0] == "/channel" and len(args) >= 3:
                print("Creating new channel")
                create_channel(args[1], bool(args[2]))
            elif args[0] == "/kick" and len(args) >= 2:
                kick(args[1]) 
            elif args[0] == "/say" and len(args) >= 3:
                pass #format /say (channel_name) (message)
            elif args[0] == "/help":
                print("/say (channel_name) (message): Sends message in channel_name\n/kick (username): Disconnects the user named username from the server\n/channel (name) (is_public)")
            else:
                print("Unknown command. Type /help for a list of commands.")
    print('user input thread exited')

#thread that interacts from the server to one client 
def client_connection_thread(user, connection):
    global stayalive
    while stayalive:
        try:
            #Server receives message contents from the user containing the user's string message and the channel it was sent in
            messsage = connection.recv(1024)
            data = None
            #if isinstance(data, Message):
            #    message = data
            #elif isinstance(data, ):
            #    pass
            if not message:
                print("data cannot be received from " + user.username)
                remove_user(user, connection)
                break
            send_message(Message(user, "<" + user.username + ">: " + message.content, channel.Channel.get_channel(channels, message.channel), datetime.now))
            message.channel.message_history.append(message)
        except Exception as e:
            print(repr(user) + "'s message has resulted in an error. Exception: " + str(e))
            remove_user(user, connection)
            break


#begin listening on your ip and port for users
def listen_thread():
    global stayalive
    global listen_socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        listen_socket = s
        print("Opening server with address " + host_ip + ":" + str(host_port))

        s.bind((host_ip, host_port))
        s.listen(max_num_users)

        #listen infinitely for new users to join 
        while True:
            try:
                (connection, connection_address) = s.accept() 
                print("Connecting to user!")
                #if the user is banned, don't allow them to join the chatroom
                #if (connection_address[0] in banned_users):
                #    remove_user(connection)
                #Initial data exchange

                #Server receives initial packet containing user's username (and maybe other data in the future)
                username = connection.recv(1024).decode()
                known_user = [i for i in known_users if i.username == username]
                if len(known_user) == 1:
                    username = [0]
                elif len(known_user) > 1:
                    print("There are multiple users with the username " + username + ". How!?")
                user = User(username, datetime.now())

                connected_users.append((user, connection))
                #Server gives the client a list of available channels and online users
                channels_json = [i.__dict__ for i in channels]
                users_json = [i.__dict__ for i in users()]

                connection.send(json.dumps(channels_json).encode())
                connection.send(json.dumps(users_json).encode())
                connection.send(json.dumps(user.__dict__).encode())
            except OSError:
                print('listen thread exited')
                return
            except Exception as e:
                print("Connection failed with " + connection_address[0] + " with error message: " + str(e))
                if user:
                    remove_user(user, connection)
                return

            #TODO send the new user to every client so they can see they are connected (and remove the user when they leave)
            print("User with id " + str(user.id) + " joined")
            client_thread = threading.Thread(target=client_connection_thread, args=[user, connection])
            client_thread.start()
    
def load_server_info():
    global banned_users
    global channels
    global known_users
    def load_file(file_path):
        if not path.exists(file_path):
            try:
                open(file_path, "w").close()
            except:
                print("Couldn't create file with path: " + file_path)
            return []
        elif path.getsize(file_path) == 0:
            return []
        with open(file_path, "rb") as file:
            return pickle.load(file)

    banned_users = load_file(banned_user_file)
    channels = load_file(channels_file)
    known_users = load_file(user_data_file)
        
if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print("Wrong syntax. Use format: server.py {ip address} {port} {max # of users}")
        exit()

    #local is 127.0.0.1 port 9090
    host_ip = sys.argv[1]
    host_port = int(sys.argv[2])
    max_num_users = int(sys.argv[3])

    load_server_info()

    
    #print(channels[0].message_history[0])
    user_thread = threading.Thread(target=server_input_thread)
    user_thread.start()

    text_thread = threading.Thread(target=listen_thread)
    text_thread.start()


