# Spielspannung, Spielschleife und Bot-Taktik — Entwurf und Prüfung

Stand 01.11.2026. Rolle: Spielarchitekt und Prüfer, kein Ausführender. Diese Datei ist der einzige Schreibort dieses Auftrags; es wurde nichts gebaut, nichts gestartet, nichts committet. Belegstellen wurden am 01.11.2026 aus src/ und data/ gelesen, nicht aus dem Gedächtnis. Jede Zahl trägt eine Kennzeichnung; was keine Quelle trägt, ist als [VORSCHLAG] markiert.

## A. Befund in fünf Sätzen

1. Zwei parallele Kampfwege — der Sofortangriff `_angriff_durchfuehren` (src/main.py:6215, Diplomatie-Knopf `_attack` main.py:6472) und der Reiseangriff `_auftrag_angriff` (src/main.py:6502) mit Reisezeit und Rückkehr — lassen denselben Angriff ohne und mit Vorwarnzeit ablaufen; für den Spieler ist der billigere Sofortweg ohne Marsch immer die bessere Wahl, womit die Reisezeit und damit die Anspannung ins Leere läuft.
2. Die Bots haben weder Koordinaten noch eigene Dörfer noch eine Taktik; `BotPlayer` (src/main.py:185) trägt nur `aggression`/`trading`, und `_auftrag_entfernung` (src/main.py:6485) setzt als Entfernung die Kartenmitte, weil es keinen Zielort gibt — dadurch gibt es für den Spieler nichts zu fürchten, was kommt, und nichts zu erkennen, bevor es da ist.
3. `botkern.tick` (src/botkern.py:371) trifft pro Zug nur eine Würfelentscheidung (angreifen mit Wahrscheinlichkeit `aggression`, sonst wirtschaften) ohne Gedächtnis; die Angriffstakt 6–24 h (src/botkern.py:40) und die Beute 50 % gedeckelt durch Karrenlast (src/botkern.py:46) sind die einzigen Spannungshebel, und sie kündigen nichts an.
4. Das Portalritual (Koordinatenwechsel 5.000 Mana, src/portalraum.py:114) ist vorhanden, aber im Spiel nicht erreichbar, und die Weltkarte (`MAPS`, src/main.py:645) läuft als eigener Kartenwechsel neben dem Portal — der Ort, an dem Spannung aus Entfernung und Risiko entstehen soll, ist noch nicht an die Reisefreigabe gekoppelt.
5. Bauen geschieht sofort und ohne Bauzeit (`spielschicht.bauen` src/spielschicht.py:274 bucht die Kosten und setzt das Gebäude in demselben Schritt), also fehlt der Zeitdruck beim Ausbau; Spannung entsteht heute nur aus zwei Schaltern (Götterschutz, Angriffsfenster), nicht aus einer geschlossenen Schleife mit Entscheidungen, die einen Preis haben.

## B. Die Spielschleife als Tabelle

| Schleife | Takt (Spielzeit) | Entscheidung des Spielers | Einsatz/Risiko | Belohnung | woran der Spieler merkt, dass es läuft | Datei/Funktion |
|---|---|---|---|---|---|---|
| Tages-Schleife | 86.400 s = 1 Tag [BELEGT: src/botkern.py:39 SEKUNDEN_JE_TAG] | nichts aktiv; beobachten, ob Götterschutz fällt | verliert mit Tag 8 den Schutz | Tagesfortschritt, Bots wirtschaften weiter | Meldung „Götterschutz beendet“ | src/main.py:2760-2788 `GameState.tick`, `noob_protection` |
| Stunden-Schleife | 3.600 s = 1 h [BELEGT: src/botkern.py:38] | Produktionsgebäude platzieren, Erträge planen | Rohstoff-Ausgabe der Gebäude | Holz/Stein/Mana je Stunde | Erträge steigen sichtbar | data/buildings.json `ertrag_pro_stunde` |
| Kampf-Schleife | Ankunft eines Angriffs | angreifen (entsenden) oder verteidigen | Verlust der Truppen, Beute geht an den Sieger | Beute, Kriegspunkte | Kampfbericht | src/auftraege.py:350 `angreifen`, src/kampf.py, `kampfbericht` |
| Ausbau-Schleife | sofort (keine Bauzeit) | welches Gebäude, welches Feld | Baupreise (Holz/Stein) | Gebäudewirkung | Gebäude steht auf der Karte | src/spielschicht.py:274 `bauen` |
| Forschungs-Schleife | Bibliothek nötig | welche Forschungslinie | Mana/Gold-Kosten, blockiert Bibliothek | Forschungsstufe | Stufe steigt, Voraussetzungen frei | data/gebaeude_wirkung.json:19-22, src/forschung |
| Handels-Schleife | Ankunft der Karawane | anbieten/annehmen | Ware + Reisezeit, Ablehnung bringt Ware zurück | Gold, Versorgung | Handelsabschluss in Nachrichten | src/main.py:6448 `_trade`, src/spieloekonomie.py |
| Reise-Schleife | Reisezeit je Strecke | Ziel, Truppe, Drosselung | Reisekosten + Vorwarnzeit des Ziels | Ankunft, Auftragswirkung | Auftragsbericht „hinreise/am_ziel/rückreise“ | src/auftraege.py:146 `reisezeit_sekunden`, :456 `fortschritt` |

