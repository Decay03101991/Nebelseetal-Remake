# Zeitlimit und Tempo — Quellenlage und Vorschlag

**Auftrag:** Entscheidung 6 (Daniel, 31.10.2026), wörtlich: „ich verstehe nicht genau, was gemeint
ist — du kennst alle Vorgaben; möglichst nach Original, sonst Indizien, sonst eine kluge Lösung, und
das dokumentieren" (`docs/ENTSCHEIDUNGEN_CODEAUDIT_20261031.md`, Z. 38). Vorgehen verbindlich:
Quelle, dann Indiz, dann eigene Lösung — jede eigene Festlegung als **VORSCHLAG**.

**Geprüfte Quellen:** `docs/original/Spielanleitung_2009_Textfassung.txt` (24-Seiten-PDF, nennt innen
01.09.2006), die 2006er Original-Seiten in `docs/original/Spielanleitung_2005/`, `docs/original/website/`,
`docs/quellen/Tutorial_eines_Spielers_Original_28-10-2026.odt`, `docs/quellen/Ruhmeshalle_31-08-2011_Original.png`,
`docs/PRUEFREGEL_ORIGINAL.md` (Register 42/50/54), Code in `src/main.py`, `src/spielzeit.py`,
`src/punkte.py`, `data/spielzeit.json`.

**Nur gelesen. Nichts im Projekt geändert.**

---

## 1. Quellenlage Zeitlimit

