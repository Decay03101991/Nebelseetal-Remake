# Offene Fragen an Daniel — Stand 01.11.2026, 18:20

Gesammelt nach der Regel „eine Runde, nicht viele Einzelrufen“. Je Frage: Messlage, Wirkung,
Empfehlung zuerst. Antworten können frei formuliert werden, Nummern genügen.

Quellen: Übergabe `UEBERGABE_NEBELSEETAL_20261101_1743.md` Abschnitt 7, Prüfvermerk
`docs/audits/PRUEFVERMERK_GPT_TEXTPAKET_20261101.md`, Register `docs/PRUEFREGEL_ORIGINAL.md` 89–91.

---

## A. Blockiert die nächste Arbeit

### F-01 Freigabe für S-5 (Weltbild als Gelände)

**Messlage:** Register 91 ist entschieden, aber ausdrücklich als „NOCH NICHT GEBAUT“ geführt. Der Code
liefert heute 400 Felder ohne Gelände (`portalraum.anzeige_raster`). Der nächste Schnitt ist vollständig
vorgedacht: sieben Geländearten aus `data/gelaende.json` (Feld `haeufigkeit`, Summe 100), als 2×2-Blöcke,
stabiler Seed je Welt.

**Wirkung:** Ohne S-5 bleibt die Gelände-Aussage im Demo-Textpaket falsch (Prüfvermerk W-01). Mit S-5
stimmt sie.

**Empfehlung:** Freigeben. Es ist der einzige Schritt, der einen bereits entschiedenen Punkt in den Code
bringt.

---

## B. Preise

### F-02 Weltensprung: 5.000 Mana oder deine 500 plus Gold?

**Messlage:** Der Code bucht heute 5.000 Mana als Festpreis (`portalraum._MANA_WECHSEL`, aus
`portal.php` 2005 als Koordinatenwechsel belegt). Dein Vorschlag aus der Sammlung war 500 Mana plus
„ein wenig Gold“. Die Tempel-Bilanz liefert 5 Mana je Spielstunde auf Nebelsee — 5.000 Mana sind damit
rund 1.000 Spielstunden, 500 Mana rund 100.

**Wirkung:** Bestimmt, ob ein Weltensprung in der Demo überhaupt erreichbar ist. Bei 5.000 ist er für
einen normalen Spielverlauf praktisch unerreichbar.

**Empfehlung:** 500 Mana plus Gold, damit der Sprung in einer Partie erlebbar wird; die 5.000 bleiben als
belegter Originalwert im Register stehen. Entscheidung fällt in S-8.

### F-03 Goldpreis G für den Sprung

**Messlage:** Zahl fehlt. Gold entsteht nur über die Goldmine (Baukunst nötig). Ohne Zahl bleibt die
Formel in S-8 offen.

**Wirkung:** Ohne G ist der Preis unvollständig und der Text (S-18) nicht schreibbar.

**Empfehlung:** 100 Gold je Sprung als Vorschlag, im Register als VORSCHLAG markiert — änderbar, ohne
Code anzufassen.

---

## C. Demo-Auslieferung

### F-04 Fester `weltkarten_seed` für die veröffentlichte Demo

**Messlage:** Der Seed wird ein neuer Konfigurationswert in `data/welten.json` (S-5). Ohne festen Wert
sieht jede Installation andere Weltkarten.

**Wirkung:** Nur Optik, aber Screenshots, Release-Notizen und Anleitungen müssen zur ausgelieferten Karte
passen.

**Empfehlung:** Ein fester Wert in der ausgelieferten Datei, zum Beispiel aus dem Veröffentlichungsdatum
abgeleitet und im Register notiert.

### F-05 Das Wort „Demo“ im Titel führen?

**Messlage:** Empfehlung O-01 des Textpakets; alle Release-Texte tragen „Demo“ bereits.

**Wirkung:** Außenwirkung. „Nebelseetal Remake — Demo 0.9“ sagt sofort, dass Bot-Angriffe, Spionage und
Kartenziehung fehlen.

**Empfehlung:** Ja, „Demo“ im Titel und in der Versionsbezeichnung führen.

---

## D. Texte und Handbuch

### F-06 W-01: Gelände-Satz warten oder streichen?

**Messlage:** Fünf Stellen im Textpaket behaupten Gelände auf den Weltkarten.

**Wirkung:** Bleibt der Satz und S-5 kommt, ist er wahr. Kommt S-5 nicht vor der Veröffentlichung, ist er
eine Zusage über eine fehlende Funktion.

**Empfehlung:** An S-5 koppeln: keine Veröffentlichung des Handbuchs vor S-5, dann stimmt der Satz.

### F-07 Handbuch eigenständig veröffentlichen?

**Messlage:** Empfehlung O-02 des Textpakets: H-01 bis H-17 als eigenes Dokument neben dem Release.

**Wirkung:** Ein Dokument mehr zu pflegen; dafür ist das Spiel ohne Handbuch für neue Spieler schwer
zugänglich.

**Empfehlung:** Ja, als eine Datei neben dem Release, ohne Ingame-Ansicht.

