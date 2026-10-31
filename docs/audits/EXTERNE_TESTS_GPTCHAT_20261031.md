# NEBELSEETAL REMAKE — EXTERNE SPIELTESTS UND HERMES-ÜBERGABE

**Dateiname:** `ExterneTests_GPTCHAT_31.10.26_HermesÜbergabe.md`  
**Prüfdatum:** 31.10.2026  
**Adressat:** Hermes — alleiniger Projekt-Hauptkoordinator  
**Rolle von ChatGPT:** unabhängige, ausschließlich lesende externe Qualitätssicherung / Zuarbeit  
**Projekt:** https://github.com/Decay03101991/Nebelseetal-Remake  
**Verifizierter öffentlicher Release:** `v0.4.0-test.1` / FIX04j vom 28.10.2026; im Release angezeigter Commit `954097a`  
**Release:** https://github.com/Decay03101991/Nebelseetal-Remake/releases/tag/v0.4.0-test.1  
**Öffentliche EXE im Release-ZIP:** `Nebelseetal_Remake_Testversion.exe`; ZIP `Nebelseetal_Remake_Testversion_FIX04j.zip`  
**Öffentlich angegebener EXE-SHA256:** `84c966470580442ac0f3736a676e1c38df66a61b4054d2d10455ee43c7f9022c`  
**Lokales Hauptprojekt laut Übergabekontext:** `D:\Arbeiten\Nebelseetal_Remake`  
**GitHub-Klon laut Übergabekontext:** `D:\Arbeiten\Nebelseetal_Remake_GitHub`

> **UNBEDINGT BEACHTEN — Beweisstatus:** Das öffentliche GitHub-Repository, der Releaseeintrag, einzelne Quelldateien auf `main` und der angegebene Release-Commit wurden lesend geprüft. Der Quelltext wurde über den Webzugriff eingesehen, ein vollständiger Git-Klon aus der Ausführungsumgebung war wegen fehlender Netzwerkauflösung nicht möglich. **Es wurde KEINE Windows-EXE gestartet, KEINE echte Tkinter-Oberfläche bedient und KEIN Projekttest ausgeführt.** Die beschriebenen „Spieler“ sind reproduzierbare, codegeleitete **Simulationen/Testszenarien**, keine tatsächlich von drei Personen durchgespielten Partien. „Quellcodebefund“ bedeutet: auffällige Implementierung im Quelltext nachgewiesen; das konkrete Spielverhalten ist, wo angegeben, noch per Ausführung zu bestätigen. Vorhandene grüne Tests im Repository sind nicht von ChatGPT neu ausgeführte Tests. Dieser ehrliche Status darf in Hermes' Entwicklungsprotokoll nicht verfälscht werden.

---

## 0 — VERBINDLICHER VERWENDUNGSRAHMEN FÜR HERMES

1. **Hermes entscheidet.** Alle Änderungen an Design, UI, Spielregeln, Test-Skills, Adminfunktionen und Roadmap in diesem Dokument sind ausdrücklich **Vorschläge**. Hermes priorisiert sie selbst, gleicht sie mit der Nutzerabsicht und den Originalunterlagen ab und integriert nur geprüfte Lösungen.
2. Erst `docs/HERMES_UEBERGABE_AKTUELL.md`, `docs/ENTWICKLUNGSPROTOKOLL.md`, Roadmap und bestehende Hermes-Skills lesen. Diese Datei ist nur eine **externe Prüfübergabe**, keine konkurrierende aktive Wahrheit.
3. Lokalen HEAD, GitHub-`main`, Release-Commit `954097a` und die wirklich gestartete EXE sauber unterscheiden. SHA-256 der jeweils getesteten EXE und Git-Commit im Testprotokoll erfassen; niemals aufgrund eines Dateinamens Gleichheit annehmen.
4. **Keine Produktiv-Spielstände antasten.** Spieler-Slots 1–3, `.bak`, Admin-Teststand und Archive vorher isoliert sichern. Tests in eigenen temporären Verzeichnissen mit eindeutiger Kennung; niemals Daten automatisch löschen oder reale Passwörter/Token protokollieren.
5. Öffentliche Spieler-EXE bleibt ohne sichtbare Admin-Tools. Admin-Werkzeuge ausschließlich in separater Entwickleredition mit bestehender Freigabe; `src/main.py` bei parallelen Arbeiten von nur einem Integrator ändern lassen.
6. **Nachweis vor Fix:** Fehler mit Zustand vorher/nachher, minimalem Repro, Log, Quellanker, Testergebnis und Sollwert dokumentieren. **Nach Fix:** denselben Repro wiederholen, Nachbarfunktionen und vollständigen Spielablauf erneut prüfen. Ergebnisse im **bestehenden** Entwicklungsprotokoll erfassen, nicht in einer neuen Parallelchronik.
7. Unterscheiden: **Originalspiel belegt** / **bewusste Remake-Regel** / **Pilot- oder Balance-Vorschlag** / **technischer Fehler**. Vorschläge nicht nachträglich als Originalregel ausgeben.

### Legende der Ergebnisbewertung

- **CODE-BESTÄTIGT:** konkret auffälliger Kontrollfluss, Datenwert oder Widerspruch im gelesenen Code.
- **STATISCH ABGEGLICHEN:** Datenzuordnung und betroffene Codestelle passen bei lesender Gegenprüfung; eine Live-Ausführung ist nicht nachgewiesen.
- **REPRO OFFEN:** tatsächlicher Fehlerfall muss im isolierten Spiel/Test noch ausgeführt werden.
- **UX-HYPOTHESE:** wahrscheinlich störend, aber ohne echte Spielperson/GUI-Test nicht belastbar gemessen.
- **VORSCHLAG:** keine vorhandene Vorgabe/kein Bugbeweis; nur eine mögliche Verbesserung.

**Priorität:** P0 = Kernspielablauf/Bestand/Speicherstand gefährdet; P1 = wichtige Funktion/Spielbarkeit/Bedingungsprüfung; P2 = Bedienkomfort und Diagnostik; P3 = spätere Verbesserung.

---

## 1 — KURZURTEIL AUS ENTWICKLER- UND SPIELERSICHT

**Stärken, statisch nachvollziehbar:** historische 10×10-Originalkarten, lokale Siedlungsbestände, differenzierte Produktions- und Forschungsdaten, 17 Originalwaren auf drei Werkstatttypen, 28 Einheiten (davon 14 mit Warenbedarf), lokale Fertigungswarteschlangen, Ausbildung mit Kosten und Wareneinsatz, getrennte Spieler-/Admin-Edition, Start-Hilfe, drei Spielerslots und Entwicklerarchiv. Ein vorhandener Integrationsdurchlauf deckt viele Teilmodule ab.

**Hauptproblem:** Der moderne lokale Ökonomiekern ist noch nicht durchgehend mit einigen älteren **globalen** Missions-, Kampf- und Portalpfaden verbunden. Einige Tests füllen künstlich Bestände auf, sodass sie diese Lücken nicht zeigen. Das trifft den eigentlichen Spielerwunsch direkt: **Waffen und Rüstungen in einem echten Dorf produzieren, damit regulär Truppen ausbilden, sie einsetzen und wieder ins richtige Dorf zurückführen.**

**Prüfentscheidung:** Vor neuen Spielinhalten zuerst P0/P1-Regressionen zur durchgängigen Produktionskette und zum lokalen Truppeneinsatz. Neue Admin-Testfunktionen sollen diese Lücken **beobachten und messen**, nicht durch Gratis-Items verschleiern.

---

## 2 — QUELLCODEBEFUNDE MIT REPRODUKTION UND NUR VORGESCHLAGENEN ABHILFEN

### F-01 [P0] Lokal ausgebildete Truppen werden im normalen Angriffsweg nicht als lokales Heer verwendet

**Beleg / Kontrollfluss:** `src/spieloekonomie.py` in `ausbildung_start` (ca. Z. 417–449) reserviert Material und Ausrüstung vor Ort; `ort_tick` (ca. Z. 459–490) schreibt fertige Einheiten nach `ort["einheiten"]`. `src/main.py` `_truppen_nach_rolle` (ca. Z. 4914–4927) liest hingegen `self.state.units`; `GameState.auftrag_starten` (ca. Z. 1684–1711) prüft und reduziert `self.units`. `_auftrag_angriff` (ca. Z. 5199–5218) führt diese Wege zusammen. **CODE-BESTÄTIGTE Inkonsistenz.**

**Minimalrepro:** Neues Testspiel ohne globale Truppen → Schmiede/Nähstube errichten → alle Forschungen regelkonform erfüllen → Ausrüstung produzieren → eine Einheit ausbilden und fertigstellen → Ortslager A hat `einheiten[Krieger]=1`, global `units[Krieger].count=0` → Angriff/Auftrag aus A versuchen. **Soll:** Einheit ist aus A auswählbar, wird genau einmal reserviert und später entsprechend Verlusten/Rückkehr in A verbucht. **Ist:** aus Code stark zu erwartende Nichtverfügbarkeit; in EXE **REPRO OFFEN**.

