from git import Repo
import subprocess
import git
import serial
import re
import time

port = '/dev/ttyACM0'
brate = 9600 #boudrate
cmd = 'temp'
repo = Repo.init('/home/plutonh')

seri = serial.Serial(port, baudrate = brate, timeout = None)
seri.write(cmd.encode())
#print(seri.name)

a = 1
can = 0

while a:
    if seri.in_waiting != 0 :

        content = seri.readline()
        num = int(content[:-2].decode())

        if num < 20:
            state = "여유"
        elif num >= 20 and num < 40:
            state = "보통"
        elif num >= 40 and num < 60:
            state = "혼잡"
        else  :
            state = "매우혼잡"

        text = open('/home/plutonh/index_origin.html', 'r')
        text = text.read()
        changed_time = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        text = text.replace('data', state)
        text = text.replace('time', changed_time)

        can = can + 1
        #print(content[:-2].decode(), '\n', can)

        with open('/home/plutonh/index.html', 'w') as f:
            f.write(text)
            f.close()

        # adding, commiting and pushing command
        if can == 10: # can == 535: approximately 30 seconds
            repo.index.add(['index.html'])
            repo.index.add(['test.py'])
            repo.index.commit(changed_time)
            origin = repo.remote(name = 'origin')
            subprocess.call("git push -u origin master", shell = True)
            can = 0
