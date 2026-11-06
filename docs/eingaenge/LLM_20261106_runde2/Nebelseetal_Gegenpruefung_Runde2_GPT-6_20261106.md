# Nebelseetal Remake – Gegenprüfung des festen Ablaufs (Runde 2)

**Modell:** GPT-6  
**Datum:** 06.11.2026  
**Geprüfte Dokumentversion:** `V_0.0.3`, Stand 06.11.2026  
**Grundlage:** `Nebelseetal_LLM_Auftrag_Runde2_20261106.md`  
**Prüfgrenze:** Kein Repository-Zugriff. Aussagen über den Code werden daher nur als Wiedergabe der Angaben im Auftragsdokument behandelt. Wo die tatsächliche Implementierung entscheidend wäre, ist das ausdrücklich als Annahme oder Prüfbedarf gekennzeichnet.

---

## Teil 1 – Der schwächste Schritt

**Schritt 9 – B-2 Regelkreis, A/B-Urteil und Feedback.**

Dieser Schritt ist am fehleranfälligsten, weil er aus Messwerten eine Änderungsentscheidung ableitet. Ein formal korrektes A/B-Ergebnis kann trotzdem eine falsche Balancing-Entscheidung erzeugen: Zehn feste Startwerte sind reproduzierbar, aber nicht automatisch repräsentativ für unterschiedliche Spielverläufe. Außerdem kann eine einzelne Kennzahl deutlich besser werden, während sich ein für Menschen wichtiger Verlauf verschlechtert, der im Urteil nicht ausreichend abgebildet ist.

Der kritischste Punkt ist nicht die technische Ausführung des Vergleichs, sondern die Schlussfolgerung „angenommen“. Die Regel „mindestens 20 Prozent bessere Zielabweichung, keine andere Größe aus dem Korridor, erstes Gefecht nicht später“ kann einen lokalen Erfolg als Gesamtverbesserung einstufen. Die Schwellen 20 Prozent und 10 Prozent sind im Auftrag ausdrücklich **VORSCHLAG**; sie sind keine belegten Spielregeln.

**Konkreter Widerlegungsfall:** Eine Änderung verbessert auf denselben zehn Startwerten die Zielabweichung um mindestens 20 Prozent und bleibt bei den erfassten Nebenkennzahlen im Korridor. Ein anschließender, reproduzierbarer Spieltest mit einem bislang nicht in der A/B-Gruppe enthaltenen Startwert zeigt jedoch, dass der erste Krieger oder das erste Gefecht deutlich später erreicht wird oder eine Sackgasse entsteht. Dann wäre das Urteil „angenommen“ trotz grüner B-2-Wache sachlich falsch. Das wäre ein Gegenbeleg zur Aussagekraft des Urteils, nicht bloß ein technischer Testfehler.

## Teil 2 – Die schwächste Wache

Die folgende Liste nennt nur Wachen, deren derzeit beschriebene Form den jeweiligen Sachverhalt nicht zuverlässig beweist. Nicht aufgeführte Wachen bewerte ich anhand des Dokuments nicht als offensichtlich untauglich.

