"""Rechnet die sechs Punkte der Rechenpflicht aus dem Opus-Pruefpaket am ECHTEN Code nach.

Zweck: Ein Modellurteil ist eine Behauptung, bis es nachgerechnet ist. Dieses Werkzeug druckt je Punkt
die Formel und die Zahl - die Zahlen kommen aus den Modulen (`forschung.dauer_stunden`,
`spielzeit.echtzeit_fuer_spielstunden`, `auftraege.SEKUNDEN_JE_FELD`, `punkte.kriegspunkte` usw.),
nicht aus dem Kopf. Aufruf:

    .venv\\Scripts\\python.exe -X utf8 tools\\opus_nachrechnen.py

Annahme, die das Werkzeug OFFEN nennt: die Dauern im Code sind SPIELZEIT-Sekunden (Handbuch), die
Spieluhr (`spielzeit.faktor()`, Standard 180) macht daraus Echtzeit. Wer das anders liest, muss die
Spalte "Echtzeit" anders rechnen - die Spalte "Spielzeit" bleibt davon unberuehrt.
"""
from __future__ import annotations

import itertools
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))

import auftraege            # noqa: E402
import forschung            # noqa: E402
import gebaeude_wirkung     # noqa: E402
import punkte               # noqa: E402
import spieloekonomie       # noqa: E402
import spielzeit            # noqa: E402


def _echt(spielsekunden: float) -> float:
    """Spielzeit-Sekunden -> Echtzeit-Sekunden bei der eingestellten Spieluhr."""
    return spielsekunden / spielzeit.faktor()


def main() -> int:
    faktor = spielzeit.faktor()
    print(f"Spieluhr (spielzeit.faktor()): {faktor}")
    print(f"1 Spielstunde in Echtzeit:     {_echt(3600):.2f} s")
    print()

    # 1. Forschung: Dauer bis Stufe n = n^2 Stunden (Originalregel in spieldaten).
    print("1. Forschung (dauer_stunden = Stufe^2 Stunden)")
    for stufe in (10, 20):
        stunden = forschung.dauer_stunden(stufe)
        spiel_s = stunden * 3600
        print(f"   Stufe {stufe:>2}: {stufe}^2 = {stunden} Spielstunden = {spiel_s} Spielsekunden"
              f" = {_echt(spiel_s):,.2f} s Echtzeit ({_echt(spiel_s) / 3600:,.2f} h)")
    print()

    # 2. Reise: SEKUNDEN_JE_FELD je Feld, bei Geschwindigkeit 1.
    print("2. Reise (reisezeit_sekunden = Felder / Geschwindigkeit * SEKUNDEN_JE_FELD)")
    je_feld = auftraege.SEKUNDEN_JE_FELD
    zehn = auftraege.reisezeit_sekunden(10, 1.0)
    print(f"   SEKUNDEN_JE_FELD = {je_feld}")
    print(f"   1 Feld (Geschw. 1):   {je_feld} Spielsekunden = {_echt(je_feld):,.2f} s Echtzeit")
    print(f"   10 Felder:            {zehn} Spielsekunden = {_echt(zehn):,.2f} s Echtzeit"
          f" ({_echt(zehn) / 60:,.2f} min)")
    print()

    # 3. Ausbildung: Grunddauer aus data/spieloekonomie.json.
    print("3. Ausbildung (REGELN['pilot_ausbildung_minuten'])")
    minuten = spieloekonomie.REGELN.get("pilot_ausbildung_minuten")
    grund = float(minuten or 0) * 60.0
    print(f"   pilot_ausbildung_minuten = {minuten} -> {grund} Spielsekunden"
          f" = {_echt(grund):,.2f} s Echtzeit")
    print()

    # 4. Siedlerzuwachs: 1 Siedler je Stunde je Siedlung (gebaeude_wirkung).
    print("4. Siedlerzuwachs (1 je Stunde je Siedlung, Heilkunde +10 Prozent je Stufe)")
    for anzahl in (1, 5):
        zuwachs = gebaeude_wirkung.siedler_zuwachs_pro_stunde([{} for _ in range(anzahl)])
        print(f"   {anzahl} Siedlung(en): {zuwachs} Siedler/Spielstunde"
              f" = 1 Siedler je {3600 / zuwachs:,.0f} Spielsekunden"
              f" = {_echt(3600 / zuwachs):,.2f} s Echtzeit")
    print()

    # 5. Punkte: Wallstufe 8 = 8^3, Gesamt = (Krieg + Forschung) // 2.
    print("5. Punkte (kriegspunkte = Wallstufe^3, gesamtpunkte = (Krieg + Forschung) // 2)")
    krieg = punkte.kriegspunkte({}, 8)
    print(f"   kriegspunkte({{}}, 8) = 8^3 = {krieg}")
    print(f"   Bei 0 Forschungspunkten: gesamt = ({krieg} + 0) // 2 = {punkte.gesamtpunkte({}, {}, 8)}")
    gebiete = forschung.gebiete()
    print(f"   Forschungsgebiete laut data: {len(gebiete)} ({', '.join(gebiete)})")
    # Kleinste Stufenkombination (je Gebiet hoechstens Stufe 8), die mit Wallstufe 8 ueber 300 kommt.
    # Nur die MULTIMENGE der Stufen zaehlt (Punkte = Summe der Stufen^3), deshalb reicht
    # combinations_with_replacement statt aller Verteilungen.
    ziel = punkte.ZIEL_PUNKTE_VERWORFEN
    treffer = None
    for anzahl in range(1, 8 * len(gebiete) + 1):
        for stufen in itertools.combinations_with_replacement(range(1, 9), anzahl):
            staende = dict(zip(gebiete, sorted(stufen, reverse=True)))
            gesamt = punkte.gesamtpunkte(staende, {}, 8)
            if gesamt > ziel:
                treffer = (stufen, gesamt, punkte.forschungspunkte(staende))
                break
        if treffer:
            break
    if treffer:
        verteilung, gesamt, fp = treffer
        print(f"   Kleinste Kombination mit Gesamtpunktzahl > {ziel}: Stufen {verteilung}"
              f" -> Forschungsstufen^3 = {fp}, gesamt = ({fp} + {krieg}) // 2 = {gesamt}")
    else:
        print(f"   Keine Kombination bis Stufe 8 je Gebiet erreicht mehr als {ziel}.")
    print(f"   Zum Vergleich: alle Gebiete Stufe 3 = {punkte.forschungspunkte(dict.fromkeys(gebiete, 3))},"
          f" gesamt = {punkte.gesamtpunkte(dict.fromkeys(gebiete, 3), {}, 8)}")
    print()

    # 6. Urteil je Zeile: die Zahl, die es traegt.
    print("6. Urteil (aus den Zahlen oben, nicht aus dem Gefuehl)")
    print(f"   Forschung Stufe 20 in Echtzeit: {_echt(forschung.dauer_stunden(20) * 3600) / 60:,.1f} min"
          f" - ein Spieler sieht die Stufe in einer Sitzung.")
    print(f"   10 Felder Reise: {_echt(auftraege.reisezeit_sekunden(10, 1.0)):,.1f} s Echtzeit"
          f" - Reisen ist billig, Auftraege sind keine Wartezeit.")
    print(f"   Ausbildung 1 Siedler: {_echt(grund):,.1f} s Echtzeit - praktisch sofort.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
