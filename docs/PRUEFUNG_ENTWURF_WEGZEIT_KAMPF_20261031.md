# Prüfung des Entwurfs „Wegzeit, Kampfablauf, Weltlage“ gegen Handbuch 2009, Vorversion 2006 und den Code

**Gegenstand:** `docs/ENTWURF_WEGZEIT_KAMPF_WELT_20261031.md` (195 Zeilen, starkes Modell, 0,039 USD)
**Prüfer:** neue Sitzung (Hermes), 31.10.2026, 02:30 · Stand `06aabcb`, Arbeitsverzeichnis sauber
**Grundlage:** Spielanleitung 2009 (`docs/original/Spielanleitung_2009_Textfassung.txt`), Seiten 2006
(`docs/original/Spielanleitung_2005/`, u. a. `portal.php.txt`), `docs/original/ORIGINAL_Kampf_und_Punkte.md`,
`docs/PRUEFREGEL_ORIGINAL.md` (34 Punkte), Vorversion-Abweichungen, und **der Code selbst**
(`src/kampf.py`, `src/kampf_alt_handbuch_2009.py`, `src/kampfbericht.py`, `src/auftraege.py`, `src/punkte.py`,
`src/main.py`, `data/buildings.json`, `data/units.json`).

**Regel dieser Prüfung:** jede Zahl bekommt eine Quelle (Seite/Zeile) oder das Urteil VORSCHLAG.
Nichts wird angeglichen, ohne dass es hier steht.

---

## 1. Ergebnis in drei Sätzen

1. **Wegzeit und Weltlage sind brauchbar** — die Formel ist rechnerisch sauber (nachgerechnet, siehe §2)
   und alle Zahlen darin sind ehrlich als VORSCHLAG gekennzeichnet.
2. **Der Kampfteil muss neu geschrieben werden.** Er baut auf dem **älteren** Handbuch-Modell (LE/AT/PA/MU),
   das im Projekt am 28.10. durch das **neuere Original-Forumssystem** ersetzt wurde (`src/kampf.py`,
   15 Profile, Prüfprotokoll „GPT-KA01…KA06, 14 Testdateien grün“). Außerdem nennt der Entwurf sechs Dinge
   als „nicht belegt / Entscheidung Daniel“, die im Handbuch **wörtlich belegt** sind.
3. **Von den 11 Umsetzungsschritten sind 6 ganz oder teilweise gebaut** — Reisezeit, Auftragsliste,
   Wallvorrunde, Kampfsequenzen, Geräteverlust und Punkte existieren bereits mit Prüfdateien.
   Die Entscheidungsliste schrumpft von **10 auf 5**.

---

## 2. Wegzeit (§1) — Rechenprüfung

### 2.1 Was hält

| Behauptung des Entwurfs | Prüfung |
|---|---|
| GS = Reisegeschwindigkeit, höher = schneller | **BELEGT** HB Z. 1103–1104 |
| Zeitangabe gilt für **eine** Strecke, Rückkehr doppelt | **BELEGT** HB Z. 1136–1141 |
| Eine Zahlenformel nennt das Handbuch nicht | **BELEGT** (es nennt nur Beispielstunden) |
| 20 × 20 Felder je Dimension | **BELEGT** `portal.php.txt` Z. 21–22 |
| Spieluhr ×180 → 1 Spielstunde = 20 s Echtzeit | **stimmt**: 3600 s / 180; so rechnet `main.py` Z. 6930 |
| GS-Werte Bürgerwehr 5, Waldläufer 35, Siedlerkarren 20 | **stimmt** mit `data/units.json` |

Alle sechs Beispielzeilen der Tabelle §1.2 **nachgerechnet und richtig**: d 6 / GS 5 → 2,4 h → 48 s;
d 16 / GS 5 → 6,4 h → 2:08 min; d 32 / GS 35 → 1,83 h → 36,6 s. Auch „0,5 Felder je GS-Punkt und
Spielstunde“ folgt korrekt aus `2·d/GS`.

### 2.2 Was nicht hält — drei Punkte

