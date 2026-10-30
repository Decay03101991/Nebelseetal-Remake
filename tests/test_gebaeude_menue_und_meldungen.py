"""Pruefdatei: Gebaeude-Menues, Ausbildungszuordnung und ehrliche Sperrmeldungen.

Deckt Daniels Vorgaben vom 30.10.2026 ab:
- Ein Gebaeude-Menuepunkt existiert erst, wenn das Gebaeude steht (Stellmacher, Diebesgilde,
  Kaserne) und "Forschung" erst ab Bibliothek.
- Die BELEGTE Original-Menueliste (MENU_ITEMS) bleibt unveraendert.
- Sperrmeldungen nennen den fehlenden Rohstoff bzw. die fehlende Forschung mit Soll/Ist.
- Die letzte Bibliothek laesst sich nicht abreissen, eine zweite schon.

Aufruf: python -X utf8 tests/test_gebaeude_menue_und_meldungen.py
"""
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))

import main          # noqa: E402
import spieloekonomie  # noqa: E402
import fehlbestand   # noqa: E402

bestanden = []
fehler = []
befunde = []


def check(name, bedingung, detail=""):
    if bedingung:
        bestanden.append(name)
    else:
        fehler.append(f"{name} — {detail}")


def befund(name, detail):
    befunde.append(f"{name} — {detail}")


class Ort:
    """Minimalsiedlung fuer die Menuepruefung (nur `bauten` wird gelesen)."""

    def __init__(self, gebaeude=()):
        self.bauten = {str(i): g for i, g in enumerate(gebaeude)}
        self.stufen = {str(i): 1 for i in range(len(gebaeude))}
        self.id = "test:kontinent:1:1"
        self.vorraete = {}
        self.einheiten = {}
        self.waren = {}
        self.bevoelkerung = 0
        self.ausbildung = []


print("=" * 70)
print("1. Die belegte Original-Menueliste bleibt unveraendert")
print("=" * 70)
check("MENU_ITEMS enthaelt Kaserne", "Kaserne" in main.MENU_ITEMS, str(main.MENU_ITEMS))
check("MENU_ITEMS enthaelt Forschung", "Forschung" in main.MENU_ITEMS, str(main.MENU_ITEMS))
check("MENU_ITEMS hat weiterhin 17 Eintraege", len(main.MENU_ITEMS) == 17,
      f"{len(main.MENU_ITEMS)} Eintraege")
check("Stellmacher steht NICHT in der Original-Liste", "Stellmacher" not in main.MENU_ITEMS,
      "der Menuepunkt ist neu und darf die Original-Liste nicht verfaelschen")

print()
print("=" * 70)
print("2. Menuepunkte erscheinen erst mit ihrem Gebaeude")
print("=" * 70)
leer = main.menu_sichtbar([])
check("ohne Siedlung: keine Kaserne", "Kaserne" not in leer, str(leer))
check("ohne Siedlung: keine Forschung", "Forschung" not in leer, str(leer))
check("ohne Siedlung: kein Stellmacher", "Stellmacher" not in leer, str(leer))
check("ohne Siedlung: Dorfzentrum bleibt", "Dorfzentrum" in leer, str(leer))

mit_akademie = main.menu_sichtbar([Ort(["kriegerakademie"])])
check("Kriegerakademie -> Kaserne erscheint", "Kaserne" in mit_akademie, str(mit_akademie))
check("Kriegerakademie allein -> keine Forschung", "Forschung" not in mit_akademie, str(mit_akademie))

mit_bibliothek = main.menu_sichtbar([Ort(["bibliothek"])])
check("Bibliothek -> Forschung erscheint", "Forschung" in mit_bibliothek, str(mit_bibliothek))

mit_stellmacher = main.menu_sichtbar([Ort(["kriegerakademie", "stellmacher"])])
check("Stellmacher erscheint hinter der Kaserne",
      mit_stellmacher.index("Stellmacher") == mit_stellmacher.index("Kaserne") + 1,
      str(mit_stellmacher))

ohne_kaserne = main.menu_sichtbar([Ort(["stellmacher"])])
check("Stellmacher ohne Kaserne trotzdem sichtbar", "Stellmacher" in ohne_kaserne, str(ohne_kaserne))
check("Stellmacher ohne Kaserne steht hinter Lager",
      ohne_kaserne.index("Stellmacher") == ohne_kaserne.index("Lager") + 1, str(ohne_kaserne))

mit_gilde = main.menu_sichtbar([Ort(["diebesgilde"])])
check("Diebesgilde -> eigener Menuepunkt", "Diebesgilde" in mit_gilde, str(mit_gilde))

print()
print("=" * 70)
print("3. Sperrmeldung nennt den fehlenden Rohstoff mit Soll/Ist")
print("=" * 70)
ort = {"vorraete": {"holz": 37.2, "metall": 280.0, "leder": 15.0}, "importiert": {},
       "bevoelkerung": 5, "waren": {}, "ausbildung": []}
try:
    spieloekonomie.verbrauchen(ort, {"holz": 100, "metall": 15, "leder": 15}, 0.0)
    check("Handkarren-Kosten bei zu wenig Holz wird abgelehnt", False, "kein Fehler geworfen")
except ValueError as e:
    text = str(e)
    check("Ablehnung nennt Holz", "holz" in text, text)
    check("Ablehnung nennt die fehlende Menge 62.80", "62.80" in text, text)
    check("Ablehnung nennt den Bestand 37.20", "37.20" in text, text)
    check("Ablehnung nennt NICHT den gedeckten Rohstoff metall", "metall" not in text, text)

