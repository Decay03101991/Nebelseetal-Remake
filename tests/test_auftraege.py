"""
Auftraege und Missionen im Spiel (Paket WA, 04.10.2026).

Beweist, dass die vier belegten Auftragsarten (stationieren, transportieren, handeln,
angreifen) nach den Regeln aus docs/ENTWURF_AUFTRAEGE.md laufen:

  * die Reise dauert Zeit, die Rueckkehr genau so lange wie eine Strecke (S. 19),
  * die Karrenladung begrenzt die Fracht - ein voller Karren laeuft nicht ueber,
  * in fremden Siedlungen darf nicht stationiert werden (S. 19),
  * transportieren nur mit Karren, handeln nur mit Handelskarawanen,
  * ein Angriff ohne Schlagkraft wird mit Begruendung abgelehnt (Vorrunde, S. 20/21),
  * angekommen liefert jede Fracht GENAU EINMAL (kein Doppelbucheffekt),
  * Mengen werden nie negativ,
  * jeder eigene Wert steht als VORSCHLAG mit Grund in offene_luecken()/auftragsarten(),
  * zwei Laeufe mit gleicher Eingabe liefern dasselbe Ergebnis.

Der Kampf selbst wird NICHT nachgebaut: das Modul nutzt `kampfbericht.vorrunde` und
`kampfbericht.beute`.

Aufruf:  python -X utf8 tests/test_auftraege.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import auftraege as A

HK = "Handkarren"            # Ladung 40, GS 10
ESP = "Einspänner"           # Ladung 100, GS 25
ZSP = "Zweispänner"          # Ladung 250, GS 30
KARAWANE = "Handelskarawane"  # Ladung 1000, GS 25


# ==========================================================================
# 1. Oberflaeche - die geforderte API ist vorhanden
# ==========================================================================

abschnitt("Oberflaeche - die geforderte API")

for _name in ("auftragsarten", "neue_liste", "starten", "fortschritt", "angekommen",
              "reisezeit_sekunden", "ladung_der_mission", "bericht",
              "spieldaten_anwenden", "offene_luecken"):
    check(f"auftraege.{_name} ist vorhanden und aufrufbar", callable(getattr(A, _name, None)))

check("neue_liste() liefert eine leere Liste", A.neue_liste() == [])
check("starten liefert immer (Wahrheitswert, Text)",
      isinstance(A.starten(A.neue_liste(), "transportieren", {HK: 1}, "H", "Z", 10, 0)[0], bool)
      and isinstance(A.starten(A.neue_liste(), "transportieren", {HK: 1}, "H", "Z", 10, 0)[1], str))


# ==========================================================================
# 2. Auftragsarten - vier belegte Arten, 10-%-Drosselung belegt
# ==========================================================================

abschnitt("Auftragsarten - vier Arten und die belegte 10-%-Drosselung")

_arten = A.auftragsarten()
check("genau die vier belegten Arten sind bekannt",
      set(_arten) == {"stationieren", "transportieren", "handeln", "angreifen"}, str(sorted(_arten)))
check("jede Art nennt einen Text", all(_arten[k].get("text") for k in _arten))
check("jede Art nennt belegte Regeln", all(_arten[k].get("belegt") for k in _arten))
check("die 10-%-Drosselung aus dem Entwurf ist woertlich genannt",
      "10" in " ".join(str(x) for x in _arten["angreifen"]["belegt"]),
      str(_arten["angreifen"]["belegt"]))
check("belegte Anzahl der Drosselungsschritte ist 10",
      A.DROSSELUNG_SCHRITTE_PROZENT == 10)
check("das Zitat zur Drosselung nennt Seite 20", "Seite 20" in A.DROSSELUNG_ZITAT,
      A.DROSSELUNG_ZITAT)
check("die Rueckkehr dauert belegt doppelt so lange (Faktor 2)",
      A.HIN_UND_RUECK_FAKTOR == 2.0)


# ==========================================================================
# 3. Reisezeit - Formel, Symmetrie und Verdopplung
# ==========================================================================

abschnitt("Reisezeit - eine Strecke, symmetrisch und doppelt so lang zurueck")

check("reisezeit_sekunden(100, 10) = 36000 s (10 h)", A.reisezeit_sekunden(100, 10) == 36000.0,
      str(A.reisezeit_sekunden(100, 10)))
check("reisezeit_sekunden(0, 10) = 0 s", A.reisezeit_sekunden(0, 10) == 0.0)
check("eine negative Entfernung ergibt 0 s (nie negativ)", A.reisezeit_sekunden(-5, 10) == 0.0)
check("ohne Geschwindigkeit ist die Reisezeit unendlich",
      A.reisezeit_sekunden(10, 0) == float("inf"))
check("doppelte Entfernung = doppelte Reisezeit",
      A.reisezeit_sekunden(200, 10) == 2 * A.reisezeit_sekunden(100, 10))
check("doppelte Geschwindigkeit = halbe Reisezeit",
      A.reisezeit_sekunden(100, 20) == A.reisezeit_sekunden(100, 10) / 2)
check("1 Feld bei Geschwindigkeit 1 dauert SEKUNDEN_JE_FELD",
      A.reisezeit_sekunden(1, 1) == A.SEKUNDEN_JE_FELD)

_sym = A.neue_liste()
A.starten(_sym, "transportieren", {HK: 1}, "Heim", "Ziel", 100, 0, {"Holz": 10})
_e = _sym[0]
check("Hinreise und Rueckreise sind gleich lang (symmetrisch)",
      (_e["ankunft"] - _e["start"]) == (_e["rueckkehr"] - _e["ankunft"] - _e["aktion_dauer"]),
      f"{( _e['ankunft'] - _e['start'])} vs {( _e['rueckkehr'] - _e['ankunft'])}")
check("die Rueckkehr liegt genau zwei Strecken nach dem Start",
      _e["rueckkehr"] - _e["start"] == 2 * _e["reisezeit"], str(_e["rueckkehr"] - _e["start"]))
check("die Reisezeit entspricht der Formel", _e["reisezeit"] == A.reisezeit_sekunden(100, 10))


# ==========================================================================
# 4. Ladung - einheiten.ladung begrenzt die Fracht
# ==========================================================================

abschnitt("Ladung - die Karrenladung begrenzt die Fracht")

check("Handkarren tragen 40", A.ladung_der_mission({HK: 1}) == 40)
check("Einspaenner tragen 100", A.ladung_der_mission({ESP: 1}) == 100)
check("Zweispaenner tragen 250", A.ladung_der_mission({ZSP: 1}) == 250)
check("zwei Handkarren tragen 80", A.ladung_der_mission({HK: 2}) == 80)
check("gemischt: Handkarren + Einspaenner = 140", A.ladung_der_mission({HK: 1, ESP: 1}) == 140)
check("Kaempfer tragen nichts", A.ladung_der_mission({"Kämpfer": 3}) == 0)
check("unbekannte Einheiten tragen nichts", A.ladung_der_mission({"Drache": 1}) == 0)
check("Ladung ist nie negativ", A.ladung_der_mission({HK: -3}) == 0)


# ==========================================================================
# 5. Starten - alle vier Arten
# ==========================================================================

abschnitt("Starten - alle vier Auftragsarten laufen an")

_vier = A.neue_liste()
ok1, m1 = A.starten(_vier, "stationieren", {"Kämpfer": 1}, "Heim", "Aussen", 80, 0)
ok2, m2 = A.starten(_vier, "transportieren", {HK: 1}, "Heim", "Ziel", 100, 0, {"Holz": 30})
ok3, m3 = A.starten(_vier, "handeln", {KARAWANE: 1}, "Heim", "Markt", 50, 0, {"Holz": 10})
ok4, m4 = A.starten(_vier, "angreifen", {"Kämpfer": 2}, "Heim", "Feind", 80, 0)
check("stationieren startet", ok1 is True, m1)
check("transportieren startet", ok2 is True, m2)
check("handeln startet", ok3 is True, m3)
check("angreifen startet", ok4 is True, m4)
check("die Meldung nennt die Auftragsart", "stationieren" in m1, m1)
check("alle vier Auftraege stehen in der Liste", len(_vier) == 4, str(len(_vier)))
check("die Startmeldung nennt die Reisezeit", "Reisezeit" in m2, m2)
check("der Angriff hat Fracht leer (keine Karren)", _vier[3]["fracht"] == {}, str(_vier[3]["fracht"]))


# ==========================================================================
# 6. Starten - Falsches wird mit Begruendung abgelehnt
# ==========================================================================

abschnitt("Starten - Falsches wird mit Begruendung abgelehnt")

_ab = A.neue_liste()
check("unbekannte Auftragsart wird abgelehnt",
      A.starten(_ab, "spionieren", {"Kämpfer": 1}, "H", "Z", 10, 0)[0] is False)
check("die Ablehnung nennt die erlaubten Arten",
      "angreifen" in A.starten(_ab, "spionieren", {"Kämpfer": 1}, "H", "Z", 10, 0)[1])
check("ohne Einheiten wird abgelehnt",
      A.starten(_ab, "transportieren", {}, "H", "Z", 10, 0)[0] is False)
check("eine unbekannte Einheit wird abgelehnt",
      A.starten(_ab, "transportieren", {"Drache": 1}, "H", "Z", 10, 0)[0] is False)
check("die Ablehnung nennt die unbekannte Einheit",
      "Drache" in A.starten(_ab, "transportieren", {"Drache": 1}, "H", "Z", 10, 0)[1])
check("Entfernung 0 wird abgelehnt",
      A.starten(_ab, "transportieren", {HK: 1}, "H", "Z", 0, 0)[0] is False)
check("gleicher Start und Ziel wird abgelehnt",
      A.starten(_ab, "transportieren", {HK: 1}, "H", "H", 10, 0)[0] is False)
check("transportieren ohne Karren wird abgelehnt",
      A.starten(_ab, "transportieren", {"Kämpfer": 1}, "H", "Z", 10, 0)[0] is False)
check("die Ablehnung 'transportieren' nennt den Karren",
      "Karren" in A.starten(_ab, "transportieren", {"Kämpfer": 1}, "H", "Z", 10, 0)[1])
check("handeln ohne Handelskarawane wird abgelehnt",
      A.starten(_ab, "handeln", {HK: 1}, "H", "Z", 10, 0)[0] is False)
check("stationieren in fremder Siedlung wird abgelehnt",
      A.starten(_ab, "stationieren", {"Kämpfer": 1}, "H", {"name": "Feind", "fremd": True},
                10, 0)[0] is False)
check("die Ablehnung nennt das Verbot (Handbuch S. 19)",
      "S. 19" in A.starten(_ab, "stationieren", {"Kämpfer": 1}, "H",
                           {"name": "Feind", "fremd": True}, 10, 0)[1])

# Angriff ohne Schlagkraft: nur Karren -> keine Kampfkraft.
_ang = A.starten(_ab, "angreifen", {HK: 1}, "H", "Feind", 10, 0)
check("Angriff nur mit Karren (keine Schlagkraft) wird abgelehnt", _ang[0] is False, _ang[1])
check("die Ablehnung nennt die Schlagkraft", "Schlagkraft" in _ang[1], _ang[1])
check("die Ablehnung nennt die Vorrunde", "Vorrunde" in _ang[1], _ang[1])

# Angriff gegen einen Wall unterhalb der belegten Schwelle.
_ziel_wall = {"name": "Feind", "wall_stufe": 4, "wall_zustand_prozent": 100.0}
_sw = A.starten(_ab, "angreifen", {"Kämpfer": 1}, "H", _ziel_wall, 10, 0)
check("Angriff unter der Wall-Schwelle wird abgelehnt", _sw[0] is False, _sw[1])
check("die Ablehnung nennt die Schwelle 160 des Walls Stufe 4", "160" in _sw[1], _sw[1])
check("der Angriff reicht gegen Wall Stufe 1 (Schwelle 10) und startet",
      A.starten(A.neue_liste(), "angreifen", {"Kämpfer": 1}, "H",
                {"name": "Feind", "wall_stufe": 1}, 10, 0)[0] is True)

# Fracht: ein voller Karren laeuft nicht ueber.
_ueber = A.starten(_ab, "transportieren", {HK: 1}, "H", "Z", 10, 0, {"Holz": 50})
check("ein voller Karren (40) mit 50 Fracht wird abgelehnt", _ueber[0] is False, _ueber[1])
check("die Ablehnung nennt 'Ueberladen' und die Ladeplaetze", "Ueberladen" in _ueber[1]
      and "40" in _ueber[1], _ueber[1])
check("genau volle Fracht (40 auf 40) ist erlaubt",
      A.starten(A.neue_liste(), "transportieren", {HK: 1}, "H", "Z", 10, 0, {"Holz": 40})[0] is True)
check("negative Fracht wird abgelehnt",
      A.starten(_ab, "transportieren", {HK: 1}, "H", "Z", 10, 0, {"Holz": -5})[0] is False)
check("abgelehnte Auftraege landen NICHT in der Liste", len(_ab) == 0, str(len(_ab)))


# ==========================================================================
# 7. Fortschritt - hinreise, am_ziel, rueckreise, abgeschlossen
# ==========================================================================

abschnitt("Fortschritt - die vier Phasen einer Reise")

_ph = A.neue_liste()
A.starten(_ph, "transportieren", {HK: 1}, "Heim", "Ziel", 100, 0, {"Holz": 10})
_ank = _ph[0]["ankunft"]
_ru = _ph[0]["rueckkehr"]

check("zu Beginn ist der Auftrag auf der Hinreise",
      A.fortschritt(_ph, 0)["hinreise"][0]["status"] == "hinreise")
check("im Ankunftsaugenblick ist er am Ziel",
      A.fortschritt(_ph, _ank)["am_ziel"][0]["status"] == "am_ziel")
check("kurz nach der Ankunft ist er auf der Rueckreise",
      A.fortschritt(_ph, _ank + 1)["rueckreise"][0]["status"] == "rueckreise")
check("nach der Rueckkehr ist er abgeschlossen",
      A.fortschritt(_ph, _ru)["abgeschlossen"][0]["status"] == "abgeschlossen")
check("der Merker 'abgeschlossen' wird gesetzt", _ph[0].get("abgeschlossen") is True)
check("fortschritt(..., 0) meldet genau einen Auftrag", A.fortschritt(_ph, 0)["gesamt"] == 1)
check("die Restzeit zu Beginn ist die Reisezeit",
      A.fortschritt(_ph, 0)["hinreise"][0]["rest_sekunden"] == _ph[0]["reisezeit"])
check("jeder Auftrag steht in der Oberliste 'je'", len(A.fortschritt(_ph, 0)["je"]) == 1)
check("eine leere Liste liefert 0 Auftraege", A.fortschritt(A.neue_liste(), 0)["gesamt"] == 0)


# ==========================================================================
# 8. Angekommen - die Fracht wird GENAU EINMAL abgeliefert
# ==========================================================================

abschnitt("Angekommen - jede Fracht wird genau einmal abgeliefert")

_ag = A.neue_liste()
A.starten(_ag, "transportieren", {HK: 1}, "Heim", "Ziel", 100, 0, {"Holz": 30})
check("vor der Ankunft ist nichts angekommen", A.angekommen(_ag, _ag[0]["ankunft"] - 1) == [])
check("im Ankunftsaugenblick kommt der Auftrag an",
      len(A.angekommen(_ag, _ag[0]["ankunft"])) == 1)
check("ein zweiter Aufruf liefert NICHTS (genau einmal)",
      A.angekommen(_ag, _ag[0]["ankunft"]) == [])

# Ein Auftrag, der angekommen UND zurueckgekehrt ist, wird genau einmal abgeliefert.
_ag2 = A.neue_liste()
A.starten(_ag2, "handeln", {KARAWANE: 1}, "Heim", "Markt", 50, 0, {"Holz": 10})
_erste = A.angekommen(_ag2, _ag2[0]["rueckkehr"])
check("ein angekommener und zurueckgekehrter Auftrag wird einmal abgeliefert", len(_erste) == 1)
check("danach liefert derselbe Auftrag kein zweites Mal", A.angekommen(_ag2, _ag2[0]["rueckkehr"]) == [])
check("der Merker 'abgeliefert' steht am Auftrag", _ag2[0].get("abgeliefert") is True)


# ==========================================================================
# 9. Bericht - typ 'auftrag'
# ==========================================================================

abschnitt("Bericht - der Auftragsbericht fuer 'Nachrichten'")

_b = A.bericht(_ag2[0])
check("bericht liefert ein Verzeichnis", isinstance(_b, dict))
check("bericht hat den Typ 'auftrag'", _b.get("typ") == "auftrag", str(_b.get("typ")))
check("bericht hat einen Titel", isinstance(_b.get("titel"), str) and bool(_b["titel"]))
check("der Titel nennt die Auftragsart", "handeln" in _b["titel"].lower(), _b["titel"])
check("bericht hat eine nicht leere Zeilenliste",
      isinstance(_b.get("zeilen"), list) and len(_b["zeilen"]) >= 4, str(len(_b.get("zeilen", []))))
check("eine Zeile nennt die Reisezeit je Strecke",
      any("Reisezeit" in z for z in _b["zeilen"]), str(_b["zeilen"]))
check("eine Zeile nennt die Fracht",
      any("Fracht" in z for z in _b["zeilen"]), str(_b["zeilen"]))


# ==========================================================================
# 10. spieldaten_anwenden - wirkt genau einmal, nie negativ
# ==========================================================================

abschnitt("spieldaten_anwenden - Beute, Gold, Stationieren, Genau-Einmal")

# Angriff mit Karren: Beute wird berechnet (kampfbericht.beute) und genau einmal gutgeschrieben.
_angriff = A.neue_liste()
A.starten(_angriff, "angreifen", {"Kämpfer": 2, HK: 1}, "Heim",
          {"name": "Feind", "wall_stufe": 1, "vorraete": {"Holz": 1000}}, 10, 0)
check("der Angriff traegt Beute eingetragen (Holz 40)", _angriff[0]["beute"] == {"Holz": 40},
      str(_angriff[0]["beute"]))

_stand = {"ressourcen": {"Holz": 5}, "einheiten": {"Kämpfer": 2, HK: 1}}
_neu1 = A.spieldaten_anwenden(_stand, _angriff[0])
check("die Beute kommt genau einmal zum Bestand (5 + 40)", _neu1["ressourcen"]["Holz"] == 45,
      str(_neu1["ressourcen"]))
check("der Eingabestand wird NICHT veraendert", _stand["ressourcen"]["Holz"] == 5)
_neu2 = A.spieldaten_anwenden(_neu1, _angriff[0])
check("ein zweiter Aufruf bucht die Beute NICHT erneut (45 bleibt 45)",
      _neu2["ressourcen"]["Holz"] == 45, str(_neu2["ressourcen"]))

# Stationieren: die Einheiten bleiben am Ziel und gehen ab - nie unter 0.
_station = A.neue_liste()
A.starten(_station, "stationieren", {"Kämpfer": 3}, "Heim", "Aussen", 80, 0)
_neu3 = A.spieldaten_anwenden({"ressourcen": {}, "einheiten": {"Kämpfer": 2}}, _station[0])
check("stationierte Einheiten gehen von der Heimat ab und werden nie negativ",
      _neu3["einheiten"]["Kämpfer"] == 0, str(_neu3["einheiten"]))

# Handeln angenommen: Gold kommt dazu.
_handel = A.neue_liste()
A.starten(_handel, "handeln", {KARAWANE: 1}, "Heim",
          {"name": "Markt", "handel_akzeptiert": True, "gold_bietet": 500}, 50, 0)
_neu4 = A.spieldaten_anwenden({"ressourcen": {"gold": 100}, "einheiten": {}}, _handel[0])
check("verdientes Gold kommt zum Bestand (100 + 500)", _neu4["ressourcen"]["gold"] == 600,
      str(_neu4["ressourcen"]))

# Handeln abgelehnt: die Waren kommen zurueck.
_abgelehnt = A.neue_liste()
A.starten(_abgelehnt, "handeln", {KARAWANE: 1}, "Heim",
          {"name": "Markt", "handel_akzeptiert": False}, 50, 0, {"Holz": 10})
_neu5 = A.spieldaten_anwenden({"ressourcen": {}, "einheiten": {}}, _abgelehnt[0])
check("bei Ablehnung kehren die Waren zurueck", _neu5["ressourcen"].get("Holz") == 10,
      str(_neu5["ressourcen"]))
check("ein leerer Zustand wird ohne Fehler verkraftet",
      isinstance(A.spieldaten_anwenden(None, _abgelehnt[0]), dict))


# ==========================================================================
# 11. Gleiche Eingabe -> gleiches Ergebnis
# ==========================================================================

abschnitt("Determinismus - gleiche Eingabe, gleiches Ergebnis")

def _bau():
    l = A.neue_liste()
    msgs = [
        A.starten(l, "transportieren", {HK: 1}, "Heim", "Ziel", 100, 0, {"Holz": 30}),
        A.starten(l, "handeln", {KARAWANE: 1}, "Heim", "Markt", 50, 0, {"Holz": 10}),
        A.starten(l, "angreifen", {"Kämpfer": 2}, "Heim", "Feind", 80, 0),
    ]
    return l, msgs


_l1, _m1 = _bau()
_l2, _m2 = _bau()
check("zwei Laeufe liefern dieselben Startmeldungen", _m1 == _m2)
check("zwei Laeufe liefern denselben Fortschritt",
      A.fortschritt(_l1, 5000) == A.fortschritt(_l2, 5000))
check("zwei Laeufe liefern denselben Bericht", A.bericht(_l1[0]) == A.bericht(_l2[0]))
check("zwei Laeufe liefern denselben Endzustand des Fortschritts",
      A.fortschritt(_l1, 10 ** 9) == A.fortschritt(_l2, 10 ** 9))


# ==========================================================================
# 12. Offene Luecken - jeder eigene Wert mit Grund
# ==========================================================================

abschnitt("Offene Luecken - jeder eigene Wert mit Grund")

_luecken = A.offene_luecken()
_texte = " ".join(str(v) for v in _luecken.values())
check("offene_luecken ist ein nicht leeres Verzeichnis", isinstance(_luecken, dict) and _luecken)
check("jede Luecke hat einen nicht leeren Grund",
      all(isinstance(v, str) and v.strip() for v in _luecken.values()))
check("SEKUNDEN_JE_FELD (3600) ist mit Grund in offene_luecken",
      str(int(A.SEKUNDEN_JE_FELD)) in _texte)
check("AKTION_DAUER_SEKUNDEN (0) ist mit Grund in offene_luecken",
      "aktion_dauer" in _luecken)
check("BEUTE_ANTEIL_PROZENT (50) ist mit Grund in offene_luecken",
      str(A.BEUTE_ANTEIL_PROZENT) in _texte)
check("DROSSELUNG_SCHRITTE_PROZENT (10) ist mit Grund in offene_luecken",
      str(A.DROSSELUNG_SCHRITTE_PROZENT) in _texte)
check("die Beute-Zahl ist ausdruecklich als VORSCHLAG gekennzeichnet",
      "VORSCHLAG" in _luecken.get("beute_anteil", ""), _luecken.get("beute_anteil", ""))
check("die Geschwindigkeitswahl ist als VORSCHLAG gekennzeichnet",
      "VORSCHLAG" in _luecken.get("geschwindigkeit_wahl", ""))
check("der Fusstruppen-Begriff ist als VORSCHLAG gekennzeichnet",
      "VORSCHLAG" in _luecken.get("fusstruppen_begriff", ""))
befund("Reisezeit-Formel und Aktionsdauer sind VORSCHLAG",
       "das Handbuch nennt weder eine Entfernung/Geschwindigkeit-Formel noch eine "
       "Aufenthaltsdauer am Ziel; beide Werte stehen mit Grund in auftraege.offene_luecken()")


sys.exit(bericht())
