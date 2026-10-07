"""Contrôle en lecture seule, transféré et exécuté sur chaque cible par Ansible."""

import json
import platform

print(json.dumps({"hostname": platform.node(), "systeme": platform.system()}))
