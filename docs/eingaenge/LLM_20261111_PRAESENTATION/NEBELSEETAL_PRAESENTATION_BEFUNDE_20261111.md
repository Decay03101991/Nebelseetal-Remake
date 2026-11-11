# Nebelseetal Remake – Präsentation und Eigenstil: Befunde und Entwürfe

*Erarbeitet von Opus 5.5 (Thinking: Mittel), 11.11.2026, 14:00–14:40. Geprüft gegen `main` = Commit
`88efbaa` (11.11.2026, 13:54) – das ist neuer als der im Auftrag genannte `b35ac2e`. Dazu die Tags
`v0.5.0-pre.1` (`ae2c8b2`) und `v_0.0.3` (Commit `2a985c3`, 06.11.2026, 08:39).*

**Zugang:** Repository per `git clone` gelesen (nur lesend). **Nicht erreichbar:** die Pages-Startseite,
`github.com`-Seiten und die GitHub-API (Werkzeug-Freigabe verweigert, HTTP 403 über den Proxy), und
Chrome war aus dieser Sitzung nicht verbunden (`list_connected_browsers` = leer, zweimal). Alles, was
nur live prüfbar ist, steht in Teil F. Byte-Angaben unten sind Linux-Zeilenenden (LF); die Zahlen im
Auftrag sind dieselben Dateien mit Windows-Zeilenenden (CRLF): `README.md` 9.395 + 150 Zeilen = 9.545,
`index.html` 9.972 + 150 = 10.122 – kein Widerspruch.

---

## Teil A – Ist-Stand (Weg eines Besuchers)

1. **Suche:** Eine Websuche nach „Nebelseetal Remake github Decay03101991“ liefert keinen Treffer zum Repo; Topics fehlen laut Auftrag (`topics: []`) – live nicht nachgeprüft.
2. **Repo-Seite:** Beschreibung nennt laut Auftrag noch `0.5.0-pre.1`; keine Lizenz, kein Social Preview – live UNBEKANNT (GitHub nicht erreichbar).
3. **README, oben:** Logo als 1,32-MB-PNG, obwohl daneben eine WebP mit 316 KB liegt; Hinweis „Vorabversion V_0.0.3“ – richtig.
4. **README, Start-Schritte:** nennen `Nebelseetal_Remake_0.5.0-pre.1.zip` und `Nebelseetal_Remake.exe` – beides Namen des ersten Pre-Release, nicht von V_0.0.3; widerspricht Zeile 10 derselben Datei.
5. **README, Repo-Tabelle:** behauptet, Werkzeuge, Prüfdateien und Entwicklungsdoku lägen nicht im Repo – `tools/` (68), `tests/` (224) und `docs/` (812 Dateien) liegen drin.
6. **README, Rechte:** „Bilder des Originalspiels nicht Teil des Projekts“ – im Repo liegen 127 aus historischen Bildern abgeleitete Kartenbilder und 424 Dateien unter `docs/original/`.
7. **Startseite live:** laut Auftrag die Fassung 0.5.0-pre.1 mit `releases/latest`; genau diese Datei (7.116 Byte) steht im Tag `v_0.0.3` – live UNBEKANNT.
8. **Startseite im Repo:** kein Screenshot, Download-Knopf erst unter einem langen Absatz (bei 360 px ab etwa 1.000 px Höhe, also nicht im ersten Bildschirm), Palette eines Buches, nicht des Spiels.
9. **Releases:** vier Vorabversionen, die neueste ~102 MB (laut Auftrag); die Infotexte im ZIP (`release_vorlage/`) sprechen alle noch von `V_0.0.1` und `Nebelseetal_Remake.exe`.
10. **Nach dem Download:** Wer über `VORSCHAU.md` weiterliest, sieht 12 von 12 Bildern kaputt – sie zeigen auf einen gelöschten Ordner.

## Teil B – Befunde

