# AUFTRAG: Spielspannung, Spielschleife und Bot-Taktik (01.11.2026)

Du bist **Spielarchitekt und Prüfer**, nicht Ausführender. Du entwirfst und begründest — du baust
nichts, du startest kein Spiel, du committest nicht.

## 0. Deine Rolle und die harten Grenzen

* **Erlaubt:** Dateien im Projekt `D:\Arbeiten\Nebelseetal_Remake` **lesen**; genau **eine** Datei
  schreiben: `docs/design/SPIELSPANNUNG_UND_BOTTAKTIK_20261101.md`.
* **Verboten:** jede andere Datei ändern, löschen, verschieben; `git` irgendeines Befehls benutzen;
  Tests oder das Spiel starten; Zahlen erfinden, die als Originalwert auftreten.
* **Sprache:** Deutsch. **Anführungszeichen paarig** („“), nie ein gerades Zeichen allein — eine
  Prüfdatei zählt sie sonst und wird rot.

## 1. Daniels Vorgabe — wörtlich

> „…um die jetzt doch sehr komplexen mechaniken zu konsistenten spielabläufen führt und ein spielen
> dadurch diesen gewissen reiz und spannung entwickelt. Dabei liegt viel auch daran was die bots
> abliefern wie kreativ sie jeweils auf den spieler wirken mit ihren taktiken und verhaltensweisen.
> Da ich keine ki dafür habe sozusagen wird das noch eine riesen aufgabe sein vermute ich.“

Zerlegt heißt das **drei** Aufgaben:

1. **Konsistenz:** die vielen Einzelmechaniken sollen zu *einem* verständlichen Ablauf werden, in dem
   jede Handlung eine erkennbare Folge hat (kein Nebeneinander von Sonderfällen).
2. **Spannung:** der Ablauf soll Zugzwang, Risiko und Belohnung erzeugen — Angst um etwas, Vorfreude
   auf etwas, Entscheidungen mit Preis.
3. **Bots als Gegenspieler:** sie sollen *auf den Spieler wirken*, als hätten sie Absichten, Taktik und
   Charakter — ohne echte KI, also über Regeln, Zustände, sichtbare Signale und Gedächtnis.

## 2. Bindende Entscheidungen (Daniel, 01.11.2026 — nicht in Frage stellen, nur umsetzen)

| Punkt | Entscheidung |
|---|---|
| Reiseort | **Der Tempel** ist der Reiseort; er steht ab Gründung (der Siedlungskarren bringt ihn mit) |
| Reisen erlaubt | **sobald der Götterschutz verlassen ist** (kein Tempelausbau, keine Forschung) |
| Weltkarte | **entfällt**; der Menüpunkt heißt künftig **Dorfzentrum** (Lagerverwaltung, Werkstätten, Bestände) |
| Weltbild im Portal | Geländekästchen der alten Legende **ohne Gebäude und Zeichen**; Felder anwählbar; eigene Dörfer transferierbar; **Gegner sichtbar**; Hover zeigt nach ein paar Sekunden die Kosten |
| Bezahlung Transfer | ein simulierter **Herold-Trupp** holt die Kosten ab (kostet keine Zeit), **Postfach-Nachricht** bestätigt die neue Koordinate |
| Lager | **ein Lager je Dorf**; Dorfzentrum ist Menüpunkt **und** Lagergebäude |
| Umzug | Dorf reist mit allem; laufende Aufträge werden **neu gerechnet**; **Weltwechsel gesperrt**, solange etwas unterwegs ist (auch Handel) |
| Forschung | ohne Bibliothek **Stufe 0** vor Ort; mit Bibliothek **Verbundstand** übernehmen und übertreffen |
| Einheiten | ein Dorf baut erst, wenn **seine** Akademie die Verbundsstufe erreicht; Stationieren überall erlaubt; **stationierte Truppen verteidigen mit** |
| Startressourcen | je Dorf 10 Siedler, 100 Holz, 100 Stein |
| Mana | **neu kalkulieren** (Originalwerte nur Richtwerte), Einbau als VORSCHLAG, Feineinstellung im Spieltest |
| Dörfer | **sechs** eigene Siedlungen, Aufteilung z. B. drei verteidigen / drei angreifen |
| Bots | feste **Koordinaten**, **eigene Dörfer**, **eine von mehreren Taktiken** (Nähe suchen, Abstand halten, angreifen) |

