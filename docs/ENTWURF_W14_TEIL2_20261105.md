# W-14 Teil 2 - Einbauplan (Stand 05.11.2026, 00:05)

Quelle: Messung am Code vom 04.11.2026 nach dem Bau von Teil 1 (Register 201).
Dieser Plan ist ein ENTWURF - gebaut wird erst nach Daniels zwei Entscheidungen und mit vollem Sammellauf.

Entwurf W-14 Teil 2 (Verdrahtung) — Messlage aus dem Code, Stand 04.11.2026

Ziel: die Drachen aus `src/drachen.py` ins Spiel bringen. Fuenf Andockstellen, jede einzeln pruefbar.

1) ZUSTAND im Spielstand
   - `GameState` bekommt ein Feld `drachen_besiegt: List[str]` (Vorgabe leer; alte Staende laden leer).
   - `GameState.save` (Zeile ~6390, Block um "bots") ergaenzt `"drachen_besiegt": list(...)`.
   - `GameState.load` (Zeile ~6573, neben `spielende`) liest es mit `or []`.
   - Pruefung: alter Spielstand ohne Feld laedt, `drachen.Zustand().aus_daten({})` ist leer.

2) ZIELWAHL im Angriffsweg
   - `_angriff_auftrag_starten(...)` erzeugt `ziel`; fuer einen Drachen fehlt ein Bot.
     Vorschlag: neues optionales Argument `drache_id: str = ""`, das `ziel["drache_id"]` setzt.
   - `kampf_am_ziel` prueft VOR der Bot-Aufloesung: `drachen.finde(welt, x, y, besiegt)` - ist ein
     Drache da, wird gegen ihn gekaempft (kein BotDorf, keine Garnison).
   - Welt und Koordinaten stehen im `ziel`; die Weltkarte kennt sie (Kartenaufbau).

3) KAMPF (geaendert 05.11.2026 nach Daniels Ansage: kein Wall, Drachenwerte)
   - Der Drache hat KEINEN Wall. Statt `wall_stufe`/`wall_zustand` gilt sein eigener Block
     `verteidigung.schuppen` (Datendatei): `schwelle_fussttruppen` 700, `schwelle_belagerungswaffen`
     950, `unbrechbar` true.
   - VORRUnde woertlich wie beim Wall, nur mit den Drachenwerten: Schlagkraft der NAHKAMPF-Einheiten
     gegen 700, Schlagkraft der Belagerungswaffen gegen 950. Reicht beides nicht, zieht der Angreifer
     ab ("unentschieden", kein Kampf) - genau die Aufgabe, die sonst der Wall hatte.
   - `unbrechbar` heisst: Belagerungswaffen richten KEINEN Mauerschaden an; `mauer_schaden` entfaellt im
     Drachenpfad, die Schwellen bleiben konstant. Ein Wall kann man klein schiessen, einen Drachen nicht.
   - FEUERATEM vor dem Nahkampf: `drachen.feueratem_verluste(eintrag, anzahl_fusstruppen)` (8 % der
     antretenden Fusstruppen, mindestens 1, hoechstens die Haelfte). Diese Verluste gehen von den
     Angreifern ab, BEVOR `kampf.fuehre_schlacht` laeuft, und stehen als eigene Zeile im Bericht.
   - Danach `kampf.fuehre_schlacht(kaempfer, drachen.verteidiger(eintrag), 0, 100.0, ...)` - Wallstufe 0,
     weil der Drache keinen Wall hat; die Verteidiger sind 120 Krieger + 60 Bogenschuetzen + 24 Paladine.

4) ANZEIGE
   - Die Kartenansicht zeichnet Bot-Doerfer als Burg (`_zeichne_siedlungskarte` / Weltkarte).
     Drachen kommen aus `drachen.anzeige_liste(welt, besiegt)` und werden als Bild gezeichnet
     (256-px-PNG, auf Feldgroesse skaliert), NIE als Burg.
   - Besiegt = `art == "ruine"`: dann das Ruinenbild; fehlt es, ein Platzhalter (grauer Steinhaufen,
     drei Ellipsen - kein erfundenes Bild).
   - Pruefung: ein besiegter Drache erzeugt `art == "ruine"` und wird nicht als Ziel angeboten.

5) PRUEFDATEIEN
   - Neu: `tests/test_drachen_einhaengung.py` (Kette: Zielwahl -> Kampf -> Beute -> Zustand -> Anzeige).
   - Mitwandern: `test_zieluebergabe` (naechster Schritt), `test_projektpfade` (MODULKARTE neu bauen),
     `test_textqualitaet` (neue Texte), `test_gpt_projektordnung` (keine neuen Hefte in docs/).

Offene Entscheidungen fuer Daniel (EINE Runde):
   A) Welche DREI Welten? Vorschlag d02, d03, d05.
   B) ENTSCHIEDEN 05.11.2026: 120 Krieger + 60 Bogenschuetzen + 24 Paladine (204), Drachenwerte statt Wall.
   C) Feste Drachenbeute oder Staffel-Beute? Vorschlag: fest (Daniels Zahlen) - der Drache hat keinen Wall, es gibt keinen Wallzustand fuer eine Staffel
   D) Duerfen Bots den Drachen angreifen? Vorschlag: nein (er ist kein Bot-Dorf).

6) BEUTE NACH LEISTUNG (Daniel 05.11.2026, Variante A)
   - Jeder Angriff bucht den Anteil, den er an den Verteidigern zerstoert hat: `drachen.beute_anteil(...)`;
     der letzte Schlag bekommt +10 %. KEIN "letzter Schlag nimmt alles" - sonst wartet ein schneller
     Gegner auf zwei Resteinheiten (Daniels eigene Sorge).
   - Der Anteil wird ueber `kampfbericht.beute_am_ziel` gebucht (EINE Buchstelle, `beute_override`).
7) TRANSPORT VORRECHNEN
   - `drachen.transport_bedarf(anteil, forschung)` sagt, welche Ladung noetig ist und welcher Wagenpark
     sie traegt; `transport_text` liefert den Satz fuer den Spieler ("Fuer deinen Anteil von 5.500 Ladung
     brauchst du 2 Grosse Handelskarawanen, 2 Zweispaenner").
   - Was nicht getragen wird, bleibt beim Drachen liegen - der naechste Angreifer findet es vor. Die
     Anzeige muss das VOR dem Angriff sagen, nicht danach.
8) BERICHT UND AUSSPAEHEN
   - `drachen.bericht(ergebnis, ueberlebende, verteidiger)`: mit Ueberlebenden ein genauer Bericht mit
     Einheiten, ohne Ueberlebende nur eigene Verluste und die ZAHL der Verteidiger.
   - `drachen.spionage_erlaubt()` -> (False, Grund): der Spionagepfad muss den Drachen ablehnen.
   - `drachen.angriffs_hinweis()` zeigt der Spieler im Angriffsfenster; die Spielerhilfe erklaert den
     Umstand (kein Ausspaehen, Bericht nur mit Ueberlebenden).
