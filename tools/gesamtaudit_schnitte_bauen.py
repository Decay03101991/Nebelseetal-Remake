"""Baut die vier GEZIELTEN Audit-Auftraege (Ausschnitt statt Gesamtdossier).

Plan: docs/audits/GESAMTAUDIT_PLAN_20261031.md
Stand 03:20 - nach Daniels Antworten vom 31.10.2026 angepasst:

  * Daniel-Regel: NEUESTE Fassung ist das Original. Nennt die neuere Fassung nur WERTE, waehrend die
    aeltere die MECHANIK beschreibt, gilt die aeltere Mechanik mit den neueren Zahlen - das ist eine
    begruendete Zusammenfuehrung, keine Erfindung. Daniels eigene Annahmen (z. B. Sieg bei 300
    Punkten) sind verwerfbar, wenn die Quellen etwas anderes vorgeben.
  * Reiseformel: Faktor 2 (2*d/GS) als Arbeitsformel gesetzt, ausdruecklich anpassbar.
  * Dimensionswechsel kostet KEINE Zeit (Daniel, sehr sicher); Dimensionen werden fuer ein
    Einzelspieler-Spiel zu "Spruengen in andere Laendereien" umgedeutet.
  * Beute wird GESTAFFELT (Mauer heil -> wenig; Mauer schon eingerissen -> viel; keine Verteidiger ->
    voller Bestand bis zur Karrenladung).
  * Kein Sieg bei 300 Punkten: das Original hat keine Siegbedingung. Stattdessen Auszeichnungen.
  * Daniel will eine Legende um das Spiel und Ideen, wie ein Einzelspieler das Interesse eines
    Mehrspieler-Spiels ersetzt.

Ergebnis: docs/audits/auftraege/  A1..A4
Aufruf: python -X utf8 tools/gesamtaudit_schnitte_bauen.py
Danach: python -X utf8 tools/gesamtaudit_lauf.py --auftrag docs/audits/auftraege/A2_wegzeit.md \
        --ziel docs/audits/BEFUND_A2_WEGZEIT_20261031.md
"""
from __future__ import annotations

import os
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIELORDNER = os.path.join(HIER, "docs", "audits", "auftraege")

KOPF = """RAHMEN UND VORGABEN (gelten fuer jede Aufgabe; Daniel, 31.10.2026)

1. ROLLE: Du bist PRUEFER UND ENTWERFER, nicht Erzaehler. Du urteilst ausschliesslich nach dem
   beigefuegten Material. Was dort nicht steht, ist "nicht belegbar" - du erfindest keine
   Zeilennummern, keine Seitenzahlen, keine Werte. Kein Vorwort, kein Lob, keine Zusammenfassung.
   Sprache: Deutsch.
2. NEUESTE FASSUNG IST DAS ORIGINAL. Nennt die NEUERE Fassung nur WERTE und beschreibt die AELTERE
   Fassung die MECHANIK, dann gilt: MECHANIK aus der aelteren, ZAHLEN aus der neueren Fassung. Das
   ist eine begruendete Zusammenfuehrung und ausdruecklich erlaubt - kennzeichne sie als
   "ZUSAMMENFUEHRUNG" und nenne beide Quellen mit Stelle.
3. NUR was in KEINER Fassung steht, ist VORSCHLAG. Vorschlaege werden so gekennzeichnet und mit
   einem Satz begruendet (Spielgefuehl, Balance, Einzelspieler-Tauglichkeit).
4. Daniels eigene fruehere Annahmen (z. B. Sieg bei 300 Gesamtpunkten) sind VERWERFBAR, wenn die
   Quellen etwas anderes vorgeben.
5. Einzelspieler statt Mehrspieler: das Original war ein Browsergame mit vielen Spielern. Hier gibt
   es EINEN Menschen und wenige Bots. Wo eine Regel nur wegen vieler Spieler existiert (z. B. 20
   Dimensionen als Platz fuer hunderte Welten), darf sie fuer den Einzelspieler neu gedeutet werden -
   aber so, dass sie Sinn ergibt und die Originalmechanik erkennbar bleibt.
6. Spieluhr: Faktor 180, also 1 Spielstunde = 20 echte Sekunden. Handbuch-Raten gelten pro
   SPIELSTUNDE; das Original lief in Echtzeit.
7. Belegpflicht: jede Aussage mit Datei und Zeile (bzw. Dokument + Stelle). "Nicht belegbar" ist ein
   vollwertiges Ergebnis.

AUSGABEFORMAT (allgemein)
- Tabellen genau in der vorgegebenen Spaltenzahl, hoechstens die genannte Zeilenzahl.
- Jede Zeile mit Quelle (Dokument + Stelle) oder dem Wort VORSCHLAG.
- Am Ende hoechstens drei Saetze "Was das fuer den Code bedeutet" - ohne Code zu schreiben.
"""


