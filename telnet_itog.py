import getpass
import telnetlib
import time

HOST = "10.10.10.3"
user='admin'
password='admin'

telnet = telnetlib.Telnet(HOST)

telnet.set_debuglevel(6)

telnet.read_until(b"Username:")
telnet.write(user.encode('utf-8')+ b'\n')

telnet.read_until(b"Password: ")
telnet.write(password.encode('utf-8')+ b'\n')
time.sleep(0.5)

telnet.write(b'conf t\n')
time.sleep(0.5)
telnet.write(b'interface loopback 0\n')
time.sleep(0.5)
telnet.write(b'ip add 8.8.8.8 255.255.255.255\n')
time.sleep(0.5)