| Quelle | Zitat (wörtlich) | was es hergibt | Urteil |
|---|---|---|---|
| Handbuch, Seite 3, Z. 49–52 | „Jeder hat bei Nebelseetal sicher seine eigenen Ziele. Großer Feldherr, friedlicher Forscher oder einflussreicher Händler, das alles ist möglich. Der Weg zu jedem dieser Ziele führt jedoch über die Rohstoffe" | Es gibt **kein gemeinsames Spielziel** und damit kein definiertes Lauf-Ende. Ein Zeitlimit wäre eine Erfindung. | **BELEGT (dass es keines gibt)** |
| Handbuch, Seite 2, Z. 25–27 | „Das Spiel läuft in Echtzeit, was bedeutet, dass Rohstoffproduktionen, Einheitenbewegungen, Forschungen etc. nicht in Runden ablaufen, sondern eine gewisse Zeit benötigen und dann abgeschlossen sind." | **Keine Runden** → kein Rundenlimit, kein „Runde 12 von 15". Die Zeit ist gleitend. | **BELEGT** |
| 2006er Seite `beschreibung.php.txt`, Z. 15–20 | „Das Spiel läuft in Echtzeit, was bedeutet, dass Rohstoffproduktionen, Einheitenbewegungen, Forschungen etc. nicht in Runden ablaufen, sondern eine gewisse Zeit benötigen und dann abgeschlossen sind. […] Eine Forschung die 2 Tage und 10 Stunden dauert, ist auch erst 2 Tage und 10 Stunden, nachdem Ihr sie in Auftrag gegeben habt, abgeschlossen." | Zweite, unabhängige Fassung derselben Aussage: Echtzeit **1 : 1**, keine Runden. | **BELEGT** |
| Handbuch, Seite 2, Z. 29 | „Eine Forschung die 2 Tage und 10 Stunden dauert, ist auch erst 58 Stunden nachdem Du sie in Auftrag gegeben hast abgeschlossen." | 2 Tage 10 Stunden = 58 **echte** Stunden. Kein Zeitraffer im Original. | **BELEGT** |
| Handbuch, Seite 4, Z. 93–96 | „Hier kannst Du Dein Passwort ändern, den Newsletter bestellen/abbestellen, einen anderen Spielskin wählen, in den Urlaubsmodus wechseln und, falls gewünscht, Deinen Account löschen. Letzteres kann nicht rückgängig gemacht werden!" | Ein Lauf endet nur durch **Kontolöschung durch den Spieler** (oder Urlaubspause), nie durch die Uhr. | **INDIZ** (Ende ja, aber freiwillig) |
| `docs/quellen/Tutorial_eines_Spielers_Original_28-10-2026.odt` | „Ihr könnt aber auch einfach abwarten und euch nicht mehr einloggen. Nach 2 Wochen werdet ihr inaktiv und nach 1 Woche wird der Account automatisch gelöscht." | Einzige zeitgebundene Beendigung im ganzen Material — sie hängt an **Inaktivität**, nicht an einer Spieldauer. Für ein Einzelspieler-Remake ohne Server kein Vorbild. | **INDIZ** (nur Inaktivität) |
| `docs/quellen/Ruhmeshalle_31-08-2011_Original.png` | Spaltenköpfe wörtlich: „Rang", „Name", „Gilde", „Punkte"; Platz 1 „Die Spinne" mit 29084 Punkten; Statusvermerk „(Urlaubmodus)" | **Keine** Spalte für Runde, Saison, Restzeit oder Spielende. Punktzahlen bis 29084 — weit über der Götterschutzgrenze 299. Also: kein Saisonende, kein Punkteende, kein Zeitlimit sichtbar. | **INDIZ (stark)** |
| Handbuch, Seite 6, Z. 210–213 | „Haben beide Spieler ebenfalls die gleiche Anzahl an Rufpunkten, steht der Spieler oben, der schon länger auf dem Server angemeldet ist." | Die Rangliste kennt **Anmeldedauer** als Kriterium, aber keinen Saison-Schnitt. | **INDIZ** |
| 2006er Seite `punktesystem.php.txt`, Z. 38 | „Wenn Ihr 24 Stunden keine Handelseinkünfte hattet, verliert ihr einen Handelspunkt." | **Punkteverfall ist belegt — aber nur für Handelspunkte und nur in der älteren Fassung.** Zeitgebunden, kein Spielende. | **BELEGT** |
| 2006er Seite `punktesystem.php.txt`, Z. 40–42 | „Wenn Ihr nun 24 Stunden lang nichts mehr verkauft wird euch ein Handelspunkt abgezogen. Nach weiteren 24 Stunden ein weiterer. Dies bedeutet, das Ihr nach drei Tagen alle drei Handelspunkte wieder verlohren habt." | Verfall läuft stückweise, ohne Untergrenze bei 0 (im Code: nicht unter 0). | **BELEGT** |
| 2006er Seite `punktesystem.php.txt`, Z. 33 | „Solltet Ihr Einheiten verlieren, verringern sich auch Eure Kriegspunkte, um den entsprechenden Wert!" | Zweiter belegter Punkteverfall — hängt an **Verlusten**, nicht an Zeit. | **BELEGT** |
| Handbuch, Seite 22, Z. 1274–1276 | „Wenn nach 10 Kampfsequenzen noch kein Sieger feststeht, geht die Schlacht unentschieden aus." | Das **einzige** Limit im ganzen Regelwerk — aber es begrenzt einen Kampf, nicht die Partie. | **BELEGT** (Kampf), nicht Partie |
| Handbuch, Seite 12/13, Z. 422–423 | „Ein Forschungsauftrag dauert (Neue Stufe*Neue Stufe) in Stunden." | Dauern sind **fest** und werden nicht durch ein Laufende verkürzt. Ein Zeitlimit verändert also nur, wie viel davon erlebbar ist. | **BELEGT** |
| Handbuch, Seite 19, Z. 1138–1141 | „Die Zeitangaben gelten für eine Strecke. Wenn also 2 Stunden angegeben sind, benötigen Deine Einheiten 2 Stunden um die Zielsiedlung zu erreichen. Sollten die Einheiten […] wieder zur Startsiedlung zurückkehren, dauert der Auftrag doppelt so lange." | Auftragsdauern sind belegt, aber ohne Bezug zu einem Laufende. | **BELEGT** |
| `docs/original/website/` (home, beschreibung, community, geplante_updates, hintergrundgeschichte 1–3) | — | **Keine** Zeile zu Zeitlimit, Runden, Saison oder Spielende. Die Seite `geplante_updates.php` ist leer (nur Rahmen). | **NICHT BELEGT** |
| `docs/PRUEFREGEL_ORIGINAL.md`, Register 42 und 50 | Register 42: „Das Original hat KEINE Siegbedingung." Register 50: „Kein Sieg — umgesetzt: `punkte.spielausgang` liefert nur noch `niederlage`/`weiter`" | Die Projektprüfung hat diesen Punkt schon entschieden: **kein Sieg, kein Ende durch Punkte**. Ein Zeitlimit darf dem nicht widersprechen. | **BELEGT** (Projektstand) |

