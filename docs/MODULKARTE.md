# Modulkarte — welche Datei wofür, und wer wen aufruft

**Erzeugt von `tools/modulkarte_bauen.py` — nicht von Hand ändern.** Stand: siehe Git-Historie.

64 Dateien in `src/`, 38989 Zeilen, 1145 Funktionen und Klassen auf oberster Ebene.

## Die Karte

| Datei | Zeilen | Zweck (erste Zeile des Docstrings) | wird gebraucht von |
|---|---:|---|---|
| `main.py` | 16993 | Nebelseetal Remake — Core Game Engine | public_start.py |
| `spieloekonomie.py` | 1888 | Nebelseetal Remake — deterministischer Kern der Spielökonomie (Ökonomie-Paket, Schritt 2). | admin_teststand.py, admin_werkzeuge.py, botkern.py, main.py, spielschicht.py, verwundete.py |
| `diplomatie.py` | 994 | Diplomatie der Bots - Gunst, Status (S4 Teil 1, 06.11.2026). | main.py |
| `spielschicht.py` | 926 | Nebelseetal Remake - FACH-SCHICHT (Spielebene) fuer die Oberflaeche. | main.py |
| `welt_optik_fein.py` | 898 | FEINERE Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (naechste Ausbaustufe). | main.py |
| `karten_optik_fein.py` | 863 | Feinere Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes | main.py |
| `bottaktik.py` | 815 | Nebelseetal Remake - Bot-Taktik (Paket BT, 01.11.2026). | main.py |
| `auftraege.py` | 754 | Nebelseetal Remake - Auftraege und Missionen (Paket WA, 04.10.2026). | bottaktik.py, main.py, spieloekonomie.py, spielschicht.py |
| `drachen.py` | 710 | Drachen des Spiels - Daten lesen, Figur oder Ruine bestimmen, Siege merken (W-14 Teil 1). | main.py |
| `botkern.py` | 668 | Nebelseetal Remake - Bot-Kern (Paket W5, 05.10.2026). | main.py, spielschicht.py |
| `portalraum.py` | 612 | Portal- und Limbus-Raum fuer das Nebelseetal-Remake (Paket W5-2). | drachen.py, main.py, spielschicht.py |
| `welt_optik.py` | 600 | Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (Paket: feinere Weltkartenoptik). | main.py |
| `karten_optik.py` | 599 | Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes (Paket: feinere Kartenoptik). | main.py |
| `kampfbericht.py` | 575 | Nebelseetal Remake - Kampfbericht (Paket W2b, 04.10.2026). | auftraege.py, main.py, spielschicht.py |
| `weltkarte_malerei.py` | 564 | Gemalte Weltkarte fuer das Nebelseetal-Remake (Designschritt D-3, 09.11.2026). | main.py |
| `punkte.py` | 529 | Nebelseetal Remake — Punkte, Rangliste, Goetterschutz und Sieg/Niederlage (Paket W6, 04.10.2026). | botkern.py, main.py, spielschicht.py |
| `kampf.py` | 487 | Nebelseetal – Kampfsystem des späteren Original-Forumstexts. | main.py |
| `wirtschaft.py` | 434 | Wirtschaft — stuendlicher Rohstoffertrag der Siedlungen (Remake Nebelseetal). | diplomatie.py, gpt_versorgungsdiagnose.py, main.py, spielerhilfe.py, spieloekonomie.py, spielschicht.py, versorgungsschutz.py |
| `werkstatt.py` | 422 | Nebelseetal Remake - Waren und Werkstaetten (Paket W3, 04.10.2026). | main.py, spieloekonomie.py, spielschicht.py |
| `spionage.py` | 410 | Spionage: Schalter, Aufklaerungswert, Bericht und Nachricht (Stufe B-5, 02.11.2026). | auftraege.py, main.py |
| `berater.py` | 399 | Berater — die Auskunft im Spiel (Reiter "Chat"). | main.py, spielerhilfe.py |
| `forschungspfad.py` | 354 | Forschungspfad -- die fachliche Frageschicht rund um die 21 Originalforschungen. | main.py, spieloekonomie.py |
| `gebaeude_wirkung.py` | 353 | Nebelseetal Remake — Wirkungen der 20 Originalgebaeude (Paket W4b-5, 04.10.2026). | bot_angriffsplanung.py, dorfwall.py, kampfbericht.py, main.py, spieloekonomie.py, spielschicht.py |
| `speichern.py` | 338 | Robustes Speichern (Paket W8) - atomar, geprueft, mit Sicherung und Wiederherstellung. | main.py, spielstaende.py |
| `einheiten.py` | 316 | Nebelseetal Remake — Einheiten-Bruecke. | admin_teststand.py, admin_werkzeuge.py, auftraege.py, bonus_system.py, bot_angriffsplanung.py, botkern.py, drachen.py, gebaeude_wirkung.py, kampf.py, kampfbericht.py, main.py, punkte.py, spieloekonomie.py, spielschicht.py, spionage.py |
| `gebaeude_optik.py` | 306 | Gebaeude-Optik: Menue-Icons und Menue-Hintergruende der 20 Originalgebaeude. | main.py |
| `dorfwall.py` | 295 | Isolierter Wallkern fuer Nebelseetal (GPT-Zuarbeit, 28.10.2026). | main.py |
| `spieldaten.py` | 276 | Nebelseetal Remake — Datenschicht. | admin_werkzeuge.py, ausruestung.py, berater.py, bot_angriffsplanung.py, diplomatie.py, drachen.py, einheiten.py, forschung.py, forschung_wirkung.py, gebaeude_optik.py, gebaeude_wirkung.py, gelaende.py, gpt_versorgungsdiagnose.py, kampf.py, main.py, marsch_optik.py, originalkarten.py, originalkarten_grafik.py, spieloekonomie.py, spielschicht.py, spielzeit.py, spionage.py, stimmen.py, story.py, welt.py, werkstatt.py, wirtschaft.py |
| `gelaende.py` | 275 | Gelaende und Siedlungskarte fuer das Nebelseetal-Remake. | admin_teststand.py, admin_werkzeuge.py, baumenue_info.py, berater.py, gebaeude_wirkung.py, gpt_versorgungsdiagnose.py, karten_optik_fein.py, main.py, originalkarten.py, portalraum.py, spieloekonomie.py, spielschicht.py, versorgungsschutz.py, weltkarte_malerei.py, werkstatt.py, wirtschaft.py |
| `ausruestung.py` | 273 | Nebelseetal Remake — Ausruestung: welche Waren eine Einheit zur Ausbildung braucht. | main.py, spieloekonomie.py |
| `postfach.py` | 261 | Postfach: Fristen, Archiv, Blaettern und Ruhm-Rang - die EINE Rechenstelle (S1, 06.11.2026). | main.py |
| `bot_angriffsplanung.py` | 254 | GPT-B01: konservative Bot-Zielwahl nach den Wallregeln der Originalanleitung. | main.py |
| `admin_werkzeuge.py` | 246 | Isolierte Admin-Testwerkzeuge (keine Aenderung der normalen Spielregeln). | admin_oberflaeche.py |
| `forschung.py` | 232 | Nebelseetal Remake — zeitlicher Ablauf der Forschung (reine Rechenlogik). | main.py, spieloekonomie.py, spielschicht.py |
| `tor.py` | 231 | Passworttor fuer das Nebelseetal-Remake (Schritt 8 in `docs/WEG_ZUR_EXE.md`). | main.py |
| `story.py` | 213 | Geschichte des Spiels (Story 1, 04.11.2026). | berater.py, main.py |
| `verwundete.py` | 195 | S3 Verwundetenheilung (06.11.2026) - die EINE Rechenstelle fuer Verwundete. | main.py |
| `admin_oberflaeche.py` | 191 | Nur die Bedienoberflaeche fuer Admin-Testwerkzeuge. | main.py |
| `boni.py` | 190 | Die Wirkung der Volks- und Taktikboni: Datenschicht und Rechnung (V-5, 03.11.2026). | bottaktik.py, main.py, spieloekonomie.py, spielschicht.py, wirtschaft.py |
| `originalkarten.py` | 190 | Original-Kartenkatalog Nebelseetal, 127 archivierte Grafiken in 3 Qualitaetsgruppen. | gelaende.py, main.py, spieloekonomie.py, spielschicht.py |
| `forschung_wirkung.py` | 188 | Nebelseetal Remake -- Wirkung der 21 Originalforschungen auf die Produktion. | bonus_system.py, gebaeude_wirkung.py, main.py |
| `oberflaeche_original.py` | 185 | Nebelseetal Remake - Menue-Vergleich (Paket W7, 04.10.2026). | — (Einstieg oder ungenutzt) |
| `spielerhilfe.py` | 176 | FIX04c – Spielerhilfe während des Götterschutzes, jederzeit aufrufbar. | admin_werkzeuge.py, main.py |
| `welt.py` | 171 | Weltkarte des Limbus fuer das Nebelseetal-Remake. | main.py, portalraum.py |
| `bonus_system.py` | 169 | Nebelseetal Remake — Central Bonus System | main.py, wirtschaft.py |
| `spielzeit.py` | 169 | Spielzeit — der Zeitfaktor (Vorgabe Daniel 05.10.2026, Spielbericht). | main.py |
| `ruinendeckung.py` | 163 | Ruinendeckung: eine besiegte Ruine deckt die Richtung, in der sie liegt (Frage 9, Register 216). | main.py |
| `spielstand_archiv.py` | 162 | Private Spielstandarchive: eindeutig, zeitgestempelt, ohne unbemerktes Loeschen. | main.py, speichern.py |
| `versorgungsschutz.py` | 160 | Reine Vorabpruefung auf selbst verschuldete Rohstoff-Sackgassen. | main.py |
| `marsch_optik.py` | 150 | Nebelseetal Remake - Optik der Truppenbewegungen auf der Weltkarte (Stufe M-1, 02.11.2026). | main.py |
| `fehlbestand.py` | 140 | Fehlbestand: welche Rohstoffe fehlen und um wieviel. | spieloekonomie.py |
| `baumenue_info.py` | 133 | FIX04 – Datenmodell fuer das historische Baumenue der Siedlungskarte. | main.py |
| `gpt_versorgungsdiagnose.py` | 126 | Nur-lesende Versorgungsdiagnose fuer Nebelseetal. | — (Einstieg oder ungenutzt) |
| `admin_teststand.py` | 125 | Reproduzierbarer Admin-Teststand: keine Aenderung von Originalertraegen. | main.py |
| `voelker.py` | 118 | Die sechs Fraktionen (Voelker) als eigene Datenschicht - Lesen, Pruefen, Verteilen (A2, 03.11.2026). | bottaktik.py, main.py |
| `zeitbasis.py` | 110 | Eine einzige Trennung von Rechnerzeit, Laufzeit und Spielzeit. | botkern.py, diplomatie.py, main.py, punkte.py, spieloekonomie.py |
| `stimmen.py` | 107 | Stimmen der fuenf Bots (Story 2, 04.11.2026). | main.py |
| `hilfen.py` | 74 | Kleine, reine Helfer, die mehrere Module brauchen. | auftraege.py, einheiten.py, kampfbericht.py, main.py, spionage.py |
| `haeuser.py` | 61 | Die sechs Haeuser der Welt als eigene Datenschicht - Name, Sitz, Farben, Burg und Wappen (W-15). | main.py |
| `spielstaende.py` | 52 | Drei stabile, unabhaengige Speicherslots und ein gesonderter Admin-Teststand. | main.py |
| `gildenrangliste_original.py` | 48 | Historische Gildenwertung als reine, inaktive Datenfunktion. | — (Einstieg oder ungenutzt) |
| `originalkarten_grafik.py` | 36 | Authentische Rasterbilder der 127 Originalkarten, keine Legacy-Symbole. | main.py |
| `public_start.py` | 26 | Windows-Testbuild: normaler Spielerweg, getrennte Laufzeitdaten. | — (Einstieg oder ungenutzt) |
| `ausgabemodus.py` | 11 | Laufzeitmodus der getrennten Windows-Testfassung. | main.py |

## Lesart der Spalte „wird gebraucht von“

Steht dort `—`, ist die Datei entweder der Einstieg (`main.py`) oder sie wird von niemandem mehr importiert (möglicher Rest, siehe `tools/code_mass.py`).
