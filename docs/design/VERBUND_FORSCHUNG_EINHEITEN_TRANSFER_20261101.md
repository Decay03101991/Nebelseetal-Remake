# AUFTRAG 2 – Entscheidungsentwurf für Weltenfresser

**Gegenstand:** S-3 Forschungsübernahme, S-4 Einheitenprüfung, S-6 Dorftransfer.
**Status:** ENTWURF, keine Implementierung und keine Freigabe fehlender Spielwerte.
**Stand:** 01.11.2026. **Quelle 1:** Hermes-Auftrag, Abschnitt 1 (lokaler Stand gilt gegenüber GitHub).
**Quelle 2:** öffentlich lesbare GitHub-Dateien auf `main`; sie sind ausdrücklich **kein** Nachweis des neueren lokalen Codes.
**Kennzeichnung:** `BELEGT` = vorgegebener Befund/ausdrücklich gelesener öffentlicher Quelltext; `VORSCHLAG` = entscheidbare neue Regel; `UNBEKANNT` = Hermes beziehungsweise Daniel muss klären.
**Geltungsgrenze:** Nur Spielmechanik. Änderungen an Hermes-Agenten, Skills und Systemregeln gehören nicht in das Nebelseetal-Entwicklungsprotokoll.

## 1. Forschungsstand – Bauform und Empfehlung

| Punkt | Bauform A: `verbund_forschung` | Bauform B: Maximum der Dorfstände | Urteil |
|---|---|---|---|
| Datenquelle | Ein globales Feld je Forschungsgebiet im JSON-Spielstand | Je Gebiet größter Dorfwert | VORSCHLAG – Auswahl A |
| Neue Bibliothek | Liest den aktuellen Verbundwert beim Bauen | Liest das aktuelle Maximum | VORSCHLAG |
| Fortentwicklung | Erfolgreicher Abschluss erhöht den einen Verbundwert | Abschluss erhöht einen Dorfwert, Maximum folgt | VORSCHLAG |
| Abriss der letzten hochstufigen Bibliothek | Erreichte Stufe bleibt erhalten | Stufe kann durch Abriss verloren gehen | VORSCHLAG – spricht für A |
| Dorf löschen | Kein Verlust der Forschung; Dorf hat keinen eigenen Verbundanspruch | Maximum kann sinken | VORSCHLAG – spricht für A |
| Bibliothek fehlt | Im Dorf ist Forschung lokal Stufe 0; Verbundwissen bleibt erhalten | Sonderfall nötig, sonst bleibt ein Dorfwert sichtbar | BELEGT (lokal Stufe 0), VORSCHLAG (Umsetzung) |
| Speicherung | Ein Feld mit einer maßgeblichen Version, kein neues Datenbanksystem | Mehrere persistierte Wahrheiten | VORSCHLAG – A minimiert Drift |
| Altstand ohne Feld | Lesefehler mit eindeutiger Abweisung; kein stiller Wert | Rekonstruktion nur, falls alte Dorfwerte vollständig sind | VORSCHLAG – Altstände dürfen brechen |
| Gleichzeitige Forschung | Aufträge prüfen globalen Zielkonflikt | Zwei Dorfstände können dieselbe Stufe bezahlen | VORSCHLAG – A mit Sperre |
| Implementierungsrisiko | Globale Aktualisierung bei Abschluss erforderlich | Lösch- und Kopierfälle fragil | VORSCHLAG |

**Entscheidungsempfehlung: Bauform A.** `verbund_forschung` ist ausschließlich für abgeschlossene Stufen maßgeblich; der lokale Forschungsstand ist ein **aus Bibliotheksbesitz und Verbundwert abgeleiteter Anzeigewert**, keine zweite unabhängig fortzuschreibende Wahrheit. **VORSCHLAG.**

| ID | Bindende Regel | Urteil |
|---|---|---|
| F-01 | Für jedes vorhandene Forschungsgebiet besitzt `verbund_forschung` genau eine nichtnegative, abgeschlossene Stufe. | VORSCHLAG |
| F-02 | Ohne eigene Bibliothek zeigt ein Dorf für alle Forschungsgebiete lokal Stufe 0 und darf dort keine Forschung beginnen. | BELEGT |
| F-03 | Mit eigener Bibliothek zeigt ein Dorf die Verbundsstufe und kann ausschließlich die nächste, noch nicht abgeschlossene Stufe starten. | BELEGT (Übernahme), VORSCHLAG (exakter Start) |
| F-04 | Nach erfolgreicher Forschung aktualisiert die Verbundsstufe **alle** vorhandenen Bibliotheksdörfer; bei jedem erneuten Öffnen wird derselbe Wert gelesen. | VORSCHLAG |
| F-05 | Wird die letzte Bibliothek abgerissen, bleibt `verbund_forschung` unverändert; neue Bibliothek übernimmt sie wieder. | VORSCHLAG |
| F-06 | Altstand ohne `verbund_forschung` wird ausdrücklich abgewiesen, ohne ihn zu überschreiben; keine automatische Migration. | VORSCHLAG |
| F-07 | Beim Start wird das Ziel je Gebiet auf `Verbundsstufe + 1` festgelegt; der gesamte Preis kommt **einmal** aus dem Ortslager des startenden Dorfes. | BELEGT (Ortslager), VORSCHLAG (Zielbindung) |
| F-08 | Ein weiteres Dorf darf dasselbe Gebiet nicht für dieselbe oder eine überlappende Zielstufe starten, solange ein Verbundauftrag dafür läuft. | VORSCHLAG |
| F-09 | Verschiedene Gebiete dürfen in verschiedenen Dörfern gleichzeitig erforscht werden; pro Dorf ist höchstens eine Forschung aktiv. | BELEGT (dorflokale Sperre), VORSCHLAG (Verbundparallelität) |
| F-10 | Bereits verbundweit abgeschlossene Stufen werden **nie** noch einmal bezahlt; die nächste Kostenstufe ist stets die nächste globale Stufe. | VORSCHLAG |
| F-11 | Bei gleichem Zeitpunkt wird ein fälliger Forschungsabschluss **vor** Abriss- oder Transferprüfung verarbeitet; danach gelten die normalen Sperren. | VORSCHLAG |
| F-12 | Alle Voraussetzungen, die der vorhandene Spielkern zusätzlich nachweislich prüft, bleiben bestehen; es werden keine neuen Forschungspreise erfunden. | VORSCHLAG |

**Quellenabgleich (öffentlicher, möglicherweise veralteter Stand):** `src/forschung.py`, Zeilen 6–25, bestätigt lokale Bibliothekspflicht, Abschluss nach Dauer, ortsbezogene Kostenabbuchung und Verlust bei Abbruch; Zeilen 110–137 sperren nur die gleichzeitige Forschung innerhalb eines Dorfstands. Die neue **gebietsglobale** Doppelstart-Sperre ist daher **VORSCHLAG**, nicht Ist-Funktion. 

## 2. S-3 – Randfallregeln der Forschungsübernahme

