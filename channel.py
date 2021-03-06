import server
import uuid
class Channel:
    def __init__(self, title, is_public):
        self.title = title
        self.is_public = is_public
        self.id = str(uuid.uuid4())
        self.message_history = []
        self.vc_users = []

        if self.is_public:
            self.users = server.connected_users
            # ^^ why did i do that???
        else:
            self.users = []

    def __eq__(self, other):
        return self.id == other.id

    def add_user(self, user):
        self.users.append(user)

    def join_voice(self, user):
        self.vc_users.append(user)

    @staticmethod
    def get_channel(channels, other):
        try:
            return [i for i in channels if other == i][0]
        except:
            return None

    def append_message(self, message):
        self.message_history.append(message)

    def message_history_str(self):
        return str([i.content for i in self.message_history])
