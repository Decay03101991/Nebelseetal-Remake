# BILDPAKET WAPPEN — passen die zehn Wappen zu den sechs Burgen? (F-78)

**Sitzung 43, 13.11.2026, 08:3x.** Rein messend und beschreibend: **keine Datei geändert**, weder
`data/bot_wappen.json` noch `FRAKTIONEN_WELTEN.md` noch ein Bild. Dies ist der Bildbeleg zu F-78 und
ein Vorschlag — die Entscheidung gehört Daniel.

**Was F-78 verlangt (Register 568, Daniels Wortlaut):** „Die burgbilder kann ich vorerst nicht ersetzen
aber das ist der einzige grund warum ich sie festlege. Heißt es muss geschichte und stil den burgen
angepasst werden. Auch Wappen usw“ — die **Burgen sind fest**, Geschichte, Stil **und Wappen** folgen.

---

## 1. Wie gemessen wurde

Zwei voneinander unabhängige Quellen, damit kein Eindruck als Beleg durchgeht:

1. **Farbfamilien, hart gezählt:** je Bild die deckenden Pixel (Alpha > 128) auf 160 × 160 verkleinert
   und in neun grobe Familien einsortiert, ausgegeben als Flächenanteil. Anteile unter 5 % sind
   weggelassen.
2. **Motiv, angesehen:** jedes Bild einzeln beschrieben (Gegenstand, Bauweise, Stimmung).

## 2. Die sechs Burgen (Bilder fest)

| Bild | Farbfamilien (gemessen) | Motiv |
|---|---|---|
| `burg_01` | grau 35 %, schwarz 17 %, gold 8 % | grauer Stein, blaue Kegeldächer, blaue Banner mit goldener Lilie |
| `burg_02` | grau 23 %, **rot 23 %**, braun 11 % | rote Kegeldächer, helle Steinmauern, rotes Banner mit goldenem Löwen, grüne Bäume |
| `burg_03` | grau 23 %, gold 20 %, **weiß/silber 19 %** | weiß-goldene Türme, blaue Kristallfenster, Statuen |
| `burg_04` | **violett 35 %**, schwarz 25 %, blau 11 % | gotische Burg, lila Licht, violette Banner, Nebel |
| `burg_05` | gold 20 %, **grün 17 %**, braun 15 % | Burg in einem Baum, grüne Dächer, goldene Lichter, Wasserfälle |
| `burg_06` | **blau 74 %**, weiß/silber 19 % | Eis- und Kristallburg **auf einer schwebenden Felseninsel**, Eiszapfen, Schneeflocken-Banner |

## 3. Die zehn Wappen

| Bild | Farbfamilien (gemessen) | Motiv |
|---|---|---|
| `wappen_01` | schwarz 31 %, weiß 14 %, gold 13 % | heulender Wolfskopf über Schneebergen, nachtblauer Schild |
| `wappen_02` | schwarz 35 %, **violett 26 %**, gold 9 % | Rabe auf Ast, Mondsichel, gotisch |
| `wappen_03` | schwarz 44 %, gold 27 %, braun 16 % | goldener Hirschkopf mit Geweih, Eichenlaub |
| `wappen_04` | **rot 35 %**, schwarz 22 %, gold 21 % | goldene Krone über rotem Banner, Lorbeer |
| `wappen_05` | schwarz 29 %, grau 27 %, gold 10 % | steinerne Zinnenburg vor Bergen |
| `wappen_06` | schwarz 27 %, gold 18 %, rot 16 % | zwei gekreuzte Schwerter, Lorbeer |
| `wappen_07` | schwarz 48 %, gold 24 %, braun 12 % | Lebensbaum mit Wurzeln (nicht kriegerisch) |
| `wappen_08` | rot 38 %, schwarz 36 %, gold 9 % | roter Drache |
| `wappen_09` | schwarz 32 %, grau 19 %, blau 13 % | silberne Mondsichel mit achtzackigem Goldstern, kleinere Sterne, Wolken — ausdrücklich „Sternennacht“ |
| `wappen_10` | schwarz 39 %, gold 18 %, grau 16 % | Schmiedehammer über Schneebergen, Knotenmuster — das klarste Zwergenmotiv des Satzes |

## 4. Der Ist-Stand (`data/bot_wappen.json`) — vier von sechs Paaren widersprechen sich

| Haus | Farben in `FRAKTIONEN_WELTEN.md` | Burg | Wappen | Widerspruch |
|---|---|---|---|---|
| Silberbach (Menschen) | Blau und Silber | `burg_01` grau/blau/gold ✓ | `wappen_04` **rot 35 %** | das Wappen bringt Rot in ein blaues Haus |
| Hammerhall (Zwerge) | Schwarz und Gold | `burg_02` **rot/grau** | `wappen_05` grau | Burg ist rot, nicht schwarz; `wappen_05` ist ein Steinturm, kein Zwergenmotiv |
| Sternenwacht (Elfen) | Silber und Grün | `burg_03` weiß/gold | `wappen_03` gold/braun | „Grün“ steht nur im Text — weder Burg noch Wappen ist grün |
| Schattenfaust (Trolle) | **Weiß und Gold** | `burg_04` **violett/schwarz** | `wappen_02` **violett** | harter Widerspruch in beide Richtungen |
| Knochenmoor (Ghule) | Violett und Grün | `burg_05` **grün/gold** | `wappen_01` schwarz/weiß | Haus violett, Burg grün, Wappen nachtblau — keine Farbe deckt sich |
| Flickwerk (Gnome) | Messing und Rauch | `burg_06` **blau 74 %** | `wappen_06` schwarz/gold/rot | Eisblau gegen Messing |

