from ma_boite.reseau import generer_ips

for ip in generer_ips("192.0.2.0/29"):
    print(ip)
