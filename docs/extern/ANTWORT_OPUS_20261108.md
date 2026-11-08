# ANTWORT Opus 5.5 auf AUFTRAG_CLAUDE_20261108 - Nebelseetal Remake

> Erarbeitet von Claude Opus 5.5 (Thinking: Mittel, Claude Pro), 08.11.2026, 17:09-17:24.
> Kosten: nur Abo-Pauschale, kein API-Verbrauch. Erweitert durch NACHTRAG 1:
> `Weiterer_Spieltest_08.11.26.md` (Spieltest, Protokolleintraege fuer Hermes, Steckbrief Opus).

Gelesen: GitHub `main` (Kopf f4eaf7c; `git diff fa5834b f4eaf7c` aendert nur `docs/`, der Code ist
also fa5834b). Daniels lokale `src/main.py` (D:\Arbeiten\..., Stand 15:46) ist zeichengleich mit
GitHub (Zeilenenden ignoriert). Auf Daniels Rechner wurde NUR gelesen, nichts geaendert, nichts
gestartet. Alle Zeilennummern = `src/main.py` in diesem Stand, sonst steht die Datei dabei.

Fuenf Teile, je unter 150 Zeilen. Wer nur einen Teil bekommt, kann ihn allein umsetzen.

==================================================================================================
TEIL 1/5 - Punkt A: Wall in die Siedlungskarte, Rubrik Verteidigung - Stand fa5834b
Bisher geliefert: nichts (erster Teil).
==================================================================================================

