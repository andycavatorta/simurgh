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
    MCAST_GRP = '224.0.0.1'
    MCAST_PORT = 10000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    print "common/main_client.py broadcastIpToServer()", msg
    sock.sendto(msg, (MCAST_GRP, MCAST_PORT))

def Recv():
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
            global SERVER_IP
            SERVER_IP = address[0]
            print "Recv()", data, address
            #client.send(data) 
        client.close()

recv = threading.Thread(target=Recv)
recv.start()

def startTurn():
    pass

def endTurn():
    pass

def sensorData():
    return [0,0]

def main(hostname, ip):
    global HOSTNAME
    global IP
    HOSTNAME = hostname
    IP = ip
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(POWER_RELAY_PIN,GPIO.OUT)
    for pin in SENSOR_PINS:
        print "sensorPin=", pin
        GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    msg = "%s|%s" % (HOSTNAME, IP)
    while SERVER_IP == "":
        broadcastIpToServer(msg)
        time.sleep(1)

