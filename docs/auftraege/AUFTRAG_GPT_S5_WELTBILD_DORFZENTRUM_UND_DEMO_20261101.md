# AUFTRAG an ein starkes Chat-Modell — Weltbild (S-5), Dorfzentrum als Lager (S-2c) und Demo-Checkliste

**Stand des Auftrags:** 01.11.2026, 12:30. **Auftraggeber:** Daniel Kössl, über Hermes (Weltenfresser).
**Arbeitsstand des Projekts:** Commit **`8d100a2`** (Register 88), Arbeitsbaum leer.
**Wichtig für dich:** Das öffentliche GitHub-Repo steht auf **`954097aa`** (Release 31.10.) und ist
**nicht** der Arbeitsstand. Wenn du nur das Repo siehst, prüfst du Code, der sechs Schnitte älter ist.
Alles, was du hier als „heute im Code“ liest, ist am 01.11.2026 gemessen; verlasse dich auf diese Angaben
und kennzeichne alles andere als Annahme.

---

## 0. Rolle und Grenze

Du bist **Entwurfs-Autor**, nicht Umsetzer. Du lieferst ein Papier mit prüfbaren Regeln, wörtlichen
Spielertexten und offenen Entscheidungen. Du änderst **keinen** Code, startest **keine** Builds, machst
**keine** Commits. Was du als BELEGT kennzeichnest, muss eine Quelle im Projekt haben (Datei und Zeile
oder ein Zitat aus dem Handbuch); alles andere ist VORSCHLAG oder UNBEKANNT. Keine Zahl ohne Quelle.

## 0a. Wer dein Papier umsetzt — und was das für dein Papier bedeutet

**Umsetzendes Modell: `deepseek-v4-flash`** (schnell, klein, arbeitet in einem Zug). Vorgabe Daniel
01.11.2026. Daraus folgt für jeden Teil:

* **Prüfbare Regeln ohne Auslegung.** Keine „man könnte“, keine Alternativen im Regeltext. Eine Regel ist
  ein Satz, den ein Prüfskript nachrechnen kann (Zahl, Grenzfall, Meldung).
* **Nur Standardbibliothek.** Keine neuen Pakete, kein neues Datenbankschema, keine Migration alter
  Spielstände (Daniel: Teststände dürfen brechen).
* **Jeder Teil in EINEM Arbeitsgang.** Wenn ein Teil nicht in einem Zug umsetzbar ist, ist er zu groß —
  teile ihn selbst und sage, in welcher Reihenfolge.
* **Spielertexte wörtlich.** Deutsche Sätze, die im Spiel erscheinen, stehen im Papier ausformuliert mit
  Platzhaltern in `{geschweiften Klammern}`. Keine englischen Reste, keine Emoji.
* **Jede Regel ohne Fenster prüfbar.** Beschreibe zu jeder Regel die Wache: was wird gesetzt, was wird
  gelesen, was darf NICHT passieren.
* Knapp. Tabellen statt Fließtext, keine Wiederholung des Auftrags.

---

## 1. Gemessene Tatsachen (nicht raten, nicht ändern)

| Gegenstand | Stand heute | Belegstelle |
|---|---|---|
| Portalansicht | zeigt oben die sechs belegten Weltkarten (Liste mit Nummer, Name, Status), darunter ein 20 × 20-Kästchen der aktuellen Welt; ein Klick wählt ein Feld (`portal_auswahl`), es wird **nichts** übertragen | `src/main.py`, `NebelseetalApp._render_portal`, `_portal_feld_waehlen` |
| Kästchen-Daten | `portalraum.anzeige_raster(index, radius, eigene)` liefert 400 Felder mit `x, y, z, eigen, status, farbe`; gefärbt wird nach der **Bannerfarbe** der Welt (eigene Welt grün, fremde rot, belegt aus portal.php 2005), **nicht** nach Gelände | `src/portalraum.py` |
| Weltkartenliste | `portalraum.weltkarten(eigene_nummern, unterwegs)` — sechs Zeilen mit `nummer, kennung, name, spielbar, status, status_text, farbe, waehlbar, grund` | `src/portalraum.py` |
| Zählweisen | Spielstand führt die 1-basierte **Nummer** (Kennung `d04` = 4); die Rechenfunktionen in `portalraum` den **Index** 0..19; Umrechnung an einer Stelle: `nummer_von`, `kennung_von`, `index_von`, `nummer_von_index` | `src/portalraum.py` |
| Startwelt | **Midgard** (Nummer 4), Daten in `data/welten.json` (`startwelt`, `weltkarten_spielbar`: Midgard und Valhalla) | `src/welt.py` |
| Sperre | Weltensprung gesperrt, solange Aufträge unterwegs sind (`auftraege.laufende`), Uhr ist die Spieluhr | `src/main.py`, `_unterwegs_anzahl` |
| Dorfzentrum | Menüpunkt „Dorfzentrum“ zeigt die Übersicht (`_render_overview`); Menüpunkt „Lager“ zeigt Bestände (`_render_storage`) | `src/main.py` |
| Dorfübersicht | `wirtschaft.dorf_uebersicht(siedlung, forschung_level, siedler_bindend)` liefert Gebäude, Anzahl, Ertrag je Stunde, Anteil | `src/wirtschaft.py` |
| Ortsbestand | `ortsbestand_text(siedlung)` liest NUR `Settlement.vorraete`/`bevoelkerung` (lokales Lager) | `src/main.py` |
| Lager als Gebäude | `data/buildings.json` → `id: lager`, Kategorie Sonstiges, **kein** `max_je_siedlung` gesetzt; die Prüfung dafür existiert bereits und wird von vier Gebäuden genutzt (`kriegerakademie`, `diebesgilde`, `stellmacher`, `bibliothek` = 1) | `data/buildings.json`, `src/main.py` `_bau_pruefen` (Zeile ~346), `src/spielschicht.py` (~304) |
| Prüfstand | 114 Prüfdateien, Sammellauf 12:17: 112 grün, 0 rot, 2 ausgesetzt, 4.132 Prüfungen, 776 s; Register 88; EXE 46.152.457 Byte, SHA256 `e12428b9…`, Start belegt | `docs/audits/sammellauf_20261101_1205.log` |

