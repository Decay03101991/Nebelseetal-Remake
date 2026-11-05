# Fragen an Daniel — gesammelt in der Sitzung ab 05.11.2026, 03:34

> Regel dieser Sitzung: Fragen werden **gesammelt**, nicht einzeln gestellt (Daniel schläft bis
> 07:55). Jede Frage nennt Messlage, Möglichkeiten mit Folge und eine Empfehlung zuerst.
> Bis zur Antwort gilt der dokumentierte Stand als VORSCHLAG.

## 1. Bots und geplünderte Ruinen

**Messlage:** `drachen_blockiert` sperrt die Koordinate nach dem Plündern; Bots räumen heute nur
lebende Drachen aus (`_bots_drachenzug`), keine Ruinen.
**a) Ja, Bots räumen auch Ruinen aus** (Empfehlung) — mit Karren, ohne Kampf, kleiner Schritt.
**b) Nein, Ruinen bleiben dem Spieler** — die Beute ist dann reines Spielerglück.
**Folge von a:** mehr Bot-Bewegung auf der Karte, Ruinen verschwinden schneller.

## 2. Zweite Kampfphase im Drachenkampf

**Messlage:** Feueratem bucht heute einmal je Gefecht (8 %). Eine zweite Phase „unter 50 % Wache
wird der Atem härter“ wäre ein Eingriff in `kampf.fuehre_schlacht`.
**a) Erst nach einer Balancing-Messung entscheiden** (Empfehlung) — die Messung liegt jetzt vor.
**b) Sofort einbauen** — ohne Messung rate ich die Schwelle.

**Messlage (05.11.2026, W-17, `tools/drachen_balancing.py`, 100 Läufe je Zelle):** Die Schwellen
gelten für **Schlagkraft**: 700 SK = **234 Krieger**, 950 SK = **22 Katapulte**. Genau dort passiert
das Entscheidende: **234 Krieger + 22 Katapulte gewinnen 0 von 100 Läufen**, weil der Feueratem
(8 % = 19 Krieger) die Truppe unter die Schwelle drückt, bevor die Vorrunde prüft — es kommt gar
nicht zum Kampf. **Sicherer Sieg ab 300 Kriegern + 22 Katapulten**, eigene Verluste dann rund 162
von 322 (50 %). Mit **12 % Atem** statt 8 %: bei 400 Kriegern 155 statt 154 eigene Verluste —
also **etwa eine Einheit Unterschied**. Folge für die Entscheidung: eine zweite Phase mit 12 %
ist Erzählung, keine Balance-Änderung. Sie würde erst spürbar, wenn sie **die Vorrunde kippt**
(Atem über der Schwelle) oder deutlich härter brennt (z. B. 20 % unter halber Wache).

## 3. Drache: Regeneration oder erneutes Erwachen

**Messlage:** nach dem Sieg bleibt eine Ruine, der Drache wächst nicht nach.
**a) Regeneration in Spieltagen** (Empfehlung) — kleiner Eingriff, der Hort füllt sich langsam.
**b) Erneutes Erwachen nach N Tagen** — größerer Eingriff (neuer Drache, neue Wache).

## 4. Protokoll verdichten

**Messlage:** `docs/ENTWICKLUNGSPROTOKOLL.md` hat 333 Zeilen; Ziel war unter 320. Die Verdichtung
löscht keine Ereignisse, sie fasst nur Zusammenfassungen zusammen.
**a) Bei der nächsten Übergabe verdichten** (Empfehlung) — ein Schnitt, dokumentiert.
**b) So lassen** — das Protokoll wächst weiter.

## 5. Versteck/Cranny für Bot-Dörfer (Recherche Nr. 2)

**Messlage:** die Recherche vom 05.11. nennt es als mögliche Mechanik; heute gibt es keine
Verstecke.
**a) Später, als eigenes Register** (Empfehlung) — eigener Schnitt mit eigener Wache.
**b) Jetzt mitnehmen** — würde W-15/Drachenschuppe überholen.

## 6. Hausfarben und Wappentinkturen passen nicht zusammen (neu, aus W-15)

**Messlage:** Die Chronik nennt je Haus Farben (Menschen „Blau und Silber“, Zwerge „Schwarz und
Gold“, Elfen „Silber und Grün“, Trolle „Dunkelrot und Schwarz“, Ghule „Grün und Knochenweiß“,
Gnome „Bunt und Grau“). Die **gelieferten Wappenbilder** führen andere Tinkturen: Silberbach
Weinrot/Gold, Hammerhall Nachtblau/Grau/Gold, Sternenwacht Dunkelgrün/Gold, Schattenfaust
Violett/Schwarz/Gold, Knochenmoor Blau/Silber/Gold, Flickwerk Karminrot/Silber/Gold. Beides steht
jetzt offen im Text („Die Farben des Hauses sind Blau und Silber. Das Wappen führt Weinrot und
Gold …“) — nichts wurde stillschweigend geändert.
**a) Hausfarben an die Wappen angleichen** (Empfehlung) — sechs Zeilen in Chronik und
`data/haeuser.json`, danach stimmt, was der Spieler sieht.
**b) Hausfarben behalten, Unterschied stehen lassen** — heraldisch möglich (Tracht ≠ Schild), aber
erklärungsbedürftig.
**c) Wappen neu zuordnen, sodass sie zu den Farben passen** — größerer Eingriff, zehn Bilder
vorhanden; würde den Ringtausch vom 04.11. wieder umwerfen.

## 7. Drachenschuppe: wohin mit der Trophäe (neu)

**Messlage:** Daniel will die Schuppe als „eigene Auszeichnung, zählt am Ende nur als Trophäe“.
Offen ist, **wo** sie liegt: eigenes Lagerfach (Handel möglich oder nicht?) und ob sie im
Punktestand auftaucht.
**a) Eigenes Lagerfach, nicht handelbar, zählt in keiner Formel** (Empfehlung) — reine Trophäe,
kein Wirtschaftsloch.
**b) Eigenes Lagerfach, handelbar** — dann bekommt sie einen Preis und wird zur Ware.
**c) Nur im Auszeichnungsverzeichnis, kein Lagerfach** — kleinster Eingriff, aber man sieht sie
nirgends im Lager.
