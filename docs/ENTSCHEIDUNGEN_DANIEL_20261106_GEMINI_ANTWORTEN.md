# Entscheidungen Daniel - Gemini-Antworten, Runde 2 (06.11.2026)

**Form:** zwei Blaetter derselben Runde (neun Fragen), nachdem die fuenf Gemini-Antworten vorlagen.
Antworten **woertlich**, je mit Folge. Runde 1 (zum Gemini-Input) steht in
`docs/ENTSCHEIDUNGEN_DANIEL_20261106_GEMINI.md`.

| Nr. | Frage | Antwort (woertlich) | Folge |
|---|---|---|---|
| 1 | Ruhm-Raenge: Schwellen 0 / 2.500 / 10.000 (Gemini, erfunden) | "A (Empfehlung): ich lege dir die Schwellen aus unseren eigenen Zahlen vor (die vier Spieltest-Laeufe endeten bei 19 bis 40 Punkten nach 8 bis 12 Tagen) - keine erfundene Zahl" | Keine fremde Schwelle. Die Sitzung rechnet eine Staffel aus unseren Punktzahlen und legt sie vor; bis zur Bestaetigung zeigt der Balken nur den Abstand zur naechsten Auszeichnung, ohne Rangnamen. |
| 2 | Mauerreparatur: Preis je Prozentpunkt | "A (Empfehlung): ich rechne den Preis je Prozentpunkt aus dem EINEN belegten Wall-Preis (16 Holz/16 Stein) und der Stufe, lege dir die Tabelle vor, du bestaetigst" | Preistabelle je Stufe 1 bis 10 aus 16/16 wird gerechnet und vorgelegt; VOR dem Einbau bestaetigen lassen. |
| 3 | Verwundetenheilung: Preis und Dauer | "Nach Empfehlung aber beachte dabei ob gemini die einheiten werte alle hatte und wirklich alle infos hatte damit sein vorschlag konsistenz hat, wenn ja dann sollten wir es so machen" | **Gemessen: Gemini hatte die Werte NICHT** (verweist auf `data/kaserne.json`, die es nicht gibt) und Einheiten kosten bei uns NICHT einheitlich Gold (Kaempfer 175 Gold, Buergerwehr 100 Nahrung + 50 Leder + 50 Wolle, Krieger 350 Gold + 1 Pferd, dazu Ausruestung). Deshalb Frage 6: Regel auf alle Kostenposten uebertragen, danach bestaetigt. |
| 4 | Postfach-Ablauf | "A (Empfehlung): 1 Spieltag fuer Berichte, Militaerberichte (Kampf, Gesamtsieg) nie loeschen, ungelesene Verlustberichte verschieben sich automatisch" | Frist 1 Spieltag (28.800 Spielsekunden) fuer Spionage, Diebstahl, Portal, Diplomatie, System; kampf und gesamtsieg ohne Ablauf; ungelesene Verlustberichte verschieben sich. |
| 5 | Diplomatie-Vertraege (NAP) | "A (Empfehlung): NAP blockiert Angriffe des Bots, laeuft 3 Spieltage, bricht automatisch wenn die Gunst unter 40 faellt - kein Kuendigungsknopf" | Laufzeit 3 Spieltage, automatischer Bruch unter Gunst 40, kein Kuendigungsknopf. |
| 6 | Heilungskosten nach der Messung | "A (Empfehlung): 75 % aller Kostenposten der Einheit (Gold, Nahrung, Leder, Wolle, Pferde - was sie eben kostet), KEINE Ausruestung, halbe Ausbildungsdauer" | Heilung = 75 Prozent der `kosten` der Einheit (alle Posten, ohne `waren`), Dauer 50 Prozent von `dauer_je`. Deckel und Rundung werden gerechnet, nicht geschaetzt. |
| 7 | Diplomatie-Events: Zahlen | "A (Empfehlung): aus unseren Preisen ableiten (Tribut ≈ Tagesproduktion eines mittleren Dorfes, Werkzeuge gegen Eisen nach Warenwert) und dir die Zahlen vorlegen" | Keine fremden Zahlen. Ableitung aus Tagesproduktion und Warenwerten, Tabelle vor dem Einbau vorlegen. |
| 8 | Siedlungsumzug | "B: Gebaeude bleiben erhalten (ziehen mit um) - Umzug wird zum bequemen Weltensprung, dafuer viel teurer" | **Abweichend von Gemini (der Verlust aller Gebaeude vorschlug).** Gebaeude UND Ausbaustufen ziehen mit; dafuer muss der Umzug deutlich teurer werden - Preis wird gerechnet und vorgelegt. Die halbe Siedler-Regel (5 Siedler) steht damit nicht mehr fest und ist mit dem Preis neu zu bestimmen. |
| 9 | Rache-Angriff: Schwelle | "A (Empfehlung): ich leite die Schwelle aus unseren Werten ab (Schlagkraft einer mittleren Verteidigung) und lege sie dir vor - keine fremde Zahl" | Schwelle aus `bot_angriffsplanung.schlagkraft` und einer mittleren Verteidigung ableiten, vorlegen, dann einbauen. |

