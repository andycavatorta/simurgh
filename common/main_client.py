"""
the job on the client side:

deliver local IP and hostname to server via multicast
listen for messages

receive 'turn' message from server via network, including duration
measure presence of bulbs
return info via network
switch power from 5v to 12v
count for duration
switch power back to 5v

threads:
discover server
listen for messages
measure duration
"""

import json
import socket
import time
import threading
import RPi.GPIO as GPIO

HOSTNAME = ""
IP = ""
SERVER_IP = ""
POWER_RELAY_PIN = 37
SENSOR_PINS = [
    11,
    12,
    13,
    15,
    16,
    18,
    22,
    29,
    31,
    33,
    35,
]
SWITCH_PINS = [
    36,
    37
]


def broadcastIpToServer(msg):
    try:
        MCAST_GRP = '224.0.0.1'
        MCAST_PORT = 10000
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        print "common/main_client.py broadcastIpToServer()", msg
        sock.sendto(msg, (MCAST_GRP, MCAST_PORT))
    except Exception as e:
        print repr(e)

def Recv():
    global lastContactTime
    host = '' 
    port = 50000 
    backlog = 5 
    size = 1024 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog) 
    while 1: 
        client, address = s.accept() 
        data = client.recv(size) 
        if data: 
            if SERVER_IP == "":
                global SERVER_IP
                SERVER_IP = address[0]
            if data == "getSensorData":
                sd = getSensorData()
                print sd
            if data == "startTurn":
                startTurn()
            if data == "endTurn":
                endTurn()
            lastContactTime = time.time()
            #client.send(data) 
        client.close()

recv = threading.Thread(target=Recv)
recv.start()

def startTurn():
    pass

def endTurn():
    pass

def getSensorData():
    socket =  False
    for p in SENSOR_PINS:
        if GPIO.input(p):
            socket = p
            break
    beats = 2
    if GPIO.input(SWITCH_PINS[0]):
        beats = 1
    if GPIO.input(SWITCH_PINS[1]):
        beats = 4
    return [socket,beats]


lastContactTime = 0
serverTimeout = 5.0
def ControlLoop():
    while 1:
        if SERVER_IP == "" or time.time() - lastContactTime > serverTimeout: # if server is missing
            msg = "%s|%s" % (HOSTNAME, IP)
            broadcastIpToServer(msg)
        time.sleep(1)


def main(hostname, ip):
    global HOSTNAME
    global IP
    HOSTNAME = hostname
    IP = ip
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(POWER_RELAY_PIN,GPIO.OUT)
    for pin in SENSOR_PINS:
        GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)    
    for pin in SWITCH_PINS:
        GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    controlloop = threading.Thread(target=ControlLoop)
    controlloop.start()
