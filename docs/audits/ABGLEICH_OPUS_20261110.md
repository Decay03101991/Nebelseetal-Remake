# ABGLEICH: der Opus-Prüflauf gegen den Code (10.11.2026)

**Was hier steht:** jede Zeile der Modellantwort ist am Code nachgeschlagen, jede Zahl nachgerechnet.
Ein Modellurteil ist eine Behauptung, bis sie geprüft ist — dieses Dokument trennt beides.

## 0. Der Lauf, in Zahlen

| Größe | Wert | Beleg |
|---|---|---|
| Antwortdatei | `docs/audits/OPUS_PRUEFUNG_20261110_1115.md`, 11.267 Byte, 70 Zeilen | Dateisystem |
| Messdatei | `docs/audits/opus_usage_20261110_1115.json` | Dateisystem |
| Modell | `opus` über Claude Code 2.1.319 (Abo) | `aufruf` in der Messdatei |
| Dauer | **432,4 s** (7 min 12 s), Rückgabe 0 | Messdatei |
| Token | 4 Eingabe, 58.022 Cache-Neu, 41.785 Cache-Treffer, 15.874 Ausgabe (davon 9.076 Denken) | Messdatei |
| Gemeldeter API-Gegenwert | **1,872 USD** — Rechengröße des Werkzeugs, **nicht abgebucht** (Abo) | `total_cost_usd` |
| Paket | 41.026 Zeichen, SHA256 `df0de7ec…`, gepinnter Commit `b341d93` | Messdatei |
| Werkzeug-Aufrufe des Modells | **0** Websuchen, **0** Web-Abrufe laut Nutzung | `server_tool_use` |
| Antwortzeichen | 10.894 | Werkzeugausgabe |

Zur Zeile »0 Web-Abrufe«: das Modell **behauptet** in seiner Antwort, sechs Dateien über
`raw.githubusercontent` nachgeladen zu haben. Die Nutzungszählung des Werkzeugs meldet 0 Abrufe. Beides
kann stimmen (Abrufe können außerhalb der gezählten Server-Werkzeuge liegen), ist aber **nicht belegt** —
deshalb steht hier beides nebeneinander und keine der zwei Zahlen wird als Wahrheit ausgegeben.

## 1. Die zwölf Behauptungen — Urteil des Modells gegen den Code