| Fall | Regel (was passiert) | Begründung | Zusage für eine Prüfdatei |
|---|---|---|---|
| S3-01: kein Dorf mit Bibliothek | Keine Forschung startbar; globale abgeschlossene Werte bleiben gespeichert. **VORSCHLAG** | Abriss darf Wissen nicht vernichten. | Ohne Bibliothek 0 Starts, globaler Wert unverändert. |
| S3-02: erste Bibliothek in Kolonie | Beim Bau wird der aktuelle globale Wert sofort angezeigt. **BELEGT/VORSCHLAG** | Eine Forschungsstand-Wahrheit. | Kolonie sieht Stufe X ohne neue Zahlung. |
| S3-03: Neubau während Hauptdorf forscht | Neue Bibliothek übernimmt nur **bereits abgeschlossene** Stufe X; die laufende Zielstufe X+1 erst bei Abschluss. **VORSCHLAG** | Kein vorzeitiger Freischaltgewinn. | Vor Abschluss X, danach X+1. |
| S3-04: niedrigere Bibliotheksstufe | Eigene Bibliotheksstufe senkt nicht die übernommene Verbundsstufe; sofern kein anderweitiger belegter Bau-Lock gilt, darf nächste Verbundstufe gestartet werden. **VORSCHLAG** | Bibliothek ist Zugang, kein Kopierdeckel. | Niedrige Bibliothek zeigt X und startet X+1. |
| S3-05: keine Bibliothek vor Forschungsstart | Start wird abgelehnt; Kosten und Aufträge bleiben gleich. **BELEGT** | Voraussetzung fehlt. | Fehlstart hat 0 Abbuchungen. |
| S3-06: zweite Forschung im selben Dorf | Start wird abgelehnt, gleichgültig welches Gebiet. **BELEGT** | Eine laufende Forschung sperrt diese Siedlung. | Zweiter Auftrag fehlt, Rohstoffe konstant. |
| S3-07: gleicher Bereich, anderes Dorf | Start wird abgelehnt, solange der erste Auftrag des Bereichs läuft. **VORSCHLAG** | Keine doppelt bezahlte Verbundsstufe. | Nur ein gebietsweiter aktiver Zielauftrag. |
| S3-08: anderes Gebiet, anderes Dorf | Start wird erlaubt, falls beide Orte jeweils alle Voraussetzungen erfüllen. **VORSCHLAG** | Dorflokale Sperre bleibt lokal. | Zwei verschiedene Gebiete dürfen laufen. |
| S3-09: Zweitdorf erreicht höhere Stufe | Nach Abschluss sehen alle Bibliotheksdörfer dieselbe höhere globale Stufe. **BELEGT/VORSCHLAG** | Zweitdorf entwickelt Hauptdorf mit. | Wert ist nachher in beiden Dörfern identisch. |
| S3-10: schon Stufe X im Verbund | Ein Dorf darf nicht erneut X bezahlen; nur X+1 wird angeboten. **VORSCHLAG** | Kein doppelter Ressourcenverbrauch. | Zahlungsanforderung zielt ausschließlich X+1. |
| S3-11: ungenügendes Ortslager | Start scheitert; weder anderes Dorf noch Reichssumme liefern Ersatz. **BELEGT** | Eigenes Ortslager. | Beide Lager und Aufträge unverändert. |
| S3-12: erfolgreicher Start | Preis wird aus startendem Dorf genau einmal abgebucht, Fertigstellung erhöht noch nicht den Wert. **BELEGT** | Start und Abschluss getrennt. | Genau eine Abbuchung, Stufe zunächst X. |
| S3-13: Abschluss | Stufe steigt bei Fälligkeit genau einmal; weitere Zeitprüfungen geben keinen zusätzlichen Stufenanstieg. **BELEGT/VORSCHLAG** | Doppelte Tick-Ausführung sicher. | Zweimal abschließen ergibt nur X+1. |
| S3-14: Abriss während Forschung | Bibliotheksabriss wird bis zum Abschluss oder **bewusst bestätigten Abbruch** blockiert; Abbruch verliert den bezahlten Preis. **BELEGT/VORSCHLAG** | Keine forschende Ruine. | Blockierter Abriss ändert nichts; Abbruch erst nach eigener Aktion. |
| S3-15: Fertigstellung und Abriss im selben Tick | Fälliger Abschluss wird zuerst verbucht; danach kann ohne aktiven Auftrag abgerissen werden. **VORSCHLAG** | Festgelegte Ereignisreihenfolge. | X+1 bleibt nach Abriss gespeichert. |
| S3-16: Dorftransfer während Forschung | Transfer wird abgelehnt, solange dieses Dorf aktiv forscht; ein fälliger Abschluss wird vorher eingetragen. **VORSCHLAG** | Keine Ortswechsel mit offenem Forschungsauftrag. | Koordinate und Lager bleiben bei Block unverändert. |
| S3-17: Laden mit gültigem globalen Feld | Alle Bibliotheksdörfer zeigen die geladenen Verbundsstufen; laufende, valide Aufträge bleiben bei ihrer fälligen Zielstufe. **VORSCHLAG** | Keine Rekonstruktion aus veralteten Dorfkopien. | Save/Load zeigt gleiche Werte, Restzeit und Lager. |
| S3-18: Laden ohne globales Feld | Ladeversuch wird lesend mit klarer Fehlermeldung beendet. **VORSCHLAG** | Teststand-Migration nicht gefordert. | Keine mutierte Datei und kein teilgeladener Zustand. |
| S3-19: zweite Bibliothek abgerissen | Nur die lokale Forschungsmöglichkeit dieses Dorfes endet; anderer Ort und globaler Stand bleiben gleich. **VORSCHLAG** | Gebietsweite Forschung bleibt ortsunabhängig. | Andere Bibliothek behält X. |
| S3-20: ungültiges Gebiet | Start wird vor Abbuchung abgelehnt. **BELEGT** | `src/forschung.py`, Zeilen 108–111. | Unbekanntes Gebiet erzeugt weder Auftrag noch Zahlung. |
| S3-21: Forschungsabbruch | Keine neue Stufe, abgebuchte Kosten bleiben verloren; globale Sperre des Gebiets wird danach frei. **BELEGT/VORSCHLAG** | Abbruchfolge aus öffentlichem Kern. | Alter Wert X, 0 Rückzahlung, neuer Start möglich. |
| S3-22: Bibliothek neu bei Verbundstand X | Kein erneutes Freischalten oder Nachzahlen für Stufen 1 bis X. **VORSCHLAG** | Verhindert Nachzahlungsfalle. | Bau setzt Ansicht X ohne Forschungskosten. |

**S-3-Abnahme:** Jeder abgelehnte Vorgang lässt globalen Stand, Ortslager, Bauzustand und offene Aufträge bytegleich; nur **erfolgreicher** Start, Abschluss, bewusster Abbruch oder Bau/Abriss ändern den jeweils betroffenen Teil. **VORSCHLAG.**

## 3. S-4 – Einheitenprüfung und stationierte Truppen