**Ergebnis Zeitlimit:** In **keiner** der beiden Anleitungen, auf keiner der 2006er Seiten, auf der
Website oder im Tutorial steht ein Zeitlimit, ein Rundenlimit oder ein Spielende. Belegt ist das
Gegenteil: Echtzeit ohne Runden, individuelle Ziele, ein Ende nur durch den Spieler selbst.
Der einzige zeitgebundene Mechanismus im Material ist der **Handelspunkte-Verfall (24 h)** — und der
ist kein Laufende.

---

## 2. Quellenlage Tempo / Spieluhr

| Quelle | Zitat (wörtlich) | was es hergibt | Urteil |
|---|---|---|---|
| Handbuch, Seite 2, Z. 23–27 | „Das Spiel läuft in Echtzeit […] Wenn Du beispielsweise durch eine Holzfällerhütte 4 Einheiten Holz pro Stunde produzierst, bekommt Deine Siedlung alle 15 Minuten 1 Einheit Holz gutgeschrieben." | Der Takt ist **Echtzeit**: 4/h = 1 je 15 echte Minuten. Ein globaler Beschleunigungsfaktor wird nirgends genannt. | **BELEGT** (1 : 1), Faktor selbst **NICHT BELEGT** |
| 2006er Seite `beschreibung.php.txt`, Z. 15–20 | „Wenn Ihr beispielsweise durch eine Holzfällerhütte 4 Holz pro Stunde produziert, bekommt eure Siedlung alle 15 Minuten 1 Holz gutgeschrieben." | Dieselbe Aussage in der älteren Fassung — **beide** Fassungen sind Echtzeit 1 : 1. | **BELEGT** |
| 2006er Seite `rohstoffe.php.txt`, Z. 20–23 | „Wieviel pro Stunde produziert wird, könnt ihr aus der Tabelle oben entnehmen. Der Wert in Klammern gibt die Produktionsmenge pro Stunde an." / „Eure Siedlung bekommt außer den Rohstoffen einen neuen Siedler pro Stunde." | „pro Stunde" ist durchgehend die **echte** Stunde. | **BELEGT** |
| Handbuch, Seite 18, Z. 1103–1104 | „GS: Der Geschwindigkeitswert gibt die Reisegeschwindigkeit einer Einheit an. Je höher dieser Wert, desto schneller kann die Einheit zwischen zwei Siedlungen reisen." | „Geschwindigkeit" im Original heißt **GS je Einheit** — nicht Spieluhr, nicht Server-Tempo. Wer „Tempo" sagt, muss das trennen. | **BELEGT** |
| Handbuch, Seite 20, Z. 1190–1193 | „dann könnt Ihr die Geschwindigkeit in 10% Schritten drosseln. Die aktuelle Dauer der Mission wird im Feld ‚Reisedauer' angezeigt. Je langsamer Eure Einheiten reisen, desto weniger Gold benötigen sie." | Tempo-Regler gibt es — aber **je Auftrag** (Drosselung), nicht global. Im Code als Formel vorhanden, Bedienung offen (Register 39/I). | **BELEGT** |
| Handbuch, Seite 12, Z. 503–504 | „Die Gebäude werden stufenweise ausgebaut. Je höher die Stufe, desto schneller werden dort Einheiten ausgebildet." | Zweiter belegter Tempo-Hebel: **Gebäudestufe**, nicht Spieluhr. Umgesetzt 31.10. (`spieloekonomie.AUSBILDUNG_STUFENFAKTOR_AKTIV`, Register 53). | **BELEGT** |
| `Tutorial_eines_Spielers_Original_28-10-2026.odt` | „Unter der Zahl steht mit einem + versehen eure Gesamtproduktion pro Stunde in Echtzeit." | Der Spielertext sagt ausdrücklich „in Echtzeit" — unabhängige Bestätigung von 1 : 1. | **INDIZ** (Spielerdokument) |
| `archiv/dokumentation/projektunterlagen_historisch/nebelseetal_research.md`, Z. 16 | „Speedserver Armageddon mit 200-facher Geschwindigkeit" | **Einziger** Träger der Idee „schnellerer Server". Es ist eine **Projektnotiz**, kein Originalzitat; die Zahl 200 steht in keiner Originaldatei. | **INDIZ (schwach)** |
| `docs/original/website/community.php`, Z. 101 u. a. | „Armageddon" nur als **Link** auf `armageddon.nebelseetal.de/login.php` | Die Welt „Armageddon" ist belegt, ihre Geschwindigkeit **nicht**. | **NICHT BELEGT** |
| 2006er Seite `einheiteninfo.php.txt`, Z. 6 | „Geschwindigkeit:" (Werteliste einer Einheit) | Bestätigt: „Geschwindigkeit" ist ein **Einheitenwert**. | **BELEGT** |

