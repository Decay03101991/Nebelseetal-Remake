RAHMEN UND VORGABEN (gelten fuer jede Aufgabe; Daniel, 31.10.2026)

1. ROLLE: Du bist PRUEFER UND ENTWERFER, nicht Erzaehler. Du urteilst ausschliesslich nach dem
   beigefuegten Material. Was dort nicht steht, ist "nicht belegbar" - du erfindest keine
   Zeilennummern, keine Seitenzahlen, keine Werte. Kein Vorwort, kein Lob, keine Zusammenfassung.
   Sprache: Deutsch.
2. NEUESTE FASSUNG IST DAS ORIGINAL. Nennt die NEUERE Fassung nur WERTE und beschreibt die AELTERE
   Fassung die MECHANIK, dann gilt: MECHANIK aus der aelteren, ZAHLEN aus der neueren Fassung. Das
   ist eine begruendete Zusammenfuehrung und ausdruecklich erlaubt - kennzeichne sie als
   "ZUSAMMENFUEHRUNG" und nenne beide Quellen mit Stelle.
3. NUR was in KEINER Fassung steht, ist VORSCHLAG. Vorschlaege werden so gekennzeichnet und mit
   einem Satz begruendet (Spielgefuehl, Balance, Einzelspieler-Tauglichkeit).
4. Daniels eigene fruehere Annahmen (z. B. Sieg bei 300 Gesamtpunkten) sind VERWERFBAR, wenn die
   Quellen etwas anderes vorgeben.
5. Einzelspieler statt Mehrspieler: das Original war ein Browsergame mit vielen Spielern. Hier gibt
   es EINEN Menschen und wenige Bots. Wo eine Regel nur wegen vieler Spieler existiert (z. B. 20
   Dimensionen als Platz fuer hunderte Welten), darf sie fuer den Einzelspieler neu gedeutet werden -
   aber so, dass sie Sinn ergibt und die Originalmechanik erkennbar bleibt.
6. Spieluhr: Faktor 180, also 1 Spielstunde = 20 echte Sekunden. Handbuch-Raten gelten pro
   SPIELSTUNDE; das Original lief in Echtzeit.
7. Belegpflicht: jede Aussage mit Datei und Zeile (bzw. Dokument + Stelle). "Nicht belegbar" ist ein
   vollwertiges Ergebnis.

AUSGABEFORMAT (allgemein)
- Tabellen genau in der vorgegebenen Spaltenzahl, hoechstens die genannte Zeilenzahl.
- Jede Zeile mit Quelle (Dokument + Stelle) oder dem Wort VORSCHLAG.
- Am Ende hoechstens drei Saetze "Was das fuer den Code bedeutet" - ohne Code zu schreiben.

AUFGABE B - WEGZEIT, AUFTRAGSKOSTEN, PORTAL: EIN ZAHLENSYSTEM FUER EIN EINZELSPIELER-SPIEL

STAND DER ENTSCHEIDUNGEN (Daniel, 31.10.2026):
  * Reiseformel: Dauer = 2 * d / GS ist GESETZT und IM CODE AKTIV
    (`auftraege.SEKUNDEN_JE_FELD = 7200`, Pruefdatei `tests/test_auftraege.py` 111 Pruefungen),
    ausdruecklich anpassbar. Grund: bei x180 waeren Wege mit Faktor 1 so kurz, dass der
    Verteidiger keine Vorwarnzeit hat. Pruefe den Faktor, erfinde keinen neuen.
  * Dimensionswechsel kostet KEINE Zeit (Daniel erinnert sich sehr sicher) - nur Mana.
  * Dimensionen existierten, weil hunderte Spieler Platz brauchten. Hier gibt es einen Menschen und
    wenige Bots -> Dimensionen sollen zu Spruengen in andere Laendereien werden.

