# AUFTRAG 3 an das starke Chat-Modell — Spionage und Kampfplanungsseite

**Für:** Daniels großes GPT-Chat-Modell. **Von:** Hermes (Weltenfresser), 01.11.2026.
**Ergebnis:** EIN Markdown-Dokument, das Daniel zurückgibt. Kein Code, keine Dateiänderung.

## 0. Rolle und Grenze

Du bist **Entwerfer für Spielregeln**. Du lieferst entscheidbare Regeln, Randfälle und Texte; ein
anderer baut sie. Du erfindest **keine** Spielwerte und **keine** Dateipfade. Was nicht in diesem
Auftrag steht, ist für dich `UNBEKANNT — von Hermes zu liefern`.

**Wichtig für dein Bild vom Spiel:** Dieses Paket ist der **letzte** Schritt einer langen Reihe. In
diesem Entwicklungsstand **greifen die Bots nicht an** — es gibt sechs Bots mit je einem Dorf, fester
Position, ohne Taktik. Die Kampfplanungsseite plant also **Angriffe des Spielers**, nicht Verteidigung
gegen Bot-Angriffe. Baue nichts, was einen Bot-Angriff voraussetzt.

## 1. Die belegten Tatsachen (nichts davon ändern)

| Gegenstand | Stand (belegt) |
|---|---|
| Spielraum | Dörfer auf 20 × 20-Weltkarten (sechs Namen: Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus); die eigene Siedlung ist eine 10 × 10-Karte; ein Spieler hat höchstens sechs Dörfer, global über alle Weltkarten |
| Reisen | Jeder Angriff **reist**: Truppen sind während des Marsches nicht im Dorf, gekämpft wird bei der **Ankunft**, die Beute kommt mit den Überlebenden zurück. Die Reise kostet **Gold, Nahrung und Mana**; Holz und Stein bleiben unberührt. Die Dauer hängt an der Entfernung in Feldern (eine Einheit „Sekunden je Feld“ existiert im Code, der Wert ist Sache des Balancings — hier `UNBEKANNT`) |
| Beute | **gestaffelte Beute ist die eine Wahrheit**: ein Anteil an der mitnehmbaren Menge, gedeckelt durch die **Karrenladung**; es gibt keine zweite Beuteformel |
| Wall | zehn Ausbaustufen; die Vorprüfung einer Schlacht rechnet mit **Schlagkraft**, nicht mit Angriffswert; ein zu schwacher Trupp wird **gewarnt**, nicht abgelehnt — entschieden wird bei der Ankunft |
| Verluste | nur der **Verlierer** verliert einen Teil seiner Karren und Belagerungswaffen; Fluchtchance wächst mit der Zahl der Kampfsequenzen; ein Unentschieden kostet nichts |
| Stationieren | überall frei, auch für Einheiten, die das Dorf selbst nicht bauen kann; **stationierte Truppen verteidigen mit** |
| Spionage (Daniel, Anhang 3) | Der Späher **reist als Auftrag** (Hin- und Rückweg, Bericht im **Postfach**, kann scheitern). Der Bericht ist **exakt**: Truppenzahl und Wallstufe stehen genau darin, keine Spannen, keine Schätzformel. Er scheitert **nur, wenn das Ziel stark verteidigt ist** |
| Spionage-Einheit | die **bestehende Kundschafter-Einheit** aus den Daten benutzen — keine neue Zahl, keine neue Einheit erfinden |
| Spionage im Fahrplan | **zusammen mit der Kampfplanungsseite** — der Bericht ist die Grundlage der Planung |
| Kampfplanungsseite (Daniel, Anhang 3) | **Ziel oder Ziele wählen, Reisezeit und Kosten anzeigen**; der erwartete Ausgang kommt **aus dem Spionagebericht**, der auch stationierte Truppen und Wallstufe zeigt |
| Götterschutz | 7 Tage oder bis zum ersten Kriegspunkt; er endet mit **einer Nachricht**, es gibt keine Daueranzeige |
| Anzeige-Begriffe | Weltkarte, Weltensprung (nicht „Dimension“); Dorfzentrum ist Menüpunkt **und** Lager |

## 2. Deine Aufgabe — sechs Teile

### Teil 1 — Der Spionage-Auftrag als Regel
Beschreibe ihn wie einen Vertrag: **wer reist** (welche Einheit, wie viele), **was er mitnimmt**,
**was er kostet** (nur die Posten, die schon belegt sind: Gold, Nahrung, Mana — Beträge `UNBEKANNT`),
**wann er ankommt**, **was bei Ankunft geprüft wird**, **wann er zurückkommt**, **was der Spieler
sieht**, **was passiert, wenn das Dorf währenddessen umzieht** (die Regel „laufende Aufträge bekommen
die neue Position“ gilt).
Tabelle: `Frage | Regel | Begründung | UNBEKANNT bleibt`.

