# Prüfung der Ökonomie-Schritte 3 und 4 (Lager/Transport, Rezepte/Ausbildung)

## 1. Zeitstempel und Stand
- Stand: **2026-10-05 17:59** (geholt mit `date '+%Y-%m-%d %H:%M'`).
- Gegenstand: `src/spieloekonomie.py` (Schritt 3: `verbrauchen`, `transport_start`, `transport_fortschritt`, `station_start`; Schritt 4: `ware_start`, `ausbildung_start`) und `src/werkstatt.py` (`dauer_sekunden`, `einreihen`). Richtschnur: `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (i.F. „Entwurf").
- Nur gelesen. Einziges Schreibziel ist diese Datei. Kein git, keine Projektänderung, kein Test/`run_tests.bat`, kein Spielstart. Der Dauer-Aufruf lief über `python -B -X utf8 -c` (schreibt keinen Bytecode).
- Hinweis zur Zuordnung: Der Auftrag nennt `station_start` für Schritt 3; im Entwurf steht die Funktion aber in Z.870-873 (Abschnitt vor dem Fremdhandel), nicht im Schritt-3-Block Z.417-505. `station_start` fehlt also nicht, gehört aber zu einem späteren Schritt.

## 2. Abweichungstabelle
| # | Entwurf (Zitat) | Code (Datei:Zeile) | Urteil | Begründung |
|---|---|---|---|---|
| 1 | `def verbrauchen(ort, kosten, jetzt)` (Z.422-434) | src/spieloekonomie.py:266-285 | GLEICHWERTIG | Algorithmus 1:1 (anteilige Importentnahme, Journal, `max(0,…)`); nur Docstring ergänzt. |
| 2 | `def transport_start(quelle, ziel, bestand, fracht, jetzt)` (Z.436) | src:288-289 (`…, frachtkanal: str = "vorraete"`) | ZUSAETZLICH | Neuer optionaler Kanal — von Z.504 ausdrücklich gefordert. |
| 3 | `if set(fracht)-set(quelle["vorraete"]):` (Z.447) | src:308 (`frachtkanal == "vorraete" and …`) | GLEICHWERTIG | Für den Warenkanal nötige Verallgemeinerung; im Rohstoffkanal identisch. |
| 4 | `if not bezahlbar(quelle["vorraete"],fracht):` (Z.449) | src:310 (`quelle[frachtkanal]`) | GLEICHWERTIG | Gleiche Wirkung, je Kanal. |
| 5 | `anteil[r] = … / v` / `importiert[r] = max(0,…)` (Z.457-462) | src:319-326 | GLEICHWERTIG | Startbuchung identisch; für Waren wird `anteil=0` und `importiert` bleibt unberührt. |
| 6 | `mission.update({… "ursprung_import":anteil, …})` (Z.466-468) | src:330-333 (+`"frachtkanal"`) | ZUSAETZLICH | Zusätzliches Feld `frachtkanal`; nötig, damit die Rückkehr den Kanal kennt. |
| 7 | (keine Prüfung) | src:296-297 (`frachtkanal not in ("vorraete","waren")`) | ZUSAETZLICH | Härtung: unbekannter Kanal wird sauber abgewiesen (test P9). |
| 8 | Ankunft schreibt `ziel["vorraete"]/["importiert"]` (Z.479/481) | src:352/355 | GLEICHWERTIG | Kanalabhängig; `importiert` nur bei Rohstoffen. |
| 9 | `quelle = neu.get(m["quelle_id"])` oben (Z.474-475) | src:348 (ziel) / 364 (quelle, im Zweig) | GLEICHWERTIG | Nur Verschiebung des Lookups; Ergebnis gleich. |
| 10 | Rückkehr prüft `quelle` nur auf Existenz; Suchlauf Z.492 | src:365-366 (`quelle["besitzer"] != m["besitzer"] → None`) | GLEICHWERTIG | Setzt exakt die Entwurfs-PROSA Z.503 um (der Codeblock Z.489-492 war unvollständig). |
| 11 | (kein Feld) | src:370 (`m["ersatzort"] = …`) | ZUSAETZLICH | Neues Diagnosefeld (test_lokale_lager Z.269/288 verlangt es); kein Fehler. |
| 12 | `m["heimgekehrt_lokal"] = True` INNERHALB `if quelle is not None` (Z.500) | src:380 (immer, außerhalb) | **SCHLECHTER** | Verhaltensänderung — siehe Punkt 3.13/Punkt 5. |
| 13 | `m["besitzer"]` (mit Kommentar „vom Adapter festzuhalten", Z.491) | src:333 (`mission["besitzer"] = quelle["besitzer"]`) | GLEICHWERTIG | Start hält die Besitzerkennung selbst fest. |
| 14 | `def station_start(quelle,ziel,bestand,fracht,jetzt)` (Z.870-873) | src:384-388 | GLEICHWERTIG | Wortgleich (`stationieren_lokal = True`); nur im Entwurf an anderer Stelle. |
| 15 | `warenforderungen`/`pilotrezept` in `src/spieloekonomie.py` (Z.510-534) | tools/warenrezepte_ableiten.py:57/78 | GLEICHWERTIG | Z.588 fordert „nicht erneut generieren"; Ableitung daher als Werkzeug, nicht zur Laufzeit. |
| 16 | `def ware_start(ort, ware, forschung, jetzt, rezepte)` (Z.536, Pflicht) | src:401-402 (`rezepte: dict = None` → `WARENREZEPTE`) | BESSER | Laufzeit lädt die eingefrorene Datei (Z.588), Rezept trotzdem injizierbar. |
| 17 | (keine Prüfung) | src:417-418 (`typ is None → ValueError`) | ZUSAETZLICH | Härtung für Waren ohne Werkstatt. |
| 18 | `schlange["kapazitaet"] = zahl` (Z.550) | src:425 (`werkstatt.kapazitaet(zahl)`) | GLEICHWERTIG | **Kosmetisch:** `kapazitaet(z) = max(0,int(z))` (werkstatt.py:178-184); `zahl>0` geprüft (src:420-421) → gleiche Zahl. Nachgerechnet: 0→0,1→1,2→2,5→5,10→10. |
| 19 | Overwrite `schlange["einheiten"][-1]["dauer"]/["auftraege"][-1]["dauer"] = rezept["dauer"]` (Z.555-556) | src:427 (`einreihen(…, rezepte)`) | BESSER | siehe Punkt 1. |
| 20 | `eintrag = U[name]` (Z.560) | src:441-443 (`U.get` + `ValueError`) | BESSER | KeyError → klare Ablehnung. |
| 21 | `kosten = dict(eintrag["kosten"])` (Z.569) | src:452 (`dict(eintrag.get("kosten") or {})`) | BESSER | Robust gegen fehlendes Feld. |
| 22 | `waren = eintrag.get("waren") or []` (Z.573, danach ungenutzt) | src: (nicht vorhanden) | GLEICHWERTIG | Tote Variable entfernt. |
| 23 | Diff `dauer_sekunden`: bei `basis is None` `warenrezepte.json[ware]["dauer"]` (Z.589) | werkstatt.py:145-166 | GLEICHWERTIG | Wortgleich umgesetzt; `dauer_belegt` bleibt unverändert. |

## 3. Antworten auf die sieben Punkte

**1. Dauer per Overwrite vs. `rezepte` an `einreihen` (Z.555-556 vs. src:427).** Der Entwurf reiht erst mit unbekannter Dauer ein und überschreibt danach zwei Felder. Das echte `ware_start` ruft `werkstatt.einreihen(schlange, ware, 1, 1, rezepte)` (src:427); `einreihen` reicht das an `dauer_sekunden(ware, s, rezepte)` weiter (werkstatt.py:231), das laut Z.589-Diff die eingefrorene `data/warenrezepte.json[ware]["dauer"]` liest. Bei `stufe=1` (einziger Aufrufwert) ist `_stufe_faktor(1) = 1.0` (werkstatt.py:140-142) → **zahlenwertig identisch**. **BESSER**, weil (a) `einheiten` und `auftraege` aus einer Quelle denselben Wert bekommen (kein Vergessen einer Zeile), (b) die Einreih-Meldung korrekt ist statt vorher „Dauer nicht belegt", (c) bei `stufe>1` der dokumentierte Stufenfaktor greift statt still überschrieben zu werden, (d) der von Z.589 geforderte `dauer_sekunden`-Rezeptpfad tatsächlich benutzt wird. Nachgerechnet: `dauer_sekunden('Messer',1,rezepte) = 1200.0 = rezept["dauer"]`.

**2. `schlange["kapazitaet"] = werkstatt.kapazitaet(zahl)` (Z.550 vs. src:425).** `kapazitaet(z) = max(0, int(z))` (werkstatt.py:178-184). In `ware_start` ist `zahl = werkstaetten_bestand(...)[typ] > 0` bereits erzwungen (src:419-421). Damit gilt `kapazitaet(zahl) == zahl` für jeden zulässigen Wert; Nachrechnung (0,1,2,5,10) bestätigt die Gleichheit. **Kosmetisch** — dieselbe Zahl; zusätzlich setzt `neue_warteschlange` das Feld ohnehin schon so (werkstatt.py:198).

**3. Importherkunft nur im Rohstoffkanal (Forderung Z.504).** Z.504: „Kosten-/Importledger für Sieg bleibt nur bei Rohstoffen." Im Code: `anteil[r]=0` für Waren (src:322), `importiert` wird nur bei `frachtkanal == "vorraete"` verändert (src:325-326 beim Start, src:353 bei Ankunft, src:376-378 bei Rückkehr). Der Entwurfsforderung entspricht das **GLEICHWERTIG**.

**4. Rückkehr-Prüfung `quelle['besitzer'] != m['besitzer']` (Entwurf Z.503 vs. src:365-366).** Entwurf Z.503: „Bei Rückkehr zusätzlich quelle["besitzer"] gegen m["besitzer"] prüfen; ein eroberter Ausgangsort gilt wie ein nicht mehr vorhandener Ausgangsort." Der Codeblock des Entwurfs (Z.489-492) prüft nur auf Existenz und widerspricht damit seiner eigenen Prosa; der echte Code prüft den Besitzer (src:365-366) und sucht dann eine Ersatzsiedlung. Urteil **GLEICHWERTIG** zur Forderung Z.503 (und dokumentiert in src:341-343); der Codeblock war unvollständig, der Code ist hier korrekt.

**5. `frachtkanal='waren'` ohne `importiert`-Eintrag (Forderung Z.504).** Z.504: „Für Waren dieselbe Transportfunktion über einen getrennten Bestandskanal erweitern: frachtkanal="waren"". Belegstellen: src:322 `anteil[r] = (0 if (v <= 0 or frachtkanal != "vorraete") else …)` und src:325 `if frachtkanal == "vorraete": neu["importiert"][r] = …`. Beim Warenkanal wird `importiert` also **nicht** angefasst (Ankunft src:353, Rückkehr src:376 gleich geschützt). Bestätigt durch tests/test_warentransport.py Z.154-157 („P3: Warenankunft erzeugt KEINEN Eintrag in ziel['importiert']"). **GLEICHWERTIG** — nur `ursprung_import` am Auftrag ist `{r:0}` (kein `importiert`).

**6. Fehlt etwas aus dem Entwurf?** Keine Funktion fehlt. `station_start` ist vorhanden (src:384-388, = Z.870-873). `warenforderungen`/`pilotrezept` fehlen im Laufzeitmodul bewusst — Z.588 verlangt „nicht erneut generieren"; sie liegen in tools/warenrezepte_ableiten.py (Z.57/78). **Eine nicht erzwungene Vorgabe:** Z.505 „`auftraege.spieldaten_anwenden` darf auf eigentransport niemals angewendet werden" steht nur als Kommentar (src:261-263), ohne Laufzeit-Sperre — relevant erst für die main-Anbindung (Schritt 9/10). Datenprüfung nebenbei: die drei Entwurfs-Prüfzahlen (Z.590) stimmen — Wollumhang 1 wolle/1200 s, Kurzschwert 4 metall/4800 s, Lederrüstung 4 leder/4800 s; Schwert 1200 s.

**7. Altmodus `werkstatt.dauer_sekunden(ware)` unverändert?** Ja. **Aufruf** (`python -B -X utf8 -c`): `dauer_sekunden('Schwert') = 1200.0`, `dauer_sekunden('Messer'/'Bogen'/'Langbogen'/'Wollumhang') = None`, `dauer_belegt('Schwert') = True`, `dauer_belegt('Messer') = False`. Grund: der neue Parameter defaultet auf `None` (werkstatt.py:145-146); `if basis is None and rezepte:` (Z.158) ist mit `None` nie wahr → nur `BELEGTE_DAUER_SEKUNDEN` zählt. **Prüfstellen:** tests/test_werkstatt.py Z.121-136 (Schwert 1200, alle anderen None) und Z.266-269 (3 Messer → „Dauer nicht belegt"), Z.277-278 (nie fertig). Auch die echten Altaufrufe `src/main.py:2476` und `src/spielschicht.py:486` übergeben kein `rezepte` → unverändert. Urteil **GLEICHWERTIG**.

## 4. Was ich NICHT prüfen konnte
- Laufzeit/Bestehen der Tests (nur Lesen erlaubt): nicht ausgeführt.
- Die main-Anbindung (Schritt 9/10): ob ein Auftrag mit `heimgekehrt_lokal=True` samt verbliebener Fracht/Einheiten verworfen wird — das entscheidet, ob Abweichung 12 nur „steckenbleibt" oder Datenverlust ist.
- Ob `auftraege.spieldaten_anwenden` faktisch nie auf einen `eigentransport`-Auftrag angewendet wird (nur Kommentar vorhanden, kein Zwang).
- Balance/Spielbarkeit der abgeleiteten Rezeptdauern und -mengen.
- Vollständigkeit der gesamten Datei; verglichen wurden nur die im Auftrag genannten Funktionen.

## 5. Schwerste gefundene Abweichung
**Abweichung 12 (Z.500 vs. src:380): `m["heimgekehrt_lokal"] = True` wird unbedingt gesetzt.** Der Entwurf setzt den Merker nur, wenn tatsächlich eine (Ausgangs- oder Ersatz-)Siedlung gefunden wurde; findet sich keine, bleibt `heimgekehrt_lokal=False` und der nächste Aufruf versucht die Rückgabe erneut — ein später auftauchender eigener Ort kann die Fracht noch erhalten. Der echte Code schließt den Auftrag sofort (`src:380`, außerhalb des `if quelle is not None`), lässt Fracht und Einheiten auf dem Auftrag (`src:374-376` werden nicht ausgeführt). Damit ist die im Entwurf angelegte spätere Rückgabemöglichkeit **entfallen**; die Fracht/Einheiten bleiben zwar am Auftragsobjekt (kein sofortiger Verlust, durch test_lokale_lager Z.284-289 gepinnt), erreichen aber bei Auftauchen einer Ersatzsiedlung nie ihr Ziel. Es ist die einzige gefundene Abweichung, die beobachtbares Verhalten über die bekannten, absichtlichen Punkte hinaus still ändert; sie ist im Docstring (src:341-343) als gewollt erklärt und mildert damit den Vorwurf, bleibt aber vom Entwurfscodeblock abweichend.
