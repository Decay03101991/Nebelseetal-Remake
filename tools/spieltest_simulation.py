"""Spieltest-Simulation: laesst das Remake OHNE Fenster spielen und protokolliert den Lauf.

Warum: Ein grosses Modell kann die tkinter-Oberflaeche nicht bedienen. Es kann aber sehr gut
BALANCE und SPIELGEFUEHL beurteilen, wenn es einen echten, nachvollziehbaren Spielverlauf sieht -
Rohstoffe ueber die Zeit, was ein Bau kostet, wann die erste Forschung fertig ist, wie ein Angriff
ausgeht, wie viele Punkte nach X Spieltagen dastehen. Genau das erzeugt dieses Werkzeug:
`docs/audits/SPIELTEST_LOG_<datum>.md`.

Es spielt mit einer einfachen, dokumentierten "Spielerpolitik" (kein Anspruch auf Optimalitaet):
  * alle 20 Spielminuten ein Schritt,
  * zuerst produzierende Gebaeude bauen, dann ausbauen,
  * Forschung starten, wenn bezahlbar,
  * Einheiten ausbilden, wenn Gold und Siedler da sind,
  * ab Spieltag 2 einmal angreifen.

Aufruf:
    python -X utf8 tools/spieltest_simulation.py            # 6 Spieltage
    python -X utf8 tools/spieltest_simulation.py --tage 10
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HIER, "src"))

import spielschicht as S            # noqa: E402
import einheiten as E               # noqa: E402
import gelaende as GE              # noqa: E402

SPIELTAG = 86400                    # Spielsekunden je Tag (Handbuch: 1 Tag = 24 Spielstunden)
SCHRITT = 1200                      # 20 Spielminuten je Schritt
GEBAEUDE_REIHENFOLGE = ("holzfäller", "farm", "steinmetz", "jaeger", "wohnhaus",
                        "bibliothek", "kaserne", "markt")


def _feld_fuer(siedlung: dict, gebaeude: str) -> int:
    """Erstes freies Feld, auf dem DIESES Gebaeude ueberhaupt stehen darf.

    Ohne diese Pruefung baut die Simulation auf das erstbeste Feld und die Farm landet im
    Wald - dann sieht der Lauf aus wie ein Spielfehler, obwohl nur die Politik dumm war.
    """
    belegt = set(int(k) for k in (siedlung.get("bauten") or {}))
    karte = siedlung.get("karte") or {}
    raster = karte.get("raster") or []
    for i, gel in enumerate(raster):
        if i in belegt:
            continue
        try:
            if GE.bau_moeglich(gebaeude, gel):
                return i
        except Exception:                      # noqa: BLE001
            continue
    return -1


def _freies_feld(siedlung: dict) -> int:
    """Erstes unbelegtes Feld der Siedlungskarte (Feldzaehlung kommt aus der Karte selbst)."""
    belegt = set(int(k) for k in (siedlung.get("bauten") or {}))
    karte = siedlung.get("karte") or {}
    anzahl = karte.get("bauplaetze") or karte.get("felder") or 0
    try:
        anzahl = int(anzahl)
    except (TypeError, ValueError):
        anzahl = 0
    for i in range(max(0, anzahl)):
        if i not in belegt:
            return i
    return -1


def _versuch(aktion, *args):
    """Fuehrt eine Spieleraktion aus und meldet (ok, text) - nie eine Ausnahme nach aussen."""
    try:
        return aktion(*args)
    except Exception as fehler:                     # noqa: BLE001
        return False, f"{type(fehler).__name__}: {fehler}"


def spielen(tage: float, saat: int = 7) -> dict:
    zustand = S.neuer_zustand(saat)
    jetzt = 0.0
    log = {"schritte": [], "ereignisse": [], "bauten": [], "forschungen": [],
           "ausbildung": [], "kaempfe": [], "_letzter_tag": -1}
    ziel_tag = tage * SPIELTAG
    angegriffen = False
    while jetzt < ziel_tag:
        jetzt += SCHRITT
        try:
            S.tick(zustand, jetzt, SCHRITT)
        except Exception as fehler:                 # noqa: BLE001
            log["ereignisse"].append(f"{jetzt / SPIELTAG:.2f} Takt-Fehler: {fehler}")
            break

        # Bauen (hoechstens ein Versuch je Schritt), sonst ausbauen.
        siedlung = (zustand.get("siedlungen") or [{}])[0]
        feld = _freies_feld(siedlung)
        gebaut = False
        vorhanden = {}
        for was in (siedlung.get("bauten") or {}).values():
            vorhanden[was] = vorhanden.get(was, 0) + 1
        if feld >= 0:
            for gebaeude in GEBAEUDE_REIHENFOLGE:
                # Ausgewogen bauen: je Gebaeude hoechstens 2, sonst baut die Politik nur
                # Holzfäller (und die Simulation zeigt ein verzerrtes Bild).
                if vorhanden.get(gebaeude, 0) >= 2:
                    continue
                feld_geb = _feld_fuer(siedlung, gebaeude)
                if feld_geb < 0:
                    continue
                ok, text = _versuch(S.bauen, zustand, 0, gebaeude, feld_geb)
                if ok:
                    log["bauten"].append((round(jetzt / SPIELTAG, 2), gebaeude))
                    gebaut = True
                    break
        if not gebaut and (siedlung.get("bauten") or {}):
            for feld_nr in sorted(int(k) for k in siedlung["bauten"]):
                ok, text = _versuch(S.ausbauen, zustand, 0, feld_nr)
                if ok:
                    log["bauten"].append((round(jetzt / SPIELTAG, 2), f"ausbau Feld {feld_nr}"))
                    break

        # Forschung
        for gebiet in ("Felderwirtschaft", "Kriegskunst", "Baukunst", "Verteidigungsanlagen"):
            stand = S.forschung_stand(zustand, jetzt)
            if stand.get("laeuft"):
                break
            ok, text = _versuch(S.forschung_starten, zustand, gebiet, jetzt)
            if ok:
                log["forschungen"].append((round(jetzt / SPIELTAG, 2), gebiet))
                break

        # Ausbildung
        for einheit in ("Kämpfer", "Bürgerwehr", "Handkarren"):
            ok, text = _versuch(S.ausbilden, zustand, einheit)
            if ok:
                log["ausbildung"].append((round(jetzt / SPIELTAG, 2), einheit))
                break

        # Ein Angriff ab Spieltag 2, wenn eigene Kaempfer da sind.
        if not angegriffen and jetzt >= 2 * SPIELTAG:
            krieger = {n: int(v) for n, v in (zustand.get("einheiten") or {}).items()
                       if int(v or 0) > 0 and E.rolle(n) in ("kaempfer", "kundschafter")}
            karren = {n: int(v) for n, v in (zustand.get("einheiten") or {}).items()
                      if int(v or 0) > 0 and E.rolle(n) == "karren"}
            if krieger and karren:
                ziel = {"name": "Bot-Siedlung", "wall_stufe": 1, "wall_zustand_prozent": 100.0,
                        "vorraete": {"holz": 400.0, "stein": 300.0, "nahrung": 250.0}}
                ok, ergebnis = _versuch(S.angriff, zustand, ziel, jetzt)
                log["kaempfe"].append({
                    "tag": round(jetzt / SPIELTAG, 2), "ok": ok,
                    "ausgang": (ergebnis or {}).get("ergebnis", {}).get("ausgang"),
                    "beute": (ergebnis or {}).get("beute"),
                    "vorrunde": (ergebnis or {}).get("bestanden"),
                    "truppen": dict(krieger, **karren)})
                angegriffen = True

        tag_rund = int(jetzt // SPIELTAG)
        if tag_rund > log["_letzter_tag"]:
            stand = S.punkte(zustand, jetzt)
            log["_letzter_tag"] = tag_rund
            log["schritte"].append({
                "tag": tag_rund, "ressourcen": dict(zustand.get("ressourcen") or {}),
                "punkte": stand.get("gesamtpunkte"), "krieg": stand.get("kriegspunkte"),
                "forschung": stand.get("forschungspunkte"),
                "einheiten": dict(zustand.get("einheiten") or {}),
                "bauten": len(siedlung.get("bauten") or {})})

    log["ende"] = {"tag": round(jetzt / SPIELTAG, 2),
                   "ressourcen": dict(zustand.get("ressourcen") or {}),
                   "punkte": S.punkte(zustand, jetzt),
                   "einheiten": dict(zustand.get("einheiten") or {})}
    return log


def bericht(log: dict, tage: float) -> str:
    z = []
    z.append(f"# Spieltest-Simulation — {tage:g} Spieltage, ohne Fenster gefahren")
    z.append("")
    z.append(f"**Erzeugt:** {datetime.datetime.now():%d.%m.%Y %H:%M} von `tools/spieltest_simulation.py` "
             "— reine Spiellogik (`src/spielschicht.py`), keine Oberflaeche.")
    z.append("**Spielerpolitik (dokumentiert, nicht optimal):** alle 20 Spielminuten ein Schritt; "
             "erst produzierende Gebaeude bauen, dann ausbauen; Forschung wenn bezahlbar; "
             "Einheiten ausbilden; ab Spieltag 2 ein Angriff auf Wallstufe 1.")
    z.append("")
    z.append("## Tagesbilanzen")
    z.append("")
    z.append("| Spieltag | Holz | Stein | Nahrung | Gold | Mana | Krieg | Forschung | Gesamt | Einheiten | Gebaeude |")
    z.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for s in log["schritte"]:
        r = s.get("ressourcen") or {}
        z.append(f"| {s['tag']} | {r.get('holz', 0):.0f} | {r.get('stein', 0):.0f} | "
                 f"{r.get('nahrung', 0):.0f} | {r.get('gold', 0):.0f} | {r.get('mana', 0):.0f} | "
                 f"{s.get('krieg')} | {s.get('forschung')} | **{s.get('punkte')}** | "
                 f"{sum(s.get('einheiten', {}).values())} | {s.get('bauten')} |")
    z.append("")
    z.append("## Gebaut (Spieltag, was)")
    z.append("")
    if log["bauten"]:
        z.append(", ".join(f"T{t} {was}" for t, was in log["bauten"][:40]))
    else:
        z.append("_nichts gebaut — entweder fehlten Rohstoffe oder alle Felder waren belegt._")
    z.append("")
    z.append("## Forschung")
    z.append("")
    z.append(", ".join(f"T{t} {was}" for t, was in log["forschungen"][:20]) or "_keine gestartet_")
    z.append("")
    z.append("## Ausbildung")
    z.append("")
    z.append(", ".join(f"T{t} {was}" for t, was in log["ausbildung"][:20]) or "_keine_")
    z.append("")
    z.append("## Kaempfe")
    z.append("")
    if log["kaempfe"]:
        for k in log["kaempfe"]:
            z.append(f"* Tag {k['tag']}: Truppen {k['truppen']} -> Ausgang **{k['ausgang']}**, "
                     f"Vorrunde bestanden: {k['vorrunde']}, Beute {k['beute']}")
    else:
        z.append("_kein Kampf zustande gekommen (keine Kaempfer oder keine Karren)._")
    z.append("")
    e = log["ende"]
    z.append("## Ende")
    z.append("")
    z.append(f"* Spieltag {e['tag']}")
    z.append(f"* Punkte: {e['punkte']}")
    z.append(f"* Einheiten: {e['einheiten'] or '{}'}")
    z.append(f"* Rohstoffe: {e['ressourcen']}")
    z.append("")
    z.append("## Was ein Pruefer daraus ablesen kann")
    z.append("")
    z.append("* **Tempo:** wie viele Spieltage bis zum ersten Gebaeude, zur ersten Forschung, "
             "zum ersten Kampf?")
    z.append("* **Engstelle:** welcher Rohstoff bremst (Tabelle oben)? ")
    z.append("* **Stillstand:** gibt es Tage ohne einen einzigen Bau? Warum?")
    z.append("* **Kampf:** Vorrunde bestanden? Beute in brauchbarer Hoehe? Truppenverlust?")
    z.append("* **Punkte:** wachsen sie plausibel (Krieg + Forschung)/2?")
    return "\n".join(z) + "\n"


def main() -> int:
    tage = 6.0
    if "--tage" in sys.argv:
        tage = float(sys.argv[sys.argv.index("--tage") + 1])
    saat = 7
    if "--saat" in sys.argv:
        saat = int(sys.argv[sys.argv.index("--saat") + 1])
    log = spielen(tage, saat)
    text = bericht(log, tage)
    ziel = os.path.join(HIER, "docs", "audits",
                        f"SPIELTEST_LOG_{datetime.datetime.now():%Y%m%d_%H%M}.md")
    with open(ziel, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(text)
    print(f"\nGESCHRIEBEN: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