| # | Aussage des Entwurfs | Befund |
|---|---|---|
| W1 | `Dauer = 2 · d / GS` | **VORSCHLAG, und im Widerspruch zum gebauten Code.** `src/auftraege.py` Z. 52/133–147 rechnet `Dauer = d / GS · 3600 s`, also **Faktor 1**: 6 Felder mit GS 5 = 1,2 h statt 2,4 h. Zwei Formeln für dieselbe Sache dürfen nicht beide im Projekt stehen → **Entscheidung E2** |
| W2 | „Jede Dimension zählt als 20 Felder“ | **VORSCHLAG.** Belegt ist nur das 20×20-Gitter und dass ein Dimensionswechsel **Mana** kostet (`portal.php.txt` Z. 11–14, 19–21) — **nicht**, dass er Zeit kostet. Die Zeitstrafe ist eine Remake-Erfindung und muss als solche im Code stehen |
| W3 | „Faktor 2 ist nötig, damit …“ | reine **Spielgefühls-Begründung**, keine Quelle. Zulässig als VORSCHLAG, aber genau so zu kennzeichnen |

**Fehlt im Entwurf:** die Auftragskosten. HB Z. 1185–1194: eigene Siedlungen kosten **Gold und Nahrung**,
fremde **zusätzlich Mana nach Entfernung**; die Geschwindigkeit ist in **10-%-Schritten drosselbar** —
**langsamer = weniger Gold, mehr Nahrung**, angezeigt als „Reisedauer“. Diese Regel ist im Code als
Konstante vorhanden (`auftraege.py` Z. 57–59), aber **nicht angeschlossen** (Z. 514) und die Reisekosten
sind leer (Z. 536).

---

## 3. Kampfablauf (§2) — der Teil, der neu geschrieben werden muss

### 3.1 Es gibt zwei Kampfsysteme im Projekt, und der Entwurf erwischt das falsche

| Modell | Datei | Status |
|---|---|---|
| **Handbuch 2009** (LE, AT, PA, MU, RS, TP; Zweikampf in Kampfrunden) | `src/kampf_alt_handbuch_2009.py` (18.772 Byte) | **Rückfallsicherung** — von `main.py` **nicht** importiert (nur `tests/test_gpt_kampf_forum_neu.py` prüft, dass sie existiert) |
| **Neueres Original-Forumssystem** (Konstitution %, Kampfwert-Spanne, Rüstung, Fernkampfchance %, Erschöpfung durch Treffer, Schwelle zur Kampfunfähigkeit; 15 Profile) | `src/kampf.py` (14.809 Byte) | **aktiv**: `main.py` Z. 42, Z. 2048/2079/2304/5564/5902. Quelle: `docs/quellen/Das_Kampfsystem_Neu_Original.odt` („die durch mich vervollständigte Erklärung aus dem Forum“, später als das Handbuch) |

Der Entwurf beschreibt das **Handbuch-Modell** und nennt als vorhandenen Code
„`src/kampf.py` mit `_geraeteverluste`, `_verluste_zaehlen`, `_zweikampf`“ — **diese drei Funktionen stehen
in `kampf_alt_handbuch_2009.py`** (Z. 155, 181, 192), nicht in `kampf.py`. `kampf.py` kennt stattdessen
`PROFILE`, `_ausgeschieden`, `_sieggeraete`, `_beute`, `fuehre_schlacht`. **Der Entwurf ist hier sachlich falsch.**

### 3.2 Sechs Punkte, die im Handbuch wörtlich belegt sind und im Entwurf als „offen“ stehen

