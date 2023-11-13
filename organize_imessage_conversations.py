import os

dir_path = '../test_messages'

for filename in os.listdir(dir_path) :
    with open(dir_path + '/' + filename) as f:
        print(f.readline())