VERLANGE:
1. Pruefe Faktor 2 nach: fuehrt er bei x180 zu sinnvollen Zeiten? Rechne die Beispiele; wenn du einen
   anderen Faktor empfiehlst, dann mit Rechnung.
2. Eine Kostentabelle: Gold und Nahrung je Einheit und Strecke; Mana je Entsendung nach Entfernung.
   Jede Zahl belegt oder VORSCHLAG.
3. Sechs Beispielreisen: 6, 16 und 32 Felder mit GS 5 und GS 35 - Spielstunden und Echtzeit bei x180,
   Hin- und Rueckweg.
4. Wirkung einer 10-%-Drosselung (Dauer, Gold, Nahrung) in einer Beispielzeile.
5. DIMENSIONEN ALS LAENDEREIEN: Wie werden aus 20 Dimensionen sinnvolle Landesteile fuer EINEN
   Spieler mit wenigen Bots? Was ist das Portal dann (Reise zwischen Laendern, Handel, Kopfgeld)?
   Welche Mana-Kosten bleiben sinnvoll, und wie bleibt die Originalmechanik erkennbar? Zwei Varianten
   mit Vor-/Nachteil und eine Empfehlung.
6. Drei Punkte, die auch nach dieser Rechnung offen bleiben.

AUSGABEFORMAT
## Formel
## Kostentabelle
| Groesse | Wert | belegt/VORSCHLAG | Quelle/Herleitung |
## Sechs Beispielreisen
| Distanz | GS | Spielstunden | Echtzeit bei x180 | Rueckweg gesamt |
## Drosselung um 10 %
## Dimensionen als Laendereien
## Drei offene Punkte


==============================================================================
1  HANDBUCH 2009 - GS, Auftragszeit, Auftragskosten (Wortlaut)
==============================================================================

Abkürzungen:
Sollte bei einer Einheit ein Wert nicht angegeben sein, ist dieser für die Aufträge, die Du mit 
Ihr ausführen kannst, nicht relevant.
LE: Die Lebensenergie einer Einheit. Je höher diese ist, desto mehr Schaden verkraftet sie in der 
Schlacht.
AT: Der Angriffs- oder Attackewert einer Einheit. Je höher dieser ist, desto höher ist ihre Chance mit der 
Waffe einen Treffer zu landen.
PA: Der Verteidigungs- oder Paradewert. Je höher dieser Wert ist, desto höher ist die Chance der Einheit 
eine gegnerische, geglückte Attacke abzuwehren. 
SI: Der Sinnesschärfewert gibt an, wie Aufmerksam eine Einheit ist und wie leicht sie Spione entdecken 
kann. (Das Spionagesystem ist zur Zeit in einer Überarbeitungsphase. Dieser Wert hat im Moment noch 
keinen Einfluss auf das Spiel.)
HE: Der Heimlichkeitswert gibt an, wie gut eine Einheit sich unauffällig verhalten kann, um der 
Entdeckung durch Feinde zu entgehen. (Das Spionagesystem ist zur Zeit in einer Überarbeitungsphase. 
Der Wert hat noch keinen Einfluss auf das Spiel.)
RS: Der Rüstungsschutz bietet der Einheit Schutz, vor dem vom Gegner angerichteten Schaden. Je höher 
der Wert, desto weniger Schaden nimmt die Einheit bei einem Treffer.
TP: Die Trefferpunkte geben an, wie viel Schaden eine Einheit bei einem Treffer anrichtet. Der Schaden 
senkt die Lebensenergie des Gegners. 
GS: Der Geschwindigkeitswert gibt die Reisegeschwindigkeit einer Einheit an. Je höher dieser Wert, desto 
schneller kann die Einheit zwischen zwei Siedlungen reisen.
MU: Der Mutwert gibt an, wie entschlossen eine Einheit im Kampf ist und wie leicht sie in die Flucht 
geschlagen werden kann.
SK: Die Schlagkraft einer Einheit wird benötigt, um die gegnerische Verteidigung zu durchbrechen.
Seite 18


