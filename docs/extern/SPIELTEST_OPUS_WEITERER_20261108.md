# NACHTRAG 1 zu `ANTWORT_OPUS_20261108.md` - Weiterer Spieltest 08.11.26

> **Art des Dokuments:** ERWEITERUNG der Antwort `ANTWORT_OPUS_20261108.md` (Desktop) um einen
> Zusatzauftrag, den Daniel Opus direkt erteilt hat (08.11.2026, 17:23). Beide Dateien gehoeren
> zusammen; die Antwort bleibt gueltig, dieser Nachtrag ergaenzt sie (Bezug: Befund S8 -> Antwort
> Teil 1, S1 -> Antwort Teil 3, S9 -> Antwort Teil 2, S10 -> Antwort Teil 4 Frage 18).
>
> **Erarbeitet von:** Claude Opus 5.5 (Anthropic), Einstellung laut Daniel "Thinking: Mittel",
> ueber Daniels Abo Claude Pro. Konfiguriertes Modell der Sitzung: `claude-opus-5-5`.
> **Kosten:** nur die Abo-Pauschale (Claude Pro, 21,42 EUR/Monat, Verlaengerung 08.12.2026). Kein
> API-Verbrauch, keine Abrechnung je Aufruf, kein DeepSeek-Guthaben verbraucht.
> **Koordination:** Hermes "Weltenfresser" (`deepseek-flash`) ist nach Daniel oberster Koordinator.
> Dieser Nachtrag ist ein ENTWURF zur Pruefung durch Hermes, keine eigenmaechtige Aenderung.
> **Geaenderte Projektpfade:** keine. Geschrieben wurde nur auf Daniels Desktop (`D:\Desktop`):
> `ANTWORT_OPUS_20261108.md` und diese Datei.

==================================================================================================
TEIL 0/7 - Eintraege fuer `docs/ENTWICKLUNGSPROTOKOLL.md` (zum Uebernehmen durch Hermes)
==================================================================================================

Format wie die bestehenden Zeilen (Zeit | Titel | Beleg). Hermes prueft und traegt ein; Register-
nummer vergibt Hermes (VORSCHLAG: 314).

| Zeit | Titel | Beleg |
|---|---|---|
| 17:09 | **Opus-Auftrag gestartet (Claude Opus 5.5, Thinking: Mittel, Claude Pro)** | Auftrag `AUFTRAG_CLAUDE_20261108.md` von Daniel in claude.ai uebergeben. Opus las GitHub `main` (Kopf `f4eaf7c`; `git diff fa5834b f4eaf7c` aendert nur `docs/`, Code = `fa5834b`) und verglich Daniels lokale `src/main.py` (nur lesen, Daniels Freigabe 17:15 "nur lesen nichts veraendern"): zeichengleich mit GitHub (Zeilenenden ignoriert). |
| 17:24 | **Antwort geliefert: `ANTWORT_OPUS_20261108.md` (5 Teile) auf dem Desktop** | 517 Zeilen, Teile <= 136 Zeilen. Punkte A-D mit Patch-Plaenen, Fragen 15-18 und Design, Zusatzfunde F1-F8. Schwerster Fund: `_portal_wechsel` versetzt kein Dorf. Desktop-Kopie byte-gleich geprueft (`cmp`). Kein Projektpfad geaendert. |
| 17:25 | **Zusatzauftrag Daniel: die letzte EXE wirklich spielen** | Daniel woertlich: "die letzte spielbare .exe von nebelseetal wirklich zu spielen und einige entwicklungswichtige Punkte festhaelst". |
| 17:27-17:33 | **Bildschirmsteuerung gescheitert, abgebrochen** | Daniel startete `Nebelseetal_Pre_Release_V_0.0.3.exe` (82.693.324 Byte), Slot 2 geladen. Fenster freigegeben, jede Aufnahme kam auf beiden Monitoren grau zurueck. In der EXE wurde NICHTS geklickt oder gespeichert. Daniel 17:34: "keine computer uebernahme mehr". Vermutete Ursache (nicht gemessen): Aufnahmeweg der Desktop-App; Nebenbefund: die Arbeitsumgebung auf dem Laptop meldete zu wenig freien Speicher. |
| 17:35-17:55 | **Spieltest ohne Bildschirm: Quellstand mit Ersatz-tkinter durchgespielt** | Linux-Umgebung (Python 3.13), NICHT Windows-verifiziert. Neuer Spieler: Tor, Profil, Neue Partie, Volk, Karte, Gruendung, Bauen, Forschung, Wall, Diebstahl, Ausbildung, Handel, Pakt, Portal, Speichern/Laden, 14 Spieltage. 0 Ausnahmen. 18 Befunde, davon 16 gehalten (S15, S17 verworfen) und 1 Messbefund verworfen (Seitenhilfe, Ersatz-tkinter kennt kein `pack_forget`). |
| 18:05 | **Nachtrag fertig: `Weiterer_Spieltest_08.11.26.md` auf dem Desktop** | Diese Datei, 8 Teile (0-7): Protokoll, Methode, Befunde S1-S18, Opus-Mehrwert, Steckbrief Opus fuer Hermes (Daniels Wunsch 17:46), Daniels Entscheidungen 17:52, Test- und Balancing-Tipps (17:55). Schwerste neue Funde: Handelspreis 300 Gold je Stueck (S2), Wall beendet Goetterschutz an Tag 4 (S3), ungelesene Diebstahlberichte werden nach 1 Spieltag geloescht (S4). |
| 17:52 | **Daniels Entscheidungen zu S2, S3 und Portal-Uhr** | Je Rohstoff / Wall beendet Schutz (gewollt) / Spielzeit. Umsetzungsplaene in Teil 6, Protokollzeile dort. |
| 17:55 | **Opus-Vorschlaege fuer Testlaeufe und Balancing** | Teil 7, Protokollzeile dort. |
| - | **Kosten** | Nur Claude-Pro-Pauschale; kein API-Aufruf, `total_cost_usd` entfaellt (Chat in claude.ai, nicht `claude -p`). DeepSeek-Guthaben unberuehrt. |

**Lernregel fuer Hermes (Muster Ursache -> Abstellmassnahme -> Test -> Skillregel):**
Ursache: Pruefdateien rufen Kernmethoden direkt (`_portal_wechsel(app, 5)`) und pruefen Rueckgabewerte,
aber nicht die Spielfolge (wo steht das Dorf danach?). Abstellung: je Knopf, der etwas kostet, eine
Wache "nach dem Klick steht X dort, wo der Spieler es erwartet". Skillregel-VORSCHLAG: "Ein Knopf,
der Rohstoffe/Mana abbucht, braucht eine Wache auf seine sichtbare Wirkung, nicht nur auf `True`."

==================================================================================================
TEIL 1/7 - Auftrag, Methode, Ueberblick - Stand Code fa5834b (= src/ in f4eaf7c)
==================================================================================================
Bisher geliefert: `ANTWORT_OPUS_20261108.md` (Punkte A-D, Fragen 15-18, Design) liegt auf dem Desktop;
Teil 0 dieses Nachtrags (Protokolleintraege).

## 0. Fuer Hermes: was ist das hier?

Daniel hat Opus am 08.11.2026 um 17:23 einen ZWEITEN Auftrag gegeben, zusaetzlich zur Antwort
auf `AUFTRAG_CLAUDE_20261108.md`. Wortlaut (gekuerzt):
"Mein Auftrag an dich ist die letzte spielbare .exe von Nebelseetal wirklich zu spielen und einige
entwicklungswichtige Punkte festzuhalten ... eine von Hermes mit deepseek flash umsetzbare und
verstaendliche Antwort ... die bisher spielbaren Ablaeufe moeglichst allesamt testen und fuer alles
ein brauchbares Feedback."

Diese Datei ist das Ergebnis. Bitte wie die erste Antwort behandeln: jede Zahl und jeden Anker
gegen den Code pruefen, dann umsetzen. Ablage spaeter unter `docs/extern/`. Format wie im Auftrag:
BEFUND / VORSCHLAG / RISIKO / PATCH-PLAN / TEST. Nichts davon ist eingebaut, auf Daniels Rechner wurde
nichts veraendert.

## 1. Wie gespielt wurde (ehrlich, bitte lesen)

