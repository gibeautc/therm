#!/usr/bin/env python
import psutil
import subprocess
import socket
from appJar import gui
import os
import sys
import time
import json


SET=60
if os.path.isdir("/home/pi"):
	system="pi"
else:
	system="chadg"


tools=["UPDATE","CLOSE","OFF"]

def tbFunc(button):
	print("ToolBar Button "+str(button)+" was pressed")
	if button=="CLOSE":
		#gpsObj.running=False
		exit()
	if button=='GPS':
		app.showSubWindow("gpsWindow")
	if button=="OFF":
		shutdown=app.yesNoBox("Shutdown","Do you really want to shut down the system?",parent=None)
		if shutdown:
			#should probably shutdown other processes?
			#will need to include a way for them to know they should shutdown
			#so that MySQL connections and other stuff is closed?
			subprocess.call("shutdown -H now",shell=True)
		return 
	if button=="UPDATE":
		app.thread(gitPull)
		
def press(but):
	global SET
	if but=="UP":
		SET=SET+1
		checkUpdate()
		return
	if but=="DOWN":
		SET=SET-1
		checkUpdate()
		

def haveInternet(host="8.8.8.8", port=53, timeout=3):
	"""
	Host: 8.8.8.8 (google-public-dns-a.google.com)
	OpenPort: 53/tcp
	Service: domain (DNS/TCP)
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print ex.message
		return False

	
def checkUpdate():
	app.thread(checkUpdateThread)

def checkUpdateThread():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect(("10.0.0.7",5050))
		s.settimeout(2)
		#s.send(str(SET))
	except:
		print("Connection Failed")
		return
	try:
		s.send(str(SET))
	except:
		print("Error Sending Set Point")
		print(sys.exc_info())
		s.close()
		return
	b=""
	st=""
	while True:
		#need to add a timeout in here
		try:
			b=s.recv(1)
		except:
			print("Timout for recv")
			print(sys.exc_info())
			s.close()
			return
		if b=='`':
			break
		st=st+b
	s.close()
	try:
		j=json.loads(st)
		print("Got new data")
		print(j)
	except:
		print("JSON loads or os.write failed")
		print(st)
		print(sys.exc_info())
		return
	try:
		app.queueFunction(app.setLabel,"lbOt",j['outside'])
		#app.setLabel("lbOt",j['outside'])
	except:	
		app.queueFunction(app.setLabel,"lbOt","ERROR")
		#app.setLabel("lbOt","ERROR")
	
	try:
		#app.setLabel("lbIt",j['inside'])
		app.queueFunction(app.setLabel,"lbIt",j['inside'])
	except:
		#app.setLabel("lbIt","ERROR")
		app.queueFunction(app.setLabel,"lbIt","ERROR")

	try:
		#app.setLabel("lbSp",j['setpoint'])
		app.queueFunction(app.setLabel,"lbSp",j['setpoint'])
	except:
		#app.setLabel("lbSp","ERROR")
		app.queueFunction(app.setLabel,"lbSp","ERROR")

	try:
		#app.setLabel("lbHs",j['heatsink'])
		app.queueFunction(app.setLabel,"lbHs",j['heatsink'])
	except:
		#app.setLabel("lbHs","ERROR")
		app.queueFunction(app.setLabel,"lbHs","ERROR")

def appSetup():
	if system=="pi":
		app.setGeometry("fullscreen")
	else:
		app.setSize(800,480)
	app.setTitle("Office Pi")
	#Tool BAR setup
	app.addToolbar(tools,tbFunc,findIcon=True)
	
	
	#Status Bar Setup
	app.addStatusbar(fields=4)
	app.setStatusbarWidth(4,3)
	app.setStatusbarBg("red",3)
	app.setStatusbar("GPS",3)
	
	#Main Tabbed Frame
	app.startTabbedFrame("Main")
	
	app.startTab("Office")
	app.addLabel("OutSidelb","OutSide Temp:",0,0)
	app.addLabel("Insidelb","Inside Temp:",1,0)
	app.addLabel("SetPointlb","Set Point:",2,0)
	app.addLabel("HeatSinklb","Heat Sink Temp:",3,0)
	app.addLabel("lbOt","00.000",0,1)
	app.addLabel("lbIt","00.000",1,1)
	app.addLabel("lbSp","00.000",2,1)
	app.addLabel("lbHs","00.000",3,1)
	app.addButton("UP",press,4,0)
	app.addButton("DOWN",press,4,1)
	app.stopTab()
		
	app.stopTabbedFrame()
	
	#Registered Events
	app.registerEvent(checkUpdate)
	app.setPollTime(10000)


app=gui()
if __name__=="__main__":
	appSetup()
#Launch Gui
	app.go()

