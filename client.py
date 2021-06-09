import socket 
import threading
import pickle
import user
#import pyaudio

class Client:
    #connects to the server's socket
    def __init__(self, ip, port, chat_window, username):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.chat_window = chat_window
        self.username = username
        
    def connect(self):
        self.client.connect
        print("Tryna connect to " + self.ip + ":" + str(self.port))
        try:
            self.client.connect((self.ip, self.port))

            #send server your username 
            self.client.send(self.username.encode())

            #server sends the channels and users in the server
            (self.channels, self.users) = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(e)
            self.chat_window.display_message("\nFailed to connect to " + self.ip + ":" + str(self.port))
            return False
        print("connected to server")
        threading.Thread(target=self.listen_thread).start()
        return True
    #listens for a message from the server
    def listen_thread(self):
        while True:
            data = pickle.loads(self.client.recv(4096))
            self.chat_window.display_message(data.content)

    #sends a message to the server to be sent to the rest of the clients
    def send_message(self, message):
        if self.client:
            print("Sending " + message.content)
            self.client.send(pickle.dumps(message))
    