1. **Versuch mit der echten EXE gescheitert.** Daniel hat `Nebelseetal_Pre_Release_V_0.0.3.exe`
   (D:\Arbeiten\Nebelseetal_Remake, 82.693.324 Byte, Stand 15:58) gestartet und Slot 2 geladen.
   Das Fenster war freigegeben, aber jede Bildschirmaufnahme kam auf beiden Monitoren als graue Flaeche
   zurueck. Ohne Bild kein Spieltest - es wurde in der EXE NICHTS geklickt und NICHTS gespeichert.
   Daniel hat danach entschieden: keine Bildschirmsteuerung mehr.
2. **Stattdessen gespielt: derselbe Quellstand ohne Bildschirm.** `src/main.py` auf Daniels Rechner
   ist zeichengleich mit GitHub (geprueft). In Opus' eigener Umgebung lief `src/` mit einem Ersatz-
   tkinter, das einen echten Widget-Baum baut: Texte und Knoepfe sind lesbar, Knoepfe werden ueber
   ihr echtes `command` gedrueckt, Zeit laeuft ueber den echten `_tick_loop` (Zeitfaktor x180).
   Gespielt als NEUER Spieler: Tor, Profil, Neue Partie, Volk, Karte, Gruendung, 14 Spieltage.
3. **Was diese Methode NICHT sieht:** Pixel, Farben, Fensterlage, Scrollen, Tempo auf 2 Kernen,
   Bilder. Wo etwas sichtbar/unsichtbar ist, entscheidet in echtem Tk auch `pack_forget` - ein solcher
   Befund (Seitenhilfe "Goetterschutz aktiv" nach Schutzende) wurde deshalb VERWORFEN.
4. **Testeingriffe** (nicht erspielt, nur um einen Weg pruefen zu koennen) sind mit TESTEINGRIFF
   markiert: 1 Handelskarawane + 5000 Gold (Handel), 6000 Mana (Portal), Gunst 60 (Pakt-Test).
5. **Kennzeichen je Befund:** GEMESSEN = im Lauf beobachtet; GELESEN = nur im Code.

## 2. Was getestet wurde - Ueberblick

| Ablauf | Ergebnis | Befund |
|---|---|---|
| Tor (Passwort festlegen, Login), Profilwahl, 3 Slots | laeuft | - |
| Neue Partie, Ankunftsfenster, Volk waehlen, feste Startkarte "Das Z" | laeuft | S12 (Entwicklertexte) |
| Gruendung, Dorfzentrum-Feld setzen (kostenlos) | laeuft | S14 |
| Bauen: Jaeger, Holzfaeller, Farm, Haus, Bibliothek, Kriegerakademie | laeuft | S13 |
| Forschung: Baukunst 1-3, Verteidigungsanlagen 1 | laeuft, Dauer = Stufe^2 h | S6, S7 |
| Wall errichten, Reparaturanzeige | laeuft | S3, S8 |
| Goetterschutz / Kriegspunkte | **Wall beendet Schutz an Tag 4** | S3 |
| Bot-Diebstahl, Postfach | laeuft, **Berichte verschwinden** | S4 |
| Ausbildung (Kaserne, Buergerwehr, Kaempfer) | Sperren korrekt | S5 |
| Marktplatz, Kaufvertrag (ohne/mit Karawane) | Mechanik ok | **S2**, S9 |
| Diplomatie: Pakt, Ereignisse (Tribut, Messer, Auskunft) | laeuft, Pakt stoppt Diebstahl | S10, S16 |
| Portal: Feld waehlen, Weltensprung | **Dorf wird nicht versetzt** | **S1** |
| Speichern Slot 1, 5 h weiter, Laden Slot 1 | **Stand identisch** (9 Werte verglichen) | S18 |
| Kampfsimulator, Spionage ohne Einheiten, Hilfe, Auskunft-Chat | ehrliche Absagen, Hilfe antwortet | - |
| Gilde, Forum, Spieler werben, Einstellungen (Tempo) | Platzhalter | S12 |
| 14 Spieltage am Stueck | **0 Ausnahmen**, 13,6 s Rechenzeit fuer 10 Tage | S11 |

**Gutes zuerst (bitte nicht kaputt machen):** In ALLEN Laeufen gab es keine einzige Ausnahme und
keinen stillen Fehlklick - jede Absage nannte einen Grund (Statuszeile). Bauen nach Rohstoffen,
Forschungsdauer (Baukunst 1 nach 1 h, Stufe 3 erst nach dem Holz fuer 200), Pakt sperrt Diebstahl
wirklich, Speichern/Laden ist verlustfrei, das Ankunftsfenster kommt nur einmal (geschichte.json).

## 3. Reihenfolge der Befunde (schwer zuerst)

S1 Portal versetzt kein Dorf - S2 Handelspreis 300 Gold je Stueck - S3 Wall beendet Goetterschutz -
S4 Diebstahlberichte verschwinden ungelesen - S5 Ausbildungspreis versteckt - S6 Forschungs-Sperrtext
mischt Soll/Ist - S7 Fehlklicks fuellen das Postfach - S8 Wall-Anzeige (bestaetigt Antwort Teil 1) -
S9 Marktplatz ohne Zustand - S10 Pakt ohne Anzeige - S11 Holz-Engpass - S12 Entwicklertexte -
S13 Zahlformat - S14 "Naechster Schritt" waehlt kein Feld - S16 unbezahlbare Ereigniswege - S18 Speichern.
(S15 und S17 entfallen: beim Gegenpruefen nicht haltbar.)

NAECHSTER TEIL: 2/7 - Befunde S1 bis S7 mit Patch-Plan.

==================================================================================================
TEIL 2/7 - Befunde S1-S7 - Stand fa5834b
Bisher geliefert: Teil 0 (Protokoll), Teil 1 (Auftrag, Methode, Ueberblick).
==================================================================================================

S1 PORTAL - GEMESSEN
BEFUND:    Vorher Dorf "Siedlung 1" auf Welt 4, Feld 19/16. TESTEINGRIFF 6000 Mana, `_portal_wechsel(5)`
           -> True, "5000 Mana abgebucht, 24 Stunden gesperrt". Danach: Dorf weiter Welt 4 / 19/16,
           `eigene_dimension` = 5. Auf der eigenen Karte (Welt 5) stehen 0 eigene Doerfer
           (Tag `portalspieler`), auf Welt 4 steht es weiter. 5000 Mana fuer nichts.
VORSCHLAG: Umbau genau nach `ANTWORT_OPUS_20261108.md` Teil 3 (Kern `dorf_versetzen`); bis dahin den
           Knopf "Weltensprung" in `_render_portal` (main.py Z. 12182) entfernen und durch eine Zeile
           "Der Weltensprung wird umgebaut" ersetzen - ein Knopf, der Mana nimmt und nichts tut, ist
           schlimmer als keiner.
RISIKO:    `tests/test_portal_uebersicht.py` ruft `_portal_wechsel` direkt - bleibt gruen, solange die
           Methode bleibt; nur der Knopf geht.
PATCH-PLAN:
  1. main.py :: _render_portal :: Anker Z. 12181 `if eintrag["waehlbar"]:`
     alt: Knopf "Weltensprung" (Z. 12182-12184).
     neu: `tk.Label(zeile, text="Sprung wird umgebaut", fg="#8a8a8a", bg=self.skin["panel"],
          font=("TkDefaultFont", 8)).pack(side=tk.RIGHT, padx=6)` - Zwischenstand bis Teil 3 steht.
TEST:      NEU `tests/test_portal_kein_leerer_sprung.py` (ASCII): GUI zeigt im Portal keinen Knopf mit
           Text "Weltensprung"; nach dem Umbau ersetzt durch die Wache aus Antwort Teil 3.

