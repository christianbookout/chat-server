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



if (len(sys.argv) != 4):
    print("Wrong syntax. Use format: server.py {ip address} {port} {max # of users}")
    exit()

#local is 127.0.0.1 port 9090
#host_ip = sys.argv[1]
#host_port = int(sys.argv[2])
#max_num_users = int(sys.argv[3])

host_ip = "127.0.0.1"
host_port = 9090
max_num_users = 10

clients = []

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
   
def send_message(connection, connection_address, message):
    for client in clients:
        if connection != client:
            toSend = "<" + connection_address[0] + ">: " + message
            client.sendall(toSend.encode())

def send_server_message(message):
    for client in clients:
        toSend = "<Server>: " + message
        client.sendall(toSend.encode())

def user_input_thread():
    while True:
        inp = input()
        if inp == "/exit":
            exit()
        send_server_message(inp)

#thread that interacts from the server to one client 
def client_connection_thread(connection, connection_address):
    connection.sendall(str("You've entered the chatroom.").encode())

    while True:
        message = connection.recv(2048).decode()
        print(connection_address)
        if not message:
            remove_user(connection)
            break
        print("<" + connection_address[0] + ">: " + message)
        send_message(connection, connection_address, message)
        
     
def remove_user(connection):
    if (connection in clients):
        clients.remove(connection)
    connection.close()

user_thread = threading.Thread(target=user_input_thread)
user_thread.start()

#begin listening on your ip and port for users
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #print(f"Opening server with ip {host_ip} and port {host_port}")
    s.bind((host_ip, host_port))
    s.listen(max_num_users)


    while True: 
  
        (connection, connection_address) = s.accept() 

        #if the user is banned, don't allow them to join the chatroom
        #if (connection_address[0] in banned_users()):
        #    remove_user(connection)

        clients.append(connection) 

        client_thread = threading.Thread(target=client_connection_thread, args=(connection, connection_address))

        client_thread.start()  


