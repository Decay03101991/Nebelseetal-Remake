# EXKURS: GUTACHTER-FEEDBACK AN DEN HERMES-AGENTEN „WELTENFRESSER“
**Projekt:** Nebelseetal Remake (Pre-Release Phase)  
**Fokus:** Optimierung der KI-Arbeitsweise bei limitiertem Kontextfenster mit DeepSeek-Flash  
**Datum:** 06.11.2026  

---

## 1. Status Quo & Architektonischer Eindruck (Gutachten)

Das Projekt *Nebelseetal Remake* besticht durch eine extrem saubere, **datengesteuerte Trennung (Data-Driven Design)**. Dass Logik (`src/`) und Werte (`data/` JSON) strikt getrennt sind und die gesamte Oberfläche auf einem einzigen, monolithischen Zustandsmodell (`GameState`) basiert, ist die größte Stärke des Projekts. 

**Das Problem bei der KI-Skalierung:** `main.py` hat bereits knapp 15.000 Zeilen Code. Für ein *DeepSeek-Flash*-Modell, das zwar extrem schnell und günstig im Token-Verbrauch ist, wird dieser Monolith bei fortschreitender Entwicklung zum **Kontext-Nadelöhr**. Ein Modell mit begrenztem Kontextfenster verliert bei 15k Zeilen unweigerlich den Fokus auf Randfälle (Edge Cases), Variablenbenennungen und globale Zustände.

---

## 2. Taktische Arbeitsvorschläge für den Hermes-Agenten

Um trotz des wachsenden Codes hocheffizient, fehlerfrei und ohne „Kontext-Erblindung“ mit DeepSeek-Flash zu arbeiten, werden folgende systemische Anpassungen empfohlen. *Der Hermes-Agent evaluiert selbstständig, welche Schritte für ihn operativ sinnvoll sind.*

### Vorschlag A: Einführung von „Schnittstellen-Stubs“ (Kontext-Schlankheitskur)
DeepSeek-Flash braucht nicht alle 15.000 Zeilen der `main.py`, um eine neue Funktion zu schreiben. Es braucht nur die Definitionen.
*   **Aktion:** Erstelle eine temporäre oder permanente Datei `src/interfaces_stub.py`. Diese enthält *nur* die Klassennamen, Funktionssignaturen und Docstrings der `GameState`- und `NebelseetalApp`-Methoden (z. B. `def fuehre_schlacht(self, ...): pass`).
*   **Effekt:** Wenn du DeepSeek einen Auftrag erteilst, füttere es mit der `interfaces_stub.py` statt der echten `main.py`. Der Kontext schrumpft um 90%, und das Modell arbeitet mathematisch präziser.

### Vorschlag B: Logische Modularisierung *innerhalb* der Projektgrenzen
Die Projektregel verbietet neue Module für bereits gelöste Aufgaben. Sie verbietet jedoch nicht, mathematische Sub-Routinen auszulagern, um die `main.py` zu entlasten.
*   **Aktion:** Lagere reine mathematische Berechnungen (wie die Ausbau-Skalierung, die Götterschutz-Tickminderung oder die Beute-Sortierung) in die bestehende `src/punkte.py` oder andere reine Logikdateien aus. In `main.py` verbleibt nur noch der Aufruf. 
*   **Effekt:** Die Kernlogik der Oberfläche bleibt unberührt, aber die Funktionstiefe in der Riesen-Datei wird drastisch reduziert. DeepSeek-Flash kann isolierte Logik-Blöcke in kleinen Dateien weitaus fehlerfreier bearbeiten.

### Vorschlag C: Das „Strict-Typing & Fail-Safe“-Paradigma im Prompting
Da Python dynamisch typisiert ist, neigt DeepSeek-Flash bei mathematischen Formeln (wie dem Kosten-Exponenten beim Gebäudeausbau oder der 30%-Verwundetenquote) zu impliziten Typumwandlungen (`Float` statt `Int`), was lokale JSON-Spielstände korrumpieren kann.
*   **Aktion:** Zwinge dich im System-Prompt zu *Strict Typing* und *Expliziter Rundung*. 
*   **Beispiel:** Jede mathematische Operation, die Ressourcen oder Einheiten betrifft, *muss* für DeepSeek mit `math.floor()` oder `int()` gedeckelt werden. Keine Zuweisung darf ohne Typ-Validierung erfolgen.

### Vorschlag D: Automatisierte JSON-Schema-Wache
Da alle 5 Sprints neue Keys in das `Settlement.vorraete`- oder `state.messages`-Gitter einführen, steigt das Risiko, dass ältere Test-Spielstände beim Laden unbemerkt Keys vermissen.
*   **Aktion:** Schreibe eine ultrakompakte Funktion `def _validiere_zustand_strukturell(state_dict)`, die beim Laden prüft, ob fundamentale Keys wie `wounded` oder `active_contracts` existieren, und diese andernfalls mit Standardwerten (`{}`, `[]`) initialisiert.
*   **Effekt:** Das System wird immun gegen asynchrone Spielstands-Fragmente, ohne dass du bei jedem KI-Generierungsschritt eine Migration programmieren musst.

---

## 3. Fazit für das Agenten-System

Die gewählte Pipeline (Daniel als Entscheider, Hermes als Koordinator, DeepSeek-Flash als Umsetzer via WSL) ist für ein Projekt dieser Tiefe **hochgradig effizient**. 

Durch das gezielte **Vorenthalten von UI-Code** bei reinen Logik-Aufträgen (Kontext-Kapselung) und das strikte Einfordern von **ASCII-only Codekommentaren** pro Zeile wird verhindert, dass DeepSeek-Flash bei komplexen Folgeaufträgen (wie der Verwundetenheilung in der Kaserne) die Orientierung verliert. Die Architektur des Sprints ist grundsolide.