# Modulkarte — welche Datei wofür, und wer wen aufruft

**Erzeugt von `tools/modulkarte_bauen.py` — nicht von Hand ändern.** Stand: siehe Git-Historie.

49 Dateien in `src/`, 21703 Zeilen, 674 Funktionen und Klassen auf oberster Ebene.

## Die Karte

| Datei | Zeilen | Zweck (erste Zeile des Docstrings) | wird gebraucht von |
|---|---:|---|---|
| `main.py` | 7375 | Nebelseetal Remake — Core Game Engine | public_start.py |
| `spieloekonomie.py` | 1072 | Nebelseetal Remake — deterministischer Kern der Spielökonomie (Ökonomie-Paket, Schritt 2). | admin_teststand.py, admin_werkzeuge.py, botkern.py, main.py |
| `welt_optik_fein.py` | 898 | FEINERE Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (naechste Ausbaustufe). | main.py |
| `karten_optik_fein.py` | 863 | Feinere Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes | main.py |
| `spielschicht.py` | 664 | Nebelseetal Remake - FACH-SCHICHT (Spielebene) fuer die Oberflaeche. | — (Einstieg oder ungenutzt) |
| `auftraege.py` | 638 | Nebelseetal Remake - Auftraege und Missionen (Paket WA, 04.10.2026). | main.py, spieloekonomie.py |
| `botkern.py` | 622 | Nebelseetal Remake - Bot-Kern (Paket W5, 05.10.2026). | main.py |
| `welt_optik.py` | 600 | Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (Paket: feinere Weltkartenoptik). | main.py |
| `karten_optik.py` | 599 | Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes (Paket: feinere Kartenoptik). | main.py |
| `kampfbericht.py` | 492 | Nebelseetal Remake - Kampfbericht (Paket W2b, 04.10.2026). | auftraege.py, main.py, spielschicht.py |
| `punkte.py` | 456 | Nebelseetal Remake — Punkte, Rangliste, Goetterschutz und Sieg/Niederlage (Paket W6, 04.10.2026). | botkern.py, main.py, spielschicht.py |
| `werkstatt.py` | 422 | Nebelseetal Remake - Waren und Werkstaetten (Paket W3, 04.10.2026). | main.py, spieloekonomie.py, spielschicht.py |
| `kampf_alt_handbuch_2009.py` | 401 | Nebelseetal Remake — Kampfablauf nach dem Originalhandbuch (Seiten 20-23). | — (Einstieg oder ungenutzt) |
| `kampf.py` | 398 | Nebelseetal – Kampfsystem des späteren Original-Forumstexts. | main.py |
| `berater.py` | 374 | Berater — die Auskunft im Spiel (Reiter "Chat"). | main.py, spielerhilfe.py |
| `forschungspfad.py` | 350 | Forschungspfad -- die fachliche Frageschicht rund um die 21 Originalforschungen. | main.py, spieloekonomie.py |
| `gebaeude_wirkung.py` | 344 | Nebelseetal Remake — Wirkungen der 20 Originalgebaeude (Paket W4b-5, 04.10.2026). | bot_angriffsplanung.py, dorfwall.py, kampfbericht.py, main.py, spieloekonomie.py, spielschicht.py |
| `speichern.py` | 338 | Robustes Speichern (Paket W8) - atomar, geprueft, mit Sicherung und Wiederherstellung. | main.py, spielstaende.py |
| `ausruestung.py` | 273 | Nebelseetal Remake — Ausruestung: welche Waren eine Einheit zur Ausbildung braucht. | main.py, spieloekonomie.py |
| `wirtschaft.py` | 252 | Wirtschaft — stuendlicher Rohstoffertrag der Siedlungen (Remake Nebelseetal). | gpt_versorgungsdiagnose.py, main.py, spielerhilfe.py, spieloekonomie.py, spielschicht.py, versorgungsschutz.py |
| `admin_werkzeuge.py` | 246 | Isolierte Admin-Testwerkzeuge (keine Aenderung der normalen Spielregeln). | admin_oberflaeche.py |
| `gelaende.py` | 233 | Gelaende und Siedlungskarte fuer das Nebelseetal-Remake. | admin_teststand.py, admin_werkzeuge.py, baumenue_info.py, berater.py, gebaeude_wirkung.py, gpt_versorgungsdiagnose.py, karten_optik_fein.py, main.py, originalkarten.py, spieloekonomie.py, spielschicht.py, versorgungsschutz.py, werkstatt.py, wirtschaft.py |
| `forschung.py` | 232 | Nebelseetal Remake — zeitlicher Ablauf der Forschung (reine Rechenlogik). | main.py, spieloekonomie.py, spielschicht.py |
| `tor.py` | 231 | Passworttor fuer das Nebelseetal-Remake (Schritt 8 in `docs/WEG_ZUR_EXE.md`). | main.py |
| `spieldaten.py` | 229 | Nebelseetal Remake — Datenschicht. | admin_werkzeuge.py, ausruestung.py, berater.py, einheiten.py, forschung.py, forschung_wirkung.py, gebaeude_wirkung.py, gelaende.py, gpt_versorgungsdiagnose.py, kampf.py, kampf_alt_handbuch_2009.py, main.py, originalkarten.py, originalkarten_grafik.py, spieloekonomie.py, spielschicht.py, spielzeit.py, welt.py, werkstatt.py |
| `portalraum.py` | 216 | Portal- und Limbus-Raum fuer das Nebelseetal-Remake (Paket W5-2). | main.py, spielschicht.py |
| `einheiten.py` | 206 | Nebelseetal Remake — Einheiten-Bruecke. | admin_teststand.py, admin_werkzeuge.py, auftraege.py, bonus_system.py, bot_angriffsplanung.py, botkern.py, gebaeude_wirkung.py, kampf.py, kampf_alt_handbuch_2009.py, kampfbericht.py, main.py, punkte.py, spieloekonomie.py, spielschicht.py |
| `admin_oberflaeche.py` | 191 | Nur die Bedienoberflaeche fuer Admin-Testwerkzeuge. | main.py |
| `oberflaeche_original.py` | 185 | Nebelseetal Remake - Menue-Vergleich (Paket W7, 04.10.2026). | — (Einstieg oder ungenutzt) |
| `forschung_wirkung.py` | 177 | Nebelseetal Remake -- Wirkung der 21 Originalforschungen auf die Produktion. | bonus_system.py |
| `spielerhilfe.py` | 176 | FIX04c – Spielerhilfe während des Götterschutzes, jederzeit aufrufbar. | admin_werkzeuge.py, main.py |
| `bonus_system.py` | 169 | Nebelseetal Remake — Central Bonus System | main.py, wirtschaft.py |
| `spielzeit.py` | 169 | Spielzeit — der Zeitfaktor (Vorgabe Daniel 05.10.2026, Spielbericht). | main.py |
| `spielstand_archiv.py` | 162 | Private Spielstandarchive: eindeutig, zeitgestempelt, ohne unbemerktes Loeschen. | main.py, speichern.py |
| `versorgungsschutz.py` | 160 | Reine Vorabpruefung auf selbst verschuldete Rohstoff-Sackgassen. | main.py |
| `fehlbestand.py` | 140 | Fehlbestand: welche Rohstoffe fehlen und um wieviel. | spieloekonomie.py |
| `welt.py` | 135 | Weltkarte des Limbus fuer das Nebelseetal-Remake. | main.py, portalraum.py |
| `baumenue_info.py` | 133 | FIX04 – Datenmodell fuer das historische Baumenue der Siedlungskarte. | main.py |
| `originalkarten.py` | 128 | Original-Kartenkatalog Nebelseetal, 127 archivierte Grafiken in 3 Qualitaetsgruppen. | gelaende.py, main.py, spieloekonomie.py, spielschicht.py |
| `gpt_versorgungsdiagnose.py` | 126 | Nur-lesende Versorgungsdiagnose fuer Nebelseetal. | — (Einstieg oder ungenutzt) |
| `admin_teststand.py` | 125 | Reproduzierbarer Admin-Teststand: keine Aenderung von Originalertraegen. | main.py |
| `dorfwall.py` | 125 | Isolierter Wallkern fuer Nebelseetal (GPT-Zuarbeit, 28.10.2026). | main.py |
| `bot_angriffsplanung.py` | 108 | GPT-B01: konservative Bot-Zielwahl nach den Wallregeln der Originalanleitung. | main.py |
| `zeitbasis.py` | 103 | Eine einzige Trennung von Rechnerzeit, Laufzeit und Spielzeit. | main.py |
| `spielstaende.py` | 52 | Drei stabile, unabhaengige Speicherslots und ein gesonderter Admin-Teststand. | main.py |
| `gildenrangliste_original.py` | 48 | Historische Gildenwertung als reine, inaktive Datenfunktion. | — (Einstieg oder ungenutzt) |
| `originalkarten_grafik.py` | 36 | Authentische Rasterbilder der 127 Originalkarten, keine Legacy-Symbole. | main.py |
| `public_start.py` | 20 | Windows-Testbuild: normaler Spielerweg, getrennte Laufzeitdaten. | — (Einstieg oder ungenutzt) |
| `ausgabemodus.py` | 11 | Laufzeitmodus der getrennten Windows-Testfassung. | main.py |

## Lesart der Spalte „wird gebraucht von“

Steht dort `—`, ist die Datei entweder der Einstieg (`main.py`) oder sie wird von niemandem mehr importiert (möglicher Rest, siehe `tools/code_mass.py`).
