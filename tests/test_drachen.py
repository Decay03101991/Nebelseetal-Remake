# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['drachen', 'einheiten', 'kampf', 'welt']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import os  # importiert os fuer Pfadoperationen
import sys  # importiert sys fuer den Modulpfad
import json  # importiert json zum Schreiben temporaerer Dateien
import tempfile  # importiert tempfile fuer temporaere Dateien
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # fuegt das Testverzeichnis zum Suchpfad hinzu
from harness import abschnitt, bericht, befund, check, import_src  # importiert die Testrahmen-Funktionen
ROOT, SRC = import_src()  # importiert das src-Verzeichnis
import drachen  # importiert das zu testende Modul

abschnitt("Datendatei vollstaendig")  # markiert den ersten Testabschnitt

daten = drachen.daten()  # laedt die Original-Datendatei
pruefwerte = daten.get("pruefwerte", {})  # holt die Pruefwerte aus der Datendatei

for eintrag in daten["drachen"]:  # iteriert ueber alle Drachen in der Datendatei
    check("Pflichtfelder vorhanden", all(feld in eintrag for feld in ("id", "welt", "name", "x", "y", "verteidigung", "beute", "ware", "bild")), f"Eintrag {eintrag.get('id', '?')} hat alle Felder")  # prueft ob alle Pflichtfelder da sind
    # W-14 (Daniel 05.11.2026): statt 40 Einheiten eine echte Drachenwache; die Summe steht in den
    # Pruefwerten der Datendatei und wird hier gegen den Block "verteidigung" geprueft.
    check("Einheitensumme wie in den Pruefwerten",
          sum(eintrag["verteidigung"]["einheiten"].values()) == pruefwerte["verteidiger_summe"],
          "Summe der Einheiten von %s ist %d" % (eintrag["id"], sum(eintrag["verteidigung"]["einheiten"].values())))
    check("Beute Gold", eintrag["beute"]["gold"] == pruefwerte["beute"]["gold"], f"Gold von {eintrag['id']} stimmt")  # prueft Gold
    check("Beute Holz", eintrag["beute"]["holz"] == pruefwerte["beute"]["holz"], f"Holz von {eintrag['id']} stimmt")  # prueft Holz
    check("Beute Stein", eintrag["beute"]["stein"] == pruefwerte["beute"]["stein"], f"Stein von {eintrag['id']} stimmt")  # prueft Stein
    check("Beute Nahrung", eintrag["beute"]["nahrung"] == pruefwerte["beute"]["nahrung"], f"Nahrung von {eintrag['id']} stimmt")  # prueft Nahrung
    check("Ware Drachenschuppe", eintrag["ware"]["Drachenschuppe"] == pruefwerte["ware"]["Drachenschuppe"], f"Drachenschuppe von {eintrag['id']} stimmt")  # prueft Drachenschuppe

welten = []  # initialisiert Liste fuer Weltkennungen
for eintrag in daten["drachen"]:  # iteriert erneut ueber die Drachen
    check("Welt einmalig", eintrag["welt"] not in welten, f"Welt {eintrag['welt']} kommt nur einmal vor")  # prueft ob Welt schon vorkam
    welten.append(eintrag["welt"])  # merkt die Welt

check("Anzahl Drachen", len(daten["drachen"]) == pruefwerte["anzahl_drachen"], "Es gibt genau so viele Drachen wie vorgesehen")  # prueft die Anzahl

abschnitt("alle() und finde()")  # markiert den zweiten Abschnitt

alle_drachen = drachen.alle()  # holt alle gueltigen Drachen
check("alle() liefert genau drei Eintraege", len(alle_drachen) == len(daten["drachen"]), f"alle() liefert {len(alle_drachen)} Eintraege")  # prueft die Anzahl von alle()

for eintrag in daten["drachen"]:  # iteriert ueber die Drachen
    gefunden = drachen.finde(eintrag["welt"], eintrag["x"], eintrag["y"])  # sucht den Drachen an seiner Position
    check("finde() findet jeden", gefunden is not None and gefunden["id"] == eintrag["id"], f"finde() findet {eintrag['id']}")  # prueft ob gefunden und korrekt

