#!/usr/local/bin/python3

# Where to connect?
eezyHost="192.168.28.116"
eezyPort="8000"

# Import the stuff we need
import websocket
import time
import random
import signal
import sys

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
  return


# Main program

# Initialize
ws = initEezy();

def signal_term_handler(signal, frame):
    print ("got SIGTERM; cleaning up")
    setNeutral(ws)
    ws.close
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

# Move the arm around a couple of times.
for x in range(10):
  print("Set arm to 90,90,50")
  setArm(ws,90,90,50,80)
  time.sleep(2)
  print("Set arm to 90,90,130")
  setArm(ws,90,90,130,80)
  time.sleep(2)
  #print("Set arm to 90,90,90")
  #setArm(ws,90,120,90,80)
  #time.sleep(5)

print("Set arm to 90,90,90")
setArm(ws,90,90,90,80)
time.sleep(5)
ws.close
