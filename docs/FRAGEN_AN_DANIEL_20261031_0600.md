# Fragen an Daniel — Stand 31.10.2026, 06:20 (nach den vier Paketen)

**Warum diese Datei:** Diese Fragen sind **nicht** selbst zu entscheiden — jede ändert Spielgefühl
oder Quellenrangfolge. Alles andere aus den vier Paketen ist bereits gebaut und geprüft (siehe
`docs/ENTWICKLUNGSPROTOKOLL.md`, Abschnitt HERMES-UMSETZUNG-02).

Jede Frage nennt die Quelle, die den Ausschlag gibt, und was ich empfehle. Antworten können kurz
sein („1 ja, 2 Ankunft, 3 Handbuch …").

---

## 1. Spionage als fünfte Auftragsart — bauen?

| | |
|---|---|
| **Beleg** | Handbuch 2009, Seite 24 (Z. 1319–1334): Spionage ist eine eigene Auftragsart mit Rückkehrbericht; im Code fehlt sie (`auftraege.AUFTRAGSARTEN` hat vier) |
| **Aufwand** | M (Auftragsart + Bericht + Prüfdatei) |
| **Empfehlung** | **Bauen, aber nach E3** — Spionage benutzt dasselbe Bewegungssystem, sonst entsteht ein dritter Pfad |
| **Frage** | Bauen (ja/nein) und wenn ja: mit oder ohne Spionageabwehr (SI/HE-Werte sind laut Handbuch „noch ohne Einfluss")? |

## 2. Wallprüfung beim Auftrag oder erst bei Ankunft?

| | |
|---|---|
| **Heute** | `auftraege.starten` rechnet die Wallvorrunde **sofort** und lehnt den Auftrag ab, wenn die Schlagkraft nicht reicht. Bequem, aber der Wall kann bis zur Ankunft repariert werden |
| **Original** | Die Prüfung gehört zum Kampf (Handbuch S. 21: „Bevor ein Kampf stattfindet …") — also bei Ankunft |
| **Empfehlung** | **Bei Ankunft prüfen**, beim Auftrag nur eine **Warnung** zeigen („Schlagkraft reicht heute nicht") |
| **Frage** | Umbauen (Warnung statt Ablehnung) oder so lassen? |

## 3. Mana: 5/1 oder 8/2 pro Stunde?

| | |
|---|---|
| **Heute** | Zwei Wahrheiten im Datenbestand: `data/resources.json` sagt **5/1** (Handbuch 2009), `data/buildings.json` sagt **8/2** (`WeitereWerteKampfsystem`, dort als Abweichung vermerkt) |
| **Empfehlung** | **5/1** (Handbuch 2009 ist die jüngere Gesamtfassung; die 8/2 stammen aus dem älteren Forumstext) — dann muss `buildings.json` die 8/2 als „alte Fassung" führen |
| **Frage** | 5/1 (Empfehlung) oder 8/2? |

## 4. Beutestaffelung (E4): Hausregel behalten?

| | |
|---|---|
| **Beleg** | Original kennt **nur** „100 % des Ortslagers, begrenzt durch die Karrenladung"; der Wallzustand ist dort **kein** Beutefaktor (A1, Handbuch S. 23) |
| **Heute** | Staffel 10/30/60/100 % ist gebaut, **wirksam** (gemessen: 1 von 10 Verteidigern überlebt → 10 % = 240 statt 400) und als bewusste Abweichung gekennzeichnet |
| **Empfehlung** | **Behalten**, weil es Daniels Entscheidung war und Angriffe taktisch macht — aber im Spieltest balancieren |
| **Frage** | Behalten oder auf Original (100 % bei Sieg) zurück? |

## 5. Was ist das Spiel — Sandbox oder Kampagne? (A4)

| | |
|---|---|
| **Zur Wahl** | (a) offenes Highscore-Spiel mit Bestwerten und Bot-Ruhmeshalle; (b) Kampagne mit festem Ziel (z. B. alle Ländereien vereinen) |
| **Warum es jetzt zählt** | Es entscheidet, ob als Nächstes Bestwerte/Bot-Rangliste gebaut werden oder ein Kampagnenbogen mit Missionszielen |
| **Empfehlung** | **(a) Sandbox** — die Quellen kennen kein Ende (Handbuch S. 3: jeder hat eigene Ziele), und die Auszeichnungen sind schon gebaut |
| **Frage** | (a), (b) oder beides (Sandbox mit optionalem Kampagnenbogen)? |

## 6. Zeitlimit für das Lauf-Ende? (A3)

| | |
|---|---|
| **Vorschlag A3** | 120 Echtminuten = 15 Spieltage bei ×180, danach Auszeichnungs-Bewertung, danach freiwillig weiterspielen |
| **Heute** | Kein Zeitlimit; nur Niederlage beendet etwas |
| **Empfehlung** | **Nicht fest einbauen**, sondern als Option im Startmenü („Lauf mit Zeitlimit 2 h") |
| **Frage** | Option einbauen (ja/nein)? |

## 7. Dimensionen: 20 mit 5–7 aktiven, oder 1 Dimension mit 6 Welten?

| | |
|---|---|
| **A2 empfiehlt** | 20 Dimensionen als Hintergrund, **5–7 aktiv**, Rest versiegelt; Portal = Tor zwischen Ländereien |
| **A3 empfiehlt** | **1 Dimension mit 6 Welten** (1 eigene + 5 Bots), passend zu maximal 6 Siedlungen |
| **Beide sind VORSCHLAG**, keiner widerspricht einer Quelle (das Original hatte 20 × 20 × 20 Felder für hunderte Spieler) |
| **Empfehlung** | **A2-Weise**: 20 als Kulisse, 6 aktiv — so bleibt die Originalstruktur sichtbar und der Einzelspieler hat keine Leere. Das ist auch der kleinste Umbau der Datendatei `data/welten.json` |
| **Frage** | A2-Weise (Empfehlung), A3-Weise (1 Dimension), oder anders? |

## 8. PR #1 auf GitHub zusammenführen (nur dein Klick)

Der PR ändert **nur** `README.md` und bringt den Hinweis auf `main`; die externen Pfade bleiben gültig.
https://github.com/Decay03101991/Nebelseetal-Remake/pull/1 — betrifft kein Spielverhalten.

---

## Was ich NICHT frage (weil entschieden oder belegt)

* Faktor 2 bei Reisezeiten — von A2 unabhängig nachgerechnet und bestätigt, bleibt.
* Kein Sieg — E5, gebaut.
* Bot-Punkte aus der Originalformel — belegt, gebaut.
* Reisekosten-Höhe — VORSCHLAG aus A2, im Spieltest zu balancieren (kein Entscheid nötig, nur Beobachtung).

---

## Neu am 31.10.2026, 12:15 — aus deinem Spieltest und aus E3

| # | Frage | Empfehlung |
|---|---|---|
| 12 | **Ausbildungsaufträge streichen:** Du hast nach einer Erstattung gefragt. Die Quellen regeln das **nicht** — belegt ist nur „Forschung abbrechen" (Handbuch Z. 442). Ich habe es so gebaut: Streichen möglich (nur wartende Aufträge), **keine Erstattung**. | So lassen (kein erfundener Betrag). Alternative: halbe Erstattung als klar gekennzeichneter VORSCHLAG |
| 13 | **Kampf auf der Weltkarte:** Ein Zug von Feld zu Feld ist jetzt ein reiner Marsch — der frühere 40-%-Münzwurf (1–4 Einheiten weg) ist entfernt. Soll ein Marsch auf eine Bot-Siedlung kämpfen können? | **Ja, aber über `kampf.fuehre_schlacht`** (dieselbe Funktion wie Auftrag/Direktangriff), nicht über einen Würfel. Aufwand M |
| 14 | **Rückweg auf der Karte:** Truppen sind nach der Ankunft sofort wieder verfügbar (alter FIX 5b). Im Auftrags-Pfad kostet der Rückweg die gleiche Zeit noch einmal. | **Rückweg auch auf der Karte berechnen** (ein Bewegungssystem, E3) — Aufwand S, ändert das Spielgefühl spürbar |
| 15 | **Anzeige der Aufträge auf der Karte:** Aufträge laufen, sind auf der Karte aber nicht zu sehen (nur `movements` werden gezeichnet). | Zusammenlegen, wenn 13/14 gebaut sind (E3-Rest) |

## Neu am 31.10.2026, 13:00 — aus dem fairen Modell-Lauf (`BEFUND_SPIELTEST_FAIR_20261031.md`)

Dieser Lauf bewertet einen KORREKTEN Spielverlauf (12 Gebaeude, Gold 1.419, Nahrung 2.056 nach
10 Spieltagen). Das Modell nennt jetzt Holz als Engstelle (Tag 6 auf 4) und empfiehlt:

| # | Vorschlag des Modells | Meine Einschaetzung |
|---|---|---|
| 16 | **Start-Holz 90 → 250** | **Nein.** Die Startwerte sind belegt (Handbuch S. 7: 100 Holz, 100 Stein). Besser: Holzproduktion/Preise im Spieltest ansehen — sonst wird eine Originalzahl erfunden |
| 17 | **Standardtempo x180 → x60** | **Deine Entscheidung.** ×180 war deine Vorgabe; das Modell argumentiert mit Bedenkzeit (1 Spieltag = 24 echte Minuten statt 8). Als **Option** im Startmenü denkbar |
| 18 | **Automatik: erste Einheit ausbilden, sobald Akademie und 100 Gold stehen** | **Nein als Automatik**, ja als **Hinweis** („Akademie steht — es fehlen noch Waren aus der Werkstatt"). Ein Spiel, das selbst Einheiten baut, nimmt dir die Entscheidung |