| Fall | Regel (was passiert) | Begründung | Prüfversprechen |
|---|---|---|---|
| S4-01: Akademie fehlt | Eine Einheit, deren Herstellungsgebäude die Kriegerakademie ist, wird hier nicht hergestellt. **BELEGT/VORSCHLAG** | Keine eigene Produktionsstätte. | Fehlende Akademie = 0 neue Akademieeinheiten. |
| S4-02: Akademiestufe = Verbundsstufe | Herstellung ist nach dieser zusätzlichen Stufenregel zulässig; normale Waren-/Siedlerkosten bleiben. **BELEGT** | Gleichheit genügt. | Gleichstand passiert Stufengate. |
| S4-03: Akademiestufe größer | Herstellung passiert das Stufengate; keine Sonderprämie oder weitere Stufe nötig. **BELEGT** | Größer ist zulässig. | A größer V passiert. |
| S4-04: Akademiestufe kleiner | Herstellung wird vor jeder Abbuchung verweigert; Meldung nennt beide Stufen. **BELEGT/VORSCHLAG** | Lokale Ausbildungsfähigkeit reicht nicht. | A kleiner V: 0 Kosten, Meldung mit A und V. |
| S4-05: Einheit noch nie im Verbund gebaut | Vorhandene, belegte Freischaltbedingungen gelten; „nie gebaut“ erzeugt **keine automatisch erfundene** hohe Verbundsstufe. **VORSCHLAG** | Erstproduktion soll nicht unmöglich werden. | Nicht vorhandener Einheitenstand wird nicht willkürlich erhöht. |
| S4-06: globale Einheitenstufe nicht definiert | Kein stiller Default für eine unbekannte Stufe; Hermes liefert Quelle/Berechnungsregel, bevor S4 freigegeben wird. **UNBEKANNT** | Die Definition von V fehlt. | Für fehlende V-Quelle keine unbemerkte Freigabe. |
| S4-07: fremde Einheit stationiert | Stationieren ist unabhängig von Akademiegebäude oder Akademiestufe erlaubt. **BELEGT** | Garnison ist nicht Herstellung. | A=0 kann fremde Einheit aufnehmen. |
| S4-08: stationierte Truppen verteidigen | Alle stationierten, kampffähigen Truppen werden in der Verteidigung berücksichtigt. **BELEGT** | Garnison zählt im Kampf. | Verteidigungsaufstellung enthält Garnison. |
| S4-09: Anzeige bei Stufensperre | Meldung nennt ausdrücklich „Akademie Stufe {akademie}“ und „Verbundsstufe {verbundstufe}“. **BELEGT/VORSCHLAG** | Spieler kann Ursache erkennen. | Beide Zahlen stehen im Ablehnungstext. |
| S4-10: Siedlerkarren | Original-Herstellungsort ist **Stellmacher**, nicht Kriegerakademie; kein Akademie-Stufengate, aber ursprüngliche Bau-/Forschungsvoraussetzungen. **BELEGT (Hersteller), VORSCHLAG (Ausnahme)** | Kein Produktionsortwechsel. | Siedlerkarren bleibt ohne Akademie möglich, wenn Originalbedingungen gelten. |
| S4-11: Kundschafter | Original-Kundschafter werden über **Diebesgilde** erstellt; Akademie-Stufengate gilt nicht dort, alle Originalbedingungen bleiben. **BELEGT (Hersteller), VORSCHLAG (Ausnahme)** | Rollen sind nicht identisch mit Akademieeinheiten. | Diebesgilde wird nicht durch Akademiezwang gesperrt. |
| S4-12: ursprüngliche Forschung | **Keine neue Zusatzforschung** wegen S-4; schon im Einheitendatensatz verlangte Forschung gilt weiterhin. **VORSCHLAG** | Regel nicht mit Freischaltung verwechseln. | S4 fügt 0 neue Forschungsforderungen hinzu. |
| S4-13: Kosten | Kein Reichsgold, keine zweite Kostenstelle: nur reguläre Kosten des herstellenden Dorfs. **BELEGT/VORSCHLAG** | Ortslager und Kaufregel bleiben. | Keine zweite Abbuchung, kein Lager eines anderen Dorfes. |
| S4-14: Garnison einer hochstufigen Einheit | Ankunft/Stationierung ist auch erlaubt, wenn örtliche Akademie niedriger ist; bei Angriff verteidigt sie regulär. **BELEGT** | Stationierung und Bau sind getrennte Operationen. | Aufnahme und Verteidigung trotz A kleiner V. |
| S4-15: Bauauftrag vor Stufenanstieg | Bereits rechtmäßig gestarteter Auftrag wird nicht nachträglich wegen eines fremden Verbundanstiegs abgebrochen; neue Aufträge werden neu geprüft. **VORSCHLAG** | Nicht rückwirkend entwerten. | Laufender Auftrag bleibt, neuer kann gesperrt werden. |
| S4-16: Wechsel des Herstellungsgebäudes | Die originale Angabe `gebaeude` je Einheit entscheidet, ob Akademieregel anwendbar ist; keine pauschale Behandlung aller Rollen. **VORSCHLAG** | Stellmacher/Diebesgilde existieren. | Nicht-Akademieeinheiten erhalten keine falsche Sperre. |
| S4-17: unbekannte Einheit | Ohne bekannten Datensatz wird nicht produziert, keine Kostenabbuchung. **VORSCHLAG** | Keine freie Interpretation. | Unbekannter Typ 0 neue Einheiten. |

**Quellenabgleich:** `data/units.json`, Zeilen 713–726: Siedlerkarren beim `Stellmacher`; Zeilen 300–303 und 330–333: Kundschafter in der `Diebesgilde`. `src/einheiten.py`, Zeilen 17–30, trennt Kämpfer, Kundschafter, Karren und Belagerung. Die **Ausnahmeentscheidung** zur Akademieregel bleibt von Daniel zu bestätigen. 

## 4. S-6 – Dorftransfer über Weltkarte/Weltensprung

