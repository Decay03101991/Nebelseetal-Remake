# Belege: Forschung global oder je Siedlung?

**Frage:** Ist die Forschung im Original ein **globaler Vorrat für alle Siedlungen** oder **je Siedlung eigen**?

**Hauptquelle (Wahrheit):** `docs/original/Spielanleitung_2009_Textfassung.txt` (Original-Handbuch 2009).
Bei Widerspruch zwischen Handbuch und allem anderen **gewinnt das Handbuch**.
Zusätzliche Quellen: `docs/original/ORIGINAL_*.md`, `src/forschung.py`, `src/main.py`,
`src/gebaeude_wirkung.py`, `src/wirtschaft.py`, `data/research.json`, `data/buildings.json`.

Zitatformat: `Z. <nr>: „<Zitat>“` = Zeilennummer in `Spielanleitung_2009_Textfassung.txt`.

> **Hinweis zum Umfang:** `src/wissenschaft.py` und `data/forschung*.json` existieren **nicht**.
> Es gibt nur `data/research.json` (21 Forschungen) und `src/forschung.py` (+ `forschung_wirkung.py`,
> `forschungspfad.py`).

---

## 1. Global oder je Siedlung? — die Handbuchstellen

### 1a. Was das Handbuch JE SIEDLUNG bindet (belegt)

Die **Forschungsstätte** (Bibliothek) ist ausdrücklich je Siedlung:

- `Z. 400: „Um Forschung zu betreiben musst Du in Deiner Siedlung zunächst eine Bibliothek bauen.“`
- `Z. 403: „Sie kann nur auf Grasland, Steppe oder Nebelseen errichtet werden.“`
- `Z. 404: „In jeder Siedlung kann nur eine einzige Bibliothek gebaut werden.“`
- `Z. 405: „Verfügt Deine Siedlung über eine Bibliothek, erscheint im Siedlungsmenü der Button „Forschung“.“`
- `Z. 407: „... solange Deine Gelehrten nicht mit Studien beschäftigt sind, die Bibliothek ausbauen, oder einen Forschungsauftrag erteilen.“`

Der **laufende Forschungsauftrag** und seine **Sperre** sind ausdrücklich je Siedlung:

- `Z. 423-424: „Während dieser Zeit kannst Du in der Siedlung, in der geforscht wird, weder die Bibliothek ausbauen, noch einen weiteren Forschungsauftrag erteilen.“`
- `Z. 439-440: „Während dieser Zeit, ist in der Siedlung, in der geforscht wird, der gesamte Forschungsbereich blockiert. Du kannst dort lediglich noch den Fortschritt der Studien beobachten ...“`

Mehrere Siedlungen können **je eigene** Forschungen laufen haben (Plural):

- `Z. 245: „Außerdem werden hier die in den Siedlungen laufenden Forschungen angezeigt.“`

**→ Stärkster wörtlicher Beleg für „je Siedlung“: Z. 423-424.** Die Formulierung „in der Siedlung,
in der geforscht wird“ verortet den Auftrag und die Sperre eindeutig in **einer** Siedlung.

### 1b. Was im Handbuch eher auf GLOBAL (Volk/Spieler) deutet (belegt, aber nicht eindeutig „Vorrat“)

- `Z. 104-106: „Um Einheiten auszubilden, Gebäude zu bauen, Waren zu produzieren und Forschungen zu betreiben muss Dein Volk bestimmte Voraussetzungen, wie Gebäudestufen oder Forschungsstufen erfüllen.“`
  → Forschungsstufen werden dem **„Volk“** zugeschrieben (nicht der einzelnen Siedlung).
- `Z. 397: „Manche von ihnen erhöhen die Produktivität Deiner Siedlungen, andere ermöglichen den Bau neuer Gebäude und Einheiten oder steigern die Effektivität Deiner Kampfeinheiten.“`
  → Wirkung auf **„Deine Siedlungen“** (Plural) — liest sich als **globaler** Effekt.
- `Z. 123-125: „Für jede Forschung die Du erlangt hast, wird die Forschungsstufe hoch drei genommen. Die so gewonnenen Werte, werden anschließend addiert und ergeben Deine Forschungspunkteanzahl.“`
  → Punktestand wird über alle Forschungen **des Spielers** summiert, **ohne** Aufteilung je Siedlung.
