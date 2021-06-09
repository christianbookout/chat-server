import server

class Channel:
    def __init__(self, title, is_public):
        self.title = title
        self.is_public = is_public
        
        if self.is_public:
            self.users = server.users
        else:
            self.users = []


    def add_user(self, user):
        self.users.append(user)