| Schritt | Was der Spieler sieht | Was der Kern prüft | Was NICHT passieren darf |
|---|---|---|---|
| T-01 Feld auswählen | Klick auf freies 20×20-Feld, Zielwelt und {x}, {y}. **BELEGT** | Existiert Zielwelt, Feld in Grenzen, frei? **VORSCHLAG** | Kein Koordinaten-Dropdown, kein direkter Umzug. |
| T-02 Zielvorschau | Markierung des gewählten Zielfelds. **VORSCHLAG** | Feld bleibt vorläufig, noch kein Besitzerwechsel. | Keine Kosten und keine Koordinatenänderung. |
| T-03 Dorfliste öffnen | Nur eigene Dörfer mit aktuell ausreichendem Ortslager; fehlende Dörfer als begründete Sperren kenntlich machen. **BELEGT/VORSCHLAG** | Eigentümer, mindestens ein Dorf, höchstens sechs eigene Dörfer insgesamt. | Keine Auswahl fremder oder zahlungsunfähiger Dörfer. |
| T-04 genau ein Dorf wählen | Name, alte Welt/Koordinate und Ziel, nicht mehrere markierbar. **BELEGT** | Ausgewähltes Dorf existiert noch und ist nicht bereits Ziel eines Transfers. | Kein Sammelumzug. |
| T-05 Kosten anzeigen | „{mana_kosten} Mana“; beim Weltensprung zusätzlich „{gold_kosten} Gold“, alles aus diesem Dorf. **BELEGT/VORSCHLAG** | Angezeigte Werte stammen aus genehmigten Regeln, nicht aus geschätzten Zahlen. | Kein verborgenes Reichslager. |
| T-06 Sperren prüfen | Alle konkreten Gründe gleichzeitig in einer Liste. **VORSCHLAG** | Aktuelle Bewegung, Forschung, Schutzflag, Zielbelegung, Lager. | Keine Abbuchung vor Freigabe. |
| T-07 Auftragsvorschau | Aufträge mit alten und neu berechneten Restwegen und Zeiten, soweit rechnerisch belegbar. **BELEGT/VORSCHLAG** | Betroffene **nicht bereits unterwegs befindliche** Aufträge ermitteln. | Nicht eingreifbare Reise blind umbiegen. |
| T-08 Langwegwarnung | „{anzahl} Aufträge würden länger als {grenzwert} dauern; längster Weg {dauer}.“ **VORSCHLAG** | Schwelle/Geschwindigkeit müssen definiert sein. **UNBEKANNT** | Ohne genehmigte Schwelle keine erfundene Warnzahl. |
| T-09 endgültig bestätigen | Alte/Neue Koordinate, Gesamtkosten, gegebenenfalls Warnung und „Bestätigen/Abbrechen“. **VORSCHLAG** | Spieler bestätigt genau diesen Zielzustand. | Warnung niemals nur informativ wegklicken. |
| T-10 unmittelbar neu prüfen | Bei Änderung: genaue Ablehnung und Rückkehr zur Vorschau. **VORSCHLAG** | Feld, Ortslager, Bewegungen, laufende Forschung, Schutz und Dorf neu prüfen. | Kein veralteter Dialog darf den Transfer autorisieren. |
| T-11 Herold nimmt Kosten | Kurze Darstellung „Herold holt {mana_kosten} Mana“ und beim Sprung {gold_kosten} Gold. **BELEGT/VORSCHLAG** | Einmalige Abbuchung im selben abgeschlossenen Vorgang; Herold ist nur Animation. | Kein echter Reiseauftrag, keine doppelte Zahlung. |
| T-12 Position ändern | Dorf wechselt mitsamt Lager, Karte, Gebäuden, stationierten Einheiten und Aufträgen. **BELEGT** | Quellfeld freigeben, Zielfeld besetzen, alte und neue Referenz konsistent. | Kein zweites Dorf, keine verwaiste Belegung. |
| T-13 erlaubte Aufträge anpassen | Sichtbare neue Ausgangskoordinate und neu berechnete Wege für nicht reisende offene Aufträge. **BELEGT/VORSCHLAG** | Derselbe Auftrag bleibt identifizierbar; nur Ortsbezug/Laufzeit wird aktualisiert. | Auftrag nicht duplizieren oder verschlucken. |
| T-14 Postfach | „Dorf {dorf} von {alte_welt} ({alt_x}/{alt_y}) nach {neue_welt} ({neu_x}/{neu_y}) versetzt.“ **BELEGT/VORSCHLAG** | Nur nach erfolgreicher Positionierung eine Bestätigung erzeugen. | Keine Erfolgsmeldung bei Ablehnung. |
| T-15 Weltkarte aktualisieren | Genau ein Dorf-Icon am neuen Feld, keines am alten. **BELEGT/VORSCHLAG** | Besitzer/Koordinaten stimmen mit gespeicherter Dorfkennung überein. | Kein Geister-Icon, kein verlorenes Dorf. |
| T-16 Abbrechen | Rückkehr ohne Meldung „erfolgreich“. **VORSCHLAG** | Ursprungswerte unverändert. | Keine Teilzahlung, keine reservierte Zielbelegung. |
| T-17 Ziel wird zwischenzeitlich belegt | Ablehnung beim abschließenden Recheck mit neuer Belegung. **VORSCHLAG** | Ziel erneut auf Belegung prüfen. | Kein Überschreiben fremden Dorfs. |
| T-18 neue Bewegung/Schutz während Dialog | Freigabe erlischt; erneute Bestätigung nach Entsperrung nötig. **VORSCHLAG** | Alle Sperren gelten im Commitzeitpunkt. | Kein Umzug über alte Freigabe. |

### Sperrliste für den Kern

| Sperre | Bedingung | Meldung (deutsch, mit Zahl/Platzhalter) | Urteil |
|---|---|---|---|
| T-L01: Feld belegt | Am Ziel liegt ein Dorf/Objekt, das Belegung sperrt. | „Feld {x}/{y} in {welt} ist bereits belegt; 0 Dörfer versetzt.“ | VORSCHLAG |
| T-L02: Feld unzulässig | Koordinate außerhalb des 20×20-Felds. | „Ziel {x}/{y} liegt außerhalb der 20×20-Weltkarte; 0 Dörfer versetzt.“ | BELEGT/VORSCHLAG |
| T-L03: Welt geschlossen | Zielwelt nicht bespielbar (zunächst nur Midgard/Valhalla). | „{welt} ist noch gesperrt; verfügbar sind {anzahl_freigeschaltete} Welten.“ | BELEGT/VORSCHLAG |
| T-L04: kein Dorf ausgewählt | Null statt exakt einem eigenen Dorf ausgewählt. | „Wähle genau 1 eigenes Dorf; gewählt: {anzahl}.“ | BELEGT/VORSCHLAG |
| T-L05: mehrere Dörfer | Mehr als ein Dorf ausgewählt. | „Pro Vorgang darf genau 1 Dorf umziehen; gewählt: {anzahl}.“ | BELEGT |
| T-L06: fremdes Dorf | Dorf gehört nicht dem Spieler. | „Dorf {dorf} gehört dir nicht; 0 Dörfer versetzt.“ | VORSCHLAG |
| T-L07: Reise läuft | Mindestens ein diesem Dorf zugeordneter echter Truppen-/Transportweg ist bereits unterwegs. | „Transfer gesperrt: {anzahl} Trupp- oder Transportbewegungen sind noch unterwegs.“ | BELEGT/VORSCHLAG |
| T-L08: Forschung läuft | Dorf hat einen aktiven Forschungsauftrag. | „Transfer gesperrt: 1 Forschungsauftrag in {dorf} läuft noch.“ | VORSCHLAG |
| T-L09: Mana fehlt | Lokal verfügbar < genehmigte Transfer-Manakosten. | „In {dorf} fehlen {fehlmenge} Mana; benötigt {mana_kosten}, vorhanden {mana_vorhanden}.“ | VORSCHLAG; Betrag UNBEKANNT |
| T-L10: Gold fehlt | Weltensprung und lokal Gold < genehmigter Goldpreis. | „In {dorf} fehlen {fehlmenge} Gold; benötigt {gold_kosten}, vorhanden {gold_vorhanden}.“ | VORSCHLAG; Betrag UNBEKANNT |
| T-L11: Götterschutz | Schutzregel untersagt Ortswechsel und Schutz ist aktiv. | „Weltensprung während Götterschutz nicht erlaubt; Restzeit {schutz_restzeit}.“ | VORSCHLAG; konkrete Sperre UNBEKANNT |
| T-L12: kein Sprungziel | Ausgewähltes Zielfeld ist das eigene aktuelle Feld. | „Dorf {dorf} steht bereits auf {x}/{y}; Entfernung 0 Felder.“ | VORSCHLAG |
| T-L13: Daten geändert | Seit der Vorschau wurde Lager/Ziel/Status verändert. | „Daten haben sich geändert; prüfe die {anzahl_geaenderte} geänderten Bedingungen erneut.“ | VORSCHLAG |
| T-L14: Transfer bereits ausgeführt | Bestätigung wird für denselben abgeschlossenen Vorgang wiederholt. | „Dorf {dorf} steht bereits am Ziel; 0 zusätzliche Mana abgebucht.“ | VORSCHLAG |
| T-L15: Weltwechselpreis offen | Der Preis für Weltensprung ist nicht freigegeben. | „Weltensprung nicht verfügbar: {anzahl_offene_kostenwerte} Kostenwerte sind ungeklärt.“ | UNBEKANNT — von Hermes/Daniel zu liefern |
| T-L16: Laufzeitschwelle offen | Warnung benötigt, aber Schwellwert nicht festgelegt. | „Laufzeitwarnung nicht verfügbar: {anzahl_fehlende_grenzwerte} Grenzwerte fehlen.“ | UNBEKANNT — von Hermes/Daniel zu liefern |

