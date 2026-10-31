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

## Nachtrag: Portalkosten (dritte Runde, 31.10.2026, nach der externen Spielpruefung)

| # | Frage | Daniels Antwort | Folge |
|---|---|---|---|
| 11 | **F-03 der externen Pruefung: aus welcher Kasse werden die 5.000 Mana des Portalwechsels bezahlt?** Die Ansicht bucht heute in die Reichsanzeige (`main.py:4771`), die selbst nur eine Summe der Ortslager ist. | **"um sachen wie das portal zu zahlen muss man halt rohstoffe in einem dorf zusammenfuehren um es zu bezahlen und dann zahlt man es von eben dem dorf"** | Das Portal zahlt **aus dem Ortslager der aktiven Siedlung** (`Settlement.vorraete`), nicht aus der Reichsanzeige. Reicht das Lager des aktiven Dorfes nicht, wird der Wechsel **abgelehnt** mit der Angabe, wie viel im Ort fehlt - kein stilles Zusammenziehen aus anderen Doerfern. Damit gilt fuer das Portal dieselbe Regel wie fuer Bauen, Forschung und Ausbildung: **bezahlt wird da, wo gehandelt wird**. Die Reichsanzeige bleibt reine Anzeige (Summe der Orte) und wird von `_reichsanzeige_aus_orten` abgeleitet. |

## Nachtrag 2: externe Spielpruefung (Fragen 12-21, 31.10.2026)

Abgefragt als Auswahlformular, Antworten woertlich uebernommen. Bindend wie alle vorherigen Punkte.

| # | Frage | Daniels Antwort | Folge |
|---|---|---|---|
| 12 | GitHub-Push des neuen Stands | **"erst nach der verarbeitung der gpt chat berichte und nachdem die grossen modelle mit ihrer arbeit fertig sind. Den wirklich neuen stand dann damit das github nicht so ueberladen wird"** | Kein Zwischen-Push. Erst wenn externe Berichte eingearbeitet sind und keine Modell-Laeufe mehr offen: **ein** Push des dann gueltigen Stands auf `stand-20261031-1400`; `main` bleibt unberuehrt. |
| 13 | Portal-Sperre, Zeitbasis | **"24 Spielstunden (Spieluhr)"** | `portalraum` rechnet die 24 h kuenftig in **Spielzeit** (`GameState.spielsekunden`), nicht in Rechnerzeit (`time.time()`). |
| 14 | F-05: Abriss der letzten Werkstatt bei laufender Warteschlange | **"abriss nicht moeglich solange fertigungswarteschlange laeuft. Sinnvoll anderes anpassen bitte"** | Abriss wird **gesperrt**, solange im Ort Auftraege in `werkstaetten[...]` laufen - mit klarer Meldung. Kein Pausieren, kein Geisterfertigen. Ist die Warteschlange leer, bleibt Abriss normal. |
| 15 | F-06: zweite Werkstatt waehrend laufender Auftraege | **"Sofort auf den offenen Rest (10 Schwerter, 1->2 Schmieden = halbe Restzeit)"** | `ort_tick` liest die Kapazitaet **bei jedem Takt** aus den gebauten Feldern; bereits geleistete Arbeit wird nicht rueckwirkend gutgeschrieben. |
| 16 | F-13: Werkstattstufen (Schmiede, Bogenbauer, Naehstube) | **"Werkstaetten meinst du alle gebaeude die items herstellen ...? dann ist die antwort wie immer. wenn moeglich aus den orginaldaten beziehen und beachte den bezug zur forschung da diese quasi die werkstatt ja sowieso schon ausbaut in dem sinne"** | **Ja, gemeint sind alle drei Warengebaeude.** Sie haben **keine eigenen Ausbaustufen**; der Ausbau ist die **Forschung** (Waffentechnik, Ruestungsbau, Naehkunst, Bogenbau, Magiekunde). Der Stufen-Tempocode (`werkstatt.STUFE_TEMPO_PROZENT`, `_stufe_wert`) und jedes UI-Versprechen "hoehere Werkstattstufe = schneller" fliegen raus - als **nicht belegt, bewusst nicht gebaut** im Register vermerkt. Tempo kommt nur aus Anzahl parallel + Forschung. |
| 17 | F-10: Sofortangriff | **"An dieselbe Einsatzregel koppeln (wie der Auftrag)"** | `_angriff_durchfuehren` benutzt denselben Weg wie `auftrag_starten` (Ortslager, Ladung, Beute, Verluste, Rueckkehr). Kein zweiter Beute-/Kostenpfad. |
| 18 | Ausbildungsdauer | **"Behalten: Dauer = Grunddauer / Stufe (Stufe 5 = ein Fuenftel)"** | `AUSBILDUNG_STUFENFAKTOR_AKTIV = True` bleibt; Formel bleibt VORSCHLAG im Register. |
| 19 | Beute-Staffel 10/30/60/100 % | **"Erst Spieltest, dann nachziehen"** | Werte bleiben vorlaeufig; nach dem naechsten Spieltest neu bewerten. Register 45 bleibt VORSCHLAG. |
| 20 | F-12: Warenoberflaeche (Rezeptkarten, Mengen, Bedarfsplaner) | **"Erst nach P1 (kein Umbau waehrend des Refactorings)"** | Kommt nach dem `main.py`-Umbau; bis dahin nur der Blocker-Fix aus F-04 (eine Quelle). |
| 21 | Budget: Diff-Gegenpruefung an ein grosses Modell | **"Ja, eine pro groesserem Umbau, vorher ansagen"** | Eine Gegenpruefung je grossem Umbau (z. B. `deepseek-v4-pro`, ~0,10 USD) ist erlaubt - **vorher ansagen**, Kosten notieren. Kein Sammelpaket. |
