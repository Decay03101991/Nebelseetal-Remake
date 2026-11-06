# ABGLEICH der vier Modellantworten - 06.11.2026

**Wozu:** Daniel will aus vier Antworten EINEN vorerst fixen Ablauf. Dieses Dokument legt die
Antworten je Thema nebeneinander, prueft jede tragende Zahl gegen Code, Daten und unsere gerechneten
Tabellen und sagt dann, was in den Ablauf kommt - und was als VORSCHLAG zu Daniel geht.

**Quellen** (alle hashgeprueft abgelegt, Index in `docs/eingaenge/LLM_20261106/README.md`):

| Kuerzel | Datei | Umfang |
|---|---|---|
| C | `antworten/Antwort_ClaudeOpus55_AUFTRAG_20261106.md` | 46.259 Byte, 463 Zeilen |
| U | `antworten/Antwort_UseAI-Instant_AUFTRAG_20261106.md` | 86.957 Byte, 720 Zeilen |
| G | `antworten/Antwort_Grok_Auftrag_20261106.odt` | 25.066 Byte, 220 Textzeilen |
| M | `antworten/Antwort_Gemini_AUFTRAG_20261106.md` (Gemini) | 8.673 Byte, 95 Zeilen |

**Verfahren.** Zuerst die Claude-Antwort vollstaendig gelesen (Daniels Vorgabe), die drei anderen
vollstaendig ausgezogen (je Thema mit Zeilenfundstelle, ohne Bewertung). Dann jede Zahl, die eine
Entscheidung traegt, gegen die Quelle gehalten: `data/`, `src/`, `docs/S0_TABELLEN_20261107.md`
(V-1 bis V-5), Handbuch 2009, 2006er Seiten. Urteile: **UEBERNEHMEN** (belegt und passend),
**VORSCHLAG** (plausibel, ohne Beleg - Daniel entscheidet), **VERWERFEN** (widerspricht Code oder Daten).

**Regel, die bleibt:** Uebereinstimmung zwischen Modellen ist **kein** Beleg. Drei Modelle koennen
dieselbe falsche Zahl aus demselben Dokument ableiten - genau das ist unten in zwei Faellen passiert
(G-1 und die A-6-Behauptungen).

---

## 1. Wo alle vier dasselbe sagen (Richtung belegt, Zahl oft nicht)