S2 HANDELSPREIS - GEMESSEN
BEFUND:    Das Kauffenster nennt "Schwellenpreis dieses Bots: 300 Gold" - JE STUECK. TESTEINGRIFF
           (Karawane, 5000 Gold): 10 Holz zu 10 Gold je Stueck -> Haug lehnt ab; 10 Holz zu 310 Gold
           -> angenommen, **3.100 Gold fuer 10 Holz**. Herkunft: `botkern.py` Z. 265
           `BESCHAFFUNGSKOSTEN = 250.0` (Kommentar Z. 255-257: "Preis des Kaempfers ... 1 Siedler +
           250 Gold") x `HANDEL_AUFSCHLAG` 1,2 = 300. Der Preis EINER KAMPFEINHEIT gilt als Preis
           JEDES Rohstoffs. Der Spieler startet mit 0 Gold; Haug hat 1.299 Holz. Handel ist damit
           praktisch nie sinnvoll - das passt zu Daniels Note 5 fuer Handel.
VORSCHLAG: Nicht still aendern (Daniels Bereich, Frage 15 betrifft genau diesen Wert). Daniel fragen:
           "Soll der Schwellenpreis je Ware gelten (z. B. aus `data/` je Rohstoff), oder bleibt 300?"
           Bis zur Antwort: im Kauffenster den Satz ergaenzen "je Stueck - Beispiel: 10 Holz = 3.000 Gold",
           damit der Spieler die Folge sieht (reine Anzeige, Zahl aus `handelspreis`).
RISIKO:    Jede neue Preisregel aendert Bot-Gold und Rachetopf-Rechnungen (`test_handel_*`).
PATCH-PLAN: erst nach Daniels Antwort; Anzeige-Satz: main.py :: _handel_maske (Z. 10569 ff.) ::
           Anker `Schwellenpreis dieses Bots:` -> Satz anhaengen, Zahl = Schwellenpreis x 10, gerechnet
           in einer Hilfsfunktion `beispiel_preis_text(preis)` neben `prozent_text` (nicht in der Ansicht).
FRAGE:     Daniel: Schwellenpreis je Rohstoff oder pauschal? (VORSCHLAG: je Rohstoff, Werte aus Daten.)

S3 WALL BEENDET GOETTERSCHUTZ - GEMESSEN
BEFUND:    Tag 4: Wall errichtet -> `punktestand()["krieg"]` = 1 (Wallstufe^3, `punkte.kriegspunkte`,
           Handbuch S. 5) -> naechster Takt: "Goetterschutz beendet (erster Kriegspunkt)" (main.py
           Z. 7785-7787). Ab dann stehlen ALLE FUENF Bots alle 12 Spielstunden (gemessen: je Bot 3 %,
           zusammen rund 10 % von Holz, Stein, Mana, Nahrung, Leder; bei x180 alle 4 echten Minuten).
           Eine reine VERTEIDIGUNG kostet den Anfaenger also 3 Tage Schutz. Der Wall-Knopf warnt nicht.
VORSCHLAG: Regel nicht aendern (Handbuch S. 5/6). Aber den Knopf ehrlich machen: solange
           `state.noob_protection` gilt, steht am Wall-Knopf "Achtung: der Wall zaehlt als Kriegspunkt
           und beendet den Goetterschutz" und der Klick fragt nach (`messagebox.askyesno`).
RISIKO:    `tests/test_gpt_wall_gui.py` drueckt den Knopf ohne Fenster - Rueckfrage nur `if root`.
PATCH-PLAN:
  1. main.py :: _karten_wall_errichten :: Anker Z. 11011 `ok, text = self.state.wall_errichten(siedlung)`
     neu: davor `if self.state.noob_protection and getattr(self, "root", None) is not None and not
          messagebox.askyesno("Dorfwall", <Warnsatz>): return`
  2. Warnsatz als Label ueber dem Knopf (nach Antwort Teil 1 in `_wall_block`).
TEST:      NEU in `tests/test_wall_verteidigung.py`: bei Schutz steht der Warnsatz im Fenster.
FRAGE:     Daniel: soll der Wall im Goetterschutz ueberhaupt zaehlen? (Handbuch sagt ja - nur fragen.)

S4 DIEBSTAHLBERICHTE VERSCHWINDEN - GEMESSEN + GELESEN
BEFUND:    Diebstahlberichte haben `type: "diebstahl"` (main.py Z. 2181 in `bot_diebstahl_nachricht`).
           `data/nachrichten.json`: Frist 86.400 Spielsekunden, verschoben werden ungelesen NUR
           `["verlust"]`. `postfach.ablauf_buchen` (Z. 140-167) LOESCHT also ungelesene Diebstahlberichte
           nach 1 Spieltag = **8 echte Minuten bei x180**. Gemessen: Postfach-Zahl fiel von 18 auf 11.
           Widerspricht `bot_diebstahl.json` "warum_postfach" (Daniel: "nur mit Bericht im Postfach") und
           Daniels Entscheidung 4 ("ungelesene Verlustberichte verschieben sich").
           Dazu: der Zeitstempel ist RECHNERZEIT ([2026-11-08T17:37:41...]), nicht Spieltag/Stunde.
VORSCHLAG: `"diebstahl"` in `verschieben_wenn_ungelesen` aufnehmen (Daten, keine Codeaenderung).
RISIKO:    Postfach waechst bei 5 Bots um 10 Berichte je Spieltag - deshalb nur ungelesene behalten.
PATCH-PLAN:
  1. data/nachrichten.json :: Anker `"verschieben_wenn_ungelesen": ["verlust"],`
     neu: `"verschieben_wenn_ungelesen": ["verlust", "diebstahl"],` und `_quelle` um
          "diebstahl = Verlustbericht (Opus-Spieltest 08.11.2026)" ergaenzen.
  2. src/postfach.py Z. 31 (Rueckfallwerte) gleich ergaenzen, sonst zwei Wahrheiten.
TEST:      `tests/test_postfach*.py` (vorhandene suchen): ungelesener Diebstahlbericht ueberlebt 2 Fristen.

S5 AUSBILDUNGSPREIS VERSTECKT - GEMESSEN
BEFUND:    Kaserne, Buergerwehr, nichts bezahlbar: Zeile "0 × Buergerwehr = 0 leder · 0 nahrung · 0 wolle
           · 0 Siedler · davon bezahlbar: 0", Knopf "Ausbilden (0)". Der Preis fehlt genau dann, wenn
           der Spieler wissen muss, was fehlt. Ursache main.py Z. 15633 `var.set("1" if moeglich >= 1
           else "0")`. Erst der Klick verraet "wolle fehlt 50.00".
VORSCHLAG: Vorschau immer mit Menge 1 rechnen; der Knopf bleibt gesperrt (das tut `zeichnen` schon).
PATCH-PLAN: main.py :: _ausbilden_block :: Anker Z. 15633 `var.set("1" if moeglich >= 1 else "0")`
           alt -> neu: `var.set("1")`.
TEST:      `tests/test_ausbildung*.py`: bei moeglich=0 enthaelt die Vorschau "1 × " und einen Preis > 0.

S6 FORSCHUNGS-SPERRTEXT - GEMESSEN
BEFUND:    "es fehlen Bibliothek 3/1, Schmiedekunst 0/1" - erste Angabe Soll/Ist, zweite Ist/Soll, im
           SELBEN Satz. `forschungspfad.py` Z. 195 `f"Bibliothek {soll}/{ist}"`, Z. 199 `f"... {ist}/{soll}"`
           (im Docstring Z. 184-185 sogar so beschrieben).
VORSCHLAG: Beide als Worte: "Bibliothek Stufe 3 (hast 1)", "Schmiedekunst Stufe 1 (hast 0)".
PATCH-PLAN: forschungspfad.py :: erfuellt :: Z. 195 und Z. 199 auf
           `f"Bibliothek Stufe {soll} (hast {ist})"` / `f"{p['was']} Stufe {soll} (hast {ist})"`.
RISIKO:    Tests, die den alten Text vergleichen (`grep -rn "3/1\|0/1" tests/`), mit umstellen.
TEST:      bestehende Forschungspfad-Pruefung + ein Fall mit beiden Arten im selben Satz.

S7 FEHLKLICKS FUELLEN DAS POSTFACH - GEMESSEN
BEFUND:    Ein Klick auf eine gesperrte Forschung schreibt eine Nachricht ("Mauerbau gesperrt — ...",
           main.py Z. 15106). Alle 21 Forschungen zeigen einen aktiven Knopf "Forschen (50 Holz)", auch
           gesperrte. Umgekehrt melden Wall (Z. 11012) und Handel (Kauffenster) Fehlschlaege NUR in der
           Statuszeile.
VORSCHLAG: Regel: Absagen auf eigene Klicks -> Statuszeile + Fenster, NIE Postfach; Postfach nur fuer
           Dinge, die ohne Klick passieren. Gesperrte Forschungsknoepfe `state=tk.DISABLED`.
PATCH-PLAN: main.py Z. 15106 `self.state.messages.append(...)` loeschen, dafuer `messagebox.showinfo`
           (wenn root). Knopf der Forschung: Grund aus derselben Pruefung, die den Satz "gesperrt:" liefert.
TEST:      Klick auf gesperrte Forschung -> Postfachlaenge unveraendert.

NAECHSTER TEIL: 3/7 - Befunde S8 bis S18 und Messwerte.

==================================================================================================
TEIL 3/7 - Befunde S8-S18, Messwerte - Stand fa5834b
Bisher geliefert: Teil 0 (Protokoll), Teil 1 (Methode), Teil 2 (S1-S7).
==================================================================================================

S8 WALL-ANZEIGE - GEMESSEN (bestaetigt Antwort Teil 1)
BEFUND:    Wall steht (Stufe 1): auf der Karte nur "Dorfwall: Erdwall · Stufe 1 · Zustand 100%", KEINE
           Reparatur; im Dorfzentrum der volle Block. Vor der Forschung wird "Wall errichten (16 Holz,
           16 Stein)" angeboten; Klick -> nur Statuszeile "Zuerst Verteidigungsanlagen erforschen.".
