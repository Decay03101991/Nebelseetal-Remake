"""W-16: die Drachenschuppe ist eine Trophae mit eigenem Lagerfach (Register 207, 05.11.2026).

Daniels Auftrag (05.11.2026, woertlich-nah): die Drachenschuppe ist eine "eigene Auszeichnung" und
"zaehlt am Ende nur als Trophae". Bis hierher buchte der Drachenkampf sie ins Leere: das Spiel
kannte kein Lagerfach und meldete "dafuer gibt es noch kein Lagerfach". Diese Datei belegt, dass
die Trophae jetzt ankommt, bleibt und trotzdem keine Ware wird:

  (a) `data/trophaeen.json` traegt genau eine Trophae, mit Bild, und nennt die Regeln,
  (b) die 17 ORIGINALwaren bleiben unberuehrt (eigene Datei, keine Vermischung),
  (c) das Lager kennt 18 Faecher: 17 Waren + 1 Trophae, mit Icon,
  (d) ein frischer Spielstand legt das Fach mit 0 an,
  (e) nach einem gewonnenen Drachenkampf steht GENAU EINE Schuppe im Lager und im Bericht,
      und die alte Meldung "kein Lagerfach" kommt nicht mehr,
  (f) Speichern und Laden verliert die Trophae nicht,
  (g) keine Werkstatt stellt sie her,
  (h) der Kern des Handels lehnt sie ab (sonst waere sie ueber einen Vertrag doch eine Ware),
  (i) GEGENPROBE: ein unbekannter Name wird weiterhin NICHT eingelagert - die Wache ist nicht blind.

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()

import drachen
import einheiten
import spieldaten
import spieloekonomie
import werkstatt

main = ausnahme("main importieren", lambda: __import__("main"))
tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))
if main is None or tk is None:
    sys.exit(bericht())

TROPHaeE = "Drachenschuppe"          # der Name, wie er in den Daten steht
KEIN_FACH = "kein Lagerfach"         # die alte Meldung, die verschwinden muss


def einheit(anfang: str) -> str:
    """Den ECHTEN Namen einer Einheit aus den Daten holen (nie tippen)."""
    treffer = [n for n in einheiten.alle() if n.startswith(anfang)]
    return treffer[0] if treffer else ""


# ==========================================================================
abschnitt("(a) die Trophaeendatei ist vollstaendig")

pfad = os.path.join(ROOT, "data", "trophaeen.json")
check("data/trophaeen.json liegt da", os.path.isfile(pfad))
with open(pfad, encoding="utf-8") as f:
    roh = json.load(f)
je_trophae = roh.get("je_trophae") or {}
check("genau eine Trophae ist eingetragen", list(je_trophae) == [TROPHaeE], str(list(je_trophae)))
eintrag = je_trophae.get(TROPHaeE, {})
check("die Trophae hat eine Beschreibung", bool(str(eintrag.get("beschreibung") or "").strip()))
_bild = os.path.join(ROOT, str(eintrag.get("icon") or "").replace("/", os.sep))
check("das Bild der Trophae liegt da", os.path.isfile(_bild), str(eintrag.get("icon")))
regeln = roh.get("regeln") or {}
check("die Trophae ist nicht handelbar", regeln.get("handelbar") is False, str(regeln.get("handelbar")))
check("die Trophae zaehlt in keiner Formel", regeln.get("zaehlt_in_formeln") is False)
check("die Trophae hat ein Lagerfach", regeln.get("lagerfach") is True)
check("die Trophae wird nicht hergestellt", str(regeln.get("werkstatt") or "") != "")

# ==========================================================================
abschnitt("(b) die 17 Originalwaren bleiben unberuehrt")

check("data/items.json fuehrt weiter 17 Waren", len(spieldaten.waren()) == 17,
      str(len(spieldaten.waren())))
check("die Trophae steht NICHT in den Originalwaren", TROPHaeE not in spieldaten.waren())

# ==========================================================================
abschnitt("(c) das Lager kennt 18 Faecher")

lager = spieldaten.lager_waren()
check("17 Waren plus 1 Trophae", len(lager) == 18, str(len(lager)))
check("die Trophae ist im Lager", TROPHaeE in lager)
check("die Originalwaren sind alle noch im Lager",
      all(n in lager for n in spieldaten.waren()))
check("fuer die Trophae gibt es ein Icon im Lager", bool(lager.get(TROPHaeE, {}).get("icon")))
check("main.py baut die Icons ueber das Lager (auch fuer die Trophae)",
      TROPHaeE in main.WARE_ICONS, str(sorted(main.WARE_ICONS)[-3:]))
check("main.py fuehrt die Trophae in den Lagerwaren", TROPHaeE in main.LAGER_WARE_EINTRAEGE)
check("main.py fuehrt sie NICHT in den Werkstattwaren", TROPHaeE not in main.WARE_EINTRAEGE)

# ==========================================================================
abschnitt("(d) ein frischer Spielstand legt das Fach mit 0 an")

frisch = main.GameState()
check("das Lagerfach der Trophae steht auf 0", int(frisch.waren.get(TROPHaeE, -1)) == 0,
      str(frisch.waren.get(TROPHaeE)))

# ==========================================================================
abschnitt("(e) nach dem Drachenkampf steht die Schuppe im Lager")

root = None
app = None
try:
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    st = app.state
    app._erste_siedlung_gruenden()
    ort = st.aktive_siedlung()
    karre = einheit("Handelskarawane")                     # Name aus den Daten, ohne Umlaut getippt
    st.eigene_dimension = 2
    st.eigene_dimensionen = [1, 2]
    ort.einheiten = {"Krieger": 300, "Katapult": 22, karre: 4}
    ort.vorraete = {"gold": 900.0, "nahrung": 900.0}
    st.spieler_fraktion = "zwergisch"

    drache = drachen.finde_id("drache_d02")
    vorher = int(st.waren.get(TROPHaeE, 0))

    ok = app._angriff_auftrag_starten(
        str(drache.get("name")), drachen.verteidiger(drache),
        wall_stufe=0, wall_zustand=100.0, vorraete={},
        entfernung=2.0, truppen=dict(ort.einheiten),
        drache_id=str(drache.get("id")))
    check("der Angriff startet", bool(ok))
    eintrag_auftrag = st.auftraege[-1]
    ende = float(eintrag_auftrag.get("rueckkehr") or eintrag_auftrag.get("ankunft") or 0.0) + 1.0
    st.spielsekunden = max(float(st.spielsekunden), ende)
    st.auftraege_fortschreiben(st.spielsekunden)

    nachher = int(st.waren.get(TROPHaeE, 0))
    check("die Schuppe wurde eingelagert", nachher == vorher + 1, f"{vorher} -> {nachher}")
    check("der Drache steht als besiegt im Spielstand",
          str(drache.get("id")) in st.drachen_besiegt, str(st.drachen_besiegt))

    # Der Bericht ist der Beleg fuer den Spieler - er muss die Schuppe nennen.
    berichte = [m for m in st.messages if m.get("type") == "kampf"]
    letzter = str((berichte[-1].get("text") if berichte else ""))
    check("der Kampfbericht nennt die Schuppe", TROPHaeE in letzter, letzter[-160:])
    check("die alte Meldung 'kein Lagerfach' ist verschwunden", KEIN_FACH not in letzter)

    # ======================================================================
    abschnitt("(f) Speichern und Laden verliert die Trophae nicht")

    def runde():
        p = os.path.join(tempfile.gettempdir(), "nebel_test_trophae.json")
        st.save(p)
        neu = main.GameState()
        neu.load(p)
        os.remove(p)
        return int(neu.waren.get(TROPHaeE, -1))
    stand = ausnahme("Speichern/Laden der Trophae", runde)
    check("die Schuppe ueberlebt Speichern und Laden", stand == nachher, f"{stand} vs {nachher}")
finally:
    if root is not None:
        ausnahme("Fenster schliessen", root.destroy)

# ==========================================================================
abschnitt("(g) keine Werkstatt stellt die Trophae her")

typen = sorted({str(e.get("werkstatt") or "") for e in spieldaten.waren().values()} - {""})
check("es gibt Werkstatttypen in den Daten", bool(typen), str(typen))
for typ in typen:
    angebot = werkstatt.waren_der_werkstatt(typ)
    check(f"Werkstatt '{typ}' kennt die Trophae nicht", TROPHaeE not in angebot,
          str([w for w in angebot if w == TROPHaeE]))

# ==========================================================================
abschnitt("(h) der Kern des Handels lehnt die Trophae ab")


def handel_probe():
    """Ein Handelsvertrag mit der Trophae muss mit ValueError scheitern."""
    kaeufer = {"besitzer": "A", "dimension": 1, "einheiten": {"Krieger": 2},
               "waren": {}, "vorraete": {"gold": 500.0, "holz": 0.0}}
    verkaeufer = {"besitzer": "B", "dimension": 1, "einheiten": {"Krieger": 2},
                  "waren": {TROPHaeE: 1}, "vorraete": {"gold": 0.0, "holz": 0.0}}
    try:
        spieloekonomie.handel_start(kaeufer, verkaeufer, {"Krieger": 2}, TROPHaeE, 1, 10.0,
                                    "waren", 0.0)
    except ValueError as fehler:
        return str(fehler)
    return ""


meldung = ausnahme("Handel mit der Trophae", handel_probe)
check("der Handel wird abgelehnt", bool(meldung), str(meldung))
check("die Ablehnung nennt den Grund", "keine handelbare Ware" in str(meldung), str(meldung))

# ==========================================================================
abschnitt("(i) GEGENPROBE: ein unbekannter Name wird nicht eingelagert")

probe = main.GameState()
vorher_unbekannt = len(probe.waren)
probe.waren["GibtEsNicht"] = int(probe.waren.get("GibtEsNicht", 0)) + 1
check("ein erfundener Name steht nicht im Lagerfach-Satz",
      "GibtEsNicht" not in main.LAGER_WARE_EINTRAEGE and vorher_unbekannt == 18,
      f"{vorher_unbekannt} Faecher")
check("der Drachencode prueft das Lagerfach weiterhin (Meldung existiert noch im Code)",
      KEIN_FACH in open(os.path.join(ROOT, "src", "main.py"), encoding="utf-8").read())

sys.exit(bericht())