| Punkt | C | U | G | M | Gegenprobe | Urteil |
|---|---|---|---|---|---|---|
| Gunst 0..100 mit drei Statusstufen 0-39 / 40-59 / 60-100 | Z. 63-67 | Z. 248-252 | Z. 39-47 | Z. 39 | `docs/extern/Nebelseetal_LLM_Auftrag_20261106.md` 7.1 = Auftragsdokument, nicht Original | UEBERNEHMEN (Auftragswert), Originalbeleg im Handbuch nachziehen |
| Gunst und Status NUR ueber `bot_als_dict` / `bot_aus_dict` | Z. 65 | Z. 250-253 | Z. 41 | Z. 39 | `src/main.py:6482` / `:6507` vorhanden; `BotPlayer` (Z. 280-320) hat kein Feld `gunst` | UEBERNEHMEN |
| NAP ab Gunst 40, 3 Spieltage, Bruch -20 Gunst und +1 Rache | Z. 80 | Z. 264-265 | Z. 70 | Z. 42 (nur -20) | Auftragsdokument 7.2 | VORSCHLAG: 86.400 s = 3 Spieltage a 28.800 s rechnerisch richtig, aber 7.2 ist kein Originalbeleg |
| Durchmarsch ab Gunst 60, nur Anzeige | Z. 80 | Z. 265 | Z. 70-74 | fehlt | Auftragsdokument 7.2 | UEBERNEHMEN als Anzeige (keine Mechanik, kein Risiko) |
| Handelsabkommen ueber den vorhandenen `spieloekonomie.handel_start` (kein zweiter Handelsweg) | Z. 79 | Z. 265 | Z. 69 | fehlt (nur Verweis) | `spieloekonomie.handel_start` vorhanden | UEBERNEHMEN - F-04 wird so nicht verletzt |
| Rachetopf: +1 je Niederlage, +1 je Spieltag ohne Kontakt, Schwelle 3 | Z. 93-94 | Z. 264-265 | Z. 55-57 | fehlt | Auftragsdokument 7.2 | VORSCHLAG (7.2 ist kein Originalbeleg) |
| Armee-Schwelle 99 SK (Wallstufe 3 = 90 SK + 10 Prozent) | Z. 94 | Z. 264 / 645 | Z. 56 | Z. 40 | `docs/S0_TABELLEN_20261107.md` V-5: Rache-Schwelle **99 SK** | UEBERNEHMEN - alle vier nennen 99, unsere V-5 auch |
| Ereignisse Haug 990 Holz / 64 Gold, Grom 5 zu 20, Silra 12 Gold | Z. 108 | Z. 644 (nur Haug) | Z. 70 | Z. 40 | `docs/S0_TABELLEN_20261107.md` V-4 | Zahlen UEBERNEHMEN (V-4), **Grom ist nicht baubar** (G-4) |
| Handelspunkte bleiben 0, der Handelsweg ist eine Sackgasse | Z. 119-127 | Z. 122-130 | Z. 25 | Z. 24-26 | Auftragsdokument 4.7; keine Gegenmessung in dieser Sitzung | UEBERNEHMEN als Messauftrag: erst Diagnose, dann Fix |
| Bots brauchen Drachenregel, Spionage und eine Reaktion | Z. 133-141 | Z. 272-287 | Z. 81-84 | Z. 28 | `src/spionage.py`, `src/bottaktik.py`, `src/drachen.py` vorhanden | UEBERNEHMEN, aber **ohne neues Modul** (U-6 hat recht: die Module existieren, es fehlt der Aufrufer) |
| Fuenf Balancing-Werkzeuge (Kennzahlenblatt, Sollkurve, Regelkreis, Feedback, Abnahme) | Z. 165-195 | Z. 370-378 | Z. 125-163 | Z. 51-59 | Auftragsdokument 9.2 | UEBERNEHMEN; Reihenfolge der Modelle weicht ab (siehe 4) |

## 2. Wo die Antworten abweichen - und was die Gegenprobe sagt

### 2.1 Wohin gehoert die Diplomatie im Code?
- C: **ein neues Modul** `src/diplomatie.py` + `data/diplomatie.json` (Z. 57).
- U: `src/gunst.py` + `data/gunst.json` (Z. 248) - eigenes Modul nur fuer die Gunst.
- G: Felder in `main.py`, Daten in `data/bot_gunst.json` (Z. 39-47).
- M: `src/botkern.py` und `src/bot_angriffsplanung.py` (Z. 38).
- **Gegenprobe:** `botkern.py` ist die Bot-Wirtschaft, `bot_angriffsplanung.py` die Zielwahl;
  `BotPlayer` steht in `main.py` (Z. 280). Gunst, Rachetopf, Vertraege und Ereignisse sind EIN Thema
  mit vier Teilen und teilen sich die Zahlen - vier Module waeren vier Lesestellen fuer eine Frage.
- **Urteil:** C. EIN Modul `src/diplomatie.py` mit einer Datendatei `data/diplomatie.json` (Vorlage
  Z-4, jede Zahl mit `quelle`). M wuerde zwei fremde Themen mischen, G verteilt Logik auf `main.py`,
  U baut ein Modul fuer ein Feld.

### 2.2 Wo sitzt die Sperre, die ein NAP und ein Vertrag pruefen muessen?
- C: in der vorhandenen Angriffssperre, Name unsicher, vermutet `versorgungsschutz.py` (Z. 79).
- U: ebenfalls `versorgungsschutz.py` (Z. 654-656: dort steht ein zweiter Grund).
- G: dasselbe Gate wie der Goetterschutz (Z. 71) - ohne Dateinamen.
- M: analog zum Goetterschutz (Z. 39).
- **Gegenprobe (G-1):** die echte Sperre ist `punkte.angreifbar` (`src/punkte.py:242`), verdrahtet an
  genau zwei Stellen: `src/main.py:7051` (Angriff auf einen Spieler-Ort) und `src/main.py:6624`
  (Diebstahl zwischen Bots). Zusaetzlich `src/main.py:6966` (`self.noob_protection`) und `:6960`
  (Demo-Regel). `src/versorgungsschutz.py` ist laut eigenem Kopf-Docstring eine Vorabpruefung auf
  Rohstoff-Sackgassen - **kein Angriffsgate**.
