# Fragen an Daniel - Sitzung 04.11.2026 (S-8 Stufe 3)

**Wozu:** Entscheidungen, die diese Sitzung nicht selbst treffen darf. Je Frage: Messlage, Wirkung,
Empfehlung. Die Antworten kommen als datierter Nachtrag hierher und in die betroffene Datendatei.

## 1. Zuordnung der fuenf Spiel-Taktiken zu den fuenf Entwurfs-Plaenen (VORSCHLAG)

**Messlage:** Der Entwurf (`S8_STUFE3_BAUPLAENE_20261103.md`) nennt fuenf abstracte Taktiken
(kriegerisch, haendlerisch, defensiv, ausgleichend, geheim). Das Spiel kennt fuenf ANDERE Namen mit
festem Bonus (`bottaktik.TAKTIKEN`): Pluenderer (Beute +5 %), Waechterin (Verteidigung +5 %),
Bastionier (Ausbau +5 %), Spaeherin (Reisegeschwindigkeit +5 %), Raecher (Angriff AT +5 %).
Zugeordnet ist nach dem Bonus: Raecher -> kriegerisch (Metall fuer Waffen), Pluenderer ->
haendlerisch (Beute wird zuerst in Gold ausgezahlt), Waechterin -> defensiv (Stein fuer Wall und
Mauer), Bastionier -> ausgleichend, Spaeherin -> geheim (Pferde fuer Reisen).

**Wirkung:** Jede Taktik baut damit ein anderes Profil - gemessen: Raecher 39 Erzminen und 8
Goldminen, Spaeherin 31 Pferdezuchten, Waechterin 21 Steinmetze. Eine andere Zuordnung tauscht nur
die Plaene unter den Bots, nicht die Mechanik.

**Empfehlung:** so lassen. Ein Wort in `data/bot_bauplan.json` (Feld `zuordnung`) genuegt, wenn du
eine Taktik anders siehst.

## 2. Erzmine steht in der Mindest-Reihenfolge VOR Steinmetz und Goldmine

**Messlage:** In der Reihenfolge der Entwurfs-Tabelle (Steinmetz, Goldmine, Erzmine) nahmen die
beiden ersten auf Berg-armen Karten jeden Berg; die Erzmine bekam keinen (gemessen: Karte
`original-118b` hat 5 Bergfelder fuer 8 Anlagen). Ohne Erzmine gibt es kein Metall, ohne Metall
keinen Siedlerkarren (80 Metall) und keine Gruendung - die Lehre steht seit S-8 Stufe 1 im Register
(174). Mit der Erzmine zuerst steigt Metall um 50 bis 100 Prozent (Haug 15 -> 24, Grom 22,5 -> 36
Metall je Stunde), dafuer fallen Gold und Stein etwas niedriger aus (Haug Gold 31.677 -> 26.493).

**Wirkung:** Metall ist der Engpass fuer Wachstum (Karren, Ausruestung), Gold und Stein sind im
Ueberfluss. Die Dorfzahl bleibt in beiden Faellen 4/4/4/4/4.

**Empfehlung:** so lassen (Erzmine zuerst).

## 3. Das Entwicklungsprotokoll steht bei 350 Zeilen (Zielgroesse: unter 320)

**Messlage:** `tests/test_protokoll.py` meldet die Zielgroesse als Befund (kein Fehler). Die
Vorgaenger-Sitzung hat das Protokoll auf 348 Zeilen hinterlassen, diese Sitzung hat zwei Zeilen
(Guthaben, S-8 Stufe 3) angehaengt.

**Wirkung:** Verdichten heisst: unveraenderte Fassung als eigene Datei sichern und committen, neue
Fassung im Zwischenspeicher schreiben und mit `tools/pruefe_protokoll.py --nach` pruefen, erst dann
einsetzen. Rund 30 Minuten Arbeit, kein Code, keine Regel aendert sich.

**Empfehlung:** ja, aber als eigener Schritt nach S-12 - nicht mitten in einem Bau-Schnitt.

## 4. Die Bots horten Metall (Raecher 55.832 nach 24 Tagen)

**Messlage:** Nach dem neuen Bauplan erntet der Raecher 111 Metall je Stunde und kommt an den
Lagerdeckel (20.000 je Dorf), waehrend Ausruestung und Einheiten nur langsam abfliessen. Die anderen
Bots liegen bei 12.000 bis 17.000.

**Wirkung:** Ein Abnehmer (mehr Ausruestung, mehr Einheiten, Werkstattauftraege) macht den Bot
staerker, ist aber ein eigener Schnitt am Kern (`ausruestung`, `spielschicht.ausbilden`).

**Empfehlung:** erst S-12 und S-11 wie von dir festgelegt, danach einen Schnitt "Metall in Truppen".

## Antworten (Daniel, 04.11.2026, rund 09:15) - alle vier wie empfohlen

**Zu 1 - Zuordnung der Taktiken:** SO LASSEN. Es bleibt bei Raecher -> kriegerisch, Pluenderer ->
haendlerisch, Waechterin -> defensiv, Bastionier -> ausgleichend, Spaeherin -> geheim. Folge: keine
Codeaenderung, das Feld `zuordnung` in `data/bot_bauplan.json` bleibt die Begruendung.

**Zu 2 - Erzmine vorne:** BLEIBT SO. Folge: die Mindest-Reihenfolge in `data/bot_bauplan.json`
bleibt (Erzmine vor Steinmetz und Goldmine); die Messung im Dokument
`docs/MESSUNG_S8_STUFE3_BAUPLAENE_20261104.md` gilt damit als abgenommen.

**Zu 3 - Protokoll verdichten:** JA, als eigener Schritt NACH S-12. Folge: steht als kommender
Schnitt im Stand-Block; Verfahren nach Skill (unveraenderte Fassung sichern und committen, neue
Fassung im Zwischenspeicher, `tools/pruefe_protokoll.py --nach`, erst dann einsetzen).

**Zu 4 - Metall-Abnehmer:** ERST S-12 und S-11, danach ein eigener Schnitt "Metall in Truppen".
Folge: steht als kommender Schnitt im Stand-Block; das gehortete Metall bleibt bis dahin ein
dokumentierter Befund (Lagerdeckel 20.000 je Dorf), kein Fehler.

