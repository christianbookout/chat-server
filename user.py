#class for the server and its clients to hold a list of all users connected to the server
class User:
    def __init__(self, username, connection_address):
        self.username = username
        self.connection_address = connection_address
        self.id = hash((self.connection_address[0]))

    def __eq__(self, other_user):
        return other_user.id == self.id

    def __repr__(self):
        return self.username + " @" + self.connection_address[0]
