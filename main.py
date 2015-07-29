"""



"""
import commands
import socket

hostnames = ['controller','ray1','ray2','ray3','ray4','ray5','ray6','ray7','ray8','ray9','ray10','ray11','ray12']
staticIpAddresses = ['10.1.1.10','10.1.1.11','10.1.1.12','10.1.1.13','10.1.1.14','10.1.1.15','10.1.1.16','10.1.1.17','10.1.1.18','10.1.1.19','10.1.1.20','10.1.1.21','10.1.1.22',]

cmd = "ip addr list eth0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1"
resp = commands.getstatusoutput(cmd)
print resp
IP = resp[1]
HOSTNAME = socket.gethostname()

if IP:
    #git pull
    #cmd = "cd /home/pi/simurgh/ && git pull -q --all -p"
    #resp = commands.getstatusoutput(cmd)
    #email IP
    from common import  emailIp
else:
    staticIpAddress = staticIpAddresses[hostnames.index(HOSTNAME)]
    cmd = "ip addr add %s dev eth0" % (staticIpAddress)
    print "cmd = ", cmd
    resp = commands.getstatusoutput(cmd)
    print resp
    # assign static IP

if HOSTNAME == 'controller':
    from common import main_server
    main_server.main(hostnames, 50000)
else:
    from common import main_client
    main_client.main(HOSTNAME,IP)


