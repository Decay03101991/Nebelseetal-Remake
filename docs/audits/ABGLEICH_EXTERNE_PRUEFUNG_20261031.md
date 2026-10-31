# Abgleich der externen Gegenprüfung (GPT) mit dem Code — 31.10.2026

**Prüfgegenstand A:** `docs/audits/EXTERNE_GEGENPRUEFUNG_GPT_20261031.txt` (ChatGPT, Abo, 19.003 Byte,
185 Zeilen). GPT hat den **öffentlichen** Stand `main` = `954097a` (28.10.2026) gelesen — das ist
**nicht** der Arbeitsstand. Wir stehen auf `c8f2ccc` (31.10.2026).
**Prüfgegenstand B:** unser Code, jede Zeile hier selbst nachgesehen (grep/read, keine Erinnerung).
**Prüfgegenstand C:** die Befunde des DeepSeek-Pakets A1 (`docs/audits/BEFUND_A1_KAMPFMODELL_20261031.md`)
und A2 (`BEFUND_A2_WEGZEIT_20261031.md`).

**Methode:** Jeder der zwölf GPT-Befunde wurde im Code aufgesucht. Urteile:
**BESTÄTIGT** (Fehler war da) · **ÜBERHOLT** (im alten `main`, hier nicht mehr) · **ANDERS** (Mechanik
existiert, aber anders als beschrieben) · **OFFEN** (Entscheidung nötig, nicht selbst entscheidbar).

---

## 1. Die zwölf GPT-Befunde

| Nr | Befund (GPT) | Fundstelle im Code, selbst geprüft | Urteil | Stand nach dieser Sitzung |
|---|---|---|---|---|
| 1 | Sieg bei 300 Gesamtpunkten noch aktiv | `punkte.VORSCHLAG_ZIEL_PUNKTE = 300`, `punkte.sieg_oder_niederlage`, Anzeige `main.py` („Ziel: x / 300“) | **BESTÄTIGT** | **behoben** in `c8f2ccc`: `spielausgang()` liefert nur noch `niederlage`/`weiter`; Konstante heißt jetzt `ZIEL_PUNKTE_VERWORFEN`; Anzeige „Punkte: X · Götterschutz bis 299 · kein Sieg“. `tests/test_punkte.py` 78/0 |
| 2 | Wallprüfung summiert AT, Kampf prüft SK | **Nachgemessen:** `auftraege._schlagkraft_fussttruppen` rechnete `E.angriff(n)` = **AT** (Kämpfer AT 40), `kampf.fuehre_schlacht` prüft **SK** (Kämpfer SK 2) — genau der Befund | **BESTÄTIGT (war noch da!)** | **behoben 31.10.2026:** `_schlagkraft_fussttruppen` rechnet jetzt `E.schlagkraft`; `tests/test_auftraege.py` 129/0/1. Folge, ehrlich benannt: zwei Kämpfer (SK 4) bestehen Wallstufe 1 (Schwelle 10) nicht mehr — zwei alte Prüfungen mussten auf 5 bzw. 20 Kämpfer angehoben werden |
| 3 | Spionage fehlt als fünfte Auftragsart | `auftraege.AUFTRAGSARTEN` (Z. 49): nur stationieren/transportieren/handeln/angreifen; Handbuch S. 24 belegt Spionage | **BESTÄTIGT** | **OFFEN** — Frage 1 an Daniel |
| 4 | Reisekosten (Gold/Nahrung/Mana) fehlen | `eintrag["kosten"] = {}` mit Kommentar „keine belegten Reisekosten“ | **BESTÄTIGT** | **behoben** in `c8f2ccc`: `auftraege.kosten_der_mission` (Sätze aus A2, alle als VORSCHLAG markiert), Kosten werden bei `auftrag_starten` gebucht und in der Meldung genannt. `tests/test_auftraege.py` 125/0 |
| 5 | Mauerprüfung bei Auftragserteilung statt bei Ankunft | `auftraege.starten` rechnet die Vorrunde sofort und **lehnt den Auftrag ab**, wenn sie nicht besteht (Z. 279–290) | **BESTÄTIGT** | **OFFEN** — Frage 2 an Daniel (Bequemlichkeit gegen Originalablauf) |
| 6 | Plünderung: Gutschrift beim Spieler, keine Abbuchung beim Ziel | `main.kampf_am_ziel` schrieb `eintrag["beute"]` aus dem Kampf, ohne die Lager des Ziels zu belasten | **BESTÄTIGT** | **behoben** in `c8f2ccc`: `kampfbericht.beute_am_ziel` rechnet **und** bucht ab; alle drei Pfade (Auftrag, Bot, Direktangriff) benutzen sie. `tests/test_beute_am_ziel.py` 24/0 |
| 7 | Mana 5/1 (`resources.json`) und 8/2 (`buildings.json`) gleichzeitig | `data/resources.json` Z. 63 = 5/1 (Handbuch 2009); `data/buildings.json` Z. 73–76 = 8/2 (`WeitereWerteKampfsystem`, Abweichung dort vermerkt) | **BESTÄTIGT** | **OFFEN** — Frage 3 an Daniel (Quellenrangfolge) |
| 8 | Kämpfer 2–20 gegen 4–22 | `kampf.PROFILE`: Kämpfer `(15, 4, 22, …)`; Konflikt ist als Registerpunkt 40 dokumentiert | **ANDERS** | kein neuer Befund; A1 beanstandet die Spannen ebenfalls — dort fehlte der zweite Forumstext im Paket |
| 9 | Turmabschirmung „30 Prozentpunkte“ | `kampf.fuehre_schlacht` Z. 210–215: Türme **schützen 10 bzw. 30 Nahkämpfer** (Anzahl, kein Prozentabzug) | **ANDERS** | Mechanik ist eine Auslegung des Forumssatzes; **als VORSCHLAG zu kennzeichnen** (offener Doku-Punkt) |
| 10 | Mauermalus linear interpoliert = erfunden | `kampf.fuehre_schlacht` Z. 222: `abzug = 0.05 * stufe * (zustand/100)`; Forum nennt keine Formel | **BESTÄTIGT** | offener Doku-Punkt: Zahl ist VORSCHLAG, bisher nirgends als solcher geführt |
| 11 | Schützenrückzug 20 % aufgerundet | `kampf.fuehre_schlacht` Z. 256: `rueckzug_je_runde = math.ceil(ursprung_fern * 0.2)` | **BESTÄTIGT** | Rundung ist VORSCHLAG (Forum nennt keine Rundung) — Doku-Punkt |
| 12 | Beute: 50-%-Vorschlag im Auftragskern doppelt zur Kampfbeute | Auftragskern führt keine 50 % mehr; `kampfbericht.beute_staffel` ist die eine Formel; `botkern.BEUTE_ANTEIL = 0.5` gilt nur noch für **Bot-Überfälle auf den Spieler** (dokumentierter VORSCHLAG) | **ÜBERHOLT / ANDERS** | mit Nr. 6 und 12 erledigt; eine Formel im Spielerpfad |

