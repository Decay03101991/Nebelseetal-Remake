# Prüfvermerk zur externen Spielprüfung (ChatGPT, 31.10.2026)

**Gegenstand:** `docs/audits/EXTERNE_TESTS_GPTCHAT_20261031.md` (57.702 Byte, SHA256
`0c33232d…`, vom Desktop übernommen und hashgleich abgelegt). Die Prüfung selbst bezieht sich auf
den **öffentlichen Release-Stand `954097a` (FIX04j)**, nicht auf den heutigen Arbeitsstand
(`a3a8e4a`). Deshalb wurde hier **jeder** der nachfolgend genannten Befunde gegen den **aktuellen
Code** gehalten — nicht gegen den Release.

**Regel, die dabei gilt:** Was hier als „“ steht, ist am heutigen Quelltext gelesen
worden. „“ heißt: nicht gelesen, nicht belegt, keine Behauptung. Wie immer gilt: ein
Befund ist erst wahr, wenn er nachgemessen ist (Projektregel seit 30.10.2026).

| Befund | Urteil am heutigen Stand | Beleg (heute gelesen) |
|---|---|---|
| **F-01 [P0] Lokal ausgebildete Truppen fehlen im Angriffsweg** | **BESTÄTIGT — Fehler besteht weiter** | `main.py:5622` `_truppen_nach_rolle` liest `self.state.units` (Reichsbestand); `main.py:5955` baut daraus den Angriff. Die Einheiten, die `spieloekonomie.ort_tick` nach `ort["einheiten"]` schreibt, kommen dort nicht vor. |
| **F-03 [P0] Portalkosten greifen auf die Reichsanzeige statt aufs Ortslager** | **BESTÄTIGT — Widerspruch besteht weiter, Verhalten nicht gemessen** | `main.py:4771` liest `self.state.resources["mana"].amount`, bucht in `4779` dorthin zurück; dieselbe Zahl wird von `_reichsanzeige_aus_orten` aus den Ortslagern neu aufgebaut. Ob die Zahlung faktisch „“, ist **REPRO OFFEN** (nicht nachgestellt). |
| **F-04 [P1] Zwei Waren mit zwei Forschungsbedingungen sind in der Ansicht zu früh frei** | **BESTÄTIGT — UI/Kern-Widerspruch, Verstoß gegen „“** | `data/warenrezepte.json` nennt für **Lederrüstung** `Nähkunst 1 + Rüstungsbau 2`, für **Magischen Paladinharnisch** `Rüstungsbau 7 + Magiekunde 2`. Die Ansicht liest dagegen `main.py:1948-1957` `ware_voraussetzung` aus `items.json` und gibt bei fehlender `voraussetzung_struktur` **True** („“) zurück; der Kern (`spieloekonomie.ware_start`) prüft alle Bedingungen und lehnt ab. |
| **F-09 [P1] Angriff startet immer aus Siedlung 0** | **BESTÄTIGT — Fehler besteht weiter** | `main.py:5967-5968` übergibt `self.state.settlements[0].name` als Start; `_auftrag_entfernung` fällt ebenfalls auf Siedlung 0 zurück. |
| **F-08 [P1] Ausbildungsdauer reagiert nicht auf die Gebäudestufe** | **ERLEDIGT — Befund ist überholt** | `spieloekonomie.py:589-590` rechnet heute `dauer = grunddauer / max(1, stufe)` (Schalter `AUSBILDUNG_STUFENFAKTOR_AKTIV`). Der Release, den die Prüfung las, hatte das noch nicht. |
| F-02, F-05, F-06, F-07, F-10, F-11, F-12, F-13, F-14 | **NICHT GEPRÜFT** | Noch nicht am heutigen Code gelesen. Die Datei nennt sie ausdrücklich als Kandidaten. Vor jeder Umsetzung gilt: erst nachweisen, dann ändern. |

## Was daraus für die nächste Sitzung folgt

1. **F-01 ist der schwerste Befund** — es ist derselbe Bruch, den das Projekt an anderer Stelle schon
   einmal geschlossen hat (Ortslager führt, Reichsanzeige leitet ab). Die Prüfung hat ihn mit 3.627
   grünen Prüfungen im Rücken gefunden: **unsere Prüfungen decken den Weg „ausgebildete Einheit →
   Angriff“ nicht ab.** Das ist ein Prüfstands-Mangel, nicht nur ein Codefehler.
2. **F-04 ist der billigste** (Ansicht und Kern auf **eine** Quelle: `warenrezepte.json`).
3. **F-09 und F-03 gehören zusammen** (Ortsbezug: richtiger Startort, richtige Kasse). Für F-03 ist
   zuerst eine Entscheidung nötig (welche Kasse zahlt das Portal), dann eine Prüfung mit Bilanz.
4. **F-08 nicht erneut anfassen** — erledigt, der Befund stammt aus dem alten Release.

## Herkunft und Kosten

Die Prüfung kostete **keine** DeepSeek-Guthaben (ChatGPT-Auftrag von Daniel, nicht über dieses
Konto). Dieser Vermerk und die Ablage kosteten nur lokale Arbeit; der nächste Modellaufruf wird
vorher angesagt.