| Nr | Urteil Modell | Was ich am Code gefunden habe | Urteil Koordinator |
|---|---|---|---|
| 1 | BESTAETIGT | `main.py:4685-4687`: »ist der **Reichsbestand die zweite Kasse**« — Zitat stimmt. Reihenfolge gegenläufig, wie behauptet: `verbrauche_am_ort` nimmt Ort, dann Reich (`main.py:4679-4683, 4700-4706`); `verbrauche_reichsweit` nimmt Reich, dann Orte (`main.py:4731, 4751-4755`). **Zusatz, den das Modell offenließ:** `_lokale_kasse_aktiv()` (`main.py:4637-4644`) liefert `True`, sobald Modus NEU + Ökonomie aktiv + Siedlungen vorhanden — dann greifen alle Zuschuss-Zweige gar nicht. Die zweite Kasse betrifft **nur Altstände**, und der Docstring nennt sie »ÜBERGANG, ehrlich benannt«. | **bestaetigt**, im Neumodus gegenstandslos |
| 2 | UNBEKANNT | `src/kampf_alt_handbuch_2009.py` **existiert nicht** (`ls`). `tests/test_gpt_kampf_forum_neu.py:84-87`: »Die alte Schlachtfassung … wurde aus dem Spielcode entfernt … Damit gilt: genau EINE Schlachtfunktion«, mit Prüfung auf Nichtexistenz. **Damit ist die alte Behauptung »zwei Kampfsysteme« erledigt.** Aber: `src/kampf.py:5` nennt die Datei weiter »Frühere Implementierung: kampf_alt_handbuch_2009.py (Rückfallsicherung)« — eine Rückfallsicherung, die es nicht gibt. | **überholt** (Befund G1: veralteter Docstring) |
| 3 | UEBERHOLT | `main.py:2749-2755`: `bauen_auf_karte` ruft `gebaeude_forschung_erlaubt(kennung, forschungsstaende)` für **jedes** Gebäude und bricht bei `not frei` ab. Funktion `main.py:2701-2719`: fünf Gebäude frei (`OHNE_FORSCHUNG_BAUBAR`), alle anderen brauchen Baukunst ≥ 1. **Die offene Unterfrage ist entschieden:** bei `forschungsstaende=None` ergibt `.get("Baukunst", 0) or 0` den Wert 0 → **kein Freipass**, nur die fünf. `data/buildings.json → regeln.ohne_forschung_baubar` nennt wörtlich dieselben fünf. | **bestaetigt (überholt)** |
| 4 | UEBERHOLT | `main.py:7911`: `tage, self._day_accum = divmod(self._day_accum, zeitbasis.SEKUNDEN_JE_TAG)`; `main.py:7920`: `if self.day > punkte.goetterschutz_tage() or krieg > 0`. `punkte.py:42`: `GOETTERSCHUTZ_TAGE = 7`. Zweite Regel bestätigt: `punkte.py:210` `alter < GOETTERSCHUTZ_TAGE * SEKUNDEN_JE_TAG`, und `punkte.py:18-20` sagt selbst, der Abbruch beim ersten Kriegspunkt sei dort »NICHT« abgebildet. **Zusatz:** die zweite Regel ist **in Betrieb** — `spielschicht.py:845` fragt `PUNKTE.goetterschutz_aktiv(...)` für den Zustandsbericht. | **bestaetigt (überholt)**, zwei Regeln leben (Befund G2) |
| 5 | TEILWEISE | `auftraege.py:66` `SEKUNDEN_JE_FELD = 7200.0`, benutzt in `auftraege.py:176` (`e / g * SEKUNDEN_JE_FELD * zeitfaktor`) — Reise also überholt. Drosselung: `auftraege.py:314-315` `drosselung = min(90.0, …)`, `tempo = 1.0 - drosselung / 100.0`; `reisezeit_sekunden` (`auftraege.py:450-451`) kennt **keine** Drosselung. Wortlaut in `offene_luecken()` (`auftraege.py:717-720`): »abgelegt, aber **nicht auf die Formel angewandt**«. Das Modell hat recht: der Satz »nicht angeschlossen« aus meiner Sichtung ist eine **Paraphrase** und steht so nicht in der Datei. | **bestaetigt** (Befund G3: Drosselung wirkt einseitig) |
| 6 | UNBEKANNT | **Selbst aufgelöst:** `spieloekonomie.py:54` `AUSBILDUNG_STUFENFAKTOR_AKTIV = True`, `spieloekonomie.py:931-939`: `dauer = grunddauer / max(1, int(stufe))`, `grunddauer = REGELN["pilot_ausbildung_minuten"] * 60`. Wert `data/spieloekonomie.json:36`: **20 Minuten** → 1.200 Spielsekunden. Der Docstring nennt die Kopplung belegt (Richtung) und die Zahl VORSCHLAG. Die alte Behauptung »Ausbildungszeit nicht an Gebäudestufe gekoppelt« ist damit **erledigt**. | **überholt** (Kopplung gebaut) |
| 7 | UNBEKANNT | `main.py:3759-3762`: `MENU_ANZEIGE` enthält tatsächlich nur »Gilde« und »Kampfsimulator« — Zitat stimmt. Der Menüpunkt existiert aber als **Zusatzpunkt**: `main.py:3766` `MENU_ZUSATZ`, hinter der Ruhmeshalle (`main.py:3780-3781`), und die Ansicht `_render_voraussetzungen` (`main.py:15570-15600`) zeigt je Forschung die Spalte »Bedingung« aus `data/research.json`. Ob sie **alle** Bedingungen des Originals zeigt, ist ohne Handbuchvergleich **nicht entschieden**. | **offen** — die Ansicht liest `research.json`, Vollständigkeit ungeprüft |
| 8 | TEILWEISE | `main.py:3652` `BIBLIOTHEK_OBERGRENZE = 2`, gelesen in `main.py:11130`. Der Kommentar `main.py:3648-3651` sagt selbst: das Handbuch kennt **»nur eine einzige Bibliothek« je Siedlung**, ohne Gesamtgrenze — Daniels 2 ist **strenger** als das Original und bleibt als Entscheidung stehen. Je Siedlung gilt `data/buildings.json` → `bibliothek.max_je_siedlung = **1**` (**die Zahl, die das Modell nicht kannte**), durchgesetzt in `main.py:2756-2765` samt Zusatz »höchstens zwei je Spieler, eine je Karte«. | **bestaetigt** — kein Widerspruch zum Original, eine bewusste Zusatzgrenze |
| 9 | BESTAETIGT | `spielzeit.py:34` `STANDARD_FAKTOR = 180.0`; `spielzeit.py:32-33` »VORSCHLAG: 1 Spielstunde = 20 Sekunden«; Kopf des Moduls »**Nicht belegt**«. Rechnung siehe Abschnitt 2. | **bestaetigt** |
| 10 | UEBERHOLT | `punkte.py:50` `ZIEL_PUNKTE_VERWORFEN = 300` mit Kommentar `punkte.py:45-49` (»Original kennt KEINEN SIEG … 300 ist die belegte GOETTERSCHUTZGRENZE«), `punkte.py:124` `(fp + kp) // 2`. **Offene Unterfrage entschieden:** `grep ZIEL_PUNKTE_VERWORFEN src/` findet **nur die Definition** — gelesen wird sie nirgends im Spielcode, nur in `tests/test_punkte.py:261`. Die Konstante ist reine Dokumentation. | **bestaetigt (überholt)** + Befund G4 |
| 11 | TEILWEISE | `auftraege.py:84` `BEUTE_ANTEIL_PROZENT = 50`, VORSCHLAG-Kommentar `81-83`. `grep BEUTE_ANTEIL_PROZENT src/` findet **nur** die Definition und zwei **Texte** (`auftraege.py:237, 727`) — keine Rechnung. Die Beute läuft über `kampfbericht.beute_staffel(...)` (`kampfbericht.py:237`, aufgerufen `auftraege.py:407`). Das Modell hat recht: die 50 ist für das Ergebnis folgenlos. | **bestaetigt** + Befund G5 |
| 12 | UNBEKANNT | `main.py:2632` `SIEDLUNGEN_MAXIMUM = 6`, **gelesen** in `main.py:5513` und `5625` (Gründung begrenzt). `gebaeude_wirkung.bevoelkerungsgrenze` (`gebaeude_wirkung.py:163-171`): ohne Siedlung **10** (belegter Startwert Handbuch S. 7), je Siedlung 10 + 5 je Haus — gemessen: `bevoelkerungsgrenze([]) = 10`, `bevoelkerungsgrenze([1 Siedlung ohne Haus]) = 10`. Die Behauptung »in Ordnung« trägt. | **bestaetigt** |