Der Ringtausch vom 04.11.2026 hat die Wappen untereinander bewegt, aber nicht auf die Burgen
abgestimmt — das ist der Kern des Befunds.

## 5. Vorschlag: sechs Paare, die sich in Bild UND Farbe decken

Die Burg bleibt bei ihrem Bild; umgehängt wird, **welche** Burg zu welchem Haus gehört, und die
Farbzeile des Hauses wird auf die Burg gezogen. `data/bot_wappen.json` ist eine Datendatei — das ist
**kein Codeeingriff**; `tests/test_bot_wappen.py` prüft Vorhandensein und Eindeutigkeit, nicht Geschmack.

| Haus | Burg neu | Wappen neu | Farben neu | Warum (aus den Bildern) |
|---|---|---|---|---|
| Silberbach (Menschen, Midgard) | `burg_02` | `wappen_04` (bleibt) | **Rot, Grau und Gold** | rote Dächer und goldener Löwe im Banner; die Krone sitzt farblich genau darauf |
| Hammerhall (Zwerge, Armageddon) | `burg_01` | `wappen_10` | **Grau, Schwarz und Gold** | grauer Stein, blaue Banner; `wappen_10` zeigt den Schmiedehammer über Bergen |
| Sternenwacht (Elfen, Valhalla) | `burg_03` | `wappen_09` | **Weiß, Silber und Nachtblau** | weiße Goldtürme mit Kristallfenstern; „Sternenwacht“ ↔ Mondsichel und Sterne |
| Schattenfaust (Trolle, Utgard) | `burg_05` | `wappen_01` | **Grün, Schwarz und Gold** | Waldburg und Wolf — Hochland und „große Bestien“ |
| Knochenmoor (Ghule, Ragnarök) | `burg_04` | `wappen_02` | **Violett und Schwarz** | violette Burg, Rabe und Mondsichel — das einzige Paar, das schon heute stimmt (nur die Burg fehlt) |
| Flickwerk (Gnome, Limbus) | `burg_06` | `wappen_05` | **Eisblau, Weiß und Messing** | `burg_06` steht **auf einer schwebenden Felseninsel** — das ist der Limbus; „aus wenig viel bauen“ ↔ Steinbau |

**Was das kostet:** fünf Burg-Zuordnungen, fünf Wappen-Zuordnungen, fünf Farbzeilen in
`FRAKTIONEN_WELTEN.md`. **Was es bringt:** jedes Paar stimmt in Farbe und Motiv.

**Ehrlich benannt:** dieser Vorschlag **ändert F-78s Farbentscheidung für die Trolle** (weiß-gold →
grün-schwarz-gold), weil keine weiße Burg übrig bleibt, sobald `burg_03` bei den Elfen sitzt
(„Sternenwacht“ und ein Sternenwappen gehören zusammen). **Alternative, wenn weiß-gold bleiben soll:**
Trolle `burg_03` + `wappen_01`, Elfen `burg_06` + `wappen_09`, Gnome `burg_05` + `wappen_05`. Dann
verliert der Limbus sein schwebendes Bild — die Gnome sitzen dann in einer Baumfeste.

**Nicht verwendet bleiben:** `wappen_03` (Hirsch), `wappen_06` (Schwerter), `wappen_07` (Lebensbaum),
`wappen_08` (Drache, rot/schwarz). Der Drache ist die Rückfalllösung, wenn die Trolle ein Kampfwappen
statt des Wolfs bekommen sollen.

## 6. Nebenbefund: ein gelieferter Elfen-Wappen liegt ungenutzt

`assets/wappen/elfen_wappen.png` (1.520.769 Byte, aus der Meshy-Lieferung vom 12.11.,
`tools/setze_meshy_1zu1.py`) samt `_128` und `_64` — **kein Treffer in `src/` oder `data/`**: das Bild
wird im Spiel nirgends gezeichnet. Es zeigt Stern, silbernes Blatt, Goldranken und blaue Edelsteine
(`docs/eingaenge/MESHY_20261112_BILDASSETS/BELEGE.md`). Wenn es der Elfen-Wappen werden soll, gehört es
als `wappen` des Hauses Sternenwacht in `data/bot_wappen.json` — dann ist `wappen_09` frei.

## 7. Was hier NICHT entschieden ist

- Ob die Häuserfarben überhaupt nachgezogen werden (F-78 sagt ja — aber die Zeilen sind Daniels Text).
- Ob die Trolle weiß-gold behalten (dann Alternative aus Abschnitt 5) oder grün-schwarz-gold bekommen.
- Ob das Meshy-Elfenwappen das Paar ersetzt.

**Vorschlag zum Ablauf:** erst der Spaltenfehler (F-89 — er ist ein Fehler, keine Gestaltung), dann
diese Tabelle als **ein** Durchgang in `data/bot_wappen.json` und `FRAKTIONEN_WELTEN.md`, dann ein
Bildschirmfoto der Weltkarte mit allen sechs Paaren als Beleg.
