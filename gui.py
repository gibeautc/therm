#!/usr/bin/env python
import psutil
import subprocess
import socket
from appJar import gui
import os
import sys


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
	try:
		s.connect(("10.0.0.7",5050))
	except:
		print("Connection Failed")
		time.sleep(5)
		return
	b=""
	st=""
	while True:
		#need to add a timeout in here
		b=s.recv(1)
		if b=="Q":
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
	app.stopTab()
		
	app.stopTabbedFrame()
	
	#Registered Events
	app.registerEvent(checkUpdate)


app=gui()
if __name__=="__main__":
	appSetup()
#Launch Gui
	app.go()