**Vorschlag an Hermes:** Ein eindeutiges Missionsmodell `quelle_id` + `einheiten[ort]`, getrennt nach verfügbar/unterwegs/gefährdet/verloren/heimgekehrt; keine parallelen globalen Kampfbestände in neuen Partien. Legacy-Saves gesondert migrieren. Auch Sofortangriff, Kampfsimulator, UI und Missionen über denselben Ortseingang führen oder Sofortangriff ausdrücklich nur als nichtmutierenden Simulator deklarieren.

### F-02 [P0] Bestehender Durchspieltest verdeckt F-01 mit künstlicher Reichsarmee

**Beleg:** `tests/test_durchspiel.py` ca. Z. 195–205 legt `ort.waren[...] = 1` direkt an; ca. Z. 214–221 setzt globale Karren und `gs.units[krieger].count = 8` für den Missionsabschnitt. Der Test prüft danach die globale Abbuchung, nicht die zuvor regulär erzeugte Orts-Einheit. **CODE-BESTÄTIGT.**

**Repro:** Testabschnitt 4–5 ohne manuelles Auffüllen von Waren-/Einheitenfeldern laufen lassen; alternativ exakten Bestandsshapshot vor/nach jedem künstlichen Setup protokollieren. **Soll:** Ein Durchspieltest mit komplettem Material→Ware→Einheit→Kampf-Pfad existiert zusätzlich zu gezielten Fixture-Tests.

**Vorschlag:** Vorhandenen Test nicht zerstören (er erfüllt eine andere Integrationsaufgabe). **Zusätzlichen** `test_produktionskette_ohne_cheats.py` einführen und als Release-Gate markieren.

### F-03 [P0] Portalkosten können wegen globaler Anzeige statt lokalem Lager verschwinden

**Beleg:** `src/main.py` `_portal_wechsel` (ca. Z. 4110–4132) nimmt 5.000 Mana von `self.state.resources["mana"].amount`; `GameState._reichsanzeige_aus_orten` (ca. Z. 937–945) baut denselben Anzeigewert aus den Ortslagern neu auf. Die Portalansicht nennt selbst noch eine abweichende gemeinsame Mana-Kasse (ca. Z. 4163–4165). **CODE-BESTÄTIGTER Widerspruch**, reales Zurücksetzen **REPRO OFFEN**.

**Repro:** Lokales Mana 5.100 → Portalwechsel → Mana unmittelbar, nach Tick, nach Speichern/Laden vergleichen; andere Siedlungen separat prüfen. **Soll:** genau einmal 5.000 aus autorisiertem Ort, keine später wiedergewonnene Zahlung. **Vorschlag:** Quelle der Portalkosten explizit wählen, lokale Transaktion mit idempotentem Journal, klare Aussage über 24h-Sperre (Echtzeit oder Spielzeit — Designentscheidung).

### F-04 [P1] Zwei Waren mit Doppel-Forschungsvoraussetzung werden in der GUI zu früh freigegeben

**Beleg:** `data/items.json` setzt `voraussetzung_struktur: null` bei **Lederrüstung** (`Nähkunst 1 + Rüstungsbau 2`) und **Magischem Paladinharnisch** (`Rüstungsbau 7 + Magiekunde 2`). `GameState.ware_voraussetzung` in `src/main.py`, ca. Z. 1660–1681, behandelt jede nicht-diktartige Struktur als **„keine Voraussetzung belegt“/True**. Die Warenansicht ca. Z. 4295–4302 aktiviert damit den Button. `spieloekonomie.ware_start`, ca. Z. 387–415, prüft dagegen korrekt **alle** Voraussetzungen aus `data/warenrezepte.json` und lehnt ab. **CODE-BESTÄTIGTER UI/Kern-Widerspruch.**

**Repro pro Ware:** Nur **eine** der beiden Forschungsbedingungen erfüllen, zweite Stufe absichtlich 1 zu niedrig; Werkstatt und Rohstoffe vorhanden. **Soll:** klar deaktivierter Button, Anzeige beider Soll/Ist-Stufen; keinerlei Abbuchung. **Ist aus Code:** Button freigegeben, Klick wird mit allgemeinem „Warenvoraussetzung fehlt“ abgelehnt. Unter vollständig erfüllten Bedingungen ist die Produktion vom Kern her vorgesehen; Live-Ausführung offen.

**Vorschlag:** Eine gemeinsame maschinenlesbare `voraussetzungen`-Struktur für Kern **und** UI verwenden (vorzugsweise aus freigegebenem `warenrezepte.json`), nicht `null` als Freigabe interpretieren. Jede Bedingung einzeln in der UI nennen; dieselbe Validierungsfunktion verwenden. `items.json` als historisches Quellenregister erhalten, nicht die historischen Textangaben überschreiben.

### F-05 [P1] Werkstattabriss verändert bestehende Fertigungswarteschlange nicht sofort

**Beleg:** `src/main.py` `_karten_abreissen`, ca. Z. 3641–3670, entfernt Bauten/Stufen, nicht aber örtliche `werkstaetten[typ]`. `spieloekonomie.ort_tick`, ca. Z. 480–484, verarbeitet die alte Schlange weiter. `ware_start` aktualisiert Kapazität nur beim **nächsten Produktionsstart**. **CODE-BESTÄTIGTE fehlende Synchronisation.**

**Repro:** Eine Schmiede, drei Schwerter in Warteschlange → Gebäude vor Fertigstellung abreißen → Zeit bis nach geplantem Produktionsende vorwärts → Lager und Queue ansehen. **Soll:** vorher festgelegte Regel (Abbruch/Pause/zu Ende fertigen) wird konsistent umgesetzt; **nicht** unbemerkt Geisterproduktion. **Vorschlag:** Hermes soll zuerst das Abrissverhalten mit dem Nutzer festlegen. Bei Abbruch: Material-/Restzeitregel dokumentieren; bei Pause: Kapazität null und Aufträge bis Neubau erhalten; bei Fertigstellung: explizit als gewollte Abschlussregel anzeigen. Kapazität zentral bei jeder baulichen Änderung synchronisieren.

### F-06 [P1] Zweite Werkstatt wird bei bestehender Warteschlange möglicherweise verspätet wirksam

**Beleg:** `spieloekonomie.ware_start` setzt `schlange["werkstaetten"]`/`["kapazitaet"]` nur beim Einreihen (ca. Z. 404–412). `ort_tick` schaut bei vorhandenen Warteschlangen nicht erneut auf aktuelle Bauten (ca. Z. 480). **CODE-BESTÄTIGTES Aktualisierungsloch**.

**Repro:** 10 Schwerter mit 1 Schmiede einreihen → zweite Schmiede bauen, **keinen weiteren Artikel einreihen** → Fälligkeitszeiten vergleichen. **Soll laut Original-Handbuch:** parallele Herstellung; 10 Schwerter zu 20 Minuten mit zwei Schmieden insgesamt 100 statt 200 Spielminuten (Regel bezüglich nachträglichem Bau bei laufenden Aufträgen noch entscheiden). **Vorschlag:** Kapazitätswechsel definiert auf Fortschritt anwenden; bereits geleistete Arbeit nicht rückwirkend erfinden; Tests für 1→2→1→0 Werkstätten.

### F-07 [P1] Ausbildungsgebäude-Prüfung der Ansicht ist reichsweit, die Ausbildung selbst lokal

**Beleg:** `src/main.py` `_render_barracks`, ca. Z. 5634–5637, verwendet `gebaeude_wirkung.ausbildungsstaette(self.state.settlements, key)` über **alle Siedlungen**; `_train_unit`, ca. Z. 5718–5740, prüft nur `[ort]`. **CODE-BESTÄTIGTER Unterschied.**

**Repro:** Kriegerakademie in A, in B keine Akademie; B als aktive Siedlung; alle Forschungs- und Warenvoraussetzungen erfüllt. **Soll:** Ausbildungsbutton in B von Anfang an nicht verfügbar und Grund: „Kriegerakademie fehlt in B“. **Vorschlag:** beide Wege auf `aktive_siedlung()` beschränken, Training UI und Regelkern denselben Blockerreport lesen lassen.

### F-08 [P1] Ausbildungsdauer reagiert nicht erkennbar auf Stufe der Ausbildungsstätte

**Beleg:** `data/buildings.json` und `src/main.py` `_render_barracks` versprechen „höhere Stufe = schnellere Ausbildung“. `spieloekonomie.ausbildung_start` (ca. Z. 444–448) setzt für alle Stufen `REGELN["pilot_ausbildung_minuten"] * 60` fest, ohne `stufe` im Dauerausdruck zu verwenden. **CODE-BESTÄTIGTER Regel-/UI-Widerspruch**, sofern nicht an anderer Stelle bewusst übersteuert (im zu prüfenden Kern ist das nicht ersichtlich).