BEFUND:
  1. `_render_overview` Z. 9732-9764: kompletter Wall-Kasten (kennwerte, `_mauer_reparatur_block`,
     Knopf "Zur Siedlungskarte").
  2. `_render_settlement_map` Z. 11505-11519: Wallzeile + Knopf "Wall errichten / Wache besetzen".
     Sie wird NACH `kartenblock` gepackt, steht also UNTER der Karte. Der Text Z. 11640 sagt
     "Er wird oberhalb der Karte ... errichtet" -> falsche Auskunft.
  3. TOTER CODE Z. 11639-11646: in der Rubrik "Verteidigung" steht `return` VOR
     `self._mauer_reparatur_block(info, siedlung)`. Die Reparatur ist auf der Karte nie sichtbar
     gewesen - nur deshalb musste sie in Test 2 ins Dorfzentrum.
  4. Die Rubrikwahl (Z. 11618-11637) liegt HINTER `if feld is None: ... return` (Z. 11543-11553).
     "Verteidigung" ist nur erreichbar, wenn man vorher ein Feld anklickt - obwohl der Wall kein
     Feld belegt. Das ist der eigentliche Grund fuer "sehr unuebersichtlich".
  5. `_karten_bauen` Z. 10953: Meldung "im Dorfzentrum 'Wall errichten' waehlen" - der Knopf war
     dort nie (er steht auf der Karte). Falsche Auskunft schon heute.
  6. `_karten_wall_errichten` Z. 11007-11014: Fehlschlag (z. B. "Zuerst Verteidigungsanlagen
     erforschen") geht nur in `_log` = Statuszeile. `_mauer_reparatur_anklicken` zeigt dagegen
     ein Fenster. Stiller Ausfall.
  7. Gemessen: in `data/buildings.json` hat die Rubrik "Verteidigung" genau EIN Gebaeude
     (`verteidigungswall`). Beleg fuer Daniels Wunsch: `data/buildings.json` Z. 21
     ("Ausbau der Verteidigungsanlagen erfolgt im Bereich Verteidigung").

VORSCHLAG: Eine neue Methode `_wall_block(eltern, siedlung)` zeichnet ALLES zum Wall und erscheint
nur in der Rubrik Verteidigung der Siedlungskarte - ohne Feldwahl; das Dorfzentrum behaelt eine
Zeile mit Knopf "Wall verwalten", der die Karte direkt in der Rubrik Verteidigung oeffnet.
Verworfen: Kasten im Dorfzentrum lassen und zusaetzlich auf der Karte - zwei Orte, Daniel will einen.

RISIKO: `tests/test_spieltest2_befunde.py` Abschnitt 1 und `tests/test_gpt_wall_gui.py` pruefen den
alten Ort und werden rot - sie muessen im SELBEN Schritt umgestellt werden (siehe TEST).

PATCH-PLAN:
  1. main.py :: _render_settlement_map :: Anker Z. 11618 `# FIX04: Der historische Screenshot nennt`
     alt: Block Z. 11618-11637 (Kommentar, `kategorien = ...`, SPIELERHILFE-Label, Zeile
          "Baubereich:", OptionMenu) steht nach der Feldpruefung.
     neu: denselben Block UNVERAENDERT verschieben direkt hinter Z. 11541
          `self._dorf_uebersicht_zeichnen(kartenblock, siedlung)`, also VOR
          `feld = getattr(self, "karten_feld", None)`. Direkt darunter einfuegen:
            if kategorie == "Verteidigung" and self.state._lokale_kasse_aktiv():
                self._wall_block(info, siedlung)
                return
  2. main.py :: _render_settlement_map :: Anker Z. 11639
     `if kategorie == "Verteidigung" and self.state._lokale_kasse_aktiv():`
     alt: der 8-Zeilen-Block bis einschliesslich dem zweiten `return` (Z. 11646).
     neu: loeschen (ersetzt durch Schritt 1; enthaelt den toten Code).
  3. main.py :: _render_settlement_map :: Anker Z. 11505 `# Dorfmauer ist Zustand der Siedlung`
     alt: Block Z. 11505-11519 (wallzeile + Knopf).
     neu: loeschen.
  4. main.py :: NebelseetalApp :: Anker `def _mauer_reparatur_block(self, eltern, siedlung):`
     neu: DAVOR zwei Methoden einfuegen (Skizze, 15 Zeilen):
       def _wall_kurztext(self, siedlung) -> str:
           w = dorfwall.kennwerte(siedlung, self.state.research)
           if not w["stufe"]:
               return "Dorfwall: noch nicht errichtet"
           return "Dorfwall: %s · Stufe %d · Zustand %.0f %%" % (
               w["name"], w["stufe"], w["zustand_prozent"])

       def _wall_block(self, eltern, siedlung):
           tk.Label(eltern, text=self._wall_kurztext(siedlung), ...gold, bold...).pack(...)
           if not siedlung.mauer_besetzt:
               preis = kosten_text(baukosten("verteidigungswall"))
               tk.Button(eltern, text=f"Wall errichten / Wache besetzen ({preis})",
                         command=self._karten_wall_errichten, ...).pack(...)
           if dorfwall.kennwerte(siedlung, self.state.research)["stufe"]:
               self._mauer_reparatur_block(eltern, siedlung)
       Den erklaerenden Satz "Die Stufe kommt aus der Forschung 'Verteidigungsanlagen' ..." aus
       Z. 9748-9749 woertlich als Label in `_wall_block` uebernehmen (Daniels Frage "wo ausbauen").
  5. main.py :: NebelseetalApp :: Anker `def _oeffne_siedlungskarte(self, siedlung):` (Z. 10829)
     neu: DAHINTER einfuegen:
       def _oeffne_verteidigung(self, siedlung):
           self._karten_baukategorie = "Verteidigung"
           self._oeffne_siedlungskarte(siedlung)
  6. main.py :: _render_overview :: Anker Z. 9732 `# ---- Dorfwall im Dorfzentrum (Daniels`
     alt: Block Z. 9732-9764 (bis einschliesslich `pady=(4, 8))` des Knopfes "Zur Siedlungskarte").
     neu: (Kommentar: "Daniel 08.11.2026, Test 3: Wall gehoert in die Karte unter Verteidigung")
       if _wall_ort is not None and self.state._lokale_kasse_aktiv():
           zeile = tk.Frame(self.content, bg=self.skin["panel"]); zeile.pack(fill=tk.X, padx=10)
           tk.Label(zeile, text=self._wall_kurztext(_wall_ort), ...).pack(side=tk.LEFT, padx=8)
           tk.Button(zeile, text="Wall verwalten",
                     command=lambda o=_wall_ort: self._oeffne_verteidigung(o), ...
                     ).pack(side=tk.RIGHT, padx=8, pady=3)
       (`_wall_ort = self.state.aktive_siedlung()` davor bleibt.)
  7. main.py :: _karten_bauen :: Anker Z. 10953
     alt: "Wall belegt kein Baufeld: im Dorfzentrum 'Wall errichten' wählen."
     neu: "Wall belegt kein Baufeld: Siedlungskarte, Baubereich 'Verteidigung', 'Wall errichten'."
  8. main.py :: _karten_wall_errichten :: Anker Z. 11012 `self._log(text)`
     neu: dahinter `if not ok and getattr(self, "root", None) is not None:`
          `messagebox.showinfo("Dorfwall", text)` (Muster `_mauer_reparatur_anklicken`).

TEST:
  * `tests/test_spieltest2_befunde.py` Abschnitt 1 neu: `_render_overview` enthaelt
    "_oeffne_verteidigung" und enthaelt NICHT "_mauer_reparatur_block(" und NICHT
    "dorfwall.kennwerte("; `_wall_block` enthaelt "_mauer_reparatur_block(", "Wall errichten" und
    "Verteidigungsanlagen".
  * `tests/test_gpt_wall_gui.py` Z. ~56: vor `self.app._render_settlement_map()` die Zeile
    `self.app._karten_baukategorie = "Verteidigung"` und `self.app.karten_feld = None` - beweist
    zugleich, dass KEIN Feld noetig ist. Die drei assertEqual danach bleiben unveraendert.
  * NEU `tests/test_wall_verteidigung.py` (ASCII): (a) im ganzen Quelltext ruft genau EINE Methode
    `_mauer_reparatur_block(` auf, und sie heisst `_wall_block` - EINE Anzeige; (b) GUI: Ort mit
    Wallstufe >= 1, `karten_feld = None`, Rubrik Verteidigung -> Text "Mauer: Stufe" wird
    gefunden; (c) Rubrik "Produktion", `karten_feld = None` -> KEIN Knopf "Wall errichten".
  * `tests/test_quelle_ast.py` muss gruen bleiben: `_wall_kurztext` formatiert nur, rechnet nicht.

NAECHSTER TEIL: 2/5 - Punkt B Marktplatz.

==================================================================================================
TEIL 2/5 - Punkt B: Handel auffindbar machen - Stand fa5834b
Bisher geliefert: Teil 1 (Wall in Rubrik Verteidigung, Patch-Plan mit 8 Schritten).
==================================================================================================

BEFUND:
  1. `_render_market` Z. 14453-14462: Titel, "Handle mit anderen Spielern oder Bots." (falsch:
     Einzelspieler), je Bot Name + "Handeln"; `if bot.trading <= 0.3: continue`.
  2. DOPPELTER RECHENWEG + WACHENLUECKE: die Grenze 0.3 steht VIERMAL ohne Namen und ohne Quelle:
     Z. 4957 (`handel_mit_bot`), Z. 5084 (`verkauf_an_bot`), Z. 14277 (`_trade`), Z. 14457
     (`_render_market`). `test_daten_und_quellen` sieht sie nicht (nur Konstanten mit Balance-Wort
     im Namen), `test_quelle_ast` auch nicht (nur Vergleiche gegen GANZZAHLEN > 1).
  3. Die Bausteine fuer "was brauche ich" existieren schon im Kern, die Ansicht nutzt sie nicht:
     `GameState.handelskarawanen_bestand(siedlung)` Z. 4876; laufender Handel steht in
     `state.auftraege` mit `"fremdvertrag": True` (`spieloekonomie.py` Z. 1779) und ist ueber
     `auftraege.laufende(...)` + `auftraege.stand(e, jetzt)` lesbar; die Voraussetzung der Karawane
     liefert `spieloekonomie.einheit_bedingungen(ort, "Handelskarawane", forschungs_stufen)` (dieselbe
     Lesestelle wie `_ausbildungs_bedingungen` Z. 15478). Laut `data/units.json`: Gebaeude
     Stellmacher, Forschung Wagenbau Stufe 2, Ladung 1000 - die Ansicht soll das LESEN, nicht abschreiben.
  4. Diplomatie zeigt "Handeln" bei JEDEM Bot (Z. 14084), auch bei Krank (trading 0.0, Z. 3458) -
     dort scheitert der Klick nur in der Statuszeile. Daniel hat zuerst in Diplomatie gesucht.

VORSCHLAG: Eine Kernfunktion `GameState.handelslage(siedlung)` liefert Haendler, Karawanen,
laufende Handel und offene Bedingungen; `_render_market` zeigt daraus drei Kaesten in fester
Reihenfolge: "So handelst du" - "Deine Handelskarawanen" - "Handelspartner".
Verworfen: Hinweistexte direkt in `_render_market` zusammensetzen - die Ansicht wuerde wieder
selbst entscheiden, was fehlt (genau das verbietet eure Quellwache).

RISIKO: Wer heute ohne Karawane auf "Handeln" klickt, bekommt die Maske mit Fehlermeldung; nach dem
Umbau sieht er statt Knopf den Grund - ein Test, der den Knopf bei jedem Bot zaehlt, wird rot.

PATCH-PLAN:
  1. main.py :: Modulebene :: Anker Z. 3459 `]` (Ende der Liste `BOTS = [`)
     neu: dahinter
       HANDELSNEIGUNG_GRENZE = 0.3   # VORSCHLAG Remake, kein Handbuchwert: darunter handelt ein Bot nicht

       def bot_handelt(bot) -> bool:
           """EINE Stelle fuer die Handelsgrenze (vorher viermal 0.3 im Code)."""
           return float(getattr(bot, "trading", 0.0) or 0.0) > HANDELSNEIGUNG_GRENZE
  2. main.py :: Z. 4957, 5084, 14277 :: Anker `if float(bot.trading) <= 0.3:`
     alt: `if float(bot.trading) <= 0.3:`   neu: `if not bot_handelt(bot):`
  3. main.py :: GameState :: Anker `def handelskarawanen_bestand(self, siedlung: Settlement)`
     neu: DAHINTER (nach deren `return bestand`) einfuegen (Skizze):
       def handelslage(self, siedlung) -> dict:
           jetzt = float(self.spielsekunden)
           unterwegs = [e for e in auftraege.laufende(self.auftraege, jetzt) if e.get("fremdvertrag")]
           try:
               bed = spieloekonomie.einheit_bedingungen(siedlung, "Handelskarawane",
                                                         self.forschungs_stufen())
           except (ValueError, KeyError, TypeError):
               bed = []
           return {"karawanen": self.handelskarawanen_bestand(siedlung) if siedlung else {},
                   "unterwegs": [{"bot": e.get("bot"), "ware": e.get("ware"), "menge": e.get("menge"),
                                  "phase": auftraege.stand(e, jetzt)[0],
                                  "rest_text": minuten_text(auftraege.stand(e, jetzt)[1])}
                                 for e in unterwegs],
                   "bedingungen": bed,
                   "haendler": [{"bot": b, "handelt": bot_handelt(b)} for b in self.bots]}
  4. main.py :: _render_market :: Anker Z. 14455 `text="Handle mit anderen Spielern oder Bots."`
     alt: ganze Methode Z. 14453-14462.
     neu: Titel bleibt "Marktplatz". Darunter, alles aus `lage = self.state.handelslage(ort)`
          (`ort = self.state.aktive_siedlung()`; ohne Ort: eine Zeile "Erst eine Siedlung gruenden"):
       Kasten 1 "So handelst du": eine Zeile, fester Text: "Handel laeuft ueber eine
         Handelskarawane: sie faehrt die Ware zum Bot, der Preis steht beim Angebot fest; lehnt er
         ab, kommt die Karawane mit der Ware zurueck." (Inhalt belegt: Handbuch S. 20, wie im
         Kommentar Z. 4870-4874 zitiert.)
       Kasten 2 "Deine Handelskarawanen": `lage["karawanen"]` als "Handelskarawane x2" oder
         "keine"; danach je `lage["unterwegs"]` eine Zeile "unterwegs zu <bot>: <menge> <ware>,
         <phase>, noch <rest_text>". Wenn KEINE Karawane: jede Bedingung aus
         `lage["bedingungen"]` als Zeile mit "erfuellt"/"fehlt" + Knopf "Zum Stellmacher"
         (`self._switch_view("Stellmacher")`), nur wenn die Route im Menue steht.
       Kasten 3 "Handelspartner": ALLE Bots. `handelt` False -> Name + "handelt nicht
         (Handelsneigung <prozent_text>)" statt Knopf. `handelt` True und Karawane vorhanden ->
         Knopf "Handeln" (`self._trade(b)`). `handelt` True ohne Karawane -> Text "erst eine
         Handelskarawane ausbilden".
  5. main.py :: _render_diplomacy :: Anker Z. 14084 `tk.Button(frame, text="Handeln", command=lambda b=bot: self._trade(b)`
     alt: Knopf bei jedem Bot.
     neu: `tk.Button(frame, text="Zum Marktplatz", command=lambda: self._switch_view("Marktplatz"), ...)`
          - EIN Handelsort, Diplomatie verweist dorthin (Daniel hat hier zuerst gesucht).
  6. Menue: Name "Marktplatz" bleibt (Routen-Name, `test_baseline` besucht jede Route; gemessen:
     er steht NICHT in `data/menue_original.json`). Stattdessen Unterzeile unter dem Titel:
     "Hier handelst du mit den Bots - Ware gegen Gold, per Handelskarawane."

