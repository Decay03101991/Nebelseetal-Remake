# Abarbeitung der externen Spielprüfung (ChatGPT, 31.10.2026)

**Grundlage:** `docs/audits/EXTERNE_TESTS_GPTCHAT_20261031.md` (hashgleich, SHA256 `0c33232d…`) und
`docs/audits/PRUEFVERMERK_EXTERNE_TESTS_20261031.md`.
**Entscheidungen Daniels:** `docs/ENTSCHEIDUNGEN_CODEAUDIT_20261031.md`, Punkte 11–21.
**Regel:** Ein Befund ist erst wahr, wenn er am **heutigen** Code nachgemessen ist. Der Bericht prüfte
`954097a` (Release FIX04j); alle Urteile hier beziehen sich auf den Arbeitsstand ab `a3a8e4a`.

## Statusmatrix — bestätigt / widerlegt / vertagt

| Befund | Urteil | Beleg am heutigen Code | Was zu tun ist | Entscheidung |
|---|---|---|---|---|
| **F-01 [P0]** Lokal ausgebildete Truppen fehlen im Angriffsweg | **BESTÄTIGT** | `main.py:5622` `_truppen_nach_rolle` liest `self.state.units`; `main.py:5663` (`_angriff_durchfuehren`) und `main.py:5955` (`_auftrag_angriff`) beziehen daraus | Ortsheer als Quelle: `quelle_id` + `ort["einheiten"]`; Reichsbestand nur noch Anzeige | — (Daniel: Auftrag) |
| **F-02 [P0]** Durchspieltest verdeckt F-01 | **BESTÄTIGT** | `test_durchspiel.py:217` setzt `_ort4.waren[_w] = 1`; `:236` und `:425` setzen `gs.units[krieger].count = 8` | Test **nicht** umbauen; zusätzlich `test_produktionskette_ohne_cheats.py` als Release-Gate | — |
| **F-03 [P0]** Portal bucht in die Reichsanzeige | **BESTÄTIGT** (Widerspruch); Verhalten nicht nachgestellt | `main.py:4771-4779` bucht `self.state.resources["mana"].amount` | Aus `Settlement.vorraete` der aktiven Siedlung zahlen; reicht es nicht → ablehnen mit Fehlbetrag | **11** (Ortslager), **13** (Sperre = 24 **Spielstunden**) |
| **F-04 [P1]** Ansicht prüft andere Quelle als der Kern | **BESTÄTIGT** | `main.py:1948-1957` liest `items.json`/`voraussetzung_struktur`, `True` bei fehlender Struktur; `warenrezepte.json` kennt bei Lederrüstung und Paladinharnisch **zwei** Bedingungen | Eine Prüffunktion für Kern **und** UI, Quelle `warenrezepte.json`; jede Bedingung einzeln anzeigen | — |
| **F-05 [P1]** Abriss lässt Warteschlange weiterlaufen | **BESTÄTIGT** (Code-Review) | `_karten_abreissen` (`main.py:3641 ff.` alt) räumt Bauten, aber keine `werkstaetten[...]` | **Abriss sperren**, solange Aufträge laufen, mit Meldung | **14** |
| **F-06 [P1]** Zweite Werkstatt wirkt verspätet | **BESTÄTIGT** | `spieloekonomie.ware_start:452-460` setzt `kapazitaet` nur beim Einreihen; `ort_tick:631` liest sie nicht neu | Kapazität bei **jedem** Takt aus den gebauten Feldern, ohne rückwirkende Gutschrift | **15** |
| **F-07 [P1]** Ausbildungsprüfung reichsweit, Ausbildung lokal | **BESTÄTIGT** | `main.py:6512` `ausbildungsstaette(self.state.settlements, …)` gegen `main.py:6679` `ausbildungsstaette([ort], …)` | Beide auf die aktive Siedlung; Grund im Klartext nennen | — |
| **F-08 [P1]** Ausbildungsdauer ignoriert die Stufe | **WIDERLEGT — erledigt** | `spieloekonomie.py:589-590` rechnet `grunddauer / max(1, stufe)` | nichts | **18** (Formel bleibt) |
| **F-09 [P1]** Angriff startet immer aus Siedlung 0 | **BESTÄTIGT** | `main.py:5967-5968` `self.state.settlements[0].name`; `_auftrag_entfernung` ebenso | `quelle_id` durch alle Auftragsphasen | — |
| **F-10 [P1]** Sofortangriff und Reiseangriff sind zwei Pfade | **BESTÄTIGT** | `_angriff_durchfuehren:5655 ff.` gegen `_auftrag_angriff:5950 ff.` | Sofortangriff an dieselbe Einsatzregel koppeln | **17** |
| **F-11 [P1]** Beute-/Kostenpfade gemischt | **VERTAGT** | nicht nachgemessen; Risiko plausibel | erst nach F-01/F-03/F-09 messen (Bilanz vor/nach Tick + Save/Load) | — |
| **F-12 [P2]** Warenoberfläche erklärt Blocker nicht | **VERTAGT** (UX-Hypothese) | `_render_storage` zeigt Rezeptdaten nicht | Rezeptkarten, Mengen 1/5/10/max, Bedarfsplaner — **erst nach P1** | **20** |
| **F-13 [P2]** Werkstattstufen-Tempocode wirkungslos | **BESTÄTIGT** | `spieloekonomie.ware_start` ruft `einreihen(..., stufe=1)`; Werkstätten fehlen in `ausbaustufen_hoechstens` | Stufen-Tempocode + UI-Versprechen raus; **Forschung** ist der Ausbau | **16** |
| **F-14 [P2]** Release-/Doku-Status überholt | **VERTAGT** | betrifft README/Übergabetexte, nicht den Code | beim nächsten Release-Push mitziehen (ohnehin erst dann, Entscheidung 12) | **12** |