| # | Entwurf sagt | Quelle sagt (wörtlich) |
|---|---|---|
| K1 | „Wallstufenwerte **fehlen**“ | HB Z. 1216–1252, **vollständige Tabelle**: Erdwall 10 / Steinwall 40 / Kleine Palisade 90 / Palisade 160 / Verst. Palisade 250 + 500 / Mauer 360 + 600 / Verst. Mauer 490 + 700 / Festungsmauer 640 + 800 / Verst. Festungsmauer 810 + 900 / Bollwerk 1000 + 1000. Steht zusätzlich in `data/buildings.json` (Gebäude 16, Stufen 1–10) und ist in `kampf.py` Z. 190–204 umgesetzt |
| K2 | „sonst halbierter Schaden“ | HB Z. 1213–1215: reicht die Schlagkraft nicht, **„ziehen sich die Truppen unverrichteter Dinge zurück. Der Kampf gilt dann als unentschieden.“** Kein halbierter Schaden |
| K3 | Genaue Zweikampfformel = Vorschlag | HB Z. 1296–1309: höherer **MU** beginnt (Gleichstand: Verteidiger), Wurf 1–100 **≤ AT** = Treffer, **PA** pariert (kein Schaden), sonst Schaden = TP − RS, Minimum 1. Alles wörtlich belegt — **nur für das Handbuch-Modell** |
| K4 | Fluchtchance 40 % + 5 % als Einheitenflucht | HB Z. 1319–1323 (Einheit): LE < 1 tot, LE < 5 → **MU** entscheidet über Flucht, Geflohene stehen danach wieder zur Verfügung. HB Z. 1334–1338 (Gerät): **der Verlierer** verliert einen Teil seiner Karren und Belagerungswaffen, „jede Einheit hat eine Fluchtchance von 40 %, jede Kampfsequenz erhöht diese Chance um 5 %“ — im Code ist das `_sieggeraete` (Geräte), nicht Einheitenflucht |
| K5 | Erschöpfung „nicht belegt“; 10 Sequenzen = Vorschlag | HB Z. 1324–1328: **Erschöpfung belegt** (Sieger eines Zweikampfs verliert 1 Punkt AT **und** PA bis Schlachtende, summiert sich). HB Z. 1274–1278: **nach 10 Sequenzen** ohne Sieger geht die Schlacht unentschieden aus, Angreifer zieht sich **ohne Beute** zurück. HB Z. 1279–1295: je Sequenz **erst Fernkampf beider Seiten gleichzeitig**, dann Nahkampf **nacheinander** gegen **zufällige** Verteidiger; Ende, wenn eine Armee keine Nahkämpfer mehr hat oder 10 Sequenzen vorbei |
| K6 | Punkteformel = Vorschlag | HB S. 5 (`ORIGINAL_Kampf_und_Punkte.md` §3): **Kriegspunkte = fester Wert je Einheit + Ausbaustufe³**, Gesamt = **(Krieg + Forschung) / 2**. So gebaut in `src/punkte.py` Z. 94–119. Der **Sieg bei 300 Punkten** ist dagegen eine **Projekt-Zielzahl** (`punkte.py` Z. 43–44, „VORSCHLAG“) |

### 3.3 Wirklich offen beim Kampf

| Frage | Stand |
|---|---|
| **Beuteanteil** | HB Z. 1332 belegt nur: **nur Transportkarren plündern**. Einen Anteil nennt das Handbuch **nicht**. Im Projekt: `auftraege.py` Z. 70 `BEUTE_ANTEIL_PROZENT = 50` steht **nur als Text**, `kampfbericht.beute` (Z. 202–242) deckelt **ausschließlich über die Karrenladung**, ohne 50-%-Grenze → **Entscheidung E4** |
| **Wer gewinnt welches Modell** (Handbuch-Zweikampf oder Forum-System) | **Entscheidung E1** — die größte offene Frage, siehe §6 |
| **Bot-Verhalten** (wann greifen Bots an, gründen sie, nutzen sie das Portal) | offen, keine Quelle |
| **Ruhmeshalle-Inhalt** | teilweise belegt: Koordinaten stehen in der Ruhmeshalle hinter dem Namen, Auftragsicon vorhanden, geschützte Spieler grün (`ORIGINAL_Kampf_und_Punkte.md` §4, `portal.php.txt` Z. 40–43) |

**Fehlt im Entwurf ganz:** der **Götterschutz**. HB Z. 215–228: erste **sieben Tage** geschützt, Ende mit dem
**ersten Kriegspunkt**; bis **299 Punkte** eingeschränkter Schutz (Angriff nur ± **20 %**), über 299 hinweg
**kein** Angriff in beide Richtungen. Das ist zwingend, sobald Bots angreifen (`main.py` Z. 2435–2446 setzt
es um). Ohne diese Regel greifen Bots einen neuen Spieler in der ersten Minute an.

---

## 4. Weltlage (§3) — was stimmt, was nicht

