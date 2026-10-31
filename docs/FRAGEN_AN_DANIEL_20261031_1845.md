# Fragen an Daniel — Stand 31.10.2026, 18:5x (Sitzung F-04 ff.)

**Warum diese Datei:** Jede Frage hier ändert Geld, Daten, Regeln, Spielgefühl oder Originaltreue — sie
wird **nicht** selbst entschieden. Bis zur Antwort gilt der dokumentierte Stand und steht im Register
als VORGABE/offen. Am Sitzungsende kommen alle Fragen in **ein** Auswahlformular.

Kurz antworten genügt („1 so lassen, 2 …“). Jede Frage nennt die Messlage, zwei Möglichkeiten mit
Folge und eine Empfehlung.

---

## 1. Sofortangriff: weiter ohne Reisezeit, oder ganz wie der Auftrag?

| | |
|---|---|
| **Messlage** | `_angriff_durchfuehren` nimmt seit F-01/F-09/F-10 **dieselbe** Quelle (Ortsheer), dieselben Verluste, dieselbe Beute und dieselbe Heimkehr wie der Auftrag (`kampf_am_ziel` ist der EINE Kampfweg) — aber er **spart die Reisezeit**: der Kampf beginnt sofort, es fallen keine A2-Reisekosten an |
| **Möglichkeit A (heute so)** | So lassen. Folge: der zweite Knopf bleibt eine bewusste Remake-Erleichterung; ein Angriff „aus dem Stand“ ist möglich, obwohl das Original Wege kennt |
| **Möglichkeit B** | Ganz wie der Auftrag reisen (Reisezeit + Kosten). Folge: der Sofortangriff-Knopf wird überflüssig und heißt dann „Angriff entsenden“ — eine Mechanik weniger, aber ein sichtbarer Unterschied zum bisherigen Spielgefühl |
| **Empfehlung** | **A** — solange kein Spieltest das Gegenteil zeigt; das Original belegt die Wegzeit für **Aufträge** (Handbuch S. 19), für einen Sofortangriff sagt es nichts. Damit bleibt die Erleichterung, aber sie ist als solche im Register vermerkt |
| **Antwort Daniel (31.10.2026, 19:0x)** | **B — ganz wie der Auftrag reisen.** Wird als eigener Schritt umgesetzt: Reisezeit und Kosten wie beim Auftrag, der Knopf heisst dann "Angriff entsenden" |

---

## 2. Beute-Deckel im Langzeitspiel

| | |
|---|---|
| **Messlage** | `docs/SPIELBALANCING_TEST.md` (gemessen 31.10.2026): Vorrat und Tragekapazität laufen auseinander. Spieltag 7: 168.158 Bestand, 60 Zweispänner tragen 15.000 — 14 Wellen für 98 %. Spieltag 30: 67 % bleiben nach 20 Wellen. Spieltag 90/180: praktisch nichts mehr zu holen. Ursache: **jeder Karren kostet Siedler**, Siedler sind bei 360 gedeckelt |
| **A — Quote bleibt** | Beute bleibt ein Anteil (10/30/60/100 %), gedeckelt durch Karren. Folge: Beute ist früh stark, spät bedeutungslos; „einmal alles stehlen“ gibt es nicht |
| **B — Kapazität wächst** | Forschung „Wagenbau“ erhöht die Ladung je Karren (z. B. +50 % je Stufe) oder die Siedlerkosten der Karren sinken. Folge: Beute bleibt im ganzen Spiel ein Ziel, die Karrenflotte wird aber zur Pflichtinvestition |
| **C — Beute ohne Karren** | Beute geht direkt ins Lager (ohne Transport). Folge: größter Eingriff, das Original belegt Karren für Beute (Handbuch S. 23) — würde eine Originalregel brechen |
| **Empfehlung** | **B, aber sparsam** — Ladung je Karren forschungsabhängig machen; die Staffel bleibt VORSCHLAG-Wert |
| **Antwort Daniel (31.10.2026)** | **B — Kapazitaet waechst mit Forschung "Wagenbau"; die belegten Einheitenwerte bleiben die BASIS (Minimum)** |

## 3. Gold als Engpass bei Armeen

| | |
|---|---|
| **Messlage** | Krieger kostet 500 Gold (belegt), Reich mit 6 Siedlungen erwirtschaftet 1.224 Gold je Spieltag → **100 Krieger = 41 Spieltage** des gesamten Golds. 360 Soldaten (Siedlerdeckel) wären 147 Spieltage |
| **A — so lassen** | Der Krieger bleibt teuer, Armeen bleiben klein (60–100), Kriege sind Wochenprojekte |
| **B — Einheitenpreis runter** | Goldpreis je Einheit senken (z. B. Krieger 250). Folge: mehr Truppen früher, Wandstufen werden eher erreichbar; Originalwert wird verlassen (dann als Remake-Abweichung im Register) |
| **C — Goldertrag rauf** | Goldmine bleibt bei 3/h (belegt), aber mehr Goldfelder je Karte (Bergfelder sind mit 9,4 je Karte knapp) — ginge nur über die Karte, nicht über die Regel |
| **Empfehlung** | **A vorerst** — der Engpass ist originalbelegt und macht Kriege zu einer Entscheidung; erst nach einem echten Spieltest ändern |
| **Frage** | A (so lassen), B (Preis runter) oder C? |

