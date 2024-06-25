from pathlib import Path
import datetime
from re import search,findall
from shutil import copy as shutil_copy

# CHANGE THESE TO THE CORRECT FULL PATHS 
input_dir_path = '../jf_imessages'
output_dir_path = '../jf_imessages_sorted'

class Bornstein_Chat_Log:
    def __init__(self,filename):
        group_sort = True

        phone_dir = 'misc_phone_numbers'
        group_chat_dir = 'misc_group_chats'
        date_re = r'(\d{4})-(\d\d)-(\d\d)'
        time_re = r'(\d\d)\.(\d\d)(?:\.(\d\d))?'
        phone_re = r'^.{0,2}[\+\d]\d+'
        regex = r'^(?:Chat with )?(.*?)(?: et al)? on '+date_re+r' at '+time_re+r'(?:-\d+)?\.txt'
        self.isGroupChat = bool(search("^Chat with .*? et al",filename))
        reg_match = findall(regex,filename)
        if not len(reg_match):
            return
        result = reg_match[0]
        self.contact = str(result[0])
        dt_tuple = []
        for i in result[1:]:
            i = i if i else 0
            dt_tuple.append(int(i))

        self.datetime = datetime.datetime(*dt_tuple)
        if self.isGroupChat and group_sort:
            self.sort_as = group_chat_dir
        elif not search(phone_re,self.contact):
            self.sort_as = self.contact
        else:
            self.sort_as = phone_dir
    def __repr__(self):
        return "<Chat_Log contact:{} datetime:{} group:{}>".format(
            self.contact,
            self.datetime,
            self.isGroupChat
        )

    def __str__(self):
        c="C"
        if self.isGroupChat:
            c="Group c"
        return f"{c}hat with {self.contact} at {self.datetime} ({self.sort_as})"
    
class Fernandez_Chat_Log:
    def __init__(self, filename):
        self.misc_phone_dir = 'misc_phone_numbers'
        self.misc_group_dir = 'misc_group_chats'
        self.phone_re = r'^.{0,2}[\+\d]\d+'
        self.regex = r'Messages - (.*?&?).txt'
        self.isGroupChat = bool(search("&",filename))
        self.reg_match = findall(self.regex,filename)
        if not len(self.reg_match):
            return
        result = self.reg_match[0]
        self.contacts = [contact.strip() for contact in result.split('&')]
        self.first_contact = self.find_first_contact()
        if self.first_contact:
            self.sort_as = self.first_contact
            return
        if self.isGroupChat:
            self.sort_as = self.misc_group_dir
        else:
            self.sort_as = self.misc_phone_dir
    
    def find_first_contact(self):
        for contact in self.contacts:
            if not search(self.phone_re,contact):
                return contact
        return False


if __name__ == "__main__":
    dir_path = Path(input_dir_path)
    export_dir = Path(output_dir_path)
    for filepath in dir_path.glob("**/*"):
        filename = filepath.name
        if filename:
            new_log = Fernandez_Chat_Log(filename)
            contact_dir = export_dir.joinpath(new_log.sort_as)

            if not contact_dir.is_dir():
                contact_dir.mkdir(parents=True)
            shutil_copy(filepath,contact_dir.joinpath(filename))

    for dir in export_dir.glob("*"):
        file_count = len(list(dir.glob("*")))
        print(f"{dir.stem}, {file_count}")