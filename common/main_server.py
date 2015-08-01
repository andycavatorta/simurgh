"""
Marina:
    x finish painting
    experiment with color circle application
        apply color circles

Justyna & Ayo
    single ray test:
        secure components
        add wiring
        test one ray on network

Marina & Andy
    finish all rays
        secure components
        complete cables
        add wiring
        test

Andy:
    x sand doors
    x fetch breakout cables from TinkerSphere
    x add dynamic timing
    x add melody detection
    add MIDI out
    work "offline" with static IPs or offline DHCP
    find location to test:
        get internet from 3rd floor to basement?
        buy superlong ether cable

"""
import json
import socket
import struct
import time
import threading
 
BEAT_PERIOD = 0.25
HOSTS = []
clientmanager = False

def Recv():
    MCAST_GRP = '224.0.0.1'
    MCAST_PORT = 10000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        msg = sock.recv(1024)
        clienthost, clientip = msg.split("|")
        clientmanager.setPresence(clienthost, clientip)
        #print "main_server.py Recv() 2", clienthost, clientip

class ClientManager():
    def __init__(self, hostnames_l,clientPort):
        self.clientPort = clientPort
        self.maxMsgSize = 1024
        self.clients = {}
        for name in hostnames_l:
            self.clients[name] = Client(name)
    def setPresence(self, hostname, b_ip):
        if b_ip == False:
            self.clients[hostname].present = False
        else:
            self.clients[hostname].present = True
            self.clients[hostname].ip = b_ip
        #print repr(self.clients[hostname].__dict__)
    def send(self, hostname, msg):
        client = self.clients[hostname]
        if self.clients[hostname].present:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.connect((client.ip,self.clientPort)) 
                s.send(msg) 
                data = s.recv(self.maxMsgSize) 
                s.close() 
                #print hostname, msg, data
                return data
            except Exception as e:
                self.clients[hostname].present = False

class Client():
    def __init__(self, hostname):
        self.hostname = hostname
        self.ip = ""
        self.present = False
        self.noteLength = 4 # [ 1,4,16 ]
        self.pitch = False # [0,1,2,3,4,5,6,7,8,9,10,11]
    def setPresent(self, b):
        self.present = b
    def setIp(self, ip):
        self.ip = ip
    def setNoteLength(self,nl):
        self.noteLength = nl
    def setPitch(self,pitch):
        self.pitch = pitch

def makeMidiMsg(bulbNumber):
    print "makeMidiMsg:", bulbNumber

def sendMIDI(channel, cmd, pitch, velocity):
    pass

def patternDetection():
    global HOSTS
    currentPattern = []
    targetPattern = [
        [False,4], # Rest
        [False,4], # G
        [False,1], # Bb
        [False,1], # C
        [False,4], # Eb
        [False,16], # C 
        [False,4], # C
        [False,4], # Eb
        [False,1], # G
        [False,1], # Bb
        [False,4], # C
        [False,16], # Bb
    ]
    for host in HOSTS:
        currentPattern.append([clientmanager.clients[host].pitch,clientmanager.clients[host].noteLength])
    print currentPattern
    found_b = False
    for i in range(12):
        if currentPattern == targetPattern:
            found_b = True
            break
        
        currentPattern.insert(0, currentPattern.pop())
    if found_b:
        print "need to add MIDI msg when found"

def ControlLoop():
    global HOSTS
    # msgs = ["startTurn","endTurn","sensorData"]
    while 1:
        for hi in range(len(HOSTS)):
            host_previous = HOSTS[ hi - 1 ] 
            host_current = HOSTS[ hi ]
            host_next = HOSTS[ hi  - (len(HOSTS)-1) ]

            if clientmanager.clients[host_previous].present:
                clientmanager.send(host_previous, "endTurn")
            if clientmanager.clients[host_current].present:
                makeMidiMsg(clientmanager.clients[host_current].pitch)
                clientmanager.send(host_current, "startTurn")
            if clientmanager.clients[host_next].present:
                sd_json = clientmanager.send(host_next, "getSensorData")
                sd_l = json.loads(sd_json)
                print host_next, sd_l
                clientmanager.clients[host_next].setPitch(sd_l[0])
                clientmanager.clients[host_next].setNoteLength(sd_l[1])
                patternDetection()
            turnPeriod = clientmanager.clients[host_current].noteLength * BEAT_PERIOD 
            time.sleep(turnPeriod)

def main(client_hostnames_l, clientPort):
    global clientmanager
    global HOSTS

    HOSTS = client_hostnames_l
    HOSTS.sort()
    HOSTS = HOSTS[1:]

    clientmanager = ClientManager(client_hostnames_l,clientPort)
    recv = threading.Thread(target=Recv)
    recv.start()
    controlloop = threading.Thread(target=ControlLoop)
    controlloop.start()

main(['controller','ray01','ray02','ray03','ray04','ray05','ray06','ray07','ray08','ray09','ray10','ray11','ray12'],50000)