| Schritt | Schwache Wache | Warum sie nicht genügt | Ersatzprüfung |
|---|---|---|---|
| 1 | Quellwache, die in `_render_diplomacy` nach den Grenzwerten 40/60 und Gunstvergleichen sucht | Eine Textsuche kann eine anders formulierte Doppelberechnung übersehen und beweist nicht, dass die tatsächlich angezeigte Zeile den Status korrekt wiedergibt. | Diplomatie-Ansicht mit Gunst 0, 39, 40, 59, 60 und 100 rendern; den angezeigten Status jeweils gegen `diplomatie.status` prüfen. |
| 2 | Zwei identische Läufe mit gleichem Startwert und Stand | Identische Ausgaben beweisen nur Reproduzierbarkeit der verwendeten Eingaben. Sie beweisen nicht, dass alle spielbestimmenden Zufalls- und Zustandsquellen im Startzustand enthalten sind. | Einen Spielstand vollständig serialisieren, einschließlich Zufallszustand; daraus zwei getrennte Prozesse starten und den vollständigen Ergebniszustand sowie das Kennzahlenblatt vergleichen. |
| 3 | Quellwache, die nur prüft, ob beide `main.py`-Stellen `diplomatie.angriff_gesperrt` aufrufen | Der Aufruf kann vorhanden sein und trotzdem am falschen Zeitpunkt, mit falschem Ziel oder ohne Wirkung auf den Start des Auftrags erfolgen. | Je ein Integrationstest am echten Bot-Angriffs- und Diebstahlpfad: aktiver NAP, gültiges Ziel und auslösungsfähiger Bot; anschließend nachweisen, dass kein Auftrag und keine Beute entstehen. |
| 4 | Wache „höchstens ein laufender Auftrag je Bot und Ziel“ | Sie erkennt doppelte laufende Aufträge, aber nicht zwingend zwei nacheinander ausgelöste Angriffe oder eine doppelte Ankündigung nach erneutem Tick. | Rache-Auslösung und normale Bot-Taktik im selben Spieltick gleichzeitig aktivieren; danach genau einen Auftrag, genau eine Ankündigung und keinen zweiten Auslöser beim Folgetick nachweisen. |
| 5 | Quellwache, dass Overlay und Kern dieselbe Preisfunktion lesen | Ein gemeinsamer Funktionsaufruf beweist nicht, dass das Overlay den aktuellen Preis korrekt anzeigt oder eine abgelaufene Frist korrekt behandelt. | Ereignis mit verändertem Ertrag erzeugen und den Preis sowohl im Overlay als auch bei der Annahme ausgeben; beide Werte müssen identisch sein. Anschließend Annahme mit exakt ausreichendem Bestand prüfen. |
| 6 | Quellwache, dass Anzeige und `punkte.handelspunkte` denselben Wert liefern | Gleiche Übergabeparameter oder ein gemeinsamer Funktionsaufruf beweisen noch nicht, dass ein real abgeschlossener Vertrag den Erlös genau einmal bucht und der Spieler den aktualisierten Wert sieht. | Vollständiger Handelsabschluss ohne gesetzte Testwerte; danach Spielstand neu laden und den angezeigten Handelspunktestand mit einer unabhängigen Berechnung aus gebuchtem Erlös und Spielzeit vergleichen. |
| 7 | „Kein Totalverlust gegen den Drachen in 10 Läufen“ | Zehn Läufe können einen seltenen, aber folgenreichen Verlust übersehen. Außerdem beweist „kein Totalverlust“ nicht, dass die Entscheidung wirtschaftlich sinnvoll ist. | Dieselben festgelegten Startwerte mit und ohne Drachenprofil ausführen; Verluste, zurückkehrende Einheiten und `tag_erstes_gefecht` pro Lauf vergleichen. Ein Profil darf nicht nur deshalb bestehen, weil kein Totalverlust auftrat. |
| 8 | „Holz plus 10 Prozent verschiebt den Holzkorridor“ | Das beweist nur, dass eine Eingabe den Output beeinflusst. Es beweist nicht, dass der Korridor korrekt aus dem Idealplan berechnet wurde. | Einen kleinen, unabhängig von `balance_kreis.py` nachgerechneten Idealplan als Referenz verwenden und Idealwert, Untergrenze sowie Obergrenze gegen die erzeugte Datei prüfen. |
| 9 | Zwei gleiche Feedbackmeldungen erzeugen ein Bündel mit Zähler 2 | Das prüft weder die vorgesehene Schwelle von drei Meldungen noch, ob unterschiedliche Schlüssel fälschlich zusammengeführt werden. | Zwei gleiche Meldungen dürfen noch keinen Messauftrag erzeugen; die dritte gleiche Meldung muss ihn erzeugen. Eine Meldung mit abweichendem Schlüssel darf den Zähler des ersten Bündels nicht erhöhen. |

## Teil 3 – Die Zahl ohne Beleg

Die Reihenfolge bewertet das Risiko für den Spielverlauf, nicht die technische Schwierigkeit. Jede vorgeschlagene Messung verwendet dieselben festen Startwerte 1 bis 10, die im Ablauf für den A/B-Vergleich vorgesehen sind. Die genannten Schwellen selbst bleiben **VORSCHLAG**, solange kein Originalbeleg nachgetragen wird.