VORSCHLAG/PATCH-PLAN: Antwort Teil 1, Schritte 1-8 (unveraendert gueltig).

S9 MARKTPLATZ OHNE ZUSTAND - GEMESSEN
BEFUND:    Waehrend die Karawane faehrt, zeigt der Marktplatz nichts davon (nur Dorfzentrum: "Handeln:
           Siedlung 1 → Haug · hinreise · noch 57.6 min"). Kauffenster: "Bot-Siedlung: angenommen auf Feld
           10/10 (Bots fuehren keine Koordinaten)" - aber die Bot-Doerfer STEHEN mit Feld auf der Weltkarte
           (`_bot_doerfer_im_raster`). Ablehnung nennt die Schwelle nicht ("Handel abgelehnt: Haug schickt
           die Karawane MIT den 10 Holz zurueck").
VORSCHLAG: Antwort Teil 2 (`handelslage`, Kasten "unterwegs") deckt Punkt 1; Punkt 2 als eigener
           Registereintrag "Handel nutzt Kartenmitte statt Bot-Dorf" (Ziel: `bot_standort` liest das
           Hauptdorf des Bots); Punkt 3: Ablehnungssatz um "(Schwelle X Gold je Stueck)" ergaenzen.

S10 PAKT OHNE ANZEIGE - GEMESSEN
BEFUND:    Nach "Pakt anbieten" verschwindet nur der Knopf; die Bot-Zeile zeigt weder "Pakt laeuft" noch
           Restzeit. Positiv gemessen: mit Pakt bei allen 5 Bots 0 Diebstaehle in 36 Spielstunden.
VORSCHLAG: In `_render_diplomacy` (Anker Z. 14080 `if _pakt_ok:`) ein `else`-Zweig: bei Grund
           `laeuft_bereits` Label "Pakt laeuft noch <minuten_text(rest)>"; Rest aus einer neuen
           Kernfunktion `diplomatie.vertrag_rest(bot_daten, "nichtangriff", jetzt)`. Passt zu Frage 18.

S11 WIRTSCHAFT: HOLZ-ENGPASS - GEMESSEN (nur Messwert, keine Aenderung)
BEFUND:    Spielstunde 73 (Tag 4): Holz 2, Stein 245, Mana 365, Nahrung 146, Leder 146. Forschung kostet
           nur Holz (50/100/200 je Stufe), ein Holzfaeller bringt 4,2/h. Baukunst 3 brauchte 40 Spielstunden,
           fast nur Wartezeit auf Holz. Stein/Mana/Leder haben frueh keinen Abnehmer.
VORSCHLAG: Daniel als Beobachtung melden, KEINE Zahl aendern. Ein Satz in "Dein naechster Schritt":
           "Holz ist dein Engpass - ein zweiter Holzfaeller lohnt sich" (Bedingung aus dem echten Lager).

S12 ENTWICKLERTEXTE IN SPIELERANSICHTEN - GEMESSEN (mit Datei:Zeile)
  * main.py Z. 11475 "Ortsbestand dieser Siedlung (lokal — führend seit Teil 3a)" -> "Lager dieser Siedlung"
  * main.py Z. 4798 "(führend seit Teil 3a)" -> streichen
  * main.py Z. 10101 "so hat Daniel es am 05.11.2026 entschieden" -> "so ist es fuer alle gleich"
  * main.py Z. 15204 "Ausgebildet wird auf der Siedlungskarte (W4b-5)." -> "(W4b-5)" streichen
  * main.py Z. 15369 "Bauten binden keine Siedler (Entscheidung 31.10.2026)" -> Klammer streichen
  * Siedlungskarte, Dorfuebersicht: "Bauten binden keine Siedler (Daniels Entscheidung 31.10.2026)" ->
    Klammer streichen (Fundstelle mit `grep -n "Daniels Entscheidung 31.10.2026)" src/main.py`)
  * main.py Z. 12071, 12327 "folgt mit S-6"; Z. 12335 "(S-5)"; Lager-Route "Schnitt S-2c", "data/items.json"
  * Dorfzentrum: "Siedlung 1 (kontinent)" zeigt die interne Karten-Id
  * Gilde Z. 14473-14477: erfundene Gilden mit Zahlen
  * spielerhilfe.py Z. 95 "Gründe im Dorfzentrum deine erste Siedlung" - gegruendet wird seit Register
    222 auf der Kartengruendungsseite -> "Gruende auf der Seite 'Kartengruendung' deine erste Siedlung"
TEST:      `tests/test_spielertexte.py` erweitern: kein `text=`-Literal in main.py enthaelt
           `Teil 3a`, `W4b-`, `S-\d`, `Entscheidung \d`, `Daniel`, `data/`.

S13 ZAHL- UND NAMENSFORMAT - GEMESSEN
BEFUND:    "Grom hat 28.51 Einheiten entwendet (1.18 holz, 4.36 leder ...)", "holz fehlt 134.72 (65.28
           von 200)", "Fehlt im Ortslager: holz 4.94", Ortsbestand "100.0 Holz". Punkt statt Komma, krumme
           Mengen, Rohstoff klein. Dorfzentrum hat 136 Textzeilen (davon 17 Waren mit "0").
VORSCHLAG: EINE Funktion `menge_text(wert)` neben `prozent_text` (ganze Zahl, wenn ganzzahlig, sonst eine
           Nachkommastelle mit Komma) und Rohstoffnamen ueber den vorhandenen Namen (gross). Waren mit 0
           im Dorfzentrum nicht auflisten ("keine Waren").

S14 "DEIN NAECHSTER SCHRITT" WAEHLT KEIN FELD - GEMESSEN
BEFUND:    Knopf "„Siedlung 1“ öffnen — Jäger bauen" oeffnet die Karte mit `karten_feld = None`; der Spieler
           muss den Wald selbst suchen.
VORSCHLAG: Der Schritt nennt schon Gebaeude und Gelaende - beim Oeffnen das erste freie passende Feld
           vorwaehlen (`self.karten_feld = i`), Rubrik passend setzen. Kern: `naechster_schritt()` liefert
           zusaetzlich `"feld"`.

S16 UNBEZAHLBARE EREIGNISWEGE - GEMESSEN
BEFUND:    Diplomatie zeigt "Haug verlangt Tribut" mit Knopf "990 Holz" bei 30 Holz im Lager; Klick ->
           "Es fehlt am Ort, was verlangt wird. Gebucht wurde nichts." Ehrlich, aber der Knopf luegt vorher.
VORSCHLAG: Knopf `state=tk.DISABLED`, wenn `diplomatie.ereignis_preis(...)` nicht gedeckt ist (Pruefung
           aus derselben Stelle, die beim Klick ablehnt).

S18 SPEICHERN - GEMESSEN
BEFUND:    Verlustfrei: Slot 1 sichern, 5 Spielstunden weiter, Slot 1 laden -> Spielzeit, Lager, Bauten,
           Forschung, Wall, Volk, Postfach, Schutz, Tag identisch. Aber nach "Sichern #1" stand in der
           Statuszeile "Willkommen in Nebelseetal." - keine Bestaetigung "in Slot 1 gespeichert".
VORSCHLAG: Nach erfolgreichem Sichern `self._log("Gespeichert in Slot N (Spieltag T).")` als LETZTE Zeile.

## Messwerte zum Nachpruefen (Startkarte "Das Z", Volk menschlich, x180)
* Start: 100 Holz, 100 Stein, 10 Siedler; Startgebaeude Holzfaeller, Steinmetz, Tempel.
* Ertrag nach Start: Holz 4,2/h (1 Holzfaeller, +5 % Volk), Stein 1,9/h, Mana 5/h (Tempel).
* Erste 24 Spielstunden: 0 Nachrichten (Goetterschutz). Nach Schutzende: 5 Diebstaehle je 12 Spielstunden.
* 10 Spieltage am Stueck: 13,6 s Rechenzeit in Opus' Umgebung, keine Ausnahme.

## Fragen an Daniel (aus diesem Test)
1. S2: Handels-Schwellenpreis je Rohstoff statt pauschal 300 Gold je Stueck?  -> ENTSCHIEDEN 17:52, siehe Teil 6
2. S3: Soll der Wall im Goetterschutz als Kriegspunkt zaehlen (Handbuch: ja)?  -> ENTSCHIEDEN 17:52, siehe Teil 6
3. Portal-Uhr (aus Antwort Teil 3): Echtzeit oder Spielzeit fuer die 24-Stunden-Sperre?  -> ENTSCHIEDEN 17:52, siehe Teil 6

## Tipp fuer Hermes
Der Ersatz-tkinter-Lauf braucht kein Fenster und keine GPU (10 Spieltage in Sekunden) und kann neben
einem Spieltest nicht stoeren, wenn er ihn nicht gleichzeitig laeuft. Wer ihn ins Projekt holen will:
Opus liefert ihn auf Daniels Wunsch als `tools/kopflos_spielen/` nach (rund 250 Zeilen, ASCII).

NAECHSTER TEIL: 4/7 - Opus-Mehrwert (gekennzeichnet).

==================================================================================================
TEIL 4/7 - OPUS-MEHRWERT (ausdruecklich gekennzeichnet) - Stand fa5834b
Bisher geliefert: Teil 0 (Protokoll), 1 (Methode), 2 (S1-S7), 3 (S8-S18).
==================================================================================================

> **Kennzeichnung:** Dieser Teil geht ueber den Auftrag hinaus. Er enthaelt Einschaetzungen, die ein
> groesseres Modell (Claude Opus 5.5, Thinking: Mittel) aus dem Zusammenhang des ganzen Spiels zieht.
> Es sind Empfehlungen, keine Messungen; jede ist als OPUS-EINSCHAETZUNG markiert. Hermes entscheidet,
> was davon in Auftraege wird. Fuer die Umsetzung durch `deepseek-flash` reichen Teil 2 und 3.

M1 OPUS-EINSCHAETZUNG - Die drei schweren Funde haben EINE gemeinsame Wurzel.
   S1 (Portal), S2 (Handelspreis), S3 (Wall beendet Schutz) und S4 (Berichte verschwinden) sind
   jeweils einzeln "richtig" - jede Funktion tut, was ihr Docstring sagt, und jede Wache ist gruen.
   Falsch ist das ZUSAMMENSPIEL: ein Wert aus Bereich A (Kaempferpreis, Wall-Kriegspunkte,
   Postfach-Frist in Spielsekunden) landet ungeprueft in Bereich B (Rohstoffhandel, Goetterschutz,
   Zeitfaktor x180). Solche Fehler findet kein Einzeltest, nur ein Durchspiel mit Messwerten.
   Empfehlung: neben dem Sammellauf EIN kopfloses Durchspiel (14 Spieltage, neuer Spieler) als feste
   Wache, die nur Kennzahlen prueft: Dorf steht nach Sprung auf der Zielwelt; 10 Holz kosten
   hoechstens X Gold (X von Daniel); Goetterschutz haelt bis Tag 7, wenn der Spieler nicht angreift;
   kein ungelesener Verlustbericht verschwindet. Laufzeit gemessen: rund 15 s ohne Fenster.

M2 OPUS-EINSCHAETZUNG - Zeitfaktor x180 als stille Fehlerquelle.
   Alles, was in Spielsekunden festgelegt ist, schrumpft fuer den Spieler um den Faktor 180:
   Postfach-Frist 1 Spieltag = 8 echte Minuten, Diebstahl alle 12 Spielstunden = 4 echte Minuten,
   Pakt 3 Spieltage = 24 echte Minuten. Gleichzeitig laufen Portal-Sperre und Umbenennen in ECHTZEIT
   (24 h). Der Spieler erlebt also zwei Uhren. Empfehlung: Daniel einmal eine Liste aller Fristen
   vorlegen (Spalten: Wert, Uhr, echte Dauer bei x180) und je Zeile entscheiden lassen. Werkzeug fuer
   Hermes: `grep -rn "sekunden\|stunden\|time.time()" data/*.json src/*.py` und daraus die Tabelle.

M3 OPUS-EINSCHAETZUNG - Warum Daniel "Handel nicht auffindbar" meldet, obwohl es einen Marktplatz gibt.
   Der Weg zum Handel hat vier Stufen, von denen der Spieler nur die letzte sieht: Baukunst ->
   Stellmacher bauen -> Wagenbau 2 erforschen -> Handelskarawane bauen (500 Holz, 250 Metall, 200 Gold,
   500 Wolle, 500 Leder, 10 Siedler, 15 Pferde, `data/units.json`) -> erst dann "Handeln". Gemessen:
   nach 14 Spieltagen hatte der Testspieler 0 Gold, 0 Metall, 0 Wolle, 0 Pferde. Danach kostet jedes
   Stueck Rohstoff 300 Gold (S2). Der Handel ist also nicht schlecht zu FINDEN, sondern fuer Wochen
   unerreichbar - die Marktplatz-Ansicht aus Antwort Teil 2 muss diesen Weg als Leiter zeigen
   ("Schritt 2 von 4: Stellmacher fehlt"), sonst bleibt die Note 5.

M4 OPUS-EINSCHAETZUNG - Reihenfolge fuer die naechste Sitzung (ersetzt Antwort Teil 5, T3).
   1. S4 (eine Datenzeile, sofort) - 2. S5, S6, S13-Teil "menge_text" (klein, sichtbar) -
   3. Punkt A Wall + S3-Warnung (gleiche Stelle) - 4. S1-Zwischenstand (Knopf weg) -
   5. Daniels drei Fragen einholen (S2, S3, Portal-Uhr) - 6. Punkt B Marktplatz mit M3-Leiter -
   7. Punkt C Portal-Umbau - 8. S12 Entwicklertexte in einem Zug mit Wache.
   Je Schritt eine EXE und ein kurzer Spieltest, nicht alles auf einmal.

M5 OPUS-EINSCHAETZUNG - Was Opus fuer Hermes kuenftig sinnvoll uebernehmen kann.
   Gut geeignet (spart `deepseek-flash` die meiste Arbeit): Durchspiele mit Messwerten wie dieses,
   Querschnittsfehler ueber mehrere Module (M1, M2), Patch-Plaene mit Ankern, Entscheidungsvorlagen
   fuer Daniel. Weniger geeignet: Bildschirmsteuerung auf diesem Laptop (gescheitert, Daniel will sie
   nicht mehr), Massenumbauten ohne Wache. Arbeitsweise-VORSCHLAG: Hermes schneidet den Auftrag,
   Opus liefert Plan + Messung, Hermes setzt um und misst nach - wie in `docs/ENTWICKLUNGSPROTOKOLL.md`
   17:35 (Register 313) festgelegt.

NAECHSTER TEIL: 5/7 - Steckbrief Opus fuer Hermes (wozu einsetzen, wie beauftragen).

==================================================================================================
TEIL 5/7 - STECKBRIEF: Claude Opus 5.5 fuer Hermes "Weltenfresser" (auf Daniels Wunsch, 17:46)
Bisher geliefert: Teil 0-4. Dieser Teil ist fuer Hermes' Auftragsformulierung gedacht.
==================================================================================================

Daniel: "Gib Hermes ... alle Daten ueber dich, damit er weiss wozu genau er dich verwenden kann und er
dies bei der Formulierung seiner Auftraege an dich beachten soll." Selbstauskunft von Opus; Werte mit
(H) hat Hermes selbst gemessen (Protokoll 17:35, Register 313), Werte mit (O) nennt Opus.

## 1. Eckdaten
| Punkt | Wert |
|---|---|
| Modell | Claude Opus 5.5 (Anthropic), Kennung `claude-opus-5-5` (O); Einstellung laut Daniel "Thinking: Mittel" |
| Zugang | Daniels Abo Claude Pro: Chat in claude.ai/Desktop-App UND Claude Code CLI (`claude -p ... --model opus`) (H) |
| Kosten | Pauschale 21,42 EUR/Monat, keine Abrechnung je Aufruf; kein `ANTHROPIC_API_KEY` gesetzt (H) |
| Grenzen des Abos | Nutzungslimits (Zeitfenster und Wochenkontingent); headless nicht ablesbar (H). Bei Erreichen: warten, nicht wiederholen |
| Kontext / Ausgabe | `contextWindow: 1000000`, `maxOutputTokens: 128000` im CLI-Lauf (H). Im Chat bricht Daniels WLAN lange Antworten ab -> Teile <= 150 Zeilen |
| Wissensstand | bis Juni 2026 (O); alles Spaetere nur aus dem Repo oder per Websuche |
| Gedaechtnis | keine Erinnerung zwischen Auftraegen, ausser was im Auftrag oder im Repo steht. Jeder Auftrag muss fuer sich lesbar sein |
| Sprache | Deutsch und Englisch gleich gut; Pruefdateien schreibt Opus ASCII-only |

## 2. Was Opus in DIESER Umgebung kann (heute gemessen)
* Oeffentliches GitHub-Repo klonen und lesen (geht, ohne Zugangsdaten).
* Daniels Laptop-Ordner lesen/schreiben NUR nach Daniels Freigabe je Ordner (heute: Projekt nur
  lesen, Desktop schreiben). Loeschen ist ohne eigene Freigabe gesperrt.
* Python in einer eigenen Linux-Umgebung (3.13): Spielkern rechnen, Durchspiele ohne Fenster,
  Messungen. NICHT: echtes tkinter, Windows-EXE, PyInstaller, `run_tests.bat`, Pakete nachladen.
* Websuche fuer Fakten nach Juni 2026.
* Bildschirmsteuerung auf diesem Laptop: gescheitert (graue Aufnahmen), Daniel will sie nicht mehr.
  -> NIE Auftraege mit "klick dich durch die EXE" stellen.

## 3. Wofuer Hermes Opus einsetzen soll (Staerken)
1. Querschnittsfehler ueber mehrere Module (Beispiel heute: Kaempferpreis wird Rohstoffpreis, S2).
2. Patch-Plaene mit Datei/Funktion/Ankerzeile fuer `deepseek-flash`.
3. Entscheidungsvorlagen fuer Daniel: Empfehlung - Grund - Preis des anderen Weges.
4. Kopflose Durchspiele mit Messwerten (14 Spieltage in Sekunden) und Code-Reviews grosser
   Funktionen (z. B. `_render_portal`, 16.000-Zeilen-`main.py` gezielt).
5. Texte fuer Spieler (Klartext, ohne Entwicklerkennungen) und Pruefideen (Wachen), die rot werden koennen.

## 4. Wofuer NICHT (Grenzen)
* Keine Windows-Verifikation: was Opus misst, ist Linux-Quellstand. Hermes prueft auf Windows nach
  (Regel aus `docs/HERMES_KONTROLLE_UND_SKILLS.md`: nichts als Windows-verifiziert bezeichnen).
* Kein Commit/Push, keine EXE, kein Sammellauf - das bleibt bei Hermes.
* Keine Zugangsdaten, Passwoerter, Tor-Dateien, Spielstaende von Daniel.
* Opus kann sich irren: jede Zahl und jeder Anker wird von Hermes gegen den Code gemessen (so wie
  im Auftrag vorgesehen). Heute selbst verworfen: 3 eigene Befunde beim Gegenpruefen.

## 5. So formuliert Hermes einen Auftrag an Opus (Vorlage)
```
AUFTRAG an Opus - <Thema> - Stand <Commit-Hash>
Ziel (1 Satz): ...
Daniels Wortlaut: "..."
Lesen (in Reihenfolge, mit Zeilenbereich): datei :: funktion, ...
Nicht anfassen / Daniels Regeln: ...
Liefern: BEFUND/VORSCHLAG/RISIKO/PATCH-PLAN/TEST | Entscheidungsvorlage | Messung
Umfang: hoechstens N Teile a 150 Zeilen; Ausgabe als Datei <Name> nach <Ordner>
Freigaben: Projekt nur lesen | Desktop schreiben
```
Hinweise fuer Hermes: (a) den Commit-Hash nennen - Opus vergleicht selbst mit GitHub; (b) lieber eine
klare Frage als zehn; (c) "Deine Meinung" ausdruecklich erbitten, wenn Daniel sie will; (d) mehr Kontext
schadet nicht (1 Mio. Token), aber Daniels WLAN begrenzt die ANTWORTlaenge; (e) im CLI-Weg
`--allowedTools "Read,Grep,Glob"` fuer reine Entwurfsauftraege, damit nichts still geaendert wird.

## 6. Kennzeichnung in Projektdateien
Alles von Opus Erarbeitete traegt im Kopf: "Erarbeitet von Claude Opus 5.5 (Thinking: Mittel, Claude
Pro), <Datum>". Uebernimmt Hermes Teile in Code oder Doku, steht im Protokoll "nach Entwurf Opus,
umgesetzt und gemessen von Hermes" - so bleibt sichtbar, wer was geprueft hat.