### Bindende Reihenfolge und Begriffe

| ID | Regel | Urteil |
|---|---|---|
| T-R01 | „Unterwegs“ meint für den **vorgeschlagenen** Sperrpfad bereits gestartete, real reisende Truppen/Transporte; offene, noch nicht gestartete ortsbezogene Aufträge können umgerechnet werden. | VORSCHLAG; Konflikt mit unbestimmtem Wort „laufende Aufträge“ offen |
| T-R02 | Sind solche Reisenden unterwegs, gibt es **keinen** Transfer und folglich keine laufende Reise, deren Route beim Umzug verändert werden müsste. | VORSCHLAG |
| T-R03 | Alle bestätigungsrelevanten Bedingungen werden beim Klick und nochmals unmittelbar vor einmaliger Abbuchung geprüft. | VORSCHLAG |
| T-R04 | Bei Fehlschlag werden Kosten, Belegungen, Aufträge und Postfach unverändert gelassen. | VORSCHLAG |
| T-R05 | Der Herold ist eine kurze Darstellung **ohne** echten Trupp, Wegzeit, Zeitfortschritt oder zweiten Auftrag. | BELEGT/VORSCHLAG |
| T-R06 | Nach erfolgreicher Abbuchung folgen Ortswechsel, erlaubte Auftragsanpassung und genau eine Postfachmeldung als ein abgeschlossener Vorgang. | VORSCHLAG |
| T-R07 | Der Zielklick aktiviert keine zusätzliche frei formulierte Koordinateneingabe. | BELEGT |
| T-R08 | Höchstens sechs Dörfer gilt **weltkartenübergreifend**; Umzug schafft kein siebtes Dorf. | BELEGT |
| T-R09 | Weltensprung bleibt gesperrt, solange erforderliche Mana-/Goldwerte nicht genehmigt sind; 500 Mana ist derzeit nur ein vorgeschlagener Wert. | VORSCHLAG / UNBEKANNT |
| T-R10 | Warngrenze für „überlange Laufzeit“ bleibt **UNBEKANNT**; keine automatische Schwellwertannahme. | UNBEKANNT — von Hermes zu liefern |

**Konflikt, zwingend vor S-6 zu entscheiden:** Der neue Auftrag fordert „gesperrt, solange etwas unterwegs ist“, zugleich „laufende Aufträge bekommen neue Position und neu berechneten Weg“. Beides ist nur widerspruchsfrei, wenn „unterwegs“ und „offener Auftrag“ klar getrennt werden. **VORSCHLAG:** schon gestartete physische Reisen sperren, rein vorgemerkte ortsbezogene Aufträge werden nach Bestätigung umgerechnet.

**Quellenkonflikt:** Öffentliches `data/welten.json`, Zeilen 18–27, dokumentiert **5.000 Mana** und **einmal in 24 Stunden** als historische Koordinatenwechsel-Regeln. Hermes-Auftrag nennt **500 Mana nur als Vorschlag** und Gold beim Weltensprung. Auch `src/welt.py`, Zeilen 64–88, kennt für Portaldimensionen eine eigene Kostenrechnung. Keine dieser Regeln ohne Daniels Entscheidung still mischen. **BELEGT (Quellen), UNBEKANNT (neue Freigabe).**

## 5. Wörtliche Spielertexte und Ablehnungen

| ID | Wortlaut (Platzhalter werden aus dem geprüften Zustand befüllt) | Urteil |
|---|---|---|
| M-01 | „In {dorf} fehlt eine Bibliothek. Lokale Forschungsstufe: 0; Verbundsstufe: {verbundstufe}.“ | VORSCHLAG |
| M-02 | „{dorf} hat die Verbundsforschung {gebiet} auf Stufe {stufe} übernommen. Forschungsgebühr: 0.“ | VORSCHLAG |
| M-03 | „Forschung {gebiet} auf Stufe {zielstufe} gestartet; Dauer {dauer_stunden} Stunden, Kosten {kosten_text} aus {dorf}.“ | VORSCHLAG |
| M-04 | „Forschung {gebiet} läuft bereits in {anderes_dorf} bis Stufe {zielstufe}; weitere Starts: 0.“ | VORSCHLAG |
| M-05 | „In {dorf} läuft bereits 1 Forschungsauftrag; erst nach dessen Abschluss kannst du erneut forschen.“ | VORSCHLAG |
| M-06 | „Forschung {gebiet} Stufe {stufe} abgeschlossen; der Verbund hat jetzt Stufe {stufe}.“ | VORSCHLAG |
| M-07 | „Forschung {gebiet} Stufe {stufe} ist im Verbund bereits vorhanden; erneute Kosten: 0.“ | VORSCHLAG |
| M-08 | „Forschung in {dorf} kann nicht starten: {fehlmenge} {rohstoff} fehlen im Ortslager.“ | VORSCHLAG |
| M-09 | „Bibliothek von {dorf} kann während 1 laufenden Forschungsauftrag nicht abgerissen werden.“ | VORSCHLAG |
| M-10 | „Forschung {gebiet} abgebrochen; erreichte Stufe {stufe}, Rückzahlung 0 Rohstoffe.“ | VORSCHLAG |
| M-11 | „Spielstand nicht geladen: Feld verbund_forschung fehlt; 0 Änderungen vorgenommen.“ | VORSCHLAG |
| M-12 | „{einheit} kann hier nicht ausgebildet werden: Akademie Stufe {akademie}, Verbundsstufe {verbundstufe}.“ | VORSCHLAG |
| M-13 | „{einheit} ist stationiert in {dorf}; für die Stationierung ist Akademie Stufe 0 ausreichend.“ | VORSCHLAG |
| M-14 | „{anzahl} stationierte kampffähige Einheiten verteidigen {dorf}.“ | VORSCHLAG |
| M-15 | „{einheit} wird in {gebaeude} hergestellt; zusätzliche Akademieanforderung: 0.“ | VORSCHLAG |
| M-16 | „Ausbildung von {einheit} nicht möglich: {fehlmenge} {rohstoff} fehlen in {dorf}.“ | VORSCHLAG |
| M-17 | „Dorf {dorf} nach {welt} ({x}/{y}) versetzen? Benötigt {mana_kosten} Mana und {gold_kosten} Gold aus diesem Dorf.“ | VORSCHLAG |
| M-18 | „{anzahl} offene Aufträge ändern ihren Weg: längste neue Laufzeit {dauer}, Grenze {grenzwert}. Trotzdem umziehen?“ | VORSCHLAG; Schwelle UNBEKANNT |
| M-19 | „Herold holt {mana_kosten} Mana und {gold_kosten} Gold in {dorf} ab.“ | VORSCHLAG |
| M-20 | „Dorf {dorf} von {alte_welt} ({alt_x}/{alt_y}) nach {neue_welt} ({neu_x}/{neu_y}) versetzt.“ | VORSCHLAG |
| M-21 | „Der Transfer wurde abgebrochen; 0 Rohstoffe abgebucht, 0 Dörfer versetzt.“ | VORSCHLAG |
| M-22 | „Transfer gesperrt: {anzahl} Truppen oder Transporte von {dorf} sind noch unterwegs.“ | VORSCHLAG |
| M-23 | „Transfer gesperrt: In {dorf} läuft noch 1 Forschungsauftrag.“ | VORSCHLAG |
| M-24 | „Zielfeld {x}/{y} in {welt} ist belegt; 0 Dörfer versetzt.“ | VORSCHLAG |
| M-25 | „Für den Transfer fehlen {fehlmenge} Mana in {dorf}; benötigt {mana_kosten}, vorhanden {mana_vorhanden}.“ | VORSCHLAG |
| M-26 | „Für den Weltensprung fehlen {fehlmenge} Gold in {dorf}; benötigt {gold_kosten}, vorhanden {gold_vorhanden}.“ | VORSCHLAG |
| M-27 | „Dorf {dorf} darf wegen Götterschutz noch {schutz_restzeit} nicht versetzt werden.“ | VORSCHLAG; Schutzregel UNBEKANNT |
| M-28 | „Weltensprung nicht freigegeben: {anzahl_offene_kostenwerte} Kostenangaben fehlen.“ | UNBEKANNT – von Hermes/Daniel zu liefern |
| M-29 | „Feld {x}/{y} in {welt} ist nicht erreichbar; erlaubte Weltkarten: {freigegebene_welten}.“ | VORSCHLAG |
| M-30 | „Dein Dorf steht bereits bei {x}/{y}; Distanz 0, Zahlung 0.“ | VORSCHLAG |