**Repro:** Identisches Einheitenrezept/Startzeit/Stadt mit Akademie Stufe 1 und 5 → Ausbildung starten und Endzeit vergleichen. **Soll:** höhere Stufe schneller; Höhe des Effekts ist zu entscheiden (nicht originalbelegt). **Vorschlag:** zentraler, dokumentierter Ausbildungszeitrechner plus UI-Vorschau; unterschiedliche Stufen und laufende Ausbildung gegenprüfen.

### F-09 [P1] Ortsbezug von Militärmissionen bei mehreren Siedlungen stimmt nicht

**Beleg:** `_auftrag_angriff`, ca. Z. 5215–5217, übergibt stets `self.state.settlements[0]` als Start; `_auftrag_entfernung` (ca. Z. 5187–5198) fällt ebenfalls auf Siedlung 0 zurück. **CODE-BESTÄTIGT.**

**Repro:** Ort A weit vom Bot, Ort B nahe am Bot; B auswählen; Angriff aus B starten. **Soll:** tatsächlicher Startort B einschließlich Distanz, Abbuchung und Rückkehr. **Vorschlag:** `quelle_id` statt Siedlungsname durch alle Auftragsphasen; Bot-Koordinate als expliziten, im Spiel erkennbaren Näherungswert führen, bis echte Bot-Orte vorhanden sind.

### F-10 [P1] Sofortangriff und Reiseangriff haben unterschiedliche Bestands-/Zeitpfade

**Beleg:** `src/main.py` `_angriff_durchfuehren` ca. Z. 4944 ff. und `_auftrag_angriff` ca. Z. 5199 ff. sind zwei Aktionen; beide beziehen Einheiten derzeit aus dem globalen Bestand. **CODE-BESTÄTIGTE Doppelpfade**, Risiko abweichender Regeln/Beutebuchung **REPRO OFFEN**.

**Repro:** Gleicher Startzustand → Sofortangriff oder Mission auf zwei isolierten Kopien auslösen; Kosten, Schutz, Verluste, Beute, Reisezeit und Ergebnis vergleichen. **Vorschlag:** Sofortangriff nur als ausdrücklich markierter *Trockentest* (ohne Mutation) oder beide Aktionen an dieselbe verbindliche Einsatzregel koppeln.

### F-11 [P1] Beute-/Kostentransaktionen in alten globalen Pfaden gegen lokale Bilanz prüfen

**Beleg:** `main.py` `_angriff_durchfuehren` und die alte Reichsbestandsverwaltung existieren neben `spieloekonomie.verbrauchen`, `ort_tick` und `_reichsanzeige_aus_orten`. **Risiko durch gemischte Modelle**; einzelne Resultatpfade vor einer konkreten Fehlerbehauptung mit Live-Snapshot vergleichen.

**Repro:** Erfolgreicher Angriff mit Beute → Lager aller Orte + Reichsanzeige + Kampfbericht vor/nach Tick und Save/Load → Bilanz einschließlich Transportwagen. **Vorschlag:** jede neue Gutschrift mit `ort_id`, `event_id`, Vor-/Nachbestand und Journal versehen; Reichsanzeige ausschließlich ableiten.

### F-12 [P2] Herstellung ist schwer planbar und Blocker sind nicht vor dem Klick vollständig sichtbar

**Beleg:** `src/main.py` `_render_storage` ca. Z. 4276–4306 zeigt die 17 Waren als Buttons pro Werkstatt, aber an diesen Buttons nicht die Rezeptkosten, lokale Rohstoffdeckung, Zielmenge, Produktionszeit oder zwei Forschungsbedingungen. `_ware_herstellen` ca. Z. 4307–4331 erzeugt **genau eine** Ware je Klick. **UX-HYPOTHESE mit Quellgrundlage.**

**Repro:** Anfänger soll 10 Kämpfer ausbilden, ohne Rezeptdaten außerhalb des Spiels. Zeit, Klickanzahl, Fehlversuche und Fragen erfassen. **Vorschläge:** pro Ware Rezeptkarte mit Icon, Werkstatt, Forschung Soll/Ist, Material Soll/Ist, Dauer, Lager, Queue und „für welche Einheiten“; Eingabe 1/5/10/max; Armee-Bedarfsplaner (z. B. 10 Kämpfer → 10 Kurzschwerter + 10 Lederrüstungen). Keine automatische Ressourcenübertragung zwischen Dörfern.

### F-13 [P2] Werkstattstufen-/Tempoidee ist im Kern nicht wirksam, aber derzeit wohl auch nicht baubar

**Beleg:** `werkstatt.py` bietet einen vorgeschlagenen 10%-Stufentempofaktor und `werkstatt_stufe`; `spieloekonomie.ware_start` ruft `werkstatt.einreihen(..., stufe=1, ...)` fest auf. `data/gebaeude_wirkung.json` führt Schmiede/Bogenbauer/Nähstube **nicht** unter ausbaubaren Gebäuden. **Kein nachgewiesener aktueller Spielerfehler**, sondern uneinheitliche Alt-/Zukunftssemantik.

**Vorschlag:** Hermes soll zuerst entscheiden, ob Werkstätten ausschließlich durch **Anzahl parallel** skalieren (historisch belegt) oder zusätzlich individuelle Ausbaustufen erhalten (nicht belegt). Danach toten/irreführenden Tempocode dokumentiert entfernen oder bewusst integrieren; keine stillen Stufenboni.

### F-14 [P2] Dokumentations-/Release-Status teilweise überholt

**Beleg:** `README.md` und Teile von `docs/HERMES_UEBERGABE_AKTUELL.md` sprechen von noch nicht gebauter/veröffentlichter FIX04j-EXE, während GitHub den Release vom 28.10.2026 samt SHA256 listet. **CODE-/DOKUMENTATIONSBEFUND.**

**Vorschlag:** Historie bewahren, nur aktive Statuszusammenfassungen auf das tatsächliche Release und den jeweils verifizierten HEAD setzen. „Unter Windows getestet“ aus dem Release gilt nur für dessen genannte Basisschritte, nicht für sämtliche Waren/Kämpfe.

---

## 3 — SPEZIALAUDIT: ALLE WERKSTÄTTEN, ALLE 17 WAREN, AUSRÜSTUNG FÜR TRUPPEN

### 3.1 Statisch abgeglichene Regeln

- `data/items.json` listet **17 originale Waren** mit Werkstattzuordnung und historischen Forschungsbezeichnungen.
- `data/warenrezepte.json` legt **für alle 17** konkrete lokale Materialkosten, Pilotdauer und strukturierte Forschungsbedingungen fest; ausschließlich die **Schwertdauer 1.200 Sekunden** ist im Modul als im Handbuch belegt markiert. Andere Dauern/Kosten sind überwiegend **VORSCHLAG**, nicht historisch zu belegen.
- `src/werkstatt.py` ordnet 8 Waren der **Schmiede**, 4 dem **Bogenbauer/Bogner** und 5 der **Nähstube** zu.
- `src/spieloekonomie.py::ware_start` prüft für **jedes Rezept** freigegebene Ware, **alle** Forschungsstufen, den richtigen lokalen Werkstatttyp und lokale Rohstoffdeckung, bucht Material und stellt einen Auftrag in die lokale Queue. `ort_tick` verbucht die fertige Ware einmalig in `ort["waren"]`.
- `src/ausruestung.py` und `data/units.json` bilden den Warenbedarf von **14 der 28 Einheiten** ab. `ausbildung_start` verlangt diese Waren **im selben Ort** und verbraucht sie beim Ausbildungsstart.

**Wichtig zur Antwort auf „Kann man wirklich alle herstellen?“:** Die Datenzuordnung aller 17 Waren und der generische Regelpfad sind **statisch vorhanden**. Damit ist die Herstellung im Code grundsätzlich vorgesehen; **nicht bewiesen** ist, dass jede Ware durch echte GUI-Klicks auf einer tatsächlich erreichbaren Siedlung mit real erspielten Forschungsvoraussetzungen herstellbar ist. Diese Lücke ist die hier definierte Hermes-Abnahmeserie. Besonders die zwei doppelten Forschungsvoraussetzungen haben schon einen nachweisbaren Anzeige-/Kernkonflikt.

### 3.2 Vollständige Warenmatrix — Herkunft, Voraussetzungen, Verbrauch

Die Minutenangabe folgt `data/warenrezepte.json` für Werkstatt-/Auftragsstufe 1; **keine real gemessene Spielzeit**. Die Produktkosten sind Pilotrezepte, nicht als Originalwerte behandeln. **Status „Daten OK / Live offen“** bedeutet nur überprüfte Zuordnung, keinen bestandenen Laufzeittest.

