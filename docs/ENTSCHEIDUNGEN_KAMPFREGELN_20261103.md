# Entscheidungen: die acht Kampfregeln (Daniel, 03.11.2026, 22:1x)

**Grundlage:** `D:/Arbeiten/Hermes/Notizen/KAMPFREGELN_20261103.md` (Entwurf des starken Modells,
gegengelesen und berichtigt: statt der fremden Rohstoffe Lehm/Eisen/Getreide gelten die eigenen
Rohstoffe). Daniel hat die Liste in EINEM Durchgang abgesegnet und vier Zusatzfragen entschieden.

**Rang:** ABGESEGNET. Die Regeln gelten ab jetzt; gebaut wird in der Reihenfolge 1 bis 8.

## Die acht Regeln (abgesegnet)

| # | Kennung | Regel |
|---|---|---|
| 1 | `fusstruppen_begriff` | Fusstruppen sind alle NAHKAMPFeinheiten. Fernkaempfer, Belagerungswaffen und Karren zaehlen nicht zur Vorrunden-Schlagkraft; das Kampfende (alle Fusstruppen tot oder geflohen) tritt ein, sobald alle Nahkaempfer tot oder geflohen sind - auch wenn Fernkaempfer leben. |
| 2 | `flucht_formel` | Nach jeder Sequenz: ist die Zahl der einsatzfaehigen Nahkaempfer unter 50 Prozent des Schlachtbeginns, wuerfelt die Seite einmal 1-100; Erfolg bei kleiner/gleich 40 + 5 x Sequenznummer. Bei Erfolg flieht die GANZE Armee (Ausgang `flucht`), die Einheiten stehen danach wieder zur Verfuegung. |
| 3 | `beute_verteilung` | Beutesatz 100 Prozent (kein Verteidiger mehr), 60 (Wall bei 0), 30 (Wall beschaedigt), 10 (Wall heil); anteilig nach vorhandener Vorratsmenge, gedeckelt durch die Karrenladung. Verteidiger verliert genau die abtransportierte Menge. |
| 4 | `beute_reihenfolge` | Reicht die Ladung nicht fuer alle Anteile, wird in DIESER Reihenfolge entnommen: **Gold, Metall, Stein, Holz, Nahrung, Leder, Wolle, Pferde** (Daniel: Gold ist der gemessene Engpass). Pro Position der volle Anteil, bis die Restladung erschoepft ist. |
| 5 | `belagerungsturm_mauerschaden` | Belagerungsturm: Schadensbereich **1-4** minus Wallstufe (Katapult 2-13); je Turm einzeln gewuerfelt, positiver Rest geht vom Zustand ab. In der Vorrunde volle Belagerungs-SK. |
| 6 | `mauer_reparatur` | Aktive Reparatur durch den Verteidiger, **MIT BAUZEIT** (der Wall bleibt waehrend der Reparatur beschaedigt). 1 Prozentpunkt Zustand kostet 1 Prozent der Baukosten der aktuellen Wallstufe; keine automatische Reparatur. |
| 7 | `vorrunde_wiederholung` | Vorrunde genau EINMAL je Schlacht, vor der ersten Sequenz; bei Scheitern unentschieden und keine Beute. Innerhalb der Schlacht keine Wiederholung; beim naechsten Angriff mit dem dann aktuellen Wallzustand. Bei Zustand 0 Prozent gilt die Vorrunde als bestanden, wenn die Belagerungs-Mindestanforderung erfuellt ist. |
| 8 | `geraetebeute` | Karren und Belagerungswaffen werden **zerstoert, nicht erbeutet**: der Verlierer verliert 10 Prozent je verstrichener Sequenz (aufgerundet je Typ), hoechstens 50 Prozent. Bei Unentschieden bleibt alles erhalten. |

## Die vier Zusatzentscheidungen

| Frage | Entscheidung |
|---|---|
| Gesamtliste | **alle acht uebernehmen**, in der Reihenfolge 1 bis 8 bauen |
| Beute-Reihenfolge | **Gold zuerst**: Gold, Metall, Stein, Holz, Nahrung, Leder, Wolle, Pferde |
| Nah-/Fernkampf | **je Einheit ein Kennzeichen in `data/units.json`** ergaenzen - heute bildet `einheiten.ROLLEN` beide auf `kaempfer` ab, sie sind im Code nicht unterscheidbar |
| Mauerreparatur | **mit Bauzeit** (Wall bleibt waehrend der Reparatur beschaedigt) |

## Was der Bau braucht (Ist-Stand, gemessen 03.11.2026)

- **Regel 1:** neue Angabe je Einheit (`data/units.json`, Feld `kampfart` = `nah`/`fern`), gelesen an EINER
  Stelle (`einheiten.kampfart(name)`); Vorrunde und Kampfende lesen sie. Ohne sie ist die Regel nicht
  umsetzbar (belegt: `einheiten.ROLLEN` kennt nur `kaempfer`).
- **Regel 2:** neue Ausloese in `kampf.fuehre_schlacht` (nach jeder Sequenz), Ausgang `flucht` in
  `kampfbericht`; die 40 + 5 x Sequenz stammen aus dem Handbuch (S. 22), die 50-Prozent-Schwelle ist
  VORSCHLAG.
- **Regel 3:** ist gebaut (`kampfbericht.beute_staffel`) - bleibt, nur die Doku-Zusage festziehen.
- **Regel 4:** in `kampfbericht.beute_staffel` ersetzt die feste Reihenfolge die anteilige Kuerzung bei
  Ladungsknappheit; Test: kleine Ladung nimmt zuerst Gold.
- **Regel 5:** Schadensbereich fuer `Belagerungsturm` und `Grosser Belagerungsturm` aus `data/units.json`
  (heute tragen die Waffen einen Schadensbereich; pruefen, welchen der Turm hat).
- **Regel 6:** neue Spieleraktion am Wall (`dorfwall`): Reparaturauftrag mit Kosten (1 Prozent der
  Baukosten je Prozentpunkt) und **Bauzeit** in Spielstunden; der Wall bleibt bis zum Abschluss
  beschaedigt. Bots brauchen dieselbe Aktion, sonst sind sie schlechter als der Spieler.
- **Regel 7:** Zustand ist schon je Wall gefuehrt - pruefen, dass die Vorrunde genau einmal laeuft und mit
  dem Zustand VOR der Schlacht rechnet.
- **Regel 8:** Verlustrechnung beim Verlierer (10 Prozent je Sequenz, max. 50, je Typ aufgerundet);
  KEINE Erbeutung durch den Sieger.

**Der naechste Schritt nach dieser Datei:** S-8 Stufe 3 (Bauplan je Taktik in `data/bot_bauplan.json`,
Mindestzahlen + Restfelder) und danach die acht Regeln 1 bis 8 in genau dieser Reihenfolge - je Regel
Wache, Sammellauf, Registerzeile.
