# Recherche: vergleichbare Spielmechaniken und was wir daraus lernen (05.11.2026)

**Auftrag (Daniel, 05.11.2026, sinngemaess):** unsere genutzten Spielmechaniken sehr genau
formulieren, nach vergleichbaren, schon existierenden Mechaniken suchen, alle hilfreichen Tipps
sammeln - und dabei pruefen, ob eine Uebernahme das Spiel kaputt machen koennte. Nichts davon wird
ohne Pruefung gebaut; dieses Dokument ist **Theorie und Vorschlag**, kein Code.

**Methode.** Zuerst die EIGENEN Mechaniken aus dem Code und den Datendateien formulieren (mit Ort),
dann die naechste Gattung (Browsergame-Raubzug) und die naechste Nachbarschaft (Raid-/Boss-Design,
Bot-Entscheidung) lesen, dann je Befund: Quelle, was wir daraus lernen, Risiko, Empfehlung.
**Grenze der Quellen:** Suchtreffer sind Kurzfassungen und Forenbeitraege, keine Primärquellen des
Originalspiels. Alles, was das ORIGINAL regelt, bleibt bei `docs/PRUEFREGEL_ORIGINAL.md`; dieses
Dokument ergaenzt nur Remake-Entscheidungen und Mechanik-Ideen.

## 1. Unsere Mechaniken - genau formuliert

| Mechanik | Wie sie bei uns genau funktioniert | Ort |
|---|---|---|
| Angriff mit Marsch | Jeder Angriff ist ein Auftrag mit Reisezeit; gekaempft wird bei Ankunft, gebucht bei Heimkehr | `GameState._angriff_auftrag_starten`, `auftraege.*` |
| Vorrunde gegen Schwellen | Fusstruppen-Schlagkraft gegen eine Schwelle, Belagerung gegen eine zweite; reicht es nicht, zieht die Truppe ab, ohne zu kaempfen | `kampf.fuehre_schlacht(..., schwellen=)` |
| Wall | Stufe 1-8 mit belegten Schwellen, Zustand in Prozent, Belagerung richtet Mauerschaden an | `gebaeude_wirkung.wall_schwelle`, `kampf.py` |
| Drachen (W-14) | Kein Wall: eigene Schwellen 700/950, unbrechbar, Feueratem 8 Prozent der Fusstruppen vor dem Nahkampf, Wache 204 Mann und **bleibt beschaedigt stehen** | `src/drachen.py`, `GameState._drachen_kampf` |
| Beute | Nur bei Sieg; Anteil nach zerstoerten Verteidigern, letzter Schlag +10 Prozent; **gedeckelt durch die Karrenladung**; was nicht passt, bleibt im Hort | `drachen.beute_anteil`, `kampfbericht.beute_am_ziel` |
| Transport | Der Bedarf wird VOR dem Angriff vorgerechnet (Ladung und Wagenpark), Wagenbau-Bonus zaehlt | `drachen.transport_bedarf`, `transport_text` |
| Aufklaerung | Spionage zeigt Wall, Taktik, Truppen, Vorraete - beim Drachen AUSDRUECKLICH nicht; genaue Zahlen nur mit Ueberlebenden im Bericht | `drachen.spionage_erlaubt`, `drachen.bericht` |
| Weltzustand, oeffentlich | Ein Flammenzeichen unter dem Drachen sagt NUR, dass schon jemand angegriffen hat; es verschwindet, wenn der Hort leer ist | `GameState.drachen_angegriffen`, `_drachen_zeichnen` |
| Ruine | Nach dem Sieg: keine zweite Schlacht, aber pluenderbar; danach gesperrte Koordinate fuer alle | `_drachen_ruine_pluendern`, `drachen_blockiert` |
| Belohnung | 4000 Mana plus gerechneter Aufwand (Versuche x Spruenge x echter Preis eines Weltensprungs) | `drachen.belohnung_mana` |
| Bot-Urteil | Der Bot vergleicht seine Schlagkraft mit den Schwellen MAL Sicherheitsmarge und nennt Bonus und erwartete Verluste; die tatsaechliche Staerke sieht er erst im Angriff | `drachen.bot_entscheidung`, `_bots_drachenzug` |
| Punkte und Gesamtsieg | Kriegspunkte je Einheit; Gesamtsieg, wenn alle Doerfer aller Bots einmal ausgeraeumt sind, danach Endlosspiel | `punkte.py`, Register 197/198 |

## 2. Vergleichbare Mechaniken - und was daraus folgt

