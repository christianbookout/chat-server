#https://www.geeksforgeeks.org/simple-chat-room-using-python/
#https://realpython.com/python-sockets/
import socket 
import sys 
import json
import threading

#TODO 
#ensure data.json is created on first startup
#make ban work
#read banned ips from data.json
#make sure program can be terminated!!!


if (len(sys.argv) != 4):
    print("Wrong syntax. Use format: server.py {ip address} {port} {max # of users}")
    exit()

#local is 127.0.0.1 port 9090
host_ip = sys.argv[1]
host_port = int(sys.argv[2])
max_num_users = int(sys.argv[3])

#host_ip = "127.0.0.1"
#host_port = 9090
#max_num_users = 10

clients = []
voice_clients = []

class ConnectionType:
    TEXT = 1
    VOICE = 2

def banned_users():
    #https://www.programiz.com/python-programming/json
    with open("data.json") as file:
        data = json.load(file)


#bans a user's ip from joining the server
def ban(connection):
    #print("banning " + connection + " dasdasd")
    #add user to banned list
    remove_user(connection)

def kick(connection):
    #print(f"kicking {connection}")
    remove_user(connection)
   
def send_message(connection, user_title, message):
    for client in clients:
        if connection != client:
            try:
                toSend = "<" + str(user_title) + ">: " + message
                client.sendall(toSend.encode())
            except:
                print("Error in sending! Removing " + client)
                remove_user(client)

def broadcast_voice(connection, voice_content):
    for client in voice_clients:
        if client != connection:
            try:
                client.sendall(voice_content)
            except:
                pass

def server_input_thread():
    while True:
        try:
            inp = input()
            if inp == "/exit":
                print("Tryna close text thread")
                text_thread.join()
                print("Closed text thread")
                exit()
            send_message(None, "Server", inp)
        except:
            print("i hate this")
            exit()

#thread that interacts from the server to one client 
def client_connection_thread(connection, connection_address):
    connection.sendall(str("You've entered the chatroom.").encode())

    while True:
        try:
            message = connection.recv(2048).decode()
            if not message:
                remove_user(connection)
                break
            print("<" + connection_address[0] + ">: " + message)
            send_message(connection, connection_address[0], message)
        except:
            remove_user(clients, connection)

#thread that sends receives voice from a client
def voice_client_connection_thread(connection, connection_address):
       while True:
            try:
                data = connection.recv(2048)
                broadcast_voice(connection, data)
            
            except:
                remove_user(voice_clients, connection)

def remove_user(client_arr, connection):
    if (connection in client_arr):
        client_arr.remove(connection)
    connection.close()

#begin listening on your ip and port for users
def listen_thread(client_arr, thread):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #print(f"Opening server with ip {host_ip} and port {host_port}")
        s.bind((host_ip, host_port))
        s.listen(max_num_users)


        while True: 
            
            (connection, connection_address) = s.accept() 

            #if the user is banned, don't allow them to join the chatroom
            #if (connection_address[0] in banned_users()):
            #    remove_user(connection)

            client_arr.append(connection) 

            client_thread = threading.Thread(target=thread, args=(connection, connection_address))

            client_thread.start()  

user_thread = threading.Thread(target=server_input_thread)
user_thread.start()

text_thread = threading.Thread(target=listen_thread, args=(clients, client_connection_thread))
text_thread.start()

#voice_thread = threading.Thread(target=listen_thread, args=(voice_clients, voice_client_connection_thread))
#voice_thread.start()

