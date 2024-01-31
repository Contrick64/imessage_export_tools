from pathlib import Path
import datetime
from re import search,findall
from shutil import copy as shutil_copy

class Chat_Log:
    def __init__(self,filename):
        group_sort = False

        phone_dir = 'misc_phone_numbers'
        group_chat_dir = 'misc_group_chats'
        date_re = r'(\d{4})-(\d\d)-(\d\d)'
        time_re = r'(\d\d)\.(\d\d)\.(\d\d)'
        phone_re = r'(?:\+1 ?)?\(?(?:[0-9]{3})\)?[-.\s]?(?:[0-9]{3})[-.\s]?(?:[0-9]{4})'
        regex = r'^(?:Chat with )?(.?'+phone_re+r'.?|.*?)(?: et al)? on '+date_re+r' at '+time_re+r'\.txt'
        self.isGroupChat = bool(search("^Chat with .*? et al",filename))
        reg_match = findall(regex,filename)
        if not len(reg_match):
            return
        result = reg_match[0]
        self.contact = result[0]
        dt_tuple = []
        for i in result[1:]:
            dt_tuple.append(int(i))

        self.datetime = datetime.datetime(*dt_tuple)
        if self.isGroupChat and group_sort:
            self.sort_as = group_chat_dir
        if not search(phone_re,self.contact):
            self.sort_as = self.contact
        else:
            self.sort_as = phone_dir
    def __repr__(self):
        return "<Chat_Log contact:%c datetime:%d group:%g>" % (
            self.contact,
            self.datetime,
            self.isGroupChat
        )

    def __str__(self):
        c="C"
        if self.isGroupChat:
            c="Group c"
        return f"{c}hat with {self.contact} at {self.datetime} ({self.sort_as})"

if __name__ == "__main__":
    parent_dir = Path(__file__).parent.parent
    # dir_path = Path(parent_dir).joinpath('test_messages')
    dir_path = Path(parent_dir).joinpath('20230526_Messages Folder_Access')
    for filepath in dir_path.glob("**/*"):
        filename = filepath.name
        if filename:
            new_log = Chat_Log(filename)
            if not hasattr(new_log,'contact'):
                continue
            contact_dir = parent_dir.joinpath('exports',new_log.sort_as)
            if not contact_dir.is_dir():
                contact_dir.mkdir()
            shutil_copy(filepath,contact_dir.joinpath(filename))