**Was heute NICHT existiert:** Gelände je Weltkartenfeld, Dorfpositionen im Kästchen, Gegner-Rahmen,
Hover-Kosten, Transferlogik (S-6), eine Zusammenführung von Dorfzentrum und Lager.

---

## 2. Teil 1 — S-5: das Weltbild im Portal

**Daniel (verbindlich):** 20 × 20 Geländekästchen, Felder anwählbar, eigene Dörfer farbig, **Gegner als
Rahmen mit Nummer**, Hover zeigt **nach ein paar Sekunden** die Transferkosten. Bots sind sechs, je ein
Dorf, feste Position, kein Angriff in dieser Stufe (`docs/KONZEPT_WELTKARTEN_UND_BOTS_20261101.md`,
Frage 8, 9, 10, 29, 30).

### 2.1 Gelände je Feld — die Quelle fehlt, und das ist deine Hauptaufgabe

Das Handbuch nennt **kein** Gelände je Weltkartenfeld; belegt sind nur 20 × 20 = 400 Felder je Welt
(portal.php 2005). Heute zeigt das Kästchen deshalb nur die Bannerfarben. Du sollst **nicht** eine Zahl
erfinden, sondern eine **belegbare Ableitung** liefern:

1. Prüfe im Projekt, ob es eine Geländequelle für ein 20 × 20-Raster gibt (Siedlungskarten sind 10 × 10
   aus `assets/karten/original/`; die alte, stillgelegte Weltkarte hatte sechs Geländearten
   `WELT_GELAENDEREIHENFOLGE` — sie ist **nicht** mehr erreichbar, ihr Code steht als Beleg).
2. Wenn es keine Quelle gibt: liefere **eine** VORSCHLAG-Tabelle (Anteile je Geländeart, Verteilung,
   Seed-Regel, dass eine Weltkarte immer gleich aussieht) und **eine** Zeile, wie Daniel sie später in
   `data/` ändern kann, ohne Code anzufassen.
3. Sage ausdrücklich, welcher Teil deiner Tabelle VORSCHLAG ist und womit er im Spieltest geprüft wird.

### 2.2 Anzeige und Bedienung

Beantworte als Regeln (je ein prüfbarer Satz) mit wörtlichen Spielertexten:

* Wie erkennt der Spieler, welches Feld sein eigenes Dorf trägt, welches ein fremdes und welches frei ist?
* Wie sieht der Gegner-Rahmen mit Nummer aus (Farbe, Linienstärke, Nummerierung 1..6, Bezug zur
  Bot-Liste im Portal)?
* Nach welcher Zeit erscheint der Hover-Hinweis, und was steht darin (Kosten in Mana, Entfernung,
  Zielwelt)? Was passiert bei fehlenden Kosten (kein Dorf ausgewählt, zu wenig Mana)?
* Was passiert bei einem Klick auf ein belegtes Feld, auf ein fremdes Dorf, auf ein freies Feld?
* Wie wird die Auswahl wieder aufgehoben?

### 2.3 Grenzen

* Kein Angriff, kein Kampf, keine Truppenbewegung in diesem Schritt — nur Anzeige und Auswahl.
* Die Anzeige darf keine Zahl zeigen, die der Kern nicht selbst rechnet (eine Rechenstelle).

---

## 3. Teil 2 — S-2c: das Dorfzentrum ist das Lager

