# S4-4 Rachetopf - Entwurf fuer die Umsetzung nach dem Sammellauf (06.11.2026)

**Stand 06.11.2026, 15:20: NICHTS davon ist gebaut.** Das ist der Entwurf fuer die naechste
Sitzung - alle Zahlen sind VORSCHLAG oder tragen die Entscheidung, auf der sie stehen; keine
Zeile davon steht in `src/diplomatie.py` oder `data/diplomatie.json`.

Grundlage: `docs/ABLAUF_LLM_20261106.md` Schritt 4, Daniels Entscheidungen 13:50 (Register 284):
Kontakt = JEDE Interaktion; der Topf steigt AUCH unter einem Pakt; Angriff fruehestens 28.800 s nach
Paktende; nach Bot-Sieg Topf 0 (F-3, 11:25).

## Datendatei `data/diplomatie.json`, Block `rache`

- `aktiv`: Schalter (A-7)
- `je_niederlage`: 1   (VORSCHLAG, Auftragsdokument 7.2)
- `je_spieltag_ohne_kontakt`: 1   (VORSCHLAG)
- `schwelle`: 3   (VORSCHLAG)
- `armee_sk`: 99  (V-5, G-2: 90 SK ist die WALL-Schwelle, nicht die Rache-Schwelle)
- `hoechstwert`: 5 (Deckel, damit der Topf nicht unbegrenzt waechst)
- `vorlauf_sekunden`: 28800  (1 Spieltag, VORSCHLAG)
- `nach_paktende_sekunden`: 28800  (ENTSCHEIDUNG Daniel 13:50)
- `nach_bot_sieg`: 0  (ENTSCHEIDUNG Daniel 11:25, F-3)
- `ruht_unter_goetterschutz`: true  (VORSCHLAG; G-1: `noob_protection` sperrt heute schon jeden Angriff)
- `ruht_unter_vertrag`: false  (ENTSCHEIDUNG Daniel 13:50: der Topf steigt AUCH unter dem Pakt)

## Felder am Bot (additiv)

- `rache: int = 0`  (Topf)
- `letzter_kontakt: float = 0.0`  (Spielzeit der letzten Interaktion; 0 = noch keine)

Beide ueber `bot_als_dict`/`bot_aus_dict` und `bot_aus_stand` fuehren - Muster wie `gunst`/`vertraege`.

## Funktionen in `src/diplomatie.py`

- `rache_block(einst)` / `rache_aktiv(einst)`
- `rache_buchen(bot_daten, grund, einst=None) -> int`  (klemmt auf 0..hoechstwert; `grund` nur fuer
  den Aufrufer, NICHT gespeichert - wie bei `gunst_aendern`)
- `kontakt_buchen(bot_daten, jetzt, einst=None)`  setzt `letzter_kontakt = jetzt`
- `rache_tag(bot_daten, jetzt, einst=None) -> int`  genau +1 je Spieltag ohne Kontakt; ruht unter
  Goetterschutz (Aufrufer uebergibt `goetterschutz=True`) - der Topf steigt unter Pakt WEITER
- `rache_bereit(bot_daten, armee_sk, jetzt, einst=None) -> bool`  Topf >= schwelle UND SK >= armee_sk
  UND `jetzt >= pakt_ende + nach_paktende_sekunden`
- `rache_nach_sieg(bot_daten, einst=None)`  Topf auf `nach_bot_sieg` (0)

## Paktende merken (EIN Speicher)

Ein gebrochener/abgelaufener Pakt wird NICHT geloescht, sondern mit `bis = jetzt` beendet und als
`beendet: True` markiert. Dann fragt `rache_bereit` das Ende aus DERSELBEN Tabelle
(`vertrag_ende(bot_daten, "nichtangriff")`) - keine zweite Buchfuehrung.
Folge: `vertrag_aktiv` liefert weiterhin False (weil `jetzt >= bis`), aber die Tests "der Pakt ist
weg" werden auf "der Pakt ist beendet" umbenannt (Entscheidung im Docstring nennen).

## Verdrahtung in `src/main.py`

- Niederlage im Bot-Angriff (dort, wo `kampf_result["ausgang"]` geprueft wird): `rache_buchen`.
- Kontakt: `_handel_ausfuehren` (Abschluss), `_bots_raubzug`-Gegenrichtung (Bot wird angegriffen),
  Geschenk (falls vorhanden), Ereignis (Schritt 5).
- Tageswechsel: `rache_tag` je Bot im Bot-Takt (`bots_fortschreiben`, fester Spielzeit-Punkt!).
- Ankuendigung: Nachricht mit `type` in `data/nachrichten.json` + Text in `data/bot_stimmen.json`
  (kein Text im Code), genau EINMAL je Ausloesung.
- Angriff: ueber den vorhandenen Raubzugweg, KEIN zweiter Angriffspfad.

## Wachen `tests/test_diplomatie_rache.py`

1. unter Goetterschutz bleibt der Topf nach 5 Tagen 0
2. ohne Schutz/ohne Kontakt nach 3 Tagen 3, nach 4 Tagen nicht 4 (Deckel je Tag)
3. Topf 3 mit SK 98: kein Angriff; mit SK 99: Angriff
4. genau EINE Ankuendigung je Ausloesung, VOR dem Angriff
5. nach Bot-Sieg Topf 0
6. aktiver Pakt blockiert den Angriff trotz Topf 3 (und der Topf steigt weiter)
7. alter Spielstand ohne `rache` laedt
8. hoechstens ein laufender Auftrag je Bot und Ziel