## Die Reihenfolge (bindend)

1. **`tests/test_produktionskette_ohne_cheats.py`** schreiben — muss **heute rot** sein (Material → Ware → Einheit in Siedlung B → Angriff aus B).
2. **F-01 + F-09 + F-10** zusammen: Ortsheer als einzige Quelle, `quelle_id`, ein Einsatzpfad.
3. **F-04**: eine Prüffunktion für Kern und UI.
4. **F-03**: Portalkosten aus dem Ortslager, Sperre auf 24 **Spielstunden**.
5. **F-05 + F-06**: Abriss gesperrt bei laufender Warteschlange; Kapazität je Takt neu lesen.
6. **F-07 + F-13**: Ausbildungsansicht ortsbezogen; Werkstattstufen-Code entfernen.
7. **F-11** messen (Bilanz), dann entscheiden.
8. Danach der bestehende Plan weiter (P3.4/P3.6 → P4 → Aufräumen → P5 → P1), **F-12 erst nach P1**.

Nach jedem Schritt: Registereintrag, Modulkarte neu, voller Sammellauf, EXE, Protokollzeile.
**Push erst am Ende** (Entscheidung 12), wenn die Berichte eingearbeitet sind und keine Modell-Läufe mehr offen sind.

## Was die Prüfung an Prüfmethodik verlangt (SK-01 bis SK-12, in den Skill übernommen)

Kern in einem Satz: **Ein Test, der den Zwischenzustand selbst schreibt, beweist nicht, dass dieser
Zustand im Spiel entstehen kann.** Daraus folgen: E2E-Kette ohne Cheats als eigenes Gate, eine
Prüffunktion je Bedingung für Kern **und** UI, datengetriebene Vollständigkeit (alle 17 Waren, alle 28
Einheiten aus den Datendateien), Grenzfälle −1/0/Soll/+1, Queue-Systeme als Zustandsautomaten,
Bestandsbilanz vor/nach jeder Mutation, und drei Gesichter je Funktion (Kern, Anzeige, Spielstand).

Die 17-Waren-Matrix und die 14 Ausrüstungs-Einheiten sind **aus den Datendateien** zu erzeugen —
keine zweite, von Hand gepflegte Tabelle.
