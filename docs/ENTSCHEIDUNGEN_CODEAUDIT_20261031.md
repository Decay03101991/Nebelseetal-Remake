# Entscheidungen Daniels zur Code-Audit-Runde — 31.10.2026

Abgefragt als Auswahlformular, Antworten wörtlich übernommen. Diese Liste ist bindend für die
Umsetzung; sie ersetzt keine früheren Entscheidungen (E1–E5 bleiben gültig), sondern ergänzt sie.
Nennt eine dieser Entscheidungen einer Quelle aus dem Handbuch widersprechen, gilt die Quelle —
dann wird nachgefragt, nicht umgesetzt.

| # | Frage | Daniels Antwort | Folge für die Arbeit |
|---|---|---|---|
| 1 | Ordnerstruktur `src/` | **Klassische Pakete mit `__init__.py`** | `src/kern/`, `src/kampfsystem/`, `src/bot/`, `src/persistenz/`, `src/ui/`, `src/admin/`, `src/alt/` — je mit `__init__.py`; Wurzel-Shims bleiben, bis alle Importe umgestellt sind; `tools/build_exe.py` bekommt `collect_submodules` |
| 2 | `main.py` aufteilen | **Stufenweise: erst der gemeinsame Render-Helfer** | Schritt 1: `seite_aufbauen(titel, untertitel, content)` ersetzt das Gerüst der 27 `_render_*`; Spielkern und Ansichten erst danach, jeder Schritt ein Commit |
| 3 | Spielmechaniken | **Alle vier** | (a) Kampf beim Marsch über `kampf.fuehre_schlacht`, (b) Aufträge auf der Karte sichtbar, (c) Zeitlimit- **und** Tempo-Option im Startmenü, (d) Dimensionen: 20 Kulisse, 6 aktiv, (e) Spionage als fünfte Auftragsart |
| 4 | Aufräumen | **Alle vier** | (a) `_render_news` und `_upgrade_building` nach `grep`-Nachweis löschen, (b) `oberflaeche_original.py` **mit** seiner Prüfdatei und `gildenrangliste_original.py` ins Archiv, (c) Skills ergänzen und Cleanup-Cronjob gegenprüfen, (d) Git-Historie **nur prüfen**, nicht ändern |
| 5 | Restbudget 2,88 USD | **Nein — nur für die Umsetzung, keine Gegenprüfung** | Keine Diff-Pakete an das große Modell. Die Umsetzung mache ich selbst; Modellaufrufe nur, wenn eine Frage ohne sie nicht zu beantworten ist (dann vorher melden) |

## Was daraus in welcher Reihenfolge folgt

1. Voller Prüflauf und EXE-Neubau (Basis herstellen).
2. P3.1–P3.3: gemeinsame Helfer (`als_zahl`, `als_int`, `aufzaehlung`), Karrenladung, Reisezeit-Kette.
3. P4: Zeichenmodule teilen (`_punkte`, `_box`, `_fuell` stehen doppelt).
4. Aufräumen nach Entscheidung 4 (a) und (b) — klein, sofort prüfbar.
5. P5: Paketgerüst nach Entscheidung 1, Umzug in Wellen mit Shims.
6. P1 nach Entscheidung 2: zuerst der Render-Helfer, dann Spielkern, dann Ansichten.
7. Die fünf Mechaniken aus Entscheidung 3 — jede mit eigener Prüfdatei und Registereintrag.
8. Skills und Cleanup-Cronjob nachziehen (Entscheidung 4c), Git-Prüfbericht schreiben (4d).

## Was ausdrücklich NICHT gemacht wird

* Keine Gegenprüfungs-Pakete an große Modelle in dieser Runde (Entscheidung 5).
* Kein Neuschreiben der Git-Historie (Entscheidung 4d: nur prüfen).
* Keine Änderung an belegten Originalzahlen — Spielgefühl-Änderungen nur über die Optionen aus
  Entscheidung 3, nicht über die Grundwerte.

## Nachtrag: fünf Detailfragen (zweite Runde, 31.10.2026)

| # | Frage | Daniels Antwort | Folge |
|---|---|---|---|
| 6 | Zeitlimit-Dauer | **„ich verstehe nicht genau, was gemeint ist — du kennst alle Vorgaben; möglichst nach Original, sonst Indizien, sonst eine kluge Lösung, und das dokumentieren“** | Die Entscheidung liegt bei mir. Vorgehen verbindlich: (1) Handbuch 2009 und 2006 auf jede Spur zu Spielende/Zeitlimit prüfen, (2) Indizien auswerten (Ruhmeshalle, Punkteverfall, Auftragsdauern, Forenzitate), (3) findet sich nichts, eine einfache, abschaltbare Lösung bauen und **die Quellenlage im Register dokumentieren** — mit dem Vermerk „VORSCHLAG EIGENTÜMER ÜBERTRAGEN“ |
| 7 | Spionage: mit Abwehr? | **Nur Spionage** — Bericht über Truppen, Vorräte, Wall. Einfach halten | `SI`/`HE` bleiben ungenutzt (Handbuch: „noch ohne Einfluss“); Spionage ist eine Auftragsart mit Rückkehrbericht, keine Kampfmechanik |
| 8 | Dimensionen: welche 6? | **„Leite die 6 aus dem Handbuch ab, lege mir keine Liste vor, bau es sinnvoll“** | Ich leite sie ab, dokumentiere die Ableitung im Register und baue; keine Rückfrage, aber nachvollziehbare Begründung je Dimension |
| 9 | Shims beim Paket-Umbau | **Am Ende entfernen** | Während des Umzugs bleiben sie, damit nichts bricht; im letzten Schritt der Umstellung fliegen sie raus und jeder Import zeigt genau einen Weg |
| 10 | Prüfdateien umziehen? | **Ja, mit umziehen** (`tests/kern/`, `tests/ui/` …) | `tools/sammellauf.py` muss rekursiv suchen; Umzug nach den Modulen, nicht davor |

**Regel aus Antwort 6 und 8:** Wo Daniel die Entscheidung an mich überträgt, gilt: erst Quelle, dann
Indiz, dann eigene Lösung — und jede eigene Festlegung wird im Prüfregister als VORSCHLAG geführt,
nie als Beleg.
