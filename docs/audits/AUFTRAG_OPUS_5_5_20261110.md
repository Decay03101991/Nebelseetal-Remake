# AUFTRAG: ein starker Pruefer (Claude, Klasse Opus) gegen die zwoelf Gesamtaudit-Befunde

**Stand:** 10.11.2026, 10:30. **Zustand: VORBEREITET, NICHT GELAUFEN.** Es wurde kein Modell aufgerufen und
kein Geld ausgegeben.

## 1. Was geprueft werden soll und warum

Das Gesamtaudit vom 31.10.2026 hat zwoelf Befunde hinterlassen (`docs/audits/GESAMTAUDIT_BEFUNDE_20261031.md`).
Sie sind **zehn Tage alt** und niemand hat sie seither am Code nachgeprueft. In der Zwischenzeit sind D-4, D-5,
D-5a, D-5b und der Layout-Schnitt gebaut worden; mindestens drei der zwoelf Punkte sehen im heutigen Code
anders aus als damals behauptet:

| Nr | Behauptung von damals | Was heute im Code steht |
|---|---|---|
| 2 | zwei Kampfsysteme | `src/kampf_alt_handbuch_2009.py` existiert nicht mehr, eine Wache verlangt genau EIN System |
| 4 | Tageszaehlung mit `if` statt `divmod` | `src/main.py:7911` rechnet bereits `divmod` gegen EINE Tageslaenge |
| 5 | Reisekosten-Konstante nicht angeschlossen | `SEKUNDEN_JE_FELD = 7200.0` wird in der Reisezeit-Formel benutzt |
| 10 | Siegbedingung 300 Punkte | Daniel hat entschieden: das Original kennt KEINEN Sieg (`ZIEL_PUNKTE_VERWORFEN = 300`) |

Diese Sichtung steht auch im Paket — **ausdruecklich als Sichtung, nicht als Urteil**. Der Pruefer soll sie
bestaetigen oder widerlegen.

## 2. Was im Paket steht

`docs/audits/OPUS_PRUEFPAKET_20261110.md` — **41.026 Zeichen, 768 Zeilen, rund 11.400 Prompt-Token**
(3,6 Zeichen je Token; die Schnitte stammen aus dem Repo-Blob am gepinnten Commit):

1. Rolle, Verbote und Pflicht-Ausgabeformat (vier Urteile: `BESTAETIGT`, `UEBERHOLT`, `TEILWEISE`, `UNBEKANNT`)
2. Messlage und Herkunftstabelle (Repo, gepinnter Commit, SHA256 je Datei)
3. Die zwoelf Behauptungen im Wortlaut (Tabelle)
4. Die Sichtung von heute, acht Zeilen mit Fundstelle
5. Rechenpflicht zur Spieluhr x180 (Forschung Stufe^2, Reise, Ausbildung, Siedlerzuwachs, Punkte/ Wallstufe 8)
6. **19 Codeschnitte im Wortlaut**, per `ast` geschnitten, jede Stelle mit `Datei:Zeile`:
   `ortsdeckung`, `verbrauche_am_ort`, `reichsdeckung`, `verbrauche_reichsweit`, `tick`, `bauen_auf_karte`,
   `BIBLIOTHEK_OBERGRENZE`, `SIEDLUNGEN_MAXIMUM`, `MENU_ANZEIGE`, `fuehre_schlacht`, die vier Auftrags-Konstanten,
   `STANDARD_FAKTOR`, `ZIEL_PUNKTE_VERWORFEN`, `kriegspunkte`, `goetterschutz_tage`, `dauer_stunden`

Bewusst **nicht** im Paket: die Handbuchauszuege. Der Handbuchabgleich war der Auftrag des alten Gutachtens;
hier geht es um die Frage „tut der Code heute noch, was damals behauptet wurde“ — das ist am Code entscheidbar
und braucht keine Quelle.

## 3. Wie es gefahren wird — Weg A, über das Repository (Daniels Entscheidung 10.11.2026)

Daniel hat **Weg A** gewählt: Claude Code über das Abo (kein Token-Preis, nur Kontingent) — und
ausdrücklich verlangt, dass **das Modell über die Repo arbeitet, nicht lokal**.

