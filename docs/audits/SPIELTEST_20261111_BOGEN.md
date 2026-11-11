# Spieltest 11.11.2026 — Daniels Testbogen, ausgewertet

**Was geprüft wurde:** `Nebelseetal_Pre_Release_V_0.0.3.exe` (83.342.035 Byte, SHA256 `4124b335…`), Test von
**17:30 bis 18:11** (40 Minuten), Bildschirm **1920 × 1080 bei 125 % Skalierung**.
**Bogen:** `ANLEITUNG_UND_TESTBOGEN_GEFUELLT.txt` (13.576 Byte, SHA256 `1c0187b7…`), wortgetreu abgelegt.
**Bilder:** neun Aufnahmen in `screenshots/` — vier davon habe ich selbst angesehen (unten mit ★).

**Stand des Bogens:** **44 Punkte beantwortet**, **3 leer** (`A0` Hash nicht geprüft, `C01` und `C02` zum
Goldrahmen), Block E nur mit zwei eigenen Tests, Block F ohne Eintrag. Leere Punkte bleiben leer und werden
nicht ergänzt.

---

## 1. Das Urteil in einem Satz

**Das Spiel ist spielbar und der Frischstart funktioniert** (Tor, Passwort, neuer Stand, Speichern/Laden,
Bauen, Forschung). **Der größte Einzelpunkt ist die Gestaltung** — wörtlich: »Designumsetzung«. Alles, was er
beanstandet, ist **Anzeige**, nicht Mechanik.

## 2. Was funktioniert (bestätigt)

| Punkt | Antwort |
|---|---|
| Start und Tor (A1–A3) | Tor erscheint in **etwa 1 Sekunde**, Passwort öffnet, **kein alter Spielstand** sichtbar (A6) |
| Weg in die Partie (A4/A5) | »schön durchgeleitet bis zum ersten Bau«; Fraktionswahl vorhanden (er wählte elfisch) |
| Erste Schritte (B01–B04) | Siedlung wird gegründet, Startdorf ist immer dasselbe, **10 Siedler**, **kein Gebäude im Baumenü vermisst** |
| Preis wird einmal abgezogen (B05) | **1590 → 1582 Holz** beim Holzfäller: genau ein Abzug, und die Vorräte steigen weiter |
| Forschung (B06/B07) | Wagenbau Stufe 1, Dauer **1 h ingame**, Restzeit läuft herunter — **aber unscheinbar** (siehe 3.7) |
| Speichern und Laden (B10) | »klappt korrekt« |
| Keine Zahl ohne Einheit (B12) | keine gefunden |
| Schmale Fenster (D1/D2/D4/D5/D6) | Legenden- und Knopfzeile bei 1024 × 720 **ganz sichtbar**; beim Verkleinern bricht zuerst die Zeile mit Beenden/Profil/Skin; kein Wort mitten durchgeschnitten |

## 3. Die Befunde aus dem Test (in seiner Reihenfolge der Wichtigkeit)

### 3.1 Gebäudeansichten zeigen ihre Hintergründe nicht — die gemalten Bilder verschwinden

**Sein Wort (B09):** »egal ob Forschung, Stellmacher oder Diebesgilde, sobald sie gebaut waren, zwar gut
angezeigt im Menü, aber deren Hintergründe waren nicht zu sehen«. **E1:** »Hintergrundbilder ganz ganz schwer
im Hintergrund, kaum erkennbar«.
**★ Selbst angesehen** (`Diebesgilde_Screenshoot.png`): der Hauptbereich ist ein dunkler, konturloser Verlauf
ohne jedes erkennbare Bild; Text und Tabelle nehmen 70–80 % der Fläche ein. Der einzige gestaltete Bereich
ist die Kopfleiste.
**Das ist der schwerste Punkt** — es ist genau die Bildwelt, für die Chris geliefert hat. Ursache im Code zu
suchen (`_ansicht_hintergrund`, Deckkraft der Textblöcke), nicht am Bild.

### 3.2 Die Ressourcenleiste ist »ganz schrecklich« — und zwei Rohstoffe fehlen ganz

**Sein Wort (D3):** »ganz schrecklich, außerdem wird weder Wolle noch Leder als Ressource angezeigt, das muss
komplett neu designed werden«. **B09:** »Ganz schlimm war der Ressourcenbalken ingame«.
**★ Selbst angesehen** (`Ressourcenbalken_Schrecklich_Screenshot.png`): Die Leiste ist auf die volle
Fensterbreite gezogen, zwischen den acht Anzeigen sitzen **28 leere goldene Kreisverzierungen** als Füllung;
das Panoramabild dahinter ist in die Breite verzerrt. Sichtbar sind acht Werte — **Wolle und Leder sind nicht
dabei**, obwohl `src/main.py:3118` neun Rohstoffe führt (`holz, stein, metall, mana, nahrung, gold, wolle,
leder, pferde`).
**Befund:** Die Anzeige ist breitengetrieben statt inhaltsgetrieben, und sie zeigt weniger als das Modell hat.

### 3.3 Die neun Menü-Icons sind nicht erkennbar

**C06:** »Leider zu klein und kaum zu erkennen«, **C07** auf die Frage, welches unklar ist: **»alle«**.
Neun erkannte Icons: 0 von 9. Das ist ein klarer Auftrag: größer, oder mit Beschriftung.

### 3.4 Das Lager: die Felder sind viel zu groß

**E2:** »viel zu große Anzeigefelder für Einheiten und Items, alles unsortiert, unübersichtlich, nur die Icons
selbst sind gut und passen« (`Siedlungs_Lager_Felder_zu_groß.png`).
**★ Selbst angesehen:** sechs Spalten, jede Kachel zu etwa **80–90 % leere braune Fläche**, Icon und Zahl
winzig darin. **Widerspruch zur Antwort:** die Waren sind **alphabetisch** sortiert (Armbrust, Bogen, …), die
Einheiten thematisch gruppiert (Fußvolk, Fernkampf, Diebe, Transport, Belagerung). »Unsortiert« stimmt also
nicht — das Problem ist allein die Größe der Kacheln.

