# Original-Oberfläche — Befunde aus den GameStar-Screenshots (30.10.2026)

**Wozu:** Daniel: „wir haben mittlerweile so viele kleine Eindrücke und Screens und Bilder von
Original-Quellen, dass wir vieles daraus erschließen müssen." Diese Datei hält fest, was auf den
echten Screenshots **wörtlich** zu sehen ist — als Grundlage für den Nachbau der Oberfläche.
**Quelle:** `docs/original/karten/gamestar/` (GameStar-Artikel mit drei Original-Screenshots,
Varianten `_204` … `_1280`; gelesen wurden die größten Fassungen `_4.jpg`).
**Verfahren:** Bild gelesen (Vision), Beschriftungen wörtlich übernommen. Was nicht sicher lesbar
war, ist als „unklar" gekennzeichnet — nichts ergänzt.

---

## 1. Es gibt ZWEI Navigationsebenen (wichtigster Befund)

Ganz oben links steht ein **Aufklappmenü**, das die Ebene umschaltet:

| Ebene | Aufklapp-Eintrag | Linke Leiste (wörtlich, in Reihenfolge) |
|---|---|---|
| Reich/Portal | „Übersicht" | Übersicht · Portal · Diplomatie · Einstellungen · Ruhmeshalle · Gildehalle · **Voraussetzungen** · Nachrichten · Neuigkeiten · Anleitung · **Schlachtsimulator** · Forum · Chat · Spieler werben · *(Banner)* · Logout |
| Siedlung | „Siedlung" | Übersicht · Portal · Diplomatie · Einstellungen · Ruhmeshalle · **Gildenhalle** · Voraussetzungen · Nachrichten · Neuigkeiten · Anleitung · Schlachtsimulator · Forum · Chat · Spieler werben · Logout |

Beide Ebenen tragen **dieselbe** Leiste — die Welt-Menüpunkte stehen immer, gewechselt wird der
Inhalt (Portal-Karte bzw. Siedlungsansicht) über das Aufklappmenü oben links.

**Folge für unser Spiel:** Unsere Leiste mischt beide Ebenen in einer Liste (`Dorfzentrum`, `Lager`,
`Kaserne`, `Marktplatz`, `Gilde`, …, `Portal`, `Karten`, `Forschung`, …). Richtig wäre:
- **Immer sichtbar:** Übersicht, Portal, Diplomatie, Einstellungen, Ruhmeshalle, Gildehalle,
  Voraussetzungen, Nachrichten, Neuigkeiten, Anleitung, Schlachtsimulator, Forum, Chat,
  Spieler werben, Logout.
- **Nur innerhalb einer Siedlung / mit Gebäude:** Dorfzentrum, Lager, Kaserne, Stellmacher,
  Diebesgilde, Forschung, Marktplatz.
