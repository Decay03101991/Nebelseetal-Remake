# -*- coding: utf-8 -*-
"""Messwerkzeug Wirtschaft (B1, 01.11.2026).

Rechnet Kennzahlen der Spielwirtschaft AUSSCHLIESSLICH aus Projektdaten und
Kernfunktionen. Aufruf:  python -X utf8 tools/mess_wirtschaft.py
Jede Kennzahl wird als EINE Zeile gedruckt:  Kennzahl | Wert | Quelle.
Reines ASCII; kein Umlaut im Code. Ende mit Rueckgabewert 0.
"""
from __future__ import annotations  # moderne Typ-Annotationen erlauben

import os  # Dateipfade aufloesen
import sys  # Modulpfad und Rueckgabewert

from collections import Counter  # Ertraege je Rohstoff aufaddieren

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektwurzel bestimmen
sys.path.insert(0, os.path.join(HIER, "src"))  # src-Module importierbar machen
sys.path.insert(0, HIER)  # Projektwurzel importierbar machen

import auftraege  # Reisekosten und Reisezeiten (Gold/Nahrung/Mana)
import forschung  # Forschungskosten (fuer die Gruendungsrechnung)
import forschung_wirkung  # belegte Produktionsfaktoren (Goetterkunde usw.)
import gebaeude_wirkung  # Siedlergrenze, Zuwachs, Bevoelkerungsgrenze
import gelaende  # Gebaeude-, Gelaende- und Ertragsdaten
import spieloekonomie  # Rechenstellen: Nahrung, Ausbildung, Gruendung
import werkstatt  # Warendauern und Warteschlangen
import wirtschaft  # ertrag_gesamt (Kernrechnung je Ort)

GEBAEUDE = gelaende.alle_gebaeude()  # {Kennung: Eintrag} aus data/buildings.json
U = spieloekonomie.U  # Einheiten aus data/units.json (je Einheit ein Eintrag)
WARENREZEPTE = spieloekonomie.WARENREZEPTE  # Rezeptdaten je Ware (Dauer, Kosten)
REGELN = spieloekonomie.REGELN  # Regeldaten aus data/spieloekonomie.json
ROHSTOFF = "rohstoff"  # Feldname des Einzelrohstoffs im Gebaeudeeintrag

# Handbuch 2009, Seite 10/11: Ertrag je Gebaeude und Gelaende (ASCII, gegen data/ pruefen).
HANDBUCH = {  # Vergleichstafel des Handbuchs als Datensatz
    "holzfaeller": {"wald": {"Holz": 4.0}, "steppe": {"Holz": 2.0}},  # Holzfaeller
    "steinmetz": {"berg": {"Stein": 4.0}, "huegel": {"Stein": 2.0}},  # Steinmetz
    "erzmine": {"berg": {"Metall": 3.0}, "huegel": {"Metall": 1.5}},  # Erzmine
    "tempel": {"nebelsee": {"Mana": 5.0}, "sonst": {"Mana": 1.0}},  # Tempel
    "farm": {"grasland": {"Nahrung": 4.0}, "steppe": {"Nahrung": 2.0}},  # Farm
    "goldmine": {"berg": {"Gold": 3.0}, "huegel": {"Gold": 1.5}},  # Goldmine
    "schafszucht": {"grasland": {"Wolle": 3.0}, "steppe": {"Wolle": 1.5}},  # Schafszucht
    "rinderfarm": {"grasland": {"Nahrung": 3.0, "Leder": 3.0},  # Rinderfarm Grasland
                   "steppe": {"Nahrung": 1.5, "Leder": 1.5}},  # Rinderfarm Steppe
    "pferdezucht": {"grasland": {"Pferde": 3.0}, "steppe": {"Pferde": 1.5}},  # Pferdezucht
    "jaeger": {"wald": {"Nahrung": 2.0, "Leder": 2.0},  # Jaeger Wald
               "steppe": {"Nahrung": 1.0, "Leder": 1.0}},  # Jaeger Steppe
}

