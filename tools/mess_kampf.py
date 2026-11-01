# Messwerkzeug B2: Kampf messen (Wall, Schlagkraft, Beute, Ladung, Reisekosten).
# Liest nur, schreibt nichts, aendert keinen Spielcode. Jede gedruckte Zeile hat die Form
#   <Kennzahl> | <Wert> | <Quelle>
# Aufruf:  python -X utf8 tools/mess_kampf.py
# Rueckgabewert 0 bei Erfolg. Kaempfe sind Zufall: 40 Laeufe je Wallstufe mit festem Startwert.

from __future__ import annotations  # moderne Typ-Annotationen.

import math  # fuer aufrunden (ceil).
import os  # fuer Pfade.
import random  # fuer den Zufallsgenerator.
import re  # fuer Treffer-Zaehlung im Protokoll.
import statistics  # fuer den Median.
import sys  # fuer sys.path und exit.
from datetime import datetime  # fuer den Zeitstempel.

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektwurzel aus dem Werkzeugpfad.
sys.path.insert(0, os.path.join(ROOT, "src"))  # src zuerst, damit die Module gefunden werden.
sys.path.insert(0, ROOT)  # auch die Wurzel (falls noetig).

import auftraege  # Reisekosten und Wegzeitfunktion.
import einheiten as E  # Einheitenwerte (SK, AT, Ladung).
import gebaeude_wirkung as GW  # dokumentierte Wallschwellen.
import kampf  # fuehre_schlacht und PROFILE.
import kampfbericht as KB  # vorrunde, beute_staffel, beute_am_ziel.
import spieldaten  # wallstufen (Quelle von fuehre_schlacht).

SEED = 20261101  # fester Startwert des Zufallsgenerators (im Bericht genannt).
LAEUFE = 40  # 40 Laeufe je Wallstufe (Abnahme).


def fern_einheit(chance):  # Fernkaempfer ueber seine eindeutige Fernkampfchance finden (ASCII-Quelle, Name darf Umlaute tragen).
    for name, profil in kampf.PROFILE.items():  # alle 15 Kampfprofile.
        if profil[4] == chance:  # Index 4 ist die Fernkampfchance (20/30/55/70).
            return name  # Name aus den Daten (z. B. mit Umlaut).
    return None  # nicht gefunden.


def kart(ladung):  # Karrenart ueber ihren eindeutigen Basiswert finden (40/100/250/1000/2500).
    for name in E.namen():  # alle 28 Einheiten.
        if E.ist_transport(name) and E.ladung(name) == ladung:  # Karren mit passendem Basiswert.
            return name  # Name aus den Daten.
    return None  # nicht gefunden.


def mittel(xs):  # Median einer Liste (Streuungsmass neben Min und Max).
    return statistics.median(xs)  # mittlerer Wert.


def schlachten(stufe, angreifer, verteidiger, geraet):  # 40 Schlachten je Wallstufe; liefert Zaehler und Verlustlisten.
    vorrunden = 0  # Zaehler bestandene Vorrunde.
    siege = 0  # Zaehler Angreifersiege.
    va = []  # Verluste Angreifer je Schlacht (Summe).
    vv = []  # Verluste Verteidiger je Schlacht (Summe).
    tf = []  # Fernkampf-Treffer je Schlacht (Summe).
    for i in range(LAEUFE):  # 40 Laeufe.
        rng = random.Random(SEED + i)  # fester Startwert je Lauf, wiederholbar.
        ergebnis = kampf.fuehre_schlacht(dict(angreifer), dict(verteidiger), wall_stufe=stufe,
                                         wall_zustand=100.0, angreifer_karren=dict(geraet),
                                         vorraete=None, rng=rng,
                                         forschung_angreifer={}, forschung_verteidiger={})  # echte Schlacht.
        if ergebnis.get("vorrunde_bestanden"):  # Wall ueberwunden?
            vorrunden += 1  # zaehlen.
        if ergebnis.get("ausgang") == "angreifer":  # Angreifersieg?
            siege += 1  # zaehlen.
        va.append(sum((ergebnis.get("verluste_angreifer") or {}).values()))  # eigene Tote je Schlacht.
        vv.append(sum((ergebnis.get("verluste_verteidiger") or {}).values()))  # gegnerische Tote je Schlacht.
        text = "\n".join(ergebnis.get("sequenzen") or [])  # Protokoll aller Sequenzen als Text.
        tf.append(sum(int(m.group(1)) for m in re.finditer(r"(\d+)\s*Treffer", text)))  # Treffer je Schlacht.
    return vorrunden, siege, va, vv, tf  # alles zurueck.