| # | Aussage | Befund |
|---|---|---|
| L1 | X-Y-Z-Koordinaten, 20 Dimensionen, 20×20, eigene Welt grün / fremde rot | **BELEGT** `portal.php.txt` Z. 16–22, 38–43; Register 3 |
| L2 | höchstens 6 Siedlungen, Karte per Zufall, nie zweimal dieselbe | **BELEGT** HB Z. 311–315; `ORIGINAL_Kampf_und_Punkte.md` §5 |
| L3 | 10×10-Baukarte aus **127** Originalkarten | **stimmt** — `docs/AKTUELLER_STAND.md`, `data/originalkarten/katalog.json` |
| L4 | **„`movements` ist heute immer leer“** | **FALSCH.** `main.py` Z. 5707 legt Bewegungen an, Z. 6937–6973 wertet Ankunft aus (Altpfad). **Zusätzlich** existiert der vollständige Auftragspfad `self.auftraege` (`auftraege.py`, `main.py` Z. 855/1395/1961/1995/2451) → **es gibt zwei Bewegungssysteme nebeneinander** |
| L5 | Portalwechsel: 5.000 Mana, einmal je 24 h | **BELEGT** `portal.php.txt` Z. 23–37 |
| L6 | „Der Wechsel verschiebt die **ausgewählte eigene Siedlung**“ | **WIDERSPRUCH zur Quelle.** Z. 23–27, 35: **die ganze Welt** wird verschoben („Eure Welt an ihren neuen Platz“), und das Mana muss **in einer einzelnen Siedlung** verfügbar sein, nicht über mehrere verteilt. Eine einzelne Siedlung umziehen ist eine Remake-Idee → **Entscheidung E5** |
| L7 | Mana nur beim Dimensionswechsel | **unvollständig.** Z. 6–14: **jedes Entsenden** kostet Mana, **unabhängig von der Anzahl der Einheiten**, Höhe nach Entfernung im Limbus. Fehlt im Entwurf |

---

## 5. Was bereits gebaut ist (nicht doppelt bauen!)

| Baustein | Beleg im Code | Prüfdatei |
|---|---|---|
| Wallvorrunde mit Schwellen + Rückzug → unentschieden | `kampf.py` Z. 190–204, `kampfbericht.vorrunde` Z. 74 | `test_kampf.py`, `test_gpt_wall_bot_kampf.py`, `test_gpt_wallsystem_eingehaengt.py` |
| Mauerschaden (Waffe − Mauerstufe), pro Waffe einzeln | `kampf.py` Z. 244–251, `kampfbericht.mauer_schaden` Z. 156 | `test_gpt_dorfwall.py` |
| Kampfsequenzen, Fernkampf-Vorrunden, Rückzug der Schützen, Konstitutionsprobe | `kampf.py` Z. 209–312 | `test_kampf.py` 36/0, `test_gpt_kampf_forum_neu.py` |
| Geräteverlust 40 % + 5 % je Sequenz | `kampf.py` `_sieggeraete` Z. 110–119 | `test_gpt_kampf_botbeute_echte_kasse.py` |
| Beute über Karrenladung | `kampf.py` `_beute` Z. 122–136, `kampfbericht.beute` Z. 202 | `test_kampfbericht.py` |
| Punkte: je Einheit + Wallstufe³, Gesamt /2, Zielzahl 300 | `punkte.py` Z. 94–119 | `test_punkte_einhaengung` 60/0/0 |
| Reisezeit `d / GS` in Sekunden, Rückkehr doppelt | `auftraege.py` Z. 133–147, `HIN_UND_RUECK_FAKTOR` Z. 55 | `test_gpt_zeit_auftragsketten.py` |
| Auftragsliste mit Start/Ankunft/Fortschritt | `auftraege.py`, `main.py` Z. 1961/1995/2451 | `test_gpt_zeit_auftragsketten.py` |
| Götterschutz 7 Tage / erster Kriegspunkt | `main.py` Z. 2435–2446 | Handbuch-Abgleich 05.10. |

**Prüfstand:** Sammellauf **60 von 60 grün, 568 s**. Seit diesem Lauf wurde **`src/` und `data/` nicht geändert**
(letzter Commit an `src/`/`data/`: `d404d66`, danach nur `docs/` und `tests/`) → **nicht erneut prüfen**.

---

## 6. Die fünf Entscheidungen, die wirklich Daniel gehören

