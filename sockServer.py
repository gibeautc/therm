#!/usr/bin/env python



import socket
import time
import json

def client_thread(c,inside,outside,sp):
	print("Connected")
	j="{}"
	j=json.loads(j)
	j['inside']=inside
	j['outside']=outside
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

	try:
		lines=data.split("\n")
		i=lines[0].split(",")[1]
		i=i.replace(")","")
		print(i)
		o=lines[1].split(",")[1]
		o=o.replace(")","")
	except:
		print("Error Parsing Data")
		time.sleep(15)
		continue
	
	try:
		print("Waiting")
		c,address=s.accept()
	except:
		print("Error connecting to client")
		continue
	ct=client_thread(c,i,o,0)
