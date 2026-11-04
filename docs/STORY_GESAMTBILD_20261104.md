# Die Geschichte des Nebelseetals — Gesamtbild zum Lesen

Stand 04.11.2026, für Daniel. Zweck: **eine stimmige Geschichte für das Spiel und für den Pre-Release**
— nicht nur für GitHub. Dieses Blatt trennt sauber, was aus dem **Original** stammt, was von **Daniel**
kommt, was ein **Agent erfunden** hat und was noch **offen** ist.

## 0. Lesehilfe: die vier Herkunftszeichen

| Zeichen | Bedeutung | Folge |
|---|---|---|
| **ORIGINAL** | steht so in einer Nebelseetal-Quelle, mit Datei und Zeile belegt | darf bleiben, ist Anker |
| **DANIEL** | deine eigene Ansage oder Entscheidung, mit Datum | gilt, wird nicht überschrieben |
| **ENTWURF** | vom Agenten geschrieben, ohne Quelle — austauschbar | darf ersetzt werden, ohne dass Spielregeln brechen |
| **VORSCHLAG** | bewusst offen, wartet auf deine Entscheidung | steht so in den Datendateien, nicht im Code |

---

## 1. Was heute im Spiel steht (wörtlich, zum Lesen)

### 1.1 Ankunft im Nebelseetal — das Intro (vier Absätze, einmalig nach dem Passworttor)

> **Die Welt ist zersprungen, und keiner weiß mehr genau, warum. Sechs Bruchstücke treiben im Limbus: Midgard, Valhalla, Utgard, Armageddon, Ragnarök — und dazwischen der Limbus selbst.**
>
> **Du hast zehn Siedler, zwei Werkzeugkisten und ein Feld, das dir niemand streitig macht. Noch nicht.**
>
> **Fünf Nachbarn haben es längst versucht: Haug raubt, Brynhild wacht, Grom baut, Silra späht, Krank vergisst nichts.**
>
> **Baue etwas, das bleibt — und finde heraus, was hinter dem Nebel liegt.**

Herkunft: die **sechs Weltnamen** sind ORIGINAL (alte Website, `data/welten.json` mit Belegvermerk), die
**fünf Botnamen** sind ENTWURF des Agenten (keine Quelle im Handbuch, keine Ansage von dir), die
**zwei Werkzeugkisten** sind ENTWURF (kommen nur in `data/story.json` vor), der **Ton** ist DANIEL
(04.11.2026: abenteuerlich und leicht).

### 1.2 Die Chronik — sieben Kapitel, wachsen mit dem Fortschritt

| Stufe | Titel | Text | Bedingung im Spiel |
|---|---|---|---|
| 0 | Ankunft | Zehn Siedler, zwei Werkzeugkisten, ein Fleck Land. Der Anfang jeder Geschichte ist eine Liste von Dingen, die fehlen. | immer |
| 1 | Die erste Siedlung | Ein Dach, ein Brunnen, ein Feuer. Zum ersten Mal riecht es hier nach Arbeit statt nach Nebel. | mindestens eine Siedlung |
| 2 | Werkstatt und Handel | Aus Rohstoffen werden Waren, aus Waren wird Handel. Der erste Karren quietscht so laut, dass die Nachbarn ihn hören können. | eine Ware hergestellt oder eine Werkstatt gebaut |
| 3 | Wissen | Die Bibliothek ist mehr Regal als Wissen — aber das erste Kapitel ist geschrieben. | eine Forschung abgeschlossen |
| 4 | Der erste Kampf | Es gibt Tage, an denen man Mauern baut, und Tage, an denen man sie braucht. Dieser Tag war der zweite. | ein Kampf gefochten |
| 5 | Ein zweites Dorf | Ein Dorf ist ein Zuhause. Zwei Dörfer sind der Anfang von etwas Größerem. | mindestens zwei Siedlungen |
| 6 | Durch das Portal | Das Portal summt, als hätte es gewartet. Dahinter liegt eine zweite Welt — und in jeder Welt wohnt jemand, der schon länger hier ist. | zwei eigene Welten (Portal benutzt) |

Herkunft: **alles ENTWURF** (Agent, 04.11.2026). Die Bedingungen spiegeln die gebauten Spielschritte
wider — das ist stimmig, der Wortlaut ist frei.

### 1.3 Der Ausgang — Sieg und Niederlage

