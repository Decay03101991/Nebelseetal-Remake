"""Pruefung des Forschungsablaufs (src/forschung.py) gegen das Originalhandbuch.

Alle Originalregeln sind belegt (Handbuch 2009, Seiten 11-13):
  * Kosten verdoppeln sich je Stufe (50, 100, 200, 400 …).
  * Dauer = neue Stufe zum Quadrat in Stunden (3 -> 9, 5 -> 25).
  * Die Stufe steigt erst nach Ablauf der Zeit, nicht beim Klick.
  * Bibliothek ist Voraussetzung; ein laufender Auftrag sperrt sein Gebiet.
  * Abbruch kostet die Rohstoffe; die Stufe steigt nicht.
  * Forschungspunkte = Stufe hoch drei.

Die Zeit wird als Sekunden-Zahl uebergeben, darum laeuft alles ohne echtes Warten.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import forschung as F
import spieldaten as S

H = 3600.0  # eine Stunde in Sekunden

abschnitt("Grunddaten des Standes")
stand0 = F.neuer_stand()
check("Stand kennt alle 21 Forschungen", len(stand0) == 21, str(len(stand0)))
check("Stand nennt genau die Originalgebiete",
      set(stand0) == set(S.forschungen()), "")
check("jedes Gebiet startet auf Stufe 0",
      all(e["stufe"] == 0 for e in stand0.values()), "")
check("zu Beginn laeuft kein Auftrag",
      all(e["auftrag"] is None for e in stand0.values()), "")

abschnitt("Dauer — neue Stufe zum Quadrat in Stunden")
check("Dauer Stufe 1 = 1 Stunde", F.dauer_stunden(1) == 1, str(F.dauer_stunden(1)))
check("Dauer Stufe 2 = 4 Stunden", F.dauer_stunden(2) == 4, str(F.dauer_stunden(2)))
check("Dauer Stufe 3 = 9 Stunden", F.dauer_stunden(3) == 9, str(F.dauer_stunden(3)))
check("Dauer Stufe 5 = 25 Stunden", F.dauer_stunden(5) == 25, str(F.dauer_stunden(5)))
check("Dauer Stufe 0 = 0 Stunden", F.dauer_stunden(0) == 0, str(F.dauer_stunden(0)))
check("Helfer liefert die Originalregel (keine eigene Zahl)",
      F.dauer_stunden(7) == S.forschungsdauer_stunden(7), str(S.forschungsdauer_stunden(7)))

abschnitt("Kosten — Verdopplung je Stufe (Handbuch Seite 13)")
k1 = F.kosten(1)
k2 = F.kosten(2)
k3 = F.kosten(3)
k4 = F.kosten(4)
check("Stufe 1 kostet 50 Holz", k1.get("holz") == 50, str(k1))
check("Stufe 2 kostet 100 Holz", k2.get("holz") == 100, str(k2))
check("Stufe 3 kostet 200 Holz", k3.get("holz") == 200, str(k3))
check("Stufe 4 kostet 400 Holz", k4.get("holz") == 400, str(k4))
check("Kosten kommen aus der belegten Datenschicht",
      [F.kosten(n)["holz"] for n in (1, 2, 3, 4)] ==
      [S.forschungs_kosten(n)["holz"] for n in (1, 2, 3, 4)], "")
stand_k = F.neuer_stand()
check("naechste_kosten liefert Stufe-1-Kosten fuer ein frisches Gebiet",
      F.naechste_kosten(stand_k, "Kriegskunst").get("holz") == 50, "")

abschnitt("Start braucht eine Bibliothek")
stand = F.neuer_stand()
roh = {"holz": 1000}
ok, meld = F.starten("Kriegskunst", stand, 0.0, hat_bibliothek=False,
                     vorhandene_rohstoffe=roh)
check("ohne Bibliothek kein Start", ok is False, str((ok, meld)))
check("Meldung nennt die Bibliothek", "bibliothek" in meld.lower(), meld)
check("ohne Bibliothek laeuft kein Auftrag", stand["Kriegskunst"]["auftrag"] is None, "")
check("ohne Bibliothek bleiben die Rohstoffe unangetastet", roh["holz"] == 1000, str(roh))

abschnitt("Start braucht die Rohstoffe")
stand = F.neuer_stand()
roh = {"holz": 49}  # Stufe 1 kostet 50
ok, meld = F.starten("Kriegskunst", stand, 0.0, hat_bibliothek=True,
                     vorhandene_rohstoffe=roh)
check("ohne Rohstoffe kein Start", ok is False, str((ok, meld)))
check("Meldung nennt den fehlenden Rohstoff", "holz" in meld.lower(), meld)
check("zu wenig Rohstoffe lassen den Auftrag nicht starten",
      stand["Kriegskunst"]["auftrag"] is None, "")
check("abgelehnter Start aendert die Rohstoffe nicht", roh["holz"] == 49, str(roh))

abschnitt("Erfolgreicher Start — Kosten abgezogen, Stufe noch unveraendert")
stand = F.neuer_stand()
roh = {"holz": 1000}
ok, meld = F.starten("Kriegskunst", stand, 0.0, hat_bibliothek=True,
                     vorhandene_rohstoffe=roh)
check("mit Bibliothek und Rohstoffen startet die Forschung", ok is True, str((ok, meld)))
check("Stufe 1 kostet genau 50 Holz (1000 -> 950)", roh["holz"] == 950, str(roh))
auftrag = stand["Kriegskunst"]["auftrag"]
check("ein laufender Auftrag ist gesetzt", auftrag is not None, "")
check("Auftrag kennt Zielstufe 1", auftrag and auftrag["zielstufe"] == 1, str(auftrag))
check("Auftrag kennt Startzeit 0 und Dauer 1 h",
      auftrag and auftrag["startzeit"] == 0.0 and auftrag["dauer_stunden"] == 1,
      str(auftrag))
check("Auftrag merkt sich die abgebuchten Kosten (50 Holz)",
      auftrag and auftrag["kosten"].get("holz") == 50, str(auftrag))
check("Stufe steigt NICHT direkt beim Start", stand["Kriegskunst"]["stufe"] == 0, "")

abschnitt("Stufe steigt nicht vor Ablauf")
f0 = F.fortschritt(stand, 0.0)
check("direkt nach dem Start noch nicht fertig",
      f0["Kriegskunst"]["laufend"] is True and f0["Kriegskunst"]["fertig"] is False,
      str(f0["Kriegskunst"]))
f1 = F.fortschritt(stand, 1.0)
check("auch nach 1 Sekunde noch nicht fertig", f1["Kriegskunst"]["fertig"] is False, "")
fvor = F.fortschritt(stand, 1 * H - 5.0)
check("5 Sekunden vor Ablauf noch nicht fertig", fvor["Kriegskunst"]["fertig"] is False, "")
check("vor Ablauf steigt die Stufe auch beim Abschliessen nicht",
      F.abschliessen(stand, 1 * H - 5.0) == [] and stand["Kriegskunst"]["stufe"] == 0, "")
check("Reststunden vor Ablauf stimmen (5 s = 5/3600 h)",
      abs(fvor["Kriegskunst"]["reststunden"] - 5.0 / H) < 1e-9,
      str(fvor["Kriegskunst"]["reststunden"]))

abschnitt("Stufe steigt genau nach Ablauf")
fgenau = F.fortschritt(stand, 1 * H)
check("genau nach 1 Stunde ist der Auftrag fertig",
      fgenau["Kriegskunst"]["fertig"] is True and fgenau["Kriegskunst"]["laufend"] is True,
      str(fgenau["Kriegskunst"]))
check("Reststunden sind dann 0", fgenau["Kriegskunst"]["reststunden"] == 0.0, "")
gestiegen = F.abschliessen(stand, 1 * H)
check("abschliessen laesst das Gebiet steigen", gestiegen == ["Kriegskunst"], str(gestiegen))
check("Stufe ist jetzt 1", stand["Kriegskunst"]["stufe"] == 1, "")
check("der Auftrag ist danach entfernt", stand["Kriegskunst"]["auftrag"] is None, "")
check("nach Ablauf meldet fortschritt 'nicht mehr laufend'",
      F.fortschritt(stand, 2 * H)["Kriegskunst"]["laufend"] is False, "")

abschnitt("abschliessen mehrfach aufrufen — keine Doppelstufe")
nochmal = F.abschliessen(stand, 100 * H)
check("zweiter Aufruf laesst nichts mehr steigen", nochmal == [], str(nochmal))
check("Stufe bleibt nach zweitem Aufruf 1", stand["Kriegskunst"]["stufe"] == 1, "")

abschnitt("Zweiter Auftrag im selben Gebiet wird abgelehnt (Gebiet gesperrt)")
stand = F.neuer_stand()
roh = {"holz": 10000}
F.starten("Kriegskunst", stand, 0.0, hat_bibliothek=True, vorhandene_rohstoffe=roh)
ok2, meld2 = F.starten("Kriegskunst", stand, 0.5 * H, hat_bibliothek=True,
                       vorhandene_rohstoffe=roh)
check("zweiter Start im selben Gebiet scheitert", ok2 is False, str((ok2, meld2)))
check("Meldung erwaehnt den laufenden Auftrag",
      "laeuft" in meld2.lower() or "auftrag" in meld2.lower(), meld2)
check("der laufende Auftrag bleibt unveraendert (Zielstufe 1, Start 0)",
      stand["Kriegskunst"]["auftrag"]["zielstufe"] == 1
      and stand["Kriegskunst"]["auftrag"]["startzeit"] == 0.0, "")
check("abgelehnter zweiter Start kostet keine Rohstoffe (nur 50 weg)",
      roh["holz"] == 10000 - 50, str(roh["holz"]))
ok3, _ = F.starten("Baukunst", stand, 0.5 * H, hat_bibliothek=True,
                   vorhandene_rohstoffe=roh)
check("ein anderes Gebiet darf parallel forschen", ok3 is True, "")

abschnitt("Stufe 2: Dauer 4 Stunden, Kosten 100 Holz")
stand = F.neuer_stand()
stand["Kriegskunst"]["stufe"] = 1
roh = {"holz": 1000}
ok, meld = F.starten("Kriegskunst", stand, 10.0, hat_bibliothek=True,
                     vorhandene_rohstoffe=roh)
check("Stufe 2 startet", ok is True, str((ok, meld)))
check("Stufe 2 kostet 100 Holz (1000 -> 900)", roh["holz"] == 900, str(roh))
check("Auftrag Stufe 2 hat Dauer 4 h",
      stand["Kriegskunst"]["auftrag"]["dauer_stunden"] == 4, "")
check("3 h 59 min 55 s vor Ablauf noch Stufe 1",
      F.abschliessen(stand, 10.0 + 4 * H - 5.0) == []
      and stand["Kriegskunst"]["stufe"] == 1, "")
check("nach genau 4 Stunden steigt Stufe 2",
      F.abschliessen(stand, 10.0 + 4 * H) == ["Kriegskunst"]
      and stand["Kriegskunst"]["stufe"] == 2, "")

abschnitt("Abbruch — Kosten verloren, Stufe steigt nicht, danach wieder startbar")
stand = F.neuer_stand()
roh = {"holz": 1000}
F.starten("Forstwirtschaft", stand, 0.0, hat_bibliothek=True, vorhandene_rohstoffe=roh)
check("Start kostet 50 Holz (1000 -> 950)", roh["holz"] == 950, str(roh["holz"]))
okab, meldab = F.abbrechen(stand, 0.5 * H, "Forstwirtschaft")
check("Abbruch gelingt", okab is True, str((okab, meldab)))
check("nach Abbruch laeuft kein Auftrag mehr",
      stand["Forstwirtschaft"]["auftrag"] is None, "")
check("nach Abbruch bleibt die Stufe 0", stand["Forstwirtschaft"]["stufe"] == 0, "")
check("die Kosten sind verloren (Holz bleibt 950)", roh["holz"] == 950, str(roh["holz"]))
check("ein spaeterer Abschluss-Versuch steigert nichts",
      F.abschliessen(stand, 100 * H) == [], "")
ok_start2, _ = F.starten("Forstwirtschaft", stand, H, hat_bibliothek=True,
                         vorhandene_rohstoffe=roh)
check("nach Abbruch ist das Gebiet wieder startbar", ok_start2 is True, "")
check("zweiter Start kostet erneut 50 Holz (950 -> 900)", roh["holz"] == 900, str(roh["holz"]))
okab2, meldab2 = F.abbrechen(stand, H, "Kriegskunst")
check("Abbruch ohne Auftrag wird abgelehnt", okab2 is False, str((okab2, meldab2)))

abschnitt("Forschungspunkte — Stufe hoch drei")
stand = F.neuer_stand(["Kriegskunst", "Baukunst"])
stand["Kriegskunst"]["stufe"] = 2
stand["Baukunst"]["stufe"] = 3
check("Stufe 2 gibt 8 Punkte", F.punkte_je_gebiet(stand)["Kriegskunst"] == 8,
      str(F.punkte_je_gebiet(stand)["Kriegskunst"]))
check("Stufe 3 gibt 27 Punkte", F.punkte_je_gebiet(stand)["Baukunst"] == 27,
      str(F.punkte_je_gebiet(stand)["Baukunst"]))
check("Summe ueber zwei Gebiete = 8 + 27 = 35", F.punkte(stand) == 35, str(F.punkte(stand)))
check("leerer Stand gibt 0 Punkte", F.punkte(F.neuer_stand(["Kriegskunst"])) == 0, "")
check("Stufe hoch drei, nicht mal drei",
      F.punkte(stand) != 2 * 3 + 3 * 3, str(F.punkte(stand)))

sys.exit(bericht())