abschnitt("finde() liefert None")  # markiert den dritten Abschnitt

erster = daten["drachen"][0]  # nimmt den ersten Drachen
verschiebung = pruefwerte["verschiebung"]  # holt die Verschiebung aus der Datendatei
check("falsche Welt", drachen.finde("falsche_welt", erster["x"], erster["y"]) is None, "finde() mit falscher Welt ist None")  # prueft falsche Welt
check("x + 1", drachen.finde(erster["welt"], erster["x"] + verschiebung, erster["y"]) is None, "finde() mit x+1 ist None")  # prueft x+1
check("x - 1", drachen.finde(erster["welt"], erster["x"] - verschiebung, erster["y"]) is None, "finde() mit x-1 ist None")  # prueft x-1
check("y + 1", drachen.finde(erster["welt"], erster["x"], erster["y"] + verschiebung) is None, "finde() mit y+1 ist None")  # prueft y+1
check("y - 1", drachen.finde(erster["welt"], erster["x"], erster["y"] - verschiebung) is None, "finde() mit y-1 ist None")  # prueft y-1
besiegt_ids = [erster["id"]]  # erstellt eine Liste mit der ID des ersten Drachen
check("besiegter Drache", drachen.finde(erster["welt"], erster["x"], erster["y"], besiegt=besiegt_ids) is None, "finde() ueberspringt besiegten Drachen")  # prueft ob besiegter Drache nicht gefunden wird

abschnitt("verteidiger() und die Drachenwerte statt Wall")  # vierter Abschnitt

verteidiger_dict = drachen.verteidiger(erster)  # holt das Verteidiger-dict
check("verteidiger() hat die Summe aus den Pruefwerten", sum(verteidiger_dict.values()) == pruefwerte["verteidiger_summe"], f"Summe ist {sum(verteidiger_dict.values())}")  # prueft Summe
check("mehr als 40 Verteidiger (Daniel 05.11.2026)", sum(verteidiger_dict.values()) > 40, f"Summe ist {sum(verteidiger_dict.values())}")  # prueft die Vorgabe
fuss, bel = drachen.schwellen(erster)  # holt die beiden Vorrunden-Schwellen
check("Schwelle Fusstruppen wie in den Pruefwerten", fuss == pruefwerte["schwelle_fussttruppen"], f"Fussttruppen {fuss}")  # prueft die Schwelle
check("Schwelle Belagerung wie in den Pruefwerten", bel == pruefwerte["schwelle_belagerungswaffen"], f"Belagerung {bel}")  # prueft die Schwelle
check("der Drache ist UNBRECHBAR (kein Wallschaden)", drachen.unbrechbar(erster) is True, "unbrechbar")  # prueft die Eigenart
check("kein wall_stufe mehr im Eintrag", "wall_stufe" not in erster, "kein Wallfeld")  # prueft den Schnitt

abschnitt("Feueratem: Verluste vor dem Kampf")  # eigener Abschnitt

atem = drachen.feueratem(erster)  # Regel des Atems
check("der Atem ist eingetragen", bool(atem) and "prozent_der_fusstruppen" in atem, str(atem))  # prueft die Regel
_prozent = atem.get("prozent_der_fusstruppen", 0)  # Anteil aus der Datendatei
check("100 Fusstruppen verlieren den eingetragenen Anteil",
      drachen.feueratem_verluste(erster, 100) == int(round(100 * _prozent / 100.0)), str(drachen.feueratem_verluste(erster, 100)))  # prueft die Rechnung
check("0 Fusstruppen verlieren nichts", drachen.feueratem_verluste(erster, 0) == 0, "0")  # Grenzfall unten
check("negative Angabe verliert nichts", drachen.feueratem_verluste(erster, -5) == 0, "-5")  # Grenzfall negativ
check("Text statt Zahl verliert nichts", drachen.feueratem_verluste(erster, "viele") == 0, "Text")  # Robustheit
check("nie mehr als die Haelfte der Truppe",
      drachen.feueratem_verluste(erster, 10) <= 5, str(drachen.feueratem_verluste(erster, 10)))  # Obergrenze
