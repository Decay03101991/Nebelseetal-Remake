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


---

# Nachtrag 31.10.2026, 20:25 - nach dem Einbau des Nahrungsverbrauchs (Register 69)

> **BEANTWORTET 31.10.2026, 20:40 (Daniel, Auswahlformular).** Antworten:
> **7 = C, aber verschaerft:** bei Nahrungsnot im Ort wird dort **nichts mehr produziert**
> (keine Truppen, keine Ware, kein Bau) und es koennen **keine Kosten mehr bezahlt** werden, bis die
> Nahrung wieder ausgeglichen ist - die Armee wird dort versorgt, wo sie stationiert/eingelagert ist;
> entweder Nahrung dorthin liefern oder die eigene Dorfproduktion ueber den Verbrauch bringen, damit
> im Dorf wieder Nahrung gelagert wird. **Kein Verlust von Einheiten.**
> **8 = A** (nur Einheiten essen, Siedler nicht). **9 = A** (Marsch kostet nur die Reisekosten, kein
> doppelter Abzug). Gebaut ist davon bisher NUR der Verbrauch (Register 69) - die Sperre bei
> Nahrungsnot und die sichtbare Warnung stehen als naechster Schritt in Register 70.

Der Verbrauch ist gebaut und laeuft (8 Nahrung je Einheit und Spieltag, `data/nahrungsverbrauch.json`).
Drei Fragen sind dabei OFFEN geblieben - bis zur Antwort gilt der jetzige Stand.

## 7. Was passiert, wenn die Nahrung nicht reicht (Unterdeckung)?

| | |
|---|---|
| **Messlage** | Der Bestand faellt heute auf 0, der Rest steht als `unterdeckung` im `produktionsjournal` - sonst passiert NICHTS. Keine Quelle nennt eine Strafe (Handbuch 2009 und Fassung 2006 kennen Nahrung nur als Preis) |
| **A - keine Strafe (heute)** | Der Spieler merkt es nur an der Kopfzeile (Rate wird negativ und orange hinterlegt) und im Lager. Folge: die Regel ist eine reine Wirtschaftsbremse, kein Risiko |
| **B - Einheiten hungern** | Bei Unterdeckung verliert die Garnison Einheiten (Vorschlag: 1 von 10 je Spieltag ohne Deckung, erst Karren, dann Kaempfer). Folge: Armee wird ein echter Posten - aber eine erfundene Strafe |
| **C - nur Warnung** | Eine deutliche Meldung in der Kopfzeile und in der Siedlungsansicht, kein Verlust. Folge: ehrlich, aber ohne Druck |
| **Empfehlung** | **C zuerst** (Warnung sichtbar machen), **B** nur wenn sich zeigt, dass Nahrung sonst bedeutungslos ist |
| **Frage** | A (so lassen), B (Einheiten hungern) oder C (nur Warnung)? |

## 8. Essen die Siedler (Bevoelkerung) auch?

| | |
|---|---|
| **Messlage** | Heute isst nur das ORTSHEER. Die Siedler (Bevoelkerung, 10 + 5 je Haus, bis 360 im Reich) kosten nichts. Im Original ist das genauso (keine Unterhaltsregel, Register 17 / Frage 6) |
| **A - nur Einheiten (heute)** | Einfach und erklaerbar. Folge: eine Siedlung ohne Armee hat keinen Nahrungsbedarf |
| **B - auch Siedler** | Z. B. 1 Nahrung je Siedler und Tag (VORSCHLAG). Folge: 360 Siedler = 360/Tag, jede Siedlung braucht dauerhaft eine Farm; die Regel wird greifbar auch ohne Armee |
| **Empfehlung** | **A** - Daniels Entscheidung 7 nennt ausdruecklich Einheiten, nicht Siedler |
| **Frage** | A (nur Einheiten) oder B (auch Siedler)? |

## 9. Ziehen Einheiten auf einem Auftrag zusaetzlich Nahrung?

| | |
|---|---|
| **Messlage** | Nein. Ein Auftrag zahlt heute seine Reisekosten (`auftraege.kosten_der_mission`, `NAHRUNG_JE_FELD_DURCH_GS` = 0,1 je Einheit und Feld), waehrend der Marsch isst die Truppe NICHT zusaetzlich (kein doppelter Abzug) |
| **A - so lassen (heute)** | Eine Quelle, keine Doppelbelastung. Folge: ein langer Feldzug ist nicht teurer als heute |
| **B - Marsch kostet den Tagessatz** | Zusaetzlich 8 je Einheit und Spieltag waehrend des Marsches. Folge: lange Wege werden spuerbar teuer, das Beuteverhaeltnis verschiebt sich |
| **Empfehlung** | **A** - die Reisekosten gibt es schon; zwei Nahrungsposten fuer denselben Marsch waeren eine zweite Wahrheit |
| **Frage** | A (so lassen) oder B (Marsch kostet zusaetzlich)? |


---

# Nachtrag 31.10.2026, 21:00 - Karten, Doerfer und Pech (Balancing-Test Teil 2)

## 10. Karten: freie Wahl (heute) oder Zufall wie im Original?

| | |
|---|---|
| **Messlage** | `tools/balancing_karten.py`: `originalkarten.vorrat()` gibt **alle 126** Karten frei, die Gruendungsmaske laesst die **freie Wahl**, `ziehchancen()` sagt selbst "nur_optionale_zufallsziehung_nicht_freie_auswahl". Das Original vergibt Karten **per Zufall** (Handbuch 2009, Z. 313). Gemessene Folge: freie Wahl = immer die beste Karte (Holz 12.730/Tag, Gold 1.534/Tag an 6 Siedlungen); Zufall = Median 24.964/Tag Ertrag gesamt, Gold 1.318/Tag, 5 % schlechteste nur 886 Gold/Tag. Pech entsteht heute ALSO GAR NICHT |
| **A - freie Wahl (heute)** | Der Spieler nimmt immer die beste Karte. Folge: kein Pech, kein Aergernis - aber auch keine Entscheidung, und die 49 "schlechten" Karten sind reine Deko |
| **B - Zufallsziehung wie im Original** | Jede Gruendung zieht eine freie Karte (gleichverteilt, reproduzierbar ueber den Seed). Folge: Pech ist moeglich (Gold -30 %), Daniel muss entscheiden, ob es dafuer einen Ausgleich gibt (z. B. Neu-Ziehen gegen Gebuehr) |
| **C - Wahl aus DREI gezogenen Karten** | Der Zufall entscheidet das Angebot, der Spieler waehlt daraus. Folge: Pech bleibt spuerbar, ist aber nicht ausweglos - Mittelweg zwischen Original und Bedienbarkeit |
| **Empfehlung** | **C** - Zufall ist belegt, reine Zufallsvergabe ohne Wahl waere im Remake bitter; C haelt beides |
| **Frage** | A, B oder C? |