## 6. Prüfplan – eine Wache je Randfall und Transferregel

**Benennung:** Die folgenden Wachen sind **neue vorgeschlagene Prüffall-IDs**, keine Behauptung bestehender Testdateien. **Altwache = `UNBEKANNT`**, bis Hermes im neueren lokalen Prüfstand den tatsächlichen Namen und eine gegebenenfalls widersprechende Erwartung nennt. Kein Test darf allein wegen des neuen Entwurfs stillschweigend geändert oder als „rot“ behauptet werden.

| Neue Wache | Zusage (Werte rein, Werte raus; ohne GUI) | Alte Wache, die dadurch rot werden kann |
|---|---|---|
| W-S3-01 | Ohne Bibliotheken bleiben alle globalen Stufen erhalten. | UNBEKANNT – Hermes prüft Bibliotheksabriss |
| W-S3-02 | Neubau übernimmt X ohne Kosten. | UNBEKANNT – Hermes prüft Koloniegründung |
| W-S3-03 | Neubau während Auftrag zeigt X, nach Abschluss X+1. | UNBEKANNT – Hermes prüft Forschungsanzeige |
| W-S3-04 | Niedrige Bibliotheksstufe deckelt globalen Stand nicht. | UNBEKANNT – Hermes prüft Startprädikate |
| W-S3-05 | Start ohne Bibliothek 0 Abbuchungen. | UNBEKANNT – Hermes prüft lokale Forschung |
| W-S3-06 | Zweiter Start im selben Dorf scheitert. | UNBEKANNT – Hermes prüft Forschungsverriegelung |
| W-S3-07 | Zwei Dörfer dürfen nicht dasselbe Gebiet parallel bezahlen. | UNBEKANNT – Hermes prüft parallele Starts |
| W-S3-08 | Zwei Dörfer dürfen unterschiedliche Gebiete gleichzeitig forschen. | UNBEKANNT – Hermes prüft globale Locks |
| W-S3-09 | Zweitdorfabschluss erhöht global und Hauptdorf. | UNBEKANNT – Hermes prüft Verbundkopplung |
| W-S3-10 | X ist kostenfrei übernommen, nächstes Ziel X+1. | UNBEKANNT – Hermes prüft Preisauswahl |
| W-S3-11 | Fehlbetrag in eigenem Ortslager führt zu kompletter Ablehnung. | UNBEKANNT – Hermes prüft Ortslager |
| W-S3-12 | Start bucht genau einmal; globale Stufe bleibt vorerst X. | UNBEKANNT – Hermes prüft Abrechnung |
| W-S3-13 | Zwei identische Fertig-Ticks erhöhen nur einmal. | UNBEKANNT – Hermes prüft Ticklogik |
| W-S3-14 | Abriss mit Auftrag abgelehnt; bestätigter Abbruch verliert Zahlung. | UNBEKANNT – Hermes prüft Abriss |
| W-S3-15 | Gleichzeitiges Fälligwerden+Abriss erhält den Abschluss. | UNBEKANNT – Hermes prüft Reihenfolge |
| W-S3-16 | Aktive Forschung blockiert Dorftransfer ohne Teiländerung. | UNBEKANNT – Hermes prüft Transferfreigabe |
| W-S3-17 | Gültiges Save/Load bewahrt Globalstand und aktive Zeit. | UNBEKANNT – Hermes prüft Save/Load |
| W-S3-18 | Fehlendes Globalfeld wird ohne Seiteneffekt abgewiesen. | UNBEKANNT – Hermes prüft Altstand |
| W-S3-19 | Abriss zweiter Bibliothek verändert andere Dorfansicht nicht. | UNBEKANNT – Hermes prüft Bibliotheksstatus |
| W-S3-20 | Unbekanntes Forschungsgebiet wird nicht bezahlt. | UNBEKANNT – Hermes prüft Eingabevalidierung |
| W-S3-21 | Abbruch gibt Ziel frei, erstattet nichts, global bleibt X. | UNBEKANNT – Hermes prüft Forschungsabbruch |
| W-S3-22 | Bibliothek auf Stufe X verlangt keine Nachzahlungen. | UNBEKANNT – Hermes prüft Übernahmekosten |
| W-S4-01 | Ohne Akademie keine Akademieproduktion. | UNBEKANNT – Hermes prüft Gebäudezuordnung |
| W-S4-02 | Eigene Akademie gleich Verbundsstufe passiert Gate. | UNBEKANNT – Hermes prüft Stufenvergleich |
| W-S4-03 | Eigene Akademie höher passiert Gate. | UNBEKANNT – Hermes prüft Stufenvergleich |
| W-S4-04 | Niedrigere Stufe blockiert ohne Abbuchung, Meldung enthält beide. | UNBEKANNT – Hermes prüft Einheitenmenü |
| W-S4-05 | Nie produzierter Typ erhält keine erfundene hohe Stufe. | UNBEKANNT – Hermes prüft Erstproduktion |
| W-S4-06 | Fehlende Verbundsstufenquelle wird nicht still als 0 gelesen. | UNBEKANNT – Hermes liefert Datenquelle |
| W-S4-07 | Fremdgarnison ohne Akademie zulässig. | UNBEKANNT – Hermes prüft Garnison |
| W-S4-08 | Kampffähige Stationierte sind Teil der Verteidigung. | UNBEKANNT – Hermes prüft Schlachtaufstellung |
| W-S4-09 | Stufenablehnung nennt beide Zahlen. | UNBEKANNT – Hermes prüft Meldungen |
| W-S4-10 | Siedlerkarren braucht keine Akademie, behält Stellmacherregeln. | UNBEKANNT – Hermes prüft Karrenbau |
| W-S4-11 | Kundschafter braucht keine Akademie, behält Diebesgilde. | UNBEKANNT – Hermes prüft Kundschafter |
| W-S4-12 | Keine neue S4-Forschung; alte Voraussetzungen bleiben. | UNBEKANNT – Hermes prüft Forschungsgates |
| W-S4-13 | Herstellung belastet nur das Ortslager einmal. | UNBEKANNT – Hermes prüft Kosten |
| W-S4-14 | Höhere fremde Garnison verteidigt trotz niedriger Akademie. | UNBEKANNT – Hermes prüft Einheitenzulassung |
| W-S4-15 | Laufender Auftrag wird durch neuen globalen Wert nicht entwertet. | UNBEKANNT – Hermes prüft Ausbildungswarteschlange |
| W-S4-16 | Akademieregel wirkt ausschließlich auf akademiegebundene Einheiten. | UNBEKANNT – Hermes prüft Herstellungsort |
| W-S4-17 | Unbekannter Einheitentyp 0 Abbuchungen. | UNBEKANNT – Hermes prüft Fehlertypen |
| W-S6-01 | Klick auf belegtes/außerhalb liegendes Feld erzeugt keine Dorfauswahl. | UNBEKANNT – Hermes prüft Kartenklick |
| W-S6-02 | Zielfeldvorschau bucht 0 Ressourcen. | UNBEKANNT – Hermes prüft Vorschau |
| W-S6-03 | Wählbar sind nur eigene zahlungsfähige Dörfer. | UNBEKANNT – Hermes prüft Dorfliste |
| W-S6-04 | Genau ein Dorf wird ausgewählt, anderes bleibt gleich. | UNBEKANNT – Hermes prüft Mehrfachtransfer |
| W-S6-05 | Kostenanzeige verwendet nur freigegebene Werte aus Ortslager. | UNBEKANNT – Hermes prüft Kostenanzeige |
| W-S6-06 | Sperrenprüfung hat 0 Seiteneffekte. | UNBEKANNT – Hermes prüft Transferablehnung |
| W-S6-07 | Nichtreisende offene Aufträge haben alte/neue Wegwerte. | UNBEKANNT – Hermes prüft Wegzeiten |
| W-S6-08 | Fehlt genehmigte Langwegschwelle, wird keine Warnzeit erfunden. | UNBEKANNT – Hermes prüft Laufzeitwarnung |
| W-S6-09 | Abbrechen nach Warnung verändert nichts. | UNBEKANNT – Hermes prüft Bestätigung |
| W-S6-10 | Wechsel von frei auf belegt verhindert Abschluss ohne Zahlung. | UNBEKANNT – Hermes prüft Recheck |
| W-S6-11 | Herold zahlt genau einmal, ohne realen Reiseauftrag. | UNBEKANNT – Hermes prüft Truppablauf |
| W-S6-12 | 1 Dorf mit allem Besitz an neuem Ort, altes Feld frei. | UNBEKANNT – Hermes prüft Weltbelegung |
| W-S6-13 | Aufträge erhalten neuen Ortsbezug und neu berechnete zulässige Wege. | UNBEKANNT – Hermes prüft Auftragsbindung |
| W-S6-14 | Nur erfolgreicher Wechsel erzeugt 1 Postfachbestätigung. | UNBEKANNT – Hermes prüft Postfach |
| W-S6-15 | 1 Icon neu und 0 Icons am alten Feld. | UNBEKANNT – nur GUI-/Datenabgleich erforderlich |
| W-S6-16 | Abbruch 0 Zahlung, 0 Zielreservierung. | UNBEKANNT – Hermes prüft Transaktionsgrenze |
| W-S6-17 | Fremde Zielbelegung unterbricht auch nach vorheriger Vorschau. | UNBEKANNT – Hermes prüft Zielkonflikt |
| W-S6-18 | Bewegung oder Schutzänderung invalidiert alte Bestätigung. | UNBEKANNT – Hermes prüft Recheck |
| W-S6-L01 | Feldbelegung: belegtes Feld bleibt unverändert; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Kartenbelegung |
| W-S6-L02 | Grenzprüfung: ungültige Koordinate blockiert; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Koordinatenprüfung |
| W-S6-L03 | Weltfreigabe: geschlossene Welt blockiert; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Weltfreigabe |
| W-S6-L04 | Kein Dorf gewählt: abgelehnt; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Dorfauswahl |
| W-S6-L05 | Mehrere Dörfer gewählt: abgelehnt; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Sammelumzug |
| W-S6-L06 | Fremdes Dorf gewählt: abgelehnt; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Eigentum |
| W-S6-L07 | Mindestens eine aktive Reise blockiert Transfer; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Truppenweg |
| W-S6-L08 | Forschungsauftrag blockiert Transfer; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Forschungslock |
| W-S6-L09 | Lokaler Manamangel blockiert ohne Kosten; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Manakosten |
| W-S6-L10 | Lokaler Goldmangel beim Sprung blockiert ohne Kosten; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Goldkosten |
| W-S6-L11 | Aktiver Götterschutz blockiert nur nach Freigabe dieser Schutzregel; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Götterschutz |
| W-S6-L12 | Identische Start- und Zielkoordinate blockiert; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Koordinatenvergleich |
| W-S6-L13 | Dialog nach Zustandsänderung neu geprüft; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Statusänderung |
| W-S6-L14 | Doppelte Bestätigung bucht kein zweites Mal; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Wiederholschutz |
| W-S6-L15 | Fehlender Weltwechselpreis sperrt Weltensprung; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Kostenfreigabe |
| W-S6-L16 | Fehlende Warnschwelle darf keinen Schwellenwert erfinden; alle Ablehnungen mit 0 Seiteneffekt und Zahlenmeldung. | UNBEKANNT – Hermes prüft Laufzeitwarnung |
| W-S6-R01 | Reisende vs. wartende Aufträge werden unterschiedlich klassifiziert. | UNBEKANNT – Hermes prüft Auftragsarten |
| W-S6-R02 | Aktiver Reiseauftrag blockiert; Auftragsdaten bleiben unverändert. | UNBEKANNT – Hermes prüft Transitverbot |
| W-S6-R03 | Vor Zahlung erneute Prüfung aller Sperren. | UNBEKANNT – Hermes prüft Bestätigung |
| W-S6-R04 | Fehlschlag ändert keine Bestände, Belegung oder Postfach. | UNBEKANNT – Hermes prüft Abbruchfolgen |
| W-S6-R05 | Herold erzeugt keinen echten Truppauftrag. | UNBEKANNT – Hermes prüft Herold |
| W-S6-R06 | Erfolg 1 Abbuchung, 1 Ortswechsel, 1 Postfacheintrag. | UNBEKANNT – Hermes prüft Abschluss |
| W-S6-R07 | Es wird keine Koordinatenliste akzeptiert. | UNBEKANNT – Hermes prüft Klicknavigation |
| W-S6-R08 | Dorfanzahl über alle Welten bleibt höchstens sechs. | UNBEKANNT – Hermes prüft Dorflimit |
| W-S6-R09 | Ohne genehmigte Transferpreise kein Zahlungsvorgang. | UNBEKANNT – Hermes prüft Preisfreigabe |
| W-S6-R10 | Ohne festgelegte Langwegschwelle keine falsche Zeitwarnung. | UNBEKANNT – Hermes prüft Langweggrenze |