| # | Fremde Mechanik (Quelle) | Was sie macht | Was wir daraus lernen | Risiko bei uns | Empfehlung |
|---|---|---|---|---|---|
| 1 | Tragekapazitaet als Beutegrenze (Die Staemme Wiki: Farmen; Travian Wiki: Bounty) | Nur Ueberlebende tragen; was nicht passt, bleibt | Wir machen es schon so - und das ist Gattungsstandard, kein Zufall | keins | **bestaetigt**, nichts aendern |
| 2 | Versteck/Cranny schuetzt einen festen Betrag vor Pluenderung (Die Staemme, Travian) | Der Verteidiger hat immer einen geschuetzten Sockel | Ein Drache braucht das NICHT, ein Bot-Dorf schon: heute verliert ein Bot alles | mittel (neue Gebaeudewirkung, Balance) | **nur Idee**, eigenes Register, erst nach Balancing-Messung |
| 3 | Beute verfaellt, wenn das Lager voll ist (Travian: Bounty) | Ueberschuss ist weg | Bei uns gibt es keine Lagerkapazitaet - Beute kommt immer an. Wer sie einfuehrt, muss die Beute-Zusage neu pruefen | hoch (beruehrt jede Beute-Buchung) | **nicht uebernehmen**, nur notieren |
| 4 | Raubzug gegen Normalangriff: Rammen beschaedigen Waende NUR im Normalangriff (Travian/Siegewise) | Zwei Angriffsarten mit unterschiedlichem Risiko | Wir haben EINE Angriffsart; eine zweite (Raubzug ohne Mauerschaden, weniger Beute) waere eine echte Bereicherung | mittel (zweiter Pfad = zweite Regel) | **spaeter pruefen**, braucht eine Entscheidung |
| 5 | Phasenwechsel bei Lebensschwellen (D&D-/Raid-Design) | Der Boss wechselt bei 50 Prozent in eine zweite Phase | Ein Drachenkampf hat heute EINE Phase. Eine zweite Phase (Feueratem haerter, Wache sammelt sich) macht den Kampf erzaehlerisch staerker | mittel (Kampfregel) | **Vorschlag** mit Zahlenvorschlag, Entscheidung Daniel |
| 6 | Schaden bleibt, bis der Boss voll regeneriert; dann Reset (Browsergame-Raid) | Halbtote Bosse bleiben kein Dauerzustand | Unser Drache bleibt dauerhaft beschaedigt. Eine langsame Regeneration in SPIELTAGEN wuerde ihn lebendig halten | mittel (Zustandslogik) | **Vorschlag**: Block `regeneration` in den Daten, AUS per Vorgabe |
| 7 | Weltboss respawnt und wird staerker (Diablo-4-Forum) | Inhalt bleibt nach dem Sieg nutzbar | Nach dem Sieg haben wir eine Ruine - gut fuer die Karte, aber der Inhalt ist zu Ende. Ein erneutes Erwachen nach N Spieltagen an NEUER Koordinate passt zu `drachen.verteile` | mittel | **Vorschlag**, an Daniels Entscheidung gebunden |
| 8 | Belohnung nach Beitrag, nicht nach letztem Treffer (Raid-Loot-Diskussion) | Wer mitschiesst, bekommt seinen Anteil; Sterben senkt den Anteil | Genau unsere Variante A. Der Anti-Jackpot-Gedanke (kein Alles-fuer-den-letzten-Schlag) ist Standard | keins | **bestaetigt** |
| 9 | Mechaniken klar ankuendigen (Raid-Design-Grundsaetze: telegraphed mechanics) | Der Spieler erkennt Regeln, bevor sie ihn treffen | Unsere Hinweise (`angriffshinweis`, Transport-Text, Flamme) sind genau das. Die Schwelle bleibt trotzdem eine Erfahrung - der Rueckzug kostet keine Truppen | keins | **bestaetigt**, Hinweise nicht kuerzen |
| 10 | Eintrittsschwelle ueber Kampfwert (Browsergame-Raid: Entry nach Schaden) | Man kommt nur mit genug Kraft hinein | Unsere 700/950 sind eine solche Schwelle. Gattungslehre: die Schwelle muss durch Ausprobieren erkennbar sein, nicht durch ein Wiki | keins | **bestaetigt** (Daniel will kein Ausspaehen) |
| 11 | Farm-Effizienz je Reisezeit und Tragekapazitaet (Die Staemme: Farmranking) | Ertrag pro Stunde entscheidet, welche Einheit farmt | Wir rechnen den Transportbedarf bereits; eine Ertrags-Anzeige (Beute je Spielstunde) waere eine reine Anzeige-Hilfe | niedrig | **Vorschlag** (Anzeige, kein Kern) |
| 12 | Utility-AI: Aktionen bewerten, Ziel je Ziel bewerten, weiche Kennlinien (Game AI Pro 3, Kap. 13; gdad.wiki) | Der Agent punktet jede Moeglichkeit und nimmt die beste; Kennlinien statt harter Schwellen | Unser Bot-Urteil ist eine harte Schwelle MAL Faktor. Eine Kennlinie (Nutzen steigt mit Armee und Belohnung, sinkt mit erwarteten Verlusten) waere glaubwuerdiger | niedrig (nur Bot-Verhalten) | **Vorschlag**: Erwartungswert-Formel im Bot-Urteil, AUS per Vorgabe |
| 13 | Erwartungswert statt Sieggarantie (Utility-/Entscheidungstheorie) | Bei Unsicherheit nach Erwartungswert entscheiden | Der Bot kennt die Wache nicht - er sollte mit erwarteten Verlusten rechnen, nicht mit einer Garantie | niedrig | wie 12 |
| 14 | Aufklaerung als eigene Ressource (Spaeher-Einheiten in Die Staemme/Travian) | Wer spaeht, weiss mehr | Wir haben Spionage - nur beim Drachen absichtlich nicht. Das ist eine bewusste Remake-Entscheidung, keine Luecke | keins | **bestaetigt** (Register 203) |

