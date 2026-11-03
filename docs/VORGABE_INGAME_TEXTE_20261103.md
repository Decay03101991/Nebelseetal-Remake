# Vorgabe: Ingame-Texte mit echten Umlauten (Daniel, 03.11.2026)

## Wortlaut

> „Eine wichtige Regel fürs Gesamte Ingame und die Optik, wie du es umsetzt ist mir egal aber es ist
> verpflichtend. Ich will Ingame NICHT das du zum Beispiel statt ‚wählen' einfach plump ‚waehlen'
> schreibst. Solche kleinigkeiten machen viel aus im Gesamteindruck. Wann du das umsetzt im bezug auf
> den ablauf ist mir egal.“

## Was die Regel verlangt

| Gegenstand | Regel |
|---|---|
| Alles, was der Spieler LIEST | echte deutsche Rechtschreibung: `wählen`, `Gebäude`, `für`, `können`, `müssen`, `Größe`, `möglich`, `zurück`, `nächste`, `schließen`, `öffnen`, `prüfen`, `Übersicht`, `Verfügbar`, `Bevölkerung`, `gründen` |
| Knöpfe, Menüs, Reiter, Dialoge, Tooltips | ebenso - ein „Auswaehlen“ auf einem Knopf ist ein Fehler |
| Meldungen, Postfach, Spiel-Log, Fehlertexte | ebenso |
| Anzeigenamen aus `data/` (Gebäude, Einheiten, Forschung, Waren) | ebenso, WENN sie angezeigt werden - die KENNUNG bleibt ASCII |
| Code-Kennungen, Dict-Schlüssel, Dateinamen, JSON-Schlüssel | bleiben ASCII (`holzfaeller`, `verteidigungswall`, `siedler`) - sie sind keine Anzeige |
| Kommentare und Docstrings in `.py` | bleiben ASCII (Projektregel: die Prüfdateien sind ASCII-only, und Kommentare sind keine Anzeige) |
| Dokumente unter `docs/` | duerfen Umlaute tragen (sie tun es bereits) |

**Die ASCII-Regel fuer `.py` bleibt in Kraft** - sie gilt fuer Code und Kommentare. Anzeigetexte waren
davon schon immer ausgenommen; diese Vorgabe macht daraus eine Pflicht.

## Ist-Stand (gemessen 03.11.2026)

Die Texte sind gemischt: `Neue Siedlung ... gegründet` und `im Dorfzentrum steht jetzt „Karte
öffnen“` tragen echte Umlaute, daneben stehen Ersatzschreibweisen (`waehlen`, `Gebaeude`, `fuer`,
`koennen`). Ein erster Zaehlversuch ueber alle String-Literale in `src/` lieferte **13.447 Treffer** -
das ist KEINE brauchbare Zahl: der Zaehler hat Docstrings, Hex-Farben und JSON-Schluessel
mitgezaehlt. Er taugt als Hinweis auf die Groesse, nicht als Messwert. Das Inventurwerkzeug muss
deshalb erst praezise werden (nur Strings, die wirklich in die Oberflaeche gehen).

## Umsetzung (Schnitt T-1, offen)

1. **Praezises Inventurwerkzeug** (`tools/anzeigetexte_inventur.py`): je Datei die String-Literale
   sammeln, die in eine Anzeige gehen (`text=`, `insert(`, `configure(` mit `text`, `_log(`,
   `messages.append`, `StringVar.set`) und darin die Ersatzschreibweisen zaehlen; Kennungen,
   Docstrings und Datenschluessel ausschliessen. Ergebnis als Tabelle in `docs/`.
2. **Schnittweise ersetzen**, Datei fuer Datei (kleinste zuerst, `main.py` zuletzt), je Datei
   `python -X utf8 -c "import <modul>"` und die betroffenen Pruefdateien.
3. **Wache** `tests/test_anzeigetexte_umlaute.py`: eine Wortliste (`waehlen`, `auswaehlen`,
   `Gebaeude`, `fuer`, `koennen`, `muessen`, `groesse`, `moeglich`, `zurueck`, `naechste`,
   `aendern`, `zusaetzlich`, `hoechstens`, `schliessen`, `oeffnen`, `pruefen`, `uebersicht`,
   `verfuegbar`, `bevoelkerung`, `gruenden`, `waere`, `ueber`, `koennte`, `muesste`) darf in
   ANZEIGE-Strings nicht mehr vorkommen; technische Ausnahmen stehen als Liste IN der Pruefdatei mit
   Begruendung.
4. **Jede umgestellte Wache** (eine, die den alten Wortlaut sucht) wird umbenannt und die Entscheidung
   im Kommentar genannt - nicht der Code zurueckgebogen (Projektregel).

## Warum das ein eigener Schnitt ist

Jede geaenderte Anzeige kann eine Wache brechen, die den alten Wortlaut sucht (`grep -rn
"<altes Wort>" tests/`). Ein Sammellauf dauert 8 Minuten; ein Schwung ueber 100 Texte ohne
Zwischenpruefung ist deshalb teurer als drei kleine Schnitte mit je einem Lauf.