| ID | Werkstatt | Ware | Forschung für Herstellung | Material je Stück | Pilotdauer | Benötigt von (laut Originaldaten) | Statusergebnis |
|---|---|---|---|---|---:|---|---|
| W01 | Schmiede | Messer | keine | Metall 1 | 20 min | Gauner | Daten OK / Live offen |
| W02 | Schmiede | Dolch | Waffentechnik 1 | Metall 2 | 40 min | Dieb | Daten OK / Live offen |
| W03 | Schmiede | Kurzschwert | Waffentechnik 3 | Metall 4 | 80 min | Kämpfer, Meisterdieb | Daten OK / Live offen |
| W04 | Schmiede | Schwert | Waffentechnik 5 | Metall 1 | 20 min | Krieger, Ritter, Paladin, Kundschafter, Waldläufer | Daten OK / Live offen |
| W05 | Schmiede | Zweihänder | Waffentechnik 8 | Metall 9 | 180 min | Paladin | Daten OK / Live offen |
| W06 | Schmiede | Kettenhemd | Rüstungsbau 3 | Metall 4 | 80 min | Krieger | Daten OK / Live offen |
| W07 | Schmiede | Plattenrüstung | Rüstungsbau 5 | Metall 6 | 120 min | Ritter | Daten OK / Live offen |
| W08 | Schmiede | Magischer Paladinharnisch | **Rüstungsbau 7 UND Magiekunde 2** | Metall 10 | 200 min | Paladin | **UI-Blocker FEHLER** / Kern vorgesehen / Live offen |
| W09 | Bogenbauer | Kurzbogen | Waffentechnik 2 | Holz 4 | 60 min | Kurzbogenschütze | Daten OK / Live offen |
| W10 | Bogenbauer | Bogen | Waffentechnik 4 | Holz 7 | 100 min | Bogenschütze | Daten OK / Live offen |
| W11 | Bogenbauer | Langbogen | Waffentechnik 6 | Holz 10 | 140 min | Langbogenschütze | Daten OK / Live offen |
| W12 | Bogenbauer | Armbrust | Waffentechnik 8 | Holz 12 | 180 min | Armbrustschütze | Daten OK / Live offen |
| W13 | Nähstube | Wollumhang | keine | Wolle 1 | 20 min | Streuner | Daten OK / Live offen |
| W14 | Nähstube | Lederrüstung | **Nähkunst 1 UND Rüstungsbau 2** | Leder 4 | 80 min | Kämpfer, Armbrustschütze | **UI-Blocker FEHLER** / Kern vorgesehen / Live offen |
| W15 | Nähstube | Diebesumhang | Nähkunst 2 | Wolle 3 | 60 min | Gauner, Dieb, Meisterdieb | Daten OK / Live offen |
| W16 | Nähstube | Fellumhang | Nähkunst 4 | Leder 5 | 100 min | Kundschafter | Daten OK / Live offen |
| W17 | Nähstube | Fellrüstung | Nähkunst 6 | Leder 7 | 140 min | Waldläufer | Daten OK / Live offen |

**Vollständigkeitsprüfungen aus Datenlesung:** 8 + 4 + 5 = 17; alle 17 haben ein Rezept; alle stehen in genau einer der drei Werkstattgruppen; beide mehrteiligen Bedingungen sind strukturiert in `warenrezepte.json`, aber im UI-Abfrageweg `items.json.voraussetzung_struktur = null`. Alle übrigen Einzelbedingungen lassen sich mit dem bestehenden `ware_voraussetzung`-Prüfer anzeigen. Keine „grünen“ praktischen Erzeugungsbelege vorhanden.

### 3.3 Für JEDE Warenzeile W01–W17 zwingend auszuführende Tests

Hermes soll die folgenden **Testvarianten parameterisiert über sämtliche 17 Waren** ausführen, statt nur ein Schwert exemplarisch zu testen:

1. **T-W-01 Zuordnung:** Mit gültiger Stadt/Werkstatt steht Ware ausschließlich in der passenden Werkstattgruppe; Name, Icon und Forschung korrekt. Falscher Werkstatttyp kann sie nicht produzieren.
2. **T-W-02 Ohne Werkstatt:** Forschung und Material vorhanden, aber passende Werkstatt fehlt **im gewählten Ort** → kein Produktionsauftrag, keine Rohstoffabbuchung, verständliche Ortsmeldung.
3. **T-W-03 Forschungsgrenze:** Jede erforderliche Forschungsstufe einzeln **einen Punkt unter Soll** → gesperrt, alle übrigen Voraussetzungen erfüllt. Mit Stufe **exakt Soll** → freigegeben. Für W08 und W14 **beide** Unterbedingungen einzeln und in Kombination testen.
4. **T-W-04 Material knapp:** Ein benötigter Rohstoff mit `Soll−1` → keine Queueänderung und **keine** Teilabbuchung; danach `Soll` → genau ein Auftrag und exakt ein Rezeptverbrauch.
5. **T-W-05 Zeitgrenze:** Vor `Ende−ε` keine fertige Ware; bei `Ende` exakt +1 im richtigen lokalen Warenlager; bei weiteren Ticks keine zweite Gutschrift.
6. **T-W-06 Speichern/Laden:** Nach Einreihen, mitten in der Herstellung und unmittelbar vor Fertigstellung speichern und laden; Auftrag, Zeit, verbrauchter Rohstoff und fertiger Warenbestand müssen erhalten bleiben. Kein kostenloser Neustart, keine Verdopplung.
7. **T-W-07 Doppelort:** Gleiche Ware in A und B; nur A hat Werkstatt/Material. A darf produzieren, B nicht. B kann die Ware nach **echtem** Warentransport verwenden, nicht durch bloßen Reichssaldo.
8. **T-W-08 Ausbildung:** Eine laut Tabelle auf die Ware angewiesene Einheit vorbereiten, Ware tatsächlich vorher produzieren (kein `waren[...] = 1`!), weitere geforderte Waren ebenso produzieren, regulär ausbilden. Beim Ausbildungsstart müssen genau die benötigten Items verschwinden; Einheit erst zum Ende entstehen.
9. **T-W-09 UI:** Bei jedem Test korrektes Button-Enabled, Soll/Ist-Forschung, Rohstoffbedarf, Produktionsstatus und Fehltext erfassen; keine stillen Ausnahmen. Wo der aktuelle UI diese Infos noch nicht anzeigt, als **UX-Nichtbestehen** markieren, nicht als Produktionskernfehler.
10. **T-W-10 Wiederholbarkeit:** Identisches Setup mit festem Seed zweimal; gleicher Endzustand bei gleichen Spielsekunden. Nach jedem Test Snapshot neu aufsetzen, keine Abhängigkeit von Testreihenfolge.

**Pass-Kriterium pro Ware:** alle Pflicht-Varianten erfolgreich; im Testbericht `ware`, `werkstatt`, `forschung_ist/soll`, `rohstoffe_vor/nach`, `auftrags_id`, `start`, `ende`, `warenlager_vor/nach`, `ausbildung`, `save_hash`, `screenshots`, `result` speichern. *PENDING* bleibt, bis Hermes sie wirklich ausgeführt hat.

### 3.4 Besondere Testfälle für Werkstattkapazität, Abriss und Zeit

| ID | Szenario | Erwartung / fachliche Entscheidung |
|---|---|---|
| Q01 | 10 Schwerter, 1 Schmiede | 200 Spielminuten bei Stufe 1 (Originalbeispiel) |
| Q02 | 10 Schwerter, 2 Schmieden von Anfang an | 100 Spielminuten; zwei parallel (Originalbeispiel) |
| Q03 | 10 Schwerter, 3 Schmieden | sinnvoller Parallelbetrieb; numerische Endzeit aus tatsächlicher Queue prüfen |
| Q04 | Zweite Schmiede nach Einreihen, ohne neuen Auftrag | Kapazitätswechsel wird gemäß definierter Regel behandelt; aktuell Verdacht verspäteter Wirkung |
| Q05 | Letzte Schmiede mit laufenden Aufträgen abreißen | keine unerklärte Geisterproduktion; Pause/Abbruch/Fertigstellen muss vorher entschieden sein |
| Q06 | Von 2 Schmieden eine abreißen | verbleibende Produktion und Planungsdaten korrekt; keine vergangenen Fertigstellungen zurücknehmen |
| Q07 | Bogenbauer und Nähstube parallel in verschiedenen Orten | getrennte Warteschlangen, Material und Waren je Ort |
| Q08 | 25 einzelne Aufträge in schneller Folge; große Spielzeitsprünge | keine doppelte Gutschrift; gleiche Endmenge, keine negativen Kosten |
| Q09 | Save/Load mitten in mehreren gleichzeitigen Aufträgen | `gemeldet`, `start`, `ende` und Queuekapazität bleiben konsistent |
| Q10 | Kein geeignetes Feld für Werkstatt | klare Bauablehnung, keine Kostenabbuchung, keine spätere Phantom-Werkstatt |
| Q11 | Alle 17 Waren auf ihrem exakten Forschungsminimum | UI und Kern widersprechen sich **für keine Ware**, insbesondere W08/W14 |
| Q12 | Werkstatt-Feld ausbauen | Nur falls Design Ausbau zulässt; aktuell Werkstätten nicht ausbaubar, keine unbelegte Bonuserwartung erzeugen |
| Q13 | Rohstoffproduktion bricht während Queue ab | Bereits bezahlte Aufträge bleiben gemäß Regel bestehen; keine nachträgliche Fremdabbuchung |
| Q14 | Produktionsauftrag bei noch gesperrter Ware per direktem API-Aufruf | Auch ohne UI muss `ware_start` sicher ablehnen, Zustand unverändert |