| Nr | Befund | Beleg | Wirkung | Aufwand | Priorität |
|---|---|---|---|---|---|
| 1 | **V1 bestätigt (indirekt):** Die laut Auftrag ausgelieferte Startseite ist bytegleich die `index.html` im Tag `v_0.0.3` (Commit `2a985c3`, 06.11. 08:39) – Pages hat seit spätestens 06.11. vormittags nicht neu veröffentlicht. Mögliche Ursachen: (a) Pages-Quelle steht auf „GitHub Actions“, aber es gibt keinen Pages-Workflow; (b) die Builds seit dem 06.11. schlagen fehl; (c) eine andere Quell-Branch – ausgeschlossen, es gibt nur `main`. | `git show v_0.0.3:index.html` = 7.116 Byte, Titel `… 0.5.0-pre.1`, Link `releases/latest`; `git ls-remote` = nur `refs/heads/main`; `.github/workflows/` enthält nur `windows-test-exe.yml` | sieht eine alte Version; `releases/latest` zeigt bei ausschließlich Vorabversionen keine davon an | S | 1 |
| 2 | **V2 bestätigt:** README nennt Paket- und EXE-Namen des ersten Pre-Release; das Bauwerkzeug benennt nach `data/version.json` = `Nebelseetal_Pre_Release_V_0.0.3.exe`. Gleicher Fehler in `index.html` Z. 64. | `README.md` Z. 35, 37; `data/version.json` `dateiname`; `tools/build_public_exe.py` Z. 33, 43 | sucht im ZIP eine Datei, die es nicht gibt | S | 1 |
| 3 | Die Texte im Release-ZIP sind beim Stand V_0.0.1 stehen geblieben (Version und EXE-Name). | `release_vorlage/START_HIER.txt` Z. 1 und 5; `BEKANNTE_GRENZEN.txt` / `SYSTEMANFORDERUNGEN.txt` Z. 2 „Stand: 04.11.2026 \| Version V_0.0.1“ | widersprüchliche Anleitung im Paket selbst | S | 1 |
| 4 | README behauptet, Prüfdateien, Werkzeuge und Entwicklungsdoku seien nicht im Repo – sie sind es. | `README.md` Z. 64–65; `git ls-files`: `tools/` 68, `tests/` 224, `docs/` 812 Dateien (46 MB) | Glaubwürdigkeit der „ehrlichen“ Seite leidet genau dort, wo sie Transparenz verspricht | S | 1 |
| 5 | Rechte-Satz „Bilder des historischen Originalspiels sind nicht Teil dieses Projekts“ hält nicht: 127 Spielfeldbilder sind laut Inventar aus historischen Bildern abgeleitet; `docs/original/` enthält Handbuchbilder, Website-Grafiken und GameStar-Material. | `README.md` Z. 127–129; `docs/BILDINVENTAR.md` Z. 25–27; `docs/original/handbuch_bilder/` 244 Bilder, `docs/original/karten/gamestar/` 21 Dateien, `docs/nebelseetal_gamestar*.jpg` | rechtliches Risiko und falsche Aussage auf der Hauptseite; Klärung, ob diese Dateien öffentlich liegen dürfen, ist nicht meine Entscheidung | M | 1 |
| 6 | `VORSCHAU.md` ist verlinkt (README Z. 31, index.html Z. 125), aber alle 12 Bilder zeigen auf `assets/hintergrund_content_20261104/`, der laut `assets/referenzbilder/README.md` mit `git rm` entfernt wurde. | `VORSCHAU.md`, 12 `src=`, 12 × Ziel fehlt | „Erste Eindrücke“ = 12 kaputte Bilder | S | 1 |
| 7 | 8 Dateien `assets/original/*.gif` sind keine Bilder, sondern gespeicherte „404 Not Found“-HTML-Seiten. | `assets/original/` 8 Dateien, zusammen 1.888 Byte, Inhalt `<title>404 Not Found</title>` | Ballast, irreführende Namen | S | 3 |
| 8 | **V7 bestätigt:** kein Screenshot in README oder Startseite. Im Repo gibt es Spielaufnahmen, aber vom 02./03.11. mit ASCII-Umlauten („Fuer“, „Uebersicht“) – nicht vorzeigbar als V_0.0.3. | `docs/design/A2_3_nach_gruendung_20261103.png` 1446 × 744, 663.108 Byte | niemand sieht, wie das Spiel aussieht | M | 2 |
| 9 | **V6 teilweise widerlegt:** Die Startseite lädt bereits die WebP (`<picture>`, Z. 47–50, 316.542 Byte); nur das README bindet die PNG mit 1.324.807 Byte ein – 76 % mehr als nötig. AVIF fehlt, ist aber nicht nötig. | `README.md` Z. 3; `assets/bilder/logo_nebelseetal_klein.webp` 1600 × 754 | langsamer erster Eindruck auf GitHub mobil | S | 2 |
| 10 | **V8 bestätigt:** Web-Gold `#edce87` auf Blaugrau `#12161c` gegen Spiel-Gold `#FFCC33` auf Rotbraun `#2a0605`. Gerendert sitzt das Logo (Nebel, warmes Banner) auf `#2a0605` deutlich stimmiger. | `index.html` Z. 9–11; `src/main.py` Z. 3788–3800 | Web und Spiel wirken wie zwei Projekte | M | 2 |
| 11 | Spielrot `#e53935` auf Spielgrund `#2a0605` hat 4,41 : 1 – knapp unter WCAG 4,5 : 1; im Spiel betrifft das die Fehlermeldung am Passworttor. | `src/main.py` Z. 8415, 8437; Rechnung Teil E | schlechter lesbare Warnung | S | 3 |
| 12 | Die Blackletter-Überschrift des Spiels hängt an einer installierten Schrift: im Repo liegt keine Schriftdatei; fehlt „Blackletter“ auf dem Rechner, ersetzt Tk sie durch die Standardschrift. | `src/main.py` Z. 8397 `font=("Blackletter", 44, "bold")`; `git ls-files` = 0 `.ttf/.otf/.woff` | das Erkennungszeichen fehlt womöglich bei Testern | M | 2 |
| 13 | **V9 widerlegt:** Die Chronik-PDF ist verlinkt; ihr fehlt nur eine Größenangabe (9.770.115 Byte). | `README.md` Z. 31; `index.html` Z. 121 | unerwarteter 9,8-MB-Download mobil | S | 3 |
| 14 | Typografie: durchgehend Geviertstrich „—“ (englische Konvention), kein Halbgeviertstrich „–“; Release-Texte ganz ohne Umlaute. | `README.md` 15 × „—“, 0 × „–“; `index.html` 13 × `&mdash;`; `START_HIER.txt` „OEFFENTLICHE“, „noetig“ | wirkt übersetzt bzw. unfertig | S | 3 |
| 15 | Mobil (gerendert, 360 px, Chrome): kein Querscrollen (`scrollWidth` 360), aber 5.168 px Seitenhöhe, Titel in 44 px bricht mit großer Lücke in zwei Zeilen, Download-Knopf erst unter dem ersten Bildschirm. Entwurf D: Knopf bei etwa 580 px, Seite 4.359 px. | Rendering `index.html` @ 360 × 740 | auf dem Telefon kein Download ohne Scrollen | S | 2 |

Nebenbefund ohne eigene Zeile: Der manuelle Windows-Workflow sucht `release_public\Nebelseetal_Remake_Testversion.exe` und lädt `…_Testversion_FIX04j.zip` hoch; das Bauwerkzeug erzeugt aber `Nebelseetal_Pre_Release_V_0.0.3.exe/.zip`. Nach dem Code müsste der Lauf beim Schritt „EXE pruefen“ scheitern (nicht ausgeführt; `.github/workflows/windows-test-exe.yml` Z. 28, 36; `tools/build_public_exe.py` Z. 43, 92).

## Teil C – Entwurf README (vollständig)

Als eigene Datei beigelegt: `README.md`. Gleicher Text:

````markdown
<p align="center">
  <img src="assets/bilder/logo_nebelseetal_klein.webp" alt="Nebelseetal – Logo: das Banner mit dem Schriftzug NEBELSEETAL im Nebel" width="720">
</p>
<p align="center"><sub>Logo: <b>Chris Fred Däubner</b>, entworfen für Daniel Kössl</sub></p>

<h1 align="center">Nebelseetal Remake</h1>

<p align="center">
  <b>Eine zersprungene Welt im Nebel: Du baust Siedlungen auf, forschst, rüstest aus und ziehst durch Portale –<br>
  neben fünf Nachbarn, die selbst wirtschaften, bauen und rauben.</b>
</p>

<p align="center">
  Einzelspieler · Windows 11, 64 Bit · offline · kostenlos · kein Konto<br>
  <a href="https://github.com/Decay03101991/Nebelseetal-Remake/releases/tag/v_0.0.3"><b>Testversion V_0.0.3 herunterladen</b></a>
  · <a href="https://decay03101991.github.io/Nebelseetal-Remake/">Startseite</a>
  · <a href="#was-noch-fehlt">Was noch fehlt</a>
</p>