**Ergebnis Tempo:** Das Original läuft in Echtzeit 1 : 1; „Geschwindigkeit" bezeichnet dort
ausschließlich Einheiten-GS, Auftragsdrosselung und Ausbildungsstufen. Eine **globale Spieluhr** ist in
keiner Quelle belegt. Der heute im Code benutzte Faktor **×180** stammt aus Daniels Spielbericht
(Rohstoffeingang nicht sichtbar) und ist in `src/spielzeit.py` selbst als „Nicht belegt" markiert.

---

## 3. Was im Code heute steht

| Datei:Zeile | Was dort steht | Bemerkung |
|---|---|---|
| `src/main.py:3148` | `def _spieler_auswahl` — das Startmenü | Erscheint nach dem Tor, baut die Auswahl auf |
| `src/main.py:3160–3175` | drei Slots: `slot_status` + „Slot {nummer} laden" (gesperrt, wenn keine Datei) | Laden je Slot |
| `src/main.py:3178–3181` | „Spielstaende verwalten / archivieren", „Neue Partie beginnen" | **Nur diese Knöpfe** — kein Zeitlimit, kein Tempo |
| `src/main.py:3184–3188` | `_spieler_neu_starten` → `GameState()` + `generate_map` → `_spiel_starten` | Eine neue Partie bekommt **keine** Optionen mit |
| `src/spielzeit.py:34` | `STANDARD_FAKTOR = 180.0` | Vorgabe: 1 Spielstunde = 20 echte Sekunden |
| `src/spielzeit.py:35` | `STUFEN = (1.0, 20.0, 60.0, 180.0, 600.0)` | ×1 ist ausdrücklich das Originaltempo |
| `data/spielzeit.json:2` | `"faktor": 180.0` | Gebündelte, **unveränderliche** Vorgabe |
| `data/spielzeit.json:10` | `"belegt": false` | Ehrlich: der Faktor ist nicht belegt |
| `src/spielzeit.py:55–64` | `einstellungspfad()` → `NEBEL_SPIELDATEN_ORDNER` oder `~/.nebelseetal/spielzeit_einstellung.json` | Spielerwahl liegt **privat**, nie im Bundle |
| `src/spielzeit.py:89–98` | `faktor()` — liest einmal, cached, fällt auf 180 zurück | Eine Quelle für alle Rechner |
| `src/spielzeit.py:152–159` | `spielstunden_je_echtsekunde`, `echtzeit_fuer_spielstunden` | Umrechnung für Wege und Anzeigen |
| `src/spielzeit.py:162–168` | `text()` → „×180 · 1 Std = 20 s" | Fertige Beschriftung für Knöpfe |
| `src/main.py:7331–7338` | `_tick_loop`: `dt = laufzeituhr.vergangen()`; `self.state.tick(dt * spielzeit.faktor())` | Der Faktor wird **genau einmal** angewandt |
| `src/main.py:6323` (Takt) | `if dt > 0 and getattr(self.state, "spielende", None) is None:` | Ist die Partie entschieden, **steht die Uhr** |
| `src/main.py:6312–6339` | `_render_settings` — Knopfreihe „Tempo:" über `spielzeit.stufen()`, `spielzeit.setzen()` | Tempo ist heute **nur** in den Einstellungen, **nicht** im Startmenü |
| `src/main.py:3352–3355` | `lbl_tempo` in der Kopfzeile: „Tempo {spielzeit.text()}" | Anzeige existiert schon |
| `src/main.py:2670–2672` | `_day_accum += dt_seconds`; `divmod(..., 86400.0)`; `self.day += int(tage)` | Spieltag **aus Spielsekunden**, beginnt bei 1 |
| `src/main.py:2720` / `2856` | `"spielsekunden": self.spielsekunden` gespeichert und geladen | **Der Zeitzähler einer Partie überlebt Speichern/Laden** |
| `src/main.py:7310–7327` | `_pruefe_spielende` → `state.spielausgang()`, setzt `state.spielende` **einmal** | Die EINE Stelle für ein Laufende |
| `src/main.py:7429–7433` | `if self.state.spielende == "niederlage":` … sonst „kein Sieg" | Nur **zwei** Zweige — ein dritter fehlt |
| `src/punkte.py:275–305` | `spielausgang` → nur `niederlage` (keine Siedlung **und** keine Einheit) oder `weiter` | „kein Sieg vorgesehen (E5)" |
| `src/punkte.py:327–328` | `HANDELSPUNKTE_JE_GOLD = 100.0`, `HANDELSPUNKTE_VERFALL_SEKUNDEN = 24 * 3600` | Der belegte Punkteverfall ist gebaut, aber **Kennzahl**, nicht Gesamtpunkte |
| `src/zeitbasis.py:3–6` | „Die monotone Uhr liefert NUR verstrichene Echtzeit […] Spielsekunden werden ausschließlich in GameState.tick fortgeschrieben." | Ein Limit darf **nie** an `time.time()` hängen |

