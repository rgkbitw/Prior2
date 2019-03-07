import random
import datetime
class Issue(object):
    """docstring for Issue."""
    def __init__(self, arg):
        super(Issue, self).__init__()
        self.arg = arg
        self.id = 0
        self.state = "open"
        self.title = "Hello World"
        self.dateofcr = "today"
        self.author = "me"
        self.comments = "Comments"
        self.noc = 0

    def get(self):
        self.id = random.randrange(1,100)
        self.noc = random.randrange(1,100)
        self.state = ["Open","Close"][random.randrange(1,100)%2]
        self.title = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(10)])
        self.dateofcr = datetime.date(random.randrange(2000,2020),random.randrange(1,12),random.randrange(1,28))
        self.author = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(10)])
        self.comments = "https://www.google.com/" + "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(10)])

    def find(self,key):
        if "state" == key:
            return self.state
        elif "dateofcr" == key:
            return self.dateofcr
        elif "noc" == key:
            return self.noc
        elif "id" == key:
            return self.id    