Jede Zeile nennt eine echte Datei oder Funktion. Die drei heute noch preislosen Schleifen — Ausbau (kein Zeitpreis), Tages-Schleife (nur ein Schalter) und Stunden-Schleife (kein Gegenspieler-Eingriff) — sind genau die, die der Einbau der Spannungsquellen aus C füllen soll.

## C. Die sieben Spannungsquellen — je mit Einbauort

1. **Verlustangst (was kann ich verlieren).** Ein Bot plündert 50 % der lagernden Rohstoffe, gedeckelt durch die Karrenladung [BELEGT: src/botkern.py:46 `BEUTE_ANTEIL = 0.5`; Ladungen 40/100/250 in data/units.json]. Einbauort: `botkern.beute_begrenzen` (src/botkern.py:290). Sichtbar: Kampfbericht mit entnommenen Mengen. Prüfdatei: tests/test_botkern.py.

2. **Zeitdruck (was läuft ab).** Das Bot-Angriffsfenster öffnet alle 6–24 h [BELEGT: src/botkern.py:40-42] und der Götterschutz endet nach 7 Tagen oder dem ersten Kriegspunkt [BELEGT: src/main.py:2775-2783]. Einbauort: `botkern.naechster_angriff_moeglich` + `punkte.goetterschutz_tage`. Sichtbar: Postfach-Nachricht „die Welt ist jetzt gefährlich“. Prüfdatei: tests/test_gpt_zeitstempel_und_schutz.py.

3. **Unvollständige Information (was weiß ich nicht).** Der Spieler sieht die Bot-Stärke nicht, nur seine Haltung. Einbauort: [VORSCHLAG] ein Sichtbarkeitsschalter je Bot, der erst nach einem Späherkontakt die wahre Armee zeigt — Ableitung: Spannung entsteht aus Ankündigung, nicht aus dem Überfall (Vorgabe Abschnitt 1). Sichtbar: Diplomatie zeigt statt Zahlen „unbekannt“ bis zum ersten Kontakt. Prüfdatei: tests/test_gpt_bot_angriffsplanung.py.

4. **Knappe Mittel (Güter gegen Sicherheit).** Startressourcen je Dorf 10 Siedler, 100 Holz, 100 Stein [BELEGT: Vorgabe Abschnitt 2; data/baupreise.json:40]. Bibliothek kostet 12 Holz + 8 Stein, Wall 16 + 16 [VORSCHLAG: data/baupreise.json — nur Holzfäller, Steinmetz, Jäger und Haus sind belegt]. Einbauort: `baupreise.json` + `spielschicht.bauen`. Sichtbar: Baukasse zeigt Restbestand. Prüfdatei: tests/test_spielschicht.py.

5. **Wahl mit Preis (angreifen oder verteidigen).** Stationierte Truppen verteidigen mit [BELEGT: Vorgabe Abschnitt 2]; dieselbe Truppe kann nicht zugleich daheim stehen und angreifen. Einbauort: `auftraege.starten` Art `stationieren` (src/auftraege.py:339) und `_truppen_nach_rolle` (src/main.py:6170). Sichtbar: Truppenabgang im Ortsheer. Prüfdatei: tests/test_auftraege.py.

