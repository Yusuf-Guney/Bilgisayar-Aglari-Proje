from scapy.all import IP

packet = IP(dst="8.8.8.8", ttl=64, flags="DF")

packet.show()
