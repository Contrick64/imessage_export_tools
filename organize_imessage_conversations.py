import os

dir_path = '../test_messages'

for filename in os.listdir(dir_path) :
    with open(dir_path + '/' + filename,'r',encoding='utf-8') as f: #weird encoding in these files, will investigate further
        contents = f.read()