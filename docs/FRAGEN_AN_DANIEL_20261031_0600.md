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