===== Seite 19 =====
Aufträge:
Einheiten und Zielspieler auswählen
Über den Button „Aufträge“ im Siedlungsmenü, kannst Du Deinen Einheiten Befehle erteilen. 
Um einen Auftrag einzuleiten klicke im Siedlungsmenü auf Aufträge. Alle Deine hier 
stationierten Einheiten werden angezeigt. 
Gib hinter den Einheiten die Anzahl an, die Du entsenden möchtest. Bei den Einheiten stehen 
auch die Kosten, die ein Auftrag verursacht. Wähle das Auftragsziel aus, zu dem Deine 
Einheiten aufbrechen sollen:
Eigene Siedlung
Wenn Du mehr als eine Siedlung besitzt, kannst Du Deine Einheiten zu einer anderen Deiner 
Siedlungen schicken, um z.B. Rohstoffe und Waren dorthin zu transportieren.
Portalkoordinaten
Wenn Du Deine Einheiten zu einem anderen Spieler schickst, musst Du seine Portalkoordinaten 
kennen. Diese stehen entweder in der Ruhmeshalle hinter dem Namen des Spielers, oder im 
Informationsfeld im Portal. Du hast auch die Möglichkeit, Aufträge über das Auftragsicon hinter 
den Spielern in der Ruhmeshalle oder im Portal zu erteilen. In diesem Fall werden die 
Koordinaten das entsprechenden Spielers automatisch hier eingetragen.
Verbündeter
Wenn Du verbündete Spieler hast, kannst Du diese hier direkt als Ziel für Deinen Auftrag 
auswählen. Du musst die Koordinaten nicht erst ausfindig machen.
Gildenmitglied
Bist Du in einer Gilde, kannst Du hier eines Deiner Gildemitglieder als Ziel für Deinen Auftrag 
auswählen. 
Auftragsdetails
Im nächsten Auswahlschirm werden zuerst die Zielsiedlung und die Auftragsart festgelegt. Je 
nach Art des Auftrags, müssen zusätzlich noch einige Einstellungen getätigt werden. Außerdem 
wird hier angezeigt, wie Lange der Auftrag dauern wird. Die Zeitangaben gelten für eine 
Strecke. Wenn also 2 Stunden angegeben sind, benötigen Deine Einheiten 2 Stunden um die 
Zielsiedlung zu erreichen. Sollten die Einheiten, wie beispielsweise bei einem Transport, wieder 
zur Startsiedlung zurückkehren, dauert der Auftrag doppelt so lange.
Zielsiedlung
In dem Auswahlfeld oben auf der Seite wähle zuerst die Siedlung aus, die das Ziel des 
Auftrages werden soll. 
Auftragsart
Als nächstes muss die Art des Auftrags gewählt werden. Welche Arten zur Auswahl stehen 
hängt von den, von Dir zuvor gewählten Einheiten ab:
Stationieren

[...]

Auftragskosten
Ein Auftrag zwischen Euren eigenen Siedlungen kostet, je nach Einheiten, verschiedene 
Mengen an Gold und Nahrung. 
Aufträge zu fremden Siedlungen kosten zusätzlich Mana, um das magische Portal zu den 
fremden Spielwelten zu öffnen. Wie viel Mana hängt von der Entfernung der Zielwelt ab. Wenn 
Ihr genauer planen möchtet, wann die Einheiten ihr Ziel erreichen, dann könnt Ihr die 
Geschwindigkeit in 10% Schritten drosseln. Die aktuelle Dauer der Mission wird im Feld 
"Reisedauer" angezeigt. Je langsamer Eure Einheiten reisen, desto weniger Gold benötigen sie. 
Allerdings steigt dabei der Bedarf an Nahrung. Wenn Ihr alles angegeben habt, klickt auf 
„Auftrag erteilen“ um den Auftrag zu starten. Die Auftragskosten werden abgezogen und Eure 
Einheiten reisen los. 
Seite 20