Damit wird auch Daniels Wunsch („Forschung erst ab Bibliothek") ohne Sonderregel erfüllt — er ist
im Original schlicht ein Siedlungs-Menüpunkt.
**Unklar:** ob das Aufklappmenü auch bei „Siedlung" die Siedlungsliste enthält und wie man zwischen
mehreren Siedlungen wechselt (im Screenshot ist nur eine Zeile „Siedlung" zu sehen).

## 2. Kopfleiste (beide Screenshots gleich)

- Links das Aufklappmenü („Übersicht" bzw. „Siedlung").
- Danach **zehn** Rohstoff-/Warensymbole, jedes mit Zahl und **Zuwachs in Klammern**,
  z. B. `10 (+ 1,00)`, `100 (+ 0,00)`. Unter jedem Symbol ein **roter Balken**
  (Lagerbalken, siehe Punkt 6).
- Keine Textbeschriftung an den Symbolen — nur Icons.

## 3. Portal-Seite (Screenshot `web_1838856`)

- Überschrift **„Portal"**, darunter: „Alle Reiche nach ihrer Lage im Limbus. Eure Koordinaten:
  **(15-18--9)**" → bestätigt das belegte Format **X-Y-Z**.
- Steuerzeile: „Aktuelle Dimension: **9**" · „Dimension wechseln" (Aufklappmenü mit 9) · Button
  **„Verschreibung"** (so gelesen; vermutlich „Verschiebung" — unklar).
- Hauptteil: **Gitter 20 × 20**, Y-Achse 20…1 (oben nach unten), X-Achse 1…20.
  Markierungen: **grüner Punkt** (eigenes Reich), **rote Punkte** (fremde Reiche).
  Das deckt sich mit der Spielanleitung 2005 (eigene Welt grün, fremde rot).
- Unten: **„Laufende Aufträge:"** mit „Keine laufenden Aufträge." ← Das ist die Stelle, an der
  später auch **laufende Truppenbewegungen** stehen (Daniels Wunsch C5).

## 4. Siedlungsseite (Screenshot `web_1838857`)

- Reiter über dem Inhalt: **„Siedlungsübersicht" · „Produktion" · „Verteidigung"**.
- Überschrift „Produktionsgebäude bauen" mit dem Satz „Eine Übersicht aller Gebäude, welche ihr
  errichten könnt." und der Aufforderung „Wählt das Gebäude aus, welches ihr errichten möchtet."
- Je Gebäude: **Button „[Gebäude] Bauen"**, danach **Beschreibungstext**, darunter die **Kosten**
  als Aufzählung.

| Gebäude | Kosten (wörtlich) | Beschreibung (wörtlich, gekürzt) |
|---|---|---|
| Holzfäller | 10 Holz · 5 Stein · 1 Siedler | „…versorgt Eure Siedlung mit Holz. Dieses findet er natürlich im Wald am besten, doch auch in der Steppe gibt es die eine oder andere bewaldete Stelle." |
| Steinmetz | 5 Holz · 10 Stein · 1 Siedler | „…versorgt Eure Siedlung mit Steinen. In den Bergen findet er freilich die besten Felsen, doch auch in den Hügeln lassen sich gute Felsen finden." |
| Jäger | 25 Holz · 25 Stein · 1 Siedler | „Der Jäger durchstreift Eure Wälder und versorgt die Siedlung mit Nahrung und Leder." |
| Haus | 80 Holz · 50 Stein | siehe Punkt 5 |

**Zu prüfen:** unsere Werte in `data/baupreise.json` gegen diese vier Zahlen halten. **Ergebnis der
Prüfung (30.10.): sie halten.** Unsere Datei führt genau diese Preise als **belegt aus demselben
Screenshot 1838857** (`preise.holzfaeller` = 10 Holz/5 Stein/1 Siedler usw.), samt widerlegtem
Altbestand (8/4) und der Regel „ein Gebäude kostet 1 Siedler, der dort arbeitet und nicht mehr zur
freien Bevölkerung zählt". Hier ist also **nichts zu ändern** — der Screenshot bestätigt den
Datenstand, statt ihn zu widerlegen.

## 5. Die Hausregel — sie erklärt Daniels Siedlerproblem

Wörtlich: „Häuser gewähren Euren Siedlern Unterschlupf. **Jedes Haus kann bis zu 5 Siedler
beherbergen.** Ist die maximale Anzahl Siedler erreicht, kommen keine Neuen mehr hinzu. **Zu den
Siedlern zählen natürlich nicht diejenigen unter ihnen, die in einem anderen Gebäude arbeiten.
Diese belegen keinen Platz in euren Häusern, sondern wohnen in dem Gebäude, in dem sie arbeiten.**"

**Folge:** Siedler, die in einem Gebäude arbeiten, zählen **nicht** gegen die Siedlergrenze der
Häuser. In Daniels Spielstand (30.10.) standen 10 Siedler bei Grenze 10 und **kein Haus** — der
Zuwachs war deshalb zu Recht blockiert, aber die Anzeige verschweigt den Grund („kein Haus").
Zu prüfen ist, ob unsere Siedlergrenze Arbeiter mitzählt; wenn ja, ist das ein Rechenfehler gegen
diesen Beleg.

## 6. Lagerbalken (neu, bisher nicht umgesetzt)

Unter jedem Rohstoffsymbol liegt im Original ein **roter Balken** — offenbar die
**Speicherkapazität**. Dazu passt Daniels Beobachtung „Lagerkapazität reicht nicht": es gibt im
Original eine Kapazitätsgrenze, die unsere Umsetzung **gar nicht** kennt (im Code existiert keine
einzige Kapazitätsregel; nachgewiesen am 30.10.2026). Was ein „Lager" an Kapazität bringt, steht
noch **nicht** belegt da — im Handbuch suchen, bevor es gebaut wird.

## 7. Punkte — immer sichtbar in der Seitenleiste

Unten links, dauerhaft: **„Eure Punkte: Forschung 0 · Krieg 0 · Gesamt 0"**. Unsere Anzeige steht
im Dorfzentrum; im Original ist sie Teil der Leiste.

---

## 8. Was noch offen ist

- Screenshot `web_1838855`: Auswertung **fehlgeschlagen** (der Bildweg lief auf ein Modell, das
  keine Bilder kann: „models/deepseek-flash is not found"). Muss mit einem bildfähigen Modell
  wiederholt werden.
- 244 Einzelbilder aus dem Handbuch (`docs/original/handbuch_bilder/`) sind **nicht** ausgewertet.
  Sie sind die Quelle für Gebäudeansichten, Kampfabläufe und Menübeschriftungen.
- Die 35 Bilder unter `docs/original/karten/` (Website) sind nur teilweise zugeordnet.
