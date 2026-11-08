# PRUEFUNG der Opus-Lieferung vom 08.11.2026 (Koordinator-Pflicht)

> **Wer:** Hermes "Weltenfresser" (`deepseek-flash`), Koordinator nach Daniels Ansage 17:35
> ("solange Weltenfresser der Top Koordinator bleibt").
> **Wann:** 08.11.2026, 18:20-18:35, Sitzung `08.11.26_V_0.0.3_Session_20`.
> **Was geprueft wurde:** die zwei Opus-Dokumente, die Daniel am 08.11.2026 auf dem Desktop
> abgelegt hatte. Gepruefter Code-Stand: `a76010e` (Code = `fa5834b`, danach nur `docs/`).
> **Regel:** Jede Zahl und jeder Anker wird gegen den Code gemessen, nicht uebernommen
> (Auftrag `docs/extern/AUFTRAG_CLAUDE_OPUS_20261108.md`, Arbeitsteilung Register 313).

## 1. Ablage und Belege

| Dokument | Ablage im Repo | SHA256 | Zeilen |
|---|---|---|---|
| `ANTWORT_OPUS_20261108.md` (5 Teile) | `docs/extern/ANTWORT_OPUS_20261108.md` | `09fd7992f3c3c6d1...` | 521 |
| `Weiterer_Spieltest_08.11.26.md` (Nachtrag 1, 8 Teile) | `docs/extern/SPIELTEST_OPUS_WEITERER_20261108.md` | `7290c7f3238feff4...` | 628 |

Beide Dateien liegen **zeichengleich** (byte-gleich) im Repo; die Desktop-Fassungen hatten bereits
LF-Zeilenenden, die Repo-Regel fuer `docs/*.md` ist damit ohne Umwandlung erfuellt. Die Herkunft
steht im Eingangsordner `D:\Arbeiten\Hermes\Eingaenge\20261108_Opus_Spieltest\` mit `MANIFEST.md`.

## 2. Gemessene Gegenprobe (Projekt-venv, `src/main.py` `a76010e`)

| # | Opus-Behauptung | Messung 18:25 | Urteil |
|---|---|---|---|
| 1 | `main.py` hat 16.457 Zeilen | **16.458** | Abweichung 1 Zeile (kein Befund) |
| 2 | `_portal_wechsel` versetzt kein Dorf (S1) | Z. 11747-11791 setzt nur `eigene_dimension`, `eigene_dimensionen`, Mana und `letzter_wechsel`; **keine** Zuweisung an `siedlung.dimension/.x/.y` | **bestaetigt** |
| 3 | Portal-Sperre rechnet in Echtzeit | `time.time()` in Z. 11774 (pruefen) und Z. 11779 (buchen), dazu `_sperre_text` Z. 11742 und `_render_portal` Z. 12343 | **bestaetigt** |
| 4 | Spielerhandel nimmt pauschal 250 x 1,2 = 300 Gold | Z. 5190 und Z. 10583: `referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)` + `botkern.handelspreis(referenz, temperament)` | **bestaetigt** |
| 5 | `botkern.oekonomie_angebot` wird nirgends aufgerufen | `grep -rn "oekonomie_angebot" src/`: nur Definition `src/botkern.py:650`, sonst ein Kommentar `main.py:683` | **bestaetigt** (eine fertige, ungenutzte Preisfunktion) |
| 6 | Erster Kriegspunkt beendet den Goetterschutz | Z. 7786: `if self.day > punkte.goetterschutz_tage() or krieg > 0:` -> `noob_protection = False`, Grund "erster Kriegspunkt" | **bestaetigt** |
| 7 | Ungelesene Diebstahlberichte werden geloescht | `data/nachrichten.json`: `frist_spielsekunden 86400`, `verschieben_wenn_ungelesen: ["verlust"]`; Rueckfall in `src/postfach.py` Z. 31 identisch | **bestaetigt** (zwei Stellen, beide gleich falsch) |
| 8 | Ausbildungs-Vorschau zeigt den Preis nur bei bezahlbarer Menge | `main.py` Z. 15632: `var.set("1" if moeglich >= 1 else "0")` | **bestaetigt** (Opus nannte 15633) |
| 9 | Forschungs-Sperrtext mischt Soll/Ist | `src/forschungspfad.py` Z. 195 `f"Bibliothek {soll}/{ist}"` gegen Z. 199 `f"{p['was']} {ist}/{soll}"` - im selben Satz | **bestaetigt** |
| 10 | Handelsgrenze 0,3 steht viermal ohne Namen | Z. 4957, 5084, 14277, 14457 (`bot.trading`); weitere 0,3 an Z. 3454/13961/14017 meinen anderes (Temperament, Schriftgroesse, Zufall) | **bestaetigt** (genau vier) |
| 11 | Toter Code: `return` vor der Reparaturzeile | Z. 11644 `return`, Z. 11645 `self._mauer_reparatur_block(info, siedlung)`, Z. 11646 `return` - unerreichbar | **bestaetigt** |
| 12 | `BIBLIOTHEK_OBERGRENZE = 2` | Z. 3527 | **bestaetigt** |
| 13 | Bibliothek: `max_je_siedlung` 1 | `data/buildings.json`, Eintrag `bibliothek`: `"max_je_siedlung": 1` | **bestaetigt** |
| 14 | Ausbaustufe der Bibliothek bis 5 | `gebaeude_wirkung.max_stufe("bibliothek") == 5` (im Projekt-venv gerechnet) | **bestaetigt** |
| 15 | `spielschicht.abreissen` hat keine Sperren | `src/spielschicht.py` Z. 407-...: Docstring nennt nur "keine Erstattung"; keine Dorfzentrum-, Bibliotheks- oder Versorgungssperre | **bestaetigt** |
| 16 | `bots_tick` zieht `random.Random()` ohne Saat | Z. 7345; ebenso Z. 6025, 6650, 14372, 14416. Mit Saat arbeiten nur Z. 1335, 4239, 6887, 6894, 13325 | **bestaetigt** |
| 17 | Entwicklertexte in Spieleransichten (S12) | Z. 10101 "so hat Daniel es am 05.11.2026 entschieden", Z. 12071 "der Dorftransfer folgt mit S-6.", Z. 14485 "Gildenprofil folgt in einer spaeteren Version.", Z. 15369 "Bauten binden keine Siedler (Entscheidung 31.10.2026)", Z. 12335 "kommen mit dem Weltbild (S-5)", Z. 4798 "(fuehrend seit Teil 3a)" | **bestaetigt** |
| 18 | Pakt-Knopf wird bei zu wenig Gunst versteckt | Z. 14078 `_pakt_ok, _pakt_grund = diplomatie.pakt_anbietbar(...)`, Z. 14080 `if _pakt_ok:` - kein `else` | **bestaetigt** |
| 19 | 94 verschiedene Hex-Farben in `main.py` | **96** verschiedene `#rrggbb`-Literale | Abweichung 2 (Zaehlweise; vor dem Umbau neu messen) |

