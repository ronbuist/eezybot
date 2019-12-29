#!/usr/local/bin/python3

# Where to connect?
eezyHost="192.168.28.127"
eezyPort="8000"

# Import the stuff we need
import websocket
import time
import random
import signal
import sys
import os

# Function to connect to the led strip server and initialize the led strip
def initEezy():
  ws = websocket.WebSocket()
  ws.connect("ws://"+eezyHost+":"+eezyPort)
  ws.send("init")
  return(ws)

# Function to set all the EezyBot servos to neutral
def setNeutral(ws):
  ws.send("setneutral")
  return

# Function to set an EezyBot servo to the specified position
def setServo(ws,servo,pos):
  ws.send("setservo " + str(servo) + " " + str(pos))
  return

# Function to open/close the gripper
def setGripper(ws,pos):
  ws.send("setgripper " + str(pos))
  return

# Function to set the arm to the specified position at the given speed
def setArm(ws,pos1,pos2,pos3,speed):
  ws.send("setarm " + str(pos1) + " " + str(pos2) + " " + str(pos3) + " " + str(speed))
  status = ws.recv()
  return

# Function to open/close the gate
def setGate(ws,pos):
  ws.send("setgate " + pos)
  return

def sayIt(text):
  print(text)
  text = "say " + text
  os.system(text)
  return

# Main program

# Initialize
ws = initEezy();

def signal_term_handler(signal, frame):
    print ("got SIGTERM; cleaning up")
    setArm(ws,90,90,90,40)
    setNeutral(ws)
    ws.close
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

# Grab the ball and drop it in the ramp a couple of times.
sayIt("Hekje dicht. Plaats de bal in de knikkerbaan.")
setGate(ws,"close")
time.sleep(5)
sayIt("Ik doe mijn grijper open")
setGripper(ws,40)

for x in range(5):
  print
  print("Iteration", str(x+1))
  sayIt("Op naar het einde van de knikkerbaan.")
  setArm(ws,130,110,150,90)
  #time.sleep(2)
  sayIt("Een beetje naar beneden.")
  setArm(ws,130,120,152,30)
  #time.sleep(1.5)
  sayIt("Hekje open")
  setGate(ws,"open")
  time.sleep(1)
  sayIt("Grijper dicht.")
  setGripper(ws,80)
  time.sleep(0.2)
  sayIt("Een beetje omhoog")
  setArm(ws,130,110,120,40)
  #time.sleep(1)
  sayIt("Hekje dicht.")
  setGate(ws,"close")
  sayIt("Breng het balletje naar boven.")
  setArm(ws,100,110,70,90)
  #time.sleep(2.5)
  sayIt("Een beetje naar rechts")
  setArm(ws,85,110,70,60)
  #time.sleep(1)
  sayIt("Laat het balletje maar vallen")
  setGripper(ws,40)
  time.sleep(1)
  sayIt("Een beetje naar links.")
  setArm(ws,100,110,70,90)
  #time.sleep(1) 

sayIt("Klaar")
time.sleep(1)
setGripper(ws,90)
setArm(ws,100,90,70,80)
#time.sleep(1)
setArm(ws,90,90,90,40)
#time.sleep(2)
ws.close
