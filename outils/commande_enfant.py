"""Processus de test portable du TP 05."""

import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["succes", "echec", "attente"])
args = parser.parse_args()
if args.mode == "succes":
    print("machine disponible")
elif args.mode == "echec":
    print("diagnostic indisponible", file=sys.stderr)
    raise SystemExit(4)
else:
    time.sleep(2)