### 3.5 Vollständige Truppen-/Ausrüstungskette: 14 Einheiten mit Warenbedarf

Die 14 ausrüstungsbedürftigen Einheitentypen sind aus `data/units.json` und dem Rückverweis `data/items.json.benoetigt_von` abzuleiten; **Hermes muss die folgende Matrix programmatisch aus den Daten generieren**, nicht als zweite manuell gepflegte Wahrheit verwenden:

| Einheit | Benötigte Waren aus Quelldaten | Ausbildungsstätte | Externer Abnahmetest |
|---|---|---|---|
| Kämpfer | Kurzschwert + Lederrüstung | Kriegerakademie | beide Waren regulär hergestellt; bei Ausbildung beide −1 |
| Krieger | Schwert + Kettenhemd | Kriegerakademie | beide Waren regulär hergestellt; lokale Einheit +1 am Ende |
| Ritter | Schwert + Plattenrüstung | Kriegerakademie | 2 Produktionsketten + Ausbaustufen prüfen |
| Paladin | Zweihänder + Schwert + Magischer Paladinharnisch | Kriegerakademie | 3 Waren; Doppel-Forschung zwingend; sehr späte Spielphase |
| Kurzbogenschütze | Kurzbogen | Kriegerakademie | Bogner-Ware, Akademie am gleichen Ort |
| Bogenschütze | Bogen | Kriegerakademie | Transport zwischen Bogner/Trainingsdorf optional |
| Langbogenschütze | Langbogen | Kriegerakademie | höhere Forschung + Queue |
| Armbrustschütze | Armbrust + Lederrüstung | Kriegerakademie | Bogenbauer + Nähstube, Doppel-Forschung |
| Streuner | Wollumhang | Diebesgilde | niedrigste Textilware, Ausbildungsgebäude prüfen |
| Gauner | Messer + Diebesumhang | Diebesgilde | Schmiede + Nähstube, 2 Waren |
| Dieb | Dolch + Diebesumhang | Diebesgilde | gemischte Produktionskette |
| Meisterdieb | Kurzschwert + Diebesumhang | Diebesgilde | gemischte Produktionskette |
| Kundschafter | Schwert + Fellumhang | Diebesgilde | Schmiede + Nähstube; Ortsheer/Mission |
| Waldläufer | Schwert + Fellrüstung | Diebesgilde | hochwertige Lederware und Ortsheer/Mission |

**Hinweis:** Die gezeigten Warennamen sind als Ausgangsmatrix statisch geprüft, die tatsächlich gültigen Kombinationen und alle 28 Ausbildungsstätten bei Testausführung **direkt aus `units.json`** ablesen. Die 14 **ohne** Warenbedarf nicht vergessen: Sie benötigen trotzdem ihre jeweilige Ausbildungsstätte, Forschung, Rohstoffe und Siedler; keine künstliche Warenpflicht hinzufügen. Stellmacher-Einheiten (Karren/Belagerung) gesondert durchspielen, weil sie für den anschließenden Einsatz der fertigen Armee wichtig sind.

**Kompletter harter Integrationsfall IK-01 (ohne Abkürzung):** Holz, Metall, Leder, Nahrung, Gold/Pferde etc. auf passenden Feldern erwirtschaften; nötige Forschungsstufen über echte Bibliotheksaufträge erreichen; passende Werkstätten regelkonform bauen; zwei Teile für 1 Krieger tatsächlich herstellen; beide Wareneingänge nach Fertigstellung prüfen; Kriegerakademie bauen; Krieger über UI ausbilden; exakt 1 Schwert und 1 Kettenhemd verbrauchen; bis Ausbildung fertigstellen; Einheit in Ortslager A sehen; aus A Auftrag mit Reisefrist starten; Zielkampf und Bericht prüfen; verbleibende Einheit korrekt zurück nach A; Save/Load an mindestens drei Zwischenstellen. **Jeder cheatartige direkte Eintrag in `ort.waren`/`state.units` macht diesen Test ungültig.** Ein gesonderter Fixture-Test mit künstlichen Beständen ist weiterhin erlaubt, aber muss so benannt sein.

---

## 4 — DREI UNABHÄNGIGE SPIELER-PERSONAS UND EIN ENTWICKLERTEST

### PERSONA S1 — Anfänger ohne Wiki (Onboarding/Verständlichkeit)

**Rahmen:** öffentliche FIX04j-EXE, neues Profil, keine Cheats/Testscripts, zunächst nur 1 Stadt. Testperson klickt nicht optimal und ignoriert optionalen Hilfetext.

**Szenario:** 1) Profil/Start; 2) ohne Siedlung bauen versuchen; 3) auf falschen Geländefeldern Holzfäller/Steinmetz/Farm setzen, dann korrekt; 4) tatsächliche Stundenproduktion mit Tempo ×1 und ×180 sehen; 5) Einstiegshilfe bis **real laufender** Holz-, Stein- und Nahrungsproduktion; 6) erste Schmiede/Nähstube bauen wollen und Baukunst-Blocker verstehen; 7) erste Ware (Messer, Wollumhang) produzieren und im Ortslager wiederfinden; 8) Slots 1/2 nutzen, Neustart/Load, Archivverhalten prüfen.

**Zu beobachten:** Zeit bis erste laufende Rohstoffketten; Fehlermeldungen (exakter Grund + welcher Ort), verständliche Differenzierung von Rohstoff/Ware/Einheit; Sind die Lagerwerte sichtbar? Kann eine neue Person erkennen, wie ein Messer entsteht und wer es verbraucht? Ist die Warenoberfläche bei 8 Schmiede-Buttons lesbar? Keine unklare „freigeschaltet, aber nicht herstellbar“-Situation.

**Verdacht:** Forschungs-/Materialkosten in der Warenoberfläche nicht sichtbar; nach Doppelvoraussetzung irreführender Button. **Vorschlag:** Ein leicht verständlicher, optionaler „Von Rohstoff zu erster Einheit“-Leitfaden mit anklickbaren Schritten. Keine Zwangsautomatisierung nach Pflicht-Tutorial.

### PERSONA S2 — Wirtschaftsoptimierer / Produktionsketten-Spieler

**Rahmen:** 3+ Dörfer mit verschiedenen Originalkarten; sehr genaue Lagerbuchhaltung; Spieltempo ×600; keine künstliche Itemvergabe.

**Szenario:** Produktionsdörfer für Holz/Metall/Leder/Wolle → Werkstätten in spezialisierter Stadt → reale Warenlieferung zu Kriegerakademie in anderer Stadt → Queue über 1/2/3 Werkstätten → Abriss/Neuaufbau → Save/Load in Produktion und Lieferung → zehn gleiche Einheiten durch mehrere Produktionsaufträge und Bedarfsrechnung.

**Zu beobachten:** Kein überörtliches Gratislager; Summenbilanz `Reich = Summe Ortslager`; verlorene/verdoppelte Transportladung; Engpässe in Material, Arbeitern und Forschung; Produktionsdurchsatz, Warteschlangenzeiten, Lagerkapazität (falls vorgesehen); Baufelder/Originalkarten gegen tatsächliche Geländeregeln. **Verdacht:** Q04/Q05, UI-Einzelklicks, schlechte Bedarfsplanung. **Vorschlag:** Bedarfsermittlung mit Einkaufs-/Transport-Checkliste und optionalen Mengenaufträgen.

### PERSONA S3 — Militärspieler / Herausforderer

**Rahmen:** Jede der drei Ausbildungsstätten; mindestens Kämpfer, Krieger, Fernkampf, Kundschafter, Karren; Gegner und Götterschutz; mehrere Dörfer.

**Szenario:** Forschungsbaum erreichen → alle nötigen Waffen/Rüstungen im selben Dorf produzieren → mehrere Einheiten ausbilden → Missionsort B statt A → Kampf, Beute, Schäden, Rückkehr → erneut ausbilden → Schutzende → Save/Load während An-/Rückreise. Zweimal identische Ausgangszustände: sofortiger Angriff vs. Reiseauftrag.

**Zu beobachten:** Alle 14 Warenbedarfs-Einheiten tatsächlich ausbildbar; keine kostenlosen Einheiten; kein Wareneinsatz ohne Abschreibung; keinerlei Überschneidung globaler und lokaler Armeen; korrekte Reisezeit, Schutz und Kriegsberichte. **Vermutlicher Blocker:** F-01/F-09. **Vorschlag:** Einheitlich lokalisierte Missionen, expliziter Quellort und eindeutige Einsatzhistorie.

### PERSONA D1 — Admin-/Entwicklertester

**Rahmen:** getrennte Entwickleredition, isolierter Admin-Teststand mit 6 Siedlungen, voller Zugriff nur nach gesonderter Autorisierung, niemals auf normalem Spielerprofil.