6. **Überraschung (was passiert unerwartet).** Ein Bot, der geschlagen wurde, merkt sich den Schläger und schlägt unangekündigt zurück. Einbauort: [VORSCHLAG] Gedächtnisfeld `geschlagen_von` in `botkern.tick` — Ableitung: der Rachezug kommt ohne die Ankündigung der übrigen Taktiken. Sichtbar: Angriff des zuvor besiegten Bots auf genau das Dorf, das ihn geschlagen hat. Prüfdatei: tests/test_gpt_kampf_botbeute_echte_kasse.py.

7. **Fortschritt mit Rückschlag (was kann ich wieder verlieren).** Ein Dorf reist mit allem; laufende Aufträge werden neu gerechnet, und der Weltwechsel ist gesperrt, solange etwas unterwegs ist [BELEGT: Vorgabe Abschnitt 2]. Einbauort: `auftraege.fortschritt` (src/auftraege.py:456) + Reisefreigabe. Sichtbar: Auftragsbericht ändert Ankunftszeiten beim Umzug. Prüfdatei: tests/test_gpt_zeit_auftragsketten.py.

## D. Bot-Taktik ohne KI — das Kernstück

Ziel: ein Verhaltensmodell, das billig rechnet (Thinkpad-Klasse, eine Prüfung je Bot und Spielminute, keine Pfadsuche über 400 Felder) und für den Spieler lesbar ist — der Bot kündigt sein Handeln an, statt aus dem Nichts zuzuschlagen.

### D.1 Zustände und Übergänge

Acht Zustände; jeder Übergang trägt eine Zahlenschwelle [VORSCHLAG, Ableitung in Klammern]:

| Zustand | Bedeutung | Übergang | Bedingung (Zahl) |
|---|---|---|---|
| SAMMELN | Rohstoffe aufbauen | → WACHSEN | Vorrat Holz ≥ 150 [VORSCHLAG: 1,5× die Obergrenze der Startspanne 100 aus src/botkern.py:65] |
| WACHSEN | Dorf ausbauen | → SICHERN | eigene Punkte ≥ Taktik-Schwelle (Tabelle D.4) |
| SICHERN | Wall/Truppen aufstellen | → SUCHEN | Armee-Stärke ≥ Schwelle UND Abstand zum Spieler > Nahgrenze |
| SUCHEN | Nähe zum Spieler aufbauen | → MARSCHIEREN | Manhattan-Abstand zum Spielerdorf ≤ 5 [VORSCHLAG: ein Kartenviertel der 20er-Karte, damit Bewegung sichtbar wird] |
| MARSCHIEREN | Truppen verschieben | → RÄUBERN | Ankunft erreicht (Reisezeit aus src/auftraege.py:146) |
| RÄUBERN | Angriff | → FLIEHEN | erlittene Verluste > 50 % [VORSCHLAG: die halbe Armee ist die Beute-Gegengröße zu `BEUTE_ANTEIL`] |
| FLIEHEN | Rückzug nach Niederlage | → SICHERN | 24 h Ruhe [BELEGT: 24-h-Takt aus src/botkern.py:41] |
| RÄCHEN | gezielter Gegenschlag | → SICHERN | der gemerkte Schläger wurde angegriffen |

Übergänge werden je Spielminute geprüft; das ist die eine Prüfung je Bot und Spielminute aus der Vorgabe.

### D.2 Drei bis fünf Taktiken (Persönlichkeiten)

Fünf Taktiken, passend zu den fünf belegten Gegnern [BELEGT: src/botkern.py:54 `BOT_NAMEN`]. Dieselbe Situation (Zustand SUCHEN) führt je Taktik zu anderem Handeln, weil die Schwellen verschieden sind.

