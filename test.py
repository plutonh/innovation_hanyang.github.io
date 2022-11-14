from git import Repo
import git
import serial
import re

port = '/dev/ttyACM0'
brate = 9600 #boudrate
cmd = 'temp'
repo = Repo.init('/home/plutonh')
#git.Git('/home/plutonh').clone("git@github.com:plutonh/innovation.github.io.git")
#repo.git.checkout('master')
#repo = git.Repo('/home/plutonh')
#repo.remote().fetch()

seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)

seri.write(cmd.encode())

a = 1
can = 0

#class ProgressPrinter(git.RemoteProgress):
# def line_dropped(self, line):
#  print("line dropped : " + str(line))

while a:
    if seri.in_waiting != 0 :
        can = can + 1
        text = open('/home/plutonh/index_origin.html', 'r')
        text = text.read()
        content = seri.readline()
        print(content[:-2].decode())
        text = text.replace('data', content[:-2].decode())
        with open('/home/plutonh/index.html', 'w') as f:
         f.write(text)
         f.close()
        if can == 10:
         #origin = repo.remote(name = 'origin')
         #origin.pull()
         repo.index.add(['index.html'])
         repo.index.commit('commit from python')
         origin = repo.remote(name = 'origin')
         origin.push()
         #repo.git.push("--set-upstream", "origin", "master")
         can = 0
