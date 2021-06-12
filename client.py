from types import SimpleNamespace as Namespace
from message import Message
import socket 
import threading
import channel
import user
import json
import pyaudio

class Client:
    #connects to the server's socket
    def __init__(self, ip, port, chat_window, username):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.chat_window = chat_window
        self.username = username
        self.channels = []
        
    def connect(self):
        self.client.connect
        print("Tryna connect to " + self.ip + ":" + str(self.port))
        try:
            self.client.connect((self.ip, self.port))

            #send server your username 
            self.client.send(self.username.encode())

            #server sends the channels and users in the server
            channels_str = self.client.recv(1024).decode()
            users_str = self.client.recv(1024).decode()
            user_str = self.client.recv(1024).decode()

            self.channels = Client.str_to_object(channels_str)
            self.users = Client.str_to_object(users_str)
            self.user = Client.str_to_object(user_str)

        except Exception as e:
            print(e)
            return False
        print("connected to server")
        threading.Thread(target=self.listen_thread).start()
        return True

    @staticmethod
    def str_to_object(str):
        #https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
        return json.loads(str, object_hook=lambda d: Namespace(**d))

    #listens for a message from the server
    def listen_thread(self):
        while True:
            pass
            #data = pickle.loads(self.client.recv(1024))
            #data.channel = channel.Channel.get_channel(self.channels, data.channel)
            #data.channel.append_message(data)
            #self.chat_window.display_message(data.content)

    #sends a message to the server to be sent to the rest of the clients
    def send_message(self, message):
        if self.client:
            pass
            #self.client.send(pickle.dumps(message))