## 3. Gemessener Ist-Zustand (aus Werkzeugen, nicht aus dem Kopf — bitte gegenprüfen, nicht blind glauben)

| Gegenstand | Stand | Belegstelle |
|---|---|---|
| Angriff | **zwei Wege**: `_angriff_durchfuehren` (ohne Reisezeit, sofort) und `_auftrag_angriff` (mit Reisezeit, Rückkehr, Bericht) | `src/main.py:6215`, `src/main.py:6502` |
| Aufrufer Sofortangriff | `_attack(bot)` (Diplomatie-Knopf) und `_attack_map(map_id)` | `src/main.py:6472`, `src/main.py:6274` |
| Reisezeit | `auftraege.reisezeit_sekunden(entfernung, geschwindigkeit)`, Formel als VORSCHLAG gekennzeichnet | `src/auftraege.py:146` |
| Auftragsarten | u. a. `angreifen`, `stationieren`, `handeln` | `src/auftraege.py`, `auftragsarten()` |
| Entfernung heute | **geschätzt**: Bot-Siedlungen haben keine Koordinaten, es gilt die Kartenmitte | `src/main.py:_auftrag_entfernung` |
| Bot-Verhalten | reine Logik in `botkern.py`: `aggression`, `trading` (0…1), Angriffsprüfung alle 6–24 h (VORSCHLAG), Beute 50 % gedeckelt durch Karrenlast; **keine** Koordinaten, **keine** eigenen Dörfer, **keine** Taktik | `src/botkern.py` (Docstring) |
| Karten | `MAPS` mit Größen 20 / 8 / 8 / 7 / 10 Feldern, je Karte eigenes Gelände | `src/main.py:645` |
| Portalritual | Koordinatenwechsel belegt: **5.000 Mana, 1× je 24 h, eine Siedlung** — vorhanden, aber im Spiel nicht erreichbar | `src/portalraum.py` |
| Tempel | erzeugt Mana: Nebelsee 5/h, sonst 1/h (Originalwerte) | `data/buildings.json` → `gebaeude[].id == "tempel"` |
| Einheiten | 28 Originaleinheiten mit LE/AT/PA/SI/HE/RS/TP/GS/MU/SK und Kosten | `data/units.json` |
| Götterschutz | `noob_protection` als Schalter, Ende an einer Grenze im Code | `src/main.py:193`, `:2775-2783` |
| Prüfstand | 110 Prüfdateien, 4.022 Prüfungen, voller Sammellauf ~6 min | `tools/sammellauf.py`, `docs/audits/` |

**Wichtig:** Prüfdateien sind **ASCII-only**. Wenn du eine Prüfdatei vorschlägst, muss ihr Name
wirklich in `tests/` existieren (`ls tests/`) — erfundene Prüfnamen sind ein Fehler.

## 4. Was du liefern sollst — Gliederung A…H

Schreibe die Ergebnisdatei mit **genau diesen Abschnitten**:

**A. Befund in fünf Sätzen.** Was heute fehlt, damit Spannung entsteht. Keine Allgemeinplätze:
nenne Mechanik, Datei und die Folge für den Spieler.

**B. Die Spielschleife als Tabelle.** Eine Zeile je Schleife (Tages-/Stunden-/Kampf-/Ausbau-/
Forschungs-/Handels-/Reise-Schleife): `Schleife | Takt (Spielzeit) | Entscheidung des Spielers |
Einsatz/Risiko | Belohnung | woran der Spieler merkt, dass es läuft | Datei/Funktion, die das heute trägt`.
Ziel: **jede** Schleife hat eine Entscheidung mit Preis und eine sichtbare Folge.

**C. Die sieben Spannungsquellen — je mit Einbauort.** Für jede Quelle: was genau gebaut wird, welche
Zahl (als `[VORSCHLAG: …]` mit Ableitung), welche Datei/Funktion, wie der Spieler sie *sieht*, und
welche Prüfdatei sie absichert. Denke an: Verlustangst (was kann ich verlieren), Zeitdruck (was
läuft ab), unvollständige Information (was weiß ich nicht), knappe Mittel (Güter gegen Sicherheit),
Wahl mit Preis (angreifen *oder* verteidigen), Überraschung (was passiert unerwartet), Fortschritt
mit Rückschlag (was kann ich wieder verlieren). Erfinde keine achtel Quelle — sieben reichen.

