# Code-Audit 31.10.2026 — Zusammenfassung, Prüfung der Befunde und Umsetzungsplan

**Auftrag (Daniel, 31.10.2026):** „lasse ein großes model den code checken … kompaktere klügere
code lösungen … alle funktionen unbeeinträchtigt … ordnerstruktur angepasst aber sauber."
Budget: **3 EUR** aus dem DeepSeek-Guthaben.

## 1. Was gelaufen ist (gemessen, nicht geschätzt)

| Paket | Frage | Lauf | Kosten |
|---|---|---|---|
| P2 | Zwei Schlacht-Implementierungen | vollständig, `BEFUND_CODE_P2.md`, 6.986 Zeichen | **0,0351 USD** |
| P5 | Ordnerstruktur des Projekts | vollständig, `BEFUND_CODE_P5.md`, 10.143 Zeichen | **0,0498 USD** |
| P3 | Doppelte Rechenwege (Wirtschaft/Aufträge) | vollständig, `BEFUND_CODE_P3.md`, 9.218 Zeichen | siehe Log |
| P4 | Vier Zeichenmodule der Karten | gestartet, Ergebnis in `BEFUND_CODE_P4.md` | siehe Log |
| P1 | Aufteilung von `main.py` (107 k Token) | **noch nicht gestartet** — nach P4 | offen |

Die ersten Läufe (P5, P3, P4) brachen zuerst an **WLAN-Aussetzern** ab (TimeoutError,
`getaddrinfo failed`) — ohne Kosten, weil keine Antwort ankam. Danach lief die Kette mit
Wiederholung (3 Versuche je Paket, 20 s Pause) sauber durch.

## 2. Was ich selbst nachgeprüft habe (nicht geglaubt, gemessen)

| Behauptung des Modells | Prüfung | Ergebnis |
|---|---|---|
| `kampf_alt_handbuch_2009.py` wird von niemandem importiert | `grep -rn` über `src/`, `tests/`, `tools/` | **stimmt** — nur eine Prüfdatei testete ihre Existenz |
| „`kampf.py` importiert die alte Fassung" | Quelltext gelesen | **falsch** — nur eine Zeile im Docstring erwähnt sie |
| `oberflaeche_original.py`, `gildenrangliste_original.py`, `originalkarten.py`, `originalkarten_grafik.py` sind stilllegbar | `grep` nach Importen | **teilweise falsch**: `originalkarten` wird von 4 Modulen + 6 Prüfdateien benutzt, `originalkarten_grafik` von `main.py`. Nur `gildenrangliste_original` (0 Importe) und `oberflaeche_original` (nur von seiner eigenen Prüfdatei) sind Kandidaten |
| `_als_zahl`, `_als_int`, `_aufzaehlung` stehen doppelt in `auftraege.py` und `kampfbericht.py` | Stichprobe im Code | **stimmt** |
| Zwei Zeichenmodule teilen `_punkte`, `_box`, `_fuell` Zeile für Zeile | AST-Vergleich | **stimmt** (je 3/7/10 Zeilen identisch) |

**Lehre:** Von fünf geprüften Modellbefunden waren drei richtig, einer falsch, einer halb richtig.
Genau deshalb wird jeder Vorschlag vor der Umsetzung nachgemessen — nicht aus Misstrauen, sondern
weil ein Modell den Code liest, aber das Projekt nicht spielt.

## 3. Was in dieser Runde schon umgesetzt ist

**P2 umgesetzt (Commit `298510a`, Register 65):** `src/kampf_alt_handbuch_2009.py` (401 Zeilen)
aus dem Spielcode entfernt, nach `archiv/alter_code/` verschoben (bleibt in der Git-Historie). Die
Prüfung, die ihre Existenz verlangte, dreht sich jetzt um und sichert zu, dass es **genau eine**
Schlachtfunktion gibt. `test_gpt_kampf_forum_neu` 43/0/0. `src/` sinkt von 21.703 auf **21.302**
Zeilen.