def lies(pfad: str) -> str:
    with open(os.path.join(HIER, pfad), encoding="utf-8", errors="replace") as f:
        return f.read()


def zeilen(pfad: str, von: int, bis: int) -> str:
    alle = lies(pfad).splitlines()
    return "\n".join(alle[von - 1:bis])


def block(titel: str, inhalt: str) -> str:
    return f"\n\n{'=' * 78}\n{titel}\n{'=' * 78}\n\n{inhalt.strip()}\n"


# ------------------------------------------------------------------ A1 Kampf + Beute

def a1() -> str:
    kopf = KOPF + """
AUFGABE A - KAMPF: WELCHE QUELLE GILT FUER WELCHEN SCHRITT, UND WIE WIRD DIE BEUTE GESTAFFELT?

Es gibt zwei Originalquellen fuer den Kampf:
  (1) HANDBUCH 2009: LE, AT, PA, RS, TP, MU, SK; Zweikampf in Kampfrunden; Sieger eines Zweikampfs
      verliert 1 Punkt AT und PA (Erschoepfung). Wallschwellen, Beute, Geraeteverlust, Punkte.
  (2) NEUERES FORUM-ORIGINAL (Material 2): Konstitution %, Kampfwert-Spanne, Ruestung, Fernkampfwert,
      Erschoepfungsschaden, Schwelle zur Kampfunfaehigkeit. Nennt WEDER Beute NOCH Geraeteverlust
      NOCH Punkte.

Im Remake folgt der Kampf heute Quelle (2) (`src/kampf.py`), Wall/Beute/Geraeteverlust/Punkte stammen
aus Quelle (1). Nach Vorgabe 2 ist das grundsaetzlich richtig - pruefe, ob es an JEDER Stelle richtig
angewandt ist.

TEIL A1: Tabelle "Kampfschritt | gilt | Quelle (Dokument + Stelle) | Art (belegt / ZUSAMMENFUEHRUNG /
VORSCHLAG)" fuer: Wallvorrunde, Mauerschaden, Fernkampf, Nahkampf/Zweikampf, Erschoepfung, Flucht,
Ausgang, Beute, Geraeteverlust, Punkte.

TEIL A2: Wo widersprechen sich die Quellen so, dass eine Zusammenfuehrung NICHT moeglich ist?
Hoechstens 6 Zeilen, je mit der kleineren Aenderung.

TEIL A3: GESTAFFELTE BEUTE (Daniels Vorgabe, noch ohne Zahlen):
  * Erster erfolgreicher Angriff, Mauer steht noch: Mauer wird beschaedigt/eingerissen, es wird WENIG
    erbeutet.
  * Mauer ist bereits (teilweise) eingerissen: deutlich MEHR Beute.
  * Keine Verteidiger mehr: der zum Angriffszeitpunkt vorhandene Bestand kann KOMPLETT mitgenommen
    werden - begrenzt durch die Karrenladung.
Belegt ist nur: "nur Transportkarren pluendern" und "Beute ist durch die Ladung begrenzt".
STAND DER UMSETZUNG (31.10.2026): Diese Staffelung ist bereits GEBAUT -
`kampfbericht.beute_staffel` mit 10 % / 30 % / 60 % / 100 %, angeschlossen in `auftraege.starten`,
Pruefdatei `tests/test_beute_staffel.py` (18 Pruefungen). Pruefe die WERTE und die Zuordnung
der Lagen, statt neue zu erfinden - und sage, wo die Staffelung den Originalregeln widerspricht.
Verlange: eine konkrete Staffelung mit Prozentwerten und die Formel, in der sie greift (Eingaben:
Wallzustand vor dem Kampf, Wallzustand nach dem Kampf, ueberlebende Verteidiger, Karrenladung,
Ortslager). Nenne je Zahl VORSCHLAG mit halbem Satz Begruendung. Sag ausdruecklich, ob diese
Staffelung mit den Originalregeln vereinbar ist oder ihnen widerspricht.

TEIL A4: Drei Saetze, was das fuer `src/kampf.py`, `src/kampfbericht.py` und `data/` bedeutet.

AUSGABEFORMAT
## Tabelle der Schritte
| Schritt | gilt | Quelle (Dokument + Stelle) | Art |
## Widersprueche (hoechstens 6 Zeilen)
| Nr | Widerspruch | Quelle A | Quelle B | kleinere Aenderung |
## Gestaffelte Beute
| Lage | Beuteanteil | Rechenweg | VORSCHLAG-Begruendung |
## In keiner Quelle geregelt
- hoechstens 4 Punkte
## Was das fuer den Code bedeutet
1.-3.
"""
    material = (block("1  HANDBUCH 2009 - Kampf, Auftraege, Punkte, Schutz (Projektauswertung)",
                      lies("docs/original/ORIGINAL_Kampf_und_Punkte.md"))
                + block("2  NEUERES FORUM-ORIGINAL (Volltext, Spielerfund)",
                        lies("docs/quellen/Das_Kampfsystem_Neu_Original.odt.txt"))
                + block("3  HANDBUCH 2009 - Kampfstellen im Wortlaut (Zeilen der Textfassung)",
                        zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 1206, 1338))
                + block("4  AKTIVER CODE - Profile und Ablauf (Auszug src/kampf.py)",
                        zeilen("src/kampf.py", 24, 70) + "\n\n[...]\n\n" + zeilen("src/kampf.py", 189, 210))
                + block("5  BEUTE IM CODE HEUTE (src/kampfbericht.py Z. 200-243)",
                        zeilen("src/kampfbericht.py", 200, 243))
                + block("6  WALLSCHWELLEN, PUNKTE, FREISCHALTUNG (Projektauswertung)",
                        lies("docs/quellen/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md")))
    return kopf + material