**Zählung:** **fünf überholt** (2, 3, 4, 6, 10 — die alte Behauptung gilt heute nicht mehr), **sechs
bestätigt** (1, 5, 8, 9, 11, 12 — vier davon mit einem Zusatz, den das Modell offenließ), **einer offen**
(7). Kein einziges Modellurteil war falsch; **die Lücken des Pakets hat es ehrlich als UNBEKANNT
markiert** statt zu raten.

## 2. Die sechs Rechenaufgaben — nachgerechnet

Werkzeug: `tools/opus_nachrechnen.py` (Ausgabe lokal in `docs/audits/opus_nachrechnung_20261110.log` —
`*.log` ist von Git ausgenommen, die Datei ist mit einem Aufruf des Werkzeugs reproduzierbar). Alle Zahlen
stammen aus den Modulen, nicht aus dem Kopf.

| Punkt | Modell | Nachgerechnet | Urteil |
|---|---|---|---|
| 1 Forschung Stufe 10 | 100 h → **2.000 s ≈ 33 min 20 s** | `forschung.dauer_stunden(10) = 100` → 2.000 s | **stimmt** |
| 1 Forschung Stufe 20 | 400 h → **8.000 s ≈ 2 h 13 min** | `dauer_stunden(20) = 400` → 8.000 s | **stimmt** |
| 1 Summen | 1→10 = 385 h = 7.700 s; 1→20 = 2.870 h = 57.400 s | 385 / 7.700 s und 2.870 / 57.400 s | **stimmt** (20·21·41/6 = 2.870) |
| 2 Reise 1 Feld | **40 s** | 7.200 / 180 = 40 s | **stimmt** |
| 2 Reise 10 Felder | **400 s = 6 min 40 s** | `reisezeit_sekunden(10, 1.0) = 72.000` → 400 s | **stimmt** |
| 3 Ausbildung | UNBEKANNT | 20 min = 1.200 Spielsekunden → **6,67 s** Echtzeit (Stufe 1); bei Stufe 5 = 1,33 s | **Lücke geschlossen** |
| 4 Siedlerzuwachs | **20 s je Siedler**, 10 Siedler in **200 s** | 3.600/180 = 20 s ✓; 10 × 20 = 200 s ✓ (Grenze 10 + 5 je Haus) | **stimmt** |
| 5 Wallstufe 8 | 512 Kriegspunkte, allein **256** Gesamt | `punkte.kriegspunkte({}, 8) = 512`, `gesamtpunkte({}, {}, 8) = 256` | **stimmt** |
| 5 Schwelle | »fp ≥ 90« | (fp + 512) // 2 ≥ 301 ⇔ fp ≥ 90 | **stimmt** |
| 5 kleinste Lösung | »4³ + 3³ = **91**« | **kleiner erreichbar: fp = 90** aus 3³+3³+3³+2³+1³ → Gesamt **301** | **widerlegt** (91 ist nicht minimal) |
| 5 Forschungszeit | 44 h Spielzeit = **880 s** echt | (1+4+9+16)+(1+4+9) = 44 h → 880 s | **stimmt** |
| 6 Götterschutz | 1 Tag **480 s**, 7 Tage **3.360 s = 56 min** | 86.400/180 = 480 s; 7×480 = 3.360 s | **stimmt** |