**Zählung:** 9 bestätigt (1, 2, 3, 4, 5, 6, 7, 10, 11 → davon 5 sofort behoben, 4 offen),
1 überholt/anders (12), 2 anders (8, 9).

**Lehre aus diesem Abgleich:** ich hatte Nr. 2 zuerst als „überholt“ abgehakt, weil ich nur die
Funktion *überflogen* hatte — nachgemessen (`E.angriff` = AT 40 gegen `E.schlagkraft` = SK 2) war der
Fehler noch da. Ein Befund gilt erst als widerlegt, wenn die Zahl geprüft ist, nicht der Name.

---

## 2. Was A1 zusätzlich gefunden hat (und was es für E4 bedeutet)

A1 (DeepSeek, 0,037 USD) prüft die Beutestaffelung gegen das Original und kommt zu einem harten Satz:

> „Nach Material 1 (Abschnitt 2.4) gewinnt der Angreifer nur, wenn alle verteidigenden Einheiten tot
> oder geflohen sind, also sind immer keine Verteidiger mehr; der Mauerzustand ist im Original kein
> Faktor für die Beute. […] Die mit dem Original vereinbare Regel lautet: **100 % des Ortslagers,
> begrenzt durch die Karrenladung**.“

**Das stimmt für das Original — und es gilt für unseren Kampf nur halb.** Nachgemessen (Probe mit
`kampf.fuehre_schlacht`, Seed 11, drei echte Schlachten):