**Szenario:** 1) Testdaten statt normalem Save laden; 2) Szenario „W08 nur Rüstungsbau“ und „W14 nur Nähkunst“ per kontrollierten Setup herstellen; 3) negativ/positiv mit Snapshot und Assertions vergleichen; 4) alle 17 Rezepte automatisiert testen; 5) Werkstätten während Queue entfernen; 6) Ausbildungsstätte in Nachbarort statt Aktivort; 7) lokales Heer auf Mission; 8) 24h-/7-Tage-/mehrere Spielwochen-Simulation; 9) Save/Load/Wiederherstellung; 10) Wechsel zwischen Entwickler-/Public-Build testen.

**Zu beobachten:** Gleiches Ergebnis über GUI und Kern; alle mutierenden Aktionen nachvollziehbar; Testdaten nicht in Spielerstand übertragbar; „Pass“ nur mit tatsächlichem Assertion-Ergebnis. **Vorschlag:** Admin-Testzentrale wie in Abschnitt 5.

---

## 5 — VORSCHLAG: NÜTZLICHE ADMIN-IN-GAME-TESTZENTRALE (HERMES ENTSCHEIDET)

### 5.1 Bereits vorhanden — nicht neu erfinden

`src/admin_oberflaeche.py` und `src/admin_werkzeuge.py` bieten: Auswahl einer Siedlung, kontrollierte lokale Rohstoff-/Waren-/Einheitenvergabe, Kartentausch, Weltposition und Spielerhilfe-Anzeigemodus. Mutation ist an Adminfreigabe/Testmodus gebunden, Speichern grundsätzlich manuell. `src/admin_teststand.py` erzeugt einen Entwicklungsstand mit sechs Siedlungen. **Diese Trennung unbedingt erhalten.**

### 5.2 Neue Register/Funktionen als Vorschläge

**A. Produktionsprüfer (P0/P1):** Dropdown `Werkstatt`, `Ware`, `Siedlung`, `Forschungsfall` (alles erfüllt / eine Bedingung fehlt / Material fehlt / Werkstatt fehlt), `Anzahl`, `nur prüfen / tatsächlich buchen`. Standard: **Dry Run** in einer Deep-Copy; dann Kosten-/Queue-/Lagerdifferenz anzeigen. Knopf „Alle 17 Rezepte in Testkopie prüfen“ mit Ergebnis-Tabelle, zeitgestempeltem Log und Export als JSON/Markdown. Forschung und Kosten immer aus den realen Datendateien lesen.

**B. Produktionsketten-Simulator (P0):** „Erzeuge 1 Kämpfer/Krieger/Ritter/Paladin ohne Items zu schenken“ und wahlweise „10x Einheit“. Zeigt Kette: fehlende Rohstoffe, notwendige Forschungsstufen, Gebäude, geplante Waren, erwartete Zeit, Ortslagerbedarf. Optional Labor-Fast-Forward nur **über echte Regelkern-Events**; nie `waren += X` als vermeintlicher Produktionserfolg. Hard-Test meldet FAIL, wenn Kette bis fertige Orts-Einheit nicht geschlossen ist.

**C. Queue-/Gebäude-Fehlerlabor (P1):** Testfälle 1→2 Schmieden, 2→1, Abriss letzte Schmiede, Lager zu knapp, Save/Load in Fertigung, exaktes Zeitfenster, 1000 Schnell-Ticks. Im Bericht Vor-/Nachzustand und Queuekapazität/Restzeit. Keine destructive Testoperation auf normalem Save.

**D. Forschungs-Voraussetzungsprüfer (P1):** Alle Forschungszustände pro Ware erzeugen; Spezialfälle W08/W14 einzeln; UI-Erlaubnis und Kern-Erlaubnis maschinell gegeneinander vergleichen. Zeigt die **konkrete** fehlende Bedingung statt „keine Voraussetzung belegt“.

**E. Armeelabor (P0):** Vergleich je Ort: `im Lager`, `in Ausbildung`, `auf Mission`, `verloren`, `zurückgekehrt`; Auftrag explizit mit `quelle_id`; Reisesimulation gegen Übungsbot mit fixem Seed und einstellbarem Wall, Schutz und Ressourcen; Bilanz aller Einheiten und Beute. Wahlweise **reiner Kampfsimulator** ohne Speicherstandmutation. Keine globalen gratis aufgestockten Einheiten als Standardfall.

**F. Zeitreisen mit kontrollierter Spielzeit (P1):** Buttons +1 Spielminute/+1 Stunde/+1 Tag/+7 Tage, „bis nächstes Ereignis“, „bis vor/nach Fertigstellung“. Immer die **gleiche produktive Tick-Pipeline** wie Spiel verwenden; Event-IDs und Einmalbuchungen vergleichen. Echtzeitsperren (z. B. Portal) gesondert testen — nicht durch Manipulation der Rechneruhr.

**G. Save-/Snapshot-Vergleich (P0):** Vorher/Nachher-Diff für jeden Ort: Rohstoffe, Waren, Einheiten, Queue, Forschung, Bevölkerung, Missionen, Berichte. „Snapshot → Aktion → Tick → Save → Reload → Diff“ als einen reproduzierbaren Test mit logischem Test-Seed. Fehlerbericht ohne Kennwörter oder private Profilinformationen.

**H. Karten-/Gebäudeprüfer (P1/P2):** Alle 127 Originalkarten auf 10×10-Raster, Baufeldregeln und potenzielle Start-/Produktions-Softlocks prüfen; 25 zuvor als unbestätigt dokumentierte Feldtypzuweisungen separat manuell visuell vergleichen. Gebiet, Originalbild und wirkliche Bauoption gemeinsam anzeigen.

**I. UX-/Klickpfadprotokoll (P2):** Nur im Teststand, bewusst aktivierbar: Menünavigation, Klickzahl bis „Krieger fertig“, deaktivierte Buttons mit Grund, UI-Callback-Exceptions, Fenstermaße/DPI. Keine Spielerdaten-/Passwortaufzeichnung. Screenshots nur bei ausdrücklicher Testaktion.

**J. Release-Selbstcheck (P1):** Edition, Commit, Build-Datum, Speicherpfad, Adminzugang in Public blockiert, 3 Slots funktionieren, SHA256, vorhandene Originalbilder, externe Ausgabeordner ohne Secrets. Kein Release auf Basis des Admin-Teststands oder ungesicherten historischen Daten.

### 5.3 Sicherheits- und Architekturregel für die vorgeschlagene Testzentrale

- GUI (`admin_oberflaeche`) nur Darstellung; Testregeln und Szenario-Erstellung in separaten Modulen unter `src/` bzw. `tests/`. Bestehende `admin_werkzeuge._pruefe_admin`-Freigabe für **jede** Mutation weiterverwenden.
- Standardmäßig **read-only Dry Run** mit Kopie der aktiven Teststadt. Jede Zustandsänderung explizit im UI bestätigen; nach Durchführung „nicht gespeichert“ sichtbar halten. Admin-Snapshots nur im Entwickler-Testordner.
- **Zwei Modi strikt trennen:** `Fixture-Modus` darf Startbedingungen gezielt setzen (mit Auditlog und Kennzeichnung „künstlich“); `Echte-Spielregel-Modus` darf Ergebnisse nur über echte Herstellungs-, Transport-, Ausbildungs- und Kampfpfade erzielen.
- Funktionale Tests sollen **ohne Adminoberfläche ausführbar** sein (CLI/CI), die Admin-UI ruft dieselben Prüfer nur auf. Kein Kopieren von Regeln in Testcode.
- Ergebnis exportieren als `run_id`, `commit`, `build`, `edition`, `test_id`, `seed`, `setup`, `actions`, `assertions`, `before`, `after`, `PASS|FAIL|BLOCKED`, `exception`, `duration`, `artifacts`.

---

## 6 — HERMES SOLL AUS DIESER PRÜFUNG LERNEN: SKILL- UND TESTMETHODE-VORSCHLÄGE

**Das ist ein ausdrücklicher Nutzerwunsch.** Hermes soll **bestehende Skills zuerst lesen**, bewährte Regeln einarbeiten und **keine doppelten Skill-Dateien oder parallel geführten Prüfanweisungen** erzeugen. Anpassungen nur nach eigener Beurteilung und mit protokolliertem Grund. Die folgenden Maßnahmen sind konkrete lernbare Regeln:

### SK-01 — „End-to-End statt Fixture-Erfolg“ (höchste Priorität)

Jedes kritische Feature bekommt zwei Ebenen:
1. **Isolierter Komponententest** mit ausdrücklich künstlichen Fixtures; gut für Regeln und Fehlerzustände.
2. **Spieler-E2E** ohne direkte Bestandsvergabe: echte Rohstoffproduktion → Forschung → Werkstatt → Ware → Ausbildung → Einsatz → Rückkehr → Speichern/Laden.

