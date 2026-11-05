"""Drachen-Balancing MESSEN (W-17, 05.11.2026).

Frage: Wie viele Truppen braucht ein Spieler wirklich, um einen Drachen zu stellen - und was
kostet ein haerterer Feueratem (Recherche-Vorschlag 2)? Daniel will solche Aenderungen "erst nach
einer Balancing-Messung" entscheiden.

Gerechnet wird AUSSCHLIESSLICH mit den echten Kernfunktionen und Datendateien:
  data/drachen.json           Verteidiger je Drache, Schwellen (700/950 Schlagkraft), Feueratem 8 %
  data/units.json             Werte der Einheiten (ueber `einheiten.schlagkraft`)
  kampf.fuehre_schlacht       Vorrunde gegen die Schwellen, Nahkampf, Verluste
  drachen.feueratem_verluste  Ausfaelle VOR dem Kampf

WICHTIG (Lehre aus dem ersten Lauf): die Schwellen 700/950 gelten fuer SCHLAGKRAFT, nicht fuer
Kopfzahl. Ein Krieger hat Schlagkraft 3, ein Katapult 45 - also oeffnen rund 234 Krieger und genau
22 Katapulte die Schuppen. Ein Verdikt ueber Kopfzahlen waere falsch.

Jede Zelle ist reproduzierbar: fester Zufallskeim, feste Anzahl Laeufe. Es wird KEIN Code des
Spiels geaendert - das Werkzeug liest und rechnet nur.

Aufruf:  python -X utf8 tools/drachen_balancing.py
         python -X utf8 tools/drachen_balancing.py --laeufe 200
"""
from __future__ import annotations

import argparse
import datetime
import os
import random
import statistics
import sys