TEST:
  * NEU `tests/test_marktplatz_lage.py` (ASCII): (a) `grep`-Pruefung: das Literal `0.3` kommt in
    `src/main.py` genau EINMAL vor (in `HANDELSNEIGUNG_GRENZE`); (b) `handelslage` ohne Karawane:
    `karawanen == {}` und mindestens eine Bedingung mit `erfuellt is False`; (c) mit einer
    Handelskarawane im Ortslager: `karawanen` nennt sie; (d) GUI: `_render_market` zeigt fuer
    JEDEN Bot eine Zeile (auch Krank), und "Handeln"-Knoepfe nur fuer `bot_handelt` UND Karawane;
    (e) AST: `_render_market` enthaelt kein `.trading` (die Grenze wird nicht in der Ansicht gelesen).
  * Bestehend gruen halten: `test_handel_transaktion`, `test_handel_spielschicht`, `test_quelle_ast`.

NAECHSTER TEIL: 3/5 - Punkt C Portal.

==================================================================================================
TEIL 3/5 - Punkt C: Portal - Dorf und Ziel per Klick auf die Weltkarte - Stand fa5834b
Bisher geliefert: Teil 1 (Wall), Teil 2 (Marktplatz, Kern `handelslage`, Grenze 0.3 an einer Stelle).
==================================================================================================