| Rang | Wert | Risiko für das Spielgefühl | Eine Messung vor dem Einbau |
|---:|---|---|---|
| 1 | Profilfaktoren 0,8 bis 1,2 – **VORSCHLAG** | Sie verändern mehrere Bot-Reaktionsschwellen und können dadurch gleichzeitig Angriffsdruck, Verluste und Entwicklungsrhythmus verschieben. | Für jeden der zehn festen Startwerte einen Lauf mit neutralem Profil und einen mit dem vorgesehenen Profil ausführen; `tag_erstes_haus`, `tag_erster_krieger`, `tag_erstes_gefecht` und Verluste paarweise vergleichen. |
| 2 | Drachen-Sicherheitsfaktor 1,5 – **VORSCHLAG** | Ein zu hoher Faktor kann Bots dauerhaft vom Drachen fernhalten; ein zu niedriger Faktor kann Armeen vernichten. Beides verändert die Weltreaktion deutlich. | Zehn feste Startwerte mit dem Faktor und ohne Drachenentscheidung vergleichen; als Messgröße die Quote der Drachenaufträge mit Verlusten sowie die zurückkehrende SK je Auftrag erfassen. |
| 3 | Rachetopf-Schwelle 3 – **VORSCHLAG** | Eine niedrige Schwelle kann häufige Vergeltung erzeugen; eine hohe Schwelle kann die angekündigte Reaktion praktisch unsichtbar machen. | In zehn festen Startwerten die Spieltage vom ersten Rachegrund bis zur Ankündigung und vom ersten Grund bis zum Angriff messen. |
| 4 | Vertragsbruch kostet 20 Gunst – **VORSCHLAG** | Der Abzug kann einen Bot weit unter die neutrale Zone drücken und damit mehrere Folgewirkungen auslösen. Er ist besonders kritisch nahe der Schwelle 40. | Mit denselben zehn Startwerten gezielt einen Vertragsbruch bei Gunst 40 auslösen und die anschließenden Gunstwerte sowie die Zahl weiterer Vertrags- und Racheauslöser messen. |
| 5 | NAP-Dauer 3 Spieltage – **VORSCHLAG** | Ein langer Pakt kann den Konfliktdruck aus einer Partie nehmen; ein kurzer Pakt kann kaum Schutzwirkung entfalten. | In zehn festen Startwerten die Zahl verhinderter Angriffe und Diebstähle während der Laufzeit sowie die Zeit bis zum nächsten erfolgreichen Angriff nach Ablauf messen. |
| 6 | Ereignisfrist 2 Spieltage – **VORSCHLAG** | Eine Frist kann so kurz sein, dass Entscheidungen im normalen Spielablauf leicht verpasst werden, oder so lang, dass Ereignisse die Partie unnötig blockieren. | Für zehn feste Startwerte messen, welcher Anteil der erzeugten Ereignisse vor Fristablauf tatsächlich geöffnet und entschieden wird. |
| 7 | Gunständerung plus/minus 5 – **VORSCHLAG** | Einzelne Ereignisse können bei Bots nahe 40 oder 60 einen Status- oder Vertragswechsel auslösen; fern der Grenzen bleibt die Änderung dagegen kaum spürbar. | Für zehn feste Startwerte die Zahl der Statuswechsel und Vertragsabbrüche messen, die ausschließlich durch eine einzelne Ereignisentscheidung ausgelöst werden. |
| 8 | Gunst-Startwert 50 – **VORSCHLAG** | Er bestimmt die Ausgangslage aller Bots. Ein anderer Wert könnte Diplomatie zu Beginn zu leicht oder zu schwer machen; der direkte Effekt ist aber weniger drastisch als bei Schwellen und Faktoren. | Für zehn feste Startwerte die Zeit bis zum ersten möglichen Vertrag und die Zahl der Bots je Status bei Spielbeginn und nach dem ersten Spieltag vergleichen. |
| 9 | Sollkurven-Bänder 0,7 und 1,1 – **VORSCHLAG** | Sie können falsche Warnungen oder falsche Entwarnung im Werkzeug erzeugen. Das Risiko betrifft zunächst die Balancing-Entscheidung, nicht unmittelbar eine laufende Partie. | Für zehn feste Startwerte prüfen, wie viele unveränderte Referenzläufe innerhalb des Korridors liegen und wie viele nachweislich problematische Läufe trotzdem als unauffällig gelten. |