**Daniel (verbindlich):** das Dorfzentrum ist Menüpunkt **und** Gebäude, dort stehen Lagerverwaltung und
Übersichten (Werkstätten, Bestände); **ein Lager je Dorf**; Teststände müssen nicht wandern.

### 3.1 Die Entscheidung, die Daniel treffen muss — und deine Empfehlung

Das Dorfzentrum soll ein Gebäude sein. Wenn es bei jeder Gründung mitgesetzt wird, hat jede Siedlung
**vier** Startgebäude statt drei (Tempel, Holzfäller, Steinmetz, Dorfzentrum) — dann müssen der Schnitt
S-1 und seine 35 Prüfungen mitziehen. Wird es nicht mitgesetzt, muss der Spieler es bauen, und ein frisch
gegründetes Dorf hat kein Lager.

Liefere beide Wege als **durchgerechnete Variante** (A: Startgebäude, B: baubar) mit: Auswirkung auf die
Startressourcen, auf die Prüfungen aus S-1, auf die Anzeige eines Dorfes ohne Lager, und auf die Regel
„ein Lager je Dorf“. **Eine Empfehlung, klar begründet.**

### 3.2 Regeln, die du festlegen sollst

* Was zeigt der Menüpunkt „Dorfzentrum“ (Lagerverwaltung, Werkstätten, Bestände des aktiven Ortes)?
* Was passiert mit dem heutigen Menüpunkt „Lager“ — zusammengeführt, stillgelegt mit Vermerk, oder bleibt
  er als Verweis stehen? (Daniel will keine zwei Wahrheiten.)
* Wie wird „ein Lager je Dorf“ durchgesetzt: reicht `max_je_siedlung: 1` in `data/buildings.json` (die
  Prüfung existiert schon), oder braucht es eine zweite Sperre?
* Was sieht ein Dorf ohne Lager (Variante B)?
* Wörtliche Texte für: Bauversuch eines zweiten Lagers, Dorf ohne Lager, Wechsel in ein Dorf mit Lager.

### 3.3 Grenzen

Keine Migration alter Spielstände. Keine neue Datenstruktur für Lager — es bleibt bei `Settlement.vorraete`
und den vorhandenen Feldern.

---

## 4. Teil 3 — Demo-Checkliste: was vor einer offiziellen Demo-EXE belegt sein muss

**Daniel:** „sobald die die aktuell groben offenen punkte im spiel bearbeitet sind möchte ich eine
offiziele spielbare demo exe meines spiels auf github hochladen“.

Liefere eine ** Checkliste in Reihenfolge** (was zuerst, was zuletzt), je Punkt: was ist zu prüfen, wie
wird es belegt (Befehl oder Datei), wer entscheidet. Mindestens:

1. Welche Schnitte müssen fertig sein (heute geplant: S-2c, S-3, S-4, S-5, S-6, S-7, S-8).
2. Frischer Spielstart: was muss in den ersten 10 Minuten funktionieren, damit die Demo „spielbar“ heißt?
3. Speichern und Laden: welche Fälle müssen belegt sein (mitten im Bau, mit laufendem Auftrag, mit zwei
   Dörfern)?
4. Was gehört in die Release-Notizen (was ist bewusst noch nicht drin: kein Bot-Angriff, keine Spionage,
   keine Kartenziehung)?
5. Reihenfolge für GitHub: Arbeitsstand committen, `main` aktualisieren (steht auf `954097aa`), Version
   setzen, Release-Notizen, EXE anhängen — mit den Befehlen, die das Projekt schon hat
   (`tools/build_exe.py`, Release-Dokumente unter `docs/RELEASE_*.md`).
6. Was darf **nicht** in die Demo: Teststände, Admin-Modus, Prüfprotokolle, `archiv/`.

---

## 5. Formregeln für dein Papier

* Deutsch. Tabellen. Keine Emoji. Abschnitte in dieser Reihenfolge: 1 Weltbild, 2 Dorfzentrum, 3 Demo.
* Jede Regel mit Kennung (`W-01`, `D-01`, `R-01`) und Urteil BELEGT / VORSCHLAG / UNBEKANNT.
* **Höchstens acht offene Entscheidungen** am Ende, jede mit zwei Möglichkeiten und deiner Empfehlung
  zuerst. Keine Frage, die du selbst beantworten kannst.
* Sage am Ende ausdrücklich, was du **nicht** wissen kannst (Repo-Stand, lokale Messwerte, Daniels
  Geschmack).

## 6. Was Hermes mit dem Papier tut

Hermes prüft jede Zahl gegen den echten Code, übernimmt die Regeln als Schnitt S-5, S-2c und
Release-Vorbereitung, und legt die acht Entscheidungen Daniel **gesammelt** vor. Was nicht belegbar ist,
wird nicht gebaut, sondern als offener Punkt geführt.
