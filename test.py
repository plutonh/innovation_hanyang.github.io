import serial
import re
from git.repo import Repo

port = '/dev/ttyACM0'
brate = 9600 #boudrate
cmd = 'temp'
repo = Repo('/home/plutonh')

seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)

seri.write(cmd.encode())

a = 1

while a:
    if seri.in_waiting != 0 :
        text = open('/home/plutonh/index_origin.html', 'r')
        text = text.read()
        content = seri.readline()
        print(content[:-2].decode())
        text = text.replace('data', content[:-2].decode())
        with open('/home/plutonh/index.html', 'w') as f:
         f.write(text)
         f.close() 
        repo.index.add(['index.html')
        repo.index.commit('commit from python')
        origin = repo.remotes[0]
        origin.push()
