# Umbauplan E3 — ein Bewegungssystem (`_welt_bewegen` über `auftraege.starten`)

**Stand:** 31.10.2026, `c8f2ccc` · **Grundlage:** `docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md`
(31.10.2026, `06aabcb`) · **Entscheidung Daniel (E3, 31.10.2026):** „Ein Bewegungssystem —
Altpfad über `auftraege.starten` leiten, nichts löschen."

**Arbeitsregel dieses Plans:** keine Code-Änderung, keine Datei außer dieser. Jede Zeilennummer
wurde am 31.10.2026 gegen `src/main.py`, `src/auftraege.py` und `src/kampfbericht.py` mit `grep -n`
nachgeschlagen. Die Landkarte ist an mehreren Stellen **veraltet** (Reisezeitfaktor, Speicherzeilen,
Ankunftsblock) — die abweichenden Stellen sind unten einzeln benannt.

**Zeilennummern:** nachgeschlagen am Arbeitsstand `623ff1e`. `src/main.py`, `src/auftraege.py`
und `src/kampfbericht.py` sind seit `c8f2ccc` unverändert (`git diff --stat c8f2ccc..HEAD`
liefert für diese drei Dateien nichts) — die Nummern gelten also für beide Stände.

---

## 1. Ist-Zustand

