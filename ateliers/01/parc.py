"""Instantané fictif du parc avant intervention ; aucun accès réseau."""

from typing import TypedDict


class MachineBrute(TypedDict):
    nom: str
    ip: str
    port: str
    actif: str
    charge: int
    services: list[str]


class MachineNormalisee(TypedDict):
    nom: str
    ip: str
    port: int
    actif: bool
    charge: int
    services: list[str]
    site: str


PARC: list[MachineBrute] = [
    {
        "nom": " SRV-PARIS-WEB-01 ",
        "ip": "192.0.2.1",
        "port": "22",
        "actif": "oui",
        "charge": 20,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-PARIS-DB-02 ",
        "ip": "192.0.2.2",
        "port": "22",
        "actif": "oui",
        "charge": 65,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-PARIS-WEB-03 ",
        "ip": "192.0.2.3",
        "port": "22",
        "actif": "non",
        "charge": 90,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-PARIS-DNS-04 ",
        "ip": "192.0.2.4",
        "port": "22",
        "actif": "oui",
        "charge": 10,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-PARIS-WEB-05 ",
        "ip": "192.0.2.5",
        "port": "22",
        "actif": "oui",
        "charge": 50,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-PARIS-DB-06 ",
        "ip": "192.0.2.6",
        "port": "22",
        "actif": "non",
        "charge": 79,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-LYON-WEB-07 ",
        "ip": "192.0.2.7",
        "port": "22",
        "actif": "oui",
        "charge": 80,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-LYON-DB-08 ",
        "ip": "192.0.2.8",
        "port": "22",
        "actif": "oui",
        "charge": 0,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-LYON-WEB-09 ",
        "ip": "192.0.2.9",
        "port": "22",
        "actif": "non",
        "charge": 90,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-LYON-DNS-10 ",
        "ip": "192.0.2.10",
        "port": "22",
        "actif": "oui",
        "charge": 85,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-LYON-WEB-11 ",
        "ip": "192.0.2.11",
        "port": "22",
        "actif": "oui",
        "charge": 30,
        "services": ["ssh"],
    },
    {
        "nom": " SRV-LYON-DB-12 ",
        "ip": "192.0.2.12",
        "port": "22",
        "actif": "oui",
        "charge": 95,
        "services": ["ssh"],
    },
]