NAECHSTER TEIL: 6/7 - Daniels Entscheidungen von 17:52 und die Umsetzungsplaene.

==================================================================================================
TEIL 6/7 - DANIELS ENTSCHEIDUNGEN 08.11.2026, 17:52 - Umsetzungsplaene - Stand fa5834b
Bisher geliefert: Teil 0-5. Dieser Teil ersetzt die drei offenen FRAGEN aus S2, S3 und Antwort Teil 3.
==================================================================================================

Daniels Wortlaut (17:52): "zu Frage 1: Handelspreis je Rohstoff statt pauschal bitte; zu Frage 2: Wall
und Ausbau sollen den Goetterschutz beenden, da es eine kriegerische Vorbereitung ist; zu Frage 3: in
der Spielzeit ist glaub ich sinnvoller."
-> Hermes: bitte als Entscheidungen 17:52 in `docs/ENTSCHEIDUNGSVERZEICHNIS.md` und ins Protokoll.

E1 HANDELSPREIS JE ROHSTOFF (ersetzt FRAGE in S2)
BEFUND (OPUS-FUND, gemessen): Ein Preis je Rohstoff ist SCHON GEBAUT, wird aber vom Spielerhandel nicht
   benutzt. `spieloekonomie.schattenpreis(karte, rohstoff, bestand, reserve)` (Z. 249-259) rechnet den
   lokalen Goldwert eines Rohstoffs aus Kartenertrag und Vorrat; `botkern.oekonomie_angebot` (Z. 650-667)
   macht daraus mit `referenzpreis_aus_beschaffung` (x1,2) und `handelspreis` (Temperament +-10 %) das
   Angebot inkl. Reserve - und wird NIRGENDS aufgerufen (gemessen: `grep -rn "oekonomie_angebot(" src/`
   findet nur die Definition). Der Spielerhandel nimmt stattdessen pauschal 250 x 1,2 = 300 (main.py
   Z. 5190 und Z. 10583). Gemessen auf der Startkarte (Bestand 1000, Reserve 100, ohne Temperament):
   Holz 0,45 · Stein 0,45 · Nahrung 0,45 · Leder 0,60 · Metall 0,60 · Wolle 0,60 · Pferde 0,60 ·
   Mana 0,36 Gold je Stueck. Keine neue Zahl noetig: die Grenzen stehen schon als VORSCHLAG in
   `data/spieloekonomie.json` (`kartenpreisgrenzen`, `vorratspreisgrenzen`, `bots.*.reserve_stunden`).
