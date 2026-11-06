# Abarbeitungsplan Gemini-Antworten (06.11.2026)

**Grundlage:** Daniels Reihenfolge (Frage 1 der Runde 1), seine Antworten der Runde 2
(`docs/ENTSCHEIDUNGEN_DANIEL_20261106_GEMINI_ANTWORTEN.md`) und der Pruefvermerk
(`docs/PRUEFVERMERK_GEMINI_ANTWORTEN_20261106.md`).
**Regel fuer JEDEN Schritt:** die sieben Phasen aus `docs/ENTWICKLUNGSABLAUF_AB_20261105.md` -
aufnehmen, messen, Zielbild, entscheiden, Paket (Datei und alt -> neu), einbauen, pruefen, ausliefern.
Kein Schritt gilt als fertig ohne Registerzeile, Protokollzeile, Stand-Block, vollen Sammellauf,
Commit und Push. **Keine Zahl aus einer Gemini-Antwort wird uebernommen** - alle Zahlen werden aus
unseren Daten gerechnet und Daniel vor dem Einbau vorgelegt.

## S0 - Vorarbeiten: fuenf gerechnete Tabellen (VOR jedem Bau)

Diese Vorlage ist Pflicht, weil Daniel zu jeder Zahl gefragt hat, wo sie herkommt. Ergebnis je Tabelle:
eine Datei unter `docs/` mit Rechenweg, Messwerten und dem Urteil BELEGT / ABGELEITET / VORSCHLAG.

| Nr. | Tabelle | Quelle der Rechnung | blockiert |
|---|---|---|---|
| V-1 | Reparaturpreis je Wallstufe (Holz und Stein je Prozentpunkt, 1 bis 10) und Dauer je Prozentpunkt | `data/baupreise.json` (16/16) plus Stufenliste `data/buildings.json`; Spieluhrfaktor 180 | S2 |
| V-2 | Heilungspreis je Einheit (75 Prozent aller Kostenposten, ohne Ausruestung) und Heilungsdauer (50 Prozent von `dauer_je`) | `data/units.json` `kosten`/`waren`; `spieloekonomie.ausbildung_grenzen` | S3 |
| V-3 | Ruhm-Raenge: Schwellen aus unseren Punktzahlen | die vier Spieltest-Laeufe (19 bis 40 Punkte nach 8 bis 12 Tagen), `punkte.auszeichnungen` | S1 (nur der Rangname; der Balken laeuft auch ohne) |
| V-4 | Ereigniszahlen der Diplomatie (Tribut, Werkzeuge gegen Eisen, Informationspreis) | Tagesproduktion eines mittleren Dorfes (`wirtschaft`/`gelaende`), Warenwerte | S4 |
| V-5 | Rache-Angriffsschwelle (Schlagkraft) | `bot_angriffsplanung.schlagkraft` gegen eine mittlere Verteidigung | S4 |

**Fertig-Kriterium S0:** fuenf Tabellen liegen, jede Zahl hat einen Rechenweg, Daniel hat sie
abgenickt oder korrigiert. Erst danach beginnt S1.

## S1 - Postfach (Filter, Archiv, Ablauf) und Ruhm-Balken

**Messlage heute (belegt):** `_render_messages` zeigt nur die letzten 20 Eintraege
(`src/main.py:13379`), aeltere Nachrichten sind im Spielstand vorhanden, aber unerreichbar; es gibt
keinen Filter, kein Archiv, keinen Ablauf. `punkte.auszeichnungen` (`src/punkte.py:417`) liefert vier
Auszeichnungen, aber keinen Balken (`Progressbar` 0 Treffer).

**Paket:** drei Felder je Nachricht (`read`, `archived`, `ablauf_am` in Spielsekunden) im vorhandenen
dict; Fristen und Kategorien in `data/nachrichten.json` (NICHT als Konstanten im Code - das war
Geminis Fehler); Ablauf im Tick mit Schutz fuer Militaerberichte (`kampf`, `gesamtsieg`) und fuer
ungelesene Verlustberichte; Ansicht mit Filterzeile, Blaettern (20 je Seite) und Archiv-Umschalter;
Ruhm-Balken mit `tk.Canvas` auf der vorhandenen Rechnung, Rangnamen erst nach V-3.

**Wache:** neue Pruefdatei `tests/test_nachrichten_archiv.py` - alter Spielstand ohne Felder laedt,
Militaerbericht laeuft nie ab, Frist greift genau einmal, ungelesener Verlustbericht verschiebt sich,
Paginierung liefert 20 von 45, Balken rechnet ohne Punkte im Render.

**Fertig-Kriterium:** Wache gruen mit Gegenprobe, voller Sammellauf ohne rote Datei, Ansicht im Test
gerendert (nicht nur Logik), Register/Protokoll/Stand/Commit/Push.
**Aufbauzeit-Effekt:** keiner - reine Anzeige und Ordnung.

## S1b - Menue-Teilgeschichten (vier Texte, reine Anzeige)