# Beispielprogramm (ANNAHME): ein 10x10-Dorf, alle 90 bebaubaren Felder belegt.
# Gelaendeverteilung aus data/gelaende.json (Gewichte): 20 Grasland, 20 Steppe, 18 Wald,
# 13 Huegel, 12 Berg, 7 Nebelsee, 10 Sumpf (unbebaubar). Anzahl je Produktionsgebaeude:
PROGRAMM = {  # Anzahl je Dorf (zusammen 89 Produktionsgebaeude + 1 Bibliothek = 90 Felder)
    "holzfaeller": 9,  # 9 Holzaeller auf Wald
    "jaeger": 9,  # 9 Jaeger auf Wald
    "steinmetz": 9,  # 9 Steinmetze (Berg und Huegel)
    "erzmine": 8,  # 8 Erzminen (Berg und Huegel)
    "goldmine": 8,  # 8 Goldminen (Berg und Huegel)
    "farm": 10,  # 10 Farmen (Grasland und Steppe)
    "schafszucht": 10,  # 10 Schafszuchten
    "rinderfarm": 10,  # 10 Rinderfarmen
    "pferdezucht": 10,  # 10 Pferdezuchten
    "tempel": 6,  # 6 Tempel auf Nebelsee (1 Feld bleibt fuer die Bibliothek)
}

# Mischbelegung (ANNAHME): welches Produktionsgebaeude auf welchem Gelaende steht.
MIX = {  # {Gebaeude: {Gelaende: Anzahl}} - die nachvollziehbare Beispielverteilung
    "holzfaeller": {"wald": 9},  # Holzfaeller nur auf Wald (bestes Gelaende)
    "jaeger": {"wald": 9},  # Jaeger nur auf Wald
    "steinmetz": {"berg": 4, "huegel": 5},  # Steinmetz: 4 Berg, 5 Huegel
    "erzmine": {"berg": 4, "huegel": 4},  # Erzmine: 4 Berg, 4 Huegel
    "goldmine": {"berg": 4, "huegel": 4},  # Goldmine: 4 Berg, 4 Huegel
    "farm": {"grasland": 5, "steppe": 5},  # Farm: 5 Grasland, 5 Steppe
    "schafszucht": {"grasland": 5, "steppe": 5},  # Schafszucht je 5
    "rinderfarm": {"grasland": 5, "steppe": 5},  # Rinderfarm je 5
    "pferdezucht": {"grasland": 5, "steppe": 5},  # Pferdezucht je 5
    "tempel": {"nebelsee": 6},  # Tempel nur auf Nebelsee
}


def fmt(x):  # eine Zahl lesbar formatieren (ganze Zahlen ohne Nachkommastellen)
    if isinstance(x, float) and x.is_integer():  # ganzzahliger Float?
        return str(int(x))  # als ganze Zahl zeigen
    return ("%.2f" % x).rstrip("0").rstrip(".")  # zwei Stellen, ueberfluessige Nullen weg


def ascii_s(s):  # Daten-Namen ohne Umlaut drucken (ae/oe/ue/ss), damit die Ausgabe rein ASCII bleibt
    return (str(s).replace("\u00e4", "ae").replace("\u00f6", "oe")  # ae und oe ersetzen
            .replace("\u00fc", "ue").replace("\u00df", "ss"))  # ue und ss ersetzen


def zeile(kennzahl, wert, quelle):  # eine Kennzahl in der Pflichtform drucken
    print("%s | %s | %s" % (kennzahl, wert, quelle))  # Kennzahl | Wert | Quelle


def rate_dict(geb_id, terrain):  # Ertrag eines Gebaeudes auf einem Gelaende als {Rohstoff: Menge}
    geb = GEBAEUDE.get(geb_id) or {}  # Gebaeudeeintrag holen (leer, wenn unbekannt)
    ertrag = gelaende.ertrag_pro_stunde(geb_id, terrain)  # Zahl, Dict oder None
    if ertrag is None:  # kein Ertrag auf diesem Gelaende?
        return {}  # leeres Ergebnis
    if isinstance(ertrag, dict):  # mehrere Rohstoffe (Jaeger, Rinderfarm)?
        return {str(k): float(v) for k, v in ertrag.items()}  # alle Eintraege uebernehmen
    roh = geb.get(ROHSTOFF)  # der einzelne Rohstoff (z. B. "Holz")
    return {str(roh): float(ertrag)} if isinstance(roh, str) else {}  # {Rohstoff: Menge}


