# Lehren aus der Sitzung vom 04.10.2026

Ehrliche Nachlese. Nicht „was gut klingt“, sondern was tatsächlich passiert ist und was daraus
dauerhaft gilt. Geschrieben vom Hauptagenten, der die Fehler selbst gemacht hat.

---

## Was schiefging — und was daraus folgt

| # | Was passierte | Was daraus gilt |
|---|---|---|
| 1 | **Kosten um Faktor 2 unterschätzt.** Ich nahm den Tageswert der Ausgaben-API als aktuell; er wird in Schüben aktualisiert. Gemeldet: 1,21 USD Mission, tatsächlich 2,79. | Nach **jedem** teuren Aufruf messen und die Zeilen `cache writes` + `cached input` + `output` getrennt summieren. Nie den Tageswert, immer die Differenz. |
| 2 | **Ein Schreibvorgang meldete Erfolg und kam nie an** (`run_tests.bat`, test_berater fehlte danach). Aufgefallen nur durch `grep`. | Nach jedem Schreiben **zurücklesen** und die Wirkung prüfen — nicht der Erfolgsmeldung glauben. |
| 3 | **Unsinnigen Code in ein Modul gepatcht** (eine verkettete Zuweisung mitten in einer Funktion), sofort gesehen und behoben. | Wenn eine Ersetzung künstlich aussieht: nicht abschicken. Ein Patch ist eine Textersetzung, keine Denkaufgabe. |
| 4 | **Funktion doppelt eingefügt** statt entfernt — der Aufräum-Patch hatte sie erneut angehängt. | Nach Umbauten `grep -c "def <name>"` laufen lassen; doppelte Definitionen gewinnt der letzte, still. |
| 5 | **Eine Prüfung war grün, ohne das Geprüfte zu prüfen:** „Steinmetz auf Wald abgelehnt“ schlug wegen der Feldbelegung an, nicht wegen des Geländes. | Bei jeder Prüfung die **Begründung** mitprüfen (Meldungstext), nicht nur den Wahrheitswert. Frei geräumte Testdaten benutzen. |
| 6 | **Zahlen in eine Commit-Nachricht geschrieben, während der Prüflauf noch lief** („260 Prüfungen, 0 Fehler“). Selbst bemerkt, korrigiert. | Erst der Lauf, dann die Zahl. Im Zweifel in die Nachricht „Lauf läuft noch“ schreiben. |
| 7 | **Zu seriell gearbeitet**, dann zu parallel: sechs Agenten gleichzeitig, der Rechner war ausgelastet und ein Fenstertest brauchte 40 statt 10 Sekunden. | 2–4 Kinder. Nebenläufigkeit ist ein Werkzeug, kein Wert an sich. |
| 8 | **Den Überblick über laufende Arbeiten verloren** — Daniel musste zweimal bremsen („du hast noch laufende Prozesse“). | Vor jedem neuen Auftrag die laufenden auflisten. Ein sichtbarer Status statt Nebenbei-Start. |
| 9 | **Zwei teure Ergebnisse lagen nur im Zwischenspeicher** (astra's Kartenanalyse, die Siedlungsvorlage) — der wird nach 24 Stunden geleert. Durch Daniels Hinweis gerettet. | Jede Modellantwort **sofort** ins Projekt kopieren (`docs/audits/`) und einchecken, samt Eingabe. |
| 10 | **Drei Anläufe an einer Schreibsperre verbrannt**, obwohl die Datei vollständig gelesen war. | Wenn die Sperre trotz vollständigem Lesen bleibt: alte Fassung archivieren, neue daneben schreiben, verschieben. Nicht weiter versuchen. |
| 11 | **Weltbezug verwechselt:** die sechs alten Weltnamen als Felder in ein Raster gesetzt statt als Dimensionen. Auch das starke Modell hatte diesen Denkfehler. | Die **Art** eines Fakts prüfen (ist das ein Feld, eine Dimension, ein Spieler?), nicht nur seine Zahl. Bei Unklarheit die Quelle lesen, nicht das Modell fragen. |
| 12 | **„Erfundene“ Baupreise waren in Wahrheit original.** Monatelang stand die Wahrheit im eigenen Code, während sie als Schätzung gekennzeichnet war. | Bevor etwas als falsch oder erfunden gilt: das eigene Artefakt gegen die neue Quelle halten. Zwei unabhängige Quellen, die übereinstimmen, sind ein Beweis. |
| 13 | **Pfadfallen zweimal getroffen** (`/c/...` für natives Python; falsche URL-Muster bei cgamed.de). Dazu eine Groß-/Kleinschreibung, die einen Debug-Zyklus kostete. | Natives Programm → `C:/...`. Erwartete URL-Muster **nicht raten**: die Seite selbst nach den Pfaden fragen. Bei Namensvergleichen Groß/Klein normalisieren. |

## Was gut lief — und beibehalten gehört

1. **Kindmeldungen mit einem anderen Verfahren nachprüfen.** Das deckte den widerlegten
   Preisvorschlag, den falschen Weltbezug und den grünen-ohne-Prüfung-Fall auf. Kinder berichten
   ehrlich, aber sie irren sich — und ihr eigener Test kann derselbe Irrtum sein.
2. **Die Quelle lesen, nicht das Modell fragen.** Alle belegten Zahlen (Terrain-Erträge,
   20×20-Felder, 5.000 Mana, Götterschutz ±20 %) kamen aus Handbuch und alten Seiten, nicht aus
   einer Modellantwort.
3. **Teure Modellläufe mit Belegen einsammeln.** Rohantwort **und** Eingabe sichern macht später
   nachvollziehbar, *worauf* geantwortet wurde.
4. **Vorschläge kennzeichnen.** Jede erfundene Zahl steht als `VORSCHLAG` mit Ableitung — dadurch
   konnte astra's Preisvorschlag überhaupt widerlegt werden.
5. **Entscheidungen, die Daniel gehören, nicht selbst treffen.** Zeitfaktor, Forschungstempo,
   Bot-Regeln, Beutemenge: vorgelegt statt verordnet.
6. **Günstiges starkes Modell zuerst.** `deepseek-v4-pro` leistete den Auftragsentwurf für 0,12 USD,
   wo `gpt-6-astra` 1,27 USD brauchte — bei gleicher Qualität (9/9 Seitenangaben stimmten).
7. **Nachprüfen der eigenen Arbeit vor der Meldung.** Alle Zahlen dieser Sitzung (488 Prüfungen,
   Kosten, Bildmaße) wurden vor dem Bericht verifiziert.

## Der teuerste Irrtum dieser Sitzung

Nicht ein Absturz und kein verlorenes Guthaben, sondern **eine nicht geprüfte Annahme**: dass unsere
Baupreistabelle erfunden sei. Sie war original. Aufgefallen ist es nur, weil ein Screenshot sie
bestätigte und das starke Modell ein Gegenmodell lieferte.

**Regel daraus:** Eine Kennzeichnung im eigenen Code („Vorschlag“, „erfunden“) ist eine Behauptung,
kein Beweis — sie gehört genauso geprüft wie fremde Zahlen.

## Reflexion der Sitzung 05.10.2026 (Nachmittag, Schritte 24–28)

**Auftrag:** Daniels Erweiterung (feinere Karten, Ausrüstung/Forschung/Hausausbau), dann zwei
Vorgaben aus dem Chat („intelligent auf ALLE Gebäude“, „ein Gebäude hat im Sumpf nichts verloren“)
und zuletzt ein **Spielbericht zur laufenden `.exe`** — der Vorrang hatte.

**Was gut lief**

1. **Erst messen, dann bauen.** Der Auftrag lautete, die Sumpfregel auf alle Gebäude anzuwenden. Die
   Messung (Einmal-Skript zur Prüfung der Sumpfregel, 20 Gebäude × 7 Gelände; nicht im Projekt abgelegt) zeigte: die Sumpfregel galt längst für alle —
   ohne Regel waren **9 andere** Gebäude (Haus im Nebelsee war möglich). Hätte ich drauflos gebaut,
   hätte ich Daniel ohne Beleg widersprochen.
2. **Der Spielbericht wurde zur Ursachensuche, nicht zur Vermutung.** Zwei belegte Ursachen: die
   Spieluhr rechnete Echtzeit 1:1 (`dt_h = dt_seconds / 3600`) → 4 Holz je **echter** Stunde; und die
   Rundung auf zwei Stellen machte daraus nach einer Sekunde „0,00“. Beides mit Testzahlen belegt.
3. **Jeder Schritt ist einzeln zurücknehmbar:** Einzeltest → Sammellauf → Protokollzeile → Commit,
   fünf kleine Commits statt einem großen.
4. **Prüfer erst nach dem Commit**, Kinder lesen nur und committen nicht — der Prüfer fand dennoch
   einen echten Punkt: Alt-Spielstände bleiben ladbar (dynamisch belegt).

**Meine vier Fehler dieser Sitzung (ehrlich, mit Folge)**

1. **Eine Zeit geschätzt.** In der Übergabe stand „.exe 12:52“ — echt war **12:38:43**
   (Dateistempel). Das verletzt die eigene Projektregel „Zeiten nie schätzen“. Es fiel nur auf, weil
   ich die Dateizeit nachgeprüft habe; korrigiert mit sichtbarem Vermerk in 0c.
2. **Folgen einer Datenänderung unterschätzt.** Die Geländeregeln stehen in `data/buildings.json`;
   ich hatte vier Prüfdateien im Blick — der **Sammellauf fand zwei weitere** (`test_baseline`,
   `test_spielschicht`, 16 Fehler). Ohne ihn wäre ein roter Stand gemeldet worden.
3. **Sammellauf parallel zum laufenden Spiel.** `test_baseline` schlug zweimal als erste Datei mit
   **leerer Ausgabe** fehl, während Daniels Spiel offen war; allein 40/0/0. Die Regel stand längst im
   Projekt — ich habe sie nicht befolgt, weil gerade zugeschaut wurde.
4. **EXE-Neubau nicht von Anfang an mitgedacht.** Nach der ersten Regeländerung in `data/` wäre die
   `.exe` veraltet geblieben. Jetzt Lehre (f) in 0c: **Datendatei geändert → `.exe` neu bauen.**

**Protokollführung — Selbstbewertung**

* Gut: jede Zeile nennt Uhrzeit (mit `date`), Belegzahlen, Dateien und Prüfzahl; die Commits tragen
  dieselben Zahlen, sodass Protokoll und Historie zusammenpassen.
* Schwach: die Zeile zu Schritt 28 ist ~4.500 Zeichen lang und damit unlesbar. **Künftig: maximal
  ~1.200 Zeichen je Zeile, Details in ein eigenes Dokument unter `docs/`.**
* Schwach: Lehren standen über 0c, BOARD und Commit-Nachrichten verstreut. **Sie gehören hierher
  (`docs/LEHREN.md`), die Übergabe verweist nur darauf.**

**Zahlen der Sitzung:** 5 Schritte (24–28) + eine Korrektur · 41 Prüfdateien, **2599 grün, 0 Fehler,
21 Befunde** · drei `.exe`-Bauten (12:38, 13:29, 13:41) · sechs Kinder (vier Module, ein Nachrechner,
ein Prüfer) · Kosten nur `deepseek-v4-flash` (Kinder/Prüfer) plus zwei astra-Bildaufrufe und ein
v4-pro-Entwurf aus dem Vormittagsauftrag.

---

## Nachtrag 31.10.2026 — Zitate werden berichtigt, aber nie stillschweigend

Ein Rechtschreib-Durchgang über 48 Markdown-Dateien fand fünf „Tippfehler" — vier davon in
**zitierten Originaltexten** der alten Website („Hier seit ihr sicher", „mit einender verbinden"),
dazu 38 eingeklebte Stellen ohne Leerzeichen („Kampfablauf:Aktuell", „1123 Gebäude"). Meine erste
Antwort war: Zitate bleiben unangetastet. **Daniel hat das am 31.10.2026 anders entschieden** — und
er hat recht: ein Zitat mit Lesefehler hilft niemandem. Die Bedingung ist die Nachvollziehbarkeit.

**Regel (gültig):** Schreibfehler in Zitaten werden berichtigt — **jede einzelne Änderung wird
vorher/nachher festgehalten**, mit Stelle und Art. Kein Wortlaut, keine Zahl, keine Bedeutung wird
geändert; wo der Sinn betroffen sein könnte, wird nicht korrigiert, sondern angemerkt.
Nachweis: `docs/ZITATKORREKTUREN.md`, Werkzeug: `tools/zitatkorrekturen.py`.
Für die Zeichen-Vereinheitlichung (372 Stellen in 22 Dateien): `tools/anfuehrungszeichen.py`.

**Lehre für mich:** „Quellen schützt man, indem man sie unverändert lässt" war zu einfach gedacht.
Schutz heißt: nachweisbar ändern, nicht gar nicht ändern.