---

## E. Begriffe und Mechanik

### F-08 Limbus ist doppelt belegt

**Messlage:** Limbus ist sowohl einer der sechs belegten Weltnamen als auch der Name der magischen Ebene,
in der alle Dimensionen liegen (`data/welten.json`).

**Wirkung:** Betrifft Anzeige und Spielertext; das Spiel umgeht die Frage heute.

**Empfehlung:** Limbus bleibt Weltname, die Ebene heißt im Text „der magische Limbus“ — zwei Wörter
statt einer Entscheidung.

### F-09 Die acht Entscheidungen des Verbund-Papiers (S-3, S-4, S-6)

**Messlage:** Stehen in `docs/design/VERBUND_FORSCHUNG_EINHEITEN_TRANSFER_20261101.md`, Abschnitt 7. Ich
lege sie vor, wenn S-3 drankommt — sie sind ohne den gebauten S-5-Kontext schwer zu beurteilen.

**Wirkung:** Betrifft Forschungsübernahme zwischen Dörfern und Dorftransfer.

**Empfehlung:** Gesammelt vorlegen, sobald S-3 beginnt, nicht jetzt am Stück beantworten.

### F-10 F-01 bis F-05 des S-7-Entwurfs

**Messlage:** Preis, Bot-Atmosphäre, Namen ab Spielbeginn, ausblendbare Hilfe, „zehn Minuten“ als
Orientierung. Geprüft in `docs/audits/PRUEFVERMERK_S7_S8_ENTWURF_20261101.md`.

**Wirkung:** Betrifft S-7 (Bots erlebbar). Mindestens F-01 (Preis) und F-03 (Namen) blockieren den Bau.

**Empfehlung:** Mit S-7 vorlegen — dann mit den gemessenen Bot-Zahlen daneben.

---

## F. Keine Entscheidung nötig, nur Arbeit

### F-11 Echte 24-Spielstunden-Messung der Mana-Bilanz

Die Tabelle im Prüfvermerk ist eine Rechnung aus Stundenwerten, keine Messung mit laufenden Ticks. Wird
gemessen, sobald S-5 und S-8 stehen; kostet keine Entscheidung.

### F-12 Bot-Ereignisquellen E-02 bis E-12 prüfen

Je Kennung nachsehen, welche Quelle heute wirklich liefert. `bottaktik` ist nachweislich nicht
angeschlossen — das ist S-7 selbst. Lesearbeit, keine Entscheidung.

---

## G. Systemseite

### F-13 Skill-Ergänzung vom 01.11. freigeben

Die Lehren der S-2c-Sitzung liegen unter `/skills pending` mit der Kennung `64d3ed88` und warten auf
deine Freigabe. Ohne Freigabe stehen sie nur in der Übergabe, nicht im Skill.

---

## Antworten — alle dreizehn Fragen beantwortet am 01.11.2026, 18:24–18:30

| Frage | Antwort | Folge |
|---|---|---|
| F-01 S-5 freigeben | **Ja, jetzt bauen** | Arbeit beginnt; Register 92 |
| F-02 Weltensprung-Preis | **500 Mana plus Gold**, 5.000 bleibt Originalwert | Einbau in S-8; Register 93 |
| F-03 Goldpreis G | **100 Gold** | Formel vollständig; Register 93 |
| F-04 `weltkarten_seed` | **Fester Wert**, aus dem Veröffentlichungsdatum | Wert beim Demo-Bau nachtragen; Register 94 |
| F-05 „Demo“ im Titel | **Ja, überall** | Release-Texte; Register 95 |
| F-06 Gelände-Satz | **An S-5 koppeln** | kein Handbuch-Release vor S-5; Register 96 |
| F-07 Handbuch eigenständig | **Ja, als eigene Datei neben dem Release** | Register 97 |
| F-08 Limbus | **Weltname bleibt, Ebene heißt „der magische Limbus“** | Register 98 |
| F-09 Verbund-Papier (acht Entscheidungen) | noch nicht gestellt | kommt mit S-3 |
| F-10 F-01…F-05 des S-7-Entwurfs | noch nicht gestellt | kommt mit S-7 |
| F-11 Mana-Messung über 24 Spielstunden | keine Entscheidung nötig | Arbeit nach S-5/S-8 |
| F-12 Bot-Ereignisquellen E-02…E-12 | keine Entscheidung nötig | Lesearbeit vor S-7 |
| F-13 Skill-Ergänzung `64d3ed88` | **Ja, freigegeben** | angewendet 18:34, Skill 753 → 781 Zeilen; Protokollzeile geschrieben |

**Zusätzliche Ansage Daniels am 01.11.2026, 18:37:** „es muss noch sehr viel umgesetzt werden bevor wir
eine demo online stellen können … ich möchte auf jedenfall ein möglichst weit umgesetztes testspiel
veröffentlichen als demo“ → Die Demo ist ein Testspiel mit möglichst vollständigem Umfang; Funktionen
gehen vor Release-Texten. Festgehalten als Register 99.