| # | Frage | Was dafür spricht |
|---|---|---|
| **E1** | **Welches Kampfsystem gilt?** (a) neueres Forum-Original = heutiger Code mit 15 Profilen, 14 grünen Prüfdateien; (b) Handbuch 2009 LE/AT/PA (Rückfallmodul); (c) Mischung: Forum-System für die Auflösung, Handbuch für Wall, Geräteverlust, Beute, Punkte | Die aktuelle Wahl (a) ist eine **dokumentierte Projektentscheidung** (29.10., GPT-KA01…KA06). Ein Wechsel auf (b) wirft 15 Profile und 14 Prüfdateien weg. Empfehlung des Prüfers: **(c)** — Forum-System behalten, die belegten Handbuchteile sind bereits eingebaut, der Entwurf wird auf dieses Modell umgeschrieben |
| **E2** | **Reiseformel:** Faktor 1 (gebaut: `d/GS` Stunden) oder Faktor 2 (Entwurf: `2·d/GS`)? | Faktor 1 ist gebaut und geprüft; Faktor 2 verdoppelt alle Wege. Beides ist Vorschlag — es darf nur **eine** Formel im Code bleiben. Dazu: kostet ein Dimensionswechsel **Zeit** (Entwurf: 20 Felder) oder nur Mana (Quelle)? |
| **E3** | **Zwei Bewegungssysteme:** `self.auftraege` (vollständig, W7) behalten und den Altpfad `state.movements`/`_welt_bewegen` (Z. 5690, mit Zufallsbeute 10–40 % und Zufallskampf) abklemmen? | Zwei Systeme mit zwei Formeln und zwei Beuteregeln widersprechen sich zwangsläufig. Empfehlung: **nur `auftraege.py`** |
| **E4** | **Beuteanteil:** Deckel 50 % (Vorschlag im Code, nirgends durchgesetzt) oder nur Karrenladung (heute)? | Quelle nennt keinen Anteil. Ohne Deckel kann ein einzelner Handkarren (40 Einheiten) eine volle Siedlung anteilig leerlaufen lassen, wenn wenige Rohstoffe lagern |
| **E5** | **Portal:** ganze Welt verschieben (Quelle) oder eine Siedlung (Entwurf)? Und: **Siegbedingung 300 Gesamtpunkte** neu bewerten — Wallstufe 10 bringt allein **1.000 Kriegspunkte**, also **500 Gesamtpunkte**, der Sieg wäre durch reinen Mauerbau erreichbar (so schon im `Fehlerregister_Nebelseetal.md` A03 vermerkt) | Quelle ist eindeutig (ganze Welt, Mana in einer Siedlung). Die 300 sind Daniels frühere Wahl und geraten durch die Original-Punkteformel in Konflikt |

---

## 7. Der EINE nächste Schritt

**Sobald E1 und E2 entschieden sind:** den Kampfteil des Entwurfs auf das gewählte Modell umschreiben
(§2.1 und §2.2 ersetzen, §5 auf die wahren Lücken kürzen) und die Wegzeit-Formel im Code auf **eine**
Fassung festlegen — erwartetes Ergebnis: `docs/ENTWURF_WEGZEIT_KAMPF_WELT_20261031.md` ohne die sechs
falschen „nicht belegt“-Einträge, und `src/auftraege.py` mit **einer** Formel, die zu `docs/` passt.
Danach erst Umsetzung, ein Commit je Schritt, mit Prüfzusage.

**Nicht nötig, weil schon gebaut:** Wallschwellen, Sequenzen, Geräteverlust, Beute über Karren,
Reisezeit-Grundfunktion, Punkte, Götterschutz.

---

## 8. Registerwirkung

Neu eingetragen in `docs/PRUEFREGEL_ORIGINAL.md`: **Punkte 35–39** (Walltabelle aus dem Handbuch selbst,
Rückzug → unentschieden, Sequenzablauf + 10 Sequenzen, Erschöpfung, Auftragskosten + Drosselung) und
**Punkt 40** (Kampfmodell-Konflikt: Handbuch vs. neueres Forum-Original). Damit ist belegt, was den
Entwurf in die Irre geführt hat: die Belege lagen in `docs/original/ORIGINAL_Kampf_und_Punkte.md`,
das der Entwurf nicht gelesen hat.

*Erstellt 31.10.2026, 02:30. Alle Zeilenangaben gegen die Textfassung geprüft, nicht aus dem Gedächtnis.*