**Prüfgrenze GUI:** T-01 (Klickziel statt Dropdown), T-11 (sichtbarer Herold), T-15 (sichtbares Icon), Meldungslayout und die tatsächliche Postfachdarstellung müssen **zusätzlich im Fenster** geprüft werden. Die zugrunde liegenden Zustände sind mit den Wachen W-S6-01, W-S6-11, W-S6-14 und W-S6-15 ohne Fenster messbar. **VORSCHLAG.**

**Umsetzungseinheiten für `deepseek-v4-flash`:** S-3a globaler Stand/Save-Lesen → S-3b Bibliotheksanzeige/Übernahme → S-3c Start- und Doppelstart-Gates → S-3d Abschluss/Abbruch; S-4a akademiegebundene Produktion → S-4b Sondergebäude/Garnison; S-6a Zielfeld/Dorfauswahl → S-6b Sperren/Kostenvorschau → S-6c einmaliger Transfer → S-6d Aufträge/Postfach → S-6e GUI/Langwegwarnung **erst nach Zahlenfreigabe**. Jeder Schnitt bekommt eigene neue Wache, anschließend vollständigen Prüflauf, EXE-Beleg und genau einen Commit durch Weltenfresser. **VORSCHLAG.**

## 7. Offene Entscheidungen an Daniel (Empfehlung zuerst; höchstens acht)

