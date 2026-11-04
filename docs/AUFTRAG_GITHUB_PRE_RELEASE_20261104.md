# Auftrag GitHub-Neuaufbau: erster Pre-Release (Daniel, 04.11.2026)

**Stand 04.11.2026, 16:20 - die Liste ist NOCH NICHT VOLLSTAENDIG.** Daniel ergaenzt, was das
Repository enthalten soll. Bis die Liste vollstaendig ist, wird am Repository **nichts** geaendert:
kein Push, kein Loeschen, kein Release, kein Pages-Umbau. Dieses Dokument ist die Akte des Auftrags;
der Fortschritt steht als eigene Zeile in Register und Protokoll.

## 1. Daniel nimmt den letzten Upload zurueck

Daniel hat am 04.11.2026 angewiesen, den letzten GitHub-Upload **zurueckzunehmen** und den
Projektstand **komplett neu zu beurteilen**. Begruendung in seinen Worten: das Spiel ist noch nicht
weit genug entwickelt, und beim alten Upload war das nicht bedacht. Damit aendert sich auch die
Beurteilung dieses Projektstands: was bisher als Veroeffentlichungsstand galt, gilt NICHT mehr als
Freigabe.

**Folgen, die ueberall mitgefuehrt werden:**

- Vom alten Upload darf auf GitHub **nichts nachweisbar bleiben** - keine alten Dateien, keine alten
  Commits, keine alten Releases, keine Reste in der History.
- Der neue Stand wird als **ERSTER Pre-Release** veroeffentlicht (Umdatierung des Stands).
- Die Anweisung ist in Protokoll und Register eingetragen, nicht nur im Chat.

## 2. Was das neue Repository enthalten soll (Stand der Liste)

| Punkt | Inhalt (Daniels Worte, zusammengefasst) |
|---|---|
| Umfang | Ein relativ aktueller Stand, wenn das Wichtigste abgeschlossen ist - **nicht alle Ordner** wie bisher, sondern die notwendigen Spielordner. |
| Schwerpunkt | Diesmal **weniger kompakt**: vor allem der wichtigste Code soll hochgeladen werden - jede Codezeile ist am Zeilenende beschrieben, genau dafuer. |
| Besucherdokument | Ein Dokument, das die Spielentwicklung fuer Besucher **grob** erklaert: die Entwicklungsschritte, aber **nicht** die Detail-Entwicklungsdateien. |
| Offizielle Erklaerung | Was das Spiel genau ist, als offizielle Version/Erklaerung. |
| Geschichte | Die komplette Geschichte des Nebelseetals als **schoen gestaltete PDF**. |
| Einfuehrung | Der aktuelle Entwicklungsstand als erste Repo-Einfuehrung. |
| Vorstellung | Fraktionen, Wappen und Welten vorstellen - mit den Bildern aus den Arbeitsordnern. |
| Sicherheit | Keine API-Schluessel, keine Tokens, keine Zugangsdaten im Repository. |
| Herkunft | Nachvollziehbar als **Daniels Arbeit mit einem Hermes-Agent-System und seinen Coding-Subagenten**. |
| Transparenz | Ueberwiegend `deepseek-v4-flash`; einzelne, kontrollierte Auftraege an das grosse DeepSeek-Modell; dazu Auftraege von GPT-6-Astra und Teile aus dem GPT-Chat-Abo - **nur grob**, ohne die Details aus den Protokollen. |

## 3. macOS-Fassung (`.app`) - ehrliche Lage

Daniel wuenscht eine `.app` fuer macOS im **gleichen Stand wie die EXE**, doppelklickbar im Ordner
Programme.

| Frage | Antwort |
|---|---|
| Ist das moeglich? | Ja, aber **nicht von diesem Rechner aus**. Eine echte `.app` entsteht mit PyInstaller **auf macOS** (Apple-Silicon oder Intel), mit einem Mac-Python und dem Tk-Framework von python.org. Auf Windows laesst sich das nicht bauen und - wichtiger - nicht pruefen. |
| In ein paar Stunden machbar? | Nur mit einem **Mac zur Hand**: dort PyInstaller-Lauf (10 bis 20 Minuten), signieren ist optional (ohne Signatur warnt Gatekeeper), Test durch Doppelklick. Ohne Mac: nein. Eine Fassung, die auf dem Zielrechner Python und Tkinter verlangt, ist keine gleichwertige `.app`. |
| Was jetzt gilt | Der Auftrag steht, gebaut ist nichts. Vor dem Bau braucht es die Entscheidung, **wo** gebaut und geprueft wird (fremder Mac, gemieteter Mac, oder die `.app` bleibt offen). |

## 4. Entscheidungen Daniels (04.11.2026, abgefragt 15:50 - beantwortet)

| Nr. | Frage | Entscheidung Daniels |
|---|---|---|
| 1 | Repository | **Bestehendes Repo loeschen und unter GLEICHEM Namen neu anlegen.** Die URL bleibt damit, die alte History ist wirklich verschwunden (ein Force-Push haette die alten Commits ueber ihre SHA abrufbar gelassen). |
| 2 | Sichtbarkeit | **Privat** bis zum Pre-Release, danach oeffentlich schalten. Kein Zwischenstand ist waehrend des Aufbaus sichtbar. |
| 3 | Ordnerliste | **Ins Repo:** `src/`, `data/`, `assets/`, `release_vorlage/`, die Startdateien, `README`/`LICENSE`, das Besucherdokument, die offizielle Erklaerung, der Entwicklungsstand als Repo-Einfuehrung und die Geschichte als PDF. **Draussen:** `tests/`, `tools/`, `docs/` (ausser den Veroeffentlichungs-Dokumenten), `archiv/`, `release_public/`, Spielstaende, EXE. |
| 4 | Besucherzugang | **Bleibt** (GitHub Pages) und wird inhaltlich **neu geschrieben** (Besucherdokument). |
| 5 | macOS-`.app` | **Bleibt offen** und wird im Pre-Release **ehrlich als fehlend** genannt (Bau und Pruefung nur auf einem Mac moeglich). |
| 6 | Pre-Release-Datum | Noch offen - Vorschlag: das Datum des Uploads, nicht ein rueckdatiertes. |

**Weiterhin offen: Daniels Inhaltsliste.** Er ergaenzt, was das Repo ausserdem enthalten soll; bis dahin
wird am Repository nichts geaendert (kein Push, kein Loeschen, kein Release, kein Pages-Umbau).

## 5. Reihenfolge, die Daniel vorgegeben hat

1. **Erst die laufende Arbeit fertig machen** (Story 2, Sammellauf, Register, Protokoll, Commit).
2. **Dann eine Sitzungsuebergabe** schreiben, in der dieses Vorhaben als eigener, grosser Auftrag steht.
3. **Dann** der GitHub-Neuaufbau - erst wenn Daniels Inhaltsliste vollstaendig ist.

Der Auftrag ist ausdruecklich als SEHR WICHTIGES PROJEKT eingeordnet: er darf nicht zwischen zwei
Spiel-Schnitten nebenher laufen, sondern bekommt eine eigene Sitzung mit eigener Reihenfolge.