### 3.5 Weltkarte: der goldene Rahmen schneidet in die vier Eckkacheln

**C10:** »dort siehst du, dass die Geländeecken über den Rahmen stehen, das sieht wirklich schlecht aus«.
**★ Selbst angesehen** (`weltkartenproblem_Screenshot.png`): Es ist **umgekehrt** — keine Kachel steht über
den Rahmen hinaus. Der Rahmen hat **innen abgerundete Ecken**, und diese Rundung **überdeckt die Ecken der
vier Eckkacheln**. Entlang der geraden Kanten liegt alles bündig. Der Befund bleibt berechtigt, nur die
Richtung ist eine andere: der Rahmen passt nicht zum Raster.

### 3.6 Das Portal-Kopfband erreicht den rechten Rand nicht

**C11:** »ist scharf, muss aber bei großem Spielfenster auch bis zum rechten Rand gehen«.
**★ Selbst angesehen** (`screenshot_portal.png`): Das Band ist scharf, endet aber **nach etwa einem Drittel
der Breite**; rechts bleibt eine große leere Fläche.

### 3.7 Was unscheinbar ist, obwohl es wichtig ist

- **Forschung (B07):** »total unscheinbar und klein, obwohl es ABSOLUT WICHTIG ist im Spielablauf«.
- **Götterschutz (B11):** »Nein, nicht auffällig genug, falls es irgendwo sein sollte«.
- **Wallbau (B11):** »noch viel zu unscheinbar designed«.
- **Marktplatz (C08):** Kennzeichen links vom Titel — »sieht echt gut aus«, »leider trotzdem zu viel braune
  Fläche, da muss noch ein Hintergrundbild rein« (`Marktplatz_Screenshot.png`).

### 3.8 Die Fraktionswahl hat im Spiel keine Folge

**C12:** Zwei Bildstile nebeneinander stören ihn **nicht** — aber: »ich wähle anfangs elfisch und es gibt
später keinerlei Bezug mehr dazu. Vielleicht sollten dann auch meine Gebäudemenüs elfisch designed werden,
bzw. bei anderer Fraktionswahl ein anderes Design«. Das ist ein **Inhaltsvorschlag**, nicht ein Fehler —
und er passt zur vorhandenen Bildwelt (sechs Häuser mit eigenen Wappen).

### 3.9 Was er ausdrücklich gelobt hat

Goldrahmen an den Geländekästchen (C03 »ja und sehr gut gemacht«, C04 »gleich und so gewollt«, C05 »passt«),
Marktplatz-Kennzeichen (C08), Icons im Lager (E2), und der Frischstart selbst: **»zügige Bebauung der ersten
Karte«** (G3).

## 4. Was NICHT beantwortet ist

`A0` (Hash der EXE per `certutil`), `C01` und `C02` (Goldrahmen sichtbar/gerade — er hat sie sinngemäß in C03
bis C05 beantwortet), `E3` bis `E5`, `F1` bis `F3` (keine Fehlermeldung, kein Absturz). `0.3`
(Fenstergröße) konnte er nicht beantworten — kein Vorwurf, die Angabe ist technisch.

## 5. Die Arbeitsliste, die aus dem Test folgt

**Stufe A — Gestaltung, was er zuerst will (G2: »Designumsetzung«):**

| Nr | Aufgabe | Beleg |
|---|---|---|
| A1 | Gebäudeansichten: die gemalten Hintergründe sichtbar machen (Deckkraft/Aufbau der Textblöcke prüfen) | B09, E1, ★Diebesgilde |
| A2 | Ressourcenleiste neu: nicht breitengetrieben strecken, Wolle und Leder aufnehmen, Verzierungen nur als Rand | D3, B09, ★Ressourcenbalken |
| A3 | Menü-Icons größer oder beschriftet (heute 0 von 9 erkannt) | C06, C07 |
| A4 | Lager: Kacheln klein, Dichte hoch, Icons behalten | E2, ★Lager |
| A5 | Weltkarte: Rahmen und Raster zusammenbringen (Ecken) | C10, ★Weltkarte |
| A6 | Portal-Kopfband bis zum rechten Rand | C11, ★Portal |
| A7 | Forschung, Götterschutz, Wallbau sichtbarer machen | B07, B11 |
| A8 | Marktplatz: Hintergrundbild statt brauner Fläche | C08 |

**Stufe B — Inhaltsvorschlag:** fraktionsabhängige Gebäudemenüs (C12) — Daniels Idee, seine Entscheidung.

**Stufe C — Mechanik:** nichts aus diesem Test. Der Bogen hat **keinen** Mechanik-Fehler gefunden;
`B05` (Preis genau einmal) bestätigt die Buchung, `B10` (Speichern/Laden) ist in Ordnung.

## 6. Belege

- Bogen (gefüllt): `docs/eingaenge/LLM_20261111_SPIELTEST/ANLEITUNG_UND_TESTBOGEN_GEFUELLT.txt`,
  13.576 Byte, SHA256 `1c0187b7921e5175…`
- Bilder: neun Dateien in `docs/eingaenge/LLM_20261111_SPIELTEST/screenshots/` (0,3 bis 1,4 MB);
  selbst angesehen: Ressourcenbalken, Diebesgilde, Weltkartenproblem, Portal, Lager
- Testzeit: 17:30 bis 18:11 (Bogen 0.4 und G4), Gerät: 1920 × 1080 bei 125 % (Bogen 0.1/0.2)