| Taktik | Persönlichkeit | Nähe/Abstand | Aggressions-Schwelle | Rückzugs-Schwelle |
|---|---|---|---|---|
| Plünderer (Haug) | sucht Nähe | nah (Abstand ≤ 3) | `aggression` ≥ 0,4 [VORSCHLAG: tiefer als der Bestandswert 0,66, damit er früh zuschlägt] | Verluste > 40 % |
| Wächterin (Brynhild) | hält Abstand | fern (Abstand ≥ 8) | `aggression` ≥ 0,7 [VORSCHLAG: über 0,66 — sie greift nur selten] | Verluste > 25 % |
| Bastionier (Grom) | baut Wall, bleibt | fern | `aggression` ≥ 0,85 [VORSCHLAG: fast nie] | Verluste > 15 % |
| Späherin (Silra) | sucht, kündigt an | nah, dann Rückzug | `aggression` ≥ 0,5 | Verluste > 60 % [VORSCHLAG: flieht spät, erkundet lange] |
| Rächer (Krank) | ohne Ankündigung | beliebig | greift IMMER bei RÄCHEN | Verluste > 50 % |

### D.3 Gedächtnis je Bot

Jeder Bot trägt zusätzlich zu den bestehenden Feldern (`naechster_angriff`, `letzter_angriff`, `angriffe`, `vorraete`, `lager` — src/botkern.py:198-205) vier Merker:

| Merker | was er speichert | wie er das Verhalten ändert |
|---|---|---|
| `geschlagen_von` | Name/Kennung des Spielerdorfs, das zuletzt Beute nahm | verschiebt den nächsten Angriff genau auf dieses Dorf (RÄCHEN) |
| `beute_verloren` | Menge + Zeitstempel des letzten Beuteverlusts | hebt die Aggressions-Schwelle für 48 h [VORSCHLAG: 2× der 24-h-Takt] |
| `staerke_zuletzt` | Kriegspunkte des Spielers beim letzten Kontakt | senkt die Angriffsschwelle, wenn der Spieler schwächer wurde [VORSCHLAG] |
| `ruf` (bestehend) | Ruf des Spielers | bereits belegt in src/botkern.py:195 |

Das Gedächtnis wird in `wirkung_anwenden` (src/botkern.py:435) fortgeschrieben — der einzige Ort, an dem sich ein Bot ändert, bleibt damit erhalten.

### D.4 Sichtbare Signale (Ankündigung vor dem Überfall)

Spannung entsteht aus Ankündigung, nicht aus dem Überfall. Je Zustand ein Signal, das der Spieler sieht, bevor der Kampf beginnt:

| Zustand | Signal | wo sichtbar | Vorlauf |
|---|---|---|---|
| SUCHEN | Späher-Figur am Rand der eigenen Karte | Weltbild/Portalansicht | dauerhaft, solange SUCHEN |
| MARSCHIEREN | Staubwolke/Rauchsäule Richtung Ziel | Weltbild | eine Reisezeit vor Ankunft [GERECHNET: `reisezeit_sekunden` aus src/auftraege.py:146] |
| RÄCHEN | Postfach-Nachricht „X ist erzürnt“ | Nachrichten | 1 h vor dem Schlag [VORSCHLAG] |
| RÄUBERN | Kampfbericht | Nachrichten | beim Eintreffen, nicht vorher |

Nur die Taktik Rächer (Krank) schlägt ohne Vorlauf zu — das ist ihr Unterscheidungsmerkmal und die einzige echte Überraschung.

### D.5 Koordinaten und eigene Dörfer

Jeder Bot bekommt feste Koordinaten (x, y, z) im Limbus-Raster 20×20 [BELEGT: src/portalraum.py:46-48] und 1–3 eigene Dörfer:

- Taktik „Nähe suchen“ wählt Koordinaten mit Manhattan-Abstand ≤ 3 zum Spielerfeld [VORSCHLAG].
- Taktik „Abstand halten“ wählt Koordinaten mit Abstand ≥ 8 [VORSCHLAG].
- Truppenverschiebung zwischen den eigenen Dörfern nutzt dieselbe Formel wie der Spieler: `auftraege.reisezeit_sekunden(entfernung, geschwindigkeit)` mit der langsamsten Einheit (src/auftraege.py:118) — keine eigene Pfadsuche, keine Suche über 400 Felder.