**Quelle:** Geminis Vorschlaege in `docs/eingaenge/GEMINI_ANTWORTEN_20261106/Antwort_Gemini_MENUESTORIES_20261106.txt`,
geprueft in `docs/PRUEFVERMERK_GEMINI_MENUESTORIES_20261106.md`.

**Was gebaut wird:** vier kurze Texte, die an einen Menuepunkt gebunden sind - Forschung (erste
Bibliothek), Portal (erster Weltwechsel, als Overlay), Kaserne (Kriegerakademie fertig), Ruhmeshalle
(erstes Oeffnen). **Alle Texte werden von uns neu geschrieben**, weil Geminis Ton dem in
`data/story.json` festgelegten Ton widerspricht (dort woertlich: abenteuerlich und leicht, kein Pathos).

**Paket:** neuer Bereich in `data/story.json` plus eine Lesestelle in `src/story.py` (kein Text im
Code); je Story ein Einmal-Kennzeichen IM SPIELSTAND (nicht in der Merkdatei, sonst sieht ein zweiter
Spielstand die Geschichte nie) mit `.get`-Fallback; Anzeige in der jeweiligen Rendering-Funktion, das
Portal-Overlay ueber die vorhandene Overlay-Technik.

**Nicht dabei:** die Diplomatie-Geschichte (Haust unter Gunst 40) - sie braucht Gunst, also S4, und
wird dort zu einer reinen Bot-Stimme ohne Antwortknoepfe. Antwortknoepfe ohne Mechanik gibt es nicht.

**Wache:** `tests/test_story_menue.py` - jede Story erscheint genau einmal je Spielstand, alter
Spielstand ohne Kennzeichen laedt und zeigt die Story nach, kein Text steht im Code (Quellwache wie
bei `test_story`), leerer Text faellt auf nichts zurueck statt zu werfen.

**Fertig-Kriterium:** wie S1; Aufbauzeit-Effekt: keiner.

## S2 - Mauerreparatur

**Vorbedingung:** V-1 abgenickt.
**Messlage heute:** Wall = Stufe + Zustand in Prozent (`dorfwall.zustand`), Schaden nur in
`kampf.fuehre_schlacht`, Luecke dokumentiert in `src/kampfbericht.py:566`; 0 Wallschaden in den
bisherigen Laeufen (beurteilbar erst mit A3).
**Paket:** zwei Felder an `Settlement` (Reparaturziel in Prozent, Fertig-Zeitpunkt) - **nicht** als
dict-Zugriff (Geminis Fehler); Rohstoffe werden beim Start atomar gebucht; Zustand steigt im Tick;
`kampf.fuehre_schlacht` bricht eine laufende Reparatur ab; Sperre zwischen Reparatur und Ausbau;
Anzeige nennt alle fehlenden Bedingungen einzeln mit dem naechsten Schritt.
**Wache:** `tests/test_mauerreparatur.py` - Gegenprobe bei 100 Prozent, Kostenbucht genau einmal,
Abbruch bei Angriff, kein negativer Bestand, Stufe 0 meldet ehrlich.
**Fertig-Kriterium:** wie S1, zusaetzlich `test_gpt_wall_bot_kampf` und `test_drachen` unveraendert
gruen (die Schlacht darf sich nicht anders verhalten, wenn nichts repariert wird).

## S3 - Verwundetenheilung

**Vorbedingung:** V-2 abgenickt.
**Messlage heute:** Heilung existiert nicht; `Heilkunde` ist Siedlerproduktion +10 Prozent je Stufe
(`forschung_wirkung.py:15`); Verluste sind endgueltig; Warteschlange heisst `ausbildung` (Liste mit
`einheit`, `gebaeude`, `start`, `ende`, `dauer_sekunden`, `stufe`, `gebucht`).
**Paket:** Verwundete als Feld an `Settlement`; Entstehung in `kampf.fuehre_schlacht` VOR der
Verlustbuchung, 30 Prozent je Einheitentyp, abgerundet; Heilung in der vorhandenen Warteschlange mit
Kennzeichen; Kosten 75 Prozent aller Kostenposten der Einheit, keine Ausruestung (Daniel, Frage 6);
Dauer 50 Prozent von `dauer_je`; Anzeige in der Kaserne mit allen Bedingungen.
**Wache:** `tests/test_verwundete.py` - ohne Verluste keine Verwundeten, 30 Prozent korrekt gerundet,
ohne Kosten keine Heilung und keine Buchung, Heilung landet nach der Dauer in der Armee, alter
Spielstand laedt.
**Fertig-Kriterium:** wie S1; zusaetzlich muss `test_spielschicht` und die Kette ohne Cheats gruen
bleiben (die Verlustbuchung darf sich nicht verschieben).

## S4 - Diplomatie mit Gunst, Vertraegen, Rachetopf und Events

