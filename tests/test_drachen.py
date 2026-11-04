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
    check("Pflichtfelder vorhanden", all(feld in eintrag for feld in ("id", "welt", "name", "x", "y", "wall_stufe", "einheiten", "beute", "ware")), f"Eintrag {eintrag.get('id', '?')} hat alle Felder")  # prueft ob alle Pflichtfelder da sind
    check("Einheitensumme 40", sum(eintrag["einheiten"].values()) == pruefwerte["verteidiger_summe"], f"Summe der Einheiten von {eintrag['id']} ist {pruefwerte['verteidiger_summe']}")  # prueft die Einheitensumme
    check("Beute Gold", eintrag["beute"]["gold"] == pruefwerte["beute"]["gold"], f"Gold von {eintrag['id']} stimmt")  # prueft Gold
    check("Beute Holz", eintrag["beute"]["holz"] == pruefwerte["beute"]["holz"], f"Holz von {eintrag['id']} stimmt")  # prueft Holz
    check("Beute Stein", eintrag["beute"]["stein"] == pruefwerte["beute"]["stein"], f"Stein von {eintrag['id']} stimmt")  # prueft Stein
    check("Beute Nahrung", eintrag["beute"]["nahrung"] == pruefwerte["beute"]["nahrung"], f"Nahrung von {eintrag['id']} stimmt")  # prueft Nahrung
    check("Ware Drachenschuppe", eintrag["ware"]["drachenschuppe"] == pruefwerte["ware"]["drachenschuppe"], f"Drachenschuppe von {eintrag['id']} stimmt")  # prueft Drachenschuppe

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

abschnitt("verteidiger() und wall()")  # markiert den vierten Abschnitt
verteidiger_dict = drachen.verteidiger(erster)  # holt das Verteidiger-dict
check("verteidiger() hat 40 Einheiten", sum(verteidiger_dict.values()) == pruefwerte["verteidiger_summe"], f"Summe ist {sum(verteidiger_dict.values())}")  # prueft Summe
wall_tupel = drachen.wall(erster)  # holt das Wall-Tupel
check("wall() liefert (8, 100.0)", wall_tupel[0] == erster["wall_stufe"] and wall_tupel[1] == erster["wall_zustand"], f"wall() = {wall_tupel}")  # prueft Tupel

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

sys.exit(bericht())  # beendet den Testlauf und gibt den Bericht aus