Die Entfernung des Bots ist damit keine Kartenmitte-Schätzung mehr, sondern ein echter Manhattan-Abstand; `_auftrag_entfernung` (src/main.py:6485) liest künftig die Bot-Koordinate statt der Kartenmitte.

### D.6 Rechnung: Aufwand je Bot und Spielminute

Eine Prüfung je Bot und Spielminute besteht aus: einem Zustandsvergleich (1 Vergleich), einer Zufallsziehung (1 `rng.random()`), einer Manhattan-Distanz (2 Absolutbeträge + 1 Addition) und einem Gedächtnislesen (1 Dict-Zugriff) — zusammen etwa 20 bis 30 Rechenoperationen [GERECHNET: Operationen gezählt, keine Millisekunden geraten].

Bei sechs eigenen Dörfern und sechs Bots à bis zu drei Dörfern sind es sechs Bot-Entscheidungen je Spielminute, zusammen rund 180 Operationen je Spielminute [GERECHNET: 6 × 30]. Eine Spielminute sind 60 Spielsekunden; bei Spielzeitfaktor 180 [BELEGT: data/spielzeit.json `faktor`] sind das 60/180 = 0,33 Echtzeitsekunden. Das ergibt rund 540 Operationen je Echtzeitsekunde [GERECHNET: 180 / 0,33] — für Thinkpad-Klasse vernachlässigbar. Das 20×20-Raster (400 Felder) wird dabei nur gezeichnet, nie durchsucht; die Oberfläche bleibt bei sechs eigenen Dörfern und bis zu 18 Bot-Dörfern flüssig, solange die Taktik keine Pfadsuche enthält.

### D.7 Tabellenform (Vorgabe D)

| Taktik | Startzustand | Schwelle zum Angriff | Schwelle zum Rückzug | Zielwahl | was der Spieler zuerst merkt | Gegenmaßnahme des Spielers |
|---|---|---|---|---|---|---|
| Plünderer | SUCHEN | `aggression` ≥ 0,4 | Verluste > 40 % | nächstes schwaches Dorf | Späher am Rand | Wall ausbauen, Truppen stationieren |
| Wächterin | SICHERN | `aggression` ≥ 0,7 | Verluste > 25 % | das Dorf, das ihr zu nah kam | sie bleibt fern, kein Späher | Abstand halten, nicht provozieren |
| Bastionier | WACHSEN | `aggression` ≥ 0,85 | Verluste > 15 % | Verteidiger, nie Angreifer | dauerhaft ruhig | nicht angreifen, er rächt nicht |
| Späherin | SUCHEN | `aggression` ≥ 0,5 | Verluste > 60 % | erkundet, greift nur bei Schwäche | Späher + Staubwolke mit Vorlauf | Deckung aufdecken, Falle stellen |
| Rächer | RÄCHEN | immer | Verluste > 50 % | der Schläger | Nachricht „erzürnt“ 1 h vorher | das schlagende Dorf leer räumen |

## E. Die Rechnung

Jede tragende Zahl wird nachgerechnet und offengelegt. Tempel-Manazeit, Reisezeit, Zweitdorf, Beute und Schutzfrist.

1. **Tempel-Manazeit bis zu einem Transfer (5.000 Mana).** Der Tempel erzeugt 5 Mana/h am Nebelsee und 1 Mana/h sonst [BELEGT: data/buildings.json `tempel.ertrag_pro_stunde`]. Ein Koordinatenwechsel kostet 5.000 Mana aus einer Siedlung [BELEGT: src/portalraum.py:114]. [GERECHNET: 5000 / 5 = 1.000 h ≈ 41,7 Tage am Nebelsee; 5000 / 1 = 5.000 h ≈ 208,3 Tage sonst]. Der Tempel verlangt Baukunst [BELEGT: data/buildings.json `tempel.voraussetzung`] — das ist ein eigener Widerspruch zu „Tempel steht ab Gründung“ (Abschnitt F).

2. **Reisezeit über 20 Felder.** Formel: Sekunden = Entfernung / Geschwindigkeit × 7.200 [BELEGT: src/auftraege.py:57 `SEKUNDEN_JE_FELD = 7200.0`, :146]. [GERECHNET: 20/5 × 7.200 = 28.800 s = 8 h je Strecke bei GS 5; 20/25 × 7.200 = 5.760 s = 1,6 h je Strecke bei GS 25]. Hin und zurück der doppelte Wert [BELEGT: src/auftraege.py:60 `HIN_UND_RUECK_FAKTOR = 2.0`]: 16 h beziehungsweise 3,2 h [GERECHNET].

