from tkinter import Tk, scrolledtext, Text, Button
from tkinter.constants import END, INSERT, LEFT, BOTTOM, CENTER
from client import Client
from re import sub

port_field_text = "Enter port"
ip_field_text = "Enter ip"

class ChatWindow:
    def __init__(self, window):
    
        self.message_field = Text(window,height=5,width=100)
        self.message_field.pack(side=BOTTOM)

        self.window = window
        window.title("Chat Server")
        self.textbox = scrolledtext.ScrolledText(window)
        self.textbox.insert(END, "Enter the ip and port of the server you'd like to connect to.")
        self.textbox.pack()

        self.ip_field = Text(window, height=2, width=50)
        self.ip_field.insert(INSERT, ip_field_text)
        self.ip_field.pack(side=LEFT)
        self.ip_field.bind('<Return>', lambda event: self.port_field.focus())
        
        def enter_port(event):
            ip = sub(r"[\n\t\s]*", "", self.ip_field.get("1.0", "end"))
            port = int(self.port_field.get("1.0", "end"))
            self.client = Client(ip, port, self)
            self.textbox.delete("1.0", "end")
            self.port_field.pack_forget()
            self.ip_field.pack_forget()

        self.port_field = Text(window, height=2, width=10)
        self.port_field.insert(INSERT, port_field_text)
        self.port_field.pack(side=LEFT, padx=20)
        self.port_field.bind('<Return>', enter_port)

        def send_message(event):
            message = self.message_field.get("1.0", "end")
            self.client.send_message(message)
            self.display_message("<me>: " + message)
            self.message_field.delete("1.0", "end")

        self.message_field.bind('<Return>', send_message)

        self.button = Button(window)

    def display_message(self, message):
        self.textbox.insert(END, "\n"+ message )

    #this isn't very cool, fix it later
    """def set_focus(self, event):
        if root.focus_displayof() == self.port_field and self.port_field.get("1.0", "end") == port_field_text:
            self.port_field.delete("1.0","end")
        elif not root.focus_displayof() == self.port_field and self.port_field.get("1.0", "end") == "":
            self.port_field.insert(INSERT, port_field_text)
        
        elif root.focus_displayof() == self.ip_field and self.ip_field.get("1.0", "end") == ip_field_text:
            self.ip_field.delete("1.0","end")
        elif not root.focus_displayof() == self.ip_field and self.ip_field.get("1.0", "end") == "":
            self.ip_field.insert(INSERT, ip_field_text)"""


root = Tk()
gui = ChatWindow(root)
#gui.message_field.bind('<Return>', lambda event: print("hi"))
root.mainloop()

