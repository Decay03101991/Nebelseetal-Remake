# Antwort auf: NEBELSEETAL REMAKE – Wissens- und Auftragsdokument

**Modell:** Claude Opus 5.5 (Anthropic) · **Datum:** 06.11.2026 · **Teile:** 1 (diese Datei)
**Fassung:** 2 (überarbeitet, mit Teil 7a *Zusätzlicher Content, weil ich es kann*)
**Bezugsdokument:** `Stand 06.11.2026, V_0.0.3`, Kopf-Commit `1c5cb73`

> **Vorsicht (Abschnitt 13, wörtlich übernommen):** Diese Antwort wird nicht direkt eingebaut. Zwei bis drei Modelle bearbeiten dieselbe Datei; danach werden die Antworten gegeneinander abgeglichen, und die nach euren Prinzipien beste Methode wird integriert. **Jede Zahl aus dieser Antwort ist bis zum Beleg ein VORSCHLAG.** Vier Prüffragen vor jeder Übernahme: Passt es zur Mechanik? Ist die Zahl belegt? Hilft es dem Spielgefühl? Braucht es ein neues Bauteil, und wenn ja, warum kein vorhandenes? Alte Abläufe werden nicht stillschweigend ersetzt.

**Kennzeichnung in dieser Antwort:**
- **[DOK x.y]**: Die Zahl steht im Auftragsdokument, Abschnitt x.y (dort mit Quelle).
- **[GERECHNET]**: Ich habe sie aus Dokumentzahlen abgeleitet; der Rechenweg steht daneben.
- **[VORSCHLAG]**: Ohne Beleg. Sie geht an Daniel.
- **[UNSICHER]**: Ich kenne den Code nicht und habe die Stelle nur aus dem Dokument erschlossen.

Ich hatte keinen Zugriff auf Code, Daten oder Handbuch. Funktionsnamen, die nicht im Dokument stehen, sind Namensvorschläge und als solche markiert.

---

## Teil 1 – Verständnis in eigenen Worten

**Das Spiel.** Nebelseetal Remake ist eine lokale Neuauflage eines Browser-Aufbauspiels: Python 3.14, tkinter, JSON-Spielstand, offline. Ein Spieler tritt gegen fünf Bots mit eigener Wirtschaft an, dazu kommen ein Drache und Ruinen auf sechs Welten. Es gibt keinen Sieg. Das Ziel sind Punkte (Krieg, Forschung, Handel, Gesamt = (Krieg + Forschung) / 2), vier Auszeichnungen und Ruhmstufen (0/10/40/160).

**Zeitbasis.** Die Spieluhr läuft mit Faktor x180. Ein Spieltag hat 28.800 Spielsekunden und dauert 8 echte Minuten. Alles Fachliche rechnet in Spielsekunden.

**Kernkreis.** Gründen → produzieren (Gelände × Gebäude, ortsgebundene Lager) → forschen (Bibliothek → Baukunst → Goldmine/Farm/Kriegerakademie) → ausrüsten (Waren aus Werkstatt und Rezepten) → ausbilden (Warteschlange je Ort, kostet Siedler) → bewegen (Aufträge, der Rückweg kostet doppelt) → kämpfen (`kampf.fuehre_schlacht`: Vorrunde, Wall, Phasen, Beute, Flucht) → punkten. Der Tick bucht Produktion, Versorgung (8 Nahrung je Einheit und Tag), Warteschlangen, den Nachrichtenablauf und die Bot-Züge. Jede Buchung ist atomar.

**Wo gerechnet wird.** Gerechnet wird in den Fachmodulen in `src/`, die Zahlen kommen ausschließlich aus `data/*.json`. `main.py` (`GameState`, `NebelseetalApp`) liest und zeichnet nur. Die Anzeige ruft dieselbe Funktion auf wie der Kern (Regel F-04). Belegte Fälle dafür: Verwundetenheilung (`src/verwundete.py` ↔ Kaserne), Ruhm-Balken (`data/ruhm.json`) und Mauerreparatur (V-1).

**Wo ich unsicher bin:**
- **[UNSICHER]** wo genau der Handelsweg (`spieloekonomie.handel_start`) Handelspunkte bucht und warum er im Spielbetrieb unerreichbar ist (fehlende Ansicht, fehlende Voraussetzung oder fehlende Punktebuchung?).
- **[UNSICHER]** wie Bot-„Takte" intern geplant werden und ob ein Bot-Angriff heute schon durch eine zentrale Sperrfunktion läuft. Für den Götterschutz ist das so beschrieben, eine Funktionssignatur kenne ich nicht.
- **[UNSICHER]** wie V-4 aus den Feldzahlen auf die Tagesproduktion kommt (siehe Einwand E-3).

---

## Teil 2 – Einwände und offene Punkte

| Nr. | Einwand | Beleg | Folge |
|---|---|---|---|
| E-1 | **Der Rachetopf zündet vor dem ersten Gefecht.** +1 je Spieltag ohne Kontakt und Schwelle 3 ergeben einen angekündigten Angriff ab Spieltag 3. Das erste Gefecht kommt erst nach 8 bis 12 Spieltagen. | DOK 7.2, 4.12 | Der Spieler wird angegriffen, bevor er sich verteidigen kann, und die Aufbauzeit steigt. Lösung in Schnitt 3: Der Kontakt-Zuwachs ruht, solange Götterschutz gilt, die Tageszählung beginnt also erst nach dem ersten Kriegspunkt. |
| E-2 | **„Rache greift ab 99 SK" vermischt zwei Größen.** Der Rachetopf zählt Ereignisse, 99 SK ist eine Armeestärke. | DOK 7.2, 7.3 V-5 | Mein Vorschlag: Topf ≥ 3 löst die Ankündigung aus. Ausgeführt wird der Angriff erst, wenn die Bot-Armee ≥ 99 SK Fußtruppen hat. Beide Werte stehen in `data/diplomatie.json`. |
| E-3 | **V-4 lässt sich aus 4.1 nicht nachrechnen.** Stein 1.026 ≈ Berg 10,7 × 4 × 24 = 1.027, dort ist Hügel ausgelassen. Holz 1.980 ≈ Wald 20,6 × 4 × 24 = 1.978, dort ist Steppe ausgelassen. Nahrung 1.720 und Gold 128 passen zu keiner Kombination aus 4.1 (Gold auf Berg allein wären 10,7 × 3 × 24 = 770). | [GERECHNET] aus DOK 4.1, 7.3 | Haugs Tribut (64 Gold) und Silras Preis (12 Gold) hängen an Gold 128. Bevor S4 Teil 3 gebaut wird, muss `s0_tabellen.py` den Rechenweg für Gold und Nahrung ausgeben. Wahrscheinlich ist eine Gebäudebelegung eingerechnet. |
| E-4 | **Die Grenze für A-6 bricht durch die neuen Wachen.** 1.346 s für 183 Dateien ergeben ≈ 7,36 s je Datei. Schon 8 neue Dateien führen zu ≈ 1.405 s und damit über 1.400 s. Außerdem schreibt A-6 genau „183 Dateien, 7.495 Prüfungen" fest. | [GERECHNET] DOK 6, 8 | Umformulieren: „≥ 183 Dateien, ≥ 7.495 Prüfungen, 0 rot, Dauer ≤ 1.400 s + 8 s je neuer Datei" [VORSCHLAG]. Alternativ bekommt `sammellauf.py` einen Parallelbetrieb. |
| E-5 | **Bruchteile im Kern widersprechen der Rundungsregel.** Ein Krieger heilt für 0,75 Pferde, der Handkarren für 11,25 je Posten. Die Regel 5.3 deckelt Ressourcen mit `int()`/`floor()`. | DOK 4.11, 5.3, 7.3 V-2 | Für die Buchung muss festgelegt werden, ob abgerundet wird (0 Pferde, die Heilung wäre also gratis) oder ob ein Rest am Ort mitgeführt wird. Mein Vorschlag: Buchung = `math.ceil` je Posten bei Heilung, damit es nie gratis wird. Ein Zahlenwert ist das nicht, nur eine Regel. Daniel muss entscheiden. |
| E-6 | **Der Portalweg ist innerhalb einer Partie unerreichbar.** 5.000 Mana / 120 je Tag ergeben 41,7 Spieltage, eine Partie dauert 8 bis 12. | DOK 4.8, 4.12 | Für A-3 ist das zulässig, weil das Portal kein Pflichtweg bis zum ersten Gefecht ist. A-1 verlangt aber eine E2E-Kette je Weg. Vorschlag: Das Portal läuft in A-1 als Langweg mit eigener Frist (60 Spieltage, Automatenspiel ohne Fenster). Ich ändere keine Zahl. |
| E-7 | **Handelspunkte zählen nicht in die Gesamtpunkte.** Gesamt = (Krieg + Forschung) / 2. Selbst wenn der Handel repariert ist, bleibt er ohne Einfluss auf Ruhm, sofern Ruhm an Gesamt hängt. | DOK 4.7 | Das ist offen, und ich ändere die Formel nicht. Wenn Handel ein Weg sein soll, muss er über eine eigene Auszeichnung belohnt werden. Ob eine der vier Auszeichnungen Handel ist, steht nicht im Dokument **[UNSICHER]**. |
| E-8 | **Kleine Verluste erzeugen keine Verwundeten.** Bei 30 % abgerundet bleiben Verluste von 1 bis 3 je Typ ohne Verwundete. | DOK 4.11 | So beabsichtigt? Früh im Spiel sind fast alle Verluste klein, die Mechanik ist dann unsichtbar. Das ist nur ein Hinweis, keine Änderung. |
| E-9 | **Die Datierung ist uneinheitlich.** Der Stand ist auf den 06.11.2026 datiert, `S0_TABELLEN_20261107.md` und `ABLAUF_20261107.md` tragen den 07.11. | DOK Kopf, 4, 4.12 | Nur fürs Register relevant, kein fachlicher Fehler. |
| E-10 | **Herrscher (160) liegt außerhalb jeder gemessenen Partie.** 160 / 3,3 ergeben ≈ 48 Spieltage. | [GERECHNET] DOK 7.3 V-3 | Für eine Langzeitstufe ist das in Ordnung. Ein Spielgefühlsrisiko entsteht nur, wenn der Balken sichtbar „steht". Nach dem ersten Kennzahlenblatt sollte das gemessen werden (Teil 4). |