Das ist in Werkzeug und Paket so gebaut:

| Was | Wie es erzwungen wird | Beleg |
|---|---|---|
| Prüfstand ist das **öffentliche Repo** | Das Paket nennt je Datei die `raw.githubusercontent.com`-URL mit **gepinntem Commit**; Abschnitt 2a sagt „nicht gegen den Arbeitsordner“ | `tools/opus_paket_bauen.py` (`_pin`, `_herkunft`) |
| Der **Code im Paket** ist der Repo-Blob | Die Schnitte werden per HTTP aus dem Repo geholt, nicht von der Platte; jede Datei wird gegen die Arbeitskopie gehasht und das Ergebnis im Paket gedruckt | Tabelle „Herkunft der Dateien“ im Paket |
| **Kein Zugriff auf lokale Dateien** | Der Aufruf läuft in einem **leeren Ordner außerhalb des Projekts**; `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` sind verboten, nur `WebFetch` ist erlaubt | `tools/opus_lauf.py` |
| Antwort landet als Datei | Das Modell schreibt nichts; die Standardausgabe schreibt das Werkzeug nach `docs/audits/OPUS_PRUEFUNG_<stempel>.md` und die Messung nach `opus_usage_<stempel>.json` | `tools/opus_lauf.py` |

**Herkunftsprüfung, gemessen (10.11.2026, Commit `42b646c`):** Repo ist öffentlich (API 200), alle sechs
benutzten Dateien sind abrufbar; **fünf bytegleich**, `src/auftraege.py` **nur in den Zeilenenden**
verschieden (Arbeitskopie CRLF, Blob LF — inhaltlich gleich, per Normalisierung geprüft).

```
cd D:\Arbeiten\Nebelseetal_Remake
.venv\Scripts\python.exe -X utf8 tools\opus_paket_bauen.py     # Paket aus dem Repo bauen (kostenlos)
.venv\Scripts\python.exe -X utf8 tools\opus_lauf.py --trocken   # messen, nichts aufrufen
.venv\Scripts\python.exe -X utf8 tools\opus_lauf.py --scharf    # der EINE Aufruf
```

**Freigabe liegt vor:** Daniel hat Weg A am 10.11.2026 ausdrücklich gewählt („Weg A bitte“). Der Aufruf
verbraucht **Abo-Kontingent**, keine Token-Abrechnung — es wird deshalb **kein USD-Wert behauptet**.
Trotzdem vorher nennen: Paketgröße (41.026 Zeichen / ~11.400 Prompt-Token), Zielpfad, Modell.
Lauf im Hintergrund; fertig ist er an `opus_usage_*.json`, nicht an der Antwortdatei.

## 4. Was danach passiert (der eigentliche Wert)

Ein Modellurteil ist eine Behauptung, bis es nachgerechnet ist:

1. **Jede Zeile der Antwort am Code nachschlagen** (`Datei:Zeile` aufschlagen und den Wert ausgeben).
2. **Jede Zahl nachrechnen** — die sechs Rechenaufgaben mit einem Probe-Skript, nicht im Kopf.
3. **Ergebnis als `docs/audits/ABGLEICH_OPUS_20261110.md`** mit dem Urteil des Koordinators je Zeile
   (`bestaetigt` / `widerlegt` / `offen`) und der Stelle, an der es entschieden wurde.
4. Was uebrig bleibt, geht als Befund ins Register — **eine Zeile je Befund mit Fundstelle**, nicht als
   Sammelabsatz.
5. Die Antwortdatei wird versioniert (Modellantworten gehen sonst verloren).

## 5. Ehrliche Grenzen

- Das Paket zeigt **19 Stellen**, nicht das ganze Projekt. Punkte, deren Stelle fehlt (z. B. die
  Ausbildungszeit-Kopplung in `spieloekonomie.py`), kann der Pruefer nur mit `UNBEKANNT` beantworten — das ist
  im Auftrag ausdruecklich erlaubt und kein Fehler des Laufs.
- Ein starkes Modell erfindet gern Pruefdateinamen und „wird nirgends benutzt“. Beides wird grundsaetzlich
  gegengeprueft, nicht uebernommen.
- Der Lauf ersetzt keinen Sammellauf und keine Spieltest-Beobachtung.