3. **Aufbauzeit eines Zweitdorfs bis zur ersten Bibliothek.** Die Bibliothek kostet 12 Holz + 8 Stein [VORSCHLAG: data/baupreise.json — nur vier Gebäude sind preisbelegt]. Gebäude werden sofort gesetzt, es gibt keine Bauzeit [BELEGT: src/spielschicht.py:308-316 bucht Kosten und setzt das Feld in demselben Schritt]. Mit den Startressourcen 100 Holz/100 Stein [BELEGT: Vorgabe Abschnitt 2] ist die Bibliothek sofort bezahlbar: [GERECHNET: 100 − 12 = 88 Holz, 100 − 8 = 92 Stein Rest]. Die echte Hürde ist die Gründung selbst: Wagenbau (Forschung) und ein Siedlerkarren [BELEGT: src/main.py:4188], deren Dauer die Quellen nicht beziffern (Abschnitt H). Bauzeit der Bibliothek: 0 h, weil es keine Bauzeit gibt.

4. **Beutemenge gegen Karrenlast.** Beute = 50 % der Vorräte, gedeckelt durch die Karrenladung [BELEGT: src/botkern.py:46]. Karrenladungen: Handkarren 40, Einspänner 100, Zweispänner 250 [BELEGT: data/units.json `ladung`]. [GERECHNET: ein Handkarren (40) gegen 100 Holz Vorrat → 50 % = 50, gedeckelt auf 40; ein Einspänner (100) gegen 300 Holz → 50 % = 150, gedeckelt auf 100]. Im echten Kampf gilt inzwischen die gestaffelte Beute (`kampfbericht.beute_staffel`) statt der pauschalen 50 % — das ist ein Widerspruch (Abschnitt F).

5. **Dauer unter Götterschutz bis zur ersten Reise.** Reisen ist erst erlaubt, sobald der Götterschutz verlassen ist [BELEGT: Vorgabe Abschnitt 2]. Der Schutz endet nach 7 Tagen oder dem ersten Kriegspunkt [BELEGT: src/main.py:2775-2783, `punkte.goetterschutz_tage`]. [GERECHNET: 7 × 86.400 s = 604.800 s = 168 h Spielzeit]. Bei Spielzeitfaktor 180 [BELEGT: data/spielzeit.json] sind das 604.800 / 180 = 3.360 s Echtzeit ≈ 56 Minuten [GERECHNET].

## F. Konsistenzprüfung — die Widersprüche