**Anti-Pattern erkannt:** `tests/test_durchspiel.py` erzeugt Ausrüstung und Armee direkt; Erfolg darf nicht als Beweis der Produktionskette gemeldet werden. **Skill-Regel:** „Wenn ein Test einen Zwischenzustand selbst schreibt, gilt der Test nicht als Nachweis für die Entstehung dieses Zustands.“

### SK-02 — „Eine Quelle je Spielzustand / UI-Kern-Vertrag“

Für jedes System genau eine führende Bestands-/Regelquelle dokumentieren: `ort.vorraete`, `ort.waren`, `ort.einheiten` statt globale Schattenkassen. Jede Bedingung **einmal als Kern-Validator**, UI fragt denselben Validator nach bool **und exaktem Fehlergrund**. Regression testet beide; insbesondere **zusammengesetzte** Bedingungen (AND, nicht OR und nicht `null=>True`).

### SK-03 — „Datengetriebene Vollständigkeitsmatrix“

Wenn es 17 Waren gibt, automatisiert **alle 17** aus der Datendatei iterieren. Bei 28 Einheiten **alle 28**. Keine Testlisten von Hand kopieren; Matrix bei Datenänderung neu erzeugen und auf unbekannte/fehlende Referenzen/Icons/Rezeptkosten/Nullwerte prüfen. Neue Ware ohne Testfall darf ein Release-Gate nicht still passieren.

### SK-04 — „Grenzfallpflicht zu jeder Prüfung“

Nicht nur Standardfall testen, sondern **−1 / exakt 0 / exakt Soll / +1** für Forschung, Material, Zeit und Einheiten; gebrochene Kombinationen einzeln. Negative Transaktionen atomar (keine Teilerstattung/Teilabbuchung) und mit unverändertem Vorher-Nachher-Snapshot nachweisen.

### SK-05 — „Zeit- und Queue-Systeme als Zustandsautomaten testen“

Für Aufträge `angelegt → wartend → läuft → fertig/gemeldet` und für Missionen `geplant → unterwegs → angekommen → rückkehrend → beendet` jeden Übergang, Neustart, Zeitvor-/rückwärts-Ausreißer, Wiederholungs-Tick und Gebäudekapazitätswechsel prüfen. Einmal-Buchung durch Event-/Auftrags-ID nachweisen. Keine `time.sleep`-Langtests; kontrollierte Spieluhr/Seed.

### SK-06 — „Bestandsbilanz vor/nach jeder Mutation“

Für lokale Ressourcen und Waren die Gleichung testen: `Bestand_nach = Bestand_vor + echte Produktion + echte Lieferung/Beute − Bau-/Forschungs-/Herstellungskosten − echter Einsatz/Versand`. Für Einheiten Ausbildungszugang, Missionsabgang, Kampfverlust und Rückkehr getrennt zählen. Globale Anzeigewerte dürfen nur abgeleitet sein.

### SK-07 — „Drei Gesichter einer Funktion prüfen“

1. **Regelkern** macht das Richtige. 2. **UI** zeigt vorher die Wahrheit und bedient es korrekt. 3. **Speicherstand** bewahrt exakt dasselbe Ergebnis. „Kern kann herstellen“ ist kein Beweis „Spieler kann herstellen“; „Button aktiv“ ist kein Beweis „Kern akzeptiert“.

### SK-08 — „Schweregrad anhand der Spielerkette“

Priorisieren, was die Kette „Rohstoff → Item → Truppe → Einsatz“ bricht, über kosmetischen Ideen. Jede neue Funktion mindestens einem Spielerziel und einer Regression zuordnen. Designverbesserung und bestätigten Bug nie in einen gemeinsamen unbegründeten Patch mischen.

### SK-09 — „Testrealität und Quellenklassifikation“

Jeder Bericht benötigt `GELESEN`, `STATISCH VERIFIZIERT`, `LOKAL AUSGEFÜHRT`, `WINDOWS-GUI VERIFIZIERT`, `PUBLIC-BUILD VERIFIZIERT`, `BLOCKED`, `VORSCHLAG`. Screenshots/Logs/Testexitcodes/Commit und Datum nur angeben, wenn real vorhanden. Originalbelege getrennt von Pilotregeln.

### SK-10 — „Reproduzierbare Fehlerfälle als Dauertests aufnehmen“

Nach Bestätigung von F-01 bis F-13 jede gefixte Stelle mit minimalem red→green-Test absichern; dieselbe Regression zusätzlich im vollständigen Durchspiel ausführen. Testfälle niemals löschen, nur weil sie nach Refactoring unbequem werden; bei Regeländerung Entscheidung und Testabsicht dokumentieren.

### SK-11 — „Admin-Prüfwerkzeuge dürfen Bugs nicht verdecken“

Admin-Tester müssen deutlich zwischen **gezielter Fixture-Vergabe** und **regelkonformer Aktion** unterscheiden; Testreport zeigt, wenn künstliche Waren/Truppen im Startsetup stecken. Automatisierte Abnahme darf bei kunstmäßig eingesetzten Endgegenständen nicht „E2E PASS“ melden.

### SK-12 — „Sicheres lokales Testen + Release-Belegkette“

Isolierte Spielstandsordner pro Test; keine echte `.env`, Nutzerpasswörter, privaten Archive, unbefugte Uploads. Ausführung von Testskripten/Builds gegen exakten Git-Commit, Hash und Edition dokumentieren; Public-EXE mit eigenem Testprofil und ohne Admin-UI prüfen. Keine Hauptprojekt- oder Git-Mutation durch externe Prüfer.

**Vorgeschlagene Skill-Aktion für Hermes:** Nach Sichtung der vorhandenen Skillliste in **passende bereits bestehende Test-, Coding-, UI-, Release- und Sicherheits-Skills** einarbeiten. Nur wenn keine passende Skill-Kategorie existiert, **eine** neue konsolidierte Fähigkeit `spielketten_regression` erwägen. Im Entwicklungsprotokoll festhalten: welche Regel ergänzt wurde, wo, warum, mit welchem Gegenbeispiel (z. B. F-02), wie sie bei künftigen Änderungen automatisch greift. Keine neue autoritative Übergabe erzeugen.

---

## 7 — EMPFOHLENE NEUE TESTDATEIEN (NICHT VON CHATGPT ANGELEGT; HERMES ENTSCHEIDET)

| Vorgeschlagener Pfad | Fokus / wichtige Assertion |
|---|---|
| `tests/test_waren_alle_rezepte.py` | Iteriert alle Waren aus `items.json`/`warenrezepte.json`, alle Forschungs- und Materialgrenzen; keine Fehlbuchung |
| `tests/test_waren_ui_kern_vertrag.py` | Für 17 Waren: `ware_voraussetzung` vs. `ware_start` unter exakt demselben Forschungszustand; W08/W14 Sonderfälle |
| `tests/test_werkstatt_lifecycle.py` | Kapazität bei Bau/Abriss/2. Werkstatt/Save-Load; einmalige Warenbuchung |
| `tests/test_truppenkette_ohne_cheats.py` | Rohstoff→Forschung→alle erforderlichen Waren→Ausbildung→lokale Truppe→Mission→Rückkehr |
| `tests/test_ausbildung_ortsbezug.py` | Akademie/Gilde/Stellmacher nur in A, aktive Stadt B; Stufen-Tempo, Soll/Ist, Kosten |
| `tests/test_auftraege_lokale_einheiten.py` | Mission startet mit genau im Quellort existierenden Truppen; keine globale Geisterarmee |
| `tests/test_portal_lokales_mana.py` | Mana genau einmal abbuchen, Tick/Save/Load, mehrere Siedlungen |
| `tests/test_economy_conservation.py` | Für Szenario/Seed: Summe der Konten, Produktivität, Verbrauch, keine negativen Werte, idempotente Events |
| `tests/test_admin_szenarien.py` | Admin-Freigabe, Dry-Run-Isolation, Teststand statt Spielerstand, Exportreports |
| `tests/test_release_public_regression.py` | Öffentliche Edition ohne Adminbedienung, drei Slots, Start/Save/Load, Buildidentität |

**Hinweis für Hermes:** Erst vorhandene `tests/test_werkstatt.py`, `tests/test_ausruestung.py`, `tests/test_spieloekonomie.py`, `tests/test_durchspiel.py` auf bereits abgedeckte Fälle prüfen. Obige Namen sind **Architekturvorschläge**, nicht die Aufforderung, blind zehn redundante Dateien anzulegen. Wiederverwendung/Erweiterung ist vorzuziehen. Tests aus Repository ohne Manipulation reproduzierbar per `python -X utf8 tests/<datei>.py`; tatsächliche Befehle an die lokale Projekt-Testkonvention und Python-Umgebung anpassen.

### Pseudocode für datengetriebenen Warentest (nur Entwurf, nicht ausführbarer Drop-in-Patch)

