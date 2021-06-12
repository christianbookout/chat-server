class Message: 
    def __init__(self, author, content, channel, timestamp):
        self.author = author
        self.content = content
        self.channel = channel
        self.timestamp = str(timestamp)
        