### Teil 2 — „stark verteidigt“: eine entscheidbare Schwelle
Der Satz steht fest, die Zahl fehlt. Liefere **drei Varianten** und **eine Empfehlung**:
- A) reine Wallstufe (z. B. ab Stufe X von 10),
- B) reine Zahl stationierter Truppen,
- C) beides zusammen, als Formel aus vorhandenen Größen (Schlagkraft der Verteidiger gegen
  Schlagkraft des Spähers).
Nenne für jede Variante: **was der Spieler lernt** (wann er einen Bericht bekommt), **was sie
kaputt macht** (z. B. „nie ein Bericht gegen ein Dorf mit Wall 10“) und **welche Zahl du bräuchtest**,
um sie zu setzen. Keine Zahl erfinden — `VORSCHLAG` mit Begründung ist erlaubt, `BELEGT` nicht.

### Teil 3 — Der Spionagebericht
Tabelle: `Was steht im Bericht | Genauigkeit | Wann fehlt es | Warum`. Pflichtfelder: Truppenzahl,
Wallstufe, ob das Dorf Bots gehört, Koordinate und Weltkarte. Kläre ausdrücklich: Was zeigt der
Bericht, wenn der Späher **abgewehrt** wird? (Daniel: exakt nur bei Erfolg — ein abgewehrter Bericht
darf keine erfundene Zahl tragen.) Wie viele Berichte bleiben im Postfach, veralten sie, und was
passiert, wenn der Spieler nach dem Bericht baut?

### Teil 4 — Die Kampfplanungsseite
Ein Ablauf Schritt für Schritt, so wie der Spieler ihn bedient:
**Ziel wählen** (eines oder mehrere — Daniels Wortlaut sagt „Ziel oder Ziele“) → **Truppen wählen**
(nur aus dem Ortslager des gewählten Dorfes, inklusive dessen, was die Akademiestufe zulässt) →
**Reisezeit und Kosten anzeigen** → **erwarteter Ausgang** (aus dem Bericht) → **Bestätigung** →
**Auftrag reist** → Ankunft → Kampfbericht → Heimkehr mit Beute.
Je Schritt: `Schritt | Was der Spieler sieht | Was der Kern prüfen muss | Was NICHT passieren darf`.
Pflichtfragen, die du beantworten musst:
- Was passiert, wenn **kein** Spionagebericht vorliegt?
- Was, wenn der Bericht **älter** ist als der letzte Bau des Ziels?
- Wie wird „erwarteter Ausgang“ dargestellt, ohne einen Sieg zu versprechen?
- Was ist gesperrt: Dorf mit laufendem Auftrag, Ziel in einer anderen Weltkarte, zu wenig Gold/Nahrung/Mana?
- Gilt der Götterschutz des **Ziels** oder nur der eigene?

### Teil 5 — Texte (deutsch, je eine Zeile, die Zahl steht im Satz)
1. Späher entsandt (mit Ankunftszeit), 2. Späher angekommen (Bericht oder Abwehr), 3. Bericht im
Postfach (Truppenzahl, Wallstufe), 4. Abwehr, 5. Planungsseite ohne Bericht, 6. Planungsseite mit
veraltetem Bericht, 7. Angriff bestätigt (Truppen, Ziel, Reisezeit, Kosten), 8. Ankunft mit Ergebnis,
9. Heimkehr mit Beute, 10. Sperren (drei Fälle aus Teil 4).
Regel: keine vagen Wörter („einige“, „reichlich“), keine Drohung, kein Pathos.

### Teil 6 — Prüfplan und offene Fragen
Tabelle `Regel | Wache (Name) | Was sie zusichert | Welche alte Wache dadurch rot wird`.
Danach **höchstens 8 offene Fragen an Daniel**, jede mit **Empfehlung zuerst**, und ein Abschnitt
„Was ich nicht wissen kann“.

## 3. Formregeln

- **Deutsch**, Tabellen, keine Emojis, **200–300 Zeilen**, kein Vorwort, kein Schlussgeplänkel.
- Urteil je Aussage: **BELEGT** (Abschnitt 1) / **VORSCHLAG** (deine Empfehlung) / **UNBEKANNT**.
- **Keine erfundenen Zahlen und keine erfundenen Einheitennamen** — die Kundschafter-Einheit steht
  schon in den Daten, alles andere wäre eine zweite Wahrheit.
- Keine Codeblöcke, kein Pseudocode, keine Dateipfade.
- Abschnitte in dieser Reihenfolge: 1 Spionage-Auftrag, 2 Schwelle, 3 Bericht, 4 Planungsseite,
  5 Texte, 6 Prüfplan, dann Offene Fragen und Was ich nicht wissen kann.

## 4. Was Hermes damit tut

Ich prüfe jede Regel gegen Code und Handbuch, entscheide die Schwelle **mit Daniel** (sie ist eine
Spielbalance-Frage, kein technisches Detail) und baue danach das Paket „Spionage + Kampfplanungsseite“
als **einen** Schritt: eine Prüfdatei je Regelgruppe, voller Sammellauf, neue EXE, ein Commit.
Was du als `UNBEKANNT` markierst, wird nicht gebaut, sondern Daniel vorgelegt.
