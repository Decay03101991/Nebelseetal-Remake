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