> **Sieg — Das Nebelseetal hat einen Namen bekommen:** Deine Siedlungen stehen, deine Nachbarn kennen deinen Namen, und die Karten tragen deine Grenzen. Die Welt ist immer noch zersprungen — aber sie ist jetzt auch ein bisschen deine.
>
> **Niederlage — Der Nebel holt sich zurück, was er hergegeben hat:** Die letzten Siedler packen, was sie tragen können. Irgendwo im Limbus fängt jemand anderes mit zehn Siedlern und zwei Werkzeugkisten an — so funktioniert diese Welt.

Herkunft: **ENTWURF** (Agent). **Achtung — hier steht die größte Unstimmigkeit des ganzen Spiels, siehe
Abschnitt 4, Punkt 1.**

### 1.4 Die fünf Nachbarn — sie sprechen seit Story 2 (je ein Beispiel)

| Bot | Herkunft im Spiel | Beispielsatz (Angriff) |
|---|---|---|
| Haug | menschlich, raubt | Haug kommt mit Karren, die schon leer sind. „Wir helfen nur beim Ausmisten“, ruft er. |
| Brynhild | menschlich, wacht | Brynhild kommt leise und bleibt am Rand. „Ihr habt eine Wahl“, sagt sie, „und ich habe Zeit.“ |
| Grom | zwergisch, baut | Grom kommt mit Werkzeug statt mit Waffen. „Ich baue euch um“, knurrt er. |
| Silra | elfisch, späht | Silra ist schon da, als alle noch suchen. „Ihr habt einen Späher überhört“, flüstert sie. |
| Krank | Trolle, vergisst nichts | Krank sagt nichts. Krank erinnert sich nur. |

Herkunft: **Namen ENTWURF**, **Rollen aus dem Code** (`bottaktik.py`, Taktikprofile), **40 Sätze
ENTWURF** (Story 2, 04.11.2026, nach deinem Ton). Keiner der fünf hat eine **Vorgeschichte** oder ein
**Ziel** — sie greifen an, gründen, rauben, und man weiß nicht, warum.

### 1.5 Die sechs Welten (Namen ORIGINAL, Zuordnung Fraktion → Welt VORSCHLAG)

| Welt | Fraktion mit Heimat dort | Begründung in der Datei |
|---|---|---|
| Armageddon (01) | zwergisch | Fels- und Aschewelt, passt zum Steinbau |
| Ragnarök (02) | Ghule | Welt des Untergangs und der Untoten |
| Utgard (03) | Trolle | Außenwelt der Riesen und Trolle |
| Midgard (04) | menschlich | Welt der Menschen, zugleich Startwelt |
| Valhalla (05) | elfisch | Halle der Gefallenen, die Elfen sind die schnellsten Kämpfer |
| Limbus (06) | Gnome | Grenz- und Vorwelt, die Gnome arbeiten an den Rändern |

Herkunft: **Weltnamen ORIGINAL**, **Zuordnung Fraktion → Welt VORSCHLAG** (so in
`data/welt_fraktionen.json` vermerkt: weder Handbuch 2009 noch Vorversion 2006 nennt eine Welt je Volk).
**Es gibt für keine der sechs Welten eine Beschreibung im Spiel** — nur Name, Lage im Limbus-Raster und
die eine Zeile Begründung.

### 1.6 Die sechs Fraktionen

| Fraktion | Plus | Minus | Herkunft |
|---|---|---|---|
| menschlich | Holzertrag +5 % | Steinertrag −5 % | ORIGINAL-nah: `bottaktik.py`, seit 30.10.2026 belegt |
| zwergisch | Steinertrag +5 % | Holzertrag −5 % | dito |
| elfisch | Reisegeschwindigkeit +5 % | PA −5 % | dito |
| Trolle | AT +5 % | Handelserloes −5 % | dito (übernimmt das Paar der alten Fraktion monster) |
| Ghule | Nahrungsertrag +5 % | PA −5 % | **DANIEL** (03.11.2026) |
| Gnome | Ausbau +5 % | AT −5 % | **DANIEL** (03.11.2026) |

Dazu die Bilder: **je Fraktion eine Burg und ein Wappen** (`data/bot_wappen.json`) — die Bilder sind
deine Lieferung, die **Zuordnung Fraktion → Bild ist VORSCHLAG** des Agenten. Für zwei Fraktionen
(menschlich und zwergisch) ist die Zuordnung unglücklich: Haug und Brynhild sind beide menschlich und
tragen dadurch **dasselbe** Wappenpaar, obwohl sie verschiedene Nachbarn sind.