genug = {"vorraete": {"holz": 400.0, "metall": 280.0, "leder": 15.0}, "importiert": {},
         "bevoelkerung": 5, "waren": {}, "ausbildung": []}
neu = spieloekonomie.verbrauchen(genug, {"holz": 100, "metall": 15, "leder": 15}, 0.0)
check("mit genug Holz wird gebucht", abs(neu["vorraete"]["holz"] - 300.0) < 1e-6,
      str(neu["vorraete"]["holz"]))

print()
print("=" * 70)
print("4. Sperrmeldung nennt die fehlende Forschung")
print("=" * 70)
ort_karren = {"vorraete": {"holz": 500.0, "metall": 300.0, "leder": 300.0, "wolle": 300.0,
                           "pferde": 10.0, "nahrung": 900.0},
              "importiert": {}, "bevoelkerung": 20, "waren": {}, "ausbildung": [],
              "bauten": {"0": "stellmacher"}, "stufen": {"0": 1}}
try:
    spieloekonomie.ausbildung_start(ort_karren, "Siedlerkarren", {}, 0.0)
    check("Siedlerkarren ohne Wagenbau wird abgelehnt", False, "kein Fehler geworfen")
except ValueError as e:
    text = str(e)
    check("Ablehnung nennt Wagenbau", "Wagenbau" in text, text)
    check("Ablehnung nennt die Soll-Stufe", "Stufe 1" in text, text)

print()
print("=" * 70)
print("5. Die letzte Bibliothek laesst sich nicht abreissen")
print("=" * 70)


class Zustand:
    def __init__(self, orte):
        self.settlements = orte

    def _lokale_kasse_aktiv(self):
        return False


class App:
    """Nur so viel App, wie `_karten_abreissen` bis zur Bibliothekssperre anfasst."""

    def __init__(self, orte, feld):
        self.state = Zustand(orte)
        self.karten_siedlung = orte[0]
        self.karten_feld = feld
        self.root = None
        self.meldungen = []

    def _log(self, text):
        self.meldungen.append(text)

    def _menue_auffrischen(self):
        pass

    def _render_view(self):
        pass


einzel = [Ort(["bibliothek", "farm"])]
app = App(einzel, 0)
main.NebelseetalApp._karten_abreissen(app)
check("letzte Bibliothek bleibt stehen", einzel[0].bauten.get("0") == "bibliothek",
      str(einzel[0].bauten))
check("Ablehnung wird gemeldet", any("letzte Bibliothek" in m for m in app.meldungen),
      str(app.meldungen))

zwei = [Ort(["bibliothek"]), Ort(["bibliothek", "farm"])]
app2 = App(zwei, "0")
app2.karten_siedlung = zwei[1]
main.NebelseetalApp._karten_abreissen(app2)
check("zweite Bibliothek laesst sich abreissen", "0" not in zwei[1].bauten, str(zwei[1].bauten))
check("die andere Bibliothek bleibt stehen", zwei[0].bauten.get("0") == "bibliothek",
      str(zwei[0].bauten))

print()
print("=" * 70)
print("6. Zwei Navigationsebenen wie im Original")
print("=" * 70)
check("EBENEN nennt Uebersicht und Siedlung", main.EBENEN == ("Uebersicht", "Siedlung"),
      str(main.EBENEN))
uebersicht = main.menu_fuer_ebene([Ort(["bibliothek", "kriegerakademie", "stellmacher"])],
                                  "Uebersicht")
siedlung = main.menu_fuer_ebene([Ort(["bibliothek", "kriegerakademie", "stellmacher"])],
                                "Siedlung")
check("Uebersicht enthaelt Portal", "Portal" in uebersicht, str(uebersicht))
check("Uebersicht enthaelt NICHT Dorfzentrum", "Dorfzentrum" not in uebersicht, str(uebersicht))
check("Uebersicht enthaelt NICHT Forschung", "Forschung" not in uebersicht, str(uebersicht))
check("Siedlung enthaelt Dorfzentrum", "Dorfzentrum" in siedlung, str(siedlung))
check("Siedlung enthaelt Forschung (Bibliothek steht)", "Forschung" in siedlung, str(siedlung))
check("Siedlung enthaelt Stellmacher", "Stellmacher" in siedlung, str(siedlung))
check("Siedlung enthaelt NICHT Portal", "Portal" not in siedlung, str(siedlung))
check("beide Ebenen zusammen = menu_sichtbar",
      sorted(uebersicht + siedlung) == sorted(main.menu_sichtbar(
          [Ort(["bibliothek", "kriegerakademie", "stellmacher"])])),
      f"{len(uebersicht)} + {len(siedlung)}")
check("jeder Menuepunkt hat eine Ebene", all(p in main.EBENE_JE_PUNKT for p in main.MENU_ITEMS),
      str([p for p in main.MENU_ITEMS if p not in main.EBENE_JE_PUNKT]))

print()
print("=" * 70)
print(f"ERGEBNIS: {len(bestanden)} bestanden, {len(fehler)} Fehler, {len(befunde)} Befunde")
print("=" * 70)
for f in fehler:
    print("  FEHLER:", f)
for b in befunde:
    print("  BEFUND:", b)
sys.exit(0 if not fehler else 1)
