import os
import datetime
from re import search,findall
from glob import iglob

dir_path = os.path.realpath(os.path.join(os.path.dirname(__file__),'../test_messages/'))

class Chat_Log:
    def __init__(self,filename):
        date_re = '(\d{4})-(\d\d)-(\d\d)'
        time_re = '(\d\d)\.(\d\d)\.(\d\d)'
        regex = f'^(?:Chat with )?(.*?)(?: et al)? on {date_re} at {time_re}\.txt'
        self.isGroupChat = bool(search("^Chat with .*? et al",filename))
        result = findall(regex,filename)[0]
        self.contact = result[0]
        dt_tuple = []
        for i in result[1:]:
            dt_tuple.append(int(i))

        self.datetime = datetime.datetime(*dt_tuple)
    
    def __repr__(self):
        c = self.contact
        d = self.datetime
        g = self.isGroupChat
        return f"<Chat_Log contact:{c} datetime:{d} group:{g}>"

    def __str__(self):
        c="C"
        if self.isGroupChat:
            c="Group c"
        return f"{c}hat with {self.contact} at {self.datetime}"

chat_logs = []

for filepath in iglob(dir_path + '**/**', recursive=True):
    filename = filepath.split('/')[-1]
    if filename:
        new_log = Chat_Log(filename)
        chat_logs.append(new_log)
        print(new_log)