### 1.7 Der Rest des Spiels in einem Absatz

Sechs Siedlungen je Reich, zehn Siedler je Siedlung und fünf je Haus, sieben Geländearten (Grasland,
Steppe, Wald, Hügel, Berg, **Nebelsee**, Sumpf — Sumpf ist nicht bebaubar), neun Rohstoffe, 17 Waren,
28 Einheiten, 20 Gebäude, 21 Forschungen, Götterschutz mit Punktegrenze, vier Auszeichnungen statt eines
Sieges, Mana-Kosten je Entfernung im Portal, fünf Bots mit eigener Wirtschaft, Krieg und Gründung.

---

## 2. Die Originalgeschichte — was die Quelle wirklich erzählt

Quelle: `docs/original/website/hintergrundgeschichte.php`, `hintergrundgeschichte2.php`,
`hintergrundgeschichte3.php` (drei Seiten, vollständig vorliegend) und das Handbuch 2009.
Das ist der **echte** Hintergrund, den das Original mitgab — und er ist erzählerisch stärker als das,
was heute im Remake steht.

### 2.1 Erschaffung und Sündenfall

> Vor langer Zeit war die Welt eine Einheit. Erschaffen von den drei göttlichen Drachen: **Epheus der Weiße**, Herr des Wachstums und der Heilung; **Tardas der Grüne**, Herr der Maßlosigkeit und der List; **Salmur der Rote**, Herr des Hasses und der Furcht.

Eine friedliche Welt, in der viele Menschenvölker Handel trieben und ihre Schöpfer verehrten. Dann wurde
Salmur unzufrieden: alles war perfekt, es gab nichts mehr zu gestalten. **Er schenkte der Welt die
Magie** — eine Kraft, die bisher nur den Göttlichen offenstand. Die Bewohner versuchten, sie zu
beherrschen, und scheiterten, weil ihnen die Weisheit fehlte.

### 2.2 Der Bruch

> Das Nebelseetal verfiel immer mehr dem Chaos … die von den Drachen erschaffene Welt wurde durch die magischen Ströme zerrissen. Ganze Kontinente wurden von der Magie verschlungen, Hunderttausende starben, die Realitäten verschwammen und splitteten sich zu vielen Welten auf, welche nun, nur noch durch magische Korridore miteinander verbunden waren.

Nach Jahrtausenden glätteten sich die Ströme. Die Überlebenden bauten sich in den Bruchstücken eine neue
Heimat, und **die Völker selbst veränderten sich**: Menschen, Feen, Echsenwesen, Zwerge, Gnome, Elben,
Orks — viele sind mit der Magie verschmolzen.

### 2.3 Die Welt, in der gespielt wird

> Die magischen Ströme sind zur Ruhe gekommen, jedoch führen sie immer noch zu wunderlichen Dingen. Die Landschaft der Welten verändert sich ständig. Wo eben noch ein Bergmassiv aufragt, ist am nächsten Morgen vielleicht ein dichter Wald, oder ein stinkender Sumpf. … Sobald sie sich an einem Ort versammeln um dort einen neuen Lebensraum für sich zu schaffen und zu siedeln, hören die Veränderungen in der unmittelbaren Nähe auf.

Und weiter:

> Auf jedem einzelnen Bruchstück der alten Welt, die nun im magischen Raum, dem Limbus, verstreut liegen, entstand ein magisches Portal.

> Epheus jedoch weint immer noch und ab und zu fallen seine Tränen auf die Welten des Nebelseetals und lassen magische **Nebelseen** entstehen aus denen magische Energien strömen. Tardas kehrte aus seiner Abgeschiedenheit zurück, um sich wieder seinen Teil an der Welt zu sichern.

### 2.4 Was das Handbuch 2009 zur Welt sagt

| Stelle | Wortlaut (gekürzt) | Folge für uns |
|---|---|---|
| Portal (Z. 20) | Alle Welten in Nebelseetal liegen im magischen **Limbus, der sich in 20 Dimensionen aufteilt**; Entfernung kostet **Mana** | Limbus ist der **Raum**, nicht eine Welt |
| Götterschutz (Z. 53) | neue Spieler sieben Tage geschützt, danach Punkteband ±20 %, Grenze 299/300 | der Name verweist auf **Götter** |
| Punkte/Ziel (S. 3, 5) | Rangliste nach Gesamtpunkten, **keine Siegbedingung** — jeder Spieler hat eigene Ziele | E5-Entscheidung, siehe Abschnitt 4 |
| Karten (S. 11) | Landschaft verändert sich, Sumpf nicht bebaubar | die Bewegung der Karte ist Originafter Erzählstoff |

