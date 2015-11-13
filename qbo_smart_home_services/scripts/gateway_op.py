#encoding=utf-8
import subprocess
import socket

def get_gateway_ip():
    tmp_file = open('/tmp/g.log','w')
    subprocess.call(['ping', '-b', '-c', '3', '255.255.255.255'], stdout=tmp_file)

    tmp_file = open('/tmp/g.log','r')
    ip_list = set()
    for line_raw in tmp_file: #get all possible ip from ping response
        line = line_raw.rstrip() #空行的长度为1，strip后长度才为0
        if line.find('bytes from') != -1:
            left_half = line.split(':')[0]
            ip = left_half.split()[-1]
            ip_list.add(ip)

    gateway_ip = ''
    for ip in ip_list:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, 5005))
            gateway_ip = ip
            s.close()
            break;
        except:
            print 'useless ip %s'%ip
            pass
    print 'gateway ip %s'%gateway_ip
    return gateway_ip
