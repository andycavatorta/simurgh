import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
to = 'andycavatorta@gmail.com'
gmail_user = 'andycavatorta@gmail.com'
gmail_password = 'Awaylfot56'
smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()
# Very Linux Specific
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
hostname = socket.gethostname()
my_ip = '%s ip is %s' %  (hostname, ipaddr)
msg = MIMEText(my_ip)
msg['Subject'] = my_ip
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