VORSCHLAG: Spielerhandel auf `botkern.oekonomie_angebot` umstellen - EINE Preisfunktion fuer Bot-Handel
   und Spielerhandel; der Pauschalwert bleibt nur dort, wo er einen Kaempfer meint (`bots_tick`, Z. 7347).
RISIKO: Handel wird sehr billig (Faktor rund 670 guenstiger) - Daniel sollte die Hoehe im naechsten
   Spieltest beurteilen. `tests/test_handel_*` mit fest 300 werden rot und muessen den Preis aus der
   Funktion lesen. Bot verkauft nichts, wenn sein Bestand unter der Reserve liegt (gewollt, Docstring).
PATCH-PLAN:
  1. botkern.py :: neu hinter `oekonomie_angebot`: `def schwellenpreis_rohstoff(dorf_karte, rohstoff,
     bestand, temperament, stufe="mittel", tagesbedarf=0.0) -> Optional[float]`, ruft
     `oekonomie_angebot(stufe, dorf_karte, rohstoff, bestand, tagesbedarf, temperament, O.REGELN)` und
     gibt `["preis"]` zurueck. Hermes prueft: Herkunft von `tagesbedarf` je Bot (VORSCHLAG: aus
     `bot_bedarf.json`, sonst 0.0 und im Kommentar so benannt).
  2. main.py :: GameState :: Anker Z. 5190 `referenz = botkern.referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)`
     alt: zwei Zeilen Pauschalpreis. neu: `schwelle = self.bot_schwellenpreis(der_bot, vertrag["ware"])`.
  3. main.py :: GameState :: neue Methode `bot_schwellenpreis(bot, ware)`: Hauptdorf
     `bot_doerfer_sicherstellen(bot)[0]`, Karte `dorf.karte_daten or _bot_karte_dict(dorf.karte)` (Muster
     Z. 831), Bestand `bot.vorraete.get(ware, 0)`; Rueckgabe None = "verkauft nicht".
  4. main.py :: _handel_maske :: Anker Z. 10583 (dieselben zwei Zeilen) -> `self.state.bot_schwellenpreis(bot, ware)`;
     der Satz "Schwellenpreis" nennt den Preis der GEWAEHLTEN Ware und aendert sich mit der Auswahl;
     bei None: "Haug gibt Holz nicht ab (Vorrat unter seiner Reserve)".