## 3. Die drei Vorschlaege, die wirklich lohnen (in dieser Reihenfolge)

1. **Bot-Urteil als Erwartungswert (Nr. 12/13).** Nur Bot-Verhalten, kein Kern. Rechnung:
   Nutzen = Manabelohnung + Hortwert, Kosten = erwartete Verluste x Einheitenwert; der Bot greift,
   wenn Nutzen/Kosten ueber einem Faktor aus der Datendatei liegt. Damit versteht ein Bot einen
   BESCHAEDIGTEN Drachen besser (weniger Wache = weniger erwartete Verluste), ohne die Wache zu
   kennen - er kennt nur das Flammenzeichen. **Risiko:** niedrig, weil nur Bot-Entscheidung.
2. **Zweite Phase im Drachenkampf (Nr. 5).** Unter 50 Prozent Wache wird der Feueratem staerker
   (8 auf 12 Prozent) und der Bericht nennt den Umschwung. **Risiko:** mittel, weil es die
   Kampfregel beruehrt; braucht eine eigene Wache und eine Balancing-Messung (wie viele Truppen
   sind noetig, um beide Phasen zu ueberstehen).
3. **Regeneration in Spieltagen (Nr. 6) oder erneutes Erwachen (Nr. 7).** Beides haelt den Drachen
   nach dem ersten Sieg relevant. **Risiko:** mittel; die Regeneration ist die kleinere Aenderung
   (ein Block in den Daten, ein Aufruf im Takt), das Erwachen die groessere (Zustand zuruecksetzen,
   neue Koordinate, neuer Hort).

## 4. Was wir ausdruecklich NICHT uebernehmen

- **Lagerkapazitaet und Beuteverfall (Nr. 3):** beruehrt jede Beute-Buchung und die Zusage, dass
  Beute ankommt. Nutzen klein, Risiko gross.
- **Versteck fuer den Drachen (Nr. 2, beim Drachen):** ein Drache mit geschuetztem Sockel widerspricht
  dem Hort-Gedanken (wer plaendert, nimmt mit, was die Karren tragen).
- **Spionage beim Drachen:** Daniels Entscheidung (Register 203) - bleibt.

## 5. Quellen (gelesen am 05.11.2026)

- Die Staemme Wiki, Farmen: `https://help.die-staemme.de/wiki/Farmen` (Tragekapazitaet, Versteck,
  Farmranking je Einheit).
- Siegewise, Rams and walls: `https://siegewise.com/en/travian/wiki/rams` (Rammen nur im
  Normalangriff, Wall als Grundwert plus Prozent).
- Travian Wiki, Bounty: `https://travian.fandom.com/wiki/Bounty` (Tragekapazitaet, Verfall bei
  vollem Lager, Cranny).
- Browsermmorpg, Raid-Phase-1: `https://browsermmorpg.com/articles/raid-phase-1-upgrade--880`
  (Schaden bleibt bis zur vollen Regeneration, dann Reset).
- Diablo-4-Forum, Weltboss-Vorschlag: `https://us.forums.blizzard.com/en/d4/t/...` (Respawn und
  staerker werden).
- Cubold Gaming, D&D-Boss-Design: `https://cuboldgaming.com/blogs/gaming/d-d-boss-fight-design-...`
  (Phasenwechsel an Schwellen).
- Design The Game, Raid-Mechaniken: `https://designthegame.com/learning/tutorial/the-power-raid-mechanics-mobile-video-games`
  (klare, angekuendigte Mechaniken; skalierbare Schwierigkeit).
- Game AI Pro 3, Kap. 13 (Utility-Considerations): `http://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter13_Choosing_Effective_Utility-Based_Considerations.pdf`
- gdad.wiki, Utility AI: `https://gdad.wiki/wiki/programming/game-ai/utility-ai` (Aktionen bewerten,
  Ziel je Ziel, Kennlinien).

**Urteil je Quelle:** alle zehn sind SEKUNDAERquellen (Wiki, Forum, Fachartikel). Fuer das Original
2009/2006 gilt weiter ausschliesslich `docs/original/` und `docs/PRUEFREGEL_ORIGINAL.md`.
