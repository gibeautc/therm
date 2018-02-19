#!/usr/bin/env python


import sys
import socket
import time
import json

def client_thread(c,inside,outside,sp,h):
	print("Connected")
	sp=c.recv(2)
	try:
		sp=int(sp)
		f=open("set","w")
		f.write(str(sp))
		f.write("\n")
		f.close()
	except:
		print("Set point failed")
		print(sp)
		print(sys.exc_info())
		
	j="{}"
	j=json.loads(j)
	j['inside']=inside
	j['outside']=outside
	j['setpoint']=sp
	j['heatsink']=h
	c.send(json.dumps(j))
	c.send("Q")


print("running")
while True:
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind(("10.0.0.7",5050))
		s.listen(5)
		break
	except:
		print("Port Busy")
		time.sleep(5)
while True:
	try:
		f=open("out.dat","r")
		data=f.read()
		f.close()
	except:
		print("Error with reading file")
		time.sleep(15)
		continue
	lines=data.split("\n")
	try:
		for line in lines:
			if "SET" in line:
				sp=line.split(":")[1]
			if "4ff" in line:
				i=line.split(",")[1].replace(")","")
			if "2ff" in line:
				o=line.split(',')[1].replace(")","")
			if "3fff" in line:
				h=line.split(',')[1].replace(")","")
	except:
		print("error parsing")
		print(sys.exc_info())
		continue
	try:
		print("Waiting")
		c,address=s.accept()
	except:
		print("Error connecting to client")
		continue
	ct=client_thread(c,i,o,sp,h)