TEST: NEU `tests/test_handelspreis_je_rohstoff.py` (ASCII): (a) Holz und Leder haben verschiedene
   Schwellen; (b) Kauf- und Pruefweg lesen dieselbe Zahl (Kaufvertrag zu Schwelle+0,01 wird angenommen,
   zu Schwelle-0,01 abgelehnt); (c) Bestand unter Reserve -> kein Angebot; (d) `grep`: main.py enthaelt
   `referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)` nur noch in `bots_tick`.

E2 WALL UND AUSBAU BEENDEN DEN GOETTERSCHUTZ (ersetzt FRAGE in S3)
BEFUND: Das ist schon so (gemessen, Teil 2 S3): Wallstufe hoch drei sind Kriegspunkte (`punkte.kriegspunkte`),
   der erste Kriegspunkt beendet den Schutz (main.py Z. 7785-7787). "Ausbau" ist mitgedeckt: jede hoehere
   Stufe gibt mehr Kriegspunkte. Erst `mauer_besetzt` zaehlt - die Forschung allein beendet nichts.
VORSCHLAG: Regel NICHT aendern, nur festschreiben und dem Spieler ansagen. Aus S3 entfaellt die
   Rueckfrage (`askyesno`); es bleibt ein Hinweis am Knopf: "Beendet den Goetterschutz - der Wall gilt
   als kriegerische Vorbereitung." (Text nach Daniels Wortlaut.)
PATCH-PLAN: (1) Label ueber dem Knopf "Wall errichten" (nach Antwort Teil 1 in `_wall_block`), nur solange
   `self.state.noob_protection`. (2) Meldung in main.py Z. 7791 ergaenzen: bei Grund "erster Kriegspunkt"
   und Wallstufe > 0 -> "Goetterschutz beendet (Wall errichtet - kriegerische Vorbereitung)".
TEST: NEU in `tests/test_wall_verteidigung.py`: Wall im Schutz errichten -> nach einem Takt
   `noob_protection is False` und die Meldung nennt den Wall. Damit ist Daniels Entscheidung als Wache
   gesichert und kann nicht still "repariert" werden.

E3 PORTAL-SPERRE IN SPIELZEIT (ersetzt FRAGE in Antwort Teil 3)
BEFUND: Echtzeit an vier Stellen: main.py Z. 11742 (`_sperre_text`), Z. 11774 und Z. 11779
   (`_portal_wechsel`: `wechsel_erlaubt(..., time.time())`, `nach_wechsel(mana, time.time())`), Z. 12343
   (Sperrzeile in `_render_portal`). `letzter_wechsel` wird gespeichert (Z. 7848) und geladen (Z. 8092).
OPUS-HINWEIS (Folge, bitte Daniel kurz bestaetigen lassen): 24 Spielstunden sind bei x180 nur
   **8 echte Minuten**. Die Sperre "einmal binnen 24 Stunden" (portal.php 2005) wirkt damit kaum noch;
   der Preis von 5000 Mana bleibt die eigentliche Bremse. Das ist stimmig mit dem uebrigen Spiel
   (alles laeuft in Spielzeit), aber Daniel schrieb "glaub ich".
RISIKO (OPUS-FUND): Alte Spielstaende tragen in `letzter_wechsel` einen ECHTZEIT-Stempel (rund
   1.790.000.000 s). Gegen `spielsekunden` (wenige Hunderttausend) gerechnet waere die Sperre JAHRZEHNTE
   lang aktiv - jeder Spieler mit einem frueheren Sprung koennte nie wieder springen.
PATCH-PLAN:
  1. main.py :: _portal_wechsel :: Z. 11774 und Z. 11779: `time.time()` -> `float(self.state.spielsekunden)`.
  2. main.py :: _render_portal :: Z. 12343 und `_sperre_text` Z. 11742: dasselbe; Text "noch X h" ->
     "noch X Spielstunden (real <Minuten bei aktuellem Tempo>)", Umrechnung in einer Hilfsfunktion neben
     `minuten_text`, nicht in der Ansicht (AST-Wache!).
  3. main.py :: load :: Anker Z. 8092 `self.letzter_wechsel = data.get("letzter_wechsel")`: dahinter
     Altstand-Reparatur: ist der Wert groesser als `self.spielsekunden + 86400`, dann `None` und eine
     Systemnachricht "Portal-Sperre auf Spielzeit umgestellt - alter Zeitstempel verworfen.".
  4. portalraum.py :: wechsel_erlaubt :: Meldung "Erst nach 24 Stunden" -> "Erst nach 24 Spielstunden".
     `_STUNDEN_SPERRE` bleibt 24 (belegt, `data/welten.json`).
  5. Im spaeteren Umbau (Antwort Teil 3, `dorf_versetzen_pruefen`) den Parameter `jetzt_echt` streichen
     und `self.spielsekunden` nehmen.
TEST: NEU `tests/test_portal_spielzeit.py` (ASCII): (a) Sprung bei Spielsekunde 0, zweiter bei 86.399 ->
   gesperrt, bei 86.400 -> erlaubt (Mana jeweils aufgefuellt); (b) Spielstand mit `letzter_wechsel =
   1.79e9` laden -> `None`, Sprung moeglich; (c) AST: `_portal_wechsel`, `_sperre_text`, `_render_portal`
   enthalten kein `time.time()`.

Protokollzeile fuer Hermes:
| 17:52 | **Daniels Entscheidungen zu drei Opus-Fragen** | (1) Handelspreis je Rohstoff statt pauschal 300 - Umsetzung ueber den vorhandenen, bisher ungenutzten `botkern.oekonomie_angebot` (Opus-Fund); (2) Wall und Ausbau beenden den Goetterschutz als kriegerische Vorbereitung - Ist-Zustand, wird per Wache festgeschrieben, Spieler bekommt Hinweis; (3) Portal-Sperre in Spielzeit - vier `time.time()`-Stellen, Altstand-Reparatur noetig. Plaene: `Weiterer_Spieltest_08.11.26.md` Teil 6. Erarbeitet von Claude Opus 5.5 (Thinking: Mittel, Claude Pro). |

NAECHSTER TEIL: 7/7 - Tipps fuer Testlaeufe und Balancing-Tests (Opus-Vorschlaege).

==================================================================================================
TEIL 7/7 - TIPPS FUER HERMES: Testlaeufe und Balancing klueger strukturieren (OPUS-VORSCHLAEGE)
Bisher geliefert: Teil 0-6. Auf Daniels Wunsch 17:55. Alles hier ist VORSCHLAG, nichts ist gebaut.
==================================================================================================

> **Kennzeichnung:** OPUS-EINSCHAETZUNG (Claude Opus 5.5, Thinking: Mittel). Gebaut auf dem, was es im
> Projekt schon gibt (gelesen: `tools/balance_kreis.py`, `data/sollkurve.json`, `data/regelkreis.json`,
> `tests/test_durchspiel.py`, `docs/HERMES_KONTROLLE_UND_SKILLS.md`). Grundsatz aus Hermes' Regeln:
> nichts doppelt anlegen, vorhandene Werkzeuge erweitern, eine Chronik, Admin-Testbarkeit je Funktion,
> Ursache -> Abstellung -> Test -> Skillregel. Hermes entscheidet, welche Tipps zu Skills werden.

## A. Testlaeufe: drei Stufen statt "immer alles" (spart auf 2 Kernen am meisten)

| Stufe | Wann | Inhalt | Dauer (Messwert/Schaetzung) |
|---|---|---|---|
| 1 Nachbartests | nach JEDEM Patch | nur Pruefdateien, die eine geaenderte Funktion beim Namen nennen | Schaetzung 1-2 min |
| 2 Kennzahl-Durchspiel | nach jedem fertigen Punkt (A, B, C ...) | 14 Spieltage neuer Spieler, prueft nur Kennzahlen (Teil 4, M1) | gemessen ~15 s (ohne Fenster) |
| 3 Sammellauf | vor jeder EXE, NIE waehrend Daniels Spieltest | alle 203 Dateien, `-j 2` | gemessen ~11 min |