- `Z. 448-449: „... erhöht sich die Stufe des Forschungsprojekts um 1.“` — ein „Forschungsprojekt“, nicht je Siedlung getrennt benannt.

---

## 2. Was kostet Forschung, woher kommt der Ertrag? (belegt)

**Kosten** — Rohstoffe aus dem Siedlungsbestand, verdoppeln sich je Stufe:

- `Z. 450-452: „Die Rohstoffkosten die zum Forschen aufgebracht werden müssen, verdoppeln sich pro Stufe. Das bedeutet, wenn Du für eine Forschung Stufe1 50Holz benötigst, benötigst Du für Stufe2 100Holz, für Stufe3 200Holz, für Stufe4 400Holz usw.“`
- `Z. 431-433: „... werden die für die Forschung benötigten Ressourcen von Deinem Siedlungsbestand abgezogen. Die Gelehrten machen sich sofort daran ...“`
- `Z. 418-419: „Die benötigten Ressourcen werden sofort zum experimentieren in die Bibliothek geschafft und Deine Gelehrten beginnen mit ihren Studien.“`

**Dauer** — neue Stufe im Quadrat, in Stunden:

- `Z. 422-423: „Ein Forschungsauftrag dauert (Neue Stufe*Neue Stufe) in Stunden.“`
- `Z. 438-439: „... wird das 9 Stunden in Anspruch nehmen. (3 * 3 = 9)“`

**Ertrag** — Das Handbuch nennt **keinen** Ertrag je Stunde für Forschung. Es nennt keinen
„Forschungs-Rohstoff“ und keinen Ertrag pro Gelehrtem. Was es nennt:

- `Z. 31: „Deine Gelehrten betreiben Forschungen in der Bibliothek.“` (keine Stückzahl, kein Unterhalt)
- `Z. 409-410: „Das Ausbauen der Bibliothek erfolgt in Stufen. Mit jeder Stufe, die Deine Bibliothek ausgebaut wird, stehen Dir weitere Forschungsmöglichkeiten in ihr offen.“`
- `Z. 414-415: „... um die Stufe der Bibliothek um 1 zu erhöhen. Der Ausbau wird mit jeder Stufe teurer.“`
- Bonus auf **Produktionsgebäude** (Wirkung, nicht Ertrag der Forschung selbst): `Z. 56-57: „Mit den Rohstoffen kannst Du dann forschen, um z.B. Deine Rohstoffproduktion zu steigern, oder neue Rohstoffe zu ermöglichen (z.B. Wolle oder Gold).“`

**→ SCHWEIGT DAS HANDBUCH:** Es gibt kein Gebaeude und keine Einheit, die „Forschung“ als
Rohstoff/Ertrag je Stunde erzeugt. Erträge entstehen nur **indirekt** als Produktionsboni.

---

## 3. Was schaltet Forschung frei? — JEDE Handbuchstelle (belegt)

**Gebäude (Baukunst):**

- `Z. 279-281: „... Holzfäller, Steinmetze, Jäger, Bibliothek und Häuser können bereits ohne Forschungen gebaut werden, für die restlichen Gebäude benötigst Du Kenntnisse in der Forschung „Baukunst“).“`

**Nahkampf-Einheiten (Kriegerakademie) — „Kriegskunst“:**

- `Z. 557: „Kriegskunst 1“` (Kämpfer)
- `Z. 575: „Kriegskunst 3“` (Krieger)
- `Z. 593: „Kriegskunst 7“` (Ritter)
- `Z. 613: „Kriegskunst 10“` (Paladin)

**Fernkampf-Einheiten (Kriegerakademie) — „Kriegskunst“:**

- `Z. 629: „Kriegskunst 2“` (Kurzbogenschütze)
- `Z. 645: „Kriegskunst 4“` (Bogenschütze)
- `Z. 661: „Kriegskunst 6“` (Langbogenschütze)
- `Z. 678: „Kriegskunst 8“` (Armbrustschütze)

**Kundschafter (Diebesgilde) — „Heimlichkeit“:**

