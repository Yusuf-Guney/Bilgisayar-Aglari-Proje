# FILE TRANSFER - SENDER WITH AES + FRAGMENTATION + AUTHENTICATION
import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
import os

CHUNK_SIZE = 1024
FILENAME = 'file.txt'
HOST = '127.0.0.1'
PORT = 12345

# Sabit AES anahtarı
key = b'0123456789abcdef'

# Bağlantı kur
s = socket.socket()
s.connect((HOST, PORT))

# Public key al
pubkey_data = s.recv(800)
public_key = RSA.import_key(pubkey_data)

# RSA ile challenge oluştur ve gönder
challenge = os.urandom(16)
cipher_rsa = PKCS1_OAEP.new(public_key)
encrypted_challenge = cipher_rsa.encrypt(challenge)
s.sendall(encrypted_challenge)

# Doğrulama sonucu al
auth_response = s.recv(20)
if auth_response != b"AUTH_OK":
    print("Kimlik doğrulama başarısız!")
    s.close()
    exit()

print("Kimlik doğrulama başarılı, dosya gönderiliyor...")

# Dosyayı oku ve AES ile şifrele
with open(FILENAME, 'rb') as f:
    plaintext = f.read()

cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
data = cipher.nonce + tag + ciphertext

# Veriyi parça parça gönder
for i in range(0, len(data), CHUNK_SIZE):
    chunk = data[i:i+CHUNK_SIZE]
    s.sendall(chunk)

print("VERI PARCALANDI VE GONDERILDI")

# Hash yazdır
hash_sender = hashlib.sha256(plaintext).hexdigest()
print("GONDERILEN VERININ SHA-256 HASH'I:", hash_sender)

s.close()