==============================================================================
2  VORVERSION 2006 - Portal, Limbus, Dimensionen, Mana (Wortlaut)
==============================================================================

Portal
|
Portal
|
Portale
Ihr spielt auf einer Welt unter vielen. Auf jeder Welt in Nebelseetal-Online gibt es ein magisches Portal, welches
Eure Welt mit der aller anderen Spieler verbinden kann. So ist es Euch möglich untereinander
Handel zu treiben, aber auch Krieg zu führen. Das Aussenden von Truppen oder
Waren erfordert allerdings eine Aktivierung des Portals mittels Magie. Dies kostet Euch, unabhängig
von der Anzahl der Einheiten, jedes Mal eine bestimmte Menge Mana.
Diese ist von der Entfernung, der zu besuchenden Welt, im magischen Limbus abhängig. Liegt
Sie weit von Eurer Welt entfernt, oder gar in einer anderen Dimension, kostet es
Euch viel Mana. Ist sie nah an Eurer Welt gelegen, benötigt Ihr nur wenig von der
kostbaren, magischen Energie.
Portalkoordinaten
Jede Spielerwelt liegt im magischen Limbus, auf bestimmten Koordinaten. Diese bestehen
aus drei Zahlen. Die ersten beiden (X und Y), zeigen die Position Eurer Welt, auf
einem zweidimensionalem Raster, in Eurer Dimension an. Die dritte Zahl (Z) zeigt die Dimension an, in
der sich Eure Welt befindet. Die Dimensionen zu durchdringen, um Welten in einer
anderen Dimension zu besuchen, kostet Euch viel Mana. Deswegen ist es ratsam
vorerst Verbündete (oder Gegner), in eurer Dimension zu suchen. Es gibt 20 Dimensionen,
in jeder Dimension sind 20 mal 20 Felder frei für Spielerwelten.
Ihr habt die Möglichkeit, einmal binnen 24 Stunden, eure Koordinaten zu wechseln. Dazu rufen
Eure Magier, durch machtvolle Formeln, eine Verwirbelung des Limbusses hervor, die Eure
Welt an ihren neuen Platz verschiebt. Sie benötigen hierfür 5.000 Mana.
Da die magische Zeremonie in einer Eurer Siedlungen abgehalten wird, darf das Mana nicht
über mehrere Siedlungen verteilt, sondern muss in einer einzelnen Siedlung verfügbar sein.
Portalkoordinaten wechseln
Um Eure Welt zu verschieben, wechselt zunächst auf die Portalansicht. Wenn ihr innerhalb der
letzten 24 Stunden Eure Koordinaten nicht gewechselt habt, befindet sich unter dem
Koordinatenraster ein Button "Verschiebungsritual durchführen". Nach einem Klick auf diesen,
werden Euch alle Eure Siedlungen in einer Auswahlbox aufgelistet, die genügend Mana
für das Ritual zur Verfügung haben. Wählt die Siedlung aus, aus der das Mana verbraucht
werden soll, gebt die von Euch gewünschten, neuen Portalkoordinaten ein und klickt auf
"Ritual durchführen". Eure Welt wird nun auf die neuen Koordinaten verschoben.
Falls ihr Eure Welt erneut verschieben möchtet, müsst Ihr 24 Stunden warten und erneut
5.000 Mana aufbringen.
Die Portalanzeige
Im Spielmenü befindet sich der Button "Portal". Wenn Ihr ihn anklickt, könnt
Ihr das Raster Eurer Dimension sehen. Eure Welt wird durch ein grünes Banner markiert,
fremde Welten durch rote. Zeigt mit dem Mauspfeil auf ein Banner um den Namen
und die Koordinaten des Besitzers zu erfahren. Außerdem werden die Reisekosten
an Mana angezeigt.
Mit dem Auswahlmenü über dem Raster könnt Ihr Euch die Karten der anderen
Dimensionen ansehen. Wählt einfach eine Dimension aus, um zu den verschiedenen
Dimensionsrastern zu wechseln.