# ------------------------------------------------------------------ A2 Wegzeit

def a2() -> str:
    kopf = KOPF + """
AUFGABE B - WEGZEIT, AUFTRAGSKOSTEN, PORTAL: EIN ZAHLENSYSTEM FUER EIN EINZELSPIELER-SPIEL

STAND DER ENTSCHEIDUNGEN (Daniel, 31.10.2026):
  * Reiseformel: Dauer = 2 * d / GS ist GESETZT und IM CODE AKTIV
    (`auftraege.SEKUNDEN_JE_FELD = 7200`, Pruefdatei `tests/test_auftraege.py` 111 Pruefungen),
    ausdruecklich anpassbar. Grund: bei x180 waeren Wege mit Faktor 1 so kurz, dass der
    Verteidiger keine Vorwarnzeit hat. Pruefe den Faktor, erfinde keinen neuen.
  * Dimensionswechsel kostet KEINE Zeit (Daniel erinnert sich sehr sicher) - nur Mana.
  * Dimensionen existierten, weil hunderte Spieler Platz brauchten. Hier gibt es einen Menschen und
    wenige Bots -> Dimensionen sollen zu Spruengen in andere Laendereien werden.

VERLANGE:
1. Pruefe Faktor 2 nach: fuehrt er bei x180 zu sinnvollen Zeiten? Rechne die Beispiele; wenn du einen
   anderen Faktor empfiehlst, dann mit Rechnung.
2. Eine Kostentabelle: Gold und Nahrung je Einheit und Strecke; Mana je Entsendung nach Entfernung.
   Jede Zahl belegt oder VORSCHLAG.
3. Sechs Beispielreisen: 6, 16 und 32 Felder mit GS 5 und GS 35 - Spielstunden und Echtzeit bei x180,
   Hin- und Rueckweg.
4. Wirkung einer 10-%-Drosselung (Dauer, Gold, Nahrung) in einer Beispielzeile.
5. DIMENSIONEN ALS LAENDEREIEN: Wie werden aus 20 Dimensionen sinnvolle Landesteile fuer EINEN
   Spieler mit wenigen Bots? Was ist das Portal dann (Reise zwischen Laendern, Handel, Kopfgeld)?
   Welche Mana-Kosten bleiben sinnvoll, und wie bleibt die Originalmechanik erkennbar? Zwei Varianten
   mit Vor-/Nachteil und eine Empfehlung.
6. Drei Punkte, die auch nach dieser Rechnung offen bleiben.

AUSGABEFORMAT
## Formel
## Kostentabelle
| Groesse | Wert | belegt/VORSCHLAG | Quelle/Herleitung |
## Sechs Beispielreisen
| Distanz | GS | Spielstunden | Echtzeit bei x180 | Rueckweg gesamt |
## Drosselung um 10 %
## Dimensionen als Laendereien
## Drei offene Punkte
"""
    material = (block("1  HANDBUCH 2009 - GS, Auftragszeit, Auftragskosten (Wortlaut)",
                      zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 1084, 1148)
                      + "\n\n[...]\n\n"
                      + zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 1185, 1196))
                + block("2  VORVERSION 2006 - Portal, Limbus, Dimensionen, Mana (Wortlaut)",
                        lies("docs/original/Spielanleitung_2005/portal.php.txt"))
                + block("3  AKTIVER CODE - Reisezeit und Kosten (src/auftraege.py)",
                        zeilen("src/auftraege.py", 44, 72) + "\n\n[...]\n\n"
                        + zeilen("src/auftraege.py", 131, 160))
                + block("4  GESCHWINDIGKEITEN UND LADUNG DER 28 EINHEITEN (data/units.json)",
                        einheiten_gs())
                + block("5  PRODUKTIONSRATEN JE STUNDE (data/resources.json, Auszug)",
                        rohstoffe_raten()))
    return kopf + material


