# 02 Teilweise brauchbar - Idee ja, Zahlen oder Modell nein

Hier steht, was einen Kern hat, den wir gebrauchen koennen, aber so wie die KI es liefert **nicht**
eingebaut wird. Die Spalte Luecke sagt, was damit geschlossen werden koennte.

## T-1 Rachepunkte fuer Krank (Rachekonto mit wachsender Armee)

**Quelle:** `20261105_2151_GoogleKI_Nachbarn_Zustandsautomat.txt` und
`20261105_2151_GoogleKI_Nachbarn_Angriff_Diebstahl.txt` (Abschnitt 2).

**Ist-Stand gemessen - mehr, als die Vorsitzung annahm:** es gibt bereits ein Bot-Gedaechtnis
(`src/bottaktik.py:345 GEDAECHTNIS_DEFAULT` mit `geschlagen_von`, `beute_verloren`,
`staerke_zuletzt`, `letzter_kontakt`), es wird nach einer Flucht mit dem Namen des Schlaegers gefuellt
(`bottaktik.py:566`) und der Zustand `RAECHEN` greift den gemerkten Schaediger an
(`bottaktik.py:483-487`, Taktik `blitz`). Im Spiel heisst der Schlaeger der **Spieler**.

**Was fehlt (und damit die eigentliche Idee):** ein **wachsender** Rachetopf, aus dem die Armee
skaliert. Heute ist Rache ein Schalter (gemerkt oder nicht), keine Menge. Zusatz: `bottaktik.py:730`
fuehrt "Rache, Beuteverlust, Staerke-Vergleich" selbst als **VORSCHLAG (D.3)** - also
Auslegungssache, keine belegte Regel.

**Luecke, die es schliessen wuerde:** "Krank vergisst nichts" bekommt eine Zahl statt eines
Schalters; Teil von B2 (Bot-Zielbild). Zahlen sind erfunden, Daniel entscheidet die Groesse.

## T-2 Wall-Belagerung in Trefferpunkten

**Quelle:** `20261105_2328_GoogleKI_Nachzuegler_A.txt`.

**Ist-Stand:** die drei Phasen des Entwurfs sind gebaut (Vorrunde am Wall, dann Gefecht, dann Beute);
der Wall rechnet in **Stufe + Zustand in Prozent** (`kampf.py:173/216`), Mauerschaden je
Belagerungsgeraet ist belegt (`einheiten.mauer_schaden`).

**Nicht brauchbar:** 5.000 Trefferpunkte, 75 Prozent Absorption, 0,05 Malus je Katapult - alles
erfunden, und ein TP-Modell waere ein zweites Wall-Modell neben dem gebauten. Der **Thema**-Teil
(Mauer nimmt Schaden und muss repariert werden) ist schon als B-4 aufgenommen.

## T-3 Goetterschutz als kaufbares Opfer

**Quelle:** `20261105_2328_GoogleKI_Nachzuegler_B.txt`.

**Ist-Stand:** der Schutz ist ein **Punkteband** (`punkte.goetterschutz_aktiv/tage/band`,
`punkte.py:189-229`) und endet mit dem ersten eigenen Kriegspunkt - genau so, wie der Entwurf es im
zweiten Absatz beschreibt.

**Nicht brauchbar:** ihn zusaetzlich fuer 100 Mana/200 Gold (24 Runden) oder 350/500 (72 Runden)
**kaufbar** zu machen. Das widerspricht der belegten Originalregel. Kein Lueckenschliesser.

## T-4 20 Limbus-Dimensionen gegen 6 Welten

**Quelle:** `20261105_2149_GoogleKI_Sechs_Welten.txt`.

**Ist-Stand gemessen:** `data/welten.json` fuehrt **sechs** Dimensionen (`d01` bis `d06`); der
Schluessel `_schnitt_w6` sagt ausdruecklich, dass die 14 leeren Platzhalter `d07` bis `d20` am
04.11.2026 entfernt wurden. **Die Frage der Sammlung ist damit erledigt** - und die Vorsitzung hat
sie als offene Datenloeschung gefuehrt, was falsch war (Korrektur in `04_LUECKEN.md`).

**Was bleibt:** keine Aktion. Kein Eintrag in der Entscheidungsrunde.

## T-5 Etappen-Reise: Idee ja, Zahlen nein

**Quelle:** `20261105_2319_GoogleKI_Wegzeit_Weltkarte_Drachen.txt`.

Die Idee steht als B-6 in `01_BRAUCHBAR.md`. **Nicht uebernehmbar:** 50 Mana Aufschlag, +2 Ticks,
`src/wegzeit_logik.py` als neues Modul (zweiter Rechenweg neben `auftraege.reisegeschwindigkeit`),
`data/weltkarte.json` im Programmordner (bricht die Regel, dass die Demo leer ausgeliefert wird).

## T-6 Verwundetenheilung: Idee ja, Quote nein

**Quelle:** `20261105_2131_GoogleKI_LordsMobile_Vergleich.txt`.

Die Idee steht als B-5 in `01_BRAUCHBAR.md`. **Nicht uebernehmbar:** 30 Prozent Heilungsquote,
Heilung ohne Kosten. Wer heilt, zahlt Ressourcen UND Zeit - sonst ist der Kampf kostenlos.

## T-7 Nachrichtenlimit: Idee ja, Begruendung nein

Die Sorge der KI ist ein Speicherproblem (Server, viele Spieler). Bei uns ist es eine
**Lesbarkeitsfrage**; technisch gibt es kein Limit und keinen Bedarf (`state.messages` im Spielstand,
29 Fuellstellen). Deshalb gehoert es zu B-3, nicht als eigenes Stueck.