---

## 3. Herkunft jedes Bausteins auf einen Blick

| Baustein | Wo er steht | Herkunft | Urteil |
|---|---|---|---|
| Sechs Weltnamen (Midgard, Valhalla, Utgard, Armageddon, Ragnarök, Limbus) | `data/welten.json`, alte Website screens.php | **ORIGINAL** | belegt, bleibt |
| Limbus = Raum mit 20 Dimensionen | Handbuch 2009 Z. 20 | **ORIGINAL** | steht im Code, wird durch W-6 auf sechs Welten verengt |
| Drei Drachen, Magie, Weltbruch | Website Hintergrundgeschichte 1–3 | **ORIGINAL** | **im Remake nirgends verwendet** |
| Nebelseen aus Epheus Tränen | Website Teil 3 | **ORIGINAL** | im Remake nur als Geländeart, ohne Erklärung |
| Völkerwandel durch Magie | Website Teil 2 | **ORIGINAL** | erklärt Fraktionen — im Remake nicht genutzt |
| Karte verändert sich, Siedeln beruhigt sie | Website Teil 3 | **ORIGINAL** | im Remake nicht erzählt (Karte ist fest) |
| Götterschutz | Handbuch Z. 53 | **ORIGINAL** | im Code, ohne Götter im Hintergrund |
| Start: eine Siedlung, 10 Siedler, 100 Holz/Stein | Handbuch S. 7 | **ORIGINAL** | im Code |
| Fraktionen menschlich/zwergisch/elfisch/Trolle mit Boni | `bottaktik.py` | **ORIGINAL-nah** | im Code |
| Fraktionen Ghule, Gnome | `data/voelker.json` | **DANIEL** 03.11.2026 | im Code, Quelle im Datenblatt vermerkt |
| Fraktion → Heimatwelt | `data/welt_fraktionen.json` | **VORSCHLAG** | ausdrücklich als nicht belegt markiert |
| Fraktion → Burg/Wappen | `data/bot_wappen.json` | **VORSCHLAG** | zwei Menschen tragen dasselbe Wappen |
| Ton der Texte (leicht, abenteuerlich) | `data/story.json` | **DANIEL** 04.11.2026 | im Code |
| Intro, sieben Chronikkapitel, Sieg-, Niederlagentext | `data/story.json` | **ENTWURF** | frei ersetzbar |
| Fünf Botnamen und ihre Rollen | `botkern.BOT_NAMEN` | **ENTWURF** | keine Quelle, keine deiner Ansagen |
| 40 Bot-Sätze | `data/bot_stimmen.json` | **ENTWURF** (Story 2) | frei ersetzbar |
| Zehn Siedler, zwei Werkzeugkisten | `data/story.json` | **ENTWURF** | Werkzeugkisten sind im Spiel kein Gegenstand |
| Sechs Welten statt 20 Dimensionen | deine Korrektur 04.11. | **DANIEL** | Schritt W-6 noch nicht gebaut |

---

## 4. Wo Geschichte und Spiel sich widersprechen (sieben Befunde)

**Befund 1 — Es gibt einen Siegtext, aber keinen Sieg.** `punkte.spielausgang` sagt wörtlich
*kein Sieg vorgesehen (E5)*, weil das Handbuch keine Siegbedingung nennt; bewertet wird über vier
Auszeichnungen. Der Siegtext in `data/story.json` wird **von keiner Stelle im Spiel aufgerufen** — er
existiert nur für die Wache. Ein Spieler kann also nie lesen, dass das Nebelseetal einen Namen bekommen
hat. Das ist entweder ein toter Text oder eine fehlende Regel.

**Befund 2 — Der Ratgeber widerspricht der Story.** `berater._antwort_sieg` antwortet weiterhin:
*Ein eindeutiges Sieg- oder Niederlage-Ereignis nennt das Handbuch nicht — das ist ein offener Punkt für
unser Remake.* Nach Story 1 gibt es aber beide Texte. Der Ratgeber ist damit veraltet.

