# receiver_scapy.py - Windows uyumlu IP fragmentation alıcı
from scapy.all import sniff, IP, get_if_list
from Crypto.Cipher import AES
import hashlib
import sys

AES_KEY = b'0123456789abcdef'
OUTPUT_FILE = 'received_scapy.txt'
TARGET_ID = 1234
received_bytes = {}

# Kullanılabilir arayüzleri yazdır
print("[*] Aktif ağ arayüzleri:")
for i, iface in enumerate(get_if_list()):
    print(f"  {i}. {iface}")

# Kullanıcıdan interface seçmesini iste
index = int(input("Lütfen dinlemek istediğiniz arayüzün numarasını girin: "))
iface_name = get_if_list()[index]
print(f"[*] Seçilen arayüz: {iface_name}")

def handle_packet(packet):
    if IP in packet and packet[IP].id == TARGET_ID:
        frag_offset = packet[IP].frag * 8
        payload = bytes(packet[IP].payload.payload)  # UDP payload

        received_bytes[frag_offset] = payload
        print(f"[+] Parça alındı: offset={frag_offset}, uzunluk={len(payload)}")

        if packet[IP].flags == 0:
            print("[-] Son parça geldi. Tüm parçalar toplanıyor...")
            reassemble_and_decrypt()

def reassemble_and_decrypt():
    try:
        data = b''.join(received_bytes[offset] for offset in sorted(received_bytes))
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]

        cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        with open(OUTPUT_FILE, 'wb') as f:
            f.write(plaintext)

        print("[✓] Dosya çözüldü ve kaydedildi:", OUTPUT_FILE)
        print("[✓] SHA-256 Hash:", hashlib.sha256(plaintext).hexdigest())
        sys.exit(0)

    except Exception as e:
        print("[!] Hata:", e)
        sys.exit(1)

print("[*] UDP paketleri dinleniyor...")
sniff(prn=handle_packet, iface=iface_name, store=0)
