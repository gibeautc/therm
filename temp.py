#!/usr/bin/env python


import os
import glob
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device1 =base_dir + '28-04165153a4ff'
device2 =base_dir + '28-0316459cc2ff'
device3 =base_dir + '28-041650f23fff'


SETTEMP=60
HSTEMP=100
onCnt=1.0
offCnt=1.0

sensors=[]
sensors.append(device1+'/w1_slave')
sensors.append(device2+'/w1_slave')
sensors.append(device3+'/w1_slave')

def read_temp_raw(device_file):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines[len(lines)-2:]
def read_temp():
    temps=[]
    for device in sensors:
        lines = read_temp_raw(device)
        #print(device)
        #print(lines)
        #print("")
        if lines[0].strip()[-3:] != 'YES':
            continue
        time.sleep(0.2)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            print(device,temp_f)
            temps.append(temp_f)
        if len(temps)==3:
            i=heat(temps)
            if i==1:
                print("STATUS:ON")
            else:    
                print("STATUS:OFF")
        
def heat(temps):
    global HSTEMP,SETTEMP,onCnt,offCnt
    print("SET:"+str(SETTEMP))
    if temps[1]-temps[0]>-2:
        print("NOTE:Outside is too warm")
        return 0
    if SETTEMP>temps[0]:
        if temps[2]<HSTEMP:
            GPIO.output(17,GPIO.HIGH)
            onCnt=onCnt+1
            return 1

    GPIO.output(17,GPIO.LOW)
    offCnt=offCnt+1
    return 0

f=open('set')
SETTEMP=int(f.read())
read_temp()