## Teil 4 – Die fehlende Abhängigkeit

**Schritt 7 muss zusätzlich von Schritt 4 abhängen.** In der Tabelle ist für die Bot-Lücken Schritt 5 genannt, nicht aber der Rachetopf aus Schritt 4.

Der Grund: Schritt 7 ergänzt Bot-Entscheidungen und Aufrufer für Drachen, Spionage und Reaktionen. Damit wird weiteres Verhalten an den vorhandenen Bot-Angriffsweg angeschlossen. Schritt 4 führt gleichzeitig einen zusätzlichen Auslöser für einen Bot-Angriff ein. Ohne die bereits fertige Rachelogik kann Schritt 7 zwar isoliert grün sein, aber die Kombination aus normaler Bot-Taktik und Racheauslöser bleibt unbewiesen. Das Risiko eines doppelten oder zeitlich widersprüchlichen Angriffs ist damit nicht vollständig abgedeckt.

**Notwendige Ergänzung der Abhängigkeit:** Schritt 7 hängt von Schritt 4 und Schritt 5 ab. Die vorhandene Wache aus Schritt 4 zur Begrenzung laufender Aufträge muss nach der Integration aus Schritt 7 erneut gegen gleichzeitig ausgelöste Bot-Taktik und Rache geprüft werden.

Die übrigen besonders genannten Reihenfolgen sind grundsätzlich tragfähig, aber nicht vollständig beweiskräftig:

- **Kennzahlenblatt vor Rachetopf:** richtig. Ohne Vorher-Messung lässt sich nicht erkennen, ob die Rachemechanik den Entwicklungsverlauf verändert. Voraussetzung ist allerdings, dass der Zufallszustand tatsächlich Teil des reproduzierbaren Startzustands ist.
- **Verträge vor Rachetopf:** richtig. Der Racheauslöser muss einen aktiven NAP als Sperre kennen. Andernfalls wird ein bereits geschützter Spieler trotzdem angegriffen.
- **Bot-Lücken nach Ereignissen:** als Reihenfolge plausibel, weil beide an Botverhalten und Diplomatie anschließen. Die zusätzliche Abhängigkeit zu Schritt 4 bleibt trotzdem erforderlich.
- **E2E-Ketten am Ende:** sinnvoll, weil sie die fertig integrierten Wege prüfen. In der Abhängigkeitstabelle steht bei Schritt 10 allerdings „3 bis 10“; das enthält Schritt 10 selbst und ist als Selbstabhängigkeit fehlerhaft. Gemeint sein kann nur „3 bis 9“. Außerdem müssen die E2E-Ketten nach jeder späteren Änderung an einem bereits abgedeckten Weg erneut laufen; ein einmaliger Lauf am Ende ersetzt keine Regression.

## Teil 5 – Der Schritt, der weg kann

**Keiner der Schritte 1 bis 13 kann nach dem vorliegenden Ablauf ohne Schaden für den Gesamtauftrag gestrichen werden.**

Die Schritte 1 bis 7 liefern die vorgesehenen Diplomatie- und Botmechaniken. Die Schritte 8 und 9 bilden die notwendige Mess- und Entscheidungsgrundlage für Balancing. Die Schritte 10 bis 13 decken die ausdrücklich benannten Qualitätssicherungsziele A-1, A-2, A-6 und A-7/A-5 ab. Insbesondere wäre das Streichen der Kennzahlenmessung kein folgenloses Kürzen: Dann fehlte die belastbare Vorher-Basis für die Rache- und Botänderungen sowie für den Regelkreis.

Einzelne Wachen können verbessert werden, wie in Teil 2 beschrieben. Das ist aber kein Beleg dafür, dass der zugehörige Schritt entfallen kann. Auch Schritt L ist kein Spielmechanikschritt, sondern ein ausdrücklich verlangter Dokumentations- und Übergabeschritt; er ist deshalb nicht mit den 13 Umsetzungsschritten gleichzusetzen.