- **Urteil:** C und U irren hier beide (gleicher Fehler, unabhaengig voneinander). Der NAP gehoert in
  die zwei Stellen, die `punkte.angreifbar` aufrufen, ueber EINE neue Hilfsfunktion
  `diplomatie.angriff_gesperrt(bot, ziel_punkte, jetzt) -> (bool, grund)`, die zuerst den Vertrag,
  dann `punkte.angreifbar` fragt. Zwei Aufrufstellen, eine Lesestelle.

### 2.3 Wann ist der Rachetopf bereit?
- C: Topf >= 3 loest die **Ankuendigung** aus, der Angriff erst bei Armee >= 99 SK (Z. 93-95, E-2).
- U: Topf-Schwelle 99 SK als eine Zahl, Ankuendigung ab 3 (Z. 264-265).
- G: Topf ab 3 **und** eigene SK ueber 99 SK (Z. 55-57).
- M: nur die Schwelle 99 SK (Z. 40).
- **Gegenprobe:** C hat recht, dass zwei Groessen gemeint sind - der Topf zaehlt Ereignisse, 99 SK ist
  eine Armeestaerke (V-5). Die Formulierung im Auftragsdokument (7.3) vermischt beides.
- **Urteil:** C. Zwei Bedingungen (`topf >= 3` UND `armee_sk >= 99`), beide in `data/diplomatie.json`.

### 2.4 Was passiert nach einem Bot-Sieg?
- C: Topf auf 0 (VORSCHLAG, Z. 94). U: `bei_sieg: -1` (Z. 264-265). G: -1 mit Untergrenze 0 (Z. 56).
- **Gegenprobe:** das Auftragsdokument 7.2 sagt nur „senkt“, ohne Zahl.
- **Urteil:** VORSCHLAG - Daniel entscheidet zwischen 0 und -1. Vorerst 0 (C), weil ein Sieg den
  Zorn vollstaendig abbaut und die Bremse gegen Dauerangriffe staerker ist. Steht als offene Frage.

### 2.5 Ruht der Rachetopf unter Goetterschutz?
- C: ja, sonst feuert er am Spieltag 3, das erste Gefecht kommt erst Tag 8-12 (E-1, Z. 40).
- U: der Zaehler ohne Kontakt ruht, solange ein Vertrag laeuft (Z. 645).
- G: kein Ruhen vorgeschlagen. M: nichts.
- **Gegenprobe:** `self.noob_protection` sperrt JEDEN Bot-Angriff bis zum ersten Kriegspunkt
  (`src/main.py:6966`, Ende `:7323-7331`). Ein Topf, der in dieser Zeit auf 3 steigt, feuert also
  unmittelbar nach dem Ende der Sperre - genau der Effekt, den E-1 beschreibt.
- **Urteil:** C, erweitert um U: der Tageszaehler ruht unter Goetterschutz UND waehrend eines
  laufenden Vertrags. Kein neuer Mechanismus, nur eine Bedingung in `rache_tag`.

### 2.6 Ereignisse: Frist, Wirkung, Haeufigkeit
- C: Frist 2 Spieltage = 57.600 s, Gunst +5 / -5, 1 Ereignis je Bot und 3 Spieltage (alles VORSCHLAG,
  Z. 107-109). U: nur Haugs Tribut, Frist in `data/nachrichten.json` (Z. 644). G: 2 Spieltage, Schalter
  `ereignisse_aktiv`, ablehnbar (Z. 67-75). M: nur die drei Kostensaetze, keine Frist (Z. 40).