check("mindestens die Untergrenze, wenn Truppen da sind",
      drachen.feueratem_verluste(erster, 100000) >= int(atem.get("mindestens", 0)), "Untergrenze")  # Untergrenze

abschnitt("figur()")  # markiert den fuenften Abschnitt
figur_drache = drachen.figur(erster)  # erzeugt Figur fuer freien Drachen
check("freier Drache art=drache", figur_drache["art"] == "drache", f"art = {figur_drache['art']}")  # prueft art
check("Drachenbild korrekt", figur_drache["bild"] == daten["figur"]["bild"], "Bildpfad stimmt")  # prueft bild
check("Drache kein Platzhalter", figur_drache["platzhalter"] == False, "platzhalter ist False")  # prueft platzhalter
figur_ruine = drachen.figur(erster, besiegt=[erster["id"]])  # erzeugt Figur fuer besiegten Drachen
check("besiegter Drache art=ruine", figur_ruine["art"] == "ruine", f"art = {figur_ruine['art']}")  # prueft art
check("Ruinenbild korrekt", figur_ruine["bild"] == daten["figur"]["ruine_bild"], "Ruinenbildpfad stimmt")  # prueft bild
check("Ruine platzhalter true", figur_ruine["platzhalter"] == daten["figur"]["ruine_platzhalter"], "platzhalter ist True")  # prueft platzhalter

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:  # erstellt eine temporaere Datei
    modifizierte_daten = daten.copy()  # kopiert die Originaldaten
    modifizierte_daten["figur"] = modifizierte_daten["figur"].copy()  # kopiert die Figuren-Konfiguration
    modifizierte_daten["figur"]["ruine_bild"] = ""  # setzt das Ruinenbild auf leer
    json.dump(modifizierte_daten, tmp)  # schreibt die modifizierten Daten in die Datei
    tmp_pfad = tmp.name  # merkt den Pfad der temporaeren Datei
try:  # versuche den Test mit fehlendem Bild
    figur_ohne_bild = drachen.figur(erster, besiegt=[erster["id"]], pfad=tmp_pfad)  # erzeugt Figur mit modifizierter Datendatei
    check("fehlendes Ruinenbild -> platzhalter True", figur_ohne_bild["platzhalter"] == True, "platzhalter ist True bei leerem Bild")  # prueft platzhalter
finally:  # stelle sicher, dass die Datei geloescht wird
    os.unlink(tmp_pfad)  # loescht die temporaere Datei

abschnitt("Zustand")  # markiert den sechsten Abschnitt
z = drachen.Zustand()  # erzeugt leeren Zustand
id_eins = alle_drachen[0]["id"]  # nimmt eine ID aus der Liste
check("besiegen erstmals True", z.besiegen(id_eins) == True, f"erster Aufruf von besiegen({id_eins}) ist True")  # prueft erstes besiegen
check("besiegen zweimal False", z.besiegen(id_eins) == False, f"zweiter Aufruf von besiegen({id_eins}) ist False")  # prueft zweites besiegen
daten_rundlauf = z.als_daten()  # holt das Spielstand-dict
z2 = drachen.Zustand().aus_daten(daten_rundlauf)  # erzeugt neuen Zustand aus den Daten
check("Rundlauf als_daten/aus_daten", z2.ist_besiegt(id_eins) == True, "nach Rundlauf ist ID besiegt")  # prueft Rundlauf
z3 = drachen.Zustand().aus_daten({})  # erzeugt Zustand aus leerem dict
check("alter Spielstand ohne Feld", z3.als_daten()["drachen_besiegt"] == [], "leerer Zustand bei fehlendem Feld")  # prueft leeren Zustand

abschnitt("alle_besiegt")  # markiert den siebten Abschnitt
alle_ids = [e["id"] for e in alle_drachen]  # sammelt alle IDs
z4 = drachen.Zustand()  # erzeugt neuen Zustand
for id_ in alle_ids[:2]:  # fuegt die ersten zwei IDs hinzu
    z4.besiegen(id_)  # markiert als besiegt