**Nicht umgesetzt (bewusst):** gemeinsame Helfer `_punkte`/`_box`/`_fuell` in ein neues Modul
`src/zeichenkern.py` ziehen. technisch gebaut, aber die Prüfdateien fanden das neue Modul nicht
(`ModuleNotFoundError`, obwohl die Datei im Suchpfad lag — Verzeichnis-Cache unter Windows). Der
Gewinn wären 20 Zeilen von 21.300. Aufwand und Risiko stehen in keinem Verhältnis → zurückgenommen,
hier dokumentiert für die nächste Runde (dann zusammen mit P4, wo dieselben Helfer in vier Dateien
stecken).

## 4. Die Befunde in Kurzform

**P3 — doppelte Rechenwege (9.218 Zeichen, umsetzbar in kleinen Schritten):**
1. `_als_zahl`, `_als_int`, `_aufzaehlung` doppelt in `auftraege.py` und `kampfbericht.py` → ein
   gemeinsames `hilfen.py` (38 → 8 Zeilen).
2. Karrenladung wird an drei Stellen unabhängig summiert → `einheiten.ladung_der_gruppe()`.
3. `auftraege.starten` und `_status_zeiten` rechnen dieselbe Reisezeit-Kette → ein `_reise_zeiten`.
4. `spieloekonomie` kopiert Manhattan-Distanz und Importanteil-Formel dreifach → zwei Helfer.
5. Bestandsanwendung ist **ähnlich, aber nicht gleich** (`max(0, …)` vs. Ausnahme) — hier darf
   nicht vereinheitlicht werden, ohne die Regel zu entscheiden.

**P5 — Ordnerstruktur (10.143 Zeichen):** schlägt sechs Themenpakete vor (`kern/`, `kampfsystem/`,
`bot/`, `persistenz/`, `ui/`, `admin/`, `alt/`) mit einzeiligen Kompat-Shims an der Wurzel, damit
Importe und die 98 Prüfdateien weiterlaufen; Umzug in 10 Schritten, nach jedem Schritt lauffähig,
zuletzt `tools/build_exe.py` um `collect_submodules` erweitern.
**Einschränkung:** Das Modell schlägt `__init__.py`-Pakete vor. Das erhöht die Zahl der Dateien und
die Zahl der Stellen, an denen Importe brechen können. Meine Empfehlung: **flacher bleiben** —
Themenordner ohne `__init__.py`-Zwang sind mit Python 3 Namespace-Paketen möglich, aber für
PyInstaller ist die klassische Variante sicherer. Entscheidung gehört zu Daniel, nicht ins Modell.

## 5. Reihenfolge für die Umsetzung (meine Empfehlung)

1. **P3.1–P3.3** (Helfer, Ladung, Reisezeit) — klein, testbar, sofortiger Lesbarkeitsgewinn.
   Beweis je Schritt: `test_auftraege` (143), `test_kampfbericht`, `test_beute_*`.
2. **P4** (Zeichenmodule) — erst wenn P4-Befund da ist; Pixel dürfen sich nicht verschieben.
3. **P5 Schritt 2–4** (Gerüst anlegen, `alt/` stilllegen) — **ohne** Dateien zu verschieben, die
   von mehreren Modulen gebraucht werden (`originalkarten`, `originalkarten_grafik`).
4. **P1** (`main.py` teilen) — zuletzt, größter Hebel, größtes Risiko. Nach jedem Modul ein Commit
   und ein voller Prüflauf.
5. Nach jedem Schritt: Registereintrag, `docs/MODULKARTE.md` neu bauen
   (`python -X utf8 tools/modulkarte_bauen.py`), `tools/sammellauf.py` grün, EXE bauen.

## 6. Kostenstand

| Posten | USD |
|---|---|
| P2 | 0,0351 |
| P5 | 0,0498 |
| P3 | siehe `docs/audits/BEFUND_CODE_P3.md` / Log |
| P4, P1 | offen |

**Budget 3 EUR ≈ 3,20 USD.** Nach den vier Paketen bleiben rund 2,9 USD für die zweite Runde:
Gegenprüfung der Umbauten (Diff-Pakete), ein Paket „was hast du übersehen" und die Endkontrolle der
Ordnerstruktur. Diese Runde wird in einer **neuen Sitzung** gefahren — mit den dann aktuellen
Zeilenzahlen, nicht mit den heutigen.