- `Z. 727: „Heimlichkeit 1“` (Gauner)
- `Z. 744: „Heimlichkeit 3“` (Dieb)
- `Z. 761: „Heimlichkeit 5“` (Meisterdieb)
- `Z. 796: „Heimlichkeit 8“` (Kundschafter)
- `Z. 813: „Heimlichkeit 10“` (Waldläufer)

**Karren und Belagerungswaffen (Stellmacher) — „Wagenbau“:**

- `Z. 864: „Wagenbau 3“`, `Z. 883: „Wagenbau 7“`, `Z. 903: „Wagenbau 2“`, `Z. 924: „Wagenbau 6“`,
  `Z. 944: „Wagenbau 1“`, `Z. 961: „Wagenbau 4“`, `Z. 977: „Wagenbau 5“`, `Z. 993: „Wagenbau 6“`,
  `Z. 1026: „Wagenbau 7“`, `Z. 1042: „Wagenbau 8“`, `Z. 1058: „Wagenbau 9“`, `Z. 1074: „Wagenbau 10“`

**Allgemeine Aussage + weitere Forschungen:**

- `Z. 396-397: „Forschungen sind wichtige Voraussetzungen, für Einheiten, Waffen, Gebäude und weitere Forschungsmöglichkeiten.“`
- `Z. 411: „Mit jeder Stufe, die Deine Bibliothek ausgebaut wird, stehen Dir weitere Forschungsmöglichkeiten in ihr offen.“`
- `Z. 463-464: „Bedenke das Du zum Bau dieser Gebäude bestimmte Voraussetzungen erfüllen musst. Diese kannst Du im Hauptmenü unter „Voraussetzungen“ einsehen.“` (Werkstätten Schmiede/Nähstube/Bogenbauer)

**Waren-Voraussetzungen (Waffentechnik / Rüstungsbau / Nähkunst / Magiekunde):**
Diese stehen **nicht** im lesbaren Text der Textfassung (die Waren-Tabellen sind beim PDF-Auslesen
zerlaufen). Sie sind nur in `docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md`, Abschnitt 3,
Zeilen 113-129 belegt (z. B. `Z. 115: „| Schmiede | Kurzschwert | Waffentechnik 3 |“`,
`Z. 118: „| Schmiede | Kettenhemd | Rüstungsbau 3 |“`, `Z. 120: „| Schmiede | Magischer Paladinharnisch | Rüstungsbau 7 + Magiekunde 2 |“`).
→ **Nicht wörtlich aus dem Handbuchtext zitierbar**; die konkreten Waren-Bedingungen gelten als
„aus ORIGINAL-Doc, Spaltenzuordnung noch am Druck zu prüfen“.

---

## 4. Läuft nur EINE Forschung oder mehrere parallel? (belegt)

- `Z. 407: „... solange Deine Gelehrten nicht mit Studien beschäftigt sind, die Bibliothek ausbauen, oder einen Forschungsauftrag erteilen.“`
- `Z. 423-424: „Während dieser Zeit kannst Du in der Siedlung, in der geforscht wird, weder die Bibliothek ausbauen, noch einen weiteren Forschungsauftrag erteilen.“`
- `Z. 439-440: „Während dieser Zeit, ist in der Siedlung, in der geforscht wird, der gesamte Forschungsbereich blockiert.“`

**Lesart (belegt):** Pro Siedlung/Bibliothek **genau EIN** Forschungsauftrag gleichzeitig; während
der Studien ist der gesamte Forschungsbereich dieser Siedlung gesperrt.

**Nicht wörtlich belegt:** dass zwei Siedlungen **wirklich gleichzeitig** forschen dürfen. Der
Plural in `Z. 245: „... die in den Siedlungen laufenden Forschungen ...“` legt es nahe, sagt es aber
nicht ausdrücklich. → siehe Abschnitt „Offene Fragen“.

---

## 5. Was passiert beim Verlust einer Siedlung? (HANDBUCH SCHWEIGT)

Einzige Stelle, die den Verlust einer Siedlung beschreibt, ist „Siedlung aufgeben“:

- `Z. 321-323: „Wenn Du mehr als eine Siedlung besitzt, kannst Du eine der Siedlungen aufgeben. ... Nach einer erneuten Sicherheitsabfrage wird die Siedlung gelöscht.“`
- `Z. 324-326: „Bedenke aber, dass das Löschen nicht rückgängig gemacht werden kann und dabei ALLE Einheiten, Waren, Gebäude und Ressourcen der Siedlung verloren gehen!“`