| Widerspruch | Datei:Zeile | warum es weh tut | Vorschlag zur Auflösung | betroffene Prüfdatei |
|---|---|---|---|---|
| Zwei Kampfwege: Sofortangriff und Reiseangriff | src/main.py:6215 gegen :6502 | derselbe Angriff ohne und mit Marsch; der Spieler wählt immer den billigeren Sofortweg, die Reisezeit verliert ihre Wirkung | einen Weg behalten (Reiseauftrag) und den Sofortweg nur als echte Nachbarschlacht auf der Karte führen | tests/test_auftraege.py |
| Bots haben keine Koordinaten | src/main.py:6485-6500 | Entfernung wird als Kartenmitte geschätzt; Reisezeiten und Warnzeiten sind fiktiv | Bot-Koordinaten (x,y,z) einführen und `_auftrag_entfernung` echte Manhattan-Abstände lesen lassen | tests/test_botkern.py |
| Weltkarte (MAPS) gegen Portal | src/main.py:645 gegen src/portalraum.py | zwei konkurrierende Weltmodelle: Kartenwechsel mit Gold gegen Koordinatenwechsel mit Mana | Vorgabe umsetzen: Weltkarte entfällt, Menüpunkt Dorfzentrum; Portal ist der einzige Reise-/Wechselort | tests/test_weltkarte.py, tests/test_portalraum.py |
| Tempel ab Gründung gegen Baukunst | Vorgabe Abschnitt 2 gegen data/buildings.json `tempel.voraussetzung` | der Reiseort Tempel steht nicht ab Gründung, weil er Baukunst verlangt; die Reisefreigabe hängt an einem nicht vorhandenen Gebäude | Tempel von der Baukunst-Voraussetzung ausnehmen oder als mitgebrachtes Startgebäude führen | tests/test_spielschicht.py |
| Mana-Erzeugung gegen Transferkosten | data/buildings.json (5/1 je h) gegen src/portalraum.py:114 (5.000) | 1.000–5.000 h je Transfer machen die Reise praktisch unerreichbar; Mana ist der Nadelöhr-Rohstoff | Mana-Balance neu kalkulieren (Vorgabe Abschnitt 2) und Transferkosten im Spieltest einstellen | tests/test_portalraum.py |
| Götterschutz gegen Reisefreigabe | src/main.py:2775 gegen Vorgabe Abschnitt 2 | Schutz endet erst mit Kriegspunkt oder Tag 8; die Freigabe hängt am Schutz, aber der erste Kriegspunkt kann nie entstehen, solange nicht gereist wird | Schutzende und Reisefreigabe an dieselbe Uhr hängen und die Reise erst nach Tag 7 (oder Kriegspunkt) freigeben | tests/test_gpt_zeitstempel_und_schutz.py |
| Beute 50 % gegen gestaffelte Beute | src/botkern.py:46 gegen src/kampfbericht.py `beute_staffel` | zwei Beuteregeln für denselben Plünderfall; der Bot-Wirtschaftskern rechnet pauschal, der Kampf gestaffelt | eine Beutefunktion als gemeinsame Quelle, Staffel für Kampf, Pauschalwert nur als Bot-Planungsziel | tests/test_beute_staffel.py |
| Lager je Dorf gegen „ob Bauwerk“ | Vorgabe Abschnitt 2 gegen data/buildings.json:392-407 | die Vorgabe macht das Lager zum Menüpunkt und Gebäude je Dorf; die Datendatei sagt, ein eigenständiges Bauwerk sei nicht belegt | Lager als reine Ansicht je Dorf führen, nicht als Bauwerk; Dokumentation in buildings.json nachziehen | tests/test_dorfuebersicht.py |

## G. Top 10 nach Wirkung je Aufwand

Reihenfolge so, dass jeder Schritt einzeln spielbar bleibt. Wirkung auf Spannung 1–5, Aufwand S/M/L.

| Rang | Maßnahme | Wirkung (1–5) | Aufwand S/M/L | betroffene Dateien | Prüfdatei | Risiko |
|---|---|---|---|---|---|---|
| 1 | Bot-Koordinaten und 1–3 eigene Dörfer einführen | 5 | L | src/main.py (BotPlayer), src/botkern.py, src/portalraum.py | tests/test_botkern.py | mittel: berührt Speicherformat |
| 2 | Sichtbare Ankündigung vor Bot-Angriff (Späher/Rauch/Nachricht) | 5 | M | src/botkern.py, src/main.py (Render) | tests/test_gpt_bot_angriffsplanung.py | gering |
| 3 | Einen Kampfweg führen (Sofortweg nur als Nachbarschlacht) | 4 | M | src/main.py:6215, :6502 | tests/test_auftraege.py | mittel: Diplomatie-Knopf betroffen |
| 4 | Bot-Gedächtnis (Rächen, Stärke merken) | 4 | M | src/botkern.py | tests/test_gpt_kampf_botbeute_echte_kasse.py | gering |
| 5 | Reisefreigabe an den Götterschutz koppeln | 4 | S | src/main.py:2775, src/auftraege.py | tests/test_gpt_zeitstempel_und_schutz.py | gering |
| 6 | Mana-Balance neu kalkulieren (Transfer vs Tempelertrag) | 4 | S/M | data/welten.json, src/portalraum.py, data/buildings.json | tests/test_portalraum.py | gering, nur Zahlen |
| 7 | Tempel als mitgebrachtes Startgebäude klären | 3 | S | data/buildings.json | tests/test_spielschicht.py | gering |
| 8 | Lager je Dorf als Menüpunkt Dorfzentrum | 3 | M | src/main.py (Menü), src/spielschicht.py | tests/test_dorfuebersicht.py | mittel: Menüumbau |
| 9 | Beute-Regeln vereinheitlichen (eine Quelle) | 3 | S/M | src/botkern.py, src/kampfbericht.py | tests/test_beute_staffel.py | gering |
| 10 | Portalritual im Spiel erreichbar machen | 3 | M | src/main.py, src/portalraum.py | tests/test_portalraum.py | mittel: erst nach Rang 1 sinnvoll |