**Der eine sachliche Fehler des Laufs** ist damit gefunden: 91 statt 90. Folge: minimal sind **fünf**
Forschungsgebiete auf Stufe 3, 3, 3, 2, 1 — nicht zwei auf 4 und 3. Das Urteil »trivial« bleibt richtig,
die Zahl war zu hoch.

## 3. Die drei schwersten Punkte

- **C1 Zwei Kassen:** bestätigt, aber **nur für Altstände**. `_lokale_kasse_aktiv()` ist im Neumodus
  `True`, dann läuft keine Zuschuss-Buchung. Kein Handlungsbedarf, ein Registervermerk genügt.
- **C2 Götterschutz endet praktisch sofort:** rechnerisch bestätigt. Wallstufe 1 = 1 Kriegspunkt → Schutz
  sofort vorbei (sofern `punktestand()["krieg"]` die Wallpunkte führt — das habe ich **nicht** geprüft);
  ohne Wall nach 3.360 s. **Neu und wichtiger als die Rechnung:** es laufen **zwei** Schutzregeln
  (Tagesregel in `tick`, Zeitstempel-Regel in `spielschicht.py:845`) mit unterschiedlicher Semantik.
- **C3 Drosselung wirkt auf Kosten, nicht auf die Zeit:** bestätigt (`auftraege.py:314-315` gegen `451`,
  Wortlaut in `offene_luecken`). Eine Spielentscheidung für Daniel, kein Fehler.

## 4. Neue Befunde aus diesem Abgleich (gehen ins Register)

