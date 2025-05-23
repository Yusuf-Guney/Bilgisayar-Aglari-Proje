# Güvenli Dosya Transferi için Şifreleme Tabanlı Basit Ağ Uygulaması

Bu proje, Bilgisayar Ağları dersi dönem projesi kapsamında geliştirilmiştir. Amaç, TCP üzerinden dosya transferi sırasında veriyi AES şifreleme ile korumak, parçalama ve bütünlük kontrolü gibi ağ katmanı özelliklerini uygulamaktır.

## Özellikler
- **AES Şifreleme:** Verinin gizliliği için şifreleme.
- **Dosya Parçalama:** Büyük verileri küçük parçalara ayırarak gönderme.
- **SHA-256 Hash Kontrolü:** Veri bütünlüğünü doğrulama.
- **IP Başlığı Analizi:** Scapy kütüphanesi ile IP paketi incelemesi.

## Proje Yapısı
- `sender.py` — Dosya şifreleyip gönderen istemci uygulaması
- `receiver.py` — Gelen veriyi çözüp kaydeden sunucu uygulaması
- `scapy_test.py` — IP başlığı inceleme örneği
- `file.txt` — Gönderilecek örnek dosya

## Kullanım
1. İlk terminalde `receiver.py` dosyasını çalıştırın:
   ```bash
   python receiver.py
   ```
2. İkinci terminalde `sender.py` dosyasını çalıştırarak dosyayı gönderin:
   ```bash
   python sender.py
   ```
3. Transfer sonrası gönderilen ve alınan dosyanın SHA-256 hash değerlerini kontrol edebilirsiniz.

4. IP başlığı analizi için:
   ```bash
   python scapy_test.py
   ```

## Gereksinimler
- Python 3.x
- `pycryptodome` kütüphanesi
- `scapy` kütüphanesi

Kurulum:
```bash
pip install pycryptodome scapy
```