## Teil 6 – Die Wechselwirkung, die keiner sieht

**Ereignisentscheidung und Nichtangriffspakt können sich gegenseitig auslösen.**

Ein Bot mit Gunst 40 kann einen NAP besitzen, weil das Angebot ab Gunst 40 vorgesehen ist. Wird anschließend ein Ereignis abgelehnt oder läuft es ab, sinkt die Gunst um 5 (**VORSCHLAG**). Der Bot fällt damit unter 40. Laut Vertragsregel bricht der NAP dann; der Vertragsbruch kostet weitere 20 Gunst und erhöht den Rachetopf um 1 (**beides VORSCHLAG**). Aus einer einzelnen Ereignisentscheidung werden somit ein Vertragsbruch und ein zusätzlicher Rachegrund. Das kann unmittelbar den Weg zur Racheankündigung verkürzen.

**Kleinste abfangende Wache:** Einen Bot mit Gunst 40 und aktivem NAP verwenden, ein Ereignis erzeugen und es ablaufen lassen. Danach in einem einzigen Integrationstest prüfen: Ereignisabzug genau einmal, NAP genau einmal beendet, Vertragsbruchabzug genau einmal, Rachetopf genau einmal erhöht. Ein weiterer Tick darf keine dieser Buchungen wiederholen. Die konkreten Gunstabzüge und die Racheerhöhung bleiben dabei als **VORSCHLAG** gekennzeichnet; der Test prüft zunächst die konsistente Umsetzung der beschlossenen Werte, nicht deren spielerische Richtigkeit.

## Teil 7 – Die Aufbauzeit

Das Ziel ist nicht, die Aufbauzeit künstlich zu verkürzen. Sie soll als Messgröße erhalten bleiben, damit neue Mechaniken den vorgesehenen Spielfluss nicht unbemerkt verschlechtern. Die Einordnung im Ablauf ist an drei Stellen zu pauschal:

| Schritt | Bewertung des angegebenen Effekts |
|---|---|
| 1 – Gunst und Status | **Richtig: keiner.** Eine reine Zahl ohne Wirkung verändert die Aufbauzeit nicht. |
| 2 – Kennzahlenblatt | **Richtig: keiner.** Das Werkzeug misst, greift aber nicht in die Partie ein. |
| 3 – Verträge | **Zu pauschal: „senkt sie“.** Ein NAP kann Angriffe und Diebstahl verhindern und dadurch Verluste vermeiden. Er ist aber optional und setzt ausreichende Gunst voraus. Für eine Partie ohne aktiven NAP gibt es keine Senkung. Der Effekt muss als bedingt ausgewiesen werden. |
| 4 – Rachetopf | **Hier widerspreche ich ausdrücklich: „erhöht den Druck, nicht die Dauer“ ist nicht belegt.** Ein ausgelöster Angriff kann Einheiten, Rohstoffe oder Zeit kosten und dadurch Meilensteine verzögern. Der Druck ist gerade ein möglicher Weg zu längerer Aufbauzeit. |
| 5 – Ereignisse | **Hier widerspreche ich ebenfalls: „neutral“ gilt nicht für angenommene Ereignisse.** Haug und Silra verlangen Ressourcen; Grom ist noch nicht endgültig festgelegt. Eine Annahme kann einen Bau- oder Produktionsschritt verzögern. Die Ablehnungsmöglichkeit verhindert einen Zwang, macht die angenommene Variante aber nicht neutral. |
| 6 – Handelspunkte | **Richtig: kein unmittelbarer Effekt durch diesen Schritt.** Es wird eine fehlende Buchung und Anzeige angeschlossen; der bestehende Handelsweg wird nicht neu gestaltet. |
| 7 – Bot-Lücken | **Plausibel, aber noch unbewiesen: kann sie heben.** Vorsichtigere Botentscheidungen können den Druck und damit Verluste reduzieren; Spionage und veränderte Reaktionen können den Konfliktverlauf auch verzögern. Die Richtung muss aus den Kennzahlen kommen. |
| 8 – Sollkurve | **Richtig: keiner.** Die Sollkurve ist ein Werkzeug und ändert keine Spielmechanik. |
| 9 – Regelkreis | **Richtig: keiner, solange nur gemessen und verglichen wird.** Erst eine später übernommene Datenänderung kann die Aufbauzeit verändern. |
| 10 – E2E-Ketten | **Richtig: keiner.** Tests dürfen den Produktions- oder Spielablauf nicht verändern. |
| 11 – AST-Quellwache | **Richtig: keiner.** Die Wache prüft Quellstruktur. |
| 12 – Sammellauf | **Richtig: keiner für die Partie.** Parallelität kann die Prüflaufzeit ändern, nicht die Spielaufbauzeit. |
| 13 – Schlussprüfung | **Richtig: keiner.** Die Prüfung verändert keine Spielwerte. |

