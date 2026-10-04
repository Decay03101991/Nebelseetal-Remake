# Lehren aus der Sitzung vom 04.10.2026

Ehrliche Nachlese. Nicht „was gut klingt", sondern was tatsächlich passiert ist und was daraus
dauerhaft gilt. Geschrieben vom Hauptagenten, der die Fehler selbst gemacht hat.

---

## Was schiefging — und was daraus folgt

| # | Was passierte | Was daraus gilt |
|---|---|---|
| 1 | **Kosten um Faktor 2 unterschätzt.** Ich nahm den Tageswert der Ausgaben-API als aktuell; er wird in Schüben aktualisiert. Gemeldet: 1,21 USD Mission, tatsächlich 2,79. | Nach **jedem** teuren Aufruf messen und die Zeilen `cache writes` + `cached input` + `output` getrennt summieren. Nie den Tageswert, immer die Differenz. |
| 2 | **Ein Schreibvorgang meldete Erfolg und kam nie an** (`run_tests.bat`, test_berater fehlte danach). Aufgefallen nur durch `grep`. | Nach jedem Schreiben **zurücklesen** und die Wirkung prüfen — nicht der Erfolgsmeldung glauben. |
| 3 | **Unsinnigen Code in ein Modul gepatcht** (eine verkettete Zuweisung mitten in einer Funktion), sofort gesehen und behoben. | Wenn eine Ersetzung künstlich aussieht: nicht abschicken. Ein Patch ist eine Textersetzung, keine Denkaufgabe. |
| 4 | **Funktion doppelt eingefügt** statt entfernt — der Aufräum-Patch hatte sie erneut angehängt. | Nach Umbauten `grep -c "def <name>"` laufen lassen; doppelte Definitionen gewinnt der letzte, still. |
| 5 | **Eine Prüfung war grün, ohne das Geprüfte zu prüfen:** „Steinmetz auf Wald abgelehnt" schlug wegen der Feldbelegung an, nicht wegen des Geländes. | Bei jeder Prüfung die **Begründung** mitprüfen (Meldungstext), nicht nur den Wahrheitswert. Frei geräumte Testdaten benutzen. |
| 6 | **Zahlen in eine Commit-Nachricht geschrieben, während der Prüflauf noch lief** („260 Prüfungen, 0 Fehler"). Selbst bemerkt, korrigiert. | Erst der Lauf, dann die Zahl. Im Zweifel in die Nachricht „Lauf läuft noch" schreiben. |
| 7 | **Zu seriell gearbeitet**, dann zu parallel: sechs Agenten gleichzeitig, der Rechner war ausgelastet und ein Fenstertest brauchte 40 statt 10 Sekunden. | 2–4 Kinder. Nebenläufigkeit ist ein Werkzeug, kein Wert an sich. |
| 8 | **Den Überblick über laufende Arbeiten verloren** — Daniel musste zweimal bremsen („du hast noch laufende Prozesse"). | Vor jedem neuen Auftrag die laufenden auflisten. Ein sichtbarer Status statt Nebenbei-Start. |
| 9 | **Zwei teure Ergebnisse lagen nur im Zwischenspeicher** (astra's Kartenanalyse, die Siedlungsvorlage) — der wird nach 24 Stunden geleert. Durch Daniels Hinweis gerettet. | Jede Modellantwort **sofort** ins Projekt kopieren (`docs/audits/`) und einchecken, samt Eingabe. |
| 10 | **Drei Anläufe an einer Schreibsperre verbrannt**, obwohl die Datei vollständig gelesen war. | Wenn die Sperre trotz vollständigem Lesen bleibt: alte Fassung archivieren, neue daneben schreiben, verschieben. Nicht weiter versuchen. |
| 11 | **Weltbezug verwechselt:** die sechs alten Weltnamen als Felder in ein Raster gesetzt statt als Dimensionen. Auch das starke Modell hatte diesen Denkfehler. | Die **Art** eines Fakts prüfen (ist das ein Feld, eine Dimension, ein Spieler?), nicht nur seine Zahl. Bei Unklarheit die Quelle lesen, nicht das Modell fragen. |
| 12 | **„Erfundene" Baupreise waren in Wahrheit original.** Monatelang stand die Wahrheit im eigenen Code, während sie als Schätzung gekennzeichnet war. | Bevor etwas als falsch oder erfunden gilt: das eigene Artefakt gegen die neue Quelle halten. Zwei unabhängige Quellen, die übereinstimmen, sind ein Beweis. |
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

**Regel daraus:** Eine Kennzeichnung im eigenen Code („Vorschlag", „erfunden") ist eine Behauptung,
kein Beweis — sie gehört genauso geprüft wie fremde Zahlen.