def best_worst(geb_id):  # (beste Rate, schlechteste Rate) eines Gebaeudes ueber alle Gelaende
    beste = {}  # bisher beste Rate (nach Summe)
    schlechteste = {}  # bisher schlechteste Rate
    for art in gelaende.GELAENDEARTEN:  # alle Gelaendearten durchgehen
        if not gelaende.ist_bebaubar(art):  # Sumpf ueberspringen (nicht bebaubar)
            continue  # naechstes Gelaende
        r = rate_dict(geb_id, art)  # Ertrag auf diesem Gelaende
        if not r:  # kein Ertrag?
            continue  # naechstes Gelaende
        if not beste or sum(r.values()) > sum(beste.values()):  # besser als bisher?
            beste = r  # als neue beste Rate merken
        if not schlechteste or sum(r.values()) < sum(schlechteste.values()):  # schlechter?
            schlechteste = r  # als neue schlechteste Rate merken
    return beste, schlechteste  # beide Raten zurueckgeben


def ertrag_text(d):  # ein Ertrags-Dict kompakt als Text ("Holz 36, Stein 26")
    return ", ".join("%s %s" % (k, fmt(v)) for k, v in sorted(d.items()))  # sortiert ausgeben


def fall_ertrag(fall):  # Reichsertrag des besten bzw. schlechtesten Falls je Stunde
    out = Counter()  # Summe je Rohstoff
    for geb_id, anzahl in PROGRAMM.items():  # jedes Produktionsgebaeude
        beste, schlechteste = best_worst(geb_id)  # beide Raten des Gebaeudes
        r = beste if fall == "best" else schlechteste  # die gewuenschte Rate waehlen
        for roh, menge in r.items():  # je Rohstoff
            out[roh] += menge * anzahl  # Rate mal Anzahl addieren
    return dict(out)  # als normales Dict zurueckgeben


def misch_ertrag():  # Ertrag der Mischbelegung (Beispiel) je Stunde
    out = Counter()  # Summe je Rohstoff
    for geb_id, zuweisung in MIX.items():  # jedes Gebaeude der Beispielbelegung
        for terrain, anzahl in zuweisung.items():  # je belegtem Gelaende
            r = rate_dict(geb_id, terrain)  # Ertrag dort
            for roh, menge in r.items():  # je Rohstoff
                out[roh] += menge * anzahl  # Menge mal Anzahl addieren
    return dict(out)  # als normales Dict zurueckgeben


def dorf(haeuser):  # ein Dorf-Dict mit `haeuser` Haeusern (fuer die Siedlerrechnung)
    bauten = {"0": "lager"}  # Feld 0 traegt das Dorfzentrum (Kennung lager)
    stufen = {}  # Ausbaustufen je Feld
    for i in range(haeuser):  # je Haus ein Feld belegen
        feld = str(i + 1)  # Feldkennung ab 1
        bauten[feld] = "haus"  # dieses Feld traegt ein Haus
        stufen[feld] = 1  # Haus der Stufe 1 (belegt)
    return {"bauten": bauten, "stufen": stufen}  # Dorf als Dict zurueckgeben


def ort_mit_akademie(stufe):  # ein Dorf-Dict mit Kriegerakademie (fuer die Ausbildungsdauer)
    return {"vorraete": {}, "waren": {}, "bevoelkerung": 100.0,  # leere Lager, viele Siedler
            "einheiten": {}, "ausbildung": [],  # keine Einheiten, keine Auftraege
            "bauten": {"0": "kriegerakademie"}, "stufen": {"0": stufe}}  # Akademie der Stufe


