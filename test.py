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
        text = open('/home/plutonh/index_origin.html', 'r')
        text = text.read()
        changed_time = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        text = text.replace('data', content[:-2].decode())
        text = text.replace('time', changed_time)

        can = can + 1
        print(content[:-2].decode(), '\n', can)

        with open('/home/plutonh/index.html', 'w') as f:
         f.write(text)
         f.close()

        if can == 10:
         repo.index.add(['index.html'])
         repo.index.add(['test.py'])
         repo.index.commit(changed_time)
         origin = repo.remote(name = 'origin')
         subprocess.call("git push -u origin master", shell = True)
         can = 0