# ------------------------------------------------------------------ A3 Spielbarkeit + Bewertung

def a3() -> str:
    kopf = KOPF + """
AUFGABE C - SPIELBARKEIT BEI x180 UND BEWERTUNG STATT SIEG

STAND DER ENTSCHEIDUNGEN (Daniel, 31.10.2026):
  * Es gibt KEINEN Sieg wie im Original - ein Lauf endet nicht mit "gewonnen". Ein Ziel bei 300
    Gesamtpunkten ist VERWORFEN (Handbuch Seite 3: "Jeder hat bei Nebelseetal sicher seine eigenen
    Ziele" - Spielziel = Feldherr, Forscher oder Haendler).
  * Stattdessen soll ein Lauf BEWERTET werden: Auszeichnungen fuer die meisten Forschungspunkte, die
    meisten Kriegspunkte, die groesste Wirtschaftsmacht o. Ae.
  * STAND DER UMSETZUNG (31.10.2026): Die Punkteformel ist gebaut (`punkte.kriegspunkte`,
  `punkte.gesamtpunkte`), die Zielzahl 300 steht noch als VORSCHLAG im Code
  (`punkte.VORSCHLAG_ZIEL_PUNKTE`) und muss ersetzt werden. Der Goetterschutz-Bis-299-Punkte-Teil
  ist als reine Funktion gebaut (`punkte.angreifbar`, `punkte.goetterschutz_band`,
  `tests/test_goetterschutz_band.py` 23 Pruefungen), die Verdrahtung in die Bot-Angriffe fehlt.

VERLANGE:
1. Tabelle "Groesse | belegter Wert | Wirkung bei x180 (gerechnet) | Urteil (spielbar / zaeh /
   unspielbar)" fuer: Produktion je Gebaeude und Gelaende, Siedlerzuwachs (1/Stunde), Forschungsdauer
   (neue Stufe hoch 2 in Stunden), Ausbildungszeiten, Kriegspunkte je Einheit, Verteidigungsanlagen
   (Ausbaustufe hoch drei), Verhaeltnis Kriegs- zu Forschungspunkten. Rechne die Echtzeit bei x180 aus.
2. BEWERTUNG STATT SIEG: Entwirf ein Auszeichnungssystem, das die im Handbuch genannten Spielziele
   (Feldherr, Forscher, Haendler) abbildet. Hoechstens 6 Auszeichnungen, je mit Name, Kennzahl,
   Rechenweg aus BELEGTEN Punkten und warum sie zum Original passt. Sag ausdruecklich, wenn eine
   Kennzahl fehlt (Handelspunkte gibt es nur in der Fassung 2006).
3. WANN ENDET EIN LAUF DANN? Zwei Varianten (Zeitlimit, erreichte Auszeichnung, freies Weiterspielen
   bis alle Siedlungen verloren) mit Vor-/Nachteil und einer Empfehlung.
4. Die drei kleinsten Stellschrauben, die keine Originalzahl veraendern (Zeitfaktor, Startbedingungen,
   Kartengroesse) - mit Zahlen.

AUSGABEFORMAT
## Tabelle
| Groesse | belegter Wert | Wirkung bei x180 | Urteil |
## Bewertung statt Sieg
| Auszeichnung | Kennzahl | Rechenweg | Passung zum Original |
## Wann endet ein Lauf
## Drei Stellschrauben
## Fehlende Zahlen
"""
    material = (block("1  PUNKTE, SCHUTZ, SPIELZIEL (Projektauswertung Handbuch)",
                      lies("docs/original/ORIGINAL_Kampf_und_Punkte.md"))
                + block("2  HANDBUCH 2009 - Spielziel im Wortlaut (Seite 3)",
                        zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 45, 90))
                + block("3  HANDBUCH 2009 - Punkte im Wortlaut (Seite 4/5)",
                        zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 90, 140))
                + block("4  VORVERSION 2006 - Punktesystem inkl. Handelspunkte",
                        lies("docs/original/Spielanleitung_2005/punktesystem.php.txt"))
                + block("5  PUNKTE-CODE (src/punkte.py, Konstanten und Rechenwege)",
                        zeilen("src/punkte.py", 1, 60) + "\n\n[...]\n\n" + zeilen("src/punkte.py", 88, 125))
                + block("6  ERTRAEGE, STARTWERTE, SIEDLER (data/resources.json und Handbuch)",
                        rohstoffe_raten() + "\n\n"
                        + zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 330, 390))
                + block("7  FORSCHUNG: DAUER UND KOSTEN (Handbuch-Wortlaut)",
                        zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 396, 455))
                + block("8  GEBAEUDE, WALLSCHWELLEN, AUSBILDUNGSGEBAEUDE",
                        lies("docs/quellen/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md")))
    return kopf + material


