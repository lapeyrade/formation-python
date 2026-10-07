"""Interface de référence du TP 04 : erreurs prévues sans traceback."""

import json
import sys

from admin_tools.metier import analyser_logs, parseur_logs


def main():
    args = parseur_logs().parse_args()
    try:
        bilan = analyser_logs(args.source)
        args.sortie.mkdir(parents=True, exist_ok=True)
        (args.sortie / "compteurs.json").write_text(
            json.dumps(bilan, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        alertes = {ip: n for ip, n in bilan["compteurs"].items() if n >= args.seuil}
        (args.sortie / "alertes.json").write_text(json.dumps(alertes, indent=2), encoding="utf-8")
    except (OSError, UnicodeError) as erreur:
        print(f"Lecture/écriture impossible : {erreur}", file=sys.stderr)
        return 1
    print(f"{len(bilan['compteurs'])} IP, {len(alertes)} alertes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