def staffel_lage(kennung):  # (wall_zustand_vor, verteidiger_uebrig) passend zur gewuenschten Staffel-Lage.
    if kennung == "keine_verteidiger":  # niemand verteidigt mehr.
        return 100.0, 0  # Zustand egal, Verteidiger 0.
    if kennung == "mauer_gebrochen":  # Wall war schon bei 0.
        return 0.0, 1  # Zustand 0, ein Verteidiger uebrig.
    if kennung == "mauer_beschaedigt":  # Wall teilweise eingerissen.
        return 50.0, 1  # Zustand 50, ein Verteidiger uebrig.
    return 100.0, 1  # mauer_heil: voller Zustand, Verteidiger uebrig.


def main():  # fuehrt alle sechs Messbloecke aus und gibt die Zeilen in der Pflichtform aus.
    krieger = "Krieger"  # ASCII-Name, Nahkampf (SK 3, AT 50).
    bogen = fern_einheit(30)  # Bogenschuetze (Fernchance 30).
    katapult = "Katapult"  # ASCII-Name, Belagerung (SK 45).
    angreifer = {krieger: 200, bogen: 30}  # Angreifer: Fuss 200, Fern 30.
    geraet = {katapult: 16}  # Belagerungsgeraet des Angreifers.
    verteidiger = {krieger: 100, bogen: 20}  # Verteidiger: Fuss 100, Fern 20.
    fuss_sk = E.schlagkraft(krieger) * 200  # Fuss-SK des Angreifers (nur Nahkampf zaehlt).
    bel_sk = E.schlagkraft(katapult) * 16  # Belagerungs-SK des Angreifers.
    fern_wert = kampf.PROFILE[bogen][4]  # Fernchance des Angreifer-Schuetzen (30).

    print("KOPF.WERKZEUG | tools/mess_kampf.py (Auftrag B2) | docs/auftraege/B2_paket_20261101.md")  # Kopf.
    print("KOPF.DATUM | %s | Systemzeit" % datetime.now().strftime("%Y-%m-%d %H:%M"))  # Zeitstempel.
    print("KOPF.SEED | %d | random.Random(seed + i), i = 0..%d" % (SEED, LAEUFE - 1))  # Startwert.
    print("AUFSTELLUNG.ANGREIFER | Krieger %d (Fuss-SK %d) + Bogenschuetze %d + Katapult %d (Belagerungs-SK %d) | einheiten.schlagkraft" % (200, fuss_sk, 30, 16, bel_sk))  # Angreifer.
    print("AUFSTELLUNG.VERTEIDIGER | Krieger %d + Bogenschuetze %d | einheiten.schlagkraft" % (100, 20))  # Verteidiger.

    print("WALL.LEGENDE | vorrunde siege verluste_angreifer(min/med/max) verluste_verteidiger(min/med/max) treffer_med | fuehre_schlacht, seed %d" % SEED)  # Legende.
    for stufe in range(0, 11):  # Wallstufen 0 bis 10.
        vorrunden, siege, va, vv, tf = schlachten(stufe, angreifer, verteidiger, geraet)  # 40 Laeufe.
        wert = "vorrunde=%d/%d siege=%d/%d va=%d/%d/%d vv=%d/%d/%d treffer=%d" % (vorrunden, LAEUFE, siege, LAEUFE, min(va), int(mittel(va)), max(va), min(vv), int(mittel(vv)), max(vv), int(mittel(tf)))  # Kennzahlen je Stufe.
        print("WALL.%d | %s | fuehre_schlacht, seed %d" % (stufe, wert, SEED))  # Tabelle C.

    print("TREFFERCHANCE.LEGENDE | chance_bogenschuetze_angreifer_in_prozent | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)")  # Legende.
    for stufe in range(0, 11):  # je Wallstufe.
        chance = fern_wert / 100.0 - 0.05 * stufe * (100.0 / 100.0)  # Fernchance minus Mauerabzug.
        chance = max(0.0, min(1.0, chance))  # auf [0,1] geklemmt, wie im Code.
        print("TREFFERCHANCE.%d | %.0f | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)" % (stufe, chance * 100))  # Zeile.

    print("SCHWELLE.LEGENDE | fuss belagerung pass_ab fail_bis abgleich_spieldaten | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle")  # Legende.
    for stufe in range(1, 11):  # Wallstufen 1 bis 10.
        doc = GW.wall_schwelle(stufe)  # dokumentierte Schwelle.
        fuss = doc["fusstruppen"]  # Fuss-Schwelle.
        bel_doc = doc["belagerungswaffen"]  # Belagerungs-Schwelle (None bei 1-4).
        bel_zu_pruefen = float(bel_doc) if bel_doc is not None else 0.0  # Belagerungs-SK zum Pruefen.
        pass_ab = KB.vorrunde(float(fuss), bel_zu_pruefen, stufe, 100.0).get("bestanden")  # besteht an der Schwelle?
        fail_bis = KB.vorrunde(float(fuss - 1), bel_zu_pruefen, stufe, 100.0).get("bestanden")  # faellt knapp darunter?
        sp = spieldaten.wallstufen()[stufe - 1]  # Gegenprobe Quelle von fuehre_schlacht.
        gleich = (sp["schwellenwert_fussttruppen"] == fuss and sp.get("schwellenwert_belagerungswaffen") == bel_doc)  # identisch?
        print("SCHWELLE.%d | fuss=%d bel=%s pass_ab=%s fail_bis=%s abgleich_spieldaten=%s | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle" % (stufe, fuss, (str(bel_doc) if bel_doc is not None else "-"), ("ja" if pass_ab else "nein"), ("ja" if fail_bis else "nein"), ("ja" if gleich else "nein")))  # Zeile.

    print("BEUTE.LEGENDE | staffel anteil% handkarren40_klein handkarren40_gross zweispaenner250_klein zweispaenner250_gross | kampfbericht.beute_staffel")  # Legende.
    klein = {"Holz": 100.0, "Stein": 100.0, "Metall": 100.0}  # kleiner Vorrat (3 x 100).
    gross = {"Holz": 10000.0, "Stein": 10000.0, "Metall": 10000.0}  # grosser Vorrat (3 x 10.000).
    hand = kart(40)  # Handkarren (Ladung 40).
    zweisp = kart(250)  # Zweispaenner (Ladung 250).
    for kennung in ("keine_verteidiger", "mauer_gebrochen", "mauer_beschaedigt", "mauer_heil"):  # vier Staffel-Lagen.
        zustand, uebrig = staffel_lage(kennung)  # Zustand und Verteidiger fuer die Lage.
        anteil = KB.BEUTE_STAFFEL_PROZENT[kennung]  # Prozentwert der Lage.
        hk = sum(KB.beute_staffel({hand: 1}, klein, wall_zustand_vor=zustand, verteidiger_uebrig=uebrig).values())  # Handkarren, klein.
        hg = sum(KB.beute_staffel({hand: 1}, gross, wall_zustand_vor=zustand, verteidiger_uebrig=uebrig).values())  # Handkarren, gross.
        zk = sum(KB.beute_staffel({zweisp: 1}, klein, wall_zustand_vor=zustand, verteidiger_uebrig=uebrig).values())  # Zweispaenner, klein.
        zg = sum(KB.beute_staffel({zweisp: 1}, gross, wall_zustand_vor=zustand, verteidiger_uebrig=uebrig).values())  # Zweispaenner, gross.
        print("BEUTE.%s | anteil=%d%% hand40_klein=%d hand40_gross=%d zweisp250_klein=%d zweisp250_gross=%d | kampfbericht.beute_staffel" % (kennung, anteil, hk, hg, zk, zg))  # Zeile.
    beute_wert, rest = KB.beute_am_ziel({hand: 1}, klein, "angreifer", wall_zustand_vor=100.0, verteidiger_uebrig=1)  # Beute UND Abbuchung.
    negativ = any(v < 0 for v in rest.values())  # irgendein Negativbestand?
    print("BEUTE.ABBUCHUNG | genommen=%d rest_summe=%.0f negativ=%s | kampfbericht.beute_am_ziel (Wall heil, 1 Verteidiger, Handkarren)" % (sum(beute_wert.values()), sum(rest.values()), negativ))  # Abbuchung.

    print("LADUNG.BASIS | handkarren=40 einspaenner=100 zweispaenner=250 handelskarawane=1000 grossehandelskarawane=2500 | einheiten.ladung (data/units.json)")  # Basiswerte.
    karten = [kart(40), kart(100), kart(250), kart(1000), kart(2500)]  # die fuenf Karrenarten (eindeutige Ladung).
    labels = ["handkarren", "einspaenner", "zweispaenner", "handelskarawane", "grossehandelskarawane"]  # ASCII-Labels.
    for stufe in (0, 1, 5, 10, 11, 15):  # Wagenbau-Stufen inkl. ueber der Hoechststufe 10.
        forschung = None if stufe == 0 else {"Wagenbau": stufe}  # Stufenkarte (None = ohne Bonus).
        werte = [E.ladung_der_gruppe({name: 1}, forschung) for name in karten]  # Ladung mit Bonus.
        faktor = E.ladungs_bonus(forschung)  # tatsaechlicher Faktor (gedeckelt bei 10).
        wert = " ".join("%s=%d" % (l, w) for l, w in zip(labels, werte))  # eine Zeile je Stufe.
        print("LADUNG.WAGENBAU%d | %s | einheiten.ladung_der_gruppe (Faktor %.1f)" % (stufe, wert, faktor))  # Zeile.

    print("REISEKOSTEN.LEGENDE | einheiten entfernung gold nahrung mana reisezeit_h | auftraege.kosten_der_mission (Saetze VORSCHLAG)")  # Legende.
    gs = E.geschwindigkeit("Krieger")  # GS 25 des Kriegers.
    for anzahl in (10, 40, 100):  # Truppengroessen.
        for entfernung in (1, 5, 20):  # Entfernungen.
            kosten = auftraege.kosten_der_mission({"Krieger": anzahl}, entfernung, gs, fremdes_ziel=True)  # Kosten.
            dauer = auftraege.reisezeit_sekunden(entfernung, gs) / 3600.0  # Reisezeit in Stunden.
            print("REISE.%d.%d | einheiten=%d gold=%.2f nahrung=%.2f mana=%.2f reisezeit=%.2f | auftraege.kosten_der_mission (VORSCHLAG)" % (anzahl, entfernung, anzahl, kosten["gold"], kosten["nahrung"], kosten["mana"], dauer))  # Zeile.

    print("GEGENPROBE.LEGENDE | stufe fuss_schwelle AT_Krieger_noetig SK_Krieger_noetig | E.angriff=50 vs E.schlagkraft=3 (Register 54)")  # Legende.
    for stufe in range(1, 11):  # Wallstufen 1 bis 10.
        fuss = GW.wall_schwelle(stufe)["fusstruppen"]  # dokumentierte Fuss-Schwelle.
        at_noetig = math.ceil(fuss / E.angriff("Krieger"))  # noetige Krieger nach AT.
        sk_noetig = math.ceil(fuss / E.schlagkraft("Krieger"))  # noetige Krieger nach SK.
        print("GEGENPROBE.%d | fuss=%d AT_Krieger=%d SK_Krieger=%d | E.angriff=%d vs E.schlagkraft=%d" % (stufe, fuss, at_noetig, sk_noetig, E.angriff("Krieger"), E.schlagkraft("Krieger")))  # Zeile.
    at_pass = KB.vorrunde(float(E.angriff("Krieger")), 0.0, 1, 100.0).get("bestanden")  # 1 Krieger, AT-Summe (falscher alter Weg).
    sk_pass = KB.vorrunde(float(E.schlagkraft("Krieger")), 0.0, 1, 100.0).get("bestanden")  # 1 Krieger, SK-Summe (richtiger Weg).
    print("GEGENPROBE.BEISPIEL | 1_Krieger_wall1 AT_besteht=%s SK_besteht=%s | AT wuerde faelschlich bestehen, SK lehnt ab (Register 54 behoben)" % (("ja" if at_pass else "nein"), ("ja" if sk_pass else "nein")))  # Beweis.
    return 0  # Erfolg.


if __name__ == "__main__":  # Start als Skript.
    sys.exit(main())  # Rueckgabewert 0.