# ------------------------------------------------------------------ A4 Einzelspieler

def a4() -> str:
    kopf = KOPF + """
AUFGABE D - ANTRIEB OHNE MITSPIELER: WIE ERZEUGT EIN EINZELSPIELER-SPIEL, WAS IM MEHRSPIELER-SPIEL
VON SELBST DA IST?

Daniel (31.10.2026): "In einem Mehrspieler-Spiel ist der Antrieb automatisch da: andere Spieler, mit
denen man sich messen kann - das ist schon ein Antrieb fuer sich. Ein Einzelspieler-Spiel muss diesen
Antrieb selbst erzeugen." Ausserdem: "Es soll eine Lobpreisung an das damalige Browsergame sein und
all seiner damaligen Spieler. Vielleicht eine kleine Geschichte, eine Legende ueber das Spiel."
Die Legende ist dabei EIN moegliches Mittel - nicht der Ersatz fuer den Antrieb.

VERLANGE (knapp und entscheidbar, keine Romanfassung):
1. WAS ERZEUGTE IM ORIGINAL DEN ANTRIEB? Hoechstens 6 Punkte, je mit Mechanik-Bezug aus dem Material
   (Ruhmeshalle und Rangfolge, Punkte, Handel, Goetterschutz, Diplomatie, Gaestersystem). Keine
   allgemeinen Browsergame-Floskeln.
2. FUENF ANTRIEBS-QUELLEN fuer den Einzelspieler, die auf BESTEHENDEN Mechaniken aufsetzen (keine neue
   Mechanik erfinden): je "Antrieb | setzt auf | wodurch entsteht der Vergleich/Massstab ohne echte
   Mitspieler (Bots als Messlatte, Ranglisten, Bestwerte, Auszeichnungen, Meilensteine) | Aufwand
   S/M/L". Wichtig: der Vergleich mit den Bots und mit frueheren eigenen Laeufen soll den Platz der
   anderen Spieler einnehmen - sag, wie weit das traegt und wo es nicht traegt.
3. LEGENDE (nur als eines der Mittel): Geruest in hoechstens 250 Woertern, ausschliesslich aus
   belegten Original-Bausteinen (Limbus, 20 Dimensionen, Nebelsee, Goetterschutz, Voelker,
   Ruhmeshalle) - getrennt in "belegt verwendet" und "neu erfunden". Kein Pathos.
4. DIMENSIONEN ALS LAENDEREIEN: drei Saetze, wie das im Einzelspieler Sinn ergibt (Anschluss B).
5. Die eine Frage, die Daniel zuerst beantworten muss, damit du weitermachen kannst.

AUSGABEFORMAT
## Was im Original den Antrieb erzeugte
| Punkt | Mechanik | Quelle |
## Fuenf Antriebs-Quellen fuer den Einzelspieler
| Antrieb | setzt auf | Massstab ohne Mitspieler | Aufwand |
## Wo der Ersatz nicht traegt
- hoechstens 3 Punkte
## Legende (eines der Mittel)
## Dimensionen als Laendereien
## Die eine Frage zuerst
"""
    material = (block("1  HANDBUCH 2009 - Spielziel, Bildschirmaufbau, Hauptmenue (Wortlaut)",
                      zeilen("docs/original/Spielanleitung_2009_Textfassung.txt", 45, 140))
                + block("2  VORVERSION 2006 - Beschreibung des Spiels (Wortlaut)",
                        lies("docs/original/Spielanleitung_2005/beschreibung.php.txt"))
                + block("3  PORTAL UND LIMBUS (Vorversion, Wortlaut)",
                        lies("docs/original/Spielanleitung_2005/portal.php.txt"))
                + block("4  PUNKTE, GOETTERSCHUTZ, BELEGTE SPIELDATEN",
                        lies("docs/original/ORIGINAL_Kampf_und_Punkte.md"))
                + block("5  WAS HEUTE SCHON DA IST (Selbstauskunft des Projekts)",
                        lies("docs/AKTUELLER_STAND.md"))
                + block("6  ORIGINAL-HINTERGRUNDGESCHICHTE DES SPIELS (Website-Archiv 11.09.2007, "
                        "Woertlich - DIE Grundlage fuer die Legende)",
                        lies("docs/quellen/ORIGINAL_HINTERGRUNDGESCHICHTE.md")))
    return kopf + material