> **Dies ist eine Vorabversion** (`V_0.0.3`, 06.11.2026). Sie ist zum Ausprobieren und Fehlersammeln
> gedacht, nicht als fertiges Spiel. Was fehlt, steht ehrlich unter [Was noch fehlt](#was-noch-fehlt).

<!-- BILDPLATZ: Screenshot aus V_0.0.3, 1600 × 900, WebP unter 250 KB, Datei assets/bilder/screenshot_v003.webp.
     Wenn vorhanden, diese Zeile einsetzen (Kommentarzeichen entfernen):
<p align="center"><img src="assets/bilder/screenshot_v003.webp" alt="Spielansicht: Dorfzentrum mit Ressourcenleiste" width="800"></p>
-->

---

## Was das Spiel ist

Du übernimmst die Rolle eines Herrschers in einer zersprungenen Welt. Sechs Bruchstücke treiben im
magischen Raum Limbus, verbunden nur durch Portale. Du gründest Siedlungen, produzierst Rohstoffe,
stellst Waren her, forschst, rüstest aus, bildest Einheiten aus, kämpfst und reist in andere Welten.

Der Kreislauf: **gründen → produzieren → forschen → ausrüsten → ausbilden → bewegen → kämpfen → punkten.**

Einen Sieg gibt es nicht, sondern Ruhm: vier Auszeichnungen – **Feldherr, Forscher, Händler,
Gesamtherrscher**. Die fünf Nachbarn haben Namen und Gewohnheiten: Haug raubt, Brynhild wacht, Grom baut,
Silra späht, Krank vergisst nichts. Die vollständige Anleitung steht im Spiel beim Berater.

## Was steckt drin

| | Anzahl | steht in |
|---|---:|---|
| Welten im Limbus (belegt) | 6 | `data/welten.json` |
| Häuser (Fraktionen) mit Wappen | 6 | `data/voelker.json` |
| Nachbarn mit eigener Wirtschaft | 5 | `data/bot_*.json` |
| Siedlungen je Reich | bis zu 6 | `data/resources.json` |
| Einheiten | 28 | `data/units.json` |
| Gebäude | 20 | `data/buildings.json` |
| Forschungen | 21 | `data/research.json` |
| Waren | 17 | `data/items.json` |
| Rohstoffe | 9 | `data/resources.json` |
| Geländearten | 7 | `data/gelaende.json` |
| Auszeichnungen | 4 | `data/ruhm.json` |

## In fünf Schritten starten

1. Unter [Releases](https://github.com/Decay03101991/Nebelseetal-Remake/releases/tag/v_0.0.3) das Paket
   `Nebelseetal_Pre_Release_V_0.0.3.zip` herunterladen (rund 102 MB). [PRÜFEN: Name und Größe gegen das Release-Asset]
2. Den Inhalt in einen **neuen, leeren Ordner** entpacken (nicht in einen Windows-geschützten Ordner).
3. `Nebelseetal_Pre_Release_V_0.0.3.exe` per Doppelklick starten. Python ist nicht nötig.
4. Am Tor ein **eigenes Passwort** festlegen und notieren – es bleibt lokal auf dem Rechner.
5. Spielen. Fehler bitte nach `FEHLER_MELDEN.txt` (liegt im ZIP) notieren.

Die Testversion startet **leer**: keine mitgelieferten Spielstände, kein fremdes Passwort. Der
Spielstand liegt unter `%LOCALAPPDATA%\Nebelseetal_Remake\Demo`. Voraussetzungen und Grenzen stehen in
`SYSTEMANFORDERUNGEN.txt` und `BEKANNTE_GRENZEN.txt` im ZIP.

**macOS:** Es gibt **keine** `.app`. Eine echte Fassung müsste auf einem Mac gebaut *und geprüft*
werden – dieser Rechner ist ein Windows-Rechner, deshalb wird hier nichts angeboten, was niemand
getestet hat.

## Was noch fehlt

- **Vorabversion.** Kein fertiges Spiel, keine Kompatibilitätszusage.
- **Drei Kampfregeln fehlen:** Fluchtformel, Beute-Reihenfolge (Gold zuerst), Mauerreparatur mit Bauzeit.
- **Sechs Welten sind noch nicht fertig umgestellt.** Im Spielcode liegen derzeit 20 Limbus-Dimensionen,
  von denen sechs mit den belegten Welten belegt sind; 14 sind leer. Der Umbau auf sechs Welten läuft.
- **Diplomatie erst zur Hälfte:** Gunst und Status sind da; Verträge, Rache und die drei Ereignisse sind
  entworfen, aber noch nicht eingebaut.
- **Handelspunkte** sind gebaut, werden aber noch nicht gebucht und stehen auf null.
- **Kein Ton, keine Musik.** Die Oberfläche ist eine Windows-Oberfläche mit Ingame-Fenstern.
- **Nur auf Windows getestet** (Windows 11, 64 Bit, ein Rechner). Windows 10, ARM und kleine Displays sind ungeprüft.
- **Admin-Werkzeuge sind in dieser Fassung gesperrt.** Sie gehören zur Entwicklerfassung, nicht zur Testversion.
- **SmartScreen kann warnen**, weil die EXE nicht signiert ist. Die Prüfsumme steht in `SHA256SUMS.txt` im ZIP.

## Weiterlesen

| | |
|---|---|
| [Die offizielle Erklärung](SPIEL_ERKLAERUNG.md) | was das Spiel ist – und was es nicht ist |
| [Sechs Häuser, sechs Welten](FRAKTIONEN_WELTEN.md) | die Fraktionen, ihre Wappen, die Welten |
| [Die Chronik der Welt](CHRONIK_DER_WELT.md) | die Geschichte der Welt als Buch · [als PDF, 9,8 MB](CHRONIK_DER_WELT.pdf) |
| [Wie dieses Spiel entstanden ist](BESUCHER.md) | Arbeitsweise, KI-Einsatz, Sicherheit |
| [Erste Eindrücke einer späteren Version](VORSCHAU.md) | [PRÜFEN: die 12 Bilder darin zeigen auf den entfernten Ordner `assets/hintergrund_content_20261104/` – erst reparieren, dann verlinken] |

## Was in diesem Repository liegt

| Ordner / Datei | Inhalt |
|---|---|
| `src/` | der Spielcode, jeder Block und jede Funktion am Zeilenende erklärt |
| `data/` | alle Spieldaten als JSON – Einheiten, Waren, Gebäude, Forschungen, Welten, Texte |
| `assets/` | Bilder: Icons, Karten, Wappen, Burgen, Gebäudehintergründe (497 Dateien, rund 64 MB) |
| `release_vorlage/` | die Infodateien, die im Release-ZIP liegen |
| `docs/` | Entwicklungsdokumentation, Prüfberichte, Quellen (812 Dateien) |
| `tools/` | Bau- und Prüfwerkzeuge (68 Dateien) |
| `tests/` | Prüfdateien (224 Dateien) |
| `START_SPIEL_WINDOWS.bat` | das Spiel aus dem Quellcode starten (braucht Python) |

[PRÜFEN: Die bisherige Fassung sagte „Nicht im Repository: Prüfdateien, Werkzeuge und die
Entwicklungsdokumentation“. Am Stand `88efbaa` liegen sie im Repository. Entweder diese Tabelle behalten
oder die Ordner aus dem öffentlichen Stand nehmen – aber nicht beides behaupten.]

## Herkunft und Transparenz

Das Remake entsteht als **Arbeit von Daniel Kössl mit einem Hermes-Agent-System und dessen
Coding-Subagenten**. Die Agenten haben Code geschrieben, geprüft und dokumentiert; die Entscheidungen
über Inhalt, Ton, Regeln und Gestaltung liegen beim Entwickler.

**Der Agent hat einen Namen: „Weltenfresser“.** Er ist der Hermes-Agent von Daniel Kössl und läuft auf
dessen Rechner. Seine Rolle im Projekt, offen gesagt:

| Rolle | Was der Agent konkret tut |
|---|---|
| **Umsetzer** | schreibt den Spielcode und die Datendateien, Modul für Modul, jede Zeile erklärt |
| **Prüfer** | legt Prüfdateien an, rechnet Zahlen gegen die Originalquellen nach, fährt Prüfläufe über den ganzen Code und meldet, was rot ist – auch wenn es seine eigene Arbeit war |
| **Chronist** | führt Entwicklungsprotokoll, Prüfregister und Übergaben, damit keine Entscheidung verloren geht |
| **Koordinator** | zerlegt große Aufgaben in Schnitte, delegiert an Subagenten, führt deren Ergebnisse zusammen |
| **Autor mit Grenzen** | schreibt Dokumente und Entwürfe – aber die Geschichte der Welt und die Gestaltung des Buches kamen aus einem bewusst stärkeren Modell, auf Anweisung des Entwicklers |
| **Bremse** | hält an, wenn eine Entscheidung dem Entwickler gehört: was Regeln, Geld, Daten oder Spielgefühl betrifft, wird gefragt statt entschieden |

Wo der Agent irrt, steht der Irrtum im Protokoll – falsche Schnitte, fehlerhafte Messungen und
widerlegte Annahmen eingeschlossen. Das ist Absicht: Ein Agent, der seine Fehler aufschreibt, ist
prüfbar; einer, der sie weglässt, nicht.

**Sicherheit und Kontrolle stehen an erster Stelle** – im ganzen System und damit auch im
Entwicklungssystem. Die Agenten arbeiten hierarchisch nach Regeln und Skills, und die Rechte sind
geteilt: Es gibt Rollen, die nur lesen dürfen, und Rollen, die schreiben dürfen. Was eine Rolle nicht
darf, kann sie auch nicht versehentlich tun. Jede Änderung an einer Regel oder einem Skill wird mit
Grund, Freigabe und Rückrollweg protokolliert.

Welche KI wofür eingesetzt wurde, grob:

| KI | Auftrag (grob) | Ausgaben (grob) |
|---|---|---|
| Hermes-Agent mit `deepseek-v4-flash` | der Hauptteil der Arbeit: Code, Prüfungen, Dokumentation | der überwiegende Teil der Gesamtausgaben |
| Großes DeepSeek-Modell (`deepseek-v4-pro`), einzelne Aufträge | Entwürfe für Regeln, Konzepte und die Chronik der Welt | wenige Cent je Auftrag |
| GPT-6-Astra | einzelne Bilddeutungen und Gutachten | rund ein US-Dollar je Auftrag |
| GPT-Chat-Abo | einzelne Text- und Gestaltungsteile | im Abo enthalten |

**Gesamtausgaben für KI bis zu dieser Vorabversion: rund 52 US-Dollar**, überwiegend für
`deepseek-v4-flash`. Keine Token-Zahlen, keine Prompts, keine Protokolle – nur diese grobe Zuordnung.
[PRÜFEN: Seit dieser Zeile sind weitere Aufträge an Claude Opus 5.5 hinzugekommen (Abo); ggf. eine Zeile ergänzen.]

**Zum früheren Stand:** Ein früherer Stand dieses Projekts war bereits auf GitHub veröffentlicht. Der
Entwickler hat diesen Stand zurückgenommen und das Projekt neu bewertet. Dieses Repository ist der
daraus hervorgegangene, offizielle Pre-Release-Stand.

## Rechte

Der Quelltext ist einsehbar. Eine Nutzungslizenz ist für diese Vorabversion **noch nicht festgelegt** –
wer den Code verwenden will, fragt bitte vorher.

[PRÜFEN: Die bisherige Fassung sagt „Die Bilder des historischen Originalspiels sind nicht Teil dieses
Projekts“. Laut `docs/BILDINVENTAR.md` sind die 127 Bilder in `assets/karten/spielfeld/` aus historischen
Bildern unter `assets/karten/original/` abgeleitet, und `docs/original/` enthält Handbuchbilder,
Website-Grafiken und GameStar-Material. Diesen Satz erst wieder einsetzen, wenn das geklärt ist.]

**Logo:** Das Banner mit dem Schriftzug NEBELSEETAL hat **Chris Fred Däubner** für Daniel Kössl
entworfen. Es ist ein fertiges Werk und steht unter seinem Urheberrecht – es wird hier mit seiner
Zustimmung gezeigt und darf nicht ohne seine Erlaubnis weiterverwendet werden. Die Datei liegt als
`assets/referenzbilder/Logo_Nebelseetal_20261106.png` (Original, 3500 × 3500, freigestellt) und als
web-optimierte Fassung `assets/bilder/logo_nebelseetal_klein.png` bzw. `.webp`.

**Bildwelt:** Die gemalten Panoramen, Gebäudekacheln und Banner des Nebelseetals stammen von
**Chris Fred Däubner**. Er hat sie mit KI eigens für dieses Spiel erzeugt, danach selbst bearbeitet
und an Daniel Kössl geliefert; sie stehen unter seinem Urheberrecht und dürfen nicht ohne seine
Erlaubnis weiterverwendet werden. Ablage, Zuordnung und Messungen stehen in
`docs/design/DESIGN_LIEFERUNG_CHRIS_20261109.md`.

**Chris im Netz:** Chris Fred Däubner zeigt seine Arbeiten auf Instagram unter
[three_ghosts.mp4](https://www.instagram.com/three_ghosts.mp4). Der Link steht hier **auf seinen Wunsch** und ist die einzige
Stelle im Projekt, die auf seine Seite führt.

## Fehler melden

Bitte als [Issue](https://github.com/Decay03101991/Nebelseetal-Remake/issues/new?template=fehlerbericht.md)
melden: was du getan hast, was du erwartet hast und was passiert ist – ohne Passwörter und ohne private
Spielstände. Dasselbe Formular liegt als `FEHLER_MELDEN.txt` im Release-ZIP.
````

## Teil D – Entwurf Startseite (vollständig)

Als eigene Datei beigelegt: `index.html`. Gerendert geprüft bei 360 px (kein Querscrollen, Download-Knopf im ersten Bildschirm) und 1280 px. Fehlende Buchschrift fällt auf Georgia zurück. Gleicher Text:

````html
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nebelseetal Remake – Pre-Release V_0.0.3</title>
<meta name="description" content="Einzelspieler-Remake des historischen Browserspiels Nebelseetal. Windows-Testversion, lokal und offline, kostenlos, ohne Konto.">
<meta name="theme-color" content="#2a0605">
<!-- Vorschaukarte beim Teilen. og:image braucht eine ABSOLUTE Adresse. Bild: unveraenderte Logo-Datei.
     [PRÜFEN: nach dem Veroeffentlichen mit einem Link-Vorschau-Werkzeug testen] -->
<meta property="og:title" content="Nebelseetal Remake – Pre-Release V_0.0.3">
<meta property="og:description" content="Einzelspieler-Remake des historischen Browserspiels Nebelseetal. Windows, offline, kostenlos.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://decay03101991.github.io/Nebelseetal-Remake/">
<meta property="og:image" content="https://decay03101991.github.io/Nebelseetal-Remake/assets/bilder/logo_nebelseetal_klein.png">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="754">
<meta property="og:image:alt" content="Logo Nebelseetal von Chris Fred Däubner">
<!--
  Entwurf: Opus 5.5 (Thinking: Mittel), 11.11.2026, gegen Repo-Kopf 88efbaa.

  PALETTE = Spielpalette aus src/main.py, Skin "standard" (Zeilen 3788-3800).
  Zwei Abweichungen, beide begruendet:
    --pergament #F2E3BF  Fliesstext. Das Spiel-Textgelb #FFFF99 (17,77:1) blendet bei langen Absaetzen;
                         es bleibt fuer kurze Hervorhebungen (Zahlen).
    --warnrot   #ef6b5b  Warnschrift. Das Spielrot #e53935 hat auf #2a0605 nur 4,41:1 (unter 4,5:1)
                         und bleibt nur fuer Linien/Rahmen.

  KONTRASTE (WCAG 2.x, relative Leuchtdichte, gerechnet):
    #F2E3BF auf #2a0605  14,66:1   Fliesstext auf Grund
    #F2E3BF auf #3e1c1a  11,92:1   Fliesstext in Kaesten
    #FFCC33 auf #2a0605  12,37:1   Ueberschriften, Links
    #FFCC33 auf #3e1c1a  10,06:1   Links in Kaesten
    #FFCC33 auf #1a0a09  12,77:1   Kopf- und Fusszeile
    #FFFF99 auf #3e1c1a  14,44:1   Zahlen
    #C0C0C0 auf #2a0605  10,24:1   Nebentext
    #C0C0C0 auf #1a0a09  10,58:1   Fusszeile
    #2a0605 auf #FFCC33  12,37:1   Hauptknopf
    #FFCC33 auf #3e2723   9,17:1   Zweitknopf
    #FFCC33 auf #5D4037   6,18:1   Zweitknopf beim Darueberfahren
    #FF6600 auf #2a0605   6,35:1   Akzent (nur Unterzeilen)
    #ef6b5b auf #3e1c1a   5,00:1   Warnschrift in Kaesten
  Kein Paar liegt unter 4,5:1.

  KEINE externen Abhaengigkeiten: keine Webfont, kein CDN, kein Skript, kein Tracking.
  Bildgewicht beim Laden: Logo-WebP 316.542 Byte (PNG-Ersatz 1.324.807 nur ohne WebP-Unterstuetzung),
  Portrait 194.338 Byte (erst beim Scrollen). Das Logo wird unveraendert gezeigt.
-->
<style>
  :root{
    --grund:#2a0605; --flaeche:#3e1c1a; --tief:#1a0a09; --rahmen:#4a1512;
    --gold:#FFCC33; --hell:#FFFF99; --pergament:#F2E3BF; --silber:#C0C0C0;
    --knopf:#3e2723; --knopf-aktiv:#5D4037; --akzent:#FF6600; --rot:#e53935; --warnrot:#ef6b5b;
    --titelschrift:"Blackletter","UnifrakturMaguntia","Old English Text MT","Goudy Text MT","Fraktur",Georgia,serif;
    --textschrift:Georgia,"Palatino Linotype","Book Antiqua",serif;
    --abstand:8px; --ecke:4px;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0;background:var(--grund);color:var(--pergament);font:17px/1.6 var(--textschrift)}
  a{color:var(--gold);text-underline-offset:3px}
  a:hover{color:var(--hell)}
  a:focus-visible,.knopf:focus-visible{outline:2px solid var(--hell);outline-offset:3px}

  /* Kopfleiste wie im Spiel: tiefes Braun, goldene Linie */
  .kopf{background:var(--tief);border-bottom:2px solid var(--gold);padding:10px 16px;
    display:flex;justify-content:space-between;align-items:center;gap:12px;font-size:15px}
  .kopf b{font-family:var(--titelschrift);color:var(--gold);font-size:20px;font-weight:normal;letter-spacing:.5px}
  .kopf span{color:var(--silber)}

  /* Buehne: Nebelbaender aus reinen CSS-Verlaeufen, kein Bild */
  .buehne{position:relative;overflow:hidden;text-align:center;padding:24px 16px 40px;
    background:
      radial-gradient(60% 40% at 15% 70%, rgba(242,227,191,.10), transparent 70%),
      radial-gradient(55% 35% at 85% 60%, rgba(242,227,191,.08), transparent 70%),
      radial-gradient(90% 60% at 50% 0%, #3e1c1a 0%, var(--grund) 70%);
    border-bottom:1px solid var(--rahmen)}
  .logo{display:block;width:100%;max-width:880px;height:auto;margin:0 auto}
  .urheber{margin:4px 0 18px;font-size:14px;color:var(--silber)}
  h1{font-family:var(--titelschrift);font-weight:normal;color:var(--gold);
    font-size:clamp(30px,8vw,52px);line-height:1.1;margin:0 0 6px;letter-spacing:.5px}
  .unterzeile{color:var(--akzent);font-size:15px;letter-spacing:.06em;text-transform:uppercase;margin:0 0 16px}
  .pitch{max-width:640px;margin:0 auto 22px;font-size:19px}
  .knoepfe{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin:0 0 14px}
  .knopf{display:inline-block;min-height:48px;padding:13px 22px;border-radius:var(--ecke);
    font-size:17px;text-decoration:none;border:1px solid var(--gold)}
  .knopf.haupt{background:var(--gold);color:var(--grund);font-weight:bold}
  .knopf.haupt:hover{background:var(--hell);color:var(--grund)}
  .knopf.zweit{background:var(--knopf);color:var(--gold)}
  .knopf.zweit:hover{background:var(--knopf-aktiv);color:var(--gold)}
  .eckdaten{font-size:15px;color:var(--silber);margin:0}

  main{max-width:920px;margin:0 auto;padding:8px 16px 48px}
  h2{font-family:var(--titelschrift);font-weight:normal;color:var(--gold);font-size:30px;line-height:1.2;
    margin:44px 0 14px;padding-bottom:6px;border-bottom:1px solid var(--rahmen)}
  p{margin:0 0 14px}
  ul,ol{padding-left:22px;margin:0 0 14px} li{margin:6px 0}
  .kasten{background:var(--flaeche);border:1px solid var(--rahmen);border-radius:var(--ecke);padding:16px 18px;margin:0 0 16px}

  /* Zahlen: zwei Spalten am Telefon, fuenf am Bildschirm */
  .zahlen{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;padding:0;margin:0;list-style:none}
  .zahlen li{margin:0;background:var(--flaeche);border:1px solid var(--rahmen);border-radius:var(--ecke);
    padding:12px 10px;text-align:center}
  .zahlen b{display:block;font-size:30px;line-height:1.1;color:var(--hell);font-weight:normal}
  .zahlen span{font-size:15px}
  @media (min-width:640px){.zahlen{grid-template-columns:repeat(5,1fr)}}

  /* Bildplatz fuer den Screenshot */
  .bildplatz{margin:0 0 16px}
  .bildplatz .rahmen{aspect-ratio:16/9;border:2px dashed var(--gold);border-radius:var(--ecke);
    background:var(--tief);display:flex;align-items:center;justify-content:center;padding:16px;text-align:center;
    color:var(--silber);font-size:15px}
  .bildplatz img{display:block;width:100%;height:auto;border:1px solid var(--gold);border-radius:var(--ecke)}
  figcaption{font-size:14px;color:var(--silber);margin-top:6px}

  .fehlt li::marker{color:var(--warnrot)}
  .fehlt strong{color:var(--warnrot)}
  .leise{color:var(--silber);font-size:15px}
  code{font-family:Consolas,"Courier New",monospace;font-size:.9em;color:var(--hell);overflow-wrap:anywhere}

  .wer{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}
  .wer img{width:120px;height:auto;border:1px solid var(--gold);border-radius:var(--ecke);flex:none}
  .wer div{flex:1;min-width:200px}

  footer{background:var(--tief);border-top:2px solid var(--gold);padding:20px 16px 28px;color:var(--silber);font-size:14px}
  footer .innen{max-width:920px;margin:0 auto}
  footer p{margin:0 0 10px}
  @media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style>
</head>
<body>

<div class="kopf"><b>Nebelseetal</b><span>Pre-Release V_0.0.3 · 06.11.2026</span></div>

<header class="buehne">
  <picture>
    <source srcset="assets/bilder/logo_nebelseetal_klein.webp" type="image/webp">
    <img class="logo" src="assets/bilder/logo_nebelseetal_klein.png" width="1600" height="754"
         alt="Logo: das Banner mit dem Schriftzug NEBELSEETAL im Nebel">
  </picture>
  <p class="urheber">Logo: <strong>Chris Fred Däubner</strong> · entworfen für Daniel Kössl</p>

  <h1>Nebelseetal Remake</h1>
  <p class="unterzeile">Einzelspieler · Windows · offline · kostenlos</p>
  <p class="pitch">Eine zersprungene Welt im Nebel: Du baust Siedlungen auf, forschst, rüstest aus und
    ziehst durch Portale – neben fünf Nachbarn, die selbst wirtschaften, bauen und rauben.</p>

  <div class="knoepfe">
    <!-- [PRÜFEN: Tag v_0.0.3 erreichbar? Alternative: /releases/latest – zeigt aber KEINE Vorabversion] -->
    <a class="knopf haupt" href="https://github.com/Decay03101991/Nebelseetal-Remake/releases/tag/v_0.0.3">Testversion herunterladen</a>
    <a class="knopf zweit" href="https://github.com/Decay03101991/Nebelseetal-Remake">Quellcode ansehen</a>
  </div>
  <!-- [PRÜFEN: Downloadgroesse gegen das Release-Asset; laut Auftrag 102.098.672 Byte = rund 102 MB] -->
  <p class="eckdaten">Windows 11, 64 Bit · Download rund 102 MB · kein Konto, kein Internet, kein Python</p>
</header>

<main>

  <h2>Was steckt drin</h2>
  <!-- Belegt in data/: units.json 28, items.json 17, buildings.json 20, research.json 21,
       gelaende.json 7, resources.json 9 Rohstoffe / max_siedlungen 6, welten.json welten_belegt 6,
       voelker.json 6 Fraktionen, ruhm.json 4 Stufen. 5 Nachbarn: README/SPIEL_ERKLAERUNG. -->
  <ul class="zahlen">
    <li><b>6</b><span>Welten im Limbus</span></li>
    <li><b>6</b><span>Häuser mit Wappen</span></li>
    <li><b>5</b><span>Nachbarn mit eigener Wirtschaft</span></li>
    <li><b>6</b><span>Siedlungen je Reich</span></li>
    <li><b>4</b><span>Auszeichnungen statt Sieg</span></li>
    <li><b>28</b><span>Einheiten</span></li>
    <li><b>20</b><span>Gebäude</span></li>
    <li><b>21</b><span>Forschungen</span></li>
    <li><b>17</b><span>Waren</span></li>
    <li><b>9</b><span>Rohstoffe</span></li>
  </ul>
  <p class="leise" style="margin-top:12px">Der Kreislauf: gründen → produzieren → forschen → ausrüsten →
    ausbilden → bewegen → kämpfen → punkten. Die vollständige Anleitung steht im Spiel beim Berater.</p>

  <figure class="bildplatz">
    <!-- BILDPLATZ – Anforderung an den Screenshot:
         Groesse   1600 × 900 px (16:9), als WebP unter 250 KB plus PNG-Ersatz; Datei:
                   assets/bilder/screenshot_v003.webp / .png
         Ausschnitt das ganze Spielfenster ohne Windows-Rahmen und Taskleiste, Fenster maximiert
         Inhalt    Dorfzentrum einer Siedlung mitten im Spiel (nicht frisch gegruendet): Ressourcenleiste
                   oben mit Zahlen ungleich 0, ein gemaltes Gebaeude- oder Fraktionsbild sichtbar,
                   Seitenleiste mit Punkten, KEINE Fehlermeldung, KEIN Admin-Menue, keine Passwortanzeige
         Fassung   genau V_0.0.3 (Unterzeile im Fenster pruefen), Skin "standard"
         Einbau    den Rahmen-DIV unten ersetzen durch:
           <picture><source srcset="assets/bilder/screenshot_v003.webp" type="image/webp">
           <img src="assets/bilder/screenshot_v003.png" width="1600" height="900" loading="lazy"
                alt="Spielansicht: Dorfzentrum mit Ressourcenleiste"></picture>
    -->
    <div class="rahmen">Hier kommt ein Bild aus dem Spiel hin (Fassung V_0.0.3, 1600 × 900).</div>
    <figcaption>Spielansicht, Pre-Release V_0.0.3.</figcaption>
  </figure>

  <h2>Was noch fehlt – ehrlich</h2>
  <div class="kasten">
    <ul class="fehlt">
      <li><strong>Vorabversion.</strong> Kein fertiges Spiel, keine Kompatibilitätszusage.</li>
      <li><strong>Drei Kampfregeln fehlen:</strong> Fluchtformel, Beute-Reihenfolge, Mauerreparatur mit Bauzeit.</li>
      <li><strong>Sechs Welten sind noch nicht fertig umgestellt:</strong> im Code liegen 20 Limbus-Dimensionen,
        sechs sind belegt, 14 leer.</li>
      <li><strong>Diplomatie erst zur Hälfte:</strong> Gunst und Status sind da; Verträge, Rache und die drei
        Ereignisse sind entworfen, aber nicht eingebaut.</li>
      <li><strong>Handelspunkte</strong> werden noch nicht gebucht und stehen auf null.</li>
      <li><strong>Kein Ton, keine Musik.</strong></li>
      <li><strong>Nur Windows 11, 64 Bit, auf einem Rechner getestet.</strong> Windows 10, ARM und kleine
        Displays sind ungeprüft. Eine macOS-Fassung gibt es nicht – sie müsste auf einem Mac gebaut und geprüft werden.</li>
      <li><strong>SmartScreen kann warnen</strong>, weil die EXE nicht signiert ist. Die Prüfsumme steht in
        <code>SHA256SUMS.txt</code> im ZIP.</li>
    </ul>
  </div>

  <h2>So startest du</h2>
  <ol>
    <!-- [PRÜFEN: Dateinamen gegen die Assets des Releases v_0.0.3; laut data/version.json
         heisst die EXE Nebelseetal_Pre_Release_V_0.0.3.exe] -->
    <li>Unter <a href="https://github.com/Decay03101991/Nebelseetal-Remake/releases/tag/v_0.0.3">Releases</a>
      das Paket <code>Nebelseetal_Pre_Release_V_0.0.3.zip</code> laden.</li>
    <li>Den Inhalt in einen <strong>neuen, leeren Ordner</strong> entpacken (kein geschützter Windows-Ordner).</li>
    <li><code>Nebelseetal_Pre_Release_V_0.0.3.exe</code> per Doppelklick starten.</li>
    <li>Am Tor ein <strong>eigenes Passwort</strong> festlegen und notieren. Es bleibt auf deinem Rechner.</li>
    <li>Spielen. Der Spielstand liegt unter <code>%LOCALAPPDATA%\Nebelseetal_Remake\Demo</code>.</li>
  </ol>

  <h2>Weiterlesen</h2>
  <ul>
    <li><a href="https://github.com/Decay03101991/Nebelseetal-Remake/blob/main/SPIEL_ERKLAERUNG.md">Die offizielle Erklärung</a>
      <span class="leise">– was das Spiel ist und was es nicht ist</span></li>
    <li><a href="https://github.com/Decay03101991/Nebelseetal-Remake/blob/main/FRAKTIONEN_WELTEN.md">Sechs Häuser, sechs Welten</a>
      <span class="leise">– Fraktionen mit Wappen</span></li>
    <li><a href="https://github.com/Decay03101991/Nebelseetal-Remake/blob/main/CHRONIK_DER_WELT.md">Die Chronik der Welt</a>
      <span class="leise">– als Text, oder als
      <a href="https://github.com/Decay03101991/Nebelseetal-Remake/blob/main/CHRONIK_DER_WELT.pdf">PDF (9,8 MB)</a></span></li>
    <li><a href="https://github.com/Decay03101991/Nebelseetal-Remake/blob/main/BESUCHER.md">Wie dieses Spiel entstanden ist</a>
      <span class="leise">– Arbeitsweise, KI-Einsatz, Sicherheit</span></li>
  </ul>

  <h2>Wer dahinter steht</h2>
  <div class="kasten wer">
    <img src="assets/bilder/daniel_portrait_klein.png" width="476" height="640" loading="lazy" alt="Daniel Kössl">
    <div>
      <p><strong>Daniel Kössl</strong>, angehender Fachinformatiker für Systemintegration – mit dem Hermes-Agent
        <strong>Weltenfresser</strong>, der Code, Prüfungen und Dokumentation beisteuert. Die Entscheidungen über
        Inhalt, Regeln und Gestaltung liegen bei Daniel.</p>
      <p class="leise">Fehler gefunden? Bitte als <a href="https://github.com/Decay03101991/Nebelseetal-Remake/issues">Issue</a>
        melden – was du getan hast, was du erwartet hast, was passiert ist. Ohne Passwörter, ohne private Spielstände.</p>
    </div>
  </div>

</main>

<footer>
  <div class="innen">
    <p><strong>Logo und Bildwelt:</strong> Chris Fred Däubner. Unter seinem Urheberrecht; Weiterverwendung nur mit
      seiner Erlaubnis.</p>
    <p><strong>Quelltext:</strong> einsehbar; eine Nutzungslizenz ist für diese Vorabversion noch nicht festgelegt.
      Wer den Code verwenden will, fragt bitte vorher.</p>
    <p>Nebelseetal Remake · Pre-Release V_0.0.3 · 06.11.2026 ·
      <a href="https://github.com/Decay03101991/Nebelseetal-Remake">Repository</a> ·
      <a href="https://github.com/Decay03101991/Nebelseetal-Remake/issues">Fehler melden</a></p>
  </div>
</footer>

</body>
</html>
````

## Teil E – Gestalt-Spezifikation (Web und Spiel)

**Grundsatz:** Das Web übernimmt die Spielpalette. Das Logo ist auf Rotbraun gemalt gedacht – auf
`#2a0605` verschmilzt sein Nebel mit dem Grund, auf dem bisherigen Blaugrau steht es als Fremdkörper
(beides gerendert verglichen). Die Buchpalette (`#edce87`, `#945c2b`, `#12161c`) bleibt nur für die
Chronik als Buch.

| Wert | Rolle | gilt in | Begründung |
|---|---|---|---|
| `#2a0605` | Grund | Spiel, Web | Spielgrund (`main.py` Z. 3789); trägt das Logo ohne Kante. |
| `#3e1c1a` | Fläche, Kasten | Spiel, Web | Spiel-Panel; hebt Kästen um eine Stufe ab, ohne Rahmen zu brauchen. |
| `#1a0a09` | Kopf- und Fußleiste | Spiel, Web | wie Spiel-Topbar; gibt der Seite oben und unten dieselbe Klammer wie dem Spielfenster. |
| `#4a1512` | Rahmen, Trennlinien | Spiel, Web | Spiel-Rahmen; dunkler als Gold, damit Linien ordnen statt glänzen. |
| `#FFCC33` | Gold: Titel, Links, Hauptknopf | Spiel, Web | Spiel-Gold; 12,37 : 1 auf Grund, 10,06 : 1 auf Fläche. |
| `#FFFF99` | Hervorhebung (Zahlen) | Spiel, Web | Spiel-Text; 17,77 : 1 – für kurze Werte gut, für lange Absätze zu grell. |
| `#F2E3BF` | Fließtext (neu, nur Web) | Web | „Pergament“: 14,66 : 1 auf Grund, ruhiger als `#FFFF99` bei Absätzen; vorgeschlagen auch für Langtexte im Spiel (Berater, Chronik). |
| `#C0C0C0` | Nebentext, Bildnachweise | Spiel, Web | steht im Spiel schon am Passworttor (Z. 8409); 10,24 : 1. |
| `#3e2723` / `#5D4037` | Zweitknopf / darüber | Spiel, Web | Spiel-Knöpfe; Gold darauf 9,17 bzw. 6,18 : 1. |
| `#FF6600` | Unterzeile, Akzent | Spiel, Web | Spiel-Subhead; 6,35 : 1 auf Grund – nicht auf `#5D4037` verwenden (3,17 : 1). |
| `#e53935` | Rot: nur Linien, Marker, Kampfsymbol | Spiel, Web | 4,41 : 1 auf Grund – als Schrift knapp zu schwach. |
| `#ef6b5b` | Warnschrift (neu) | Web, für das Spiel vorgeschlagen | aufgehelltes Spielrot: 6,15 : 1 auf Grund, 5,00 : 1 auf Fläche. |
| Titelschrift | `"Blackletter","UnifrakturMaguntia","Old English Text MT","Goudy Text MT","Fraktur",Georgia,serif` | Spiel (Blackletter), Web | nur lokal installierte Schriften: keine Webfont, keine fremden Server; wo keine Buchschrift installiert ist, steht Georgia – der Eigenstil trägt dann das Logo, nicht die Schrift. |
| Textschrift | `Georgia,"Palatino Linotype","Book Antiqua",serif` | Web | auf Windows, macOS, iOS vorhanden; Android fällt auf seine Serifenschrift zurück. |
| Abstände | Raster 8 px; Seitenrand 16 px; Abschnitt 44 px oben | Web | ein Grundmaß; 16 px Rand ist das kleinste, bei dem 360-px-Telefone nicht am Rand kleben. |
| Ecken | 4 px | Web, Spiel-Knöpfe | fast eckig wie die Tk-Oberfläche; rund wirkt nach App, nicht nach Burg. |
| Knöpfe | Höhe ≥ 48 px | Web | Fingerziel auf dem Telefon. |
| Bildformat | WebP, PNG als Ersatz; kein AVIF nötig | Web | WebP läuft in allen aktuellen Browsern und auf GitHub; AVIF spart wenig mehr. |
| Zielgewichte | Logo ≤ 320 KB (ist 316.542 Byte); Screenshot ≤ 250 KB; erster Seitenaufruf ≤ 600 KB | Web | Entwurf D: 15.801 Byte HTML + 316.542 Logo; Portrait (194.338) erst beim Scrollen. |
| Logo | immer unverändert, mit Zeile „Logo: Chris Fred Däubner“ | überall | Urheberrecht; kein Zuschnitt, keine Färbung, kein Hintergrund im Bild. |

**Bildsprache in drei Sätzen:** Gezeigt wird nur Gemaltes und Echtes – Chris’ Logo und Bildwelt und
unbearbeitete Aufnahmen aus dem Spiel, nie Stockfotos oder neu erzeugte Bilder. Der Nebel kommt im Web
aus Farbe und Verlauf, nicht aus zusätzlichen Bildern. Jedes Bild zeigt einen Ort oder einen Zustand des
Spiels, keine Stimmung ohne Inhalt.

**Anforderung an einen Illustrator (falls gewünscht, nicht Teil des Entwurfs):** ein Kopfband 1600 × 400 px,
Nebelmeer mit zwei Weltbruchstücken und einem Portal, Palette `#2a0605` / `#FFCC33` / Nebelweiß,
links ruhig für Text, als WebP ≤ 200 KB – von Chris oder mit seiner Zustimmung.

## Teil F – Was ich nicht geprüft habe

| Punkt (Auftrag Abschnitt 8) | Stand |
|---|---|
| 1 Startseite live | **teilweise.** Live UNBEKANNT (Pages nicht erreichbar). Repo-Fassung gelesen; die im Auftrag beschriebene Live-Fassung im Tag `v_0.0.3` gefunden (Befund 1). |
| 2 README auf GitHub gerendert | **UNBEKANNT** (github.com nicht erreichbar). Lokal: Anker `#bekannte-grenzen` passt zur Überschrift Z. 112; alle 7 relativen Ziele existieren. |
| 3 Links mit HTTP-Status | **teilweise.** Alle Repo-internen Ziele aus README und index.html existieren im Baum; Tag `v_0.0.3` existiert (`git ls-remote`). HTTP-Status von Releases, Issues, Instagram: UNBEKANNT. |
| 4 Release-Seite | **UNBEKANNT** (API und Seite nicht erreichbar). Zusätzlich gefunden: ein Tag `vor-nullzustand-20261105` ohne bekannte Release-Zuordnung. |
| 5 Bildgewicht | **gemessen** (Befund 9, Teil E). |
| 6 Kontraste | **gerechnet** für alte und neue Palette (alte Web-Palette: alle Paare ≥ 5,5 : 1). |
| 7 Mobil 360 px | **Startseite gerendert** (Chrome, headless, alt und Entwurf). README bei 360 px: UNBEKANNT. |
| 8 Typografie | **geprüft** (Befund 14). |
| 9 GitHub-Metadaten | **UNBEKANNT**: Beschreibung, Topics, Lizenz, Homepage, Social Preview nicht abrufbar – V3, V4, V10 weder bestätigt noch widerlegt. Ersatz im Entwurf D: `og:`-Tags für die Startseite. |
| 10 Namen und Wege | **geprüft** (Befunde 2, 3, Nebenbefund Workflow). Speicherordner tatsächlich `%LOCALAPPDATA%\Nebelseetal_Remake\Demo` (`src/public_start.py` Z. 16–18), README nennt ihn ohne `\Demo`. |
| 11 Erster Eindruck | **gemacht.** Offene Fragen nach 30 Sekunden: Wie sieht das Spiel aus? Wie groß ist der Download und was genau lade ich? Wie lange spielt man eine Partie? |
| 12 Wiedererkennung | **Heute: kaum.** Die Startseite ist eine dunkle Serifen-Textseite mit Goldtitel; ohne das Logo könnte sie zu jedem Fantasy-Projekt gehören – Rotbraun, Buchschrift und gemalte Bilder des Spiels fehlen. |

Ebenfalls nicht geprüft: ob die Spielaufnahmen in `docs/design/` und die Bilder in
`assets/referenzbilder/` von Chris stammen – deshalb nutzt Entwurf D außer dem Logo nur Daniels Portrait.

**Die drei stärksten Ideen**

1. Spielpalette ins Web: Rotbraun und Spiel-Gold machen Startseite, Logo und Spielfenster zu einem Ort statt drei Stilen.
2. Ein einziger echter Screenshot aus V_0.0.3 (1600 × 900, WebP ≤ 250 KB) beantwortet die wichtigste offene Besucherfrage.
3. Version und Dateinamen nur noch aus `data/version.json`: ein kleiner Test, der README, `index.html` und `release_vorlage/` gegen diese Datei prüft, verhindert Befunde 2 und 3 beim nächsten Release.

**Die eine Sache zuerst:** In den Repo-Einstellungen unter Pages Quelle und letzten Build-Lauf ansehen und
die Startseite neu ausrollen – jeder Besucher sieht heute die Seite vom 06.11. vormittags.
