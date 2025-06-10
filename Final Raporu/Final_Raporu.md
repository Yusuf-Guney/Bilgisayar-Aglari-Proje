# Bilgisayar Ağları Dönem Projesi

**Proje Başlığı:** Güvenli Dosya Transferi için Şifreleme Tabanlı Ağ Uygulaması  
**Öğrenci:** Yusuf Güney - 22360859041  
**Tarih:** Haziran 2025  
**Üniversite:** Bursa Teknik Üniversitesi

---

## 1. Proje Amacı
Bu projede, istemci ile sunucu arasında gerçekleştirilen dosya transferinin güvenliğini ve doğruluğunu sağlamak için aşağıdaki teknolojilerle bir sistem geliştirilmiştir:

- AES şifreleme (EAX modu)
- RSA ile kimlik doğrulama
- SHA-256 ile bütünlük kontrolü
- Scapy ile manuel IP paketleme
- Wireshark ile paket analizi
- iPerf3 ile ağ performans ölçümü

---

## 2. Teknik Bileşenler

### 2.1 AES ile Şifreleme
- Gönderici taraf dosyayı AES-128 (EAX) moduyla şifreler.
- `nonce`, `tag` ve `ciphertext` birleştirilerek transfer edilir.
- Alıcı, aynı anahtar ile dosyayı çözer.

### 2.2 RSA ile Kimlik Doğrulama
- Alıcı kendi RSA key pair’ini oluşturur (private/public).
- Gönderici, alıcının public key’i ile challenge şifreleyip yollar.
- Alıcı, private key ile çözüm yapar. Başarılıysa aktarım başlar.

### 2.3 SHA-256 ile Bütünlük Kontrolü
- Gönderici, dosyanın hash'ini gönderim öncesi hesaplar.
- Alıcı, dosya alındıktan sonra yeniden hesaplar.
- Hash’ler karşılaştırılarak bütünlük sağlanır.

### 2.4 Scapy ile IP Fragmentation
- Şifrelenmiş veri UDP/IP üzerinden fragmanlara ayrılarak gönderilir.
- IP header alanları manuel olarak ayarlanır:
  - `id = 1234`, `ttl = 64`, `flags = MF`, `frag offset = i * FRAGMENT_SIZE`

### 2.5 Wireshark ile Trafik Analizi
- Paketler Wireshark ile yakalanır.
- UDP payload kısmı şifreli ve okunamaz yapıdadır.
- IP header üzerindeki alanlar incelenmiştir.

### 2.6 iPerf3 ile Performans Testi
- `iperf3 -s` ve `iperf3 -c 127.0.0.1` ile bant genişliği ölçümü yapılır.
- Ortalama hız: ~945 Mbit/s

---

## 3. Kullanılan Araçlar ve Teknolojiler

| Araç/Kütüphane | Açıklama |
|----------------|----------|
| Python         | Ana programlama dili |
| PyCryptodome   | AES ve RSA işlemleri için |
| Scapy          | Düşük seviye ağ paketi oluşturma |
| Wireshark      | Paket analizi ve görsel denetim |
| iPerf3         | Ağ bant genişliği testi |

---

## 4. Sonuç ve Değerlendirme
Bu proje, hem uygulamalı ağ programlaması hem de güvenlik konseptleri açısından güçlü bir pratik sunmuştur. 
RSA ve AES kombinasyonu ile güvenli bir aktarım başarıyla sağlanmış, Scapy ile düşük seviye IP işlemleri uygulanmış ve Wireshark ile görsel analiz gerçekleştirilmiştir.

Proje kapsamında elde edilen çıktılar teorik bilginin pratiğe dönüşmesini sağlamıştır.

---

## 5. Ek Dosyalar ve Bağlantılar

- [YouTube Tanıtım Videosu](https://www.youtube.com/watch?v=3GeCIZ7Rs-U) *(video linkini buraya ekle)*
- [Linkedin Proje Tanıtımı](https://www.linkedin.com/posts/yusuf-guney_proje-raporu-activity-7338256885969489921-hpGH?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD50XoABVLRC2PZXh1B23ruv5sLKrWW8_FM)

---

## 6. Ekran Görüntüleri

Ekran görüntüleri aşağıdaki klasöre eklenmiştir: `./gorseller/`

| Şekil | Açıklama |
|-------|----------|
| 8     | RSA anahtar üretimi kod çıktısı |
| 9     | receiver.py dosyasında RSA doğrulama kodu |
| 10    | sender_scapy.py fragment gönderimi ekranı |
| 11    | receiver_scapy.py birleşim çıktısı |
| 12    | Wireshark - IP fragment paketi görünümü |
| 13    | Wireshark - UDP Payload şifreli veri |
| 14    | iPerf istemci çıktısı |
| 15    | iPerf bant genişliği tablosu |

---

## 7. Kaynaklar

- PyCryptodome: https://www.pycryptodome.org
- Scapy Docs: https://scapy.readthedocs.io
- Wireshark Guide: https://www.wireshark.org/docs
- iPerf3: https://iperf.fr
- Kurose & Ross, Computer Networking
- Tanenbaum, Computer Networks