**Ergebnis: 17 von 19 Angaben stimmen zeichengenau, zwei sind Zaehlabweichungen ohne Folge.**
Keine erfundene Zahl gefunden - der Auftrag "keine Zahl ohne Quelle" hat gegriffen.

## 3. Zusatzbefund des Koordinators (nicht von Opus)

**Die Bibliothek ist nicht nur Daniels Regel, sondern Originalregel.** `data/buildings.json` fuehrt
beim Eintrag `bibliothek` den Beleg `_belegt_nur_auf`: *"Bibliothek nur auf Grasland, Steppe oder
Nebelsee, **eine je Siedlung**"* (`ORIGINAL_Einheiten_Waren_Rohstoffe.md`, Abschnitt 4).
Damit ist Frage 17 schaerfer als in der Uebergabe beschrieben: **"eine je Siedlung" ist belegt**, ein
Versetzen, das genau EINE Bibliothek je Siedlung erhaelt, verletzt die Originalregel NICHT. Ein
"Abriss erlauben" (Variante a) wuerde sie dagegen fuer einen Moment verletzen - das ist ein Grund
mehr fuer Opus' Empfehlung (b) "Versetzen als eine Buchung".

## 4. Was NICHT geprueft ist (offen vor dem Bauen)

1. **Zeilennummern der Ansichten** (`_render_market`, `_render_diplomacy`, `_render_portal`) wurden
   stichprobenartig, nicht vollstaendig nachgezaehlt. Vor jedem Patch gilt: Ankertext suchen, nicht
   Zeilennummer vertrauen.
2. **Opus' Messwerte aus seiner Linux-Umgebung** (z. B. "10 Holz kosten 3.100 Gold", "33 Nachrichten
   in 10 Spieltagen", Schwellenpreise 0,45/0,60 Gold) sind **nicht** Windows-verifiziert. Sie duerfen
   als Beobachtung zitiert, aber nicht als Spielbefund gemeldet werden.
3. **`_render_market` und die Handelskarawanen-Bedingungen**: die von Opus genannten Kernfunktionen
   (`handelskarawanen_bestand`, `einheit_bedingungen`) existieren; ihr Zusammenspiel mit der Ansicht
   ist noch nicht gelesen.
4. **Design-Zahlen** (94/96 Farben, 70x "Arial", 50x "TkDefaultFont") sind erst beim Anfassen der
   Design-Aufgabe neu zu messen.

## 5. Folge fuer den Auftrag an Opus

Kein neuer Auftrag noetig: die Lieferung deckt die vier Test-3-Punkte (A-D), die fuenf Fragen
(15-18, Design) und 18 Zusatzbefunde ab. Offen ist nur, was Daniel selbst entscheiden muss
(Fragen 15-18 sind durch seine Entscheidungen 17:52 teilweise beantwortet, siehe
`docs/ENTSCHEIDUNGSVERZEICHNIS.md`). Eine Nachforderung wird erst gestellt, wenn beim Bauen eine
Stelle auftaucht, die der Entwurf nicht abdeckt.