**Befund 3 — Limbus ist im Original der Raum, im Remake eine Welt.** Das Handbuch: alle Welten liegen
**im** Limbus (20 Dimensionen). Unsere Story und `welt_fraktionen.json` behandeln Limbus als **sechstes
Bruchstück** mit den Gnomen als Heimat. Beides zugleich geht nicht.

**Befund 4 — Der Name Nebelseetal ist doppelt vergeben.** Im Original heißt die **eine** Welt vor dem
Bruch Nebelseetal; die Seen darin sind Nebelseen. Im Remake heißt das Spielfeld Nebelseetal, und der
Siegtext sagt, der Spieler gebe ihm *einen Namen* — obwohl es schon einen hat.

**Befund 5 — Götterschutz ohne Götter.** Der Begriff kommt aus dem Handbuch und steckt im Code
(Punktegrenze, sieben Tage). Die heutige Story kennt keine Götter — also schützt niemand.

**Befund 6 — 20 Dimensionen im Code, sechs Bruchstücke in der Story.** `data/welten.json` führt 20
Dimensionen, 14 davon leer (d07–d20). Die Story spricht von sechs. Der Schritt W-6 soll das schließen;
bis dahin widersprechen sich Daten und Text.

**Befund 7 — Die Fraktionen haben keine Herkunft.** Sie haben Boni und ein Bild. Warum sie in ihrer Welt
sitzen, warum es sie überhaupt gibt (nach dem Weltbruch!), steht nirgends — obwohl das Original genau
dafür eine Erklärung liefert (Völker verschmolzen mit der Magie).

---

## 5. Was fehlt — meine Sicht, mit Vorschlag je Punkt

| Nr. | Was fehlt | Warum es fehlt (Folge im Spiel) | Vorschlag |
|---|---|---|---|
| A | **Der Grund des Bruchs** | Die Story sagt *keiner weiß mehr, warum* — das Original weiß es (Salmur, die Magie). Ein Rätsel ohne Auflösung trägt keine Geschichte über 20 Spielstunden | Die drei Drachen als **Rahmen** zurückholen: Epheus, Tardas, Salmur. Sie müssen im Spiel nichts tun — sie erklären nur, warum es Welten, Portale und Nebelseen gibt |
| B | **Die Nebelseen** | Sie sind der **Namensgeber** des Spiels und im Spiel nur ein Gelände. Kein Text sagt, was sie sind | Aus Epheus Tränen: Nebelseen sind **Magie, die aus dem Boden läuft**. Damit hätte Mana (Portal) und Forschung einen Ort |
| C | **Herkunft der sechs Fraktionen** | Ohne Herkunft sind Fraktionen nur Boni | Je zwei bis drei Sätze: aus welchem Volk nach dem Bruch geworden, warum in dieser Welt. Ghule und Gnome (deine Entscheidung) brauchen eine eigene, kurze Begründung |
| D | **Motive der fünf Nachbarn** | Sie greifen an, ohne Grund; der Spieler hat keinen Bezug zu ihnen | Je ein Ziel (Haug will Vorräte, Brynhild Ordnung, Grom Steine, Silra Wissen, Krank Rache für Vergessenes). Passt zu ihren Taktikprofilen |
| E | **Warum der Spieler anfängt** | Zehn Siedler und zwei Werkzeugkisten sind gesetzt, nicht erzählt | Ein Satz Herkunft: wer schickt sie, was wollen sie |
| F | **Zeit im Spiel** | Die Spieluhr (Faktor 180) läuft schneller als echte Zeit, ohne Erklärung | Limbus-Zeit läuft anders — ein Satz genügt und erklärt nebenbei die Spielgeschwindigkeit |
| G | **Die vier Auszeichnungen als Ziel** | Das Spiel bewertet über Auszeichnungen, die Story erzählt von einem Sieg | Vier Wege, ein Ruf: Feldherr, Forscher, Händler, Gesamtherrscher. Der Ausgangstext gehört dorthin statt auf einen Sieg |
| H | **Was bei der Niederlage bleibt** | Der Niederlagentext ist gut, aber es gibt keinen Anschluss (Neustart) | Ein Satz: der Limbus nimmt das Reich zurück, ein anderer fängt an — genau wie im heutigen Text; das passt |
| I | **Eine Karte der Bruchstücke** | Der Spieler sieht im Portal ein Raster, aber keine Erzählung dazu | Die sechs Welten mit je einem Satz Landschaft und einem Bild — genau das Material, das für die PDF und die Repo-Vorstellung gebraucht wird |

