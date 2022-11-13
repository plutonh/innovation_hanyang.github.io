import serial

port = '/dev/ttyACM0'
brate = 9600 #boudrate
cmd = 'temp'

seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)

seri.write(cmd.encode())

a = 1
cnt = 100

while a:
    cnt = cnt - 1
    if seri.in_waiting != 0 :
        content = seri.readline()
        print(content[:-2].decode())