# ------------------------------------------------------------------ Hilfen

def einheiten_gs() -> str:
    import json
    d = json.load(open(os.path.join(HIER, "data", "units.json"), encoding="utf-8"))
    zeilen = ["Name | GS | Ladung | Gebaeude"]
    for n, e in d["einheiten"].items():
        w = e.get("werte") or {}
        zeilen.append(f"{n} | {w.get('GS')} | {e.get('ladung')} | {e.get('gebaeude')}")
    return "\n".join(zeilen)


def rohstoffe_raten() -> str:
    import json
    d = json.load(open(os.path.join(HIER, "data", "resources.json"), encoding="utf-8"))
    return json.dumps({k: v for k, v in d.items() if not k.startswith("_")},
                      ensure_ascii=False, indent=1)[:4000]


def main():
    txt = os.path.join(HIER, "docs", "quellen", "Das_Kampfsystem_Neu_Original.odt.txt")
    if not os.path.isfile(txt):
        import re
        import zipfile
        with zipfile.ZipFile(os.path.join(HIER, "docs", "quellen",
                                          "Das_Kampfsystem_Neu_Original.odt")) as z:
            x = z.read("content.xml").decode("utf-8")
        x = re.sub(r"</text:p>", "\n", x)
        t = re.sub(r"<[^>]+>", "", x)
        t = re.sub(r"[ \t]+", " ", t)
        with open(txt, "w", encoding="utf-8", newline="\n") as f:
            f.write(re.sub(r"\n{3,}", "\n\n", t).strip())

    os.makedirs(ZIELORDNER, exist_ok=True)
    auftraege = {"A1_kampfmodell.md": a1(), "A2_wegzeit.md": a2(),
                 "A3_spielbarkeit.md": a3(), "A4_einzelspieler.md": a4()}
    gesamt = 0.0
    for name, text in auftraege.items():
        with open(os.path.join(ZIELORDNER, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        kosten = len(text) / 3.5 / 1e6 * 0.66 + 15000 / 1e6 * 1.98
        gesamt += kosten
        print(f"{name:26s} {len(text):7d} Zeichen  ~{len(text) / 3.5:6.0f} Prompt-Token  ~{kosten:.3f} USD")
    print(f"{'GESAMT (4 Laeufe)':26s} {'':7s}            {'':22s}  ~{gesamt:.3f} USD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
