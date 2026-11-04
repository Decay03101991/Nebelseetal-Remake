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

3) KAMPF
   - `kampf.fuehre_schlacht(kaempfer, drachen.verteidiger(eintrag), *drachen.wall(eintrag), ...)`
     - der Verteidiger ist ein einfaches dict, es braucht KEIN Dorf-Objekt.
   - Beute ueber die EINE Buchstelle: `kampfbericht.beute_am_ziel(...)` liefert die Staffel-Beute; die
     Drachenbeute (5.000 Gold usw.) ist eine FESTE Beute und kommt aus `drachen.beute(eintrag)`.
     Zwei Moeglichkeiten: (a) `beute_am_ziel` um `beute_override` erweitern (eine Buchstelle, aber
     Signatur der meistgenutzten Funktion aendert sich), (b) im Drachenpfad die feste Beute direkt
     buchen und `beute_am_ziel` NICHT aufrufen (zwei Buchstellen). Empfehlung: (a) mit Vorgabe None -
     bestehende Aufrufer bleiben unveraendert.

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
   B) Welche Einheiten verteidigen? Vorschlag 20 Krieger + 20 Bogenschuetze (= 40).
   C) Feste Drachenbeute oder Staffel-Beute nach Wallzustand? Vorschlag: fest (Daniels Zahlen).
   D) Duerfen Bots den Drachen angreifen? Vorschlag: nein (er ist kein Bot-Dorf).