def main():  # alle Kennzahlen rechnen und drucken
    print("# Messwirtschaft Nebelseetal Remake (B1, 01.11.2026)")  # Kopfzeile

    # ------------------------------------------------------- 1. Ertraege je Gebaeude
    print("\n## 1. Ertraege je Gebaeude und Gelaende")  # Abschnitt 1
    for geb_id in sorted(GEBAEUDE):  # alle 20 Gebaeude, alphabetisch
        geb = GEBAEUDE[geb_id]  # Eintrag des Gebaeudes
        tabelle = geb.get("ertrag_pro_stunde")  # Ertragstafel (None bei Nicht-Produzenten)
        if not tabelle:  # kein Ertrag belegt (Werkstatt, Ausbildung, Wall, Haus, ...)?
            zeile("Ertrag_%s" % geb_id, "kein Ertrag", "data/buildings.json")  # nennen
            continue  # naechstes Gebaeude
        for name, wert in tabelle.items():  # je Gelaende-Eintrag der Tafel
            tid = "sonst" if name.startswith("alle") else gelaende.NACH_NAME.get(name, name)  # ASCII-Kennung
            if isinstance(wert, dict):  # mehrere Rohstoffe?
                text = ", ".join("%s %s" % (k, fmt(v)) for k, v in wert.items())  # einzeln
            else:  # ein Rohstoff
                text = "%s %s" % (geb.get(ROHSTOFF), fmt(wert))  # Rohstoff und Menge
            zeile("Ertrag_%s_%s" % (geb_id, tid), text, "data/buildings.json:ertrag_pro_stunde")  # drucken

    print("\n## 1b. Handbuchabgleich (2009, Seite 10/11)")  # Vergleichsblock
    for geb_id in sorted(HANDBUCH):  # nur die neun Produktionsgebaeude mit Handbuchwert
        hb = HANDBUCH[geb_id]  # Handbuchtafel des Gebaeudes
        daten = {}  # Datenwert je Gelaende (ASCII)
        tabelle = GEBAEUDE[geb_id].get("ertrag_pro_stunde") or {}  # Datentafel
        for name, wert in tabelle.items():  # je Gelaende-Eintrag
            tid = "sonst" if name.startswith("alle") else gelaende.NACH_NAME.get(name, name)  # ASCII
            if isinstance(wert, dict):  # mehrere Rohstoffe
                daten[tid] = {str(k): float(v) for k, v in wert.items()}  # uebernehmen
            else:  # ein Rohstoff
                daten[tid] = {str(GEBAEUDE[geb_id].get(ROHSTOFF)): float(wert)}  # uebernehmen
        gleich = daten == hb  # stimmen Daten und Handbuch ueberein?
        urteil = "BELEGT" if gleich else "WIDERSPRUCH"  # Urteil vergeben
        zeile("Handbuch_%s" % geb_id, urteil, "Handbuch2009:S.10/11")  # Urteil drucken
    # Der WIDERSPRUCH der Rinderfarm wird einzeln belegt (Handbuch 3/3 gegen Daten 1/3).
    zeile("Handbuch_rinderfarm_Detail", "Handbuch Grasland Nahrung 3 Leder 3, Steppe 1.5/1.5; Daten Grasland Nahrung 1 Leder 3, Steppe 0.5/1.5", "Handbuch2009:S.10/11 vs data/buildings.json")  # Detail

    # ---------------------------------------------- 2. Reichsertrag (drei Faelle)
    print("\n## 2. Reichsertrag je Spielstunde und Spieltag")  # Abschnitt 2
    for geb_id, anzahl in sorted(PROGRAMM.items()):  # das angenommene Beispielprogramm
        zeile("Programm_%s" % geb_id, str(anzahl), "ANNAHME: 10x10-Dorf, 90 Felder belegt")  # je Gebaeude
    misch = misch_ertrag()  # Beispielertrag je Stunde
    bester = fall_ertrag("best")  # bester Fall je Stunde
    schlechtester = fall_ertrag("worst")  # schlechtester Fall je Stunde
    for titel, ertrag in (("Beispiel", misch), ("Bester_Fall", bester), ("Schlechtester_Fall", schlechtester)):  # drei Faelle
        zeile("Dorf_%s_je_Stunde" % titel, ertrag_text(ertrag), "Rechnung aus data/buildings.json + data/gelaende.json")  # je Dorf/h
        reich = {k: v * 6 for k, v in ertrag.items()}  # sechs Doerfer
        zeile("Reich_%s_je_Stunde" % titel, ertrag_text(reich), "6 Doerfer (sechs Doerfer)")  # Reich/h
        zeile("Reich_%s_je_Tag" % titel, ertrag_text({k: v * 24 for k, v in reich.items()}), "24 Spielstunden je Spieltag")  # Reich/Tag

    # -------------------------------------------------------------- 3. Siedler
    print("\n## 3. Siedlerzuwachs und Siedlerdecke")  # Abschnitt 3
    sechs_leer = [dorf(0) for _ in range(6)]  # sechs Doerfer ohne Haeuser
    sechs_voll = [dorf(10) for _ in range(6)]  # sechs Doerfer mit je 10 Haeusern
    zeile("Zuwachs_je_Stunde_Reich", fmt(gebaeude_wirkung.siedler_zuwachs_pro_stunde(sechs_leer)), "src/gebaeude_wirkung.py:siedler_zuwachs_pro_stunde")  # Zuwachs
    zeile("Zuwachs_je_Stunde_Reich_Heilkunde10", fmt(gebaeude_wirkung.siedler_zuwachs_pro_stunde(sechs_leer, {"heilkunde": 10})), "heilkunde (Kleinbuchstabe, so liest gebaeude_wirkung.py:180)")  # mit Heilkunde
    zeile("Befund_Heilkunde_Schluessel", "gebaeude_wirkung.py liest 'heilkunde', die Forschung heisst 'Heilkunde' - Bonus greift im Spiel nicht", "src/gebaeude_wirkung.py:180 vs data/research.json")  # Befund Schluessel
    zeile("Grenze_je_Dorf_ohne_Haus", str(gebaeude_wirkung.siedlergrenze_je_siedlung(dorf(0))), "src/gebaeude_wirkung.py:siedlergrenze_je_siedlung")  # Grundgrenze
    zeile("Grenze_je_Dorf_10_Haeuser", str(gebaeude_wirkung.siedlergrenze_je_siedlung(dorf(10))), "10 + 5 je Haus")  # mit Haeusern
    zeile("Reichsdeckel_ohne_Haus", str(gebaeude_wirkung.bevoelkerungsgrenze(sechs_leer)), "src/gebaeude_wirkung.py:bevoelkerungsgrenze")  # Deckel
    zeile("Reichsdeckel_10_Haeuser_je_Dorf", str(gebaeude_wirkung.bevoelkerungsgrenze(sechs_voll)), "6 Doerfer x (10 + 5x10)")  # voller Deckel
    zeile("Zeit_bis_volle_Siedlung_Stunden", fmt((60 - 10) / 1.0), "Start 10 -> Grenze 60, 1 Siedler/h")  # Zeit bis voll

    # ------------------------------------------------------------ 4. Goldfluss
    print("\n## 4. Goldfluss je Spieltag")  # Abschnitt 4
    zeile("Goldmine_Berg_je_Stunde", "3", "data/buildings.json:goldmine.ertrag_pro_stunde")  # Gold Berg
    zeile("Goldmine_Huegel_je_Stunde", "1.5", "data/buildings.json:goldmine.ertrag_pro_stunde")  # Gold Huegel
    gold_misch_tag = misch.get("Gold", 0.0) * 6 * 24  # Beispiel Gold je Reich und Tag
    zeile("Gold_Einnahme_Reich_je_Tag", fmt(gold_misch_tag), "Beispielprogramm, 8 Goldminen je Dorf, 6 Doerfer")  # Einnahme
    # Abfluss Gold: Einheitenkosten sind BELEGT, Reisekosten sind VORSCHLAG, Baukosten fehlen.
    krieger_gold = U["Krieger"]["kosten"].get("gold", 0)  # Gold je Krieger (belegt)
    zeile("Gold_Abfluss_Einheit_Krieger", fmt(krieger_gold), "data/units.json:Krieger.kosten.gold")  # Einheitenkosten
    zeile("Gold_Abfluss_Baukosten", "nicht vorhanden", "data/baupreise.json: kein Goldposten")  # Baukosten
    zeile("Gold_Abfluss_Reisekosten", "nicht belegt", "src/auftraege.py:GOLD_JE_FELD_JE_GS=0.1 (VORSCHLAG)")  # Reisekosten

    # ------------------------------------------------------------------ 5. Mana
    print("\n## 5. Mana je Spielstunde")  # Abschnitt 5
    mana_name = forschung_wirkung.belegte_faktoren()["mana"]["forschung"]  # belegter Forschungsname (Goetterkunde)
    zeile("Tempel_Nebelsee_je_Stunde", "5", "data/buildings.json:tempel.ertrag_pro_stunde")  # Nebelsee
    zeile("Tempel_sonst_je_Stunde", "1", "data/buildings.json:tempel (alle ausser Sumpf)")  # sonst
    zeile("Tempel_Sumpf_je_Stunde", "0", "Sumpf unbebaubar (Handbuch S. 11)")  # Sumpf
    for stufe in (1, 5, 10):  # Goetterkunde-Stufen durchrechnen
        faktor = forschung_wirkung.faktor({mana_name: stufe}, "mana")  # Faktor je Stufe
        zeile("Tempel_Nebelsee_Goetterkunde%d" % stufe, fmt(5.0 * faktor), "%s +5 %% je Stufe" % ascii_s(mana_name))  # mit Bonus

    # --------------------------------------------------------------- 6. Nahrung
    print("\n## 6. Nahrungsverbrauch")  # Abschnitt 6
    zeile("Verbrauch_je_Einheit_je_Tag", "8", "data/nahrungsverbrauch.json:je_einheit_pro_tag")  # je Tag
    bedarf_100 = spieloekonomie.tagesbedarf_nahrung({"Krieger": 100})  # 100 Einheiten
    bedarf_360 = spieloekonomie.tagesbedarf_nahrung({"Krieger": 360})  # 360 Einheiten
    zeile("Bedarf_100_Einheiten_je_Tag", fmt(bedarf_100), "src/spieloekonomie.py:tagesbedarf_nahrung")  # 100
    zeile("Bedarf_360_Einheiten_je_Tag", fmt(bedarf_360), "src/spieloekonomie.py:tagesbedarf_nahrung")  # 360
    zeile("Bedarf_100_Einheiten_je_Stunde", fmt(bedarf_100 / 24.0), "src/spieloekonomie.py:verbrauch_pro_stunde (geteilt durch 24)")  # je Stunde
    # Reisekosten je Feld (Richtung belegt, Hoehe VORSCHLAG).
    zeile("Reisekosten_Nahrung_je_Feld", "0.1 je Einheit je Feld geteilt durch GS", "src/auftraege.py:NAHRUNG_JE_FELD_DURCH_GS (VORSCHLAG)")  # je Feld
    gs_krieger = U["Krieger"]["werte"].get("GS", 25)  # Geschwindigkeit des Kriegers
    kosten10 = auftraege.kosten_der_mission({"Krieger": 40}, 10, gs_krieger, 0, 0, fremdes_ziel=True)  # Beispiel 10 Felder
    zeile("Reisekosten_Beispiel_40Krieger_10Felder", "Gold %s, Nahrung %s, Mana %s" % (fmt(kosten10["gold"]), fmt(kosten10["nahrung"]), fmt(kosten10["mana"])), "src/auftraege.py:kosten_der_mission")  # Beispiel

    # ----------------------------------------------------------------- 7. Dauern
    print("\n## 7. Waren- und Ausbildungsdauern")  # Abschnitt 7
    for ware in sorted(WARENREZEPTE):  # jede Ware aus den Rezeptdaten
        dauer = WARENREZEPTE[ware].get("dauer")  # Dauer in Sekunden
        belegt = "belegt" if werkstatt.dauer_belegt(ware) else "VORSCHLAG"  # Schwert ist belegt
        zeile("Warendauer_%s" % ascii_s(ware), "%s s = %s min" % (fmt(dauer), fmt(float(dauer) / 60.0)), "data/warenrezepte.json:dauer (%s)" % belegt)  # Dauer je Ware
    for stufe in (1, 2, 3, 4, 5):  # Ausbildungsdauer je Stufe
        dauer = spieloekonomie.ausbildung_grenzen(ort_mit_akademie(stufe), "Krieger", {"Kriegskunst": 3})["dauer_je"]  # echte Rechenstelle
        zeile("Ausbildungsdauer_Stufe_%d" % stufe, "%s s = %s min" % (fmt(dauer), fmt(float(dauer) / 60.0)), "src/spieloekonomie.py:ausbildung_start (Grunddauer / Stufe)")  # Dauer je Stufe
    # Warteschlangen-Effekt: Handbuchbeispiel 10 Schwerter a 20 min, 1 oder 2 Schmieden.
    for anzahl_ws in (1, 2):  # eine und zwei Schmieden
        schlange = werkstatt.neue_warteschlange("schmiede", anzahl_ws)  # leere Schlange
        werkstatt.einreihen(schlange, "Schwert", 10, 1, WARENREZEPTE)  # 10 Schwerter einreihen
        rest = werkstatt.fortschritt(schlange, 0.0)["rest_sekunden"]  # Restzeit des Stapels
        zeile("Warteschlange_10Schwerter_%dSchmiede_min" % anzahl_ws, fmt(float(rest) / 60.0), "Handbuch S. 13 Beispiel; src/werkstatt.py")  # Effekt drucken

    # --------------------------------------------------- 8. Verhaeltniskennzahlen
    print("\n## 8. Verhaeltniskennzahlen")  # Abschnitt 8
    reich_misch = {k: v * 6 for k, v in misch.items()}  # Reichsertrag Beispiel je Stunde
    summe_h = sum(reich_misch.values())  # Summe aller Rohstoffe je Stunde
    zeile("Ertrag_je_Siedler_360", fmt(summe_h / 360.0), "Reichsertrag (Summe) / Siedlerdeckel 360")  # je Siedler (voll)
    zeile("Ertrag_je_Siedler_60", fmt(summe_h / 60.0), "Reichsertrag (Summe) / Grunddeckel 60")  # je Siedler (Grund)
    zeile("Siedler_je_Gebaeude", fmt(360.0 / (90.0 * 6)), "360 Siedler / (90 Gebaeude x 6 Doerfer)")  # je Gebaeude
    # Zeit bis zur ersten Siedlung: Gruendungsbedarf geteilt durch Dorf-Tagesertrag (engster Rohstoff).
    preis, paket, minimum = spieloekonomie.gruendungskosten()  # Gruendungsgebuehr, Paket, Mindestbestand
    karren = {k: float(v) for k, v in U["Siedlerkarren"]["kosten"].items() if isinstance(v, (int, float)) and not isinstance(v, bool)}  # Karrenkosten
    fk = {k: float(v) for k, v in forschung.kosten(1).items() if isinstance(v, (int, float)) and not isinstance(v, bool)}  # Wagenbau 1
    bedarf = Counter()  # Gesamtbedarf je Rohstoff
    for quelle in (minimum, karren, fk):  # alle drei Posten
        for roh, menge in quelle.items():  # je Rohstoff
            if roh == "siedler":  # Siedler sind Bevoelkerung, kein Material
                continue  # ueberspringen
            bedarf[str(roh).lower()] += menge  # addieren
    misch_klein = {str(k).lower(): v for k, v in misch.items()}  # Dorf-Ertrag in Kleinbuchstaben
    tage_liste = []  # je Rohstoff die Deckungszeit
    for roh, menge in bedarf.items():  # je benoetigtem Rohstoff
        rate_tag = misch_klein.get(roh, 0.0) * 24  # Tagesertrag des Dorfs
        tage_liste.append(menge / rate_tag if rate_tag > 0 else float("inf"))  # Tage (oder unendlich)
    zeile("Zeit_bis_erste_Siedlung_Tage", fmt(max(tage_liste)), "Gruendungsbedarf / Dorf-Tagesertrag (Vollertrag, Anlaufzeit nicht enthalten)")  # Zeit
    zeile("Gruendungsbedarf", ertrag_text({k: v for k, v in bedarf.items()}), "spieloekonomie.gruendungskosten + Siedlerkarren + Wagenbau 1")  # Bedarf
    # Zeit bis 100 Einheiten: Engpass ist Gold (100 Krieger je 500 Gold).
    gold_100 = 100 * krieger_gold  # Gold fuer 100 Krieger
    zeile("Zeit_bis_100_Einheiten_Gold_Tage", fmt(gold_100 / gold_misch_tag), "100 Krieger x 500 Gold / Reichs-Goldertrag je Tag")  # Gold-Engpass
    zeile("Zeit_bis_100_Einheiten_Siedler_Tage", fmt((100.0 / 6.0) / 24.0), "100 Siedler / 6 Siedler je Stunde")  # Siedleranteil
    zeile("Zeit_bis_100_Einheiten_Ausbildung_Tage", fmt((100 * 1200.0 / 3600.0) / 24.0), "100 x 20 min, eine Akademie")  # Ausbildungsanteil
    # Verbrauchsanteil der Nahrung am Tagesertrag (100 und 360 Einheiten).
    nah_tag = misch_klein.get("nahrung", 0.0) * 6 * 24  # Reichs-Nahrungsertrag je Tag
    zeile("Nahrung_Anteil_100_Einheiten_Prozent", fmt(100.0 * bedarf_100 / nah_tag), "800 je Tag / Reichs-Nahrungsertrag")  # 100
    zeile("Nahrung_Anteil_360_Einheiten_Prozent", fmt(100.0 * bedarf_360 / nah_tag), "2880 je Tag / Reichs-Nahrungsertrag")  # 360
    return 0  # fertig, ohne Fehler


if __name__ == "__main__":  # als Skript aufgerufen?
    sys.exit(main())  # main ausfuehren und Rueckgabewert weitergeben