==============================================================================
3  AKTIVER CODE - Reisezeit und Kosten (src/auftraege.py)
==============================================================================

import kampfbericht as KB

STAND = "2026-10-04.1"

# Die vier belegten Auftragsarten (docs/ENTWURF_AUFTRAEGE.md, Tabelle).
AUFTRAGSARTEN: Tuple[str, ...] = ("stationieren", "transportieren", "handeln", "angreifen")

# VORGABE DANIEL 31.10.2026 (Registerpunkt 43): Das Handbuch nennt KEINE Formel aus Entfernung und
# Geschwindigkeit, nur Beispielstunden (S. 19). Deshalb gilt als anpassbare Arbeitsformel:
#     Dauer (eine Strecke) = 2 * Entfernung / Geschwindigkeit  ->  2 * 3600 s je Feld und GS 1
# Grund fuer den Faktor 2: bei Spieluhr x180 waeren Wege mit Faktor 1 so kurz, dass der Verteidiger
# keine Vorwarnzeit hat. Der Faktor ist EINE Konstante und wird hier bewusst offen benannt.
SEKUNDEN_JE_FELD = 7200.0

# BELEGT: die Rueckkehr dauert so lange wie eine Strecke, zusammen also das Doppelte (S. 19).
HIN_UND_RUECK_FAKTOR = 2.0

# BELEGT: die Geschwindigkeit ist in 10-%-Schritten drosselbar (Handbuch S. 20, Z. 1191).
DROSSELUNG_SCHRITTE_PROZENT = 10
DROSSELUNG_ZITAT = "Drosselung in 10-%-Schritten (Handbuch 2009, Seite 20)"

# VORSCHLAG: Die Handlung am Ziel ist hier sofort fertig (Dauer 0). Das Handbuch nennt
# fuer stationieren/transportieren/angreifen keine Aufenthaltsdauer; handeln wartet laut
# Entwurf auf eine Bestaetigung, deren Dauer aber nicht beziffert ist. Der Zustand
# 'am_ziel' wird darum nur im Ankunftsaugenblick gezeigt.
AKTION_DAUER_SEKUNDEN = 0.0

# VORSCHLAG: Beutemenge 50 % der Lager, gedeckelt durch die Karrenladung. Der Entwurf
# selbst nennt diese Zahl ausdruecklich VORSCHLAG (docs/ENTWURF_AUFTRAEGE.md, "Was Daniel

[...]

def _schlagkraft_belagerung(bestand: Dict[str, int]) -> float:
    return float(sum(E.schlagkraft(n) * k for n, k in bestand.items() if E.ist_belagerung(n)))


# ------------------------------------------------------------------------- Reisemodell

def reisezeit_sekunden(entfernung: Any, geschwindigkeit: Any) -> float:
    """Dauer EINER Strecke in Sekunden (Handbuch S. 19: die Dauer gilt fuer eine Strecke).

    Formel (VORSCHLAG, siehe offene_luecken['reisezeit_formel']):
        Sekunden = Entfernung / Geschwindigkeit * SEKUNDEN_JE_FELD
    Eine ungueltige (nicht positive) Geschwindigkeit liefert unendlich - der Auftrag
    kann so nicht starten; `starten` weist das vorher ab.
    """
    e = max(0.0, _als_zahl(entfernung))
    if e <= 0.0:
        return 0.0
    g = _als_zahl(geschwindigkeit)
    if g <= 0.0:
        return float("inf")
    return e / g * SEKUNDEN_JE_FELD


def ladung_der_mission(einheiten: Any) -> int:
    """Gesamte Tragefaehigkeit der mitgefuehrten Karren (einheiten.kapazitaet).

    Nur Transporteinheiten tragen; Kaempfer und Belagerungswaffen tragen nichts.
    """
    return int(max(0, sum(E.kapazitaet(n, k) for n, k in _bestand(einheiten).items())))


