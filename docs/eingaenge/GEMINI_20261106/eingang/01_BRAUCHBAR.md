# 01 Brauchbar - was wir pruefen und uebernehmen sollten

**Stand:** 06.11.2026, Kopf `3c5189a`. Jede Zeile nennt Quelle (Rohdatei und Abschnitt der Sammlung),
Messlage im heutigen Code und den erwarteten Effekt. Reihenfolge nach Wirkung, nicht nach Wunsch.

## B-1 Diplomatie mit Beziehungen und Vertraegen (die groesste Idee)

**Quelle:** `20261105_2320_GoogleKI_Diplomatie.txt`, Abschnitte 1 bis 4.

**Messlage:** `src/main.py:13135 _render_diplomacy` zeigt je Bot genau zwei Kennzahlen
(`Handel: x%`, `Aggression: y%`), dazu die Taktik-Zeile aus `bottaktik.anzeige` und zwei Knoepfe
(`Handeln`, `Angriff entsenden`). **Keine Gesinnung, keine Vertraege, kein Vertrauenswert.**
`vertrag` kommt im Code nur als `Kaufvertrag` (`spieloekonomie.handel_start`) und `fremdvertrag`
(Transport, `auftraege.py:686`) vor - beides ist Handel, nicht Diplomatie.

**Was zu bauen waere:** Gunstwert je Nachbar, Statusstufen, drei Vertragsarten (Nichtangriffspakt,
Durchmarschrecht, Handelsabkommen) mit Mindestgunst, Vertragsbruch senkt die Gunst, jeder Nachbar
verhaelt sich anders. **Alle Zahlen des Entwurfs sind erfunden** - sie gehoeren in eine
Entscheidungsrunde, nicht in den Code.

**Erwarteter Effekt:** die Ansicht gewinnt eine Spielentscheidung, die es heute nicht gibt (heute
sind beide Knoepfe immer gleich - Handel oder Angriff, ohne Vorstufe). Beruehrt B2 (Bot-Zielbild)
und B5 (Handel/Spionage). Aufwand L.

## B-2 Proaktive Diplomatie-Events mit zwei Antworten

**Quelle:** `20261105_2324_GoogleKI_Diplomatie_Events.txt`, Abschnitte 1 und 2.

**Messlage:** die Overlay-Technik ist da (`_overlay_` 35 Treffer in `src/main.py`), der Anlass fehlt:
kein Ereignis fordert den Spieler zu einer Entscheidung auf, Nachrichten sind Berichte.
Die Armee des Bot kommt aus der Bot-Wirtschaft (`bot_armee_aufstellen`, Register 169) - eine im
Code festgeschriebene Rachearmee, wie der Entwurf sie vorschlaegt, waere eine zweite Wahrheit.

**Erwarteter Effekt:** aus Berichten werden Entscheidungen; passt in die Diplomatie-Runde (B-1) und
kostet dort wenig zusaetzlich. Aufwand M, aber nur zusammen mit B-1 sinnvoll.

## B-3 Postfach mit Filter, Archiv und Ablauf

**Quelle:** `20261105_2323_GoogleKI_Postfach_Archiv.txt`, Abschnitte 1 bis 3.

**Messlage:** `state.messages` wird an **29 Stellen** gefuellt (`grep -c "state.messages.append"
src/main.py`), Typ und Farbe je Nachricht gibt es (`NACHRICHTEN_FARBEN`), aber **kein Limit, kein
Archiv, kein Ablauf** fuer Nachrichten - die Archiv-Funktion `spielstand_archiv` betrifft
Spielstand-Slots, nicht das Postfach.

**Erwarteter Effekt:** laengere Partien bleiben lesbar; die guenstigste Verbesserung der ganzen
Sammlung. Aufwand S.

## B-4 Mauerreparatur

**Quelle:** `20261105_2141_GoogleKI_Beute_Flucht_Mauer.txt`, Abschnitt Mauerreparatur.

**Messlage:** die Luecke steht schon bei uns: `src/kampfbericht.py:566` -
«Ob und wie sich eine beschaedigte oder eroberte Mauer erholt, sagt das Handbuch nicht.»
Unser Wall rechnet in **Stufe + Zustand in Prozent** (`wall_zustand`), nicht in Trefferpunkten.
**Gemessen in den Spieltest-Laeufen: 0 Wallschaden** - beurteilbar wird das erst mit A3
(Kampf gegen ein echtes Bot-Dorf).