**Fazit Code:** Zeitlimit gibt es **nicht** (auch keine Option). Tempo gibt es, aber nur in den
Einstellungen nach dem Start — das Startmenü kennt weder das eine noch das andere.

---

## 4. Vorschlag

**Grundsatz:** Beide Optionen sind **abschaltbar** und **standardmäßig aus**. Das ist keine Bequemlichkeit,
sondern die einzige Form, die den Quellen nicht widerspricht: Das Original kennt kein Laufende
(Register 42) und keinen Zeitfaktor. Wer beides als Pflicht einbaut, entfernt sich von der Vorlage.

### 4a. Option „Zeitlimit" (im Startmenü, neben „Neue Partie beginnen")

| Punkt | Festlegung |
|---|---|
| Auswahl | „Ohne Zeitlimit" / „15 Spieltage" / „30 Spieltage" / „60 Spieltage" |
| **Vorgabe** | **„Ohne Zeitlimit"** |
| Einheit | **Spieltage**, gemessen an `state.spielsekunden` (86400 s = 1 Spieltag) — **nicht** Echtzeit |
| Zeitpunkt | Wahl wirkt nur auf eine **neue** Partie; sie steht danach im Spielstand |
| Erreichen | Meldung + Nachricht „Laufziel erreicht: 15 Spieltage" + Bewertung über `punkte.auszeichnungen`, **keine** Niederlage |
| Danach | zwei Knöpfe: „Weiterspielen" (setzt das Limit im laufenden Spielstand auf „ohne") und „Partie beenden" |
| Anzeige | Kopfzeile unter `lbl_tempo`: „Lauf 7 / 15 Spieltage" bzw. „Lauf: ohne Limit" |
| Anzeige bei der Wahl | „15 Spieltage · bei ×180 etwa 2 Std" (aus `spielzeit.echtzeit_fuer_spielstunden`) |

**Warum Spieltage und nicht Echtminuten:** Die Quellen rechnen in Spieltagen und Spielstunden
(Götterschutz 7 Tage, Forschung Stufe² in Stunden). Der Spieltag ist die Währung der Vorlage. Zweitens
wird das Limit damit **tempo-unabhängig**: 15 Spieltage bleiben 15 Spieltage, egal ob ×1 oder ×600 —
das Tempo ändert nur, wie lange man dafür am Rechner sitzt. Drittens ist `spielsekunden` schon
gespeichert (`main.py:2720`, `2856`) und gegen Systemuhr-Manipulation unempfindlich (`zeitbasis.py:3–6`).