**Meine Einschätzung nach Rang:** A, B und G sind Pflicht (sie erklären das Spiel selbst). C, D und I
tragen die Vorstellung nach außen (Repo, PDF, Völkerwahl). E, F und H sind Kür und kosten je einen Satz.

---

## 6. Was das große Modell dazu sagt

Gelaufen am 04.11.2026 mit `deepseek-v4-pro` (ein Aufruf, 2.360 Prompt- und 13.320 Antwort-Token, davon
9.634 Denk-Token, rund 0,1 USD). Vollständiger Text: **`docs/STORY_BIBEL_ENTWURF_20261104.md`** — dort
stehen der Rahmen, die sechs Welten, die sechs Fraktionen, die fünf Nachbarn, der Spieler, die vier
Auszeichnungen, die Niederlage und Vorschläge für die Chronik, jeweils mit [NEU] markiert.

**Sein Urteil, zusammengefasst:** es bestätigt meine sieben Befunde und fügt drei hinzu, die ich für die
wichtigsten halte:

1. **Die Geschichte hört nach der Chronik auf.** Sie trägt weder Wirtschaft noch Forschung noch Kampf
   noch Portale. Es fehlen die **Alltagstexte**: Rohstoff- und Warenlegende, Gebäudebeschreibungen,
   Einheitentexte, Forschungstexte, Nachbarn-Dialoge, Portal-Ereignisse, Auszeichnungsmeldungen. Das ist
   der größte Einzelbefund — er betrifft genau die Texte, die der Spieler täglich liest.
2. **Mana und Portal sind mechanisch, aber nicht erzählt.** Warum kostet eine Reise Mana, warum zählt
   die Entfernung? Antwort liegt im Original (Nebelseen speisen die Magie) und fehlt im Spiel.
3. **Die vier Auszeichnungen sind nicht erzählerisch definiert** — es gibt Rechenwege, aber keinen Satz,
   was ein Feldherr, Forscher, Händler oder Gesamtherrscher in dieser Welt bedeutet.

**Seine Lösung für den Limbus-Widerspruch** (Befund 3 oben) ist die beste Idee des Laufs: Limbus bleibt
der Raum, aber die Magie hat in ihm **feste Inseln** gebildet, und dort sitzen die Gnome. Damit stimmt
die alte Serverliste (sechs Einträge), es bleibt bei fünf echten Welten, und niemand muss eine siebte
erfinden.

**Was ich davon nicht übernehme** (Begründung in der Bibel-Datei, Abschnitt Befunde): Valhalla als
schwebende Inseln (widerspricht den gemalten Karten), zwei Fragen, die längst entschieden und gebaut sind
(Fraktionswahl des Spielers), und die Chronik-Vorschläge nur als Auswahl, nicht als Ersatz.

---

## 7. Was Daniel entscheiden muss

| Nr. | Frage | Empfehlung |
|---|---|---|
| 1 | **Drachen zurückholen?** (Epheus, Tardas, Salmur als Rahmen der Geschichte) | Ja — sie kosten keine Spielmechanik und erklären Welt, Portale, Nebelseen und Götterschutz in einem Zug |
| 2 | **Limbus: Raum oder Welt?** | Limbus als **Raum** (wie im Handbuch); die sechste Welt bekommt einen eigenen Namen. Dann braucht `welt_fraktionen.json` eine Änderung |
| 3 | **Sieg oder kein Sieg?** | E5 behalten (kein Sieg) und den Siegtext zu einem **Auszeichnungstext** umbauen — oder eine echte Siegbedingung bauen. Das ist eine Regelentscheidung, keine Textfrage |
| 4 | **Nebelseetal: Name des Spielfelds oder der alten Welt?** | Nebelseetal bleibt der Name der **alten, zersprungenen Welt**; das Spielfeld heißt im Text einfach die Bruchstücke. Dann passt auch der Siegtext nicht mehr |
| 5 | **Wappen für die beiden Menschen** | Haug und Brynhild brauchen verschiedene Wappen (dafür sind zehn Wappen da, sechs Fraktionen brauchen nur sechs) |
| 6 | **Wer schreibt die Texte?** | Das große Modell schreibt sie im vereinbarten Ton, ich prüfe sie gegen diese Tabelle und trage sie als Datendatei ein (kein Text im Code) |
