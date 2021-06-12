#class for the server and its clients to hold a list of all users connected to the server
import uuid
class User:
    def __init__(self, username, timestamp):
        self.username = username
        self.timestamp = str(timestamp)
        self.id = str(uuid.uuid4())

    def __eq__(self, other_user):
        return other_user.id == self.id

    def __repr__(self):
        return self.username + " @" + self.id