---

## Teil 3 – Schnitte

Querverweis: Schnitte 1–6 setzen voraus, dass Determinismus (Z-2.5) und der Lade-Helfer (Z-2.6) aus Teil 7a entweder gebaut oder bewusst verworfen sind; ohne Z-2.5 ist jede A/B-Messung in Teil 4 nur eingeschränkt gültig.

Grundsatz: Es gibt **ein** neues Modul (`src/diplomatie.py`), weil Gunst, Rachetopf, Verträge und Ereignisse heute keine Fachdatei haben. `botkern.py` ist Wirtschaft, `bottaktik.py` ist Kampftaktik. Würde man es dort einbauen, mischten sich Themen. Alles andere geht in vorhandene Dateien.

### Schnitt 1 – S4 Teil 1: Gunst und Status

| Feld | Inhalt |
|---|---|
| Ziel | Jeder Bot hat eine Gunst von 0 bis 100 mit Status, gespeichert und angezeigt aus einer Funktion. |
| Dateien | neu: `src/diplomatie.py`, `data/diplomatie.json`, `tests/test_diplomatie_gunst.py`; geändert: `main.py` (`bot_als_dict`/`bot_aus_dict`, Diplomatie-Ansicht) |
| Änderung | `diplomatie.gunst_setzen(bot, wert) -> int` (Deckel 0..100, `int`), `diplomatie.gunst_aendern(bot, delta, grund) -> int`, `diplomatie.status(gunst) -> str` (Schlüssel `feindselig`/`wachsam`/`freundlich`). Die Felder `gunst` und `rache` am Bot werden nur über `bot_als_dict`/`bot_aus_dict` gelesen und geschrieben, fehlende Schlüssel bekommen den Standardwert. Die Anzeigezeile ruft `status()` auf. Schalter `aktiv`. |
| Daten | Grenzen 39/40 und 59/60 [DOK 7.1]; Start-Gunst 50 [VORSCHLAG: Mitte von „wachsam", also neutral]. Auslöser: Geschenk +1 je 100 Rohstoffeinheiten Gegenwert, Deckel +10 je Geschenk [VORSCHLAG]; eigener Angriff auf den Bot −15 [VORSCHLAG]; Vertragsbruch −20 [DOK 7.2]. |
| Wache | (1) Setzen auf −5 ergibt 0, auf 130 ergibt 100. (2) `status(39)=feindselig`, `status(40)=wachsam`, `status(59)=wachsam`, `status(60)=freundlich`, dazu 0 und 100. (3) Ein alter Spielstand ohne `gunst` lädt mit 50, ohne dass geschrieben wird (Datei-Hash vorher = nachher). (4) Quellwache: Die Ansicht in `main.py` enthält keine Zahl 40/60 und keinen Vergleich auf `gunst`, nur den Aufruf `diplomatie.status`. (5) Der Rachetopf ist nach Gunständerungen unverändert. |
| Fertig-Kriterium | 5 von 5 Wachen grün, voller Sammellauf 0 rot |
| Aufbauzeit-Effekt | unverändert, weil die Gunst ohne Aktion keine Wirkung hat |
| Ablösung | keine |
| Risiko | Ein `asdict()` lässt Felder weg (Regel 5.3). Wache (3) mit Speichern→Laden→Speichern fängt das. |

### Schnitt 2 – S4 Teil 2a: Verträge (Nichtangriffspakt, Handelsabkommen, Durchmarsch-Anzeige)

| Feld | Inhalt |
|---|---|
| Ziel | Der Nichtangriffspakt sperrt Bot-Angriffe im Kern über dieselbe Sperre wie der Götterschutz. |
| Dateien | `src/diplomatie.py`, `data/diplomatie.json`, `src/versorgungsschutz.py` (Sperrprüfung erweitern), `main.py` (Knöpfe), `tests/test_diplomatie_vertraege.py` |
| Änderung | `vertrag_anbieten(state, bot, art) -> (ok, grund)`, `vertrag_aktiv(state, bot, art, jetzt) -> bool`, `vertraege_tick(state, jetzt)` (Ablauf, Bruch unter 40). Die vorhandene Angriffssperre (Götterschutz-Pfad, Name **[UNSICHER]**) fragt zusätzlich `vertrag_aktiv(..., "nap")` ab, für Angriff **und** Diebstahl (4.6: dieselben Gates). Ein Handelsabkommen ruft `spieloekonomie.handel_start` auf, einen eigenen Handelsweg gibt es nicht. Durchmarsch ist nur ein Anzeigetext ab Gunst 60. |
| Daten | NAP ab Gunst 40, Dauer 3 Spieltage = 86.400 Spielsekunden, Bruch −20 Gunst und +1 Rache [DOK 7.2]; Durchmarsch ab 60 [DOK 7.2] |
| Wache | (1) Bei aktivem NAP startet der Bot-Angriff nicht, Grund `nap`. (2) Dasselbe gilt für den Diebstahl. (3) Der NAP läuft nach genau 86.400 s ab, bei 86.399 s ist er noch aktiv. (4) Fällt die Gunst auf 39, bricht der Pakt; die Gunst sinkt um genau 20, die Rache steigt um genau 1. (5) Ein NAP-Angebot bei Gunst 39 wird abgelehnt. (6) Durchmarsch: Die Quellwache findet keine Mechanikwirkung (kein Aufruf in `auftraege`). (7) Ein alter Spielstand ohne `vertraege` lädt. |
| Fertig-Kriterium | 7 von 7 grün, Sammellauf 0 rot |
| Aufbauzeit-Effekt | senkt oder lässt gleich, weil ein NAP Störungen im Aufbau verhindert |
| Ablösung | keine; die Götterschutz-Sperre bleibt und bekommt eine weitere Bedingung |
| Risiko | Wird die Sperre an zwei Stellen geprüft, ist F-04 verletzt. Die Quellwache (Wache 1/2 über die Kernfunktion, nicht über die Ansicht) fängt das. |

### Schnitt 3 – S4 Teil 2b: Rachetopf und angekündigter Angriff

| Feld | Inhalt |
|---|---|
| Ziel | Bots reagieren auf den Spieler: Niederlagen und Ignorieren führen zu einem angekündigten Angriff. |
| Dateien | `src/diplomatie.py`, `data/diplomatie.json`, `src/bot_angriffsplanung.py` (Ziel- und Zeitwahl liest `rache_bereit`), `data/nachrichten.json` (Typ `ankuendigung`), `tests/test_diplomatie_rache.py` |
| Änderung | `rache_buchen(bot, grund)`, `rache_tag(state, bot, jetzt)` (nur wenn kein Götterschutz besteht, siehe E-1, und kein Kontakt am Spieltag), `rache_bereit(bot, armee_sk) -> bool` (Topf ≥ Schwelle **und** SK ≥ 99). Nach der Ankündigung folgt die Nachricht `ankuendigung` mit Vorlauf, dann der Angriff über den vorhandenen Raubzugweg. Ein Bot-Sieg setzt den Topf auf 0. „Kontakt" heißt Handel, Geschenk, Vertrag oder Kampf mit diesem Bot. |
| Daten | +1 je Niederlage, +1 je Tag ohne Kontakt, Schwelle 3, 99 SK [DOK 7.2, V-5]; Vorlauf der Ankündigung 1 Spieltag [VORSCHLAG: entspricht der Berichtsfrist 4.10, der Spieler sieht sie also sicher]; Senkung nach Bot-Sieg auf 0 [VORSCHLAG, das Dokument sagt nur „senkt"]. |
| Wache | (1) Unter Götterschutz bleibt der Topf nach 5 Tagen bei 0. (2) Ohne Schutz und ohne Kontakt steht der Topf nach 3 Tagen bei 3. (3) Bei Topf 3 und SK 98 wird nicht angegriffen, bei SK 99 schon. (4) Jede Ankündigung erzeugt genau eine Nachricht `ankuendigung`, vor dem Angriff. (5) Nach einem Bot-Sieg ist der Topf 0. (6) Ein aktiver NAP blockiert trotz Topf ≥ 3. (7) Ein alter Spielstand ohne `rache` lädt. |
| Fertig-Kriterium | 7 von 7 grün; Automatenspiel 12 Tage: Spieltag des ersten Gefechts nicht früher als vorher (Kennzahlenblatt) |
| Aufbauzeit-Effekt | lässt gleich, durch die Schutz-Kopplung (E-1); ohne Kopplung würde er sie heben |
| Ablösung | Die heutige Zeitwahl des Raubzugs bleibt. Der Rachetopf ist ein zusätzlicher Auslöser, kein Ersatz. |
| Risiko | Doppelter Angriff (Takt plus Rache). Wache: höchstens ein laufender Auftrag je Bot und Ziel. |

### Schnitt 4 – S4 Teil 3: Ereignisse (Haug, Grom, Silra)

| Feld | Inhalt |
|---|---|
| Ziel | Drei Bot-Ereignisse mit zwei Tagen Frist über das vorhandene Overlay, mit Gunstwirkung. |
| Dateien | `src/diplomatie.py`, `data/ereignisse.json` (Texte und Zahlen), `story`-Overlay (vorhanden, `main.py` ruft es nur auf), `tests/test_diplomatie_ereignisse.py` |
| Änderung | `ereignis_erzeugen(state, bot, art, jetzt)`, `ereignis_annehmen(state, id) -> (ok, grund)` (atomar: fehlt der Bestand am **Ort**, wird nichts gebucht), `ereignisse_tick` (Ablauf). Annehmen bringt Gunst +, Ablehnen oder Ablauf Gunst −. |
| Daten | Frist 2 Spieltage = 57.600 s; Haug 990 Holz oder 64 Gold; Grom 5 Werkzeuge gegen 20 Eisen (Tausch 1:4 ist VORSCHLAG im Dokument); Silra 12 Gold, mindestens 1 [DOK 7.2, V-4, aber E-3 beachten]. Gunst bei Annahme +5, bei Ablehnung −5, Häufigkeit 1 Ereignis je Bot und 3 Spieltage [alles VORSCHLAG]. Hinweis: Im Dokument heißt die Ware „Eisen", der Rohstoff „Metall". Ob „Eisen" eine der 17 Waren ist, ist **[UNSICHER]**. Das muss in `items.json` geprüft werden. |
| Wache | (1) Ablauf nach 57.600 s mit Gunst −5, bei 57.599 s noch offen. (2) Annahme mit 989 Holz: abgelehnt, Bestand unverändert. (3) Annahme Holz: genau 990 abgebucht, Gunst +5. (4) Silra bei Gold-Ertrag 5: Preis 1 (Mindestwert). (5) Overlay und Kern lesen dieselbe Preisfunktion (Quellwache). (6) Ein alter Spielstand ohne `ereignisse` lädt. |
| Fertig-Kriterium | 6 von 6 grün, und E-3 ist geklärt (Rechenweg Gold steht in S0) |
| Aufbauzeit-Effekt | hebt leicht, wenn Tribut gezahlt wird; abgemildert, weil Ablehnen möglich ist. Die Messung im A/B-Lauf geschieht über das Kennzahlenblatt. |
| Ablösung | keine |
| Risiko | Preis aus einer festen Zahl statt aus dem Ertrag. Wache (4) fängt das. |

### Schnitt 5 – Handelspunkte erreichbar machen (Lücke 4.7)

| Feld | Inhalt |
|---|---|
| Ziel | Ein normaler Spieler erzielt ohne Cheats Handelspunkte > 0. |
| Dateien | zuerst nur Diagnose: `tools/handelsweg_diagnose.py` (neu, Werkzeug), dann je nach Befund `spieloekonomie.py`, `punkte.py`, `main.py` |
| Änderung | Die Diagnose läuft den Handelsweg im Automatenspiel ab und schreibt den **ersten** abgelehnten Schritt mit Grund auf (Gebäude fehlt, Karren fehlt, kein Handelspartner, keine Punktebuchung). Erst danach folgt der eigentliche Fix als eigener Commit. Das Handelsabkommen (Schnitt 2) gibt den Bots einen Handelspartner. Das ist wahrscheinlich die fehlende Gegenseite **[UNSICHER]**. |
| Daten | Handelspunkte je Handel: aus vorhandenen Daten (`punkte.py`), keine neue Zahl. Fehlt ein Wert: VORSCHLAG, dann an Daniel. |
| Wache | (1) E2E: Karren → Handel mit einem Bot → Rückkehr → Handelspunkte > 0, ohne gesetzte Zustände. (2) Anzeige-Leiste und `punkte` liefern denselben Wert. (3) Automatenspiel 12 Tage: Handelspunkte > 0 in mindestens 1 von 10 Läufen mit festem Startwert. |
| Fertig-Kriterium | Wache 1–3 grün; im Kennzahlenblatt ist `handelspunkte` nicht mehr konstant 0 |
| Aufbauzeit-Effekt | unverändert, weil Handel parallel zum Weg ins Gefecht läuft |
| Ablösung | wird erst nach der Diagnose benannt; vorher ändere ich nichts |
| Risiko | Die Diagnose findet mehrere Ursachen. Dann wird jede zu einem eigenen Schnitt. |

### Schnitt 6 – Bot-Drachenregel, Bot-Spionage, Persönlichkeit (Lücke 4.9)

| Feld | Inhalt |
|---|---|
| Ziel | Bots meiden den Drachen oder greifen ihn gezielt an, spionieren den Spieler aus und folgen einem durchgehenden Profil. |
| Dateien | `src/bottaktik.py` (Drache, Spionageauftrag), `src/spionage.py` (vorhandenen Weg nutzen), `data/bot_persoenlichkeit.json` (neu, Daten), `data/bot_raubzug.json`, `tests/test_bot_drache.py`, `tests/test_bot_spionage.py`, `tests/test_bot_profil.py` |
| Änderung | `bot_drache_entscheidung(bot, drache) -> "meiden"/"angreifen"`: angreifen nur bei Armee-SK ≥ Drachenwert × Sicherheitsfaktor. Die Spionage nutzt den vorhandenen Spieler-Spionageweg mit vertauschten Rollen, vor einem Raubzug, wenn der letzte Bericht älter als die Frist ist. Profil je Bot (`vorsichtig`/`gierig`/`haendler`/`raecher`/`forscher`): Es setzt nur **Faktoren** auf vorhandene Schwellen (Rache, Raubzug, Gunst-Änderung), es führt keine neue Logik ein. |
| Daten | Sicherheitsfaktor 1,5 [VORSCHLAG: entspricht dem Reserveprinzip aus V-5, aber stärker, weil der Drache nicht flieht **[UNSICHER]**]; Spionage-Frist 1 Spieltag [VORSCHLAG = Berichtsfrist]; Profilfaktoren 0,8 bis 1,2 [VORSCHLAG, kleine Spanne, damit die Balance stabil bleibt] |
| Wache | (1) Bot mit SK < Schwelle: nie ein Auftrag gegen den Drachen. (2) SK ≥ Schwelle und Profil `gierig`: angreifen. (3) Vor einem Raubzug ohne frischen Bericht entsteht genau ein Spionageauftrag. (4) Spionage gegen den Spieler läuft durch dieselben Gates wie der Angriff (Götterschutz, NAP). (5) Alle 5 Bots haben ein Profil, und ein alter Spielstand ohne Profil lädt mit dem Standard `vorsichtig`. |
| Fertig-Kriterium | 5 von 5 grün; im Automatenspiel greift kein Bot den Drachen mit Verlust von 100 % an (0 Totalverluste in 10 Läufen) |
| Aufbauzeit-Effekt | Spionage: unverändert. Profile: können die Aufbauzeit heben (aggressive Bots). Messung im A/B-Lauf, und Pflicht: Die Spanne 0,8–1,2 darf das erste Gefecht um höchstens 1 Spieltag verschieben [VORSCHLAG] |
| Ablösung | Bot-Konstanten in `bot_raubzug.json` bleiben; die Profile multiplizieren sie. Es wird nichts migriert. |
| Risiko | Die Profile machen die Läufe unvergleichbar. Gegenmittel: Profile hängen am festen Startwert (Wache 5). |

### Schnitt 7 – E2E-Wegeketten (A-1) und Quellwache Anzeige (A-2)

| Feld | Inhalt |
|---|---|
| Ziel | Jeder Spielweg ist als Kette ohne gesetzten Zustand belegt, und keine Ansicht rechnet selbst. |
| Dateien | `tests/test_e2e_wege.py`, `tests/test_quelle_anzeige.py` |
| Änderung | Ketten: Rohstoff, Forschung, Ware, Ausbildung, Einsatz, Rückkehr, Speichern/Laden, dazu Handel (Schnitt 5), Heilung, Reparatur, Vertrag und Portal (Langweg, E-6). Die Quellwache prüft die Methoden der Ansichten in `NebelseetalApp` auf Rechenmuster bei Kosten, Sperren, Gunst, Mengen und Dauer (Multiplikation mit Datenwerten, Vergleich auf Grenzwerte), Docstring und Kommentar sind abgeschnitten (Regel 5.3). |
| Daten | keine neuen Zahlen |
| Wache | je Weg eine Kette (12) und je Ansicht eine Quellprüfung |
| Fertig-Kriterium | alle Ketten grün ohne `state.<feld> = `-Zuweisungen außer dem Startwert |
| Aufbauzeit-Effekt | unverändert, weil nur geprüft wird |
| Ablösung | keine |
| Risiko | Lange Laufzeit, Folge E-4. Das Portal läuft deshalb mit Zeitsprung im Tick, nicht in Echtzeit. |

### Schnitt 8 – S5 Siedlungsumzug (**GESPERRT, nur Vorschlag, nicht fertig**)

Das ist ein durchdachter Entwurf, **kein Einbauvorschlag zur Freigabe**. Es gibt keinen Preis, weil Daniel einen gerechneten Preis verlangt und mir dafür die Grundlage fehlt. Ablauf: Prüfen → Siedler und Mana atomar buchen → Gebäude und Stufen auf die zufällige Zielkarte übertragen → die alte Karte zurück in den Katalog → Vorräte genau einmal übertragen. Offene Frage: Was passiert mit Gebäuden, deren Gelände auf der Zielkarte fehlt? Wache (geplant, wie im Dokument): zu wenig Siedler, laufende Aufträge sperren, alte Karte wieder verfügbar, Vorräte einmal gebucht, Gebäude unverändert. Zusätzlich: ein Gelände-Konflikt wird mit Grund abgelehnt. Aufbauzeit-Effekt: keiner bis zum ersten Gefecht, weil es ein Spätweg ist.

---

## Teil 4 – Balancing-Konzept (9.2)

Alle Werkzeuge liegen in `tools/` und laufen nie im Spiel mit. Neue Datei nur: `tools/balance_kreis.py` (Begründung: Regelkreis und A/B gibt es noch nicht). Das Kennzahlenblatt kommt in das vorhandene `spieltest_simulation.py`.

### 4.1 Kennzahlenblatt je Partie
- **Zweck:** messbarer Fingerabdruck jeder Partie.
- **Eingaben:** Journal und Zustand aus `spieltest_simulation.py`, Startwert.
- **Ausgaben:** `docs/balancing/kennzahlen.jsonl` (eine Zeile je Partie), `docs/balancing/KENNZAHLEN_<JJJJMMTT>.md`.
- **Aufruf:** `python tools/spieltest_simulation.py --tage 12 --startwert 42 --kennzahlen`
- **Beispielzeile:** `{"startwert":42,"stand":"1c5cb73","daten_hash":"…","tag_erstes_haus":0.9,"tag_erste_bibliothek":1.4,"tag_erste_ware":4.2,"tag_erster_krieger":6.8,"tag_erstes_gefecht":9.1,"ruhm_stufe":1,"ausgaben":{"holz":4120},"leerlauf_sek":{"ausbildung":30200},"fehlschlaege":[{"aktion":"handel_start","grund":"kein_partner","anzahl":14}],"handelspunkte":0,"beute_je_feldzug":[38],"verluste_je_gefecht":[3]}` (die Werte sind Platzhalter für das Format, keine Messung).
- **Prüffall:** `tests/test_kennzahlenblatt.py` prüft 12 Pflichtschlüssel und ob gleicher Startwert und gleicher Stand eine identische Zeile ergeben (außer Zeitstempel). Fehlt ein Meilenstein, steht `null`, nicht 0.

### 4.2 Sollkurve
- **Zweck:** Zielkorridor je Spieltag, gerechnet statt getippt.
- **Rechnung:** Aus `resources.json`, Startkarte, `baupreise.json`, `research.json` und `units.json` spielt ein deterministischer „Idealplan" die belegte Kette (4.3) nach. Untere Grenze = Idealplan × 0,7, obere Grenze = Idealplan × 1,1 [VORSCHLAG: Menschen spielen nie ideal, und mehr als 10 % über ideal deutet auf einen Fehler hin]. Punkte: Ziel 3,3 je Tag [DOK V-3].
- **Ausgaben:** `data/sollkurve.json` (erzeugt, mit Kopf `erzeugt_aus` = Hash der Eingabedateien).
- **Aufruf:** `python tools/balance_kreis.py sollkurve`
- **Prüffall:** Neu rechnen ohne Datenänderung ergibt eine identische Datei. Holz +10 % in `resources.json` muss den Holzkorridor ändern (die Kurve kommt also wirklich aus den Daten).

### 4.3 Regelkreis
1. `balance_kreis.py messen --laeufe 10 --startwert 1..10`: Kennzahlen gegen Sollkurve, Abweichung je Größe und Tag.
2. `vorschlag`: höchstens **ein** Datenwert je Runde (Datei, Schlüssel, alt, neu, Quelle = die Abweichung). Die Schrittweite ist höchstens 10 % [VORSCHLAG]. Werte mit Kennzeichen BELEGT werden **nie** vorgeschlagen, sondern als Befund an Daniel gemeldet.
3. `ab --aenderung vorschlag_<n>.json`: dieselben 10 Startwerte mit und ohne Änderung, gleiche Reihenfolge, die Daten in einer temporären Kopie, **kein** Schreiben in `data/`.
4. `urteil`: angenommen, wenn die Abweichungssumme der Zielgröße um ≥ 20 % sinkt **und** keine andere Größe aus dem Korridor fällt **und** `tag_erstes_gefecht` nicht steigt (4.12) [Schwellen VORSCHLAG]. Ausgabe nach `docs/balancing/URTEIL_<n>.md`.
- **Prüffall:** Eine Quellwache stellt sicher, dass `balance_kreis.py` keine Datei unter `src/` schreibt. Wird ein BELEGT-Wert vorgeschlagen, endet das als Fehler.

### 4.4 Tester-Feedback-Eingang
- **Vorlage** `docs/feedback/VORLAGE.md`: Was (Beobachtung, keine Wertung), Wann (Spieltag und Uhr), Stand (Version, Commit, Spielstand-Datei), Zahl (welcher Wert war erwartet, welcher sichtbar), Gefühl 1–5.
- **Bündeln:** `python tools/balance_kreis.py feedback` ordnet jede Meldung einem Schlüssel (Ansicht + Mechanik + Kennzahl) zu. Gleiche Schlüssel werden zu einem Eintrag mit Zähler zusammengefasst und in `docs/feedback/BUENDEL.md` geschrieben. Ab 3 Meldungen [VORSCHLAG] wird daraus ein Messauftrag an den Regelkreis.
- **Prüffall:** Zwei inhaltsgleiche Meldungen ergeben 1 Bündel mit Zähler 2. Eine Meldung ohne Stand wird mit Grund zurückgewiesen.

### 4.5 Abnahmekriterium je Änderung
Für jede Änderung im Register: Zahl vorher, Zahl nachher, Startwerte 1..10, gleicher Commit, gleicher `daten_hash` außer dem geänderten Schlüssel. `urteil` prüft das selbst und verweigert bei einer Abweichung.

---

## Teil 5 – Abschlusserklärung A-1 bis A-7

Alles ist **offen**, weil ich nichts gebaut oder ausgeführt habe. Hier steht, womit jede Bedingung nach den Schnitten erfüllt wäre:

| Nr. | Zustand | Beleg nach Umsetzung |
|---|---|---|
| A-1 | offen | `tests/test_e2e_wege.py`: 12 Ketten grün (Schnitt 7); Handel erst nach Schnitt 5 |
| A-2 | offen | `tests/test_quelle_anzeige.py` grün |
| A-3 | offen | Kennzahlenblatt: 10 von 10 Läufen mit `tag_erstes_gefecht ≤ 12`, Ware und Einheit nicht `null` |
| A-4 | offen | Ladewachen in Schnitt 1–4 und 6 (jeweils „alter Spielstand lädt") |
| A-5 | offen, mit Grund | Alle meine VORSCHLAG-Zahlen brauchen Daniels Entscheidung; E-3 blockiert die Ereigniszahlen |
| A-6 | offen, mit Grund | Die heutige Grenze von 1.400 s fällt voraussichtlich (E-4); die Formulierung muss angepasst werden |
| A-7 | offen | Neue Zahlen nur in `diplomatie.json`, `ereignisse.json`, `bot_persoenlichkeit.json`, `sollkurve.json`, je Mechanik ein Schalter `aktiv` |

---

## Teil 6 – Reihenfolge der Umsetzung

1. E-3 klären (Rechenweg V-4) und A-6 umformulieren (E-4). Keine Abhängigkeit.
2. Kennzahlenblatt (4.1). Es liefert die Vorher-Zahlen für alle weiteren Schnitte.
3. Schnitt 1 Gunst, hängt an 2 (Messung).
4. Schnitt 2 Verträge, hängt an 3.
5. Schnitt 5 Diagnose des Handelswegs, hängt an 4 (Handelsabkommen als Partner).
6. Schnitt 3 Rachetopf, hängt an 3 und 4 (NAP-Sperre).
7. Schnitt 4 Ereignisse, hängt an 1 und 3.
8. Schnitt 6 Bot-Drache, Spionage und Profil, hängt an 6.
9. Sollkurve und Regelkreis (4.2–4.5), hängen an 2.
10. Schnitt 7 E2E und Quellwache, ganz am Ende, weil es alle Wege prüft.
11. S5 bleibt gesperrt bis zur Freigabe.

---

## Teil 7 – Was ich absichtlich nicht liefere

- **Fertigen Code:** ohne Einblick in `main.py` (15.351 Zeilen) wären Signaturen geraten. Signaturen sind Namensvorschläge.
- **Belegte Zahlen über das Dokument hinaus:** Handbuch und Daten kann ich nicht einsehen (Regel 14.1).
- **Einen Preis für S5:** Er ist gesperrt, und es fehlt die gerechnete Grundlage.
- **Eine Änderung der Gesamtpunkte-Formel** (E-7): Das ist eine Designentscheidung.

## Antworten auf Anhang B

1. **Was fehlt für „komplett":** ein erreichbarer Handelsweg (messbar: Handelspunkte > 0 im Automatenspiel) und Bot-Reaktion bzw. Diplomatie (Schnitte 1–4, 6).
2. **Was am Balancing-Werkzeug fehlt:** Es fehlt eine Rückkopplung. Messwerkzeuge gibt es, aber keine Sollkurve, kein A/B mit festem Startwert und kein Urteil (Teil 4).
3. **Zahlen, die das Spielgefühl gefährden:** der Rachetopf ab Tag 3 (E-1), die Ereignispreise auf unklarem V-4 (E-3) und Herrscher 160 (E-10, erst messen). Gegenvorschlag: Rache ruht unter Götterschutz.
4. **Was überflüssig wird:** keiner der alten Abläufe. Rache und Profile ergänzen die Raubzug-Zeitwahl. Zu migrieren ist nichts, neue Felder werden mit Standardwert gelesen.
5. **Drei Prüfungen, die meinen Vorschlag am schnellsten widerlegen:** (a) Das Automatenspiel mit Schnitt 3 verschiebt `tag_erstes_gefecht` nach vorn. (b) `handelsweg_diagnose` zeigt, dass Handelsabkommen die Ursache nicht treffen. (c) Der Sammellauf mit allen neuen Wachen braucht über 1.500 s.
---

## Teil 7a – *Zusätzlicher Content, weil ich es kann*

> **Kennzeichnung:** Alles in Teil 7a gehört **nicht** zum Pflichtumfang aus Abschnitt 11. Es ist zusätzliches Material, das ich als großes Modell beisteuere. Jede Zahl darin ist **VORSCHLAG**. Jede Code-Korrektur ist ein **Ablöse-Vorschlag** im Sinne von Abschnitt 13. Ich habe den Code nicht gesehen, deshalb setzt jede Korrektur voraus, dass der beschriebene Zustand zutrifft. Das muss zuerst geprüft werden, Prüfbefehl steht jeweils dabei. Wer Teil 7a streicht, verliert nichts aus Teil 1–8.

### Z-1 Für den Weltenfresser-Hermes-Agenten: Arbeitsprotokoll je Schnitt

Euren Agenten kenne ich nur dem Namen nach. Die folgenden Regeln sind werkzeugneutral und passen zu jedem Agenten, der Dateien liest, Befehle ausführt und committet.

**Z-1.1 Ablauf je Schnitt (Zustandsmaschine).** Der Agent geht nur vorwärts, wenn der vorige Zustand belegt ist:

| Zustand | Ausgang | Beleg, den der Agent ablegt |
|---|---|---|
| `LESEN` | betroffene Dateien und Funktionen gefunden | Liste Pfad:Zeile in `docs/agent/<schnitt>/lesen.md` |
| `VORHER` | Kennzahlen und gezielte Wachen vor der Änderung | `vorher.json` (Kennzahlenblatt, Testergebnis) |
| `WACHE_ROT` | neue Wachen geschrieben, **schlagen fehl** | Ausgabe mit erwartetem Rot |
| `BAUEN` | kleinste Änderung, bis die neuen Wachen grün sind | Diff |
| `TEILLAUF` | nur betroffene Prüfdateien (Z-2.4) grün | Log |
| `SAMMELLAUF` | voller Lauf 0 rot | Log mit Dauer |
| `NACHHER` | Kennzahlenblatt mit gleichen Startwerten | `nachher.json`, Vergleich |
| `COMMIT` | ein Commit, Nachricht mit Registernummer | Hash |

**Warum `WACHE_ROT`:** Eine Wache, die vor dem Bau schon grün ist, prüft nichts. Das ist dieselbe Fehlerklasse wie F-04 („zweimal grün geprüft und trotzdem falsch“).

**Z-1.2 Abbruchregeln (gegen Agentenschleifen).**
- Derselbe Fehler dreimal nach Korrekturversuch: Stopp, Befund an Daniel, nicht weiterraten.
- Ein Diff über 400 Zeilen in einem Schnitt [VORSCHLAG]: Stopp, Schnitt teilen.
- Eine Zahl ohne Quelle landet in `data/`: Stopp. Der Agent schreibt sie mit `"quelle": "VORSCHLAG"` und meldet sie, statt sie still zu setzen.
- Eine Änderung an einem BELEGT-Wert: immer Stopp.

**Z-1.3 Abgleich mehrerer Modellantworten (euer Verfahren aus Abschnitt 0, als Werkzeug).** Mein Vorschlag ist eine Abgleichmatrix `docs/eingaenge/LLM_<datum>/ABGLEICH.md`:

| Punkt | Modell A | Modell B | Modell C | Beleg vorhanden? | 4 Prüffragen | Urteil |
|---|---|---|---|---|---|---|
| Rache-Start | ab Tag 3 | ruht unter Götterschutz | … | V-5, 4.12 | j/j/j/n | B |

Regel: Übereinstimmung zwischen Modellen ist **kein** Beleg. Drei Modelle können dieselbe falsche Zahl aus demselben Dokument ableiten. Entscheidend bleibt der Beleg nach Abschnitt 13.

**Z-1.4 Maschinenlesbares Register.** `docs/PRUEFREGEL_ORIGINAL.md` hat 259 Einträge in Prosa. Zusätzlich vorgeschlagen: `docs/register.jsonl` mit einer Zeile je Eintrag (`nr`, `datum`, `schnitt`, `dateien`, `wachen`, `commit`, `quelle`). Dann kann der Agent vor jeder Zahl prüfen, ob sie schon belegt oder schon verworfen wurde, statt die Prosa zu durchsuchen.

**Z-1.5 Kontextbudget.** `main.py` hat 15.351 Zeilen und passt in kein Modellfenster mit Spielraum. Der Agent soll nie die ganze Datei lesen, sondern über einen Index arbeiten: `tools/code_index.py` (neu, Werkzeug) schreibt `docs/agent/code_index.json` mit Funktion → Datei, Zeile von/bis, aufgerufene Funktionen, gelesene `data/`-Schlüssel. Aufbau mit `ast` aus der Standardbibliothek, also ohne neue Abhängigkeit.

### Z-2 Korrekturvorschläge am vorhandenen Code (Ablöse-Schnitte, ungeprüft)

Jeder Punkt ist ein **eigener Schnitt** nach Abschnitt 13: was fällt, was bleibt, was migriert.

**Z-2.1 Bot-Funktionen aus `main.py` herausziehen.**
- **Befund laut Dokument:** 69 von 74 `bot_*`-Funktionen stehen in `main.py`, obwohl es `botkern.py` gibt. Das widerspricht Regel 14.3 („reine Rechnung in die Fachdatei“).
- **Prüfbefehl vorher:** `python tools/code_index.py --filter bot_ --datei src/main.py` zeigt, welche davon zeichnen (tkinter-Aufrufe) und welche nur rechnen.
- **Fällt:** nichts am Verhalten. **Bleibt:** Namen in `main.py` als dünne Weiterleitung (`def bot_x(self, ...): return botkern.bot_x(self.state, ...)`), damit alte Aufrufer und Quellwachen nicht brechen. **Migriert:** nur reine Rechenfunktionen, in Tranchen von höchstens 10 je Schnitt [VORSCHLAG].
- **Wache:** Golden-Run, also Automatenspiel 12 Tage mit 3 festen Startwerten. Die Journal-Hashes müssen vorher und nachher **identisch** sein. Bei reinem Verschieben ist das die schärfste mögliche Prüfung.
- **Aufbauzeit-Effekt:** unverändert.

**Z-2.2 F-04 maschinell erzwingen statt per Textsuche.** Quellwachen mit Textmustern sind brüchig (Kommentare, Umbenennungen). Vorschlag ist eine AST-Wache: In Methoden von `NebelseetalApp`, deren Name mit `_zeige`/`_zeichne`/`ansicht` beginnt [Präfixe UNSICHER, aus dem Index ablesen], gilt jede `BinOp` mit `Mult`/`Div` auf einen Wert, der aus `data` oder `spieldaten` stammt, als Befund. Ebenso jeder `Compare` gegen eine Ganzzahl-Konstante > 1.

```python
# tests/test_quelle_ast.py  (ASCII, Skizze)
import ast, pathlib
from harness import check, bericht

QUELLE = pathlib.Path("src/main.py").read_text(encoding="utf-8")
BAUM = ast.parse(QUELLE)
PRAEFIXE = ("_zeige", "_zeichne", "ansicht_")   # aus code_index pruefen

def ansichts_methoden(baum):
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ClassDef) and knoten.name == "NebelseetalApp":
            for f in knoten.body:
                if isinstance(f, ast.FunctionDef) and f.name.startswith(PRAEFIXE):
                    yield f

def rechenstellen(funktion):
    for k in ast.walk(funktion):
        if isinstance(k, ast.BinOp) and isinstance(k.op, (ast.Mult, ast.Div, ast.FloorDiv)):
            yield k.lineno
        if isinstance(k, ast.Compare):
            for c in k.comparators:
                if isinstance(c, ast.Constant) and isinstance(c.value, int) and c.value > 1:
                    yield k.lineno

for f in ansichts_methoden(BAUM):
    zeilen = list(rechenstellen(f))
    check(f"{f.name} rechnet nicht selbst", zeilen == [], detail=str(zeilen))
bericht()
```

Weil Docstrings und Kommentare im AST gar nicht als Ausdrücke vorkommen, erledigt sich die Regel „Docstring abschneiden“ von selbst. Für bekannte, erlaubte Stellen (Pixelrechnung im Canvas) gibt es eine Ausnahmeliste `tests/quelle_ast_ausnahmen.json` mit Begründung je Zeile.

**Z-2.3 Atomare Buchung als ein Helfer.** „Jede Buchung ist atomar, mit Rückbuchung“ steht als Regel im Dokument. Ob es dafür **eine** Funktion gibt, weiß ich nicht. Falls jedes Modul selbst prüft und abbucht, ist das eine wiederkehrende Fehlerquelle (halbe Buchung bei Ausnahme). Vorschlag für `src/wirtschaft.py` (vorhandenes Modul, kein neues):

```python
def buche_atomar(ort, kosten: dict[str, float], grund: str) -> tuple[bool, str]:
    """Bucht alle Posten oder keinen. Rueckgabe (ok, grund)."""
    bedarf = {k: math.ceil(v) for k, v in kosten.items() if v > 0}   # E-5: nie gratis
    fehlt = {k: bedarf[k] - ort.vorrat.get(k, 0)
             for k in bedarf if ort.vorrat.get(k, 0) < bedarf[k]}
    if fehlt:
        return False, "fehlbestand:" + ",".join(sorted(fehlt))
    for k, menge in bedarf.items():
        ort.vorrat[k] = ort.vorrat.get(k, 0) - menge
    journal_buchen(ort, grund, bedarf)
    return True, ""
```

**Ablösung:** Vorhandene Einzelbuchungen bleiben, bis jede mit eigener Wache auf den Helfer umgestellt ist (ein Modul je Schnitt). Das `math.ceil` ist die Regel aus E-5 und **gilt nur nach Daniels Entscheidung**. Ohne Entscheidung bleibt das heutige `int()`.

**Z-2.4 Sammellauf beschleunigen (löst E-4 technisch).** 1.346 s für 183 Dateien bei einem Prozess.
- `tools/sammellauf.py --teil`: Aus dem Code-Index wird bestimmt, welche Prüfdateien ein geänderter Pfad betrifft (Import-Graph). Nur die laufen im Zustand `TEILLAUF`. Der volle Lauf bleibt Pflicht vor dem Commit (Regel 14.8 unverändert).
- `tools/sammellauf.py --parallel N`: Jede Prüfdatei läuft als eigener Prozess (`concurrent.futures.ProcessPoolExecutor`, Standardbibliothek). Voraussetzung: Keine Prüfdatei schreibt in einen gemeinsamen Pfad. Prüfbefehl dafür: einmal mit `--parallel 1` und einmal mit `--parallel 4` laufen lassen, die Ergebnislisten müssen identisch sein.
- Bei 4 Kernen erwarte ich grob ein Viertel bis ein Drittel der Dauer. Das ist **geschätzt, nicht gemessen**.
- Die zwei Dateien ohne Ergebniszeile (Abschnitt 6) bekommen eine Pflicht-Ergebniszeile. Sonst kann ein Parallel-Lauf „Rückgabe 0, aber nichts geprüft“ nicht von „grün“ unterscheiden.

**Z-2.5 Determinismus als Grundbedingung des Regelkreises.** Der A/B-Lauf aus Teil 4 ist nur gültig, wenn derselbe Startwert dasselbe Spiel ergibt. Die „flatternde Kartenwahl-Wache“ aus Block 5 zeigt, dass es mindestens eine Zufallsstelle ohne festen Startwert gab. Vorschlag:
- Eine einzige Zufallsquelle `GameState.rng = random.Random(startwert)`, an alle Fachmodule durchgereicht. Kein `random.random()` auf Modulebene.
- Wache `tests/test_determinismus.py`: (1) Quellwache, `src/` enthält keinen Aufruf `random.<funktion>(` außer `random.Random(`. (2) Zwei Automatenspiele mit Startwert 7 über 3 Spieltage ergeben ein identisches Journal (Hash). (3) Dasselbe gilt nach Speichern/Laden in der Mitte, deshalb gehört der RNG-Zustand (`rng.getstate()`) in den Spielstand, wobei ein fehlender Schlüssel mit Startwert neu gesät wird (Regel 14.6).
- Dasselbe gilt für die Uhr: Fachmodule lesen nur `spielzeit.jetzt(state)`, nie `time.time()`. Wache (1) analog für `time.time(` und `datetime.now(` außerhalb von `spielzeit`/`zeitbasis` und Anzeige-Uhren.

**Z-2.6 Feld gegen Eigenschaft beim Laden, eine Stelle.** Regel 5.3 beschreibt das `asdict()`/`BotPlayer(**daten)`-Problem. Vorschlag ist ein Helfer `speichern.lade_dataclass(cls, daten, standard: dict)`: Er filtert unbekannte Schlüssel heraus, ergänzt fehlende aus `standard` und schreibt **nichts** zurück. Alle neuen Felder aus Schnitt 1–6 laufen darüber, die Wache „alter Spielstand lädt“ wird dann einmal generisch geschrieben statt sechsmal.

### Z-3 Meine Sicht aufs Spiel: Spielgefühl-Befunde

Das sind Design-Einschätzungen, keine Zahlenvorschläge. Jede ist mit einer Messung verbunden, damit sie widerlegbar ist.

1. **Die ersten 30 echten Minuten tragen das Spiel.** Erstes Gefecht nach 8–12 Spieltagen sind 64–96 echte Minuten. Davor gibt es nur Wirtschaft. Ob Spieler bis dahin bleiben, entscheidet sich an der Dichte kleiner Ziele. Messung: Im Kennzahlenblatt `abstand_meilensteine_max` ergänzen, also die längste Strecke ohne neuen Meilenstein in Spielstunden. Ich vermute, sie liegt zwischen Bibliothek und erster Ware. Wenn ja, sind die Ereignisse (Schnitt 4) das richtige Werkzeug, um sie zu füllen, und zwar **früher** als „1 je 3 Tage“.
2. **Ein Handel, der nicht zählt, wird nicht gespielt.** Selbst repariert bleibt Handel außerhalb von Gesamtpunkten und vermutlich Ruhm (E-7). Wenn eine der vier Auszeichnungen Handel belohnt, reicht das. Wenn nicht, ist der Handelsweg Dekoration. Das ist eine Daniel-Entscheidung, Messung erst nach Schnitt 5.
3. **Verwundete werden früh unsichtbar sein** (E-8). Das ist kein Fehler. Aber der Verlustbericht könnte „0 Verwundete (unter 4 Verlusten je Typ)“ schreiben, damit der Spieler die Regel lernt. Das ist ein Text in `data/nachrichten.json`, keine Mechanik.
4. **Der Rachetopf ist die erste Mechanik, die auf den Spieler reagiert,** und damit die wichtigste für das Gefühl „die Welt lebt“. Deshalb lohnt sich eine Ankündigung mit Stimme aus `bot_stimmen.json`, etwa mit den Stufen Topf 1, 2, 3 als steigende Drohung. Kosten: nur Texte.
5. **Das Portal ist ein Spätziel ohne Zwischenstufen.** 41,7 Spieltage mit einem Tempel sind etwa 5,5 echte Stunden. Ein Fortschrittsbalken in der Portal-Ansicht (Mana gesammelt / 5.000, gelesen aus derselben Kostenfunktion) macht das Warten sichtbar, ohne eine Zahl zu ändern.
6. **Bot-Profile sind gefährlich für die Balance und wertvoll für das Gefühl.** Deshalb habe ich sie auf Faktoren 0,8–1,2 begrenzt. Ein Profil soll man im Postfach **erkennen** können (Stimmen), aber in der Bilanz kaum merken.

### Z-4 Vollständige Datendatei-Vorlage `data/diplomatie.json`

Damit der Agent ohne Rückfrage bauen kann. Jeder Wert trägt seine Quelle.

```json
{
  "aktiv": true,
  "gunst": {
    "min": 0, "max": 100, "start": 50,
    "status": [
      {"bis": 39,  "schluessel": "feindselig", "text": "feindselig", "quelle": "DOK 7.1"},
      {"bis": 59,  "schluessel": "wachsam",    "text": "wachsam",    "quelle": "DOK 7.1"},
      {"bis": 100, "schluessel": "freundlich", "text": "freundlich", "quelle": "DOK 7.1"}
    ],
    "quelle_start": "VORSCHLAG: Mitte von wachsam",
    "aenderung": {
      "geschenk_je_100_gegenwert": 1, "geschenk_deckel": 10,
      "eigener_angriff": -15, "vertragsbruch": -20,
      "ereignis_angenommen": 5, "ereignis_abgelehnt": -5,
      "quelle": {"vertragsbruch": "DOK 7.2", "rest": "VORSCHLAG"}
    }
  },
  "rache": {
    "je_niederlage": 1, "je_tag_ohne_kontakt": 1, "schwelle": 3,
    "ruht_unter_goetterschutz": true,
    "nach_bot_sieg": 0,
    "armee_mindest_sk": 99,
    "ankuendigung_vorlauf_sek": 28800,
    "quelle": {"je_niederlage": "DOK 7.2", "je_tag_ohne_kontakt": "DOK 7.2",
               "schwelle": "DOK 7.2", "armee_mindest_sk": "DOK V-5",
               "ruht_unter_goetterschutz": "VORSCHLAG E-1",
               "nach_bot_sieg": "VORSCHLAG", "ankuendigung_vorlauf_sek": "VORSCHLAG = Berichtsfrist 4.10"}
  },
  "vertraege": {
    "nap": {"ab_gunst": 40, "dauer_sek": 86400, "bruch_unter": 40,
            "bruch_gunst": -20, "bruch_rache": 1, "quelle": "DOK 7.2"},
    "handel": {"ab_gunst": 40, "weg": "spieloekonomie.handel_start",
               "quelle": {"weg": "DOK 7.2", "ab_gunst": "VORSCHLAG"}},
    "durchmarsch": {"ab_gunst": 60, "nur_anzeige": true, "quelle": "DOK 7.2"}
  }
}
```

### Z-5 Kennzahlenblatt: Kern der Auswertung als Skizze

```python
# tools/balance_kreis.py  (Auszug urteil, ASCII)
def urteil(vorher: list[dict], nachher: list[dict], ziel: str, korridor: dict) -> dict:
    """vorher/nachher: je eine Kennzahlzeile pro Startwert, gleiche Reihenfolge."""
    assert [z["startwert"] for z in vorher] == [z["startwert"] for z in nachher]
    def abweichung(laeufe, groesse):
        soll = korridor[groesse]
        return sum(max(0, soll["unten"] - z[groesse], z[groesse] - soll["oben"])
                   for z in laeufe if z.get(groesse) is not None)
    a, b = abweichung(vorher, ziel), abweichung(nachher, ziel)
    besser = a > 0 and (a - b) / a >= KONF["mindest_verbesserung"]        # 0.20 VORSCHLAG
    neu_draussen = [g for g in korridor if g != ziel
                    and abweichung(nachher, g) > abweichung(vorher, g)]
    gefecht_spaeter = (median(z["tag_erstes_gefecht"] for z in nachher)
                       > median(z["tag_erstes_gefecht"] for z in vorher))
    return {"angenommen": besser and not neu_draussen and not gefecht_spaeter,
            "ziel": ziel, "vorher": a, "nachher": b,
            "verschlechtert": neu_draussen, "gefecht_spaeter": gefecht_spaeter}
```

**Prüffall** `tests/test_balance_urteil.py`: (1) Identische Listen ergeben `angenommen = False`, weil keine Verbesserung. (2) Ziel um 50 % besser, aber eine zweite Größe schlechter, ergibt `False` mit Nennung der Größe. (3) Ungleiche Startwert-Reihenfolge führt zu einem Fehler. (4) `tag_erstes_gefecht = null` in einem Lauf wird übergangen statt als 0 gezählt.

### Z-6 Drei Risiken, die ich im Gesamtplan sehe

1. **„Sich selbst verbessern“ kann auf Messfehler optimieren.** Wenn das Automatenspiel anders spielt als Menschen, kalibriert der Regelkreis das Spiel auf den Automaten. Gegenmittel: Ein Tester-Bündel (4.4) mit ≥ 3 Meldungen sticht im Urteil eine reine Kennzahl, Daniel entscheidet.
2. **Bezahlte Modellgutachten (`gesamtaudit_lauf.py`, `balancing_gutachten.py`) erzeugen Zahlen ohne Beleg.** Ihre Ausgaben sollten automatisch mit `VORSCHLAG` gestempelt in das Register laufen, nie direkt nach `data/`.
3. **Wachen-Inflation.** 7.495 Prüfungen sind viel, ein Teil davon prüft vermutlich Text statt Verhalten. Vorschlag: einmalig `tools/wachen_wert.py` laufen lassen. Es mutiert je Fachmodul eine Datenzahl (+1) und zählt, welche Prüfungen rot werden. Prüfungen, die bei **keiner** Mutation rot werden, sind Kandidaten für Durchsicht (nicht zum Löschen, Regel 12: nichts löschen).


---

## Teil 8 – Ablagehinweise an den Agenten

```
Ablage (fuer den Agenten):
- Zieldatei: docs/eingaenge/LLM_20261106/antworten/Antwort_ClaudeOpus55_AUFTRAG_20261106_2.md
- Index:     docs/eingaenge/LLM_20261106/README.md  (Spalten: Datei, Modell, Datum, Teile, Urteil, Quelle)
- Rohform:   unveraendert ablegen, nicht redigieren; SHA256 beim Ablegen bilden und im Index nennen
- Nichts loeschen, nichts ueberschreiben: vorhandene Datei mit gleichem Namen bekommt _2, _3 ...
- Desktop:   die Antwortdatei gehoert NICHT auf den Desktop; nach der Ablage dort nichts liegen lassen
```

Modell: Claude Opus 5.5 · Datum: 06.11.2026 · Teile: 1 · Fassung 2 · Dokumentversion: Stand 06.11.2026, V_0.0.3 · keine flüchtigen Links als Beleg.