Die Aufzählung nennt **Einheiten, Waren, Gebäude, Ressourcen** — **Forschungen/Forschungsstufen
werden NICHT genannt.**

Auch der Kampf-Verlust nennt nur anderes:

- `Z. 1334-1335: „Der Verlierer verliert einen Teil seiner stationierten bzw. mitgeschickten Karren und Belagerungswaffen.“`
- `Z. 1332: „Falls er Transportkarren in seiner Angriffstruppe mitführt, beginnen diese die Siedlung zu plündern.“`

**→ SCHWEIGT DAS HANDBUCH:** Ob Forschungsstufen beim Verlust/Aufgeben einer Siedlung verloren
gehen oder erhalten bleiben, **sagt das Handbuch nicht**. (Offene Frage an Daniel.)

---

## 6. Vergleich mit dem IST im Code (Datei + Zeile, keine Behauptungen)

### 6a. `src/forschung.py` — reine Rechenlogik (kein Siedlungsbezug im Datenmodell)

- Kosten delegiert: `Z. 56-58` `kosten()` → `spieldaten.forschungs_kosten`.
- Dauer: `Z. 41-49` `dauer_stunden()` = Stufe² (delegiert an `spieldaten.forschungsdauer_stunden`).
- Bibliothek ist Pflicht, aber nur **ein bool**: `Z. 125-126` `if not hat_bibliothek: return False, "Forschung braucht eine Bibliothek."`
- **Sperre ist GLOBAL über den übergebenen `stand`**, nicht je Siedlung:
  `Z. 130-134: laufend = [name for name, eintrag in stand.items() if eintrag.get("auftrag") is not None]` →
  `if laufend: return False, ("In dieser Siedlung forscht bereits ...")`.
  → Die **Meldung** sagt „In dieser Siedlung“, aber die **Funktion kennt keine Siedlung** — sie
  sperrt jede weitere Forschung im ganzen übergebenen `stand`.
- Stufe steigt erst nach Ablauf: `Z. 192-206` `abschliessen()`; Abbruch verloren: `Z. 209-222`.
- Forschungspunkte = Stufe³: `Z. 225-227` `punkte()`.
- Eigener Hinweis im Modul: `Z. 15-20` (Doku-Kommentar) „Ein laufender Auftrag sperrt die GANZE
  Siedlung ... mit mehreren Siedlungen je eigener Bibliothek gilt die Sperre je Siedlung.“ →
  das ist eine **Auslegung/Annahme**, kein Zitat.

### 6b. `src/main.py` — der Forschungsstand wird GLOBAL (auf dem Spieler) gehalten

- `class GameState` bei `Z. 508`; darin `Z. 517: self.research: Dict[str, Research] = ...` und
  `Z. 567: self.forschungsauftraege: Dict[str, dict] = {}` — **ein** Bestand für den **ganzen Spieler**.
- `class Settlement` `Z. 161-180` hat **kein** Forschungsfeld (nur `buildings`, `units`, `karte`, `bauten`, `stufen`).
  → Forschungsstufen sind **nicht** an der Siedlung gespeichert.
- `forschung_stand()` `Z. 905-912` baut aus `self.research` **einen** (globalen) Stand.
- Bibliotheks-Prüfung: `Z. 1657` und `Z. 1714` rufen `gebaeude_wirkung.forschung_erlaubt(self.state.settlements)`;
  `forschung_erlaubt` (`src/gebaeude_wirkung.py` `Z. 198-203`) fragt `bibliothek_stufe(siedlungen)`,
  und `bibliothek_stufe` (`Z. 189-191`) liefert `max(... )` = **irgendeine** Siedlung mit Bibliothek
  genügt → **globaler** Freischalter.
- Ausbau-Sperre ebenfalls global: `Z. 1930-1934` („Die Bibliothek ist die eine Forschungsstätte,
  also gilt die Sperre, solange irgendein Forschungsauftrag läuft.“).
- Wirkung ebenfalls global: `Z. 715-716` `wirtschaft.ertrag_gesamt(self.settlements, levels)`
  mit `levels` aus `self.research` für **alle** Siedlungen (`src/wirtschaft.py` `Z. 150-156`).
