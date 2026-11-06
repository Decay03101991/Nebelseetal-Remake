# Pruefvermerk: Geminis Menue-Teilgeschichten (06.11.2026)

**Geprueft:** fuenf Vorschlaege aus `docs/eingaenge/GEMINI_ANTWORTEN_20261106/Antwort_Gemini_MENUESTORIES_20261106.txt`
gegen unser Spiel (Kopf `c90d7d8`). **Ergebnis: vier Texte sind brauchbar, einer nicht; der Ton passt
bei KEINEM** - und zwei der vier sind keine Texte, sondern versteckte Mechaniken.

## 1. Der schwerste Befund: der Ton stimmt nicht

`data/story.json` traegt oben den Ton, den Daniel am 04.11.2026 entschieden hat, woertlich:
"abenteuerlich und leicht - Aufbruch, Entdecken, Humor ... kein Pathos, kein Weltschmerz, aber ein
Ziel."

Geminis Texte sind das Gegenteil: "Die Leere vergisst nicht", "Die Klingen schaerfen", "Krank erinnert
an eine alte Schuld", "in Stein gemeisselt". Das ist dunkle Fantasy, nicht unser Ton.
**Folge: alle fuenf Texte werden vor dem Einbau neu geschrieben** - Inhalt (Anlass, Ort, Wirkung) kann
bleiben, die Sprache nicht. Der Ton kommt aus der Datendatei, nicht aus dem Modell.

## 2. Was in den Vorschlaegen technisch nicht stimmt

| Vorschlag | Befund |
|---|---|
| "Strings niemals in `src/gui_berater.py`" | Die Datei heisst `src/berater.py`; die Regel selbst ist richtig - Texte gehoeren in Datendateien. |
| `state.bots["haug"]["favor_warnung"]` | `BotPlayer` ist eine **dataclass**; Zugriff ueber Felder, neue Felder muessen in `bot_als_dict`/`bot_aus_dict` mitgefuehrt werden, sonst sind sie nach dem Speichern weg. |
| "Antwort A erhoeht Gunst um 5, falls Gold gesendet wird" | Das ist **keine Textantwort, sondern eine Mechanik** - und "Gold senden" gibt es nicht. Die Gunst entsteht erst mit S4; die Story haengt damit an S4. |
| "Antwort B senkt Gunst sofort um 10" | dito: eine Mechanik, keine Erzaehlung. |
| `state.forschungen_entdeckt`, `state.kaserne_errichtet`, `state.ruhmeshalle_besucht` | Freie Feldnamen ohne Ableitung. Wir haben bereits zwei Wege: Spielstand-Felder (je Speicherstand) und die Merkdatei (`story.intro_gesehen`/`intro_merken`). Ein "einmal gesehen" fuer eine Story im Spielverlauf gehoert in den **Spielstand**, nicht in die Merkdatei - sonst sieht ein zweiter Spielstand die Geschichte nie. |
| "permanenter Archiv-Hinweis im Portalmenue" (Antwort B) | Neues dauerhaftes Anzeigeelement ohne Vorbild - erst nach S1 (Postfach-Archiv) sinnvoll, dort gibt es einen Archivbegriff. |

## 3. Urteil je Geschichte

| Nr. | Menuepunkt | Ausloeser brauchbar? | Text brauchbar? | Einbau |
|---|---|---|---|---|
| 1 | Forschung (erste Bibliothek) | ja: der Menuepunkt erscheint genau dann (Freischaltung ueber `bibliothek`, `MENUE_BEDINGUNG`) | Inhalt ja, Ton nein | **S1b**, reine Anzeige |
| 2 | Portal (erster Weltwechsel) | ja: `state.eigene_dimension` wechselt, Sperre 24 Spielstunden | Inhalt ja, Ton nein | **S1b**, Overlay vorhanden - staerkste Geschichte, wie Gemini selbst sagt |
| 3 | Kaserne (Kriegerakademie fertig) | ja: Freischaltung ueber `kriegerakademie` | Inhalt ja, Ton nein | **S1b**, Textblock unter der Warteschlange; darf die Bedingungsanzeige aus A1 nicht verdraengen |
| 4 | Diplomatie (Haug unter Gunst 40) | **nein, heute nicht**: Gunst existiert erst mit S4 | nein (zwei Mechaniken) | **erst nach S4**, als reine Bot-Stimme ohne Antwortknoepfe |
| 5 | Ruhmeshalle (erstes Oeffnen) | ja: Menuepunkt steht in der Leiste (Zeile 3373) | Inhalt ja, Ton nein | **S1b**, Overlay beim ersten Betreten |

## 4. Was daraus fuer die Umsetzung folgt

1. **Vier Texte** (Forschung, Portal, Kaserne, Ruhmeshalle) kommen als reine Anzeige in die
   Datendatei - Muster: `data/story.json` bekommt einen eigenen Bereich, `src/story.py` liest ihn
   (EINE Lesestelle, kein Text im Code). Nichts davon aendert eine Spielzahl.
2. **Einmal-Flags** liegen im Spielstand (je Speicherstand), mit `.get`-Fallback fuer alte Staende;
   die Merkdatei bleibt fuer den Spielstart (Intro).
3. **Die Diplomatie-Geschichte** wird auf eine Stimme ohne Antworten reduziert und an S4 gehaengt.
4. **Alle Texte werden vor dem Einbau von uns neu geschrieben** (Ton aus `data/story.json`, hoechstens
   drei Saetze, keine neuen Zahlen) - Geminis Wortlaut ist Vorlage, nicht Lieferung.
5. **Kein Antwortknopf ohne Mechanik:** was eine Wirkung haben soll, laeuft ueber die in S4
   entschiedenen Wege (Gunst, Rachetopf), nicht ueber eine Textzeile.

**Offene Frage an Daniel (eine):** sollen die zwei Antworten der Portal-Geschichte eine Wirkung haben
(derzeit: nur Text) - und wenn ja, welche ohne neue Mechanik?