**Warum 15 / 30 / 60:** 15 Spieltage ist **genau** der bereits notierte A3-Vorschlag
(120 Echtminuten bei ×180; 15 × 86400 / 180 = 7200 s = 120 min). Damit kommt keine dritte Zahl in die
Welt. 30 und 60 sind die Verdopplung für längere Läufe.

### 4b. Option „Tempo" (im Startmenü, neben der Slot-Wahl)

| Punkt | Festlegung |
|---|---|
| Auswahl | Knopfreihe aus `spielzeit.stufen()`: ×1 / ×20 / ×60 / ×180 / ×600 |
| Beschriftung | `spielzeit.text(stufe)` → „×1 · Originaltempo (1 Std = 1 Std)", „×180 · 1 Std = 20 s" |
| **Vorgabe** | **×180** (unverändert zu `data/spielzeit.json:2`) |
| Wirkung | nur die Spieluhr (`main.py:7338`); Handbuchformeln bleiben unangetastet |
| Speicherort | privater Ordner über `spielzeit.setzen()` (`spielzeit.py:55–64`) — **nicht** im Spielstand, **nicht** im Bundle |
| Hinweiszeile | „VORSCHLAG — im Original nicht belegt; das Original läuft in Echtzeit (Handbuch S. 2)." |

**Warum ein Hinweis im Startmenü:** Der Faktor ist die einzige Zahl im Spiel, die eine
Spielgefühls-Entscheidung ist und **keine** Quelle hat. Eine Zeile genügt, damit sie später niemand
für belegt hält — genau der Fehler, den Register 46/55 schon einmal teuer gemacht haben.

**Warum ×1 sichtbar bleiben muss:** ×1 ist das Original. Solange die Stufe wählbar ist, kann jeder
die Vorlage erleben und der Vergleich „Original gegen Remake" bleibt möglich.

### 4c. Was dabei NICHT passieren darf (Fallstricke, alle im Code nachgesehen)

1. **Faktor nur einmal anwenden.** `_tick_loop` multipliziert bereits (`main.py:7338`). Ein zweiter
   Faktor im Limit oder in einer Anzeige verdoppelt das Tempo.
2. **Limit gegen `state.spielsekunden` prüfen, nie gegen `time.time()`** (`zeitbasis.py:3–6`).
3. **Off-by-one bei `self.day`:** `day` startet bei **1** und zählt erst nach 86400 s hoch
   (`main.py:2670–2672`). „15 Spieltage" heißt `spielsekunden >= 15 * 86400`, nicht `day > 15`.
4. **`spielende` wird gespeichert** (`main.py:2739`) und geladen (`2883`). Ein neuer Wert „zeitlimit"
   muss beim Laden und in `_render` (`7429`) behandelt werden — sonst steht nach dem Laden wieder
   „kein Sieg" in der Seitenleiste.
5. **Die Uhr steht, sobald `spielende` gesetzt ist** (`main.py:6323`). „Weiterspielen" muss
   `state.spielende = None` **und** das Limit auf „ohne" setzen, sonst ist die Partie eingefroren.
6. **Admin-Teststand umgeht `_pruefe_spielende`** (`main.py:7305–7306`). Das Limit dort ebenfalls
   inaktiv lassen, sonst sperrt sich der Testbetrieb selbst.
7. **Alte Spielstände haben kein Limit-Feld** → „ohne Limit". Keine Migration, kein Sonderfall.
8. **Zwei Editionen, zwei Einstellungsordner** (`spielzeit.py:55–64`). Das Startmenü muss denselben
   Weg über `spielzeit.setzen()` nehmen, sonst schreibt die öffentliche EXE in den Entwicklerordner.

### 4d. Wo es hingehört (Umsetzungsskizze, nicht ausgeführt)

- Neues Modul `src/laufziel.py`: `daten()`, `setzen()`, `abgelaufen(spielsekunden)`, `text()` —
  gleiche Bauform wie `spielzeit.py` (private Datei, gebündelte Vorgabe, atomares Schreiben).