**Vorbedingung:** V-4 und V-5 abgenickt; S1 bis S3 fertig (die Anzeige baut auf dem Postfach auf).
**Messlage heute:** die Ansicht zeigt zwei Kennzahlen je Bot (`src/main.py:13135`); Vertraege gibt es
nicht; das Bot-Gedaechtnis existiert (`bottaktik.py:345/483/566`); Overlays sind vorhanden (35 Stellen).
**Paket in drei Teilen (jeder Teil ein eigener Commit mit vollem Lauf):**
1. **Gunst und Status** im Bot (ueber `bot_als_dict`/`bot_aus_dict` mitgefuehrt - Geminis dict-Zugriff
   war falsch), Statusgrenzen 0-39/40-59/60-100, Anzeigezeile.
2. **Rachetopf** im vorhandenen Gedaechtnis, Ankuendigung bei 3, Schwelle aus V-5, Abbau bei Bot-Sieg.
3. **Vertraege und Events:** Nichtangriffspakt (ab Gunst 40, 3 Spieltage, blockiert den vorhandenen
   Angriffsweg, bricht unter Gunst 40), Durchmarschrecht (Wirkung bei uns noch zu definieren),
   Handelsabkommen (Rabatt ueber `spieloekonomie.handel_start`, nicht in der Anzeige); drei Ereignisse
   mit Zwei-Spieltage-Frist ueber die Overlay-Technik, Zahlen aus V-4.
**Wache:** `tests/test_diplomatie.py` - ohne Gunst kein Vertrag, Bruch kostet genau 20, NAP blockiert
den Bot-Angriff, Rache steigt und faellt wie entschieden, Ereignis mit Frist laeuft ab, alter
Spielstand laedt.
**Offene Frage in diesem Schritt:** was das Durchmarschrecht bei uns mechanisch bedeutet (es gibt keine
Bot-Gebiete, nur Dimensionen).

## S5 - Siedlungsumzug

**Vorbedingung:** Preis gerechnet und abgenickt (Daniel, Frage 8: Gebaeude ziehen MIT um, dafuer teurer).
**Messlage heute:** Gruenden, Kartenziehen (`originalkarten.zufalls_originalkarte`), Aufgeben erst ab
sechs Siedlungen, Weltensprung gesperrt solange Auftraege unterwegs sind (`main.py:10857`); Siedler
sind `Settlement.bevoelkerung`, NICHT `vorraete["siedler"]`; `welt.portalkosten` rechnet zwischen
DIMENSIONEN, nicht aus Koordinaten.
**Paket:** Umzugsmethode in `GameState`; neue Zielkarte zufaellig, alte Karte zurueck in den Vorrat;
Gebaeude und Stufen ziehen mit (Daniels Entscheidung, gegen Geminis Verlust-Variante); Sperren ueber
die vorhandene Zaehlfunktion; Rueckfrage mit Preis und Kartenvorschau; Siedler aus `bevoelkerung`.
**Wache:** `tests/test_siedlungsumzug.py` - zu wenig Siedler, laufende Auftraege sperren, alte Karte
wieder verfuegbar, Vorraete genau einmal gebucht, Gebaeude unveraendert mitgezogen.

## Gesperrt bis auf Weiteres

| Stueck | Grund |
|---|---|
| **B-6 Etappen-Reise** | verlaengert Reisen; erst die A2-Messpflicht-Tabelle, dann Daniels Entscheidung |
| **A1b Spieltest-Werkzeug** | nach S1 bis S5 oder frueher, wenn Daniel die Reihenfolge dreht |
| **A2 Messpflicht-Tabelle** | Vorbedingung fuer B-6 und fuer jede Aufbauzeit-Aenderung |
| **A3 Kampf gegen ein echtes Bot-Dorf** | ohne A3 bleibt die Mauerreparatur nicht beurteilbar |

## Querschnittsregeln fuer alle fuenf Schritte

1. **Ein Schnitt, ein Commit, ein voller Sammellauf** - nie zwei Stuecke in einem Commit.
2. **Alte Spielstaende laden ohne Migration** (`.get` mit Standardwert); fehlende Schluessel werden
   HOECHSTENS gemeldet, nie still geschrieben (Geminis Vorschlag D richtig gedacht, falsch geloest).
3. **Anzeige und Kern lesen dieselbe Funktion** (F-04-Muster) - besonders bei Kosten, Sperren, Gunst.
4. **Rundung und Deckel:** jede Groesse, die Ressourcen oder Einheiten beruehrt, wird mit `int()` oder
   `math.floor()` gedeckelt und nie negativ (Geminis Vorschlag C, unsere Regel).
5. **Kein neues Modul fuer eine geloeste Aufgabe;** waechst eine Datei ueber die Komfortgrenze, wird
   reine Rechnung in die vorhandene Fachdatei gezogen - kein Umbau der Oberflaeche.
6. **Modell-Auftraege bekommen nur die noetigen Signaturen** (Geminis Vorschlag A, als erzeugtes
   Artefakt in `tools/`/Scratch, nicht als `src/`-Modul).
