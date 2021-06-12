import os
import random
from tkinter import Tk, scrolledtext, Text, Button, OptionMenu, StringVar
from tkinter.constants import END, INSERT, LEFT, BOTTOM, CENTER, TOP
from client import Client
from message import Message
from channel import Channel
from re import sub
import pathlib
from datetime import datetime
#from ttkthemes import ThemedStyle

port_field_text = "Enter port"
ip_field_text = "Enter ip"
message_field_text = "Send a message in "

class ChatWindow:
    #initialize a chat window w/ a message display field, chat box, ip field, and port field 
    def __init__(self, window):
    
        #self.selected_channel = "general"

        self.window = window
        window.title("Chat Server")
        self.textbox = scrolledtext.ScrolledText(window)
        self.textbox.insert(END, "Enter the ip and port of the server you'd like to connect to.")
        self.textbox.pack()

        self.ip_field = Text(window, height=2, width=50)
        self.ip_field.insert(INSERT, ip_field_text)
        self.ip_field.pack(side=LEFT)
        self.ip_field['foreground'] = 'gray'

        #Event when widget comes into focus, removes the default gray placeholder text and makes the text black
        def on_focus(widget, placeholder_text):
            if sub(r"[\n]*", "",widget.get("1.0", "end")) == placeholder_text:
                widget.delete("1.0", "end")
            widget['foreground'] = 'black'
        
        #Event when the widget comes out of focus, replaces the gray placeholder text as long as the unfocused widget's text is empty 
        def on_unfocus(widget, placeholder_text):
            if sub(r"[\n\t\s]*", "",widget.get("1.0", "end")) == "":
                widget.insert(INSERT, placeholder_text)
                widget['foreground'] = 'gray'
            return 'break'
            

        #Tells the client to send a message of the message_field's contents
        def send_message(event):
            message = self.message_field.get("1.0", "end")
            self.client.send_message(Message(self.client.user, message, self.selected_channel, datetime.now))
            self.message_field.delete("1.0", "end")
            return 'break'

        #Selects the channel from client.channels w/ the name channel
        def select_channel(channel):
            self.message_field.delete("1.0", "end")
            self.textbox.delete("1.0", "end")
            #Remove focus from message field
            root.focus()

            #have to use strings for a optionmenu 
            for i in self.client.channels:
                if i.title == channel:
                    self.selected_channel = i
                    break
            if not self.selected_channel:
                print("channel selection no work? tried to select " + channel)

            self.display_message(str("").join([i.content for i in self.selected_channel.message_history]))

            if not self.window.focus_get() == self.message_field:
                on_unfocus(self.message_field, message_field_text + "" + str(self.selected_channel.title))

        #connects to the server when the user presses enter on the port textfield
        def enter_port(event):
            ip = sub(r"[\n\t\s]*", "", self.ip_field.get("1.0", "end"))
            port = int(self.port_field.get("1.0", "end"))

            self.username = self.get_random_name()

            self.client = Client(ip, port, self, self.username)
            if not self.client.connect():
                self.display_message("\nFailed to connect to " + ip + ":" + str(port))
                return
            self.textbox.delete("1.0", "end")
            self.port_field.pack_forget()
            self.ip_field.pack_forget()

            self.selected_channel = None
            titles = [i.title for i in self.client.channels]
            default_value = StringVar(root)
            default_value.set("Select a channel")
            self.channel_dropdown = OptionMenu(window, default_value, *titles, command=select_channel)
            self.channel_dropdown.pack(side=TOP)

            self.message_field = Text(window,height=5,width=100)
            self.message_field.pack(side=BOTTOM)
            self.message_field['foreground'] = 'gray'
            self.message_field.bind('<Return>', send_message)

            self.message_field.bind('<FocusIn>', lambda event: on_focus(event.widget, message_field_text + "" + str(self.selected_channel.title)) if self.selected_channel else None)
            self.message_field.bind('<FocusOut>', lambda event: on_unfocus(event.widget, message_field_text + "" + str(self.selected_channel.title)) if self.selected_channel else None)
            return 'break'
        
        self.port_field = Text(window, height=2, width=10)
        self.port_field.insert(INSERT, port_field_text)
        self.port_field.pack(side=LEFT, padx=20)
        self.port_field['foreground'] = 'gray'

        self.port_field.bind('<Return>', enter_port)
        self.port_field.bind('<FocusIn>', lambda event:on_focus(event.widget, port_field_text))
        self.port_field.bind('<FocusOut>', lambda event: on_unfocus(event.widget, port_field_text))

        self.ip_field.bind('<Return>', lambda event: self.port_field.focus())
        self.ip_field.bind('<FocusIn>', lambda event:on_focus(event.widget, ip_field_text))
        self.ip_field.bind('<FocusOut>', lambda event: on_unfocus(event.widget, ip_field_text))

        self.button = Button(window)

    #Gets a random name from names.txt
    def get_random_name(self):
        with open(os.path.join(str(pathlib.Path().absolute()) + '\\resources\\names.txt')) as f:
                return random.choice(f.read().split('\n'))

    #Displays a message on the chatwindow
    def display_message(self, message):
        self.textbox.insert(END, str(message) )
        self.textbox.see(END)

    #Sets the channels variable (when it's sent to the client from the server)
    def set_channels(self, channels):
        self.channels = channels

    def set_channel(self, channel):
        for message in channel.message_history:
            self.display_message(message)
        

if __name__ == '__main__':
    root = Tk()
    gui = ChatWindow(root)
    root.mainloop()