BEFUND (das Wichtigste zuerst - hier steckt ein echter Fehler, nicht nur Bedienung):
  1. `_portal_wechsel` Z. 11747-11790 VERSETZT KEIN DORF. Es setzt nur
     `state.eigene_dimension` und `eigene_dimensionen`; `siedlung.dimension`, `.x`, `.y` bleiben.
     `_render_portal` zeichnet eigene Doerfer aber nach `_ort.dimension` (Z. 12266-12273). Nach
     einem bezahlten Sprung (5000 Mana) stehen die Doerfer also weiter auf der alten Welt, die
     "eigene" Ansicht zeigt sie nicht mehr. Daher Daniels "ich kann nicht auswaehlen, welches Dorf
     wohin springt": das kann der Code gar nicht.
  2. Die "Auswahlliste" ist die Liste der sechs Welten mit Knopf "Weltensprung" (Z. 12182) plus die
     Zeile "Ansehen" (Z. 12189-12201) - zwei Zeilen fuer dieselbe Welt.
  3. Ein Feldklick existiert schon (`_portal_klick` Z. 12024 -> `_portal_feld_waehlen`), bucht aber
     nichts ("der Dorftransfer folgt mit S-6", Z. 12071 und Z. 12327 - Entwicklertext in der
     Spieleransicht).
  4. FALSCHE WELT: `_portal_feld_waehlen` prueft gegen `state.eigene_dimension`, und
     `_render_portal` Z. 12320 liest `portalraum.gelaende_von_feld(nummer, ...)` mit der EIGENEN
     Nummer - auch wenn der Spieler gerade eine FREMDE Welt ansieht. Gelaende und Weltnummer der
     Anzeige sind dann falsch.
  5. ZWEI UHREN: die 24-h-Sperre rechnet mit `time.time()` (Z. 11776/11784, Echtzeit), die
     Unterwegs-Sperre mit `state.spielsekunden`. Siehe FRAGE.
  6. Beleg der Regel: `data/welten.json` Z. 30-33 (5000 Mana, einmal binnen 24 Stunden, "Welt an
     ihren neuen Platz verschiebt").

VORSCHLAG: Der Kern bekommt EINE Pruef- und EINE Buchungsfunktion fuer "Dorf X nach Welt z, Feld x/y";
die Ansicht kennt nur Klicks: Klick auf eigenes Dorf = Dorf waehlen, Klick auf freies Feld = Ziel
waehlen, darunter ein Kasten mit jeder Bedingung (erfuellt/fehlt) und EINEM Knopf "Hierher versetzen".
Verworfen: die alte Welt-Liste behalten und nur ein Feld nachfragen - Daniel will ausdruecklich keine
Liste, und die Liste versetzt kein Dorf.

RISIKO: `test_portal_uebersicht.py` (Z. ~224 "die Anwahl uebertraegt kein Dorf (S-6 fehlt noch)",
Z. ~236 `_portal_wechsel(app, 5)`) und ggf. `test_portalraum`/`test_portal_fremdblick` haengen am alten
Weg; `eigene_dimension` wird an vielen Stellen gelesen (Angriffssperre ueber die Weltgrenze).

PATCH-PLAN:
  1. main.py :: GameState :: Anker `def freie_weltfelder(self, anzahl: int = 6) -> list:` (Z. 5336)
     neu: DAVOR drei Methoden (Skizze der ersten, 15 Zeilen):
       def weltfeld_belegt(self, welt: int, x: int, y: int) -> str:
           """Leer = frei. Sonst der Grund. EINE Stelle fuer 'Feld frei?' auf der Portalkarte."""
           for s in self.settlements:
               if (int(s.dimension), int(s.x), int(s.y)) == (int(welt), int(x), int(y)):
                   return "Dort steht schon dein Dorf %s." % s.name
           for bot in self.bots:
               for dorf in bot_doerfer_sicherstellen(bot):
                   if (int(dorf.dimension), int(dorf.x), int(dorf.y)) == (int(welt), int(x), int(y)):
                       return "Dort steht das Dorf %s von %s." % (dorf.name, bot.name)
           if self.drache_an(int(welt), int(x), int(y)) is not None:
               return "Dort lagert ein Drache."
           return ""
       `dorf_versetzen_pruefen(self, siedlung, welt, x, y, jetzt_echt=None) -> dict`
         Rueckgabe wie `dorfwall.reparatur_pruefen`: {"moeglich", "gruende": [..], "kosten"}.
         Sammelt ALLE Gruende (nicht beim ersten abbrechen):
           - `siedlung not in self.settlements` -> "Dieses Dorf gehoert nicht zu deinem Reich."
           - `portalraum.koordinate(x, y, portalraum.index_von(welt)) is None` -> "Feld liegt nicht auf der Karte."
           - gleiches Feld wie jetzt -> "Das Dorf steht bereits dort."
           - `self.weltfeld_belegt(...)` nicht leer -> dieser Text.
           - `auftraege.laufende(self.auftraege, self.spielsekunden)` nicht leer -> der Satz aus
             `_portal_wechsel` Z. 11759-11760 (woertlich, Regel Daniel 01.11.2026 bleibt GLOBAL).
           - `portalraum.wechsel_erlaubt(index_von(siedlung.dimension), index_von(welt),
              mana, self.letzter_wechsel, jetzt_echt or time.time())` -> deren Meldung, falls False.
           "kosten" = `portalraum.wechselkosten()` (keine Zahl im Code).
       `dorf_versetzen(self, siedlung, welt, x, y, jetzt_echt=None) -> (bool, str)`
         ruft `dorf_versetzen_pruefen`; bei Ablehnung `(False, "; ".join(gruende))`, NICHTS
         veraendert. Sonst: `gebucht = portalraum.nach_wechsel(mana, jetzt)`, Mana und
         `letzter_wechsel` setzen (wie Z. 11780-11782), dann `siedlung.dimension, .x, .y = welt, x, y`,
         `welt` in `eigene_dimensionen` aufnehmen, `self.eigene_dimension = int(welt)`,
         `self.aktive_siedlung_id = siedlung.id`; Meldung ins Postfach (`type: "portal"`).
         Gelaende des Ziels wird NICHT geprueft: Docstring Z. 12134-12136 legt fest, dass das
         Portal-Gelaende "keine Bauplatz-, Rohstoff- oder Ertragswirkung" hat.
  2. main.py :: _portal_klick :: Anker Z. 12043 `return self._portal_feld_waehlen(x, y)`
     neu: davor (nach dem Marsch-Zweig) einfuegen: eigenes Dorf auf (angezeigte Welt, x, y)?
          -> `self._portal_dorf = siedlung.id; self._render_view(); return True`.
  3. main.py :: _portal_feld_waehlen :: Anker Z. 12064 (erstes Vorkommen in `_portal_feld_waehlen`) `nummer = int(self.state.eigene_dimension)`
     alt: eigene Welt.
     neu: `nummer = int(getattr(self, "_portal_blick", 0) or self.state.eigene_dimension)` und
          `self.portal_auswahl = (nummer, int(x), int(y))` (DREI Werte: Welt, x, y). Log-Text ohne "S-6".
  4. main.py :: _render_portal :: Anker Z. 12181 `if eintrag["waehlbar"]:`
     alt: Knopf "Weltensprung" / Grund.
     neu: Knopf "Ansehen" (`self._portal_ansehen(n)`); die Extra-Zeile "1b. ANSEHEN" (Z. 12189-12201)
          loeschen. Die Spalte `status_text` (Bannerfarbe) bleibt.
  5. main.py :: _render_portal :: Anker Z. 12317 `if auswahl:` (zweites Vorkommen in `_render_portal`, Text "Angewähltes Feld")
     alt: Text mit "Der Dorftransfer folgt mit S-6".
     neu: `welt, ax, ay = auswahl`; Gelaende mit `welt` statt `nummer` lesen (behebt Befund 4).
          Ist `self._portal_dorf` gesetzt (sonst: bei genau einer Siedlung diese), Kasten zeichnen:
          Zeile "Dorf <name> von Welt <a>, Feld x/y nach Welt <b>, Feld x/y";
          `p = self.state.dorf_versetzen_pruefen(...)`; je `p["gruende"]` eine Zeile "- ...";
          bei `p["moeglich"]` Knopf "Hierher versetzen (<p['kosten']> Mana)" ->
          `self._portal_versetzen(dorf, welt, ax, ay)`. Ohne gewaehltes Dorf: "Erst dein Dorf auf
          der Karte anklicken."
          Das gewaehlte eigene Dorf bekommt denselben Goldrand wie das gewaehlte Feld (vorhandene
          zwei `create_rectangle`-Zeilen Z. 12310-12313 noch einmal mit dessen x/y).
  6. main.py :: NebelseetalApp :: neu `_portal_versetzen(self, dorf, welt, x, y)`: Rueckfrage
     `messagebox.askyesno` (wenn root), dann `ok, text = self.state.dorf_versetzen(...)`, `_log`,
     bei Fehlschlag `messagebox.showinfo`, `self.portal_auswahl = None`, `self._render_view()`.
  7. Die Sperre bleibt sichtbar: die vorhandene Zeile Z. 12344 "Mana ... · Sperre: ..." bleibt
     oberhalb; zusaetzlich steht der Sperrgrund im Kasten (aus `gruende`). Die 20 Pixelrechnungen
     bleiben in der begruendeten Ausnahme; der neue Code rechnet keine Pixel ausser dem Goldrand.
  8. `_portal_wechsel` und die Zeile Z. 12351 "(Unser Mana liegt in EINEM gemeinsamen Vorrat ...)":
     `_portal_wechsel` bekommt keinen Knopf mehr. Im selben Schritt im Fehlerregister eintragen:
     "nach gruener Wache test_portal_versetzen loeschen" - nicht still liegen lassen.

TEST:
  * NEU `tests/test_portal_versetzen.py` (ASCII, ohne Fenster, nur GameState):
    (a) Ziel = Feld eines Bot-Dorfs -> `moeglich False`, Grund nennt das Dorf, Spielstand unveraendert
        (`copy.deepcopy` vorher/nachher vergleichen: settlements, mana, letzter_wechsel);
    (b) freies Feld, Mana >= `portalraum.wechselkosten()`, keine Sperre -> True; danach
        `dimension/x/y` des Dorfes neu, Mana genau um `wechselkosten()` kleiner, `letzter_wechsel` gesetzt;
    (c) sofort ein zweites Mal -> False mit "Erst nach";
    (d) laufender Auftrag -> False, nichts veraendert;
    (e) mehrere Gruende gleichzeitig (belegt + zu wenig Mana) -> beide in `gruende`.
  * AST in derselben Datei: `_render_portal` enthaelt kein "OptionMenu" und keinen Aufruf
    `_portal_wechsel(`; neben `dorf_versetzen_pruefen` rufen `wechsel_erlaubt(` nur noch
    die Sperrzeile in `_render_portal` (Z. 12342) und `_portal_wechsel` (bis dieses geloescht ist).
  * `test_portal_uebersicht.py` Z. ~224: Pruefung umstellen auf "Anwahl allein bucht nichts".

FRAGE: Die 24-h-Sperre laeuft in Echtzeit (`time.time()`), alles andere in Spielzeit. Bei Faktor 180
sind 24 echte Stunden = 180 Spieltage. Deine Regel "ein Spieltag = 86.400 Sekunden" spricht fuer
Spielzeit; `_rename_settlement` Z. 10445 nimmt bewusst Echtzeit. Welche Uhr gilt fuers Portal?
(Ich habe NICHTS umgestellt; der Plan oben laesst `time.time()` stehen.)

NAECHSTER TEIL: 4/5 - Punkt D Bibliothek und die fuenf Entscheidungsfragen.

==================================================================================================
TEIL 4/5 - Punkt D Bibliothek versetzen + Entscheidungsfragen 15-18 und Design - Stand fa5834b
Bisher geliefert: Teil 1 (Wall), 2 (Marktplatz), 3 (Portal: Kern dorf_versetzen, Klick statt Liste).
==================================================================================================

BEFUND:
  1. `_karten_abreissen` Z. 11098-11104: letzte Bibliothek gesperrt (Daniel 30.10.2026); die
     Ablehnung geht nur in `_log` (Statuszeile), kein Fenster.
  2. `bauen_auf_karte` Z. 2696-2705: `max_je_siedlung: 1`; `_karten_bauen` Z. 10946-10951:
     `BIBLIOTHEK_OBERGRENZE = 2` (Z. 3527).
  3. Gemessen: `gebaeude_wirkung.max_stufe("bibliothek") == 5`. Jeder Weg ueber Abriss + Neubau
     kostet die Ausbaustufe (Neubau = Stufe 1, `bauen_auf_karte` Z. 2712; Abriss erstattet nichts).
  4. WIDERSPRUCH: `src/spielschicht.py` Z. 407 `abreissen` hat KEINE der Sperren (Dorfzentrum,
     letzte Bibliothek, Versorgungsschutz), obwohl der Modulkopf sagt, diese Schicht sei "die
     EINZIGE Stelle, an der die Oberflaeche den Spielstand anfasst". Das Spiel ruft sie nicht
     (gemessen: nur `tests/test_spielschicht.py` Z. 269/275). Der Test prueft also einen Weg, den
     der Spieler nie geht - und beweist dort den Abriss der letzten Bibliothek als "ok".

VORSCHLAG: Weg (b) - ein Knopf "Versetzen" an der Bibliothek: Zielfeld anklicken, dann Abriss alt +
Neubau neu in EINER Buchung ueber den bestehenden Bauweg (`_karten_bauen`), nur fuer die Bibliothek.

RISIKO: Der Spieler verliert die Ausbaustufe (bis zu 4 Stufen) - das muss VOR dem Klick dastehen,
sonst ist es eine Falle.

PATCH-PLAN:
  1. main.py :: _karten_bauen :: Anker Z. 10930 `def _karten_bauen(self, gebaeude_key: str):`
     neu: `def _karten_bauen(self, gebaeude_key: str, ersetzt_feld=None):` und direkt nach der
          `feld`-Pruefung:
            if ersetzt_feld is not None and (gelaende.finde_gebaeude(gebaeude_key) != "bibliothek"
                    or gelaende.finde_gebaeude(str(siedlung.bauten.get(str(ersetzt_feld)) or ""))
                    != "bibliothek"):
                self._log("Versetzen gibt es nur fuer die Bibliothek."); return
  2. main.py :: _karten_bauen :: Anker Z. 10946 `if str(gebaeude_key).lower().startswith("bibliothek"):`
     neu: `... .startswith("bibliothek") and ersetzt_feld is None:` (Anzahl bleibt beim Versetzen gleich).
  3. main.py :: _karten_bauen :: Anker Z. 10965 `baubar, grund = bauen_auf_karte(`
     alt: Vorpruefung gegen `siedlung`, `bau_probe = copy.deepcopy(siedlung)` erst Z. 10988.
     neu: `bau_probe = copy.deepcopy(siedlung)` VOR diese Zeile ziehen; wenn `ersetzt_feld` gesetzt:
          `bau_probe.bauten.pop(str(ersetzt_feld), None); bau_probe.stufen.pop(str(ersetzt_feld), None)`;
          die Vorpruefung UND der echte Bau (Z. 10989) laufen auf `bau_probe` (die zweite
          `deepcopy`-Zeile entfaellt). Die Uebernahme Z. 10998-10999 bleibt - sie traegt dann
          Abriss und Neubau zugleich. Danach `self._versetzen_von = None`.
          Damit gelten Nahrungssperre, Gelaende, Forschung, Ortsdeckung und Versorgungsschutz
          unveraendert - kein zweiter Bauweg.
  4. main.py :: _render_settlement_map :: Anker Z. 11593 `tk.Button(knopfreihe, text="Abreißen"`
     neu: davor, nur wenn `gelaende.finde_gebaeude(str(gebaut)) == "bibliothek"`:
          `tk.Button(knopfreihe, text="Versetzen", command=lambda f=feld: self._versetzen_merken(f), ...)`
  5. NEU `_versetzen_merken(self, feld)`: `self._versetzen_von = (siedlung.id, int(feld))`,
     `self.karten_feld = None`, Log "Bibliothek versetzen: jetzt das Zielfeld anklicken.", neu zeichnen.
  6. main.py :: _render_settlement_map :: Anker Z. 11618 `# FIX04: Der historische Screenshot`
     (nach Teil 1 steht dieser Block weiter oben - Anker dann der Kommentar `# S-2c-D (Daniel
     01.11.2026): Das Dorfzentrum ist mit der Gruendung`): davor Kasten, wenn `_versetzen_von` zu
     dieser Siedlung gehoert und `bau_moeglich("bibliothek", art)[0]`: Zeile "Bibliothek von <alt>
     hierher - Stufe <stufe_von_feld(alt)> wird zu Stufe 1, Preis <kosten_text(baukosten('bibliothek'))>,
     keine Erstattung"; Knopf "Hierher versetzen" -> Rueckfrage (askyesno, wenn root) ->
     `self._karten_bauen("bibliothek", ersetzt_feld=alt)`; Knopf "Abbrechen" -> `_versetzen_von = None`.
     Ist das Gelaende verboten: nur die Zeile mit `bau_moeglich(...)[1]`.
  7. main.py :: _karten_abreissen :: Anker Z. 11101 `self._log("Die letzte Bibliothek kann nicht`
     neu: Satz ergaenzen um "Oder 'Versetzen' waehlen." und zusaetzlich `messagebox.showinfo` (wenn root).
  8. src/spielschicht.py :: abreissen :: NICHT in diesem Schritt angleichen; als eigener
     Registereintrag "spielschicht.abreissen ohne Sperren" anlegen (keine Massenaenderung).

TEST: NEU `tests/test_bibliothek_versetzen.py` (ASCII, Aufbau wie `test_gpt_wall_gui` setUp):
  (a) nach dem Versetzen genau EINE Bibliothek in der Siedlung, auf dem neuen Feld, Stufe 1;
  (b) Ortslager genau um `baukosten("bibliothek")` kleiner (Werte aus der Funktion, keine Literale);
  (c) Ziel auf verbotenem Gelaende -> nichts veraendert (deepcopy-Vergleich bauten/stufen/vorraete);
  (d) in Nahrungsnot -> abgelehnt, nichts veraendert; (e) `ersetzt_feld` an einem Holzfaeller -> abgelehnt;
  (f) `BIBLIOTHEK_OBERGRENZE` erreicht (2 Siedlungen, 2 Bibliotheken) -> Versetzen trotzdem moeglich.

ENTSCHEIDUNGEN (je: Empfehlung - Grund - Preis des anderen Weges)

Frage 17 Bibliothek:
  Empfehlung: (b) "Versetzen" als eine Buchung, Neubau auf Stufe 1, normaler Baupreis.
  Grund: Deine Regel bleibt woertlich wahr - es gibt keinen Moment ohne Bibliothek; alle Zahlen
  kommen aus bestehenden Regeln (keine Erstattung, Neubau Stufe 1).
  Preis: (a) laesst die Forschung still stehen und macht den Abriss zur Falle; (c) laesst einen
  Anfaengerfehler vom ersten Tag fuer immer stehen (genau das ist dir in Test 3 passiert). Die
  Stufe MITZUNEHMEN waere eine neue Regel ohne Beleg - nur auf dein Wort.

Frage 18 Pakt:
  Empfehlung: Keine Wahrscheinlichkeit. Die Regel "nach Einstellung" GIBT es schon: `min_gunst 40`
  (`data/diplomatie.json`, vertraege.nichtangriff). Der Fehler ist die Ansicht: `_render_diplomacy`
  Z. 14080 `if _pakt_ok:` VERSTECKT den Knopf bei zu wenig Gunst - der Spieler sieht nie eine
  Ablehnung, deshalb wirkt es, als buche der Knopf immer. Knopf immer zeigen (ausser Grund
  `vertraege_aus`; bei `laeuft_bereits` Text statt Knopf); die Ablehnung kommt als Antwort des Bots
  ins Postfach, mit Gunststatus (`diplomatie.status`) und noetiger Gunst.
  Grund: reproduzierbar, testbar, jede Zahl schon belegt/als VORSCHLAG markiert; der Spieler
  versteht WARUM und weiss, was er tun muss (Gunst heben).
  Preis Zufall: eine neue unbelegte Zahl, Tests werden zufallsabhaengig, gleiche Lage ergibt
  verschiedene Antworten - wirkt wie ein Fehler. Taktik/Volk einzurechnen: ohne Quelle -> nein.
  Patch-Kern: neue `diplomatie.ablehnung_text(bot_daten, grund, name)` liest eine Vorlage mit
  Platzhaltern {name} {status} {gunst} {noetig} aus `data/diplomatie.json` `_gruende`
  (neuer Schluessel `gunst_zu_niedrig_bot`, Text als VORSCHLAG markiert). `tests/test_pakt_knopf.py`
  Abschnitt B ("ohne genug Gunst erscheint KEIN Knopf") wird umgedreht: Knopf da, Klick bucht
  nichts, Gunst unveraendert, Postfach nennt Status und Grenze.

Frage 15 (neun Werte):
  Empfehlung: im Code lassen, je Zeile das WAHRE Quellenwort - nicht nach `data/` verschieben.
  Grund: drei haben schon eine Herkunft, die die Wache nur nicht erkennt:
  FORSCHUNG_GRUNDKOSTEN_HOLZ 50 = Handbuch S. 13 (steht so in `data/research.json` Z. 10) ->
  "Handbuch S. 13"; BESCHAFFUNGSKOSTEN 250 -> "gerechnet" (Kaempferpreis x 1,2; der Faktor 1,2 selbst
  ist VORSCHLAG); STANDARD_FAKTOR 180 ist ein DOPPEL zu `data/spielzeit.json` "faktor" (dort
  aenderbar, "Von Daniel aenderbar") - Zeile als "Rueckfall, wenn data/spielzeit.json fehlt;
  Entscheidung Daniel" markieren. Die uebrigen sechs bekommen "VORSCHLAG".
  Preis `data/`: sechs Module brauchen Ladecode, Fehlerpfad und Wache - viel Umbau, null Gewinn an
  Wahrheit. Ausnahme spaeter: wenn du einen Wert wirklich drehen willst, DANN in die Datei.

Frage 16 (sechs Dateien):
  Empfehlung: jede bekommt `"_quelle"` mit einem ehrlichen Satz: fuenf "VORSCHLAG Remake, kein
  Originalbeleg; angelegt <Datum aus `git log --diff-filter=A --format=%cs -- data/<datei>`>",
  `marsch_optik.json` "Anzeige, kein Spielwert (keine Regelwirkung)". Vorher je Datei
  `grep -rl <dateiname> docs/` - nennt ein Auftrags-/LLM-Dokument die Werte, diesen Pfad mit
  nennen (Muster `diplomatie.json`). Danach die sechs aus `daten_quellen_bestand.json` streichen.
  Grund: ehrlich, in 15 Minuten fertig, die Wache wird schaerfer statt nachsichtiger.
  Preis "Herkunft recherchieren": Stunden ohne Ergebnis - das Handbuch nennt Bot-Verhalten nicht.

Design (drei Eingriffe ohne neue Palette):
  1. Farben an EINE Stelle: gemessen 94 verschiedene Hex-Farben fest in `main.py`. Sechs davon
     SIND schon Skin-Werte und stehen trotzdem als Literal: #3e2723 (37x = skin "button"),
     #2a0605 (31x = "bg"), #5D4037 (17x = "button_active"), #FFCC33 (16x = "gold"), #e53935 (12x =
     "red"), #FFFF99 (7x = "text"). Ersetzen durch `self.skin[...]` aendert im Standard-Skin
     NICHTS, repariert aber die beiden anderen Skins (dort sind diese Stellen heute falsch gefaerbt).
     Danach die drei haeufigsten Nicht-Skin-Farben als neue Schluessel MIT IHREM HEUTIGEN WERT in
     alle drei Skins: "hinweis" #C0C0C0 (58x), "warnung" #FDBA74 (32x), "info" #7FD1FF (15x).
     Herr Duebner aendert spaeter EINE Stelle. Wache: Anzahl Hex-Literale in main.py darf nicht steigen.
  2. Ein Seitenkopf: Dorfzentrum nutzt `_kasten_label`, Marktplatz/Portal/Gilde rohe Labels; Schrift
     gemischt (gemessen 70x "Arial", 50x "TkDefaultFont"). Eine Methode `_seitenkopf(titel, unterzeile)`
     fuer alle `_render_*`; Text einheitlich "TkDefaultFont". Daniel mag den Satzbau - den nicht anfassen.
  3. Entwicklertexte und Attrappen aus den Spieleransichten: "folgt mit S-6" (Z. 12071, 12327);
     "Gelaendefarben je Feld kommen mit dem Weltbild (S-5)" (Z. 12335 - S-5 ist laut Docstring
     Z. 12133 laengst gebaut, also falsch); "Gildenprofil folgt" und die Gildentabelle Z. 14473-14477
     mit ERFUNDENEN Gilden und Zahlen ("Nebelwoelfe", 12, 4520 ...) - verstoesst gegen eure eigene
     Regel. Ersatz: "Gilden gibt es im Einzelspieler nicht." Wache: `test_spielertexte` um die
     Muster `S-\d`, `folgt mit`, `folgt in einer` in `text=`-Argumenten erweitern.

