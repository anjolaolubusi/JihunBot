import sys
import pickle

with open(sys.argv[1]) as f:
    content = f.readlines()

cleaned = ""

for line in content:
    text = ""
    split_lines = line.split()
    for i in range(len(split_lines)):
        if(split_lines[i][:1] != ':'):
            text += split_lines[i].lower()
        else:
            text += split_lines[i]
        if(i != len(line.split())-1):
            text += " "
    cleaned += text + '\n'

file = open('out.txt', 'w')
file.write(cleaned)
file.close()
