# Konformitäts-Audit — astra, 04.10.2026

**Einsatz 2 des Plans `docs/PLAN_ASTRA_EINSATZ.md`.** Modell `gpt-6-astra`, zwei Umläufe
(Seiten 1–22 und Nachtrag Seiten 23–24), astra hat die Quellen selbst gelesen, danach keine
Werkzeuge. Kosten: **0,78 USD**. Rohantworten unverändert in `docs/audits/`.

**Auftrag:** Handbuch Seite 1–24 der Reihe nach gegen eine ehrliche Selbstdarstellung des Codes
prüfen → Zustand je Regel: vorhanden / teilweise / fehlt / abweichend.

**Meine Nachprüfung:** astra urteilte allein aufgrund meiner Selbstauskunft (das sagt es selbst
im Bericht). Ich habe die tragenden Befunde am Code gegengeprüft — besonders die, die meine eigene
Darstellung korrigieren.

---

## Die fünf größten Lücken (astra, nach Wirkung auf die Spielbarkeit)

1. **Kein ausführbares Auftragssystem.** Ohne echte Ziele, Reisen und Rückkehr sind Transport,
   Stationieren, Handel, Spionage und Angriff unbenutzbar.
2. **Keine originalgetreue Wirtschafts- und Warenkette.** Fehlendes Gelände, abweichende Gebäude
   und Ersatz-Handelsgüter verhindern den Aufbau bis zur Ausrüstung der Armee.
3. **Kampfmodul nicht angebunden.** Krieg, Verteidigung und Plünderung sind über die Oberfläche
   nicht spielbar — obwohl das Modul geprüft ist.
4. **Fortschritt ohne Zeit und Voraussetzung.** Sofortige Forschung und Ausbildung ohne die
   nötigen Gebäude umgehen die zentralen Aufbauentscheidungen.
5. **Keine handelnden Gegner.** Bots bauen nicht aus, forschen nicht, greifen nicht an — dem
   Einzelspieler fehlt der Gegenspieler.

**Meine Bewertung:** Die Reihenfolge halte ich für richtig — mit einer Verschiebung. Punkt 2 muss
**vor** Punkt 1 laufen: Ein Auftragssystem ohne echte Waren und Erträge transportiert nichts
Sinnvolles. Ich ordne deshalb: **Wirtschaft (2) → Waren (2b) → Aufträge + Kampf (1+3) → Bots (5)
→ Punkte/Schutz (4)**.

## Befunde, die meinen Code betreffen — gegengeprüft

| Handbuch | astra-Befund | mein Befund am Code |
|---|---|---|
| S. 3 | höchstens **6** Siedlungen | bestätigt: `if len(...) >= 3` in `_found_settlement` |
| S. 4 | Forschungspunkte = Σ Stufe³ | bestätigt: Code addiert pauschal `score += 10` je Forschung |
| S. 11 | **1 Siedler je Stunde** | bestätigt: `population + dt_min * 0.5` = **30 je Stunde** |
| S. 12 | Forschungs**dauer** Stufe² Stunden, Stufe steigt erst nach Ablauf | bestätigt: `_start_research` erhöht die Stufe **sofort** |
| S. 12 | Forschung braucht **Bibliothek**, blockiert den Bereich | bestätigt: keine Prüfung im Code |
| S. 15 | Ausbildungsgebäude (Stellmacher, Diebesgilde, Kriegerakademie) | bestätigt: alle 28 Einheiten in einer Kaserne |
| S. 10/11 | Ertrag **je Geländeart**, Sümpfe unbebaubar | bestätigt: feste `prod_map`, keine Siedlung hat ein Gelände |
| S. 14 | 17 Original**waren** aus Schmiede/Bogenbauer/Nähstube | bestätigt: erfundene Handelsgüter (Brot, Bier, Glas …) |
| S. 3/5 | Limbus, 20 Dimensionen, Manakosten je Entfernung | bestätigt: fehlt vollständig |

## astra hat einen Fehler in MEINER Darstellung gefunden

Ich hatte in der Selbstdarstellung „**zehn** Tage Götterschutz" geschrieben. Handbuch Seite 5/6
sagt **sieben Tage**, endend mit dem ersten Kriegspunkt. astra hat den Widerspruch bemerkt und
benannt — die Vorlage ist korrigiert. Gut, dass die Quelle mitgeliefert wurde.

## Was astra ausdrücklich offen ließ (ehrlich)

- Es urteilte über **meine Beschreibung** des Codes, nicht über den Code selbst — alle „teilweise"
  bei den Kampfregeln spiegeln das.
- Zu mehreren Stellen sagt es „Handbuch schweigt": Preise für Gebäude, Ausbildungsdauern,
  konkrete Forschungsgrundkosten (50 Holz sind ein **Beispiel**), Behandlung von genau 300 Punkten.
  Diese Punkte bleiben Entscheidungen für Daniel, nicht für ein Modell.
- SI und HE ohne Wirkung: astra weist ausdrücklich darauf hin, dass das **keine** Lücke ist —
  das Handbuch gibt diesen Werten in der ausgelieferten Fassung keine Wirkung.

## Abgeleitete Paketreihenfolge (neu geordnet)

| neu | Paket | Inhalt |
|---|---|---|
| 1 | **W4b Wirtschaft** | Gelände je Siedlung, Erträge je Geländeart, 20 Originalgebäude, Sümpfe unbebaubar, 6 Siedlungen, Siedler 1/h |
| 2 | **W3 Waren** | 17 Originalwaren, Schmiede/Bogenbauer/Nähstube, Warteschlangen, Waren als Einheitenvoraussetzung |
| 3 | **W4c Forschung** | Dauer Stufe² Stunden, Stufe erst nach Ablauf, Bibliotheksvoraussetzung, Bereich blockiert, Abbruch |
| 4 | **W2b + WA Aufträge** | Kampf ins Spiel; dazu Stationieren, Transportieren, Handeln, Angriff mit Reisezeit und Rückkehr |
| 5 | **W5 Bots** | Bots bauen, forschen, handeln, greifen an |
| 6 | **W6 Punkte** | Forschungspunkte Σ Stufe³, Kriegspunkte, Verteidigung³, Gesamt = halbe Summe, Ruf, Götterschutz 7 Tage, Rangliste, Siegbedingung |
| 7 | **W7/W8/W9** | Oberfläche, Speichern, Auslieferung |

## Kostenstand der Mission

| Einsatz | Kosten USD | verbleibend USD |
|---|---|---|
| 1 Kampf-Audit | 0,43 | 8,46 |
| 2 Konformitäts-Audit | 0,78 | 7,68 |
| **offen** | | **7,68** für Waren-/Auftrags-/Bot-Entwurf und astra-Code |
