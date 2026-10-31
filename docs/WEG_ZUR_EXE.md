# Weg zur fertigen .exe — Zieldefinition und Prüfmaßstab

**Ziel (Daniel, 04.10.2026):** Eine fertige, schlüssige, fehlerfrei spielbare `.exe`, die das
Spiel Nebelseetal als Einzelspieler-Remake stabil startet, überprüft und mit einem selbst
gesetzten Passwort geschützt.

---

## Was „fertig“ konkret heißt

Nach dem Konformitäts-Audit (`docs/AUDIT_KONFORMITAET_astra.md`) fehlen bis zu einer spielbaren
Partie neun Dinge. Sie sind die Schritte 1–9 dieses Wegs, in dieser Reihenfolge:

| # | Schritt | Ergebnis | Prüfung |
|---|---|---|---|
| 1 | **Wirtschaft** (W4b) | Gelände je Siedlung, Ertrag je Geländeart, 20 Originalgebäude, Sümpfe unbebaubar, 6 Siedlungen, Siedler 1/Stunde | `test_wirtschaft.py` + Spielstand-Rundlauf |
| 2 | **Waren** (W3) | 17 Originalwaren aus Schmiede, Bogenbauer, Nähstube; Warteschlangen; Waren als Einheitenvoraussetzung | Test: Ware fertigen, Einheit ausrüsten, Voraussetzung greift |
| 3 | **Forschung** (W4c) | Dauer Stufe² Stunden, Stufe steigt erst nach Ablauf, Bibliothek als Voraussetzung, Bereich blockiert, Abbruch mit Verlust | Test: Stufe steigt zeitgesteuert, nicht beim Klick |
| 4 | **Aufträge** (WA) | Stationieren, Transportieren, Handeln, Angriff; Reisezeit für eine Strecke, Rückkehr ebenso lang; Gold/Nahrung/Mana; 10-%-Drosselung | Test: Einheit reist und kehrt zurück, Angriff löst Kampf aus |
| 5 | **Kampf im Spiel** (W2b) | Angriff über die Oberfläche, Bericht in den Nachrichten, Beute in den Lagern | 42 Kampfprüfungen + Klickpfad-Test |
| 6 | **Bots** (W5) | Bots bauen, forschen, handeln und greifen an | Test: Bot-Werte verändern sich über die Zeit; Angriffe kommen an |
| 7 | **Punkte und Ende** (W6) | Forschungspunkte Σ Stufe³, Kriegspunkte, Gesamt = halbe Summe, Ruf, Götterschutz 7 Tage, Rangliste, **Sieg/Niederlage** | Test: Punkteformeln gegen Handbuchbeispiele |
| 8 | **Passworttor** (neu) | siehe unten | Test: falsches Passwort verweigert, richtiges startet |
| 9 | **Auslieferung** (W9) | PyInstaller-Einzeldatei mit Symbol, ohne Konsole, startet ohne installiertes Python | Start aus einem Pfad **mit Leerzeichen**, Rundlauf, genau **eine** EXE im Ordner |

## Das Passworttor — wie es gebaut wird

**Daniel setzt das Passwort selbst beim ersten Start.** Nicht im Chat, nicht durch mich.

- Beim ersten Start: Fenster „Passwort festlegen“ → er tippt es zweimal ein.
- Gespeichert wird **nicht das Passwort**, sondern ein **gesalzener Prüfwert** (PBKDF2-HMAC-SHA256,
  Zufallssalz, viele Runden) in `~/.nebelseetal/tor.json`.
- Jeder weitere Start verlangt das Passwort; nach drei Fehlversuchen kurze Wartezeit.
- Änderbar über das Tor-Fenster (altes Passwort nötig) und notfalls über den Spielordner
  (Datei löschen = neues Passwort setzen, der Spielstand bleibt).
- Ein Passwort kann als **vergessen** markiert werden? Nein — ohne Prüfwert kein Zugang; deshalb
  steht der Hinweis „Datei löschen setzt das Tor zurück“ direkt im Tor.

**Ehrliche Grenze:** Ein Tor in einer lokalen EXE hält **Gelegenheitsspieler** und Mitbewohner ab.
Wer die Dateien lesen kann, kann sie auch verändern. Mehr ist ohne Server nicht möglich — und
einen Server will dieses Spiel ausdrücklich nicht.

## Prüfmaßstab (das, was ich belegen kann)

Bei der Auslieferung nenne ich getrennt:
1. **Was geprüft ist** — Programmstart, Tor, alle Prüfläufe, Speichern/Laden über einen Neustart,
   Start aus einem Pfad mit Leerzeichen, Angriff→Kampf→Bericht→Beute.
2. **Was nicht geprüft ist** — alles, was ein Mensch sehen muss (Optik, Gefühl, Balance) und
   alles, was nur durch langes Spielen auffällt (Gleichgewichtsprobleme späterer Stunden).
   „Fehlerfrei“ behaupte ich nur so weit, wie die Prüfliste reicht — nicht als Gefühl.
3. **Der Prüflauf selbst** wird mit ausgeliefert (`run_tests.bat` bleibt im Ordner).

## Was NICHT hineinkommt

- Forum, IRC-Chat, Login, Newsletter, Account-Löschung (reine Netzfunktionen des Originals).
- Ein Server. Das Spiel bleibt offline, kostenlos, ohne Abo.
- Erfundene Daten: Wo das Handbuch schweigt, steht ein **gekennzeichneter Vorschlag**
  (Wirtschaftszahlen aus Einsatz 3) — und der wird Daniel zur Abnahme vorgelegt.

## Kostenrahmen

| Posten | Betrag |
|---|---|
| Guthaben OpenAI für diese Aufgabe | 8,89 USD |
| verbraucht (Einsatz 1 Kampf-Audit, Einsatz 2 Konformität) | 1,21 USD |
| laufend (Einsatz 3 Wirtschaft, später Bot-Kern) | ~1,3 USD geplant |
| **Reserve für Nachläufe** | **~6,4 USD** |

Alles andere (Umsetzung, Tests, Build) läuft auf dem Standardmodell und ist damit
vernachlässigbar billig.
