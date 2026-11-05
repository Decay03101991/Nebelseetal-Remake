# Arbeitsplan ab 05.11.2026 — Stueck fuer Stueck, nichts mehr ziellos

Grundlage: `docs/GESAMTBILD_SPIEL_20261105.md` (Mechanik- und Bot-Landkarte, gemessen) und
`docs/ENTWICKLUNGSABLAUF_AB_20261105.md` (sieben Phasen je Schnitt, Rangfolge der Quellen).

**Regel fuer jedes Stueck:** Ziel + Messzahl, Eingriff mit Datei und alt -> neu, Nebenwirkungen,
Aufbauzeit-Effekt, Quellenlage, Rueckrollweg — **vor** dem Bauen. Ein Stueck ist fertig, wenn
Einzelwachen gruen sind, der Sammellauf 0 rot hat (nach `src/`-Aenderungen), Register, Protokoll und
Stand-Block stehen und - bei sichtbarer Aenderung - eine Version angekuendigt ist.

## Stufe A — Fundament und Sichtbarkeit (zuerst, weil alles andere darauf misst)

| Stueck | Ziel | Messzahl / Fertig-Kriterium | Abhaengig von | Aufwand | Modellpaket |
|---|---|---|---|---|---|
| **A1** Voraussetzungen sichtbar (B3/B4/B7) | der Spieler sieht am Knopf, was fehlt (Waffentechnik 3, Schmiede, Ware) | Fehlversuche in einem Spieltest-Lauf sinken von 283+156+82 auf < 50; `test_anzeigetexte_umlaute` gruen | - | M | ja (fertige Patches fuer `src/main.py:11653`, `:14213`) |
| **A2** Messpflicht-Tabelle im Werkzeug | jede Balancing-Aenderung messbar machen | `tools/spieltest_simulation.py` gibt "Spieltage bis Gebaeude n / Forschung n / erste Einheit / erster Weltwechsel / voll ausgebaut" aus | - | S | nein (Sitzung baut selbst) |
| **A3** Kampf gegen ein echtes Bot-Dorf | Kampf, Wall und Verluste werden beurteilbar | ein Lauf enthaelt ein Gefecht gegen einen Bot mit variabler Beute/Verlusten (nicht immer 16/10/12) | A2 | M | ja |

## Stufe B — Bots voll handlungsfaehig (das groesste offene Feld)

| Stueck | Ziel | Messzahl / Fertig-Kriterium | Abhaengig von | Aufwand | Modellpaket |
|---|---|---|---|---|---|
| **B1** Bot-Kern aus `main.py` loesen | Bot ohne Oberflaeche messbar und balancierbar machen | 69 `bot_*`-Funktionen wandern in `src/bot_spieler.py` (nur Umzug, keine Regel), alle 29 Bot-Wachen unveraendert gruen | - | L | ja (Umbau-Schnitt mit Wache) |
| **B2** Zielbild Bots entscheiden | Profile, Reaktion auf den Spieler, Schwierigkeit | eine Entscheidungsliste mit Daniels Antworten (Profile, Skalierung, kein Betrug) | A2 | S | nein |
| **B3** Bots reagieren auf den Spieler | Bot ruestet nach, wenn der Spieler davonzieht; greift an, wenn er sich stark fuehlt | im Lauf mindestens ein Angriff eines Bots auf eine Spielersiedlung | B1, B2 | M | ja |
| **B4** Drachen-Regel fuer Bots | Bots greifen den Drachen an oder meiden ihn bewusst | Wache: Bot mit Armee > Schwelle plant Drachenangriff; ohne Armee meidet er das Feld | B1 | M | ja |
| **B5** Handel und aktive Spionage der Bots | Bots handeln und spionieren | je eine Wache mit belegtem Zug (Ware gegen Rohstoff, Spionageauftrag ausgeloest) | B1, B2 | M | ja |

## Stufe C — Balancing als eigene Runde (mit Messpflicht, Leitlinie Aufbauspiel)

| Stueck | Ziel | Messzahl / Fertig-Kriterium | Abhaengig von | Aufwand | Modellpaket |
|---|---|---|---|---|---|
| **C1** Mana-Kette oeffnen | Weltwechsel erreichbar machen, ohne den Aufbau zu verkuerzen | Bedarf je Partie gerechnet; Tempel-Ertrag und Wechselpreis so gesetzt, dass ein Wechsel in X Spieltagen erreichbar ist (X von Daniel); Wache | A2 | M | ja |
| **C2** Forschungsdauern und -kosten senken | Kämpfer nicht erst an Spieltag 8 | erster Kämpfer <= Spieltag 5 bei gleicher Aufbauzeit bis "voll ausgebaut" (Differenz <= 0) | A2 | M | ja |
| **C3** Aufbauzeit-Zielbild | "voll ausgebaut" braucht viele Spieltage, aber keine Leerlaeufe | Tabelle vorher/nachher; kein Tag ohne sinnvolle Entscheidung | C1, C2 | M | nein (Entscheidung + Messung) |
| **C4** Handelspunkte messbar | Auszeichnung "Haendler" existiert im Verlauf | ein Lauf mit Handelspunkten > 0 | B5 | S | ja |

## Stufe D — Auslieferung und Abgleich (laufend)

| Stueck | Ziel | Fertig-Kriterium |
|---|---|---|
| **D1** Version je sichtbarer Aenderung | Spiel bleibt beim Spieler aktuell | EXE gebaut, am Bildschirm geprueft, Release angekuendigt (Muster 0.0.2) |
| **D2** Abweichungs-Register pflegen | Ommage bleibt nachvollziehbar | jede Abweichung vom Original mit Quelle, alt, neu, Grund in `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` |
| **D3** Rueckblick je Woche | kein zielloses Arbeiten | eine Seite: was gebaut, was gemessen, was verschoben, naechste drei Stuecke |

## Reihenfolge (Beschluss fuer die naechste Sitzung)

1. **A1** (Voraussetzungen sichtbar) — laeuft die sieben Phasen einmal vollstaendig durch, als Muster.
2. **A2** (Messpflicht-Tabelle) — Voraussetzung fuer jede Balancing-Zahl.
3. **B1 + B2** (Bot-Kern loesen, Zielbild entscheiden) — ohne das bleibt jede Bot-Frage Bauchgefuehl.
4. **C1 + C2** (Mana, Forschungsdauern) — mit Aufbauzeit-Nachweis.
5. **A3, B3, B4, B5, C4** — in der Reihenfolge, in der die Messungen die groessten Luecken zeigen.

**Was NICHT mehr passiert:** Einzelwuensche ohne Gesamtbezug; Zahlen aendern ohne Messung; Bots
„verbessern“, ohne dass ein Lauf den Unterschied zeigt; Versionen ohne Ankuendigung.