| Nr | Befund | Fundstelle | Größe |
|---|---|---|---|
| G1 | `kampf.py` wirbt mit einer »Rückfallsicherung«, die es nicht mehr gibt (eine Wache verbietet die Datei) | `src/kampf.py:5` gegen `tests/test_gpt_kampf_forum_neu.py:84-87` | Doku, klein |
| G2 | Zwei Götterschutz-Regeln mit verschiedener Grundlage (Tag + erster Kriegspunkt gegen reines Zeitfenster) können sich widersprechen | `main.py:7920` gegen `punkte.py:210`, benutzt `spielschicht.py:845` | Regel, mittel |
| G3 | Drosselung verteuert die Mission, verkürzt aber die Reisezeit nicht — der Spieler kann Kosten verschieben, ohne die Zeit zu tragen | `auftraege.py:314-315, 450-451, 717-720` | Balancing, mittel |
| G4 | `ZIEL_PUNKTE_VERWORFEN = 300` wird im Spielcode **nirgends gelesen** (nur in einer Prüfung) | `src/punkte.py:50`, `tests/test_punkte.py:261` | totes Gut, klein |
| G5 | `BEUTE_ANTEIL_PROZENT = 50` steht nur noch in zwei Anzeigetexten, keine Rechnung liest sie | `auftraege.py:84, 237, 727` | totes Gut, klein |
| G6 | `forschung.dauer_sekunden` bricht ab (`None * 3600`), wenn kein Regeltext das Wort »Quadrat« enthält — heute enthalten (`research.json → regeln.dauer`), also nur eine künftige Falle | `spieldaten.py:232-237`, `forschung.py:52-53`, `data/research.json` | Robustheit, klein |
| G7 | Die 300-Punkte-Marke ist mit Wallstufe 8 und fünf Forschungsstufen in **880 s** erreichbar (Gesamt 301) — die alte Audit-Zeile 10 ist damit **quantitativ** belegt, nicht nur behauptet | Rechnung Abschnitt 2 | Beleg, kein Schaden |

## 5. Was das Modell nicht wissen konnte — aufgelöst oder offen

| Frage des Modells | Antwort |
|---|---|
| Existiert `kampf_alt_handbuch_2009.py`? | Nein, entfernt; eine Wache prüft die Abwesenheit. Docstring veraltet (G1). |
| `gebaeude_forschung_erlaubt` bei `forschungsstaende=None`? | Kein Freipass: nur die fünf belegten Gebäude. |
| Wer liest `BIBLIOTHEK_OBERGRENZE`? | `main.py:11130` (Bau-Weiche); je Siedlung gilt `max_je_siedlung = 1` aus `buildings.json`. |
| Was tut `_lokale_kasse_aktiv`? | `True` im Neumodus → die zweite Kasse ist ein Altstanden-Übergang. |
| Wo liegt `pilot_ausbildung_minuten`? | `data/spieloekonomie.json:36` = 20; Kopplung an die Gebäudestufe aktiv (`spieloekonomie.py:54, 931-939`). |
| Bricht `dauer_sekunden` bei fehlendem »Quadrat«? | Heute nicht (`research.json → regeln.dauer` enthält es), künftig möglich (G6). |
| Zeigt »Voraussetzungen« alle Bedingungen? | **Offen** — die Ansicht liest `research.json` vollständig als Spalte, ein Handbuchvergleich fehlt. |
| Enthält `punktestand()["krieg"]` die Wallpunkte? | **Nicht geprüft** — entscheidet C2, gehört in die nächste Runde. |

## 6. Grenzen dieses Abgleichs

- Geprüft sind die **19 Stellen des Pakets** plus die Stellen, die ich zum Auflösen der Lücken gebraucht
  habe. **Kein vollständiger Gesamtaudit** — der fehlt weiterhin.
- `punktestand()` und die Tick-Schleife (`_tick_loop`) sind **nicht** gelesen: die Zeitrechnung in
  Abschnitt 2 gilt unter der Annahme, dass `tick` Spielsekunden bekommt.
- Der gemeldete API-Gegenwert (1,872 USD) ist **keine Ausgabe**; das Abo trägt den Lauf.
- Ein Modellurteil bleibt eine Behauptung: die Spalte »Urteil Koordinator« nennt je Zeile die Stelle, an
  der es entschieden wurde — nachschlagbar, nicht glaubbar.