## 4. Wall 10 praktisch uneinnehmbar?

| | |
|---|---|
| **Messlage** | Wall 10 (Bollwerk) verlangt 1.000 Schlagkraft Fußtruppen = **333 Krieger** = 92 % des Soldaten-Deckels von 360; zusätzlich 1.000 Belagerungs-Schlagkraft. Wall 6 (Mauer) verlangt 120 Krieger = 33 % |
| **A — so lassen** | Eine voll ausgebaute Wand ist nur mit dem ganzen Reich und Belagerungswaffen zu brechen — das ist eine klare, lesbare Machtaussage |
| **B — Schwellen relativ** | Schwellen relativ zur möglichen Armeegröße deckeln (z. B. höchstens 60 % des Soldaten-Deckels). Folge: Originalzahlen (S. 21) werden verlassen |
| **Empfehlung** | **A** — die Schwellen sind belegt; wer 360 Siedler in Soldaten steckt, hat keine Wirtschaft mehr, das ist die eigentliche Bremse |
| **Frage** | A (belegte Schwellen) oder B (relativ gedeckelt)? |

---

## 5. Bots haben keine Wirtschaft — sollen sie eine bekommen?

| | |
|---|---|
| **Messlage** | `docs/audits/BEFUND_SIEDLER_UND_BOTS_20261031.md`: nach **30 Spieltagen** haben die Bots **1 bis 4 Einheiten** (Haug 1 Kurzbogenschütze, Brynhild 1 Streuner, Krank 4 Streuner), keinen Wall und keine Produktion — ihre Vorräte stammen einmalig aus `botkern.VORSCHLAG_START_VORRAETE` und wachsen nie. Der Spieler steht zur selben Zeit bei ~168.000 Rohstoffen |
| **A — volle Wirtschaft + Wall** | Bots bekommen eigene Siedlungen mit Erträgen aus `data/buildings.json`, Siedlerwachstum 1/h bis zur Grenze, Einheitenkauf zu den belegten Preisen (Siedler verbrauchend) und Wallausbau nach Punkten. Folge: die belegten Wallschwellen wirken endlich in BEIDE Richtungen, Kriege werden eine Entscheidung |
| **B — nur Wirtschaft, kein Wall** | Bots wachsen mit, bleiben aber wehrlos. Folge: Angriffe bleiben fast verlustfrei, das Kampfsystem wird weiter kaum gefordert |
| **C — so lassen** | Bots bleiben Kulisse. Folge: der Langzeittest bleibt sinnlos, weil niemand den Spieler fordert |
| **Empfehlung** | **A** — ohne wirtschaftende Gegner ist jede Balancing-Zahl gegenstandslos |
| **Frage** | A, B oder C? |

## 6. Rohstoffe haben keine Senke — Lagerschwund einbauen?

| | |
|---|---|
| **Messlage** | Der Vorrat wächst unbegrenzt: 168.000 (Tag 7) → 4,3 Mio (Tag 180). Das Original kennt **kein** Lagerlimit (Register 17) und **keine** Unterhaltsregel — `Nahrung` kommt im Handbuch nur als Preis vor (Z. 506/676/910/1148), nie als Verbrauch je Siedler. Deshalb ist „alles stehlen“ strukturell nur früh möglich (SPIELBALANCING_TEST Abschnitt 3.9) |
| **A — so lassen** | Keine Erfindung. Folge: Beute bleibt eine Quote; die Karren-Kapazität (mit Wagenbau-Forschung) ist der einzige Hebel |
| **B — Unterhalt erfinden** | Z. B. 1 Nahrung je Siedler und Stunde (VORSCHLAG, klar gekennzeichnet, abschaltbar). Folge: Vorräte bleiben klein, Beute wird wieder wertvoll — aber es ist eine **Remake-Regel ohne Quelle** |
| **C — Lagerlimit** | Obergrenze je Rohstoff und Siedlung (z. B. 10.000). Folge: ebenfalls Remake-Regel; macht Lagerausbau nötig, den es im Original nicht gibt |
| **Empfehlung** | **A zuerst**, dann im Spieltest prüfen; erst wenn Beute sich tot anfühlt, B als abschaltbare Regel |
| **Frage** | A (so lassen), B (Unterhalt) oder C (Lagerlimit)? |
