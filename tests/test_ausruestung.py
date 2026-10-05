"""
Ausruestung — Warenbedarf, Fehlmengen, Ausbildung, Verbrauch und Kette (05.10.2026).

Beweist die FACHLICHE Schicht src/ausruestung.py gegen die echten Projektdaten:

  * Genau 14 der 28 Einheiten nennen in data/units.json Waren ('waren'), die 14 uebrigen
    brauchen keine Ware (Handbuch 2009).
  * Der Warenbedarf kommt aus data/units.json, die Werkstatt/Voraussetzung aus items.json.
  * Eine leere Werkstatt macht die Ausbildung unmoeglich, fuehrende Gruende nennen Soll/Ist.
  * verbrauchen zieht nie unter 0 und veraendert das uebergebene Lager nicht.
  * Die Kette leitet sich vollstaendig aus units.json + items.json ab.

Aufruf:  python -X utf8 tests/test_ausruestung.py
Kein tkinter, kein Fenster.
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import spieldaten
import ausruestung as A


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def valueerror_von(fn):
    """Fuehrt fn aus und gibt die ValueError zurueck — None, wenn keine kam."""
    try:
        fn()
    except ValueError as e:
        return e
    except Exception:
        return None
    return None


# ==========================================================================
# 1. Datengrundlage
# ==========================================================================

abschnitt("Datengrundlage — 28 Einheiten, 17 Waren, 14 mit Warenbedarf")

_einheiten = spieldaten.einheiten()
_waren = spieldaten.waren()
_mit_bedarf = [n for n in _einheiten if A.bedarf(n)]
_ohne_bedarf = [n for n in _einheiten if not A.bedarf(n)]

check("es gibt genau 28 Einheiten", len(_einheiten) == 28, str(len(_einheiten)))
check("es gibt genau 17 Waren", len(_waren) == 17, str(len(_waren)))
check("genau 14 der 28 Einheiten haben Warenbedarf",
      len(_mit_bedarf) == 14, f"{len(_mit_bedarf)}: {_mit_bedarf}")
check("die uebrigen 14 brauchen keine Ware", len(_ohne_bedarf) == 14, str(len(_ohne_bedarf)))
check("bedarf('Kämpfer') ist genau Kurzschwert und Lederrüstung",
      A.bedarf("Kämpfer") == ["Kurzschwert", "Lederrüstung"], str(A.bedarf("Kämpfer")))
check("bedarf haelt die Reihenfolge der Datei ein (Paladin)",
      A.bedarf("Paladin") == ["Zweihänder", "Schwert", "Magischer Paladinharnisch"],
      str(A.bedarf("Paladin")))
check("eine Einheit ohne Ware liefert eine leere Liste",
      A.bedarf("Bürgerwehr") == [], str(A.bedarf("Bürgerwehr")))

_probe = A.bedarf("Kämpfer")
_probe.append("Drache")
check("bedarf gibt eine Kopie zurueck, die Datenliste bleibt unberuehrt",
      "Drache" not in A.bedarf("Kämpfer"), str(A.bedarf("Kämpfer")))

_alle_waren = sorted({w for n in _einheiten for w in A.bedarf(n)})
check("jede in bedarf genannte Ware ist ein Schluessel in data/items.json",
      all(w in _waren for w in _alle_waren),
      str([w for w in _alle_waren if w not in _waren]))
check("die 14 Einheiten brauchen zusammen genau die 17 Waren",
      set(_alle_waren) == set(_waren), f"{len(_alle_waren)} Waren")
_werkstaetten = {str((_waren[w] or {}).get("werkstatt")) for w in _alle_waren}
check("jede benoetigte Ware hat eine der drei Werkstaetten",
      _werkstaetten <= {"Schmiede", "Bogner", "Nähstube"}, str(sorted(_werkstaetten)))


# ==========================================================================
# 2. Unbekannte Einheit — kein Raten, sondern ValueError
# ==========================================================================

abschnitt("Unbekannte Einheit — ValueError nennt den Namen und die bekannten Schluessel")

_e = valueerror_von(lambda: A.bedarf("Drache"))
check("bedarf einer unbekannten Einheit wirft ValueError", _e is not None, repr(_e))
check("die Meldung nennt die unbekannte Einheit", _e is not None and "Drache" in str(_e), str(_e))
check("die Meldung nennt bekannte Schluessel (z. B. Kämpfer)",
      _e is not None and "Kämpfer" in str(_e), str(_e))
check("fehlende wirft bei unbekannter Einheit ValueError",
      valueerror_von(lambda: A.fehlende("Drache", {})) is not None)
check("ausbildbar wirft bei unbekannter Einheit ValueError",
      valueerror_von(lambda: A.ausbildbar("Drache", {})) is not None)
check("verbrauchen wirft bei unbekannter Einheit ValueError",
      valueerror_von(lambda: A.verbrauchen({}, "Drache")) is not None)
check("kette wirft bei unbekannter Einheit ValueError",
      valueerror_von(lambda: A.kette("Drache")) is not None)


# ==========================================================================
# 3. Fehlmengen
# ==========================================================================

abschnitt("Fehlmengen je Anzahl rechnen")

check("leeres Lager: beide Waren fehlen je 1",
      A.fehlende("Kämpfer", {}) == {"Kurzschwert": 1, "Lederrüstung": 1},
      str(A.fehlende("Kämpfer", {})))
check("volles Lager: nichts fehlt",
      A.fehlende("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 1}) == {},
      str(A.fehlende("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 1})))
check("Lagerstand 1 bei anzahl=3 ergibt Fehlmenge 2 beim Kurzschwert",
      A.fehlende("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 3}, anzahl=3) == {"Kurzschwert": 2},
      str(A.fehlende("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 3}, anzahl=3)))
check("ein fehlendes zweites Gut wird mit der vollen Stueckzahl gezaehlt",
      A.fehlende("Kämpfer", {"Kurzschwert": 1}, anzahl=3) == {"Kurzschwert": 2, "Lederrüstung": 3},
      str(A.fehlende("Kämpfer", {"Kurzschwert": 1}, anzahl=3)))
check("ein reichlich vorhandenes Gut steht nicht im Fehl-dict",
      A.fehlende("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 9}, anzahl=3) == {"Kurzschwert": 2},
      str(A.fehlende("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 9}, anzahl=3)))
check("Waren, die die Einheit nicht braucht, stoeren nicht",
      A.fehlende("Kämpfer", {"Messer": 0}) == {"Kurzschwert": 1, "Lederrüstung": 1},
      str(A.fehlende("Kämpfer", {"Messer": 0})))
check("eine Einheit ohne Warenbedarf hat nie eine Fehlmenge",
      A.fehlende("Bürgerwehr", {}) == {}, str(A.fehlende("Bürgerwehr", {})))
check("fehlende mit anzahl=0 wirft ValueError",
      valueerror_von(lambda: A.fehlende("Kämpfer", {}, anzahl=0)) is not None)


# ==========================================================================
# 4. Ausbildbarkeit
# ==========================================================================

abschnitt("Ausbildbarkeit — leeres Lager sperrt, volles Lager erlaubt")

_ok, _text = A.ausbildbar("Kämpfer", {})
check("mit leerem Lager ist der Kämpfer nicht ausbildbar", _ok is False, str(_ok))
check("die Begruendung nennt das Kurzschwert mit Soll/Ist", "Kurzschwert 1/0" in _text, _text)
check("die Begruendung nennt die Lederrüstung mit Soll/Ist", "Lederrüstung 1/0" in _text, _text)
check("die Begruendung beginnt mit 'Es fehlen'", _text.startswith("Es fehlen"), _text)

_ok2, _text2 = A.ausbildbar("Kämpfer", {"Kurzschwert": 1, "Lederrüstung": 1})
check("mit vollem Lager ist der Kämpfer ausbildbar", _ok2 is True, str(_ok2))
check("und die Begruendung ist nicht leer", bool(_text2), _text2)

_ok3, _text3 = A.ausbildbar("Kämpfer", {"Kurzschwert": 1}, anzahl=3)
check("anzahl=3 mit Lagerstand 1 ist nicht ausbildbar", _ok3 is False, str(_ok3))
check("und die Begruendung zeigt 3/1 fuer das Kurzschwert", "Kurzschwert 3/1" in _text3, _text3)

_ok4, _text4 = A.ausbildbar("Bürgerwehr", {})
check("eine Einheit ohne Warenbedarf ist immer ausbildbar", _ok4 is True, f"{_ok4} {_text4}")

check("ausbildbar mit anzahl=0 wirft ValueError",
      valueerror_von(lambda: A.ausbildbar("Kämpfer", {}, anzahl=0)) is not None)
check("ausbildbar mit anzahl=-1 wirft ValueError",
      valueerror_von(lambda: A.ausbildbar("Kämpfer", {}, anzahl=-1)) is not None)


# ==========================================================================
# 5. Verbrauch
# ==========================================================================

abschnitt("Verbrauch — neues dict, nie unter 0, kein Teilverbrauch")

_lager = {"Kurzschwert": 2, "Lederrüstung": 2, "Messer": 5}
_vorher = dict(_lager)
_neu = A.verbrauchen(_lager, "Kämpfer")
check("verbrauchen veraendert das uebergebene Lager nicht", _lager == _vorher, str(_lager))
check("verbrauchen liefert ein neues dict (nicht dasselbe Objekt)", _neu is not _lager)
check("nach dem Verbrauch sind Kurzschwert und Lederrüstung je 1",
      _neu["Kurzschwert"] == 1 and _neu["Lederrüstung"] == 1, str(_neu))
check("nicht benoetigte Waren bleiben unberuehrt", _neu["Messer"] == 5, str(_neu))

_zu_wenig = {"Kurzschwert": 5, "Lederrüstung": 0}
_vorher2 = dict(_zu_wenig)
_ergebnis = A.verbrauchen(_zu_wenig, "Kämpfer")
check("bei zu wenig Bestand kommt das Lager unveraendert zurueck",
      _ergebnis == _vorher2, str(_ergebnis))
check("und nichts wird abgezogen (kein Teilverbrauch)", _ergebnis["Kurzschwert"] == 5, str(_ergebnis))
check("der Bestand geht nie unter 0", all(v >= 0 for v in _ergebnis.values()), str(_ergebnis))
check("auch das Eingangs-dict bleibt bei zu wenig Bestand unveraendert",
      _zu_wenig == _vorher2, str(_zu_wenig))

_neu3 = A.verbrauchen({"Kurzschwert": 5, "Lederrüstung": 5}, "Kämpfer", anzahl=3)
check("anzahl=3 zieht je 3 ab",
      _neu3 == {"Kurzschwert": 2, "Lederrüstung": 2}, str(_neu3))
check("eine Einheit ohne Warenbedarf verbraucht nichts",
      A.verbrauchen({}, "Bürgerwehr") == {}, str(A.verbrauchen({}, "Bürgerwehr")))


# ==========================================================================
# 6. Die Kette
# ==========================================================================

abschnitt("Kette('Ritter') — Schwert, Waffentechnik 5, Schmiede, Kriegerakademie")

_kette = A.kette("Ritter")
_was = [s["was"] for s in _kette]
_wo = [s["wo"] for s in _kette]
_arten = [s["art"] for s in _kette]
check("kette('Ritter') enthaelt die Ware Schwert", "Schwert" in _was, str(_was))
check("kette('Ritter') enthaelt die Forschung Waffentechnik 5",
      "Waffentechnik 5" in _was, str(_was))
check("kette('Ritter') enthaelt die Werkstatt Schmiede", "Schmiede" in _was, str(_was))
check("kette('Ritter') nennt die Kriegerakademie als Ort",
      "Kriegerakademie" in _wo, str(_wo))
check("kette('Ritter') nummeriert 1-basiert fortlaufend",
      [s["schritt"] for s in _kette] == list(range(1, len(_kette) + 1)),
      str([s["schritt"] for s in _kette]))
check("kette('Ritter') endet mit dem Ausbildungsschritt", _arten[-1] == "einheit", str(_arten))
check("jeder Schritt hat genau die fuenf Felder",
      all(set(s) == {"schritt", "art", "was", "wo", "hinweis"} for s in _kette),
      str([sorted(s) for s in _kette]))
check("alle Schrittarten sind erlaubt (A.ARTEN)", set(_arten) <= set(A.ARTEN),
      str(sorted(set(_arten))))
check("jeder Schritt hat einen deutschen Hinweis", all(s["hinweis"] for s in _kette))

_was_k = [s["was"] for s in A.kette("Kämpfer")]
check("kette('Kämpfer') nennt beide Werkstaetten",
      "Schmiede" in _was_k and "Nähstube" in _was_k, str(_was_k))
check("kette('Kämpfer') enthaelt die kombinierte Voraussetzung 'Nähkunst 1'",
      "Nähkunst 1" in _was_k, str(_was_k))
check("kette('Kämpfer') enthaelt die kombinierte Voraussetzung 'Rüstungsbau 2'",
      "Rüstungsbau 2" in _was_k, str(_was_k))

_was_p = [s["was"] for s in A.kette("Paladin")]
check("kette('Paladin') nennt alle drei Waren",
      all(w in _was_p for w in ("Zweihänder", "Schwert", "Magischer Paladinharnisch")),
      str(_was_p))
check("kette('Paladin') enthaelt beide Voraussetzungen des Harnischs",
      "Rüstungsbau 7" in _was_p and "Magiekunde 2" in _was_p, str(_was_p))

_kette_ohne = A.kette("Bürgerwehr")
check("eine Einheit ohne Warenbedarf hat genau einen Schritt",
      len(_kette_ohne) == 1, str(_kette_ohne))
check("und dieser Schritt ist die Ausbildung",
      _kette_ohne[0]["art"] == "einheit", str(_kette_ohne))


# ==========================================================================
# 7. Anzeige und offene Luecken
# ==========================================================================

abschnitt("bestand_text und offene_luecken")

check("bestand_text ohne Fehlmenge sagt 'alles im Lager'",
      A.bestand_text({}) == "alles im Lager", A.bestand_text({}))
_leer_text = A.bestand_text(A.fehlende("Kämpfer", {}))
check("bestand_text fuer ein leeres Lager enthaelt 'fehlt'", "fehlt" in _leer_text, _leer_text)
_beispiel = A.bestand_text({"Kurzschwert": (1, 0), "Lederrüstung": (1, 0)})
check("bestand_text nennt Soll/Ist, wenn er sie bekommt",
      _beispiel == "fehlt: Kurzschwert 1/0 · Lederrüstung 1/0", _beispiel)

_luecken = A.offene_luecken()
check("offene_luecken liefert eine nichtleere Liste von Textzeilen",
      isinstance(_luecken, list) and bool(_luecken)
      and all(isinstance(z, str) and z for z in _luecken), str(_luecken))
check("offene_luecken nennt die kombinierte Voraussetzung des Paladinharnischs",
      any("Magischer Paladinharnisch" in z for z in _luecken), str(_luecken))

befund("Forschungsvoraussetzung der Einheit nicht in der Kette",
       "data/units.json kennt je Einheit eine Forschungsstufe (z. B. Kriegskunst 3 fuer den "
       "Krieger); die gehoert zur Forschungspruefung und ist bewusst nicht Teil der Warenkette.")


sys.exit(bericht())