- **Gegenprobe:** kein Originalbeleg fuer Frist oder Haeufigkeit (Handbuch/2006er schweigen dazu);
  `story`-Overlay ist vorhanden. Die Ereignispreise stehen in V-4.
- **Urteil:** C als Vorlage, Schalter `aktiv` aus G - aber alles, was nicht in V-4 steht, ist
  VORSCHLAG und geht an Daniel.

### 2.7 Grom-Ereignis: gibt es Werkzeuge und Eisen?
- **Gegenprobe (G-4):** 17 Waren in `data/items.json` (Messer bis Fellruestung - keine Werkzeuge),
  9 Rohstoffe in `data/resources.json` (holz, stein, metall, mana, nahrung, gold, wolle, leder,
  pferde - kein Eisen). Alle vier Antworten schreiben den V-4-Satz ab, ohne das zu merken.
- **Urteil:** nicht baubar wie geschrieben. **Frage an Daniel**: Grom tauscht 5 Waren gegen 20 Metall
  (naechstliegende vorhandene Gueter) oder das Ereignis entfaellt. Keine Zahl erfinden.

### 2.8 Handelsweg: Diagnose oder gleich bauen?
- C: erst `tools/handelsweg_diagnose.py`, erster abgelehnter Schritt mit Grund, Fix als eigener
  Commit (Z. 120-127).
- U: eine Prueffunktion `angebotswege.pruefe_handel(ort, ziel, ware, menge) -> (bool, grund)` mit fuenf
  Grunden (`kein_karren`, `keine_ware`, `kein_kontakt`, `gesperrt_auftrag`, `kein_punktetyp`) und
  einem Zaehler je Grund im Journal (Z. 227-239).
- G: `handel_start` um die Richtung Spieler-zu-Bot erweitern, Punkte = Warenwert / 100 (VORSCHLAG,
  Z. 91-103). M: nur der Einwand.
- **Gegenprobe:** ohne Messung ist jede der drei Ursachen eine Vermutung. U's Zaehler je Grund ist
  die billigste Diagnose, die zugleich dauerhaft bleibt (A-2: eine Urteilsfunktion fuer Kern und
  Anzeige).
- **Urteil:** U's Prueffunktion **als Diagnose** (sie liefert den Grund und ist schon die spaetere
  Anzeige), C's Reihenfolge (erst messen, dann EIN Fix-Commit). G's Punktwert bleibt VORSCHLAG.

### 2.9 Bot-Luecken: neues Modul oder vorhandene Module?
- C: `bot_drache_entscheidung` (SK >= Drachenwert x 1,5, VORSCHLAG), `data/bot_persoenlichkeit.json`
  mit Faktoren 0,8-1,2 auf vorhandene Schwellen (Z. 135-141).
- U: **kein neues Modul** - `spionage.pruefe_bot_gegen_spieler`, `drachen.bedrohung(ort)`, Daten in
  `bot_drachen.json`, `bot_spionage.json`, `bot_reaktion.json`; Meidung um den Hort in 3 Stufen
  (Z. 272-287).
- G: Bots meiden den Drachen unter der eigenen SK-Schwelle, Gunst -1 je Kriegspunkt (Z. 81-84).
- M: nichts.
- **Gegenprobe:** `src/spionage.py`, `src/drachen.py`, `src/bottaktik.py` existieren; U hat den
  besseren Beleg. C's Persoenlichkeitsdatei ist additiv und ohne neue Logik - vertraeglich.
- **Urteil:** U's Bauteile + C's Faktoren, in EINER Datendatei `data/bot_diplomatie.json` statt drei
  (eine Datei je Thema, nicht je Funktion). Der Sicherheitsfaktor 1,5 bleibt VORSCHLAG.

### 2.10 Balancing-Werkzeuge: wo liegen die Dateien?
- C: `docs/balancing/kennzahlen.jsonl` + `KENNZAHLEN_<Datum>.md`, Werkzeug `tools/balance_kreis.py`,
  Kennzahlenblatt im vorhandenen `spieltest_simulation.py` (Z. 165-195).
