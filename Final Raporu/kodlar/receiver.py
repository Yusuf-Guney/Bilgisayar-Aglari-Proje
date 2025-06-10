# FILE TRANSFER - RECEIVER WITH AES + REASSEMBLY + AUTHENTICATION
import socket
import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

CHUNK_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
OUTPUT_FILE = 'received.txt'
key = b'0123456789abcdef'

# RSA anahtarlarını yükle
with open("private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())
with open("public.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print("BAGLANTI BEKLENIYOR...")
conn, addr = s.accept()
print("BAGLANDI:", addr)

# Public key gönder
conn.sendall(public_key.export_key())

# Challenge'ı al ve çöz
encrypted_challenge = conn.recv(256)
cipher_rsa = PKCS1_OAEP.new(private_key)
try:
    challenge = cipher_rsa.decrypt(encrypted_challenge)
    print("DOĞRULAMA BAŞARILI:", challenge.decode(errors='ignore'))
    conn.sendall(b"AUTH_OK")
except:
    print("DOĞRULAMA BAŞARISIZ")
    conn.sendall(b"AUTH_FAIL")
    conn.close()
    s.close()
    exit()

# VERIYI PARCALAR HALINDE AL
data = b''
while True:
    chunk = conn.recv(CHUNK_SIZE)
    if not chunk:
        break
    data += chunk

# VERIYI AYIR VE COZ
nonce = data[:16]
tag = data[16:32]
ciphertext = data[32:]

cipher = AES.new(key, AES.MODE_EAX, nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, tag)

# Dosyayı yaz
with open(OUTPUT_FILE, 'wb') as f:
    f.write(plaintext)

print("VERI BIRLEŞTIRILDI VE COZULDU:", OUTPUT_FILE)

# Hash hesapla
hash_receiver = hashlib.sha256(plaintext).hexdigest()
print("ALINAN VERININ SHA-256 HASH'I:", hash_receiver)

conn.close()
s.close()