**Was daraus fuer den Einbau folgt (noch vor dem Bau vorzulegen):** drei gerechnete Tabellen -
Reparaturpreis je Wallstufe, Heilungspreis je Einheit, Event-Zahlen - und zwei abgeleitete Schwellen
(Ruhm-Raenge, Rache-Angriff). **Ohne diese Vorlage wird keines der fuenf Stuecke gebaut.**

## Runde 3 - der Nachtauftrag (06.11.2026, 02:16 bis 02:25)

Gefragt wurde sieben Punkte; Daniel geht schlafen und ist ab **07:55** wieder am Laptop.

| Nr. | Frage | Antwort (woertlich) | Folge |
|---|---|---|---|
| 1 | Portal-Geschichte: Wirkung der zwei Antworten? | "A (Empfehlung): keine Wirkung - reiner Text, keine Knoepfe, damit sofort in S1b baubar" | Story erscheint als Text ohne Antwortknoepfe. |
| 2 | Durchmarschrecht: Mechanik? | "A (Empfehlung): reine Anzeige - das Recht steht im Vertrag, hat aber keine Mechanik (ehrlich dokumentiert)" | Vertrag wird gefuehrt und angezeigt; in `kampfbericht`/Doku als "ohne Mechanik" ausgewiesen. Keine erfundene Wirkung. |
| 3 | Ruhm-Raenge ohne Daniel | "A (Empfehlung): aus unseren Spieltest-Zahlen ableiten (12 Tage ≈ 40 Punkte) und als VORSCHLAG sofort nutzen, Namen aenderbar" | Vier Stufen aus der Messung, im Register als VORSCHLAG. |
| 4 | Modellbudget der Nacht | **"B: hoechstens 4,00 USD - mehr Modellhilfe, mehr Risiko"** | Obergrenze 4,00 USD, je Aufruf hoechstens 0,25 USD, Kontostand vor und nach jeder Runde messen. |
| 5 | Wie weit in der Nacht? | "A (Empfehlung): so weit wie moeglich, Mindestziel S1 + S1b + S2; wenn Zeit bleibt weiter bis S3/S4; S5 nur wenn alles gruen ist" | Mindestziel **S1, S1b, S2**; danach S3, dann S4; S5 gesperrt (siehe 7). |
| 6 | Behaelt eine geheilte Einheit ihre Ausruestung? | "A (Empfehlung): ja, sie behaelt ihre Ausruestung - sonst waere Heilung fast wertlos, und die Waffe bleibt am Soldaten" | Heilung kostet 75 Prozent der `kosten`, NICHT die `waren`. |
| 7 | S5 (Siedlungsumzug) in der Nacht? | "A (Empfehlung): S5 heute Nacht NICHT bauen ... erst nach deinem Aufwachen" | S5 bleibt liegen; wird nach dem Aufwachen vorgelegt. |

**Zusaetzlich pauschal freigegeben (Daniel, 02:16):** die Skill-Freigabe fuer die naechste Sitzung gilt
**pauschal** - die vier vorgemerkten Ergaenzungen duerfen ohne Rueckfrage gespeichert werden
(`9a7f3335`, `5797a0fc`, `9120cc35`, `36452699`), jede mit Zeile im `SKILL_UND_REGEL_PROTOKOLL.md`.