check("zwei von drei nicht alle besiegt", z4.alle_besiegt() == False, "alle_besiegt() ist False bei zwei")  # prueft False
z4.besiegen(alle_ids[2])  # fuegt die dritte ID hinzu
check("drei von drei alle besiegt", z4.alle_besiegt() == True, "alle_besiegt() ist True bei drei")  # prueft True

abschnitt("Robustheit")  # markiert den achten Abschnitt
kaputter_eintrag = erster.copy()  # kopiert einen gueltigen Eintrag
del kaputter_eintrag["beute"]  # entfernt das Feld beute
modifizierte_drachen = daten["drachen"] + [kaputter_eintrag]  # haengt den kaputten Eintrag an
modifizierte_daten = daten.copy()  # kopiert die Daten
modifizierte_daten["drachen"] = modifizierte_drachen  # ersetzt die Drachenliste
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:  # erstellt temporaere Datei
    json.dump(modifizierte_daten, tmp)  # schreibt die modifizierten Daten
    tmp_pfad2 = tmp.name  # merkt den Pfad
try:  # versuche alle() mit kaputtem Eintrag
    ergebnis = drachen.alle(pfad=tmp_pfad2)  # laedt die modifizierten Daten
    check("kaputter Eintrag wird uebersprungen", len(ergebnis) < len(modifizierte_drachen), f"alle() liefert {len(ergebnis)} statt {len(modifizierte_drachen)}")  # prueft ob weniger Eintraege
except Exception as e:  # falls eine Exception auftritt
    check("keine Exception", False, f"Exception: {e}")  # meldet Fehler
finally:  # stelle sicher, dass die Datei geloescht wird
    os.unlink(tmp_pfad2)  # loescht temporaere Datei

abschnitt("Beute: Anteil nach Leistung, Bonus fuer den letzten Schlag")  # Nachtrag 05.11.2026

_beute_vorrat = {"gold": 5000, "holz": 2000, "stein": 2000, "nahrung": 2000}  # Vorrat des Drachen
_halb = drachen.beute_anteil(100, 200, _beute_vorrat)  # halbe Leistung, kein letzter Schlag
check("halbe Leistung bringt den halben Vorrat", _halb.get("gold") == 2500, str(_halb))  # prueft den Anteil
check("alle Stoffe werden anteilig gebucht", set(_halb) == set(_beute_vorrat), str(sorted(_halb)))  # prueft die Stoffe
_letzter = drachen.beute_anteil(100, 200, _beute_vorrat, letzter_schlag=True)  # mit letztem Schlag
check("der letzte Schlag bekommt mehr als ohne Bonus", _letzter.get("gold", 0) > _halb.get("gold", 0), f"{_letzter.get('gold')} gegen {_halb.get('gold')}")  # prueft den Bonus
check("auch mit Bonus nie mehr als der Vorrat", all(_letzter[s] <= _beute_vorrat[s] for s in _beute_vorrat), str(_letzter))  # Obergrenze
_klein = drachen.beute_anteil(2, 200, _beute_vorrat, letzter_schlag=True)  # der getimte Billigangriff
check("zwei Resteinheiten ergeben NICHT die ganze Beute", _klein.get("gold", 0) < 5000, str(_klein))  # genau Daniels Sorge
check("ohne Leistung keine Beute", drachen.beute_anteil(0, 200, _beute_vorrat) == {}, "0 Verteidiger")  # Grenzfall
check("unbrauchbare Zahlen geben keine Beute", drachen.beute_anteil("viel", 200, _beute_vorrat) == {}, "Text")  # Robustheit
check("ohne Beute keine Beute", drachen.beute_anteil(50, 100, {}) == {}, "leer")  # Robustheit

abschnitt("Bericht: episch, aber ehrlich")  # Nachtrag 05.11.2026

