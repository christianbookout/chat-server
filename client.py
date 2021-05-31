import socket 
import sys 
import threading


if (len(sys.argv) != 3):
    print("Enter server.py {ip address} {port}")
    exit()

host_ip = sys.argv[1]
host_port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host_ip, host_port))

    
    def user_input_thread():
        while True:
            inp = input()
            s.sendall(inp.encode())

    user_thread = threading.Thread(target=user_input_thread)
    user_thread.start()

    while True:
        data = s.recv(2048).decode()
        print(data)