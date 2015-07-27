"""



"""
import commands
import socket

cmd = "ip addr list eth0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1"
resp = commands.getstatusoutput(cmd)
print resp
IP = resp[1]
HOSTNAME = socket.gethostname()

if IP:
    # git pull
    cmd = "cd /home/pi/simurgh/ && git pull -q --all -p"
    resp = commands.getstatusoutput(cmd)
    # email IP
    from common import  emailIp
else:
    pass
    # assign static IP



