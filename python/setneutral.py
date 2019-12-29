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

# Main program

# Initialize
ws = initEezy();

def signal_term_handler(signal, frame):
    print ("got SIGTERM; cleaning up")
    setNeutral(ws)
    ws.close
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

# Clean up.
setNeutral(ws)
ws.close