**D. Bot-Taktik ohne KI — das Kernstück.** Entwirf ein Verhaltensmodell, das *billig zu rechnen*
(Thinkpad-Klasse, eine Prüfung je Bot und Spielminute, keine Pfadsuche über 400 Felder) und *für den
Spieler lesbar* ist:
   * **Zustände** (z. B. Sammeln, Wachsen, Sichern, Suchen, Marschieren, Räubern, Fliehen, Rächen) mit
     Übergangsbedingungen als Zahlen.
   * **Drei bis fünf Taktiken** (Persönlichkeiten) mit je eigenen Schwellen — so, dass zwei Bots
     desselben Zustands unterschiedlich handeln.
   * **Gedächtnis** je Bot: was er sich merkt (wer ihn geschlagen hat, wo er Beute verlor, wie stark
     der Spieler zuletzt war) und wie das sein Verhalten ändert.
   * **Sichtbare Signale**: was der Spieler von einem Bot *merkt*, bevor er angreift (Späher, Rauch,
     Nachricht, Bewegung im Weltbild) — Spannung entsteht aus Ankündigung, nicht aus dem Überfall.
   * **Koordinaten und eigene Dörfer**: wie ein Bot seine 1–3 Dörfer wählt (Nähe suchen, Abstand
     halten) und wie er zwischen ihnen Truppen verschiebt.
   * **Rechnung**: Aufwand je Bot und Spielminute (Rechenoperationen, nicht Millisekunden raten) und
     wie viele Bots die Oberfläche bei 6 eigenen Dörfern noch flüssig trägt.
   * Tabellenform: `Taktik | Startzustand | Schwelle zum Angriff | Schwelle zum Rückzug | Zielwahl |
     was der Spieler zuerst merkt | Gegenmaßnahme des Spielers`.

**E. Die Rechnung.** Rechne die tragenden Zahlen selbst nach und lege die Rechnung offen (Formel +
Werte + Ergebnis, keine Behauptung): Tempel-Manazeit bis zu einem Transfer (5.000 Mana), Reisezeit
über 20 Felder bei Geschwindigkeit 5 und 25, Aufbauzeit eines Zweitdorfs mit 10 Siedlern/100 Holz/100
Stein bis zur ersten Bibliothek, Beutemenge gegen Karrenlast, und wie lange ein Spieler unter
Götterschutz braucht, bevor die erste Reise möglich ist. Kennzeichne jedes Ergebnis `[GERECHNET]`.

**F. Konsistenzprüfung — die Widersprüche.** Tabelle `Widerspruch | Datei:Zeile | warum es weh tut |
Vorschlag zur Auflösung | betroffene Prüfdatei`. Suche mindestens sechs, auch unbequeme (zwei
Kampfwege, Koordinaten fehlen, Weltkarte gegen Portal, Lager je Dorf gegen bestehende Teststände,
Mana-Erzeugung gegen Transferkosten, Götterschutz gegen Reisefreigabe).

**G. Top 10 nach Wirkung je Aufwand.** Tabelle `Rang | Maßnahme | Wirkung auf Spannung (1–5) |
Aufwand S/M/L | betroffene Dateien | Prüfdatei | Risiko`. Reihenfolge so, dass **jeder Schritt einzeln
spielbar bleibt**. Danach ein kurzer Abschnitt „“ mit Begründung.

**H. Was du nicht belegen kannst.** Liste: jede Stelle, an der die Quellen (Handbuch, Code) schweigen
und dein Vorschlag reine Design-Entscheidung ist. Diese Liste ist Pflicht — sie trennt Originaltreue
von Erfindung und wird von Daniel gelesen.

## 5. Form

* Höchstens **1.000 Zeilen**, Tabellen statt Fließtext, keine Wiederholung der Vorgabe.
* Jede Zahl trägt **eine** Kennzeichnung: `[BELEGT: quelle]`, `[GERECHNET: formel]` oder
  `[VORSCHLAG: ableitung]`. Eine nackte Zahl ohne Kennzeichnung ist ein Fehler.
* Kein Code-Block über 15 Zeilen. Signaturen und drei bis fünf Kernzeilen genügen.
* Am Ende: **eine** Zeile `FERTIG <Zeilenzahl>`.

## 6. Fertig-Definition

Die Datei existiert, hat die Abschnitte A–H, jede Zeile der Tabellen B und F nennt eine Datei oder
Funktion, die es wirklich gibt, und die Rechnung in E ist nachvollziehbar. Antworte am Ende **nur**
mit `FERTIG <Zeilenzahl>`.
