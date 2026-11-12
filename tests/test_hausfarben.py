"""Frage 6: die Hausfarben folgen den Wappentinkturen (Register 213, 05.11.2026).

Daniels Entscheidung (05.11.2026, Frage 6): "Ja, angleichen" - die sechs Hausfarben in der
Chronik und in `data/haeuser.json` folgen den Tinkturen der GELIEFERTEN Wappenbilder. Vorher
stand dort die alte Chronik-Farbe (Menschen "Blau und Silber" gegen ein weinrot-goldenes Wappen).

Diese Datei belegt vier Dinge und eine Gegenprobe:

  (a) `data/haeuser.json` traegt sechs Haeuser, jedes mit einem Wert "farben",
  (b) dieser Wert ist aus dem WAPPENSATZ desselben Hauses ableitbar - gleiche Anzahl Farben,
      jede Tinktur der Wappenbeschreibung kommt in "farben" vor und umgekehrt. Damit ist "farben"
      keine zweite Wahrheit, sondern eine Kurzfassung des Satzes aus dem Bild,
  (c) die Chronik nennt je Haus GENAU den Wert aus der Datei (Bindung ueber den Sitz, nicht ueber
      die Reihenfolge), in BEIDEN Chronik-Fassungen, und die alten Farben kommen dort nicht mehr vor,
  (d) beide Chronik-Fassungen sind hashgleich (sonst zeigen zwei Dokumente zwei Staende),
  (e) GEGENPROBE: eine absichtlich falsche Farbe MUSS als Fehler erkannt werden - sonst ist die
      Pruefung blind und ihr Gruen bedeutet nichts.

Eine ehrliche Grenze bleibt und ist erlaubt: die Elfen fuehren im Wappensatz das blosse "Gruen",
ihre Hausfarbe heisst "Dunkelgruen" wie der Schildgrund - dieselbe Farbe, genauere Benennung.
Deshalb vergleicht (b) Farbstaemme, nicht Zeichen fuer Zeichen.

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['haeuser', 'stimmen']
PRUEF_DATEN = ['haeuser.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Die beiden Chronik-Fassungen (Wurzel und docs/) - beide tragen dieselben Saetze.
FASSUNGEN = ("CHRONIK_DER_WELT.md", os.path.join("docs", "CHRONIK_DER_WELT_20261104.md"))

# Wortlaut-Anker der beiden beteiligten Saetze (Umlaute als Escape, Datei bleibt ASCII).
WAPPEN_ANFANG = "Das Wappen f\u00fchrt "          # "Das Wappen fuehrt ..."
FARBEN_ANFANG = "Die Farben des Hauses sind "     # "Die Farben des Hauses sind ..."

# Die alten Chronik-Farben. Sie duerfen in keinem Farben-Satz mehr stehen.
ALTE_FARBEN = ("Blau und Silber", "Schwarz und Gold", "Silber und Gr\u00fcn",
               "Dunkelrot und Schwarz", "Gr\u00fcn und Knochenwei\u00df", "Bunt und Grau")


def _lies(pfad: str) -> str:
    """Eine Datei als Text (UTF-8) - der eine Lesezugriff dieser Pruefung."""
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def _lies_bytes(pfad: str) -> bytes:
    """Eine Datei als Rohbytes - fuer den Hash, damit er zu `sha256sum` passt."""
    with open(pfad, "rb") as f:
        return f.read()


def zerlege(liste: str) -> list:
    """Eine Farbaufzaehlung in Einzelwoerter: 'Nachtblau, Grau und Gold' -> drei Woerter.

    Trenner sind Komma und das Wort 'und'; leere Stuecke fallen weg. So liest dieselbe
    Funktion die Tinkturliste des Wappensatzes UND den Wert aus der Datendatei.
    """
    roh = str(liste or "").replace(",", " und ")           # Komma wie ein 'und' behandeln
    teile = [t.strip() for t in roh.split(" und ")]        # an jedem 'und' trennen
    return [t for t in teile if t]                         # leere Stuecke weg


def pruefe_tinktur(kennung: str, eintrag: dict) -> list:
    """Vergleicht den Wert 'farben' mit der Tinkturliste des Wappensatzes. Gibt Fehler zurueck.

    Geprueft wird in beide Richtungen, damit weder eine Farbe des Wappens fehlt noch eine
    Farbe im Datensatz steht, die das Bild nicht fuehrt. Verglichen werden Staemme
    ('Dunkelgruen' deckt 'Gruen' ab), nicht ganze Zeichenketten.
    """
    fehler: list = []
    farben = zerlege(eintrag.get("farben"))                        # der Wert aus der Datendatei
    beschreibung = str(eintrag.get("wappen_beschreibung") or "")   # der Satz aus dem Bild
    if not farben:
        return ["%s: kein Wert in farben" % kennung]
    stelle = beschreibung.find(WAPPEN_ANFANG)                      # wo der Wappensatz beginnt
    if stelle < 0:
        return ["%s: Wappensatz fehlt in der Beschreibung" % kennung]
    rest = beschreibung[stelle + len(WAPPEN_ANFANG):]               # der Text nach "fuehrt "
    doppelpunkt = rest.find(":")                                   # die Tinkturliste endet am Doppelpunkt
    if doppelpunkt < 0:
        return ["%s: Tinkturliste ohne Doppelpunkt" % kennung]
    tinkturen = zerlege(rest[:doppelpunkt])                        # z. B. ['Nachtblau', 'Grau', 'Gold']
    if len(tinkturen) != len(farben):                              # gleiche Anzahl Farben
        fehler.append("%s: %d Tinkturen im Wappen, %d in farben (%s)"
                      % (kennung, len(tinkturen), len(farben), eintrag.get("farben")))
    for tinktur in tinkturen:                                      # keine Tinktur darf fehlen
        if not any(f.lower().endswith(tinktur.lower()) for f in farben):
            fehler.append("%s: Tinktur %s fehlt in farben" % (kennung, tinktur))
    for farbe in farben:                                           # keine erfundene Farbe
        if farbe.lower() not in beschreibung.lower():
            fehler.append("%s: Farbe %s kommt im Wappensatz nicht vor" % (kennung, farbe))
    return fehler


def pruefe_chronik(daten: dict, chronik: str, fassung: str) -> list:
    """Prueft je Haus den Chronik-Satz gegen die Datendatei. Gibt Fehler zurueck.

    Die Bindung laeuft ueber den SITZ des Hauses ('Burg Silberbach'), nicht ueber die
    Reihenfolge - so faellt ein vertauschter Absatz sofort auf.
    """
    fehler: list = []
    zeilen = [z for z in chronik.splitlines() if FARBEN_ANFANG in z]   # alle Farben-Saetze
    if len(zeilen) != 6:
        fehler.append("%s: %d Farben-Saetze statt 6" % (fassung, len(zeilen)))
    for kennung, eintrag in (daten.get("je_haus") or {}).items():
        sitz = str(eintrag.get("sitz") or "")                          # der Anker im Absatz
        soll = str(eintrag.get("farben") or "")                        # der Wert aus der Datei
        treffer = [z for z in zeilen if sitz and sitz in z]            # die Zeile dieses Hauses
        if len(treffer) != 1:
            fehler.append("%s/%s: %d Zeilen mit Sitz %r statt 1"
                          % (fassung, kennung, len(treffer), sitz))
            continue
        zeile = treffer[0]
        stelle = zeile.find(FARBEN_ANFANG) + len(FARBEN_ANFANG)        # hinter "sind "
        ist = zeile[stelle:].split(".")[0].strip()                     # bis zum Satzpunkt
        if ist != soll:
            fehler.append("%s/%s: Chronik sagt %r, Datei %r" % (fassung, kennung, ist, soll))
        for alt in ALTE_FARBEN:                                        # die alte Farbe darf nicht bleiben
            if ist == alt:
                fehler.append("%s/%s: alte Farbe %r steht noch da" % (fassung, kennung, alt))
    return fehler


def haupt() -> int:
    """Fuehrt alle Abschnitte aus und liefert den Rueckgabewert des Pruefrahmens."""
    daten = json.loads(_lies(os.path.join(ROOT, "data", "haeuser.json")))  # die EINE Quelle der Haeuser
    haeuser = daten.get("je_haus") or {}

    # ------------------------------------------------------------------ (a) Datendatei vollstaendig
    abschnitt("(a) data/haeuser.json traegt sechs Haeuser mit Farben")
    check("sechs Haeuser", len(haeuser) == 6, "%d" % len(haeuser))
    for kennung, eintrag in haeuser.items():
        check("%s hat einen Wert farben" % kennung, bool(str(eintrag.get("farben") or "").strip()),
              str(eintrag.get("farben")))

    # ------------------------------------------------- (b) farben ist aus dem Wappensatz ableitbar
    abschnitt("(b) die Farben folgen den Tinkturen des eigenen Wappensatzes")
    for kennung, eintrag in haeuser.items():
        fehler = pruefe_tinktur(kennung, eintrag)
        check("%s: farben deckt den Wappensatz" % kennung, not fehler, "; ".join(fehler))

    # ---------------------------------------------------- (c) Chronik nennt genau diese Werte
    abschnitt("(c) die Chronik nennt je Haus genau den Wert aus der Datei (beide Fassungen)")
    for fassung in FASSUNGEN:
        pfad = os.path.join(ROOT, fassung)
        check("%s vorhanden" % fassung, os.path.isfile(pfad))
        chronik = _lies(pfad)                                         # die Fassung als Text
        fehler = pruefe_chronik(daten, chronik, fassung)
        check("%s: sechs Farben-Saetze stimmen" % fassung, not fehler, "; ".join(fehler))
        for alt in ALTE_FARBEN:                                       # alte Farbe nirgends mehr im Satz
            bleibt = [z for z in chronik.splitlines()
                      if FARBEN_ANFANG + alt in z]
            check("%s: alte Farbe %r ist weg" % (fassung, alt), not bleibt)

    # --------------------------------------------------- (d) beide Chronik-Fassungen hashgleich
    abschnitt("(d) beide Chronik-Fassungen sind hashgleich")
    hashes = [hashlib.sha256(_lies_bytes(os.path.join(ROOT, f))).hexdigest()
              for f in FASSUNGEN]
    check("gleicher SHA256 in Wurzel und docs/", hashes[0] == hashes[1], hashes[0][:16])

    # ------------------------------------------------------------------------ (e) Gegenprobe
    abschnitt("(e) GEGENPROBE: eine falsche Farbe MUSS rot werden")
    kaputt = copy.deepcopy(daten)                                     # Arbeitskopie, nie die Quelle
    kaputt["je_haus"]["menschlich"]["farben"] = "Blau und Silber"      # die alte, falsche Farbe
    chronik = _lies(os.path.join(ROOT, FASSUNGEN[0]))
    fehler_chronik = pruefe_chronik(kaputt, chronik, "Gegenprobe")
    fehler_tinktur = pruefe_tinktur("menschlich", kaputt["je_haus"]["menschlich"])
    check("Gegenprobe: Chronik widerspricht der falschen Farbe", bool(fehler_chronik),
          "; ".join(fehler_chronik)[:120])
    check("Gegenprobe: falsche Farbe faellt auch am Wappensatz auf", bool(fehler_tinktur),
          "; ".join(fehler_tinktur)[:120])
    fehler_erfunden = pruefe_tinktur("ghule", dict(haeuser["Ghule"], farben="Blau und Pink"))
    check("Gegenprobe: eine erfundene Farbe faellt auf", bool(fehler_erfunden),
          "; ".join(fehler_erfunden)[:120])

    befund("Die Elfen fuehren im Wappensatz 'Gruen', ihre Hausfarbe heisst 'Dunkelgruen' "
           "(Schildgrund) - dieselbe Farbe, genauere Benennung, deshalb Stammvergleich in (b).")

    return bericht()


if __name__ == "__main__":
    sys.exit(haupt())