- `data/research.json` `"regeln"` fasst zusammen: `"blockiert": "Forschungsbereich der Siedlung waehrend der Studien"` (Formulierung je Siedlung, Logik global).

### 6c. BELEGT vs. NICHT BELEGT im Code

| Aussage im Code | Status |
|---|---|
| Dauer = Stufe² Stunden | **BELEGT** (`Z. 422-423`, `Z. 438`) |
| Kosten verdoppeln sich je Stufe (50/100/200/400) | **BELEGT** (`Z. 450-452`) |
| Stufe steigt erst nach Ablauf der Zeit | **BELEGT** (`Z. 446-449`) |
| Abbruch: Zeit und Ressourcen verloren | **BELEGT** (`Z. 425-426`, `Z. 443-445`) |
| Forschung braucht eine Bibliothek | **BELEGT** (`Z. 400`, `Z. 405`) |
| Forschungspunkte = Σ Stufe³ | **BELEGT** (`Z. 123-125`) |
| Bibliothek nur Grasland/Steppe/Nebelsee, eine je Siedlung | **BELEGT** (`Z. 403-404`) |
| Während der Studien ist der Forschungsbereich blockiert | **BELEGT** — aber **je Siedlung** (`Z. 423-424`, `Z. 439-440`) |
| ForschungsSTAND wird als **ein globaler Vorrat** geführt (`GameState.research`, `GameState.forschungsauftraege`) | **NICHT BELEGT** — Handbuch bindet Bibliothek und laufende Forschung an die Siedlung; ein globaler Vorrat ist nirgends wörtlich |
| Sperre gilt **global über alle Siedlungen** (`forschung.py` `Z. 130-134`) | **NICHT BELEGT** — Handbuch sagt „in der Siedlung, in der geforscht wird“; zu Mehrfach-Siedlungen schweigt es |
| Meldung „In dieser Siedlung forscht bereits ...“ obwohl die Funktion keine Siedlung kennt | **Irreführend** — Code-Wortlaut passt nicht zur Funktionssignatur |

---

## VORSCHLAG (nicht belegt, zur Entscheidung — nichts davon ist umgesetzt)

- **V1:** Forschungsstand **je Siedlung** speichern (Feld an `Settlement`), Bibliothek-Stufe je Siedlung als Freischalter, Sperre je Siedlung; Punktesumme weiter global. Begründung: `Z. 404`, `Z. 423-424`, `Z. 245`.
- **V2:** Forschungsstand **global** lassen, aber die Sperre je Siedlung anwenden (die Bibliothek ist die Stätte). Begründung: `Z. 104-106` („Dein Volk“), `Z. 397` („Deine Siedlungen“).
- **V3:** Meldung in `src/forschung.py` `Z. 132` neutral formulieren, solange die Funktion keinen Siedlungsparameter hat.

---

## SCHWEIGT DAS HANDBUCH (offene Fragen an Daniel)

1. Ist die **Forschungsstufe** (der erreichte Wert einer Forschung) ein **globaler Wert für das Volk** oder **je Siedlung** eigen? Das Handbuch bindet Bibliothek + laufenden Auftrag an die Siedlung (`Z. 404`, `Z. 423-424`), schreibt die Stufen aber dem „Volk“ (`Z. 104-106`) und die Wirkung „Deinen Siedlungen“ (`Z. 397`) zu. **Kein wörtlicher Satz entscheidet es.**
2. Dürfen **zwei Siedlungen gleichzeitig** forschen? Der Plural `Z. 245` legt es nahe, sagt es aber nicht ausdrücklich; `Z. 423-424`/`Z. 439-440` sind jeweils auf „die Siedlung, in der geforscht wird“ beschränkt.
3. Sind **Forschungsstufen beim Verlust/Aufgeben** einer Siedlung weg oder bleiben sie? `Z. 324-326` nennt nur Einheiten, Waren, Gebäude, Ressourcen — **Forschung nicht**.
4. Gibt es **Ertrag/Menge** der Gelehrten je Stunde? Das Handbuch nennt keinen (`Z. 31` nur „betreiben Forschungen“).

---

*Erstellt 2026-10-05. Nur gelesen, nichts geändert. Diese Datei ist neu und die einzige angelegte Datei.*