| Fall | Ausgang | gefallene Verteidiger | im Ort verblieben | Lage nach `beute_lage` | Beute |
|---|---|---|---|---|---|
| Paladin 30 gegen Bürgerwehr 3, Wall 0/100 % | Angreifer | 3 von 3 | 0 | `keine_verteidiger` → 100 % | 400 (= Ladung) |
| Ritter 20 gegen Bürgerwehr 10, Wall 1/100 % | Angreifer | 9 von 10 | 1 (kampfunfähig) | `mauer_heil` → 10 % | 240 |
| Kämpfer 40 gegen Bürgerwehr 20, Wall 2/50 % | Angreifer | 17 von 20 | 3 (kampfunfähig) | `mauer_beschaedigt` → 30 % | 400 (= Ladung) |

Weil im Remake nur die **Gefallenen** aus dem Ortsbestand gestrichen werden, bleiben kampfunfähige
Verteidiger im Ort stehen — genau der Fall, den A3-Vorschlag („überlebende kampfUNfähige Verteidiger
schließen einen Angreifersieg nicht aus“) beschreibt. **E4 ist damit wirksam**, nicht dekorativ: die
Stufen 10/30/60 % werden im Spiel erreicht, wenn Verteidiger überleben.

Der Widerspruch zum Original bleibt trotzdem bestehen (Original: Wallzustand ist kein Beutefaktor) —
er ist eine **bewusste Abweichung (E4)** und muss als solche gekennzeichnet bleiben, nicht als
Originalregel verkauft werden.

→ **Frage 4 an Daniel.**

---

## 3. Wo die drei Quellen übereinstimmen (belastbar)

| Gegenstand | GPT | A1 | A2 | Code |
|---|---|---|---|---|
| Rückweg doppelt so lang (S. 19) | ja | ja | ja | `HIN_UND_RUECK_FAKTOR = 2.0` |
| Reisezeit `2·d/GS` (Faktor 2) | empfiehlt T2 = `4d/GS` (Vorschlag) | — | **bestätigt Faktor 2** nach Rechnung (32 Felder/GS 5 → 512 s gesamt) | `SEKUNDEN_JE_FELD = 7200` |
| Drosselung in 10-%-Schritten; langsamer = weniger Gold, mehr Nahrung | ja | ja | ja, mit Zahlen | `DROSSELUNG_SCHRITTE_PROZENT = 10` |
| Beute nur mit Transportkarren, durch Ladung begrenzt | ja | ja (belegt) | — | `beute_staffel`, `beute_am_ziel` |
| Kein Sieg im Original (S. 3) | ja | ja | — | seit `c8f2ccc` umgesetzt |
| Punkteformel ΣStufe³ / (Krieg+Forschung)/2 | ja | ja | — | `punkte.forschungspunkte`/`kriegspunkte` |

**GPT liegt bei der Reisezeit daneben, nicht wir:** GPT schlägt `T2 = 4d/GS` vor, ohne den bereits
geltenden Faktor 2 zu kennen (der Prompt war bewusst blind). A2 hat den Faktor 2 **nachgerechnet** und
bestätigt (256 s pro Strecke bei 32 Feldern/GS 5). Zwei unabhängige Wege, ein Ergebnis → Faktor 2 bleibt.

---

## 4. Was jetzt noch offen ist (bewusst nicht selbst entschieden)

1. **Spionage als fünfte Auftragsart** (GPT 3, Handbuch S. 24 belegt, im Code fehlt sie).
2. **Mauerprüfung bei Ankunft statt bei Auftragserteilung** (GPT 5).
3. **Mana 5/1 gegen 8/2** — welche Fassung gilt (GPT 7; Handbuch 2009 gegen `WeitereWerteKampfsystem`).
4. **Beutestaffelung E4** — Hausregel behalten oder auf „100 % bei Sieg, ladungsbegrenzt“ zurück.
5. **Doku-Punkte ohne Entscheidung, nur Kennzeichnung:** Mauermalus 5 %/Stufe (GPT 10),
   Schützenrückzug mit `ceil` (GPT 11), Turmschutz als Anzahl statt Prozent (GPT 9).

---

*Geschrieben 31.10.2026 nach Selbstprüfung am Code; jede Fundstelle mit Zeile. Zahlen aus
`tests/`-Läufen dieser Sitzung: 8 berührte Prüfdateien, 608 Prüfungen, 0 Fehler.*