NAECHSTER TEIL: 5/5 - weitere Fehlerfunde und Tipps.

==================================================================================================
TEIL 5/5 - Weitere Fehlerfunde (nicht beauftragt) und Tipps - Stand fa5834b
Bisher geliefert: Teil 1-4 (Punkte A-D, Fragen 15-18, Design).
==================================================================================================

FEHLERFUNDE (je mit Ort; nichts davon ist im Plan oben schon behoben, ausser wo vermerkt):
  F1. Wachenluecke `tests/test_quelle_ast.py` Z. 41: `PRAEFIXE = ("_zeige", "_zeichne", "_render")`.
      Methoden, die mit `_zeichnen` ENDEN oder `_block` heissen, rutschen durch:
      `_ruhm_balken_zeichnen` Z. 14513 rechnet `breite * fortschritt`, `_mauer_reparatur_block`
      rechnet `ende - spielsekunden`. Ausserdem fehlen Vergleiche gegen Kommazahlen (0.3, Teil 2).
      Vorschlag: Endungen `_zeichnen`, `_block` aufnehmen; jedes Zahlliteral ausser 0 und 1 zaehlt.
      Erst MESSEN, wie viele neue Treffer kommen, dann begruenden oder beheben.
  F2. Toter Code nach `return` (Teil 1, Z. 11644-11646) - diese Fehlerklasse hat keine Wache.
      Vorschlag: AST-Wache ueber `src/*.py`: in keinem Block folgt ein Statement auf
      `return`/`raise`/`continue`/`break`. Laeuft ohne Fenster in unter 1 s.
  F3. Zwei Weltmodelle (VERMUTUNG, bitte messen): `freie_weltfelder` Z. 5336 (Gruendung) sperrt
      Wasser nach `MAPS`/`get_tile`-Gelaende (Z. 3427: Karten 20/8/8/7/10 mit Quests/NPCs ohne
      Quelle), das Portal zeigt Gelaende aus `portalraum.weltbild` und erklaert es zur reinen
      Anzeige. Messung: fuer alle 400 Felder `get_tile(x,y,20).terrain` gegen
      `portalraum.gelaende_von_feld(eigene_dimension,x,y)` vergleichen und zaehlen. Weichen sie ab,
      sieht der Spieler "Ebene" und bekommt bei der Gruendung trotzdem "Wasser".
  F4. `_portal_wechsel` versetzt kein Dorf (Teil 3, Befund 1) - der schwerste Fund dieser Runde.
  F5. 0.3 viermal ohne Quelle (Teil 2). F6. `spielschicht.abreissen` ohne Sperren (Teil 4).
  F7. Stille Ausfaelle in Statuszeile statt Fenster: `_karten_wall_errichten` (Teil 1),
      Bibliothek-Abrisssperre (Teil 4), `_trade` bei Neigung <= Grenze (Z. 14278). Muster fuer
      alle: Klick, der nichts bucht, zeigt den Grund dort, wo der Spieler hinschaut.
  F8. Falsche Ortsangaben in Spielertexten: Z. 10953 ("im Dorfzentrum"), Z. 11640 ("oberhalb
      der Karte"), Z. 12335 ("kommen mit S-5"). Eine Wache "Texte nennen keine Ansicht, die es
      nicht gibt" ist schwer; billiger: bei jedem Umzug einer Anzeige `grep` nach dem alten Ortsnamen.

TIPPS (getrennt von der Aufgabe):
  T1. Sammellauf 11 min auf 2 Kernen: ein `tools/nachbartests.py`, das die in `git diff` beruehrten
      Funktionsnamen nimmt und nur die `tests/*.py` startet, die diese Namen enthalten. Der volle
      Lauf bleibt Pflicht vor jeder EXE, aber zwischen zwei Patches reichen 1-2 Minuten.
  T2. Wenn Hermes Opus per `claude -p` fragt: fuer Auftraege wie diesen `--allowedTools
      "Read,Grep,Glob"` (nur lesen) - dann kann ein Entwurf nie still Dateien aendern; schreiben
      tut nur der Koordinator. Das passt zu eurer Arbeitsteilung und zu Daniels "nur lesen".
  T3. Reihenfolge der Umsetzung (meine Empfehlung): A (klein, Daniels klarste Anweisung) -> D
      (klein, eine Methode) -> B (mittel) -> Frage 18 (klein) -> C (gross, braucht Daniels Antwort
      zur Uhr nicht, aber Zeit) -> Design 3 -> Design 1. Je Punkt EINE EXE, nicht alle auf einmal:
      sonst weiss der naechste Spieltest nicht, welcher Umbau welche Note bekommt.
  T4. Spieltest-Anleitung: zu jedem Punkt einen Satz "wo wuerdest du es zuerst suchen?" BEVOR der
      Weg verraten wird - Daniels Antwort bei Handel (Diplomatie, Kampfsimulator) war der wertvollste
      Befund des ganzen Tests.

ENDE. Alle Anker gegen `src/main.py` 16.457 Zeilen (Stand fa5834b = f4eaf7c fuer `src/`).
