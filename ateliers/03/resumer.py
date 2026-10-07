from ma_boite.modeles import Machine
from ma_boite.reseau import generer_ips

for i, ip in enumerate(generer_ips("192.0.2.0/29"), 1):
    print(Machine(f"h{i}", ip).resume())
