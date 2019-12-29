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

def linksRechts(ws):

  print("Arm naar links")
  for x in range(0,-90,-1):
    setServo(ws,1,x)
    time.sleep(0.05)
  print("Arm naar rechts")
  for x in range(-90,90):
    setServo(ws,1,x)
    time.sleep(0.05)
  print("Arm naar het midden")
  for x in range(90,0,-1):
    setServo(ws,1,x)
    time.sleep(0.05)
  return

def omlaagOmhoog(ws):

  print("Arm omlaag")
  for x in range(0,-40,-1):
    setServo(ws,3,x)
    time.sleep(0.05)
  print("Arm omhoog")
  for x in range(-40,40):
    setServo(ws,3,x)
    time.sleep(0.05)
  print("Arm naar het midden")
  for x in range(40,0,-1):
    setServo(ws,3,x)
    time.sleep(0.05)
  return

def voorAchter(ws):

  print("Arm naar voren")
  for x in range(0,-60,-1):
    setServo(ws,2,x)
    time.sleep(0.05)
  print("Arm naaar achteren")
  for x in range(-60,60):
    setServo(ws,2,x)
    time.sleep(0.05)
  print("Arm naar het midden")
  for x in range(60,0,-1):
    setServo(ws,2,x)
    time.sleep(0.05)
  return

def openDicht(ws):

  print("Grijper open")
  setServo(ws,4,-50)
  time.sleep(0.5)
  print("Grijper dicht")
  setServo(ws,4,0)
  time.sleep(0.5)
  return

def hekOpenDicht(ws):

  print("Hek open")
  setServo(ws,5,0)
  time.sleep(0.5)
  print("Hek dicht")
  setServo(ws,5,80)
  time.sleep(0.5)
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

setNeutral(ws)
# Keep looping over the effects
while True:
  try:
    #linksRechts(ws)
    #omlaagOmhoog(ws)
    #voorAchter(ws)
    #openDicht(ws)
    hekOpenDicht(ws)
  except KeyboardInterrupt:
    break

# Clean up.
setNeutral(ws)
ws.close