- U: fuenf Werkzeuge, Sollkurve mit Baendern 0,8/1,05 und 2,5..4,5 Punkten, Regelkreis mit Schwelle
  15 Prozent und 5 Laeufen, neues Gate G-7 (Z. 370-378).
- G: `docs/balancing/partie_<id>.jsonl` (Z. 129-132). M: `tools/partie_metrik.py`, `docs/audits/`.
- **Gegenprobe:** `tools/spieltest_simulation.py` und `tools/balancing_messung.py` gibt es;
  `tools/balance_kreis.py` nicht. Fuer Punkte je Spieltag nennt V-3 **3,3** - U's Band 2,5..4,5 ist
  daraus abgeleitet, nicht belegt.
- **Urteil:** C's Orte (`docs/balancing/`) und C's einziges neues Werkzeug; U's Gate G-7 als
  **Kennzahl** im Kennzahlenblatt, nicht als neue Abschlussbedingung (A-3 bleibt A-3).
  Alle Baender bleiben VORSCHLAG.

### 2.11 Ist A-6 erfuellt?
- C: **offen**, die 1.400 s fallen voraussichtlich (E-4, Z. 43).
- U: **offen mit Grund**, Sammellauf nicht fahrbar (Z. 556).
- G: erfuellt nach jedem Schnitt, 183 Dateien / 7.495 Pruefungen / 0 rot / unter 1.400 s (Z. 174).
- M: alle sieben Bedingungen **Erfuellt** (Z. 63-71).
- **Gegenprobe (G-5):** `docs/audits/sammellauf_20261106_0755.log` endet mit
  `181 von 183 gruen, 0 rot, 1612 s` und `183 Dateien, zusammen 7502 bestandene Pruefungen, 0 Fehler,
  60 Befunde`. Also **1.612 s statt unter 1.400 s** und **7.502 statt 7.495** Pruefungen.
- **Urteil:** G und M behaupten einen erfuellten Zustand, der messbar nicht besteht - das ist genau
  die Fehlerklasse, vor der das Auftragsdokument warnt. C und U haben recht. A-6 muss umformuliert
  werden (Dauer und Pruefzahl) **und** der Sammellauf schneller werden.

### 2.12 Reihenfolge: kommt das Kennzahlenblatt vor oder nach S4 Teil 1?
- C: Kennzahlenblatt **vor** Schnitt 1, weil es die Vorher-Zahlen liefert (Z. 217-219).
- U: erst der Angebotsweg-Diagnoseschnitt, dann S4/1 (Z. 224, 241).
- G: Gunst zuerst (Z. 179). M: Gunst zuerst (Z. 75).
- **Gegenprobe:** Gunst hat laut allen vier Antworten **keinen** Aufbauzeit-Effekt - sie veraendert
  kein messbares Spielverhalten. Ein Kennzahlenblatt davor bringt fuer diesen Schnitt also nichts.
  Daniels Vorgabe ist ausserdem ausdruecklich: mit S4 Teil 1 beginnen (Uebergabe 06.11.2026).
- **Urteil:** Daniels Reihenfolge gilt. Das Kennzahlenblatt kommt **unmittelbar nach S4 Teil 1**, weil
  ab dem Rachetopf jede Aenderung eine Vorher-Messung braucht.

## 3. Feste Befunde aus der Gegenprobe (nicht aus einer Antwort)

