import socket
from Crypto.Cipher import AES
import hashlib

# AYARLAR
HOST = '127.0.0.1'
PORT = 12345
CHUNK_SIZE = 1024
OUTPUT_FILE = 'received.txt'

# SABIT ANAHTAR
key = b'0123456789abcdef'

# SUNUCUYU BASLAT
s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print("Bağlantı Bekleniyor...")
conn, addr = s.accept()
print("Bağlandı:", addr)

# VERILERI AL VE BIRLESTIR
data = b''
while True:
    chunk = conn.recv(CHUNK_SIZE)
    if not chunk:
        break
    data += chunk

# VERIDEN NONCE, TAG VE CIPHERTEXT AYIR
nonce = data[:16]
tag = data[16:32]
ciphertext = data[32:]

# AES ILE COZ
cipher = AES.new(key, AES.MODE_EAX, nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, tag)

# DOSYAYA YAZ
with open(OUTPUT_FILE, 'wb') as f:
    f.write(plaintext)

print("Dosya Kapatıldı:", OUTPUT_FILE)

# SHA-256 HASH HESAPLA
hash_receiver = hashlib.sha256(plaintext).hexdigest()
print("Alınan Dosya HASH:", hash_receiver)

conn.close()
s.close()
