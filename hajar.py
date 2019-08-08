import os
import sys
import random
import socket
import select
import datetime
import threading

lock = threading.RLock(); os.system('cls' if os.name == 'nt' else 'clear')

def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def filter_array(array):
    for i in range(len(array)):
        array[i] = array[i].strip()
        if array[i].startswith('#'):
            array[i] = ''

    return [x for x in array if x]

def colors(value):
    patterns = {
        'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
        'G1' : '\033[32;1m', 'Y1' : '\033[33;1m',
        'P1' : '\033[35;1m', 'CC' : '\033[0m'
    }

    for code in patterns:
        value = value.replace('[{}]'.format(code), patterns[code])

    return value

def log(value, status='', color=''):
    value = colors('{color}[{time}] [CC]Mencari Server {color}{status} [CC]{color}{value}[CC]'.format(
        time=datetime.datetime.now().strftime('%H:%M'),
        value=value,
        color=color,
        status=status
    ))
    with lock: print(value)

def log_replace(value, status='Inject', color=''):
    value = colors('{}{} ({})        [CC]\r'.format(color, status, value))
    with lock:
        sys.stdout.write(value)
        sys.stdout.flush()

class inject(object):
    def __init__(self, inject_host, inject_port):
        super(inject, self).__init__()

        self.inject_host = str(inject_host)
        self.inject_port = int(inject_port)

    def log(self, value, color='[G1]'):
        log(value, color=color)

    def start(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.bind((self.inject_host, self.inject_port))
            socket_server.listen(1)
            frontend_domains = open(real_path('/opok.txt.enc')).readlines()
            frontend_domains = filter_array(frontend_domains)
            if len(frontend_domains) == 0:
                self.log('Frontend Domains not found. Please check opok.txt.enc', color='G1')
                return
            self.log(' #====Jangan Lupa Subscribe====#\nLocal Host : 127.0.0.1\nLocal Port : 8080\nInjecksi sukses (200 OK) \nSilahkan Buka Psiphon !!!'.format(self.inject_host, self.inject_port))
            while True:
                socket_client, _ = socket_server.accept()
                socket_client.recv(4096)
                domain_fronting(socket_client, frontend_domains).start()
        except Exception as exception:
            self.log('Gagal!!!Mohon Restar Android anda'.format(self.inject_host, self.inject_port), color='[R1]')

class domain_fronting(threading.Thread):
    def __init__(self, socket_client, frontend_domains):
        super(domain_fronting, self).__init__()

        self.frontend_domains = frontend_domains
        self.socket_tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client = socket_client
        self.buffer_size = 2048
        self.daemon = True

    def log(self, value, status='Ditemukan', 
    color=''):
        log(value, status=status, color=color)

    def handler(self, socket_tunnel, socket_client, buffer_size):
        sockets = [socket_tunnel, socket_client]
        timeout = 0
        while True:
            timeout += 1
            socket_io, _, errors = select.select(sockets, [], sockets, 3)
            if errors: break
            if socket_io:
                for sock in socket_io:
                    try:
                        data = sock.recv(buffer_size)
                        if not data: break
                        # SENT -> RECEIVED
                        elif sock is socket_client:
                            socket_tunnel.sendall(data)
                        elif sock is socket_tunnel:
                            socket_client.sendall(data)
                        timeout = 0
                    except: break
            if timeout == 60: break

    def run(self):
        try:
            self.proxy_host_port = random.choice(self.frontend_domains).split(':')
            self.proxy_host = self.proxy_host_port[0]
            self.proxy_port = self.proxy_host_port[1] if len(self.proxy_host_port) >= 2 and self.proxy_host_port[1] else '443'
            self.log('[CC]Menghubungkan...!!!'.format(self.proxy_host, self.proxy_port))
            self.socket_tunnel.connect((str(self.proxy_host), int(self.proxy_port)))
            self.socket_client.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            self.handler(self.socket_tunnel, self.socket_client, self.buffer_size)
            self.socket_client.close()
            self.socket_tunnel.close()
            self.log('sukses 200 ok!!!'.format(self.proxy_host, self.proxy_port), color='[G1]')
        except OSError:
            self.log('Connection error', color='[CC]')
        except TimeoutError:
            self.log('{} not responding'.format(self.proxy_host), color='[CC]')

G = '\033[1;33m'

print G + '(|_F_A_S_T  C_O_N_E_C_T  U_P_D_A_T_E_|) \n'

print(colors('\n'.join([
        '[G1][!]Recode By :Oprek Bareng','[CC]'
        '[G1][!]Remode By :Oprek Bareng','[CC]'
        '[G1][!]Injection :Telkomsel Opok Agustus 2019','[CC]'
        '[G1][!]Blog https://oprek-bareng.blogspot.com','[CC]' '==========================================','[CC]'
       '[R1]>>>>>|[!]Developers:Aztec Rabbit[!]|<<<<<<','[CC]' '==========================================','[CC]'
        'Inject [!] Telkomsel E106 dan E51 [!]','[CC]'
        
    ])))
def main():
    D = ' [G1][!] masukin password nya !'
    Yes = 'Yes Aku Bisa'
    user_input = raw_input(' [!] input password [!] : ')
    if user_input != Yes:
        sys.exit(' [!] password salah [!]\n')
    print ' [!] Asiyapp Enjoy [!]\n'
    inject('127.0.0.1', '8080').start()

if __name__ == '__main__':
    main()