| Nr | Befund | Beleg |
|---|---|---|
| G-1 | Angriffssperre ist `punkte.angreifbar` an `src/main.py:7051` (Angriff) und `:6624` (Diebstahl), dazu `noob_protection` `:6966` und Demo `:6960`. `versorgungsschutz.py` ist KEIN Gate. | `src/punkte.py:242`, `src/main.py` |
| G-2 | Rache-Schwelle ist **99 SK**; `docs/ABLAUF_20261107.md:85` schreibt faelschlich 90 SK (das ist die Wall-Schwelle). | `docs/S0_TABELLEN_20261107.md:117-132` |
| G-3 | E-3 (V-4 nicht nachrechenbar) ist **aufgeloest**: `tools/s0_tabellen.py:110` rechnet Nahrung `(gras+steppe)*2*24 = 1.723`, `:111` Gold `berg*0,5*24 = 128`. Beide Formeln sind im Werkzeug VORSCHLAG, im Dokument fehlen sie. | `tools/s0_tabellen.py` |
| G-4 | Werkzeuge und Eisen gibt es nicht: 17 Waren, 9 Rohstoffe (metall, kein eisen). Grom-Ereignis so nicht baubar. | `data/items.json`, `data/resources.json` |
| G-5 | A-6 ist heute nicht erfuellt: 1.612 s und 7.502 Pruefungen gegen unter 1.400 s und 7.495. | `docs/audits/sammellauf_20261106_0755.log` |
| G-6 | `BotPlayer` hat kein Feld `gunst` und kein Feld `rache`; `bot_als_dict` Z. 6482, `bot_aus_dict` Z. 6507. `data/diplomatie.json` und `data/ereignisse.json` fehlen. | `src/main.py` |
| G-7 | `data/bot_raubzug.json`, `data/bot_stimmen.json`, `data/nachrichten.json`, `data/story.json`, `src/spionage.py`, `src/drachen.py` sind vorhanden - Bot-Luecken brauchen Daten und Aufrufer, keine Module. | `src/`, `data/` |

## 4. Was in den fixen Ablauf kommt (Kurzfassung, ausfuehrlich in `docs/ABLAUF_LLM_20261106.md`)

1. S4 Teil 1 Gunst und Status (C, mit U's Prueffallzahl 10) - `src/diplomatie.py`, `data/diplomatie.json`.
2. Kennzahlenblatt (C 4.1, U-Gate G-7 als Kennzahl) - liefert die Vorher-Zahlen fuer alles Weitere.
3. S4 Teil 2a Vertraege (C + G; Sperre an den ZWEI echten Gates, G-1).
4. S4 Teil 2b Rachetopf (C, mit Ruhen unter Goetterschutz und Vertrag; 99 SK aus V-5).
5. S4 Teil 3 Ereignisse (C + G; Grom nur nach Daniels Entscheidung, G-4).
6. Handelsweg: Diagnose (U's Prueffunktion) und EIN Fix-Commit.
7. Bot-Luecken: Drache, Spionage, Reaktion (U's Bauteile + C's Faktoren, eine Datendatei).
8. Sollkurve und Regelkreis (C 4.2-4.5).
9. A-1/A-2 E2E-Ketten und Quellwache (C Schnitt 7) - ganz am Ende, weil sie alle Wege pruefen.
10. A-6: Sammellauf beschleunigen ODER Grenze neu fassen (Daniel, G-5).
11. S5 bleibt gesperrt.

## 5. Offene Entscheidungen fuer Daniel (werden in EINER Runde gestellt)

| Nr | Frage | Messlage | Empfehlung |
|---|---|---|---|
| F-1 | Grom-Ereignis: 5 Waren gegen 20 Metall, oder Ereignis streichen? | G-4: Werkzeuge und Eisen existieren nicht | 5 Waren gegen 20 Metall, Schalter `aktiv` |
| F-2 | A-6: Grenze neu fassen (z. B. 1.800 s) oder Sammellauf beschleunigen? | G-5: 1.612 s heute, Ziel war 1.400 s | erst beschleunigen (`--parallel`), Grenze als VORSCHLAG 1.800 s bis dahin |
| F-3 | Rachetopf nach Bot-Sieg: auf 0 oder -1? | Auftrag 7.2 sagt nur senkt | 0 (C) |
| F-4 | Gunst-Startwert 50 ohne Quittung? | Alle vier nennen 50, keiner belegt es | 50 als VORSCHLAG eintragen, Daniel bestaetigt |
| F-5 | Kennzahlenblatt direkt nach S4 Teil 1? | Gunst hat keinen Aufbauzeit-Effekt, Messung bringt dort nichts | ja, als naechster Schritt |
