import socket 
import threading
#import pyaudio


class Client:
    def __init__(self, ip, port, chat_window):
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.chat_window = chat_window
        threading.Thread(target=self.listen_thread).start()
    """def start(self):
        self.s = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect((host_ip, host_port))
            
            #def send_message(message):
            #    if s:
            #        s.sendall(message.encode())
            print("Connected!")
            self.send_message("hi")
            self.message_sendy.bind('<Return>', lambda event: self.send_message("yo"))
            #user_thread = threading.Thread(target=user_input_thread)
            #user_thread.start()

            #while True:
            #    data = s.recv(2048).decode()
            #    print(data)"""
    def listen_thread(self):
        while True:
            data = self.client.recv(2048).decode()
            print("Getting " + data)
            self.chat_window.display_message(data)

    def send_message(self, message):
        if self.client:
            print("Sending " + message)
            self.client.sendall(message.encode())
    
