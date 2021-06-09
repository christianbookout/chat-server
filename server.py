#https://www.geeksforgeeks.org/simple-chat-room-using-python/
#https://realpython.com/python-sockets/
import socket 
import sys 
import json
import threading
import pickle
from user import User
from message import Message
import channel

#TODO 
#ensure data.json is created on first startup
#make ban work
#read banned ips from data.json
#make sure program can be terminated!!!
#make channels appear on the chatwindow
#make users able to start calls in a channel
#make users able to make their own username
#send user a message if the server is full (listen for max_num_users + 1 and then if current number of users == max_num_users say "server is full")
#make the server able to create channels and store the channels in a file along with their message history (maybe)
#run as daemon in the background
#put more try/excepts around so server will never crash

data_file = "data.json"

#host_ip = "127.0.0.1"
#host_port = 9090
#max_num_users = 10

#(users, connection)
connected_users = []
channels = []
banned_users = []

def users():
    return [i[0] for i in connected_users]

def connections():
    return [i[1] for i in connected_users]

def load_server_info():
    #https://www.programiz.com/python-programming/json
    with open(data_file) as file:
        data = json.load(file)


#bans a user's ip from joining the server
def ban(user):
    #print("banning " + connection + " dasdasd")
    #add user to banned list
    banned_users.append(user)
    remove_user(user)

def kick(user):
    #print(f"kicking {connection}")
    remove_user(user)
   
def send_message(message):
    for (u, conn) in connected_users:
        #if u != user:
        try:
            conn.sendall(pickle.dumps(message))
        except:
            print("Error in sending! Removing " + u.username)
            remove_user(u, conn)

"""def broadcast_voice(connection, voice_content):
    for client in voice_clients:
        if client != connection:
            try:
                client.send(voice_content)
            except:
                pass"""
                
def create_channel():
    channels.append(channel.Channel())

def store_data():
    #store everything to data.json
    with open(data_file, "w") as file:
        file.write("")
        #store channels, banned users

def server_input_thread():
    while True:
        try:
            inp = input()
            args = inp.split(" ")
            if len(args) == 0:
                continue
            if args[0].startswith("/"):
                if args[0] == "/exit":
                    print("Tryna close text thread")
                    text_thread.join()
                    print("Closed text thread")
                    exit()
                elif args[0] == "/channel" and len(args) >= 2:
                    print("Creating new channel")

                else:
                    print("Unknown command")
            #else:
                #send_message(None, "<Server>: " + inp)
        except:
            print("Server input thread broke")

#thread that interacts from the server to one client 
def client_connection_thread(user, connection):
    while True:
        try:
            #Server receives message contents from the user containing the user's string message and the channel it was sent in
            message = pickle.loads(connection.recv(4096))
            if not message:
                remove_user(user, connection)
                break
            print(str(message.content))
            send_message(Message("<" + user.username + ">: " + message.content, channel.Channel("general", False)))
        except Exception as e:
            print("here")
            print(repr(user) + " has left the server. Exception: " + str(e))
            remove_user(user, connection)
            sys.exit()

def remove_user(user, connection):
    #print("Removing " + repr(user))
    if ((user, connection) in connected_users):
        connected_users.remove((user, connection))
    connection.close()

#begin listening on your ip and port for users
def listen_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        print("Opening server with address " + host_ip + ":" + str(host_port))

        s.bind((host_ip, host_port))
        s.listen(max_num_users)

        #listen infinitely for new users to join 
        while True: 
            (connection, connection_address) = s.accept() 

            print("Connecting to user!")
            #if the user is banned, don't allow them to join the chatroom
            #if (connection_address[0] in banned_users()):
            #    remove_user(connection)

            #Initial data exchange
            try:
                #Server receives initial packet containing user's username (and maybe other data in the future)
                username = connection.recv(4096).decode()
                #print("username: " + username)
                user = User(username, connection_address)
                connected_users.append((user, connection))
                #Server gives the client a list of available channels and users
                connection.send(pickle.dumps((channels, users())))
            except Exception as e:
                print("Connection failed with " + connection_address[0] + " with error message: " + str(e))
                if user:
                    remove_user(user, connection)
                return

            #TODO send the new user to every client so they can see they are connected (and remove the user when they leave)

            client_thread = threading.Thread(target=client_connection_thread, args=[user, connection])
            client_thread.start()  
            
if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print("Wrong syntax. Use format: server.py {ip address} {port} {max # of users}")
        exit()

    #local is 127.0.0.1 port 9090
    host_ip = sys.argv[1]
    host_port = int(sys.argv[2])
    max_num_users = int(sys.argv[3])

    user_thread = threading.Thread(target=server_input_thread)
    user_thread.start()

    text_thread = threading.Thread(target=listen_thread)
    text_thread.start()