T1 Nachbartests automatisch waehlen (Umsetzung):
   neues Werkzeug `tools/nachbartests.py` (read-only): `git diff --name-only` + `git diff -U0` -> Namen der
   beruehrten `def`-Bloecke (per `ast`, Zeilenbereiche) -> `grep -l` dieser Namen in `tests/*.py` -> diese
   Dateien nacheinander starten. Immer dazu: `test_quelle_ast`, `test_daten_und_quellen`, `test_spielertexte`
   (die Querschnittswachen). Rueckgabe: Liste + Ergebnis je Datei. Kein Ersatz fuer Stufe 3.
T2 Reihenfolge im Sammellauf: zuletzt rote und zuletzt geaenderte Dateien ZUERST starten, langsamste
   zuletzt. Ein Fehler kommt dann nach Sekunden statt nach Minuten; Abbruch frueh moeglich
   ("fail fast" als Option, nicht als Standard - der volle Bericht bleibt Pflicht vor der EXE).
T3 Schonung: Sammellauf und EXE-Build mit niedriger Prozessprioritaet starten (Windows:
   `start /low /wait ...` oder `psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)`), vorher freien
   RAM UND freien Plattenplatz pruefen und ins Protokoll schreiben (Regel steht schon im Hardware-Rahmen;
   Nebenbefund heute: die Desktop-App meldete fuer ihre Arbeitsumgebung zu wenig freien Plattenplatz).

## B. Balancing: die vorhandene Sollkurve misst den idealen Spieler - das echte Spiel weicht ab

T4 OPUS-FUND (gelesen): `tools/balance_kreis.py` spielt laut Kopf den Idealplan ohne Bots, ohne Diebstahl
   und ohne Forschungskosten ("research.json - KOSTEN stehen nicht darin"). Gemessen im echten Spiel:
   (a) Forschung kostet Holz (50/100/200) und war DER Engpass (Baukunst 3 erst nach 40 Spielstunden);
   (b) nach Schutzende fehlen alle 12 Spielstunden rund 10 % der Lager (5 Bots je 3 %, Teil 2 S3/S4);
   (c) der Wall beendet den Schutz frueh (jetzt Daniels Regel E2). Die Sollkurve ist damit zu optimistisch,
   und der Regelkreis wuerde Preise SENKEN wollen, obwohl der Spieler eigentlich bestohlen wird.
   Vorschlag: in `data/regelkreis.json` unter `messung` ein Feld `stoerungen` ("keine" | "diebstahl" |
   "voll") und in `balance_kreis.messung` durchreichen; Sollkurve bleibt das Ideal, die Messung zeigt
   den Abstand zur Wirklichkeit. Zahlen nur aus vorhandenen Daten (`bot_diebstahl.json`).
T5 Spielerprofile statt eines Stils: neben `stil: "breit"` zwei Profile messen, die echte Spieler
   machen: "forscher" (Bibliothek zuerst, Holz in Forschung) und "verteidiger" (frueh Wall - beendet
   seit E2 den Schutz). Daniel spielt eher wie "verteidiger" (Spieltest 2/3: Wall gesucht). Ergebnis je
   Profil in derselben Tabelle, damit Balance nicht nur fuer EINEN Weg stimmt.
T6 Meilensteine statt nur Punkte je Tag: zusaetzlich die SPIELSTUNDE messen, in der erreicht wird:
   erste Bibliothek, Baukunst 3, erster Wall, erste Einheit, Handelskarawane, zweite Siedlung. Dazu je
   Phase der Engpass-Rohstoff (kleinster Vorrat gemessen am naechsten Preis) und "Stau" (Rohstoff, der
   3 Tage nur waechst). Heute gemessen: Engpass Holz, Stau Stein/Mana/Leder. Das zeigt Daniel in einer
   Zeile, WO das Spiel zaeh ist - Punkte je Tag zeigen nur DASS.
T7 Determinismus pruefen (Hinweis, bitte messen): `bots_tick` wird mit `rng = random.Random()` ohne Saat
   aufgerufen (main.py Z. 7345), ebenso Kaempfe (Z. 6025, 6650). Laeuft die Balancemessung ueber diesen
   Weg, sind die Saaten 1..10 aus `regelkreis.json` nicht voll wirksam. Probe: denselben Lauf zweimal
   mit Saat 1 -> identische Tagesstaende? Wenn nein: Saat nur im Mess-/Admin-Weg durchreichen (z. B.
   Umgebungsvariable `NEBEL_TEST_SAAT`), Spielmechanik unveraendert - genau das verlangt die
   Admin-Testbarkeits-Regel FIX04d (an/aus, reproduzierbar, ohne Mechanik zu verfaelschen).
T8 Streuung berichten: je Kennzahl Median UND Spannweite der 10 Saaten. Ein Mittelwert allein versteckt
   Laeufe, in denen der Spieler verhungert oder leergestohlen wird.
T9 Zeitfaktor-Tabelle als Wache (aus Teil 4, M2): `tools/fristen_tabelle.py` listet jede Frist aus
   `data/*.json` und jede `time.time()`-Stelle in `src/` mit "Uhr" und "echte Dauer bei x180". Neue Frist
   ohne Eintrag -> Befund (Muster `test_daten_und_quellen` mit Bestand).

## C. Wachen, die wirklich etwas fangen

T10 Spielfolge-Wache je kostenpflichtigem Knopf (Lernregel aus Teil 0): nicht "Rueckgabe True", sondern
   "danach steht X dort, wo der Spieler es erwartet" (Dorf auf Zielwelt, Ware im Lager, Pakt sichtbar).
T11 Gegenprobe fuer Kennzahl-Wachen (wie es `test_quelle_ast` schon vormacht): eine Kopie der Daten mit
   absichtlich falschem Wert (z. B. Handelspreis x1000) muss die Wache ROT machen - sonst prueft sie nichts.
T12 Spieltest-Anleitungen fuer Daniel: je Schritt zuerst "Wo wuerdest du das suchen?" und "wie viele
   Minuten hat es gedauert?", erst dann der Weg. EINE Aenderung je EXE, damit jede Note einem Umbau gehoert.

## D. Wie Hermes das in seine Skills uebernimmt (ohne Dopplung)
* Zuerst pruefen, ob eine bestehende Regel es schon abdeckt (Hermes' eigene Regel). Neu waeren nach
  meinem Lesen nur drei Saetze: (1) "Drei Teststufen: Nachbartests nach Patch, Kennzahl-Durchspiel nach
  Punkt, Sammellauf vor EXE." (2) "Kostenpflichtige Knoepfe brauchen eine Spielfolge-Wache." (3)
  "Balancemessungen laufen mit Saat und Stoerungsprofil und berichten Median und Spannweite."
* Ergebnisse in die VORHANDENEN Orte: Messwerte in die bestehende Messwert-Ablage (`test_messwerte_schreiben`),
  Entscheidungen ins Entscheidungsverzeichnis, Verlauf ins Entwicklungsprotokoll - keine neue Statusdatei.
* Arbeitsteilung: Hermes (`deepseek-flash`) baut T1, T2, T3, T9 selbst (klar umrissen, viel Handarbeit);
  fuer T4-T8 (Profile, Stoerungen, Kennzahlen) zuerst einen Opus-Auftrag "Entwurf + Messplan" stellen und
  Daniel die Kennzahl-Grenzen entscheiden lassen - dort steckt die Urteilsarbeit.

Protokollzeile fuer Hermes:
| 17:55 | **Opus-Vorschlaege fuer Testlaeufe und Balancing (Teil 7 des Nachtrags)** | Drei Teststufen (Nachbartests / Kennzahl-Durchspiel ~15 s / Sammellauf ~11 min), Nachbartest-Werkzeug, niedrige Prioritaet; Balancing: Sollkurve ohne Diebstahl/Forschungskosten zu optimistisch (Opus-Fund), Stoerungsprofil, Spielerprofile, Meilensteine, Saat-Probe (`random.Random()` ohne Saat in `bots_tick`), Median+Spannweite; drei Skill-Saetze ohne Dopplung. Alles VORSCHLAG. Erarbeitet von Claude Opus 5.5 (Thinking: Mittel, Claude Pro). |

ENDE NACHTRAG 1. Erarbeitet von Claude Opus 5.5 (Thinking: Mittel, Claude Pro), 08.11.2026.