**Erwarteter Effekt:** der Wall ist nicht mehr nur ein Verbrauchsgut. Aufwand M, Zahlen muessen
von Daniel entschieden werden (das Original schweigt).

## B-5 Verwundetenheilung (Teil der Verluste heilbar)

**Quelle:** `20261105_2131_GoogleKI_LordsMobile_Vergleich.txt`, Abschnitt 2 Kampf.

**Messlage:** fehlt komplett. `Heilkunde` ist **Siedlerproduktion +10 Prozent je Stufe**
(`forschung_wirkung.py:15/57`), keine Heilung von Verlusten; `verwundet` kommt im Code nicht vor.
Verluste sind heute endgueltig.

**Erwarteter Effekt:** Verluste tun weh, sind aber nicht endgueltig - das bindet Ressourcen und Zeit
und verkuerzt den Aufbau NICHT (passt zu Leitlinie 237: es muss ein Aufbauspiel bleiben).
Aufwand M. Heilungsquote = Daniels Entscheidung.

## B-6 Etappen-Reise beim Weltwechsel

**Quelle:** `20261105_2135_GoogleKI_Limbus_Portale_Kampf.txt` Abschnitt 1 und
`20261105_2319_GoogleKI_Wegzeit_Weltkarte_Drachen.txt` Abschnitt 1.

**Messlage:** `grep -rilE "etappe" src/*.py` = **0 Treffer**. Eine Reise ist EINE Strecke
(`auftraege.reisegeschwindigkeit` plus `welt.entfernung`); es gibt keinen Zwischenhalt am Portal.

**Ehrliche Folge:** das **verlaengert** Reisen. Damit greift die Messpflicht-Tabelle (A2) und die
Leitlinie aus Register 237 - eine Aenderung, die den Ablauf verlangsamt, wird Daniel vorgelegt.
Aufwand L. Zahlen des Entwurfs (50 Mana, +2 Ticks) sind erfunden.

## B-7 Siedlungsumzug

**Quelle:** `20261105_2135_GoogleKI_Limbus_Portale_Kampf.txt`, Abschnitt Siedlungsumzug.

**Messlage:** keine Umzugsfunktion im Code. Es gibt Gruenden, Aufgeben (erst ab sechs Siedlungen,
Register 228) und den Weltensprung des Dorfes; eine bestehende Siedlung an eine andere Stelle oder in
eine andere Welt zu **versetzen** gibt es nicht. Wort "Umzug" im Code = nur die Sperre bei laufenden
Auftraegen.

**Erwarteter Effekt:** ein taktisches Werkzeug gegen die feste Platzwahl. Beruehrt Siedler, Portalkosten
und die Kartenregel. Aufwand L, braucht Daniels Zielbild.

## B-8 Ruhm-Fortschrittsbalken

**Quelle:** `20261105_2153_GoogleKI_Ruhm_Auszeichnungen.txt` und `20261105_2325_GoogleKI_Ruhm_Dashboard.txt`.

**Messlage:** die Rechnung ist da (`src/punkte.py:417 auszeichnungen`, vier Auszeichnungen mit
Kennzahl, Wert und Rechenweg), die Anzeige fehlt: `Progressbar` 0 Treffer in `src/main.py`.
Balken also mit `tk.Canvas` wie die uebrigen Balken, nicht mit ttk.

**Erwarteter Effekt:** der naechste Rang ist sichtbar, ohne neue Zahl im Spiel. Aufwand S.

## B-9 Nachrichten-Uebersicht begrenzen

**Quelle:** `20261105_2131_GoogleKI_LordsMobile_Vergleich.txt`, Abschnitt 3 Post.

**Messlage:** kein Limit im Code (siehe B-3). Fuer einen Einzelspieler ist das **kein Speicherproblem**,
sondern eine Lesbarkeitsfrage - deshalb zusammen mit B-3 bauen, nicht als eigenes Stueck.

## B-10 Hygiene: `pathlib` und Type Hints fuer NEUEN Code

**Quelle:** `20261105_2144_GoogleKI_Code_Workflow.txt`, Abschnitte 2 und 3.

**Messlage:** `pathlib` nutzen **14 von 60** Modulen (`src/*.py`), Rueckgabetypen tragen **767**
`def`-Zeilen. Kein Spielnutzen, reine Aufraeumarbeit.

**Erwarteter Effekt:** keine Spielwirkung. Nur als eigener Aufraeumschnitt, wenn Daniel ihn will -
und nie als Nebenprodukt eines Feature-Schnitts.