ROOT = os.environ.get("NEBEL_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import drachen  # noqa: E402  (Drachenwerte, Schwellen, Feueratem)
import einheiten  # noqa: E402  (echte Einheitennamen, Rollen, Schlagkraft)
import kampf  # noqa: E402  (die echte Schlacht)


def name_mit(anfang: str) -> str:
    """Den ECHTEN Einheitennamen aus den Daten holen (nie tippen)."""
    treffer = [n for n in einheiten.alle() if str(n).startswith(anfang)]
    return treffer[0] if treffer else ""


def kampf_probe(drache: dict, angreifer: dict, atem_prozent: float, saat: int,
                zweite_phase: dict = None) -> dict:
    """Einen Drachenkampf rechnen und die Kennzahlen zurueckgeben.

    Eingabe: Drachen-Eintrag, Truppen des Angreifers, Feueratem-Prozent, Zufallskeim.
    Ausgabe: dict mit ausgang, vorrunde, eigene (Verluste), fremde (Verluste beim Drachen), atem.
    """
    wachen = drachen.verteidiger(drache)                       # der Verteidiger des Drachen
    schwellen = drachen.schwellen(drache)                       # 700 Fusstruppen / 950 Belagerung
    fuss = sum(int(a) for n, a in angreifer.items()
               if einheiten.rolle(n) == "kaempfer")             # nur Kaempfer atmen lassen
    # Der Feueratem schlaegt VOR dem Kampf zu. Fuer die Gegenprobe mit einer anderen Quote wird
    # der Eintrag kopiert und der Prozentsatz darin ersetzt - das Spiel selbst bleibt unberuehrt.
    probe = {"verteidigung": dict(drache.get("verteidigung") or {})}
    probe["verteidigung"]["feueratem"] = dict(drachen.feueratem(drache) or {})
    probe["verteidigung"]["feueratem"]["prozent_der_fusstruppen"] = float(atem_prozent)
    atem = drachen.feueratem_verluste(probe, fuss)              # Ausfaelle durch den Atem
    truppen = dict(angreifer)                                   # Kopie, damit der Aufruf sauber bleibt
    rest = int(atem)                                            # was der Atem noch zu verteilen hat
    for n in sorted(truppen):                                   # Ausfaelle auf die Kaempfer legen
        if rest <= 0:
            break
        if einheiten.rolle(n) != "kaempfer":
            continue
        weg = min(rest, int(truppen[n]))
        truppen[n] = int(truppen[n]) - weg
        rest -= weg
    truppen = {n: a for n, a in truppen.items() if int(a) > 0}

    ergebnis = kampf.fuehre_schlacht(truppen, wachen, wall_stufe=0, wall_zustand=100.0,
                                     rng=random.Random(saat), schwellen=schwellen,
                                     zweite_phase=zweite_phase)
    eigene = sum(int(v) for v in (ergebnis.get("verluste_angreifer") or {}).values())
    fremde = sum(int(v) for v in (ergebnis.get("verluste_verteidiger") or {}).values())
    zp = ergebnis.get("zweite_phase") or {}
    return {"ausgang": str(ergebnis.get("ausgang") or ""),
            "vorrunde": bool(ergebnis.get("vorrunde_bestanden")),
            "eigene": eigene, "fremde": fremde, "atem": int(atem),
            "zp_aus": bool(zp.get("ausgeloest")), "zp_verluste": int(zp.get("verluste") or 0)}


def zeile(drache: dict, fuss: int, belagerung: int, atem_prozent: float, laeufe: int,
          fuss_name: str, geraet_name: str) -> dict:
    """Eine Zelle der Messmatrix: feste Truppenzahl, viele Laeufe, Kennzahlen daraus."""
    angreifer = {fuss_name: int(fuss)}                          # Fusstruppen
    if belagerung:
        angreifer[geraet_name] = int(belagerung)                # Belagerungswaffen
    siegege = 0
    verluste = []
    fremde = []
    for i in range(laeufe):                                     # jede Zelle mehrfach wuerfeln
        r = kampf_probe(drache, angreifer, atem_prozent, 1000 + i)
        siegege += 1 if r["ausgang"] == "angreifer" else 0
        verluste.append(r["eigene"])
        fremde.append(r["fremde"])
    return {"fuss": fuss, "belagerung": belagerung,
            "sk_fuss": int(einheiten.schlagkraft(fuss_name)) * int(fuss),
            "sk_bel": int(einheiten.schlagkraft(geraet_name)) * int(belagerung),
            "siege": siegege, "laeufe": laeufe,
            "quote": 100.0 * siegege / max(1, laeufe),
            "verluste": statistics.fmean(verluste) if verluste else 0.0,
            "fremde": statistics.fmean(fremde) if fremde else 0.0}


def main() -> int:
    """Die Messmatrix rechnen und als Markdown ausgeben."""
    t = argparse.ArgumentParser()
    t.add_argument("--laeufe", type=int, default=100)           # Laeufe je Zelle
    args = t.parse_args()

    drache = drachen.finde_id("drache_d02") or (drachen.alle() or [None])[0]
    if not drache:
        print("Kein Drache in den Daten.")
        return 1
    wachen = drachen.verteidiger(drache)
    schwellen = drachen.schwellen(drache)
    atem_daten = float((drachen.feueratem(drache) or {}).get("prozent_der_fusstruppen", 8))
    fuss_name = name_mit("Krieger")
    geraet_name = name_mit("Katapult")
    sk_fuss = int(einheiten.schlagkraft(fuss_name))
    sk_geraet = int(einheiten.schlagkraft(geraet_name))
    min_fuss = -(-int(schwellen[0]) // max(1, sk_fuss))          # aufrunden: noetige Krieger
    min_geraet = -(-int(schwellen[1]) // max(1, sk_geraet))      # aufrunden: noetige Katapulte

    print("# Drachen-Balancing (gemessen %s)" % datetime.date.today().isoformat())
    print("\nDrache: **%s** · Verteidiger %d Einheiten · Schwellen %s Schlagkraft · Feueratem %.0f %%"
          % (drache.get("name"), sum(int(v) for v in wachen.values()), schwellen, atem_daten))
    print("\nEinheiten: %s (Schlagkraft %d), %s (Schlagkraft %d) · Laeufe je Zelle: %d · "
          "fester Zufallskeim" % (fuss_name, sk_fuss, geraet_name, sk_geraet, args.laeufe))
    print("\n**Schwellen in Stueck gerechnet:** %d Schlagkraft = **%d %s**, %d Schlagkraft = "
          "**%d %s**." % (int(schwellen[0]), min_fuss, fuss_name, int(schwellen[1]),
                          min_geraet, geraet_name))
    print("\n| %s | SK Fuss | %s | SK Belagerung | Siege | Siegquote | eigene Verluste (Oe) | "
          "beim Drachen (Oe) |" % (fuss_name, geraet_name))
    print("|---|---|---|---|---|---|---|---|")

    ergebnisse = []
    for fuss in (200, 234, 300, 400, 500, 600, 700, 800, 1000):
        for bel in (11, 22, 33, 44):
            z = zeile(drache, fuss, bel, atem_daten, args.laeufe, fuss_name, geraet_name)
            ergebnisse.append(z)
            print("| %d | %d | %d | %d | %d/%d | %.0f %% | %.0f | %.0f |"
                  % (z["fuss"], z["sk_fuss"], z["belagerung"], z["sk_bel"], z["siege"],
                     z["laeufe"], z["quote"], z["verluste"], z["fremde"]))

    print("\n## Verdikt (maschinell, ohne Deutung)\n")
    unter_schwelle = [z for z in ergebnisse if z["sk_fuss"] < int(schwellen[0])
                      or z["sk_bel"] < int(schwellen[1])]
    gewinne_unten = [z for z in unter_schwelle if z["siege"] > 0]
    print("- Zellen UNTER einer der beiden Schwellen: %d. Davon mit Sieg: **%d**."
          % (len(unter_schwelle), len(gewinne_unten)))
    print("  (0 heisst: die Vorrunde haelt - unter der Schwelle wird nicht gekaempft, sondern "
          "zurueckgezogen.)")
    sicher = [z for z in ergebnisse if z["siege"] == z["laeufe"]]
    if sicher:
        beste = min(sicher, key=lambda z: (z["sk_fuss"] + 3 * z["sk_bel"], z["verluste"]))
        print("- **Sicherer Sieg ab**: %d %s (%d SK) und %d %s (%d SK), Siegquote 100 %%, "
              "Oe %.0f eigene Verluste von %d."
              % (beste["fuss"], fuss_name, beste["sk_fuss"], beste["belagerung"], geraet_name,
                 beste["sk_bel"], beste["verluste"], beste["fuss"]))
        print("- **Verlustquote** in dieser Zelle: %.0f %% der Truppe."
              % (100.0 * beste["verluste"] / max(1, beste["fuss"] + beste["belagerung"])))
    else:
        print("- **Keine Zelle** dieser Messung gewinnt in jedem Lauf.")

    print("\n## Gegenprobe: Feueratem mit 12 %% statt %.0f %% (Recherche-Vorschlag 2)\n" % atem_daten)
    print("| %s | %s | SK Fuss | Siege | Siegquote | eigene Verluste (Oe) | Atem-Ausfaelle |"
          % (fuss_name, geraet_name))
    print("|---|---|---|---|---|---|")
    for fuss in (234, 400, 700):
        z = zeile(drache, fuss, min_geraet, 12.0, args.laeufe, fuss_name, geraet_name)
        atem_verluste = drachen.feueratem_verluste(
            {"verteidigung": {"feueratem": {"prozent_der_fusstruppen": 12.0,
                                            "mindestens": 1, "hoechstens_anteil": 0.5}}}, fuss)
        print("| %d | %d | %d | %d/%d | %.0f %% | %.0f | %d |"
              % (fuss, min_geraet, z["sk_fuss"], z["siege"], z["laeufe"], z["quote"],
                 z["verluste"], atem_verluste))
    print("\nDie 12 % sind **keine** zweite Phase, sondern die Obergrenze: so viel kostet der Atem, "
          "wenn er im ganzen Gefecht haerter brennt. Eine echte zweite Phase (erst 8 %, unter 50 % "
          "Wache 12 %) liegt darunter und braucht eigenen Code.")
    # ------------------------------------------------- Frage 2: zweite Atemphase messen
    # Daniels Entscheidung (05.11.2026, Frage 2): "20 % unter halber Wache ansetzen - vorher
    # messen". Hier wird die Phase NICHT gebaut und nicht behauptet, sondern mit der echten
    # Schlacht (Parameter `zweite_phase`) gegen dieselben Zellen ohne Phase gerechnet.
    zp = {"atem_prozent": 20.0, "unter_anteil": 0.5}
    print("\n## Frage 2: zweite Atemphase - 20 % unter halber Wache\n")
    print("Gerechnet mit `kampf.fuehre_schlacht(..., zweite_phase=...)`, dieselben Keime und "
          "dieselbe Truppe wie ohne Phase - der Unterschied stammt also aus der Phase, nicht "
          "aus dem Zufall.\n")
    print("| %s | %s | SK Fuss | Siege ohne | Siege mit | eigene Verluste ohne | mit | "
          "Phase ausgeloest | Tote durch den 2. Atem |" % (fuss_name, geraet_name))
    print("|---|---|---|---|---|---|---|---|---|")
    unterschiede = []
    for fuss in (234, 300, 400, 700, 1000):
        angreifer = {fuss_name: int(fuss)}
        if min_geraet:
            angreifer[geraet_name] = int(min_geraet)
        ohne = [kampf_probe(drache, angreifer, atem_daten, 1000 + i) for i in range(args.laeufe)]
        mit = [kampf_probe(drache, angreifer, atem_daten, 1000 + i, zp) for i in range(args.laeufe)]
        s_ohne = sum(1 for r in ohne if r["ausgang"] == "angreifer")
        s_mit = sum(1 for r in mit if r["ausgang"] == "angreifer")
        v_ohne = statistics.fmean([r["eigene"] for r in ohne]) if ohne else 0.0
        v_mit = statistics.fmean([r["eigene"] for r in mit]) if mit else 0.0
        aus = sum(1 for r in mit if r["zp_aus"])
        tot2 = statistics.fmean([r["zp_verluste"] for r in mit]) if mit else 0.0
        unterschiede.append((fuss, v_mit - v_ohne, s_mit - s_ohne, aus))
        print("| %d | %d | %d | %d/%d | %d/%d | %.0f | %.0f | %d/%d | %.0f |"
              % (fuss, min_geraet, int(einheiten.schlagkraft(fuss_name)) * fuss, s_ohne,
                 args.laeufe, s_mit, args.laeufe, v_ohne, v_mit, aus, args.laeufe, tot2))
    if unterschiede:
        print("\n**Verdikt (maschinell):** der zweite Atem kostet zwischen **%+.0f** und **%+.0f** "
              "eigene Einheiten und aendert die Siegquote um **%+d** bis **%+d** von %d Laeufen. "
              "Ausgeloest in %d bis %d von %d Laeufen."
              % (min(u[1] for u in unterschiede), max(u[1] for u in unterschiede),
                 min(u[2] for u in unterschiede), max(u[2] for u in unterschiede), args.laeufe,
                 min(u[3] for u in unterschiede), max(u[3] for u in unterschiede), args.laeufe))
    return 0


if __name__ == "__main__":
    sys.exit(main())