| Nr. | Empfehlung | Zu entscheiden / warum | Urteil |
|---|---|---|---|
| Q-01 | **A: globales Feld `verbund_forschung`**; alte Teststände ohne Feld nicht laden. | Alternative B verliert Wissen bei Abriss; soll der JSON-Fallback ausdrücklich ausbleiben? | VORSCHLAG |
| Q-02 | **Herstellungsort respektieren**: Akademiestufe nur für echte Kriegerakademieeinheiten. | Wörtliche All-Einheiten-Regel M-5 würde sonst Stellmacher/Diebesgilde mit sperren. | VORSCHLAG; Daniel bestätigt |
| Q-03 | **500 Mana noch nicht bauen.** Bestehenden historischen Wert 5.000 Mana plus 24-Stunden-Regel mit neuer M-9/M-10-Regel abgleichen. | Welcher Wert und welche Sperrfrist gelten für Dorf- versus Weltwechsel? | UNBEKANNT – Daniel liefert |
| Q-04 | **Weltensprung zusätzlich Gold aus Dorf-Ortslager**, aber erst nach Festlegung des konkreten Preises. | „Ein wenig Gold“ ist keine prüfbare Zahl. | UNBEKANNT – Daniel liefert |
| Q-05 | **Bereits reisende Truppen blockieren; nur nicht gestartete offene Aufträge umrechnen.** | Wie unterscheidet der lokale Code „unterwegs“ von „laufendem Auftrag“? | VORSCHLAG; Hermes prüft |
| Q-06 | **Götterschutz blockiert Transfer während seiner Aktivität**; beim Recheck erneut prüfen. | Ist Schutz wirklich eine Transfersperre, oder nur Angriffs-/Verteidigungsschutz? | VORSCHLAG; Daniel bestätigt |
| Q-07 | **Warnung nur mit genehmigter Schwelle**; keine frei geschätzte Anzahl Stunden. | Welche maximale neue Laufzeit löst die Warnung aus? | UNBEKANNT – Daniel liefert |
| Q-08 | **Einheiten-Verbundsstufe aus einer eindeutigen vorhandenen Quelle**; bei fehlender Quelle kein stilles Level 0. | Wann entsteht/erhöht sich diese Stufe (Erstbau, Ausbildung oder Forschung)? | UNBEKANNT – Hermes/gegebenenfalls Daniel liefern |

## 8. Was ich nicht wissen kann

| Gegenstand | Sichere Grenze der Aussage | Benötigter Beleg |
|---|---|---|
| Lokaler Stand S-3/S-4/S-6 | **UNBEKANNT:** Öffentlicher GitHub-Code ist ausdrücklich älter als Hermes' lokaler Arbeitsstand. | Hermes: aktueller Commit/Dateistand und betroffene echte Funktionen. |
| Bestehende Testnamen und welche rot werden | **UNBEKANNT:** Die neuen W-IDs sind Vorschläge; kein alter Test wurde hier ausgeführt. | Hermes: Inventar der 113 lokalen Prüfdateien, jeweilige Behauptung, echte Testausgabe. |
| Exakter Speicherort globaler Forschungsstände | **UNBEKANNT:** Das vorgeschlagene JSON-Feld ist nicht als existierender Code nachgewiesen. | Hermes: Lesestelle, Schreibstelle, Save-/Load-Kontrakt. |
| Einheiten-Verbundsstufe | **UNBEKANNT:** Wie die Einheit ihre Verbundsstufe bekommt, ist im Auftrag nicht definiert. | Hermes: vorhandene Datenquelle oder Daniel: neue Regel. |
| Akademieausnahmen | **BELEGT:** Public `data/units.json` unterscheidet Stellmacher und Diebesgilde; **UNBEKANNT**, ob lokale M-5-Umsetzung dies schon behandelt. | Hermes: lokaler Produktionspfad je Einheitenrolle. |
| Transfer-Mana | **UNBEKANNT:** Neuer 500-Vorschlag und historischer 5.000-Wert widersprechen einander in der Auswahl. | Daniel: verbindlicher Preis je Transferart. |
| Gold und Kostenquelle bei Weltensprung | **UNBEKANNT:** Goldhöhe ist nicht genannt; Dorf-Ortslager ist meine Empfehlung. | Daniel: Betrag/Preisregel, Hermes: Lagerzugriff. |
| 24-Stunden-Sperre | **UNBEKANNT:** Historische Portalquelle nennt ein Mal je 24 Stunden; neuer Auftrag schweigt dazu. | Daniel: beibehalten oder streichen. |
| „Etwas unterwegs“ und Umrechnung | **UNBEKANNT:** Die zwei Auftragsformulierungen haben ohne Trennung widersprüchliche Folgen. | Hermes: lokale Auftragsarten und Wegsemantik; Daniel: gewählte Regel. |
| Langwegwarnung | **UNBEKANNT:** Schwelle und belastbare Berechnung nicht geliefert. | Daniel: Warnschwelle; Hermes: existierende Wegzeitfunktion. |
| Götterschutz | **UNBEKANNT:** Als möglicher neuer Blocker genannt, aber keine bestätigte Transferwirkung. | Hermes: bestehende Schutzregeln; Daniel: Freigabe. |
| Fälligkeit exakt beim Abriss | **UNBEKANNT:** Ereignisreihenfolge im lokalen Tick ist nicht eingesehen; hier nur ein deterministischer Entwurf. | Hermes: Tick-Reihenfolge und Gegenprobe. |
| Weltkarte und Koordinaten | **BELEGT im Auftrag:** sechs Namen, zwei zunächst bespielbare Welten, 20×20-Felder; **UNBEKANNT**: aktuelle lokale Feldbelegungsfunktion. | Hermes: lokale Weltkarten-/Belegungsprüfung. |
| Nachweis eines funktionierenden UI-Transfers | **UNBEKANNT:** Kein Fenster, keine lokale EXE und keine Spielstanddatei wurden ausgeführt. | Hermes: realer Windows-Fenstertest, Prozess-/Screenshotbelege, neue EXE-Prüfung. |

**Öffentliche Quellstellen (nur als Abgleich, nicht als lokale Code-Wahrheit):**

- [`src/forschung.py`](https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/src/forschung.py): Zeilen 6–25, 96–137, 172–199.
- [`src/einheiten.py`](https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/src/einheiten.py): Zeilen 16–30, 32–54, 70–80.
- [`data/units.json`](https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/data/units.json): Zeilen 300–303, 330–333, 713–726.
- [`data/welten.json`](https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/data/welten.json): Zeilen 18–27, 42–49.
- [`docs/AKTUELLER_STAND.md`](https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/docs/AKTUELLER_STAND.md): Zeilen 0–15; weist selbst auf abweichende lokale Entwicklungsstände hin.