==============================================================================
4  GESCHWINDIGKEITEN UND LADUNG DER 28 EINHEITEN (data/units.json)
==============================================================================

Name | GS | Ladung | Gebaeude
Bürgerwehr | 5 | None | Kriegerakademie
Kämpfer | 10 | None | Kriegerakademie
Krieger | 25 | None | Kriegerakademie
Ritter | 20 | None | Kriegerakademie
Paladin | 20 | None | Kriegerakademie
Kurzbogenschütze | 5 | None | Kriegerakademie
Bogenschütze | 5 | None | Kriegerakademie
Langbogenschütze | 5 | None | Kriegerakademie
Armbrustschütze | 5 | None | Kriegerakademie
Streuner | 10 | None | Diebesgilde
Gauner | 15 | None | Diebesgilde
Dieb | 20 | None | Diebesgilde
Meisterdieb | 25 | None | Diebesgilde
Kundschafter | 30 | None | Diebesgilde
Waldläufer | 35 | None | Diebesgilde
Handkarren | 10 | 40 | Stellmacher
Einspänner | 25 | 100 | Stellmacher
Zweispänner | 30 | 250 | Stellmacher
Handelskarawane | 25 | 1000 | Stellmacher
Große Handelskarawane | 30 | 2500 | Stellmacher
Siedlerkarren | 20 | None | Stellmacher
Belagerungsturm | 15 | None | Stellmacher
Ramme | 15 | None | Stellmacher
Großer Belagerungsturm | 15 | None | Stellmacher
Große Ramme | 15 | None | Stellmacher
Balliste | 15 | None | Stellmacher
Katapult | 15 | None | Stellmacher
Großes Katapult | 15 | None | Stellmacher


==============================================================================
5  PRODUKTIONSRATEN JE STUNDE (data/resources.json, Auszug)
==============================================================================