```python
for ware, original in items["waren"].items():
    rezept = rezepte[ware]
    werkstatt_typ = werkstatt.werkstatt_fuer(ware)
    assert werkstatt_typ in {"schmiede", "bogenbauer", "naehstube"}
    for fehlende_bedingung in [None, *rezept["voraussetzungen"]]:
        ort = neues_isoliertes_ort_fixture(werkstatt_typ)
        forschung = exakt_erforderliche_stufen(rezept)
        if fehlende_bedingung:
            forschung[fehlende_bedingung] -= 1
        vor = snapshot(ort)
        if fehlende_bedingung:
            assert_raises(ValueError, spieloekonomie.ware_start,
                          ort, ware, forschung, jetzt=0)
            assert snapshot(ort) == vor
        else:
            neu = spieloekonomie.ware_start(ort, ware, forschung, jetzt=0)
            assert_rohstoff_differenz(vor, neu, rezept["kosten"])
            ende = eindeutiges_ende_der_angelegten_ware(neu, ware)
            neu2 = spieloekonomie.ort_tick(neu, 0, ende, forschung)
            assert neu2["waren"].get(ware, 0) == vor["waren"].get(ware, 0) + 1
            assert_keine_zweite_gutschrift(neu2, ware, ende)  # Platzhalter: API korrekt anbinden
```

Der Pseudocode erläutert den **Testplan**, ist absichtlich kein unmittelbar lauffertiger Patch; Hilfsfunktionen existieren noch nicht. Der letzte Platzhalter enthält bewusst keine zugesicherte Funktionssignatur und ist bei Umsetzung anzupassen. Hermes soll kein Pseudocode-Snippet in Produktivcode kopieren, sondern auf Basis realer APIs eine saubere ausführbare Testdatei schreiben.

---

## 8 — GEORDNETER ABNAHMEPLAN / DEFINITION OF DONE

### Phase A — Ausgangszustand, keine Änderungen

- [ ] HEAD, Commit, Edition, Build-Hash, aktive Übergabe/Roadmap, vorhandene Tests und Skills protokollieren.
- [ ] Testdaten vollständig isolieren; originalen Nutzer- und Admin-Save unangetastet lassen.
- [ ] Bestehende Werkstatt-, Ausrüstungs-, Durchspiel- und Speichertests ausführen; tatsächliche PASS/FAIL/Blocker mit Exitcodes festhalten.
- [ ] In der realen Windows-Entwickleredition die drei Personen-Szenarien S1/S2/S3 wenigstens mit nachvollziehbarem Beobachtungsprotokoll gegenprüfen.

### Phase B — P0 zuerst

- [ ] F-01/F-02: echte Herstellung → Ausbildung → Mission aus lokalem Ort ohne künstliche Einheiten **läuft durch**.
- [ ] F-03: Portal-Mana vollständig lokal belastet, Tick/Save/Load konsistent.
- [ ] Missions-, Waren- und Rohstoffbilanz ohne Verdopplung; keine globalen Schattenbestände in neuem Modus.

### Phase C — alle 17 Waren und alle relevanten Gebäude

- [ ] W01–W17 positive und negative Fälle sowie W08/W14 kombinierte Bedingungen tatsächlich ausgeführt.
- [ ] Schmiede, Bogenbauer, Nähstube richtig auf geeigneten Feldern baubar; alle ihre Waren ausschließlich dort.
- [ ] Baukunst-Bedingung, Forschungsschwellen, Materialkosten, Werkstattanzahl, Queue und Speichern/Laden geprüft.
- [ ] Für alle 14 Einheiten mit Warenbedarf die vollständige Item-Verwendung und richtige Ausbildungsstätte geprüft.
- [ ] Für die weiteren 14 Einheiten Kosten/Stätte/Forschung ohne erfundene Warenpflicht geprüft.
- [ ] F-05/F-06 Abriss/Kapazitätswechsel fachlich entschieden, umgesetzt und regressiongetestet.
- [ ] F-07/F-08 lokale Ausbildungsstätten und Ausbau-/Tempoangaben konsistent.
- [ ] GUI: keine freigegebene, im Kern wegen Forschung abgewiesene Ware; Button/Fehltext nennt genauen Grund.

### Phase D — Admin-Prüfwerkzeuge / Skills / Release

- [ ] Sinnvolle Admin-Prüfer zunächst als **separate** Regel-/Testmodule, danach optional in Entwickleroberfläche integrieren.
- [ ] Vorhandene Hermes-Skills auf SK-01 bis SK-12 abgleichen und relevante dauerhafte Prüfregeln ergänzen (keine Dopplungen).
- [ ] Release-Selbstcheck im Public-Build, drei Slots und Admin-Abwesenheit im UI; Windows-DPI und tatsächliches Speichern/Neuladen.
- [ ] Abweichungen gegen Originalunterlagen, bewusst vorgeschlagene Regeln und künftiges Spielziel eindeutig markieren.
- [ ] Für alle Änderungen ein Eintrag im vorhandenen `docs/ENTWICKLUNGSPROTOKOLL.md`: Ursache, Entscheidung, Dateien, Testbefehle, echte Ergebnisse, betroffene Saves, Git-Commit, offener Rest.

**Definition of Done für diese externe Übergabe:** Hermes hat jeden Befund **bestätigt, widerlegt oder ausdrücklich vertagt**, inklusive Testbeleg; die 17-Waren-Matrix und die 14 Ausrüstungs-Einheiten wurden mit echten Regelaktionen abgearbeitet; Skills wurden bewusst überprüft und ggf. konsolidiert erweitert; die öffentliche Edition bleibt getrennt. **Diese Übergabe selbst ist mit Erstellung abgeschlossen, die Spiele-Regressionstests sind es noch nicht.**

---

## 9 — BELEG- UND CODELINKS (STABILER RELEASE-COMMIT)

Alle nachfolgenden URLs beziehen sich als Reproduktionsanker auf `954097a`; Hermes muss bei Änderungen am lokalen HEAD die Zeilen und Verhalten neu ermitteln. Die öffentlich lesbaren Rohdateien von `main` wurden am 31.10.2026 zusätzlich geprüft; damit ist **nicht** nachgewiesen, dass der lokale Hermes-HEAD identisch ist.

- Release / Windows-EXE / SHA256: https://github.com/Decay03101991/Nebelseetal-Remake/releases/tag/v0.4.0-test.1
- Hauptlogik / UI / Lager / Missionspfade: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/src/main.py
  - globale Truppen: ungefähr `#L1684-L1711`, `#L4914-L4927`, `#L5199-L5227`
  - UI-Forschung: ungefähr `#L1660-L1681`; Warenoberfläche: `#L4276-L4331`
  - Abriss: `#L3641-L3670`; Portal: `#L4110-L4132`; Reichsanzeige `#L937-L945`
  - Kaserne/Ausbildung: `#L5603-L5761`
- Lokaler Ökonomiekern: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/src/spieloekonomie.py
  - `verbrauchen #L256-L274`, `ware_start #L387-L415`, `ausbildung_start #L417-L449`, `ort_tick #L459-L490`
- Werkstätten/Warteschlangen: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/src/werkstatt.py
  - `waren_der_werkstatt #L88-L99`, `einreihen #L180-L214`, `fortschritt #L216-L297`, `fertige_waren #L315-L325`
- Historische Warenzuordnung: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/data/items.json
- Aktive Pilot-Rezepte: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/data/warenrezepte.json
- 28 Einheiten / 14 Warenbedarfe: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/data/units.json
- Gebäude, Baukunst, Werkstätten, Ausbildungsstätten: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/data/buildings.json
- Ausrüstungskette: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/src/ausruestung.py
- Ausbaustufen/Regelherkunft: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/data/gebaeude_wirkung.json
- Admin-UI: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/src/admin_oberflaeche.py
- Admin-Mutationen: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/src/admin_werkzeuge.py
- Vorhandener Gesamt-Durchspieltest: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/tests/test_durchspiel.py
- Vorhandene Komponenten-Tests: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/tests/test_werkstatt.py und https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/tests/test_ausruestung.py
- Aktive Hermes-Übergabe: https://github.com/Decay03101991/Nebelseetal-Remake/blob/954097a/docs/HERMES_UEBERGABE_AKTUELL.md

---

## 10 — KURZE AUFTRAGSÜBERGABE AN HERMES

**Bitte nicht einfach „alles fixen“ und dadurch neue Abweichungen schaffen.** Zuerst die P0-Funde reproduzieren und durch Tests beweisen; dann mit dem Nutzer/Originalquellen über unklare Regeln (Abriss, Werkstattstufen, Sofortangriff, Echtzeit-Sperre) entscheiden. Danach alle W01–W17 und alle 14 Ausrüstungsketten als echte Herstellungs-/Ausbildungsketten testen. Den Adminbereich bevorzugt zur **Diagnose und reproduzierbaren Simulation** erweitern statt nur Bestände zu verschenken. Test-Skills anhand SK-01–SK-12 dauerhaft verbessern, sofern nicht bereits abgedeckt. Alle Änderungen nachvollziehbar, codeklar, ordentlich und ohne unnötige Doppeldateien halten. Hermes ist der einzige Hauptkoordinator; diese Datei bleibt externe Zuarbeit.

**Ende der externen Prüfung vom 31.10.2026.**
