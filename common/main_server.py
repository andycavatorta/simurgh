"""
What do the client and server talk about?

client->server:
    broadcast to discover server

server->client:
    turn { True | False }
    request bulb and switch position

"""
import json
import socket
import struct
import time
import threading
 
BEAT_PERIOD = 0.25
clientmanager = False

# move to thread
def Recv():
    #print "main_server.py Recv() 2"
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
        print "main_server.py Recv() 2", clienthost, clientip

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
        print repr(self.clients[hostname].__dict__)
    def send(self, hostname, msg):
        client = self.clients[hostname]
        if self.clients[hostname].present:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.connect((client.ip,self.clientPort)) 
                s.send(msg) 
                data = s.recv(self.maxMsgSize) 
                s.close() 
                print data
                return data
            except Exception as e:
                self.clients[hostname].present = False


class Client():
    def __init__(self, hostname):
        self.hostname = hostname
        self.ip = ""
        self.present = False
        self.noteLength = 2 # [ 1,2,4 ]
        self.pitch = 0 # [0,1,2,3,4,5,6,7,8]
    def setPresent(self, b):
        self.present = b
    def setIp(self, ip):
        self.ip = ip
    def setNoteLength(self,nl):
        self.noteLength = nl
    def setPitch(self,pitch):
        self.pitch = pitch

def ControlLoop():
    justhosts_l = clientmanager.clients.keys()
    justhosts_l.sort()
    justhosts_l = justhosts_l[1:]
    # msgs = ["startTurn","endTurn","sensorData"]
    while 1:
        for hi in range(len(justhosts_l)):
            host_previous = justhosts_l[ hi - 1 ] 
            host_current = justhosts_l[ hi ]
            host_next = justhosts_l[ hi  - (len(justhosts_l)-1) ]

            print "host_previous",host_previous
            print "host_current", host_current
            print "host_next",host_next
            print 

            if clientmanager.clients[host_previous].present:
                clientmanager.send(host_previous, "endTurn")
            if clientmanager.clients[host_current].present:
                clientmanager.send(host_current, "startTurn")
            if clientmanager.clients[host_next].present:
                clientmanager.send(host_next, "getSensorData")
            turnPeriod = clientmanager.clients[host_current].noteLength * BEAT_PERIOD       
            time.sleep(turnPeriod)

def main(client_hostnames_l, clientPort):
    global clientmanager
    clientmanager = ClientManager(client_hostnames_l,clientPort)
    recv = threading.Thread(target=Recv)
    recv.start()
    controlloop = threading.Thread(target=ControlLoop)
    controlloop.start()

main(['controller','ray01','ray02','ray03','ray04','ray05','ray06','ray07','ray08','ray09','ray10','ray11','ray12'],50000)