{
 "versionsvermerk": "Zwei Fassungen belegt: archivierte Spielanleitung 2005 (HTML) und Handbuch 2009 (Textfassung). Sie weichen bei mehreren Ertraegen und bei der Siedlergrenze ab. Primaerwerte = 2009; Abweichungen sind je Rohstoff in 'abweichung' bzw. unter 'siedler' vermerkt.",
 "gebaeude_ohne_forschung": [
  "Holzfäller",
  "Steinmetz",
  "Jäger",
  "Bibliothek",
  "Haus"
 ],
 "regeln": {
  "gelände": "Jedes produzierende Gebäude erzeugt auf 2 verschiedenen Geländearten unterschiedliche Mengen. Ausnahme: der Jäger (in der 2005er Fassung nur Wald, 2009 auch Steppe).",
  "sumpf": "Sümpfe sind unbebaubar und für Siedlungen wertlos.",
  "zuwachs": "Der Wert in Klammern ist die Produktionsmenge pro Stunde; der Rohstoffzuwachs pro Stunde steht im Spiel in Klammern hinter dem Bestand, ein Balken zeigt, wann die nächste Einheit dazukommt.",
  "echtzeit": "Produktion läuft in Echtzeit (Beispiel Handbuch: 4 Holz/Stunde = alle 15 Minuten 1 Einheit Holz).",
  "abriss": "Ein Abriss bringt keine Rohstoffe zurück.",
  "bibliothek": "Bibliothek nur auf Grasland, Steppe oder Nebelsee, eine je Siedlung."
 },
 "siedler": {
  "produktion_pro_stunde": 1,
  "grenze_neue_siedlung": {
   "handbuch_2009": 10,
   "fassung_2005": 5
  },
  "erhoehung_pro_haus": 5,
  "abweichung": "Siedlergrenze einer neuen Siedlung: Handbuch 2009 = 10 Siedler, 2005er Fassung = 5 Siedler. Erhöhung pro Haus in beiden Fassungen +5."
 },
 "startwerte": {
  "siedler": 10,
  "holz": 100,
  "steine": 100,
  "_anmerkung": "Startwerte laut Handbuch 2009 Seite 7 (10 Siedler, 100 Holz, 100 Steine) und ORIGINAL_Kampf_und_Punkte.md Abschnitt 5."
 },
 "max_siedlungen": 6,
 "rohstoffe": [
  {
   "id": "holz",
   "name": "Holz",
   "erzeugendes_gebaeude": [
    "Holzfäller"
   ],
   "ertrag_pro_stunde": {
    "Wald": 4,
    "Steppe": 2
   },
   "ertrag_2005": {
    "Wald": 4,
    "Steppe": 1
   },
   "abweichung": "Steppe: 2005 = 1, Handbuch 2009 = 2. Wald in beiden Fassungen 4."
  },
  {
   "id": "stein",
   "name": "Stein",
   "erzeugendes_gebaeude": [
    "Steinmetz"
   ],
   "ertrag_pro_stunde": {
    "Berg": 4,
    "Hügel": 2
   },
   "ertrag_2005": {
    "Berg": 4,
    "Hügel": 1
   },
   "abweichung": "Hügel: 2005 = 1, Handbuch 2009 = 2. Berg in beiden Fassungen 4."
  },
  {
   "id": "metall",
   "name": "Metall",
   "erzeugendes_gebaeude": [
    "Erzmine"
   ],
   "ertrag_pro_stunde": {
    "Berg": 3,
    "Hügel": 1.5
   },
   "ertrag_2005": {
    "Berg": 3,
    "Hügel": 1
   },
   "abweichung": "Hügel: 2005 = 1, Handbuch 2009 = 1,5. Berg in beiden Fassungen 3."
  },
  {
   "id": "mana",
   "name": "Mana",
   "erzeugendes_gebaeude": [
    "Tempel"
   ],
   "ertrag_pro_stunde": {
    "Nebelsee": 5,
    "alle Gelände außer Sumpf": 1
   },
   "ertrag_2005": {
    "Nebelsee": 8,
    "alle Gelände außer Sumpf": 2
   },
   "abweichung": "Nebelsee: 2005 = 8, Handbuch 2009 = 5. Übriges Gelände (außer Sumpf): 2005 = 2, Handbuch 2009 = 1."
  },
  {
   "id": "nahrung",
   "name": "Nahrung",
   "erzeugendes_gebaeude": [
    "Farm",
    "Jäger",
    "Rinderfarm (siehe Leder, Anmerkung)"
   ],
   "ertrag_pro_stunde": {
    "Grasland": 4,
    "Steppe": 2
   },
   "ertrag_2005": {
    "Grasland": 4,
    "Steppe": 2
   },
   "abweichung": null,
   "weitere_erzeuger": {
    "Jäger": {
     "ertrag_pro_stunde": {
      "Wald": 2,
      "Steppe": 1
     },
     "ertrag_2005": {
      "Wald": 1
     },
     "abweichung": "Jäger: Handbuch 2009 nennt zusätzlich Steppe (1 Nahrung), 2005 nur Wald (1 Nahrung); Wald: 2005 = 1, 2009 = 2."
    }
   }
  },
  {
   "id": "gold",
   "name": "Gold",
   "erzeugendes_gebaeude": [
    "Goldmine"
   ],
   "ertrag_pro_stunde": {
    "Berg": 3,
    "Hügel": 1.5
   },
   "ertrag_2005": {
    "Berg": 3,
    "Hügel": 1
   },
   "abweichung": "Hügel: 2005 = 1, Handbuch 2009 = 1,5. Berg in beiden Fassungen 3.",
   "anmerkung": "Schreibweise 2005: 'Goldmiene', Handbuch 2009: 'Goldmine'."
  },
  {
   "id": "wolle",
   "name": "Wolle",
   "erzeugendes_gebaeude": [
    "S