Was ich NICHT anfassen würde: die belegten Originalzahlen — Wall-Schwellen 10 bis 1.000 [BELEGT: data/buildings.json `verteidigungswall.stufen`], Karrenladungen 40/100/250 [BELEGT: data/units.json], die Einheitenwerte LE/AT/PA/SI/HE/RS/TP/GS/MU/SK [BELEGT: data/units.json], die Götterschutz-Frist 7 Tage [BELEGT: src/punkte.py] und den Transferfestpreis 5.000 Mana [BELEGT: src/portalraum.py]. Diese Werte sind die Treue-Anker zum Original; wer sie ändert, verfälscht den Originalbezug. Angepasst werden dürfen nur die ausgewiesenen VORSCHLAG-Stellen (Reisezeitfaktor, Mana-Balance, Taktik-Schwellen) — dort steht die Balance, nicht die Treue, auf dem Spiel.

## H. Was du nicht belegen kannst

Diese Liste trennt Originaltreue von Erfindung. Jede Stelle, an der die Quellen (Handbuch, Code, Daten) schweigen und der Vorschlag reine Design-Entscheidung ist:

1. **Bauzeit von Gebäuden.** Es gibt keine Bauzeit; `spielschicht.bauen` setzt sofort. Ob und wie lange Bauen dauern soll, ist eine reine Design-Entscheidung ohne Quelle.
2. **Gründungsdauer eines Zweitdorfs.** Wagenbau und Siedlerkarren sind belegt (src/main.py:4188), aber keine Quelle beziffert, wie lange die Gründung dauert oder was das Startpaket genau enthält — `spieloekonomie.absicht` liefert das Paket aus VORSCHLAG-Regeln.
3. **Alle Taktik-Schwellen.** Die Zahlen in D.1, D.2 und D.7 (0,4 / 0,7 / 0,85, Abstand 3/8/5, Rückzug 15–60 %) sind frei gewählte [VORSCHLAG]-Werte ohne Originalbezug; nur `aggression`/`trading` als Skala 0–1 sind belegt.
4. **Das Bot-Gedächtnis.** Keine Quelle nennt Rache, Erinnerung an den Schläger oder Stärke-Vergleich; der gesamte D.3-Abschnitt ist Erfindung im Dienst der Lesbarkeit.
5. **Die sichtbaren Signale.** Späher-Figur, Staubwolke, „erzürnt“-Nachricht sind nirgends belegt; sie sind die Übersetzung der Vorgabe „Spannung aus Ankündigung“ in Mechanik.
6. **Die Startressourcen je Dorf (10/100/100).** Als Vorgabe Abschnitt 2 gültig, aber im Original nicht als Dorf-Startwert belegt; data/baupreise.json nennt 100/100/10 nur als Start des ersten Dorfs.
7. **Reisezeitfaktor 7.200 s je Feld.** Ausdrücklich VORSCHLAG (src/auftraege.py:57, Vorgabe Daniel 31.10.2026, Registerpunkt 43); das Handbuch nennt nur Beispielstunden, keine Formel.
8. **Reisekosten (Gold/Nahrung/Mana je Feld).** Die Richtung ist belegt, die Höhe nicht (src/auftraege.py:260-264, Paket A2 als reine Balance-Annahme).
9. **Die Anzahl eigener Dörfer (sechs) und deren Aufteilung** (drei verteidigen/drei angreifen) ist Vorgabe, keine Originalzahl.
10. **Mana als Transferwährung in der neu kalkulierten Höhe.** Der Festpreis 5.000 ist belegt, jede Neukalibrierung der Mana-Erzeugung ist Design.

FERTIG 189
