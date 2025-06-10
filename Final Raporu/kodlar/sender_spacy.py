# sender_scapy.py - IP fragmentation gönderici (AES + UDP/IP)
from scapy.all import IP, UDP, send
from Crypto.Cipher import AES
import hashlib
import os

DEST_IP = '127.0.0.1'  # Receiver IP
DEST_PORT = 12345
FILENAME = 'file.txt'
AES_KEY = b'0123456789abcdef'
FRAGMENT_SIZE = 512
IP_ID = 1234  # Receiver ile aynı olmalı

# Dosyayı oku ve AES ile şifrele
with open(FILENAME, 'rb') as f:
    plaintext = f.read()

cipher = AES.new(AES_KEY, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
data = cipher.nonce + tag + ciphertext

# Veriyi fragmanlara ayır
fragments = [data[i:i+FRAGMENT_SIZE] for i in range(0, len(data), FRAGMENT_SIZE)]

# Her fragmanı sırayla IP paketi olarak gönder
for i, fragment in enumerate(fragments):
    ip = IP(dst=DEST_IP, id=IP_ID, ttl=64)
    frag_offset = (i * FRAGMENT_SIZE) // 8

    ip.flags = 'MF' if i < len(fragments) - 1 else 0
    ip.frag = frag_offset

    udp = UDP(sport=4444, dport=DEST_PORT)
    packet = ip / udp / fragment
    send(packet, verbose=0)

    print(f"[+] Fragment gönderildi: offset={frag_offset}, uzunluk={len(fragment)}")

# SHA-256 hash yazdır
hash_sender = hashlib.sha256(plaintext).hexdigest()
print("[✓] Tüm parçalar gönderildi.")
print("GONDERILEN VERININ SHA-256 HASH'I:", hash_sender)
