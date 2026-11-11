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
