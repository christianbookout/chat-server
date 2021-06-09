import os
import random
from tkinter import Tk, scrolledtext, Text, Button, OptionMenu, StringVar
from tkinter.constants import END, INSERT, LEFT, BOTTOM, CENTER, TOP
from client import Client
from message import Message
from channel import Channel
from re import sub
import pathlib
#from ttkthemes import ThemedStyle

port_field_text = "Enter port"
ip_field_text = "Enter ip"
message_field_text = "Send a message in "

class ChatWindow:
    #initialize a chat window w/ a message display field, chat box, ip field, and port field 
    def __init__(self, window):
    
        self.channels = []
        self.selected_channel = "General"

        self.window = window
        window.title("Chat Server")
        self.textbox = scrolledtext.ScrolledText(window)
        self.textbox.insert(END, "Enter the ip and port of the server you'd like to connect to.")
        self.textbox.pack()

        self.ip_field = Text(window, height=2, width=50)
        self.ip_field.insert(INSERT, ip_field_text)
        self.ip_field.pack(side=LEFT)
        self.ip_field['foreground'] = 'gray'

        def on_focus(event, placeholder_text):
            #print("Focussed")
            if sub(r"[\n]*", "",event.widget.get("1.0", "end")) == placeholder_text:
                event.widget.delete("1.0", "end")
            event.widget['foreground'] = 'black'
        
        def on_unfocus(event, placeholder_text):
            #print("unfocussed " + sub(r"[\n\t\s]*", "",event.widget.get("1.0", "end")))
            if sub(r"[\n\t\s]*", "",event.widget.get("1.0", "end")) == "":
                event.widget.insert(INSERT, placeholder_text)
                event.widget['foreground'] = 'gray'
            return 'break'
            
        self.ip_field.bind('<FocusIn>', on_focus)
        #Tells the client to send a message of the message_field's contents
        def send_message(event):
            message = self.message_field.get("1.0", "end")
            self.client.send_message(Message(message, self.get_selected_channel()))
            self.message_field.delete("1.0", "end")
            return 'break'

        def select_channel(channel):
            self.selected_channel = channel

        #connects to the server when the user presses enter on the port textfield
        def enter_port(event):
            ip = sub(r"[\n\t\s]*", "", self.ip_field.get("1.0", "end"))
            port = int(self.port_field.get("1.0", "end"))

            with open(os.path.join(str(pathlib.Path().absolute()) + '\\resources\\names.txt')) as f:
                self.username = random.choice(f.read().split('\n'))

            self.client = Client(ip, port, self, self.username)
            if not self.client.connect():
                return
            self.textbox.delete("1.0", "end")
            self.port_field.pack_forget()
            self.ip_field.pack_forget()

            general_placeholder = StringVar(window)
            general_placeholder.set("general")
            self.channel_dropdown = OptionMenu(window, general_placeholder, self.channels, command=select_channel)
            self.channel_dropdown.pack(side=TOP)

            self.message_field = Text(window,height=5,width=100)
            self.message_field.pack(side=BOTTOM)
            self.message_field['foreground'] = 'gray'
            self.message_field.insert(INSERT, message_field_text + "" + self.selected_channel)
            self.message_field.bind('<Return>', send_message)
            self.message_field.bind('<FocusIn>', lambda event: on_focus(event, message_field_text + "" + self.selected_channel))
            self.message_field.bind('<FocusOut>', lambda event: on_unfocus(event, message_field_text + "" + self.selected_channel))
            return 'break'
        
        self.port_field = Text(window, height=2, width=10)
        self.port_field.insert(INSERT, port_field_text)
        self.port_field.pack(side=LEFT, padx=20)
        self.port_field['foreground'] = 'gray'

        self.port_field.bind('<Return>', enter_port)
        self.port_field.bind('<FocusIn>', lambda event:on_focus(event, port_field_text))
        self.port_field.bind('<FocusOut>', lambda event: on_unfocus(event, port_field_text))

        self.ip_field.bind('<Return>', lambda event: self.port_field.focus())
        self.ip_field.bind('<FocusIn>', lambda event:on_focus(event, ip_field_text))
        self.ip_field.bind('<FocusOut>', lambda event: on_unfocus(event, ip_field_text))

        self.button = Button(window)

    #Displays a message on the chatwindow
    def display_message(self, message):
        self.textbox.insert(END, str(message) )

    #Sets the channels variable (when it's sent to the client from the server)
    def set_channels(self, channels):
        self.channels = channels
    
    #Get the selected channel by the channel list's current selected channel string
    def get_selected_channel(self):
        if not self.channels:
            return None
        
        #TODO make sure this works lol
        return [i for i in self.channels if i.get() == self.selected_channel][0]
        

if __name__ == '__main__':
    root = Tk()
    gui = ChatWindow(root)
    root.mainloop()