| Pfad | Einstiegspunkt (Datei:Zeile) | wie wird Zeit gerechnet | wie wird Beute/Verlust gerechnet | was ist anders als im Auftrags-Pfad |
|---|---|---|---|---|
| **A — Auftrag/Mission** (Zielsystem) | `main.auftrag_starten` `main.py:1940` → `auftraege.starten` `auftraege.py:264`; Oberfläche `main.py:5888` (`_auftrag_angriff`, `5871`) | `auftraege.reisezeit_sekunden` `auftraege.py:137-151`: `entfernung / GS · SEKUNDEN_JE_FELD`, `SEKUNDEN_JE_FELD = 7200.0` (`auftraege.py:56`, Faktor 2 seit `ef6f6f5`). GS = **langsamste** Einheit (`auftraege.py:119-123`, geprüft `299-301`). Ankunft `345-347`, Rückkehr doppelt (`HIN_UND_RUECK_FAKTOR` `auftraege.py:59`, `349`, `403`). Uhr: **Spielsekunden** (`main.py:1963`) | Beute **nur** über `kampfbericht.beute_am_ziel` (`kampfbericht.py:282-312`), eingehängt in `main.kampf_am_ziel` `main.py:2138-2144`; Buchung des Ziels vor Ort (`2141-2143`), Gutschrift des Spielers über `auftraege.spieldaten_anwenden` (`auftraege.py:542-545`), **genau einmal**. Verluste aus `kampf.fuehre_schlacht` (`main.py:2098-2106`), Rückkehr der Überlebenden `main.py:2050-2058` | — (Referenz) |
| **B — Weltkarte** (Altpfad) | `main._welt_bewegen` `main.py:5749-5782`; Auslöser `_on_map_click` `main.py:5704-5731`, Aufruf `5725`; Knopf „Truppen von hier bewegen" `main.py:5412` über `_welt_bewegung_starten` `5733` | `main.py:5759-5760`: `abstand = |dx|+|dy|` (durch `5724` immer **1**), `dauer = max(2, abstand*5)` **Minuten**; `arrival` `5770`. **GS völlig wirkungslos**, keine Rückreise | `main.py:7009-7016`: 10–40 % je Rohstoff **zufällig** aus `tile.resources`, **ohne Karren, ohne Ladungsgrenze, ohne Abbuchung**; Kampf `7017-7021`: 40 % Münzwurf gegen einen **beim Start zufällig gewürfelten** Bot (`5761-5765`), Verlust `randint(1,4)` auf **einer zufälligen Einheit** (`7019-7020`) | alles: keine Einheiten-Auswahl (`5751-5752` nimmt **alle**), keine GS, keine Karren, keine Ladung, keine Wallvorrunde, kein `kampf.fuehre_schlacht`, keine Rückreise, keine Reisekosten, kein Bericht im Auftragsformat |
| **C — Direktangriff** (Altknopf „Angreifen") | `main._attack` `main.py:5844-5852` → `_angriff_durchfuehren` `main.py:5591-5659` | **keine** — Kampf sofort im Klick | Beute ebenfalls `beute_am_ziel` (`main.py:5629-5631`), Buchung über `kampfbericht.spieldaten_anwenden` (`5641-5649`) | reist nicht, kostet nichts, kennt keine GS/Rückkehr — **nicht Teil von E3**, aber derselbe Truppenbestand |

**Speicher/Anzeige (Randbedingungen für den Umbau):**
`state.movements` wird angelegt `main.py:798`, gespeichert `2527`, geladen `2652`; die Restzeit
steht **nur** aus `movements` auf der Karte (`main.py:5537-5549`). Aufträge werden gespeichert
`main.py:2546`, geladen `2714`, angezeigt `main.py:3544-3561`, fortgeschrieben aus `tick`
(`main.py:2391`) über `auftraege_fortschreiben` (`2505`, Methode `1989`).

---

## 2. Die fünf Widersprüche — aktuelle Fundstelle und Stand nach der heutigen Änderung

Heute (`c8f2ccc`) wurden `kampfbericht.beute_am_ziel` eingeführt (Beute einheitlich gerechnet
**und beim Ziel abgebucht**) und der 300-Punkte-Sieg entfernt (`main.py:987-995`, E5: „KEIN
Sieg").

| # | Widerspruch | System A heute | System B heute | besteht weiter? |
|---|---|---|---|---|
| 1 | **Reisezeit** | `auftraege.py:56` + `137-151` + `345-347`: 7200 s je Feld und GS-Punkt (Faktor 2), langsamste Einheit bremst | `main.py:5759-5760` + `5770`: 5 Spielminuten je Feld, GS wirkungslos | **Ja.** Der Abstand ist sogar **größer** geworden: die Landkarte nannte für A noch `3600 s`; seit `ef6f6f5` sind es `7200 s`. Bei GS 5 sind das 24 min je Strecke gegen 5 min im Altpfad |
| 2 | **Wer reist** | `auftraege.py:292-304` (Bestand, GS, Ladung) + `154-159`; die Oberfläche wählt nach Rolle `main.py:5876-5879` | `main.py:5751-5752`: **alle** Einheiten mit `count > 0`, ohne Karren, ohne Auswahl | **Ja.** Unverändert — E3 muss diese Zeile ausdrücklich behandeln, sonst reist weiterhin das ganze Heer |
| 3 | **Beute** | `kampfbericht.beute_am_ziel` `kampfbericht.py:282-312`, eingehängt `main.py:2138-2144`; Gutschrift `auftraege.py:542-545` | `main.py:7009-7016`: 10–40 % zufällig, gutgeschrieben in `self.state.resources` (`7015-7016`), **das Feld behält alles** | **Ja — und jetzt allein.** Innerhalb von A ist „Güter aus dem Nichts" behoben (Befund Nr. 6). B ist damit die **einzige** Stelle im Code, die Rohstoffe ohne Abbuchung erzeugt. Da der 300-Punkte-Sieg weg ist, gibt es auch keine Punkteschwelle mehr, hinter der das auffiele |
| 4 | **Kampf** | `main.py:2098-2106`: `kampf.fuehre_schlacht` mit Wall, Sequenzen, Rollen, `kampfbericht.vorrunde` | `main.py:7017-7021`: 40 % Münzwurf, `randint(1,4)` Verlust auf einer **zufälligen** Einheit — der Zielbot wird schon beim Start gewürfelt (`5761-5765`), ohne Bezug zum Feld | **Ja.** Unverändert |
| 5 | **Rückweg** | `auftraege.py:59` + `349` + `403`, Heimkehr `main.py:2050-2058` | `main.py:7027-7030`: Einheiten kommen **im Ankunftstakt sofort** zurück, `movements`-Eintrag wird gelöscht (`7032`) | **Ja.** Unverändert |

**Folge für E3:** Solange B eigene Zeit-, Beute-, Kampf- und Rückregeln hat, ist jede neue
Wegzeit- oder Beuteformel eine dritte Wahrheit. Der Umbau muss deshalb **die vier Rechenschritte
von B ersetzen, nicht nur den Startpunkt**.

---

## 3. Kleinster sicherer Umbau

Leitlinie: `_welt_bewegen` **bleibt** als Funktion und als Name erhalten (E3: nichts löschen),
aber ihr Rumpf startet keinen eigenen Zug mehr, sondern einen Auftrag. Der alte Rumpf bleibt
darunter stehen und ist ab dem Umbau unerreichbar; `movements` bleibt im Spielstand lesbar.

**Schritt 1 — Feld als Ziel beschreiben.** Neue Hilfe `_welt_ziel_daten(self, x, y)` neben
`_welt_bewegen` (`main.py:5749`): liest das Feld über `state.get_tile` (`main.py:1071`) und
liefert ein Zielverzeichnis nach dem Vertrag von `auftraege.starten` (`auftraege.py:270-274`):
`{"name": koordinate, "tile_key": "x:y", "fremd": False, "vorraete": dict(tile.resources)}`.
**Darf nicht:** `tile.resources` selbst verändern, `wall_stufe` setzen (sonst greift die Vorrunde
in `auftraege.py:325-330` schon beim Start), einen Bot erfinden, Siedlungspositionen (`Settlement.x/y`,
`main.py:181-185`) anfassen.
**Prüfdatei:** `tests/test_weltkarte_auftrag.py` (fehlt).

**Schritt 2 — `_welt_bewegen` umleiten.** In `main.py:5749` nach der Leerprüfung (`5753-5758`)
`self._welt_zug_als_auftrag(start, ziel)` aufrufen und zurückkehren; der bisherige Rumpf
(`5759-5782`) bleibt als toter, kommentierter Altpfad stehen.
**Darf nicht:** Einheiten selbst abziehen (das tut `auftrag_starten` `main.py:1966-1967`), einen
Eintrag in `state.movements` anhängen (sonst reist dieselbe Truppe zweimal), Code löschen.
**Prüfdatei:** `tests/test_weltkarte_auftrag.py` (fehlt).

**Schritt 3 — Art und Ablehnungen festlegen.** `_welt_zug_als_auftrag(self, start, ziel)` (neu,
direkt unter `_welt_bewegen`): Art ist **`"angreifen"`** — nur diese der vier Arten
(`auftraege.py:49`) liefert Kampf **und** Beute **und** Heimkehr. Vorher drei Prüfungen:
(a) Zielfeld trägt eine **eigene** Siedlung → ablehnen mit Verweis auf „Einheiten stationieren"
(`main.py:5406`), (b) `state.noob_protection` und fremdes Ziel → ablehnen (Wortlaut aus
`main.py:7006-7007` bzw. `5845-5846`), (c) keine Truppen → bestehende Meldung `5755`.
Danach `self.state.auftrag_starten("angreifen", bestand, von, ziel, 1.0)`.
**Darf nicht:** gegen die eigene Siedlung kämpfen, einen Zielbot erfinden (`5761-5765` entfällt),
Passierbarkeit/Wasser neu regeln, `_welt_start`/`welt_auswahl` ändern.
**Prüfdatei:** `tests/test_weltkarte_auftrag.py` (fehlt) + `tests/test_goetterschutz_band.py` (vorhanden).

**Schritt 4 — Reisekosten auf eigener Karte.** In `auftraege.starten` `auftraege.py:353` die
Zeile `fremdes_ziel = bool(ziel.get("fremd")) or art == "angreifen"` so fassen, dass ein
**ausdrücklich** als `"fremd": False` gemeldetes Ziel kein Mana kostet (`MANA_GRUND = 5.0` usw.
`auftraege.py:232-234`, `258-260`); fehlt der Schlüssel, bleibt die heutige Regel.
**Darf nicht:** den Diplomatie-Angriff verbilligen (`main.py:5883` setzt `"fremd": True`), die
Mana-Regel für fremde Ziele oder die Gold-/Nahrungssätze (`230-231`) ändern.
**Prüfdatei:** `tests/test_reisekosten_eigene_karte.py` (fehlt) + `tests/test_auftraege.py` (vorhanden).

**Schritt 5 — Feldbeute beim Ziel abbuchen.** In `auftraege_fortschreiben` (`main.py:2014-2021`)
vor `self.kampf_am_ziel(eintrag)` das Feld über `eintrag["ziel"]["tile_key"]` **frisch** auflösen
und `eintrag["ziel"]["vorraete"]` an das lebende `tile.resources` hängen; `kamf_am_ziel` schreibt
danach über `vorraete_ziel.clear()/update()` (`main.py:2141-2143`) in genau dieses Verzeichnis.
**Darf nicht:** dieselbe Beute zweimal gutschreiben, nach dem Laden (`main.py:2714`) eine
entkoppelte Kopie abbuchen (das wäre Befund Nr. 6 an neuer Stelle), `tile.resources` negativ
machen (`kampfbericht.py:311` deckelt bereits auf 0).
**Prüfdatei:** `tests/test_weltkarte_beute.py` (fehlt) + `tests/test_beute_am_ziel.py` (vorhanden).

**Schritt 6 — Rückweg nicht neu bauen.** Nichts ändern: `HIN_UND_RUECK_FAKTOR` (`auftraege.py:59`)
und die Heimkehr in `main.py:2050-2058` gelten automatisch; nur prüfen, dass die Einheiten
**genau einmal** zurückkommen (`heimgekehrt`-Merker `2052`).
**Darf nicht:** Einheiten am Ziel lassen (das ist allein `stationieren`, `2053-2054`), doppelt
gutschreiben, die Reisezeitformel anfassen.
**Prüfdatei:** `tests/test_gpt_zeit_auftragsketten.py` (vorhanden).

**Schritt 7 — Anzeige auf der Karte.** In `main.py:5537-5549` zusätzlich zu `movements` die
Aufträge dieses Feldes aus `auftraege.fortschritt` (`main.py:3554`) zeichnen (Restzeit + Art),
damit ein umgeleiteter Zug nicht unsichtbar wird.
**Darf nicht:** die `movements`-Anzeige entfernen (alte Stände), dieselbe Truppe doppelt zählen,
die Zoom-/Scroll-Logik (`5530-5550`) verändern.
**Prüfdatei:** `tests/test_weltkarte.py` (vorhanden, Z. 75 und 176).

**Schritt 8 — Altpfad stilllegen, nicht löschen.** `_tick_loop` `main.py:6996-7032` unverändert
lassen (läuft für neue Züge leer, weil nichts mehr angehängt wird), mit einem Hinweiskommentar
auf `_welt_zug_als_auftrag` versehen; `movements` bleibt in Speichern (`2527`) und Laden (`2652`).
**Darf nicht:** den Block entfernen, alte Spielstände unlesbar machen, `state.movements` aus dem
Spielstand nehmen.
**Prüfdatei:** `tests/test_speichern_robust.py` (vorhanden) + `tests/test_weltkarte_auftrag.py` (fehlt).

---

## 4. Risiken

1. **Zeitsprung.** Ein Nachbarfeld kostet künftig `7200 / GS` Sekunden je Strecke statt 5 Minuten
   (`auftraege.py:56` gegen `main.py:5760`). Bei GS 5 sind das 24 min hin und 24 min zurück —
   jede Kartenbewegung wird rund zehnmal langsamer, und die Rückreise gibt es neu. Das ist die
   gewollte Vereinheitlichung, aber eine spürbare Balanceänderung.
2. **Jeder Zug wird ein Angriff.** `"angreifen"` erzwingt Schlagkraft (`auftraege.py:320-324`) —
   ein reiner Karrenzug wird abgelehnt, obwohl der Altpfad ihn erlaubte. Ohne Schritt 4 zahlt
   außerdem jeder Zug Gold, Nahrung **und 5,5 Mana** (`auftraege.py:232-234`, `353`).
3. **Doppelbuchung der Truppe.** Zieht `_welt_bewegen` weiter selbst ab (`5775-5776`) oder hängt
   weiter an `movements` (`5766`), reist dieselbe Einheit zweimal bzw. verschwindet. Der Umbau
   muss den alten Rumpf unerreichbar machen, nicht nur „überspringen".
4. **Beute über eine Kopie.** `auftraege.starten` kopiert das Ziel nur flach
   (`auftraege.py:303`, `dict(nach)`); nach Speichern/Laden (`main.py:2714`) zeigt
   `ziel["vorraete"]` nicht mehr auf `tile.resources` — dann entstehen Güter aus dem Nichts,
   genau der heutige Befund Nr. 6 an neuer Stelle. Schritt 5 ist deshalb Pflicht, nicht Kür.
5. **Zwei Wahrheiten in der Übergangszeit.** Alte Spielstände mit `movements` rechnen weiter nach
   den Altregeln (`main.py:6996-7032`), und dieser Block läuft auch bei gesetztem `spielende`
   (die Prüfung `6987` umschließt ihn nicht). `kamf_am_ziel` prüft den Götterschutz nicht selbst
   (nur `5845` und `7006`) — die Prüfung aus Schritt 3 ist die einzige.