Die entscheidenden Korrekturen sind damit Schritt 4 und Schritt 5. Bei Schritt 3 ist die Richtung plausibel, aber nur für Partien mit tatsächlich wirksamem Vertrag. Bei Schritt 7 ist die angegebene Möglichkeit einer längeren Aufbauzeit angemessen vorsichtig; sie darf nicht ohne Messung als feststehende Wirkung behandelt werden.

## Teil 8 – Die drei Prüfungen, die den Ablauf am schnellsten widerlegen

| Was tun? | Was messen? | Welches Ergebnis kippt den Ablauf? |
|---|---|---|
| Einen Bot mit Gunst 40 und aktivem NAP ein Ereignis ablehnen oder ablaufen lassen. | Gunstbuchungen, Vertragsstatus und Rachetopf vor und nach dem Ereignis sowie nach einem weiteren Tick. | NAP bleibt trotz Gunst unter 40 aktiv, eine Buchung erfolgt mehrfach oder der Rachetopf wird nicht konsistent erhöht. Dann ist die Wechselwirkung aus Teil 6 nicht korrekt modelliert. |
| Einen festen Startwert mit aktivierter Rachemechanik bis zum ersten Bot-Angriff und anschließend bis zum nächsten Entwicklungsmeilenstein spielen; denselben Startwert ohne Rache als Vergleich verwenden. | `tag_erstes_haus`, `tag_erster_krieger`, `tag_erstes_gefecht`, Verluste und Wiederaufbauzeit. | Die Rachemechanik verzögert einen Meilenstein oder erzeugt einen Wiederaufbauverlust, obwohl der Ablauf behauptet, sie erhöhe nur den Druck und nicht die Dauer. Dann ist die Effekteinstufung von Schritt 4 widerlegt. |
| Den B-2-Regelkreis mit denselben zehn festen Startwerten ausführen und danach einen bislang nicht in der A/B-Gruppe enthaltenen reproduzierbaren Startwert gegenprüfen. | A/B-Urteil und die Meilensteine des zusätzlichen Startwerts, insbesondere erster Krieger und erstes Gefecht. | B-2 nimmt eine Änderung an, während der zusätzliche Startwert eine deutliche Verschlechterung oder Sackgasse zeigt. Dann ist die Aussagekraft der Annahmeregel mit der vorgesehenen Stichprobe nicht ausreichend. |

---

## Abschließende Einordnung

Der Ablauf ist als kontrollierte, schrittweise Umsetzung grundsätzlich nachvollziehbar. Die größten fachlichen Risiken liegen nicht in fehlenden Modulen, sondern in Übergängen zwischen Mechaniken und in der Aussagekraft der Mess- und Annahmeregeln.

Vor allem müssen die Wechselwirkung aus Ereignis und NAP sowie die Kombination aus Racheauslöser und normaler Bot-Taktik ausdrücklich geprüft werden. Außerdem darf „kein Einfluss auf die Aufbauzeit“ nicht aus der bloßen Optionalität einer Mechanik abgeleitet werden: Angenommene Ressourcenkosten und tatsächlich ausgeführte Vergeltungsangriffe können den Fortschritt sehr wohl verzögern.

Es wurden keine neuen Zahlen als belegte Spielregeln ausgegeben. Wo der Auftrag keine Quelle nennt, bleiben die Werte ausdrücklich **VORSCHLAG**. Eine Repository-Prüfung oder ein Nachweis über die tatsächliche Implementierung wurde nicht vorgenommen.
