from collections import deque

class DataBuffer:
    def __init__(self):
        print("New DataBuffer instantiated.")
        self.unprocessedTweets = deque([], 50)

    def popItem(self):
        return self.unprocessedTweets.pop()
        
    def pushItem(self, item):
        self.unprocessedTweets.appendleft(item)
        
    def length(self):
        return len(self.unprocessedTweets)
    
    def dumpItems(self, dataBacklog):
        try:
            backlog = open(dataBacklog, 'x')
        except FileExistsError:
            try:
                backlog = open(dataBacklog, 'a')
            except PermissionError:
                print("Unable to write backlogged data to buffer. Data may be discarded.")
                return
        
        while self.length() > 10:
            backlog.write(self.popItem())