# Entwurf: Navigation in zwei Ebenen (nach dem Original)

**Grundlage:** Screenshots `docs/original/karten/gamestar/web_1838856_4.jpg` und `web_1838857_4.jpg`,
ausgewertet in `docs/quellen/ORIGINAL_UI_BEFUNDE.md`. Kein geratener Aufbau — die Listen unten sind
wörtlich von den Bildern.

## Was das Original macht

1. Oben links ein **Aufklappmenü** mit der aktuellen Ebene: **„Übersicht"** (Reich/Portal) oder
   **„Siedlung"**.
2. Die **linke Leiste ist in beiden Ebenen dieselbe** und enthält nur Reichs-Menüpunkte:
   Übersicht · Portal · Diplomatie · Einstellungen · Ruhmeshalle · Gildehalle · Voraussetzungen ·
   Nachrichten · Neuigkeiten · Anleitung · Schlachtsimulator · Forum · Chat · Spieler werben ·
   Logout.
3. Der **Inhalt** wechselt mit der Ebene: Portal zeigt die Dimensionskarte (20×20, farbige Punkte),
   Siedlung zeigt die Reiter **Siedlungsübersicht · Produktion · Verteidigung** mit den
   Gebäuden und ihren Baukosten.
4. Unten links dauerhaft: „Nebelseetal unterstützen", „Neue Nachrichten", **„Eure Punkte:
   Forschung · Krieg · Gesamt"**.

## Was unser Spiel heute macht (Ist)

Eine einzige Liste mit 17 Punkten, die beide Ebenen mischt:
`Dorfzentrum · Lager · Kaserne · Marktplatz · Gilde · Nachrichten · Portal · Karten · Forschung ·
Diplomatie · Einstellungen · Ruhmeshalle · Anleitung · Kampfsimulator · Forum · Chat · Spieler werben`
(seit 30.10. sind Kaserne und Forschung zusätzlich an ihr Gebäude gebunden.)

## Vorschlag (Umbau in vier kleinen Schritten)

**Schritt 1 — Ebenen-Schalter, ohne Inhalte zu ändern.** Oben links ein Aufklappmenü
„Übersicht / Siedlung". Es setzt `self.ebene` und rendert neu. Noch keine Umbenennung, keine
Filterung: reine Mechanik, prüfbar über eine neue Wache (beide Ebenen rendern 17 bzw. 17 Punkte).

**Schritt 2 — Leiste je Ebene.** Neue Funktion `menu_fuer_ebene(settlements, ebene)`, die auf
`menu_sichtbar()` aufsetzt:

| Ebene „Übersicht" (immer) | Ebene „Siedlung" (Gebäude nötig) |
|---|---|
| Übersicht, Portal, Diplomatie, Einstellungen, Ruhmeshalle, Gildehalle, Voraussetzungen, Nachrichten, Neuigkeiten, Anleitung, Schlachtsimulator, Forum, Chat, Spieler werben | Dorfzentrum, Lager, Marktplatz, Siedlungskarte, Kaserne (Kriegerakademie), Stellmacher, Diebesgilde, Forschung (Bibliothek) |

**Schritt 3 — Beschriftungen an das Original angleichen.** Die Screenshots schreiben
**„Schlachtsimulator"** (wir: „Kampfsimulator"), **„Gildehalle"/„Gildenhalle"** (wir: „Gilde",
„Gildehalle"), **„Neuigkeiten"** und **„Voraussetzungen"** (bei uns gar nicht vorhanden).
`MENU_ITEMS` wird dabei **nicht** überschrieben, sondern um eine Umbenennungs-Tabelle ergänzt
(`MENU_ANZEIGE = {"Kampfsimulator": "Schlachtsimulator", ...}`) — die belegte Liste bleibt lesbar.
**Achtung:** `tests/test_oberflaeche_original.py` vergleicht `MENU_ITEMS` mit dem Original-Muster;
die Umbenennung muss dort als *Anzeige* geprüft werden, nicht als Liste.

**Schritt 4 — Punkte in die Leiste.** „Forschung / Krieg / Gesamt" dauerhaft unten links, gespeist
aus `state.punktestand()` (eine Quelle). Heute steht das nur im Dorfzentrum.

## Prüfzusagen je Schritt

- Nach Schritt 1: beide Ebenen lassen sich umschalten, jede Ansicht rendert ohne Fehler
  (`tests/test_gui_fehler.py` muss weiter grün sein, 18 Ansichten).
- Nach Schritt 2: eine neue Wache `tests/test_navigation_ebenen.py` belegt je Ebene die erwartete
  Liste **und** dass ein Siedlungs-Menüpunkt ohne Gebäude fehlt.
- Nach Schritt 3: `tests/test_oberflaeche_original.py` prüft zusätzlich die Anzeige-Tabelle.
- Nach Schritt 4: die Punkte in der Leiste stimmen mit `state.punktestand()` überein.

## Was NICHT in diesem Entwurf steht

- Wie man zwischen **mehreren Siedlungen** umschaltet (im Screenshot nicht sichtbar) — offen.
- Was der Menüpunkt **„Voraussetzungen"** anzeigt — offen (Register in `docs/PRUEFREGEL_ORIGINAL.md`).
- Die Siedlungsansicht als **Karte** (wir haben sie schon) gegen die Reiter-Ansicht des Originals —
  beides ist vereinbar: Reiter „Produktion/Verteidigung" können auf unsere Karte verweisen.