_verteidiger = drachen.verteidiger(erster)  # die Wache des Drachen
_mit = drachen.bericht({"ausgang": "angreifer"}, 5, _verteidiger)  # mit Ueberlebenden
check("mit Ueberlebenden nennt der Bericht die Einheiten", any("Krieger" in z for z in _mit["zeilen"]), str(_mit["zeilen"]))  # aufgeklaert
check("der Bericht hat eine Ueberschrift aus der Datendatei", bool(_mit["titel"]), _mit["titel"])  # Titel
check("der Bericht hat den Typ kampf", _mit.get("typ") == "kampf", str(_mit.get("typ")))  # Typ
_ohne = drachen.bericht({"ausgang": "verteidiger"}, 0, _verteidiger)  # niemand kam zurueck
check("ohne Ueberlebende nennt der Bericht KEINE Einheiten", not any("Krieger" in z or "Paladin" in z for z in _ohne["zeilen"]), str(_ohne["zeilen"]))  # genau Daniels Regel
check("ohne Ueberlebende nennt der Bericht die ZAHL der Verteidiger", any(str(sum(_verteidiger.values())) in z for z in _ohne["zeilen"]), str(_ohne["zeilen"]))  # die Zahl bleibt
check("ohne Ueberlebende gibt es einen ehrlichen Zusatz", len(_ohne["zeilen"]) >= 2, str(_ohne["zeilen"]))  # Zusatz aus den Daten

abschnitt("Kein Ausspaehen, klarer Hinweis")  # Nachtrag 05.11.2026

_erlaubt, _grund = drachen.spionage_erlaubt()  # Regel aus der Datendatei
check("Drachen lassen sich NICHT ausspaehen", _erlaubt is False, str(_erlaubt))  # Daniels Regel
check("der Grund steht in der Datendatei", bool(_grund), _grund[:60])  # kein Code-Text
check("der Angriffshinweis fuer den Spieler ist da", bool(drachen.angriffs_hinweis()), drachen.angriffs_hinweis()[:60])  # Hinweis

abschnitt("Transport: Karren fuer den Anteil (Daniel 05.11.2026)")  # Nachtrag

_voll = drachen.transport_bedarf({"gold": 5000, "holz": 2000, "stein": 2000, "nahrung": 2000})  # 11.000 Ladung
check("die noetige Ladung ist die Summe der Beute", _voll["ladung"] == 11000, str(_voll["ladung"]))  # Summe
check("der Wagenpark traegt die ganze Ladung (kein Rest)", _voll["rest"] == 0, str(_voll["rest"]))  # kein Rest
check("der Wagenpark nennt Karren aus dem Spiel", all(k in ("Handkarren", "Einsp\u00e4nner", "Zweisp\u00e4nner", "Handelskarawane", "Gro\u00dfe Handelskarawane") for k in _voll["karren"]), str(sorted(_voll["karren"])))  # bekannte Namen
# Tragfaehigkeit nachrechnen: die genannten Karren MUESSEN die Ladung tragen
import einheiten as _E  # Einheitenmodul fuer die Ladung
_trag = _E.ladung_der_gruppe(_voll["karren"])  # Kapazitaet des Vorschlags
check("die genannten Karren tragen mindestens die Ladung", _trag >= _voll["ladung"], f"{_trag} gegen {_voll['ladung']}")  # Nachrechnung
_halb = drachen.transport_bedarf({"gold": 2500})  # kleine Beute
check("kleine Beute braucht wenige Karren", sum(_halb["karren"].values()) <= 2, str(_halb))  # Verhaeltnis
check("unbrauchbare Beute braucht keine Karren", drachen.transport_bedarf("kaputt")["ladung"] == 0, "Text")  # Robustheit
_txt = drachen.transport_text({"gold": 2500})  # der Satz fuer den Spieler
check("der Transportsatz nennt die Ladung", "2500" in _txt, _txt[:80])  # Klartext
check("der Transportsatz nennt Karren", "Karren" in _txt or "Handelskarawane" in _txt or "Zweisp\u00e4nner" in _txt, _txt[-80:])  # Klartext
check("der Transportsatz hat keinen Platzhalter mehr", "{" not in _txt, _txt)  # eingesetzt

sys.exit(bericht())  # beendet den Testlauf und gibt den Bericht aus
