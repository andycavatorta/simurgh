"""
What do the client and server talk about?

client->server:
    broadcast to discover server

server->client:
    turn { True | False }
    request bulb and switch position

"""

import socket
import struct
import threading
 
clientmanager = False


# move to thread
def Recv():
    MCAST_GRP = '224.0.0.1'
    MCAST_PORT = 10000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
      print sock.recv(1024)
 
recv = threading.Thread(target=Recv)
recv.start()

class ClientManager():
    def __init__(self, hostnames_l,clientPort):
        self.clientPort = clientPort
        self.maxMsgSize = 1024
        self.clients = {}
        for name in hostnames_l:
            self.clients[name] = Client(name)
    def setPresence(self, hostname, b):
        self.clients[hostname] = b
    def send(self, hostname, msg):
        client = self.clients[hostname]
        if self.clients[hostname].present:
            size = 1024 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            s.connect((client.ip,self.clientPort)) 
            s.send(msg) 
            data = s.recv(self.maxMsgSize) 
            s.close() 
            print data
            return data

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

def main(client_hostnames_l, clientPort):
    global clientmanager
    clientmanager = ClientManager(client_hostnames_l,clientPort)


main(['controller','ray1','ray2','ray3','ray4','ray5','ray6','ray7','ray8','ray9','ray10','ray11','ray12'],50000)