
import socket
from Crypto.Cipher import AES
import hashlib

# AYARLAR
HOST = '127.0.0.1'
PORT = 12345
CHUNK_SIZE = 1024
FILENAME = 'file.txt'

# SABIT ANAHTAR
key = b'0123456789abcdef'

# AES SIFRELEYICIYI OLUSTUR
cipher = AES.new(key, AES.MODE_EAX)

# DOSYAYI OKU
with open(FILENAME, 'rb') as f:
    plaintext = f.read()

# DOSYAYI SIFRELE
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

# NONCE, TAG VE SIFRELI VERIYI BIRLESTIR
data = cipher.nonce + tag + ciphertext

# SHA-256 HASH HESAPLA
hash_sender = hashlib.sha256(plaintext).hexdigest()
print("Gönderilen Dosya HASH:", hash_sender)

# BAGLANTI KUR
s = socket.socket()
s.connect((HOST, PORT))

# VERIYI PARCA PARCA GONDER
for i in range(0, len(data), CHUNK_SIZE):
    chunk = data[i:i+CHUNK_SIZE]
    s.sendall(chunk)

print("Dosya Gönderildi.")
s.close()