- `main.py:3148–3188`: zwei Optionszeilen im Startmenü, Werte an `GameState` übergeben.
- `main.py:7310–7327`: dritter Ausgang `"zeitlimit"` in `_pruefe_spielende`.
- `main.py:7429`: dritter Anzeigezweig in `_render`.
- `main.py:3352`: zweites Label neben `lbl_tempo`.
- Prüfdateien: neue `tests/test_laufziel.py`; `tests/test_gpt_spielzeit_einstellungen_fix05.py`
  (6 Prüfungen, Tempo-Schreibweg) und `tests/test_startspiel.py` um je eine Prüfung „Startmenü setzt
  Tempo/Zeitlimit" erweitern.
- Register: `docs/PRUEFREGEL_ORIGINAL.md` neue Zeile „Zeitlimit-Option" mit Urteil
  **VORSCHLAG EIGENTÜMER ÜBERTRAGEN** und Verweis auf diese Datei.

---

## 5. Offene Fragen an Daniel

| # | Frage | Meine Empfehlung |
|---|---|---|
| 1 | Einheit des Limits: **Spieltage** oder Echtminuten? | Spieltage (tempo-unabhängig, Quellenwährung) |
| 2 | Vorgabe „ohne Limit" oder „15 Spieltage"? | „ohne Limit" — das Original kennt kein Ende |
| 3 | Nach dem Laufziel **weiterspielen** erlauben? | Ja, ein Knopf; sonst wird aus der Option eine Sperre |
| 4 | Limit im **Spielstand** (je Slot) oder global in den Einstellungen? | im Spielstand — zwei Partien dürfen verschieden lang sein |
| 5 | Tempo-Vorgabe ×180 beibehalten? (1 Spieltag = 8 Echtminuten, 1 Spielstunde = 20 s) | beibehalten, aber im Startmenü sichtbar machen |
| 6 | Darf die Hinweiszeile „VORSCHLAG, im Original nicht belegt" im Startmenü stehen? | ja, eine Zeile, kein Dialog |
| 7 | **UNGELÄRT:** Der PDF-Deckel nennt 01.09.2006, der Dateiname 2009 (`docs/original/00_QUELLEN.md`, Quellenkorrektur). Für diese Frage unschädlich (beide Fassungen sagen Echtzeit), für künftige Zitate aber zu beachten: Welche Fassung gilt als „2009"? | so lassen, Deckblatt-Zitat künftig mitnennen |
| 8 | **UNGELÄRT:** „Speedserver Armageddon mit 200-facher Geschwindigkeit" steht nur in einer Projektnotiz (`archiv/.../nebelseetal_research.md:16`), nicht in einer Originaldatei. Als Indiz führen oder streichen? | als **INDIZ (schwach)** führen, ausdrücklich ohne Originalbeleg |

---

## Belegstellen kurz (zum Nachschlagen)

- `docs/original/Spielanleitung_2009_Textfassung.txt` Z. 25–27 (Echtzeit), 29 (58 Stunden), 49–52
  (Spielziel), 93–96 (Urlaubsmodus/Kontolöschung), 210–213 (Rangliste), 422–423 (Forschungsdauer),
  503–504 (Ausbildungsstufe), 1103–1104 (GS), 1138–1141 (Auftragsdauer), 1190–1193 (Drosselung),
  1274–1276 (10 Kampfsequenzen)
- `docs/original/Spielanleitung_2005/beschreibung.php.txt` Z. 15–20 · `punktesystem.php.txt` Z. 33, 38–42
  · `rohstoffe.php.txt` Z. 20–23 · `einheiteninfo.php.txt` Z. 6
- `src/spielzeit.py` Z. 16–17, 34–35, 55–64, 89–98, 152–168 · `data/spielzeit.json` Z. 2, 10
- `src/main.py` Z. 2670–2672, 2720, 2856, 3148, 3178, 6323, 6328, 7310, 7338, 7429
- `src/punkte.py` Z. 275–305, 327–328 · `src/zeitbasis.py` Z. 3–6
