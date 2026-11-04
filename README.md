# Nebelseetal Remake — Pre-Release-Testversion

**Ein Einzelspieler-Remake des historischen Browserspiels Nebelseetal.** Läuft lokal, offline,
kostenlos. Windows-Testversion als `.exe`, kein Python nötig.

> **Dies ist die erste Vorabversion** (`0.5.0-pre.1`). Sie ist zum Ausprobieren und Fehlersammeln
> gedacht, nicht als fertiges Spiel. Was fehlt, steht ehrlich unter [Bekannte Grenzen](#bekannte-grenzen).

---

## Was das Spiel ist

Du übernimmst die Rolle eines Herrschers in einer zersprungenen Welt. Sechs Bruchstücke treiben im
magischen Raum Limbus, verbunden nur durch Portale. Du gründest Siedlungen, produzierst Rohstoffe,
stellst Waren her, forschst, rüstest aus, bildest Einheiten aus, kämpfst und reist in andere Welten.

Der Kreislauf: **gründen → produzieren → forschen → ausrüsten → ausbilden → bewegen → kämpfen → punkten.**

- bis zu **6 Siedlungen** je Reich, **10 Siedler** je Siedlung und **5 je Haus**
- **7 Geländearten**, **9 Rohstoffe**, **17 Waren**, **28 Einheiten**, **20 Gebäude**, **21 Forschungen**
- **fünf Nachbarn** mit eigener Wirtschaft: Haug raubt, Brynhild wacht, Grom baut, Silra späht,
  Krank vergisst nichts
- **kein Sieg, sondern Ruhm:** vier Auszeichnungen — Feldherr, Forscher, Händler, Gesamtherrscher
- vollständige Anleitung im Spiel über den Berater

Ausführlicher: [Die offizielle Erklärung](SPIEL_ERKLAERUNG.md) · [Die Chronik der Welt](CHRONIK_DER_WELT.md)
· [Sechs Häuser, sechs Welten](FRAKTIONEN_WELTEN.md) · [Die Geschichte als PDF](CHRONIK_DER_WELT.pdf) · [Erste Eindrücke einer späteren Version](VORSCHAU.md)

## Diese Version herunterladen und starten

1. Im Bereich **Releases** das Paket `Nebelseetal_Remake_0.5.0-pre.1.zip` herunterladen.
2. ZIP-Inhalt in einen **neuen leeren Ordner** entpacken (nicht in einen Windows-geschützten Ordner).
3. `Nebelseetal_Remake.exe` per Doppelklick starten.
4. Beim ersten Start ein **eigenes Passwort** festlegen und notieren — es bleibt lokal auf dem Rechner.
5. Spielen. Fehler bitte nach `FEHLER_MELDEN.txt` (liegt im ZIP) notieren.

Die Testversion startet **leer**: keine mitgelieferten Spielstände, kein fremdes Passwort, ein eigener
Speicherordner unter `%LOCALAPPDATA%\Nebelseetal_Remake\`. Voraussetzungen und Grenzen stehen in
`SYSTEMANFORDERUNGEN.txt` und `BEKANNTE_GRENZEN.txt` im ZIP.

**macOS:** es gibt **keine** `.app`. Eine echte Fassung müsste auf einem Mac gebaut *und geprüft*
werden — dieser Rechner ist ein Windows-Rechner, deshalb wird hier nichts angeboten, was niemand
getestet hat.

## Was in diesem Repository liegt

| Ordner / Datei | Inhalt |
|---|---|
| `src/` | der Spielcode, jeder Block und jede Funktion am Zeilenende erklärt |
| `data/` | alle Spieldaten als JSON — Einheiten, Waren, Gebäude, Forschungen, Welten, Texte |
| `assets/` | Bilder: Icons, Karten, Wappen, Burgen, Gebäudehintergründe |
| `release_vorlage/` | die Infodateien, die im Release-ZIP liegen |
| `START_SPIEL_WINDOWS.bat` | das Spiel aus dem Quellcode starten (braucht Python) |
| `SPIEL_ERKLAERUNG.md` | was das Spiel ist, offiziell |
| `BESUCHER.md` | wie dieses Spiel entstanden ist — für Besucher, grob |
| `FRAKTIONEN_WELTEN.md` | die sechs Häuser, ihre Wappen, die sechs Welten |
| `CHRONIK_DER_WELT.md` / `.pdf` | die Geschichte der Welt, als Buch gestaltet |
| `VORSCHAU.md` | erste Eindrücke einer späteren Version: Fraktionen, Gebäude, Burgen, Panoramen |

Nicht im Repository: Prüfdateien, Werkzeuge und die Entwicklungsdokumentation. Sie bleiben im
Arbeitsstand des Entwicklers — dieses Repository ist für Spieler gedacht, nicht als Werkstatt.

## Herkunft und Transparenz

Das Remake entsteht als **Arbeit von Daniel Kössl mit einem Hermes-Agent-System und dessen
Coding-Subagenten**. Die Agenten haben Code geschrieben, geprüft und dokumentiert; die Entscheidungen
über Inhalt, Ton, Regeln und Gestaltung liegen beim Entwickler.

**Der Agent hat einen Namen: „Weltenfresser“.** Er ist der Hermes-Agent von Daniel Kössl und läuft auf
dessen Rechner. Seine Rolle im Projekt, offen gesagt:

| Rolle | Was der Agent konkret tut |
|---|---|
| **Umsetzer** | schreibt den Spielcode und die Datendateien, Modul für Modul, jede Zeile erklärt |
| **Prüfer** | legt Prüfdateien an, rechnet Zahlen gegen die Originalquellen nach, fährt Prüfläufe über den ganzen Code und meldet, was rot ist — auch wenn es seine eigene Arbeit war |
| **Chronist** | führt Entwicklungsprotokoll, Prüfregister und Übergaben, damit keine Entscheidung verloren geht |
| **Koordinator** | zerlegt große Aufgaben in Schnitte, delegiert an Subagenten, führt deren Ergebnisse zusammen |
| **Autor mit Grenzen** | schreibt Dokumente und Entwürfe — aber die Geschichte der Welt und die Gestaltung des Buches kamen aus einem bewusst stärkeren Modell, auf Anweisung des Entwicklers |
| **Bremse** | hält an, wenn eine Entscheidung dem Entwickler gehört: was Regeln, Geld, Daten oder Spielgefühl betrifft, wird gefragt statt entschieden |

Wo der Agent irrt, steht der Irrtum im Protokoll — falsche Schnitte, fehlerhafte Messungen und
widerlegte Annahmen eingeschlossen. Das ist Absicht: ein Agent, der seine Fehler aufschreibt, ist
prüfbar; einer, der sie weglässt, nicht.

**Sicherheit und Kontrolle stehen an erster Stelle** — im ganzen System und damit auch im
Entwicklungssystem. Die Agenten arbeiten hierarchisch nach Regeln und Skills, und die Rechte sind
geteilt: es gibt Rollen, die nur lesen dürfen, und Rollen, die schreiben dürfen. Was eine Rolle nicht
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
`deepseek-v4-flash`. Keine Token-Zahlen, keine Prompts, keine Protokolle — nur diese grobe Zuordnung.

**Zum früheren Stand:** Ein früherer Stand dieses Projekts war bereits auf GitHub veröffentlicht. Der
Entwickler hat diesen Stand zurückgenommen und das Projekt neu bewertet. Dieses Repository ist der
daraus hervorgegangene, offizielle Pre-Release-Stand.

## Bekannte Grenzen

- **Vorabversion.** Kein fertiges Spiel, keine Kompatibilitätszusage.
- **Sechs Welten sind noch nicht fertig umgestellt.** Im Spielcode liegen derzeit 20 Limbus-Dimensionen,
  von denen sechs mit den belegten Welten belegt sind; 14 sind leer. Der Umbau auf sechs Welten läuft.
- **Drei Kampfregeln fehlen:** Fluchtformel, Beute-Reihenfolge (Gold zuerst), Mauerreparatur mit Bauzeit.
- **Kein Ton, keine Musik.** Die Oberfläche ist eine Windows-Oberfläche mit Ingame-Fenstern.
- **Nur auf Windows getestet** (Windows 11, 64 Bit). Windows 10, ARM und kleine Displays sind ungeprüft.
- **Admin-Werkzeuge sind in dieser Fassung gesperrt.** Sie gehören zur Entwicklerfassung, nicht zur
  Testversion.
- SmartScreen kann bei unbekanntem Herausgeber warnen. Die Prüfsumme steht in `SHA256SUMS.txt` im ZIP.

## Rechte

Der Quelltext ist einsehbar. Eine Nutzungslizenz ist für diese Vorabversion **noch nicht festgelegt** —
wer den Code verwenden will, fragt bitte vorher. Die Bilder des historischen Originalspiels sind nicht
Teil dieses Projekts; die im Spiel verwendeten Bilder stammen aus eigenen Lieferungen und eigenen
Generierungen.

## Fehler melden

Bitte mit Beschreibung, was du getan hast, was du erwartet hast und was passiert ist — ohne Passwörter
und ohne private Spielstände. Das Formular liegt als `FEHLER_MELDEN.txt` im Release-ZIP.
