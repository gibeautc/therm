#!/usr/bin/env python
import socket
import time
import json
import os


if os.path.isdir("/home/pi"):
	system="pi"
else:
	system="chadg"





toGuiPath="/home/"+system+"/pipeToGui"
fromGuiPath="/home/"+system+"/pipeFromGui"

try:
	os.mkfifo(toGuiPath)
except:
	pass
	#if not os.path.isfile(fromGuiPath):
try:
	os.mkfifo(fromGuiPath)
except:
	pass

pipeOut=os.open(toGuiPath,os.O_WRONLY|os.O_NONBLOCK)
pipeIn=os.open(fromGuiPath,os.O_RDWR)


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)



while True:
	try:
		s.connect(("10.0.0.7",5050))
	except:
		print("Connection Failed")
		time.sleep(5)
		continue
	b=""
	st=""
	while True:
		b=s.recv(1)
		if b=="Q":
			break
		st=st+b
	s.close()
	try:
		j=json.loads(st)
		os.write(pipeOut,str(j))
		print("Write to pipe succesfull")
	except:
		print("JSON loads or os.write failed")
		print(st)
			
	time.sleep(5)


