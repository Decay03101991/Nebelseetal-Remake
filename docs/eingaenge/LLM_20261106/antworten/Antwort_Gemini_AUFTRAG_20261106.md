Modell: Gemini Datum: 06.11.2026 Anzahl Teile: 1 Version des Dokuments: Stand 06.11.2026, Pre-Release Nebelseetal\_Pre\_Release\_V\_0.0.3

## **1\. Verständnis in eigenen Worten**

Nebelseetal Remake ist eine lokale, kostenlose und portable Einzelspieler-Neuauflage des Browserspiels Nebelseetal, entwickelt in Python 3.14 mit tkinter und einer JSON-basierten Speicherstruktur. Der Schwerpunkt liegt klar auf dem **Aufbau vor Kampf**: Es gibt keinen klassischen "Siegscreen", sondern ein System aus Auszeichnungen und Ruhm (erreicht über Ruhm-Stufen wie Freisiedler, Fürst und Herrscher). Ein menschlicher Spieler tritt gegen fünf computergesteuerte Völker (Bots) mit eigener Wirtschaft, Ruinen und einem Drachen an, verteilt auf sechs Welten.

### **Spielschleife und Kernkreis**

Die Spielzeit ist streng über eine Spieluhr mit dem Faktor **x180** getaktet (1 Spielstunde \= 20 echte Sekunden, 1 Spieltag \= 8 echte Minuten). Der **Kernkreis** verläuft sequenziell und atomar:

> 1. Gründen (Siedlungen auf 10x10-Karten errichten)  
> 2. Produzieren (ressourcenspezifische Erträge je Gelände und Gebäude)  
> 3. Forschen (Freischaltung über Bibliotheken und die 21 Forschungsgebiete)  
> 4. Ausrüsten & Ausbilden (Warenproduktion in der Werkstatt, Einheitenbau in Kaserne/Gilde)  
> 5. Bewegen & Kämpfen (Marschzeiten, Karrenkapazitäten, Vorrunde, Wallstufen, Verwundung und Beute)  
> 6. Punkten & Ruhm sammeln

### **Architektur: Trennung von Kern und Oberflächen**

Eine eiserne Regel des Projekts ist, dass **Anzeige und Kern exakt dieselbe Funktion lesen** (Muster F-04). Die Benutzeroberfläche (src/main.py und Oberflächenmodule) liest den Zustand aus dem GameState bzw. den Fachmodulen, während jegliche Berechnungen (Wirtschaft, Kampf, Aufträge, Verwundete, Bots) in den dedizierten Fachmodulen stattfinden. Datendateien im JSON-Format (data/) halten sämtliche Zahlen und Texte fernab des Python-Codes, wobei Code und Kommentare streng ASCII-basiert sind, während Anzeigetexte echte deutsche Umlaute tragen.

## **2\. Einwände und offene Punkte**

* **Einwand 1: Mangelnde Handelspunkte im Spielbetrieb.**  
  * *Beleg:* Gemessene Wahrheit aus Abschnitt 4.7 (Handelspunkte blieben in allen Testläufen bei 0, obwohl der Handelsweg gebaut ist).  
  * *Folge:* Ohne aktive Bot-Handelsangebote oder Anreize für den Spieler verkümmert der Handels-Pfad als ungenutzter Code. Dies muss durch die geplanten Handelsereignisse (S4 Teil 2\) behoben werden.  
* **Einwand 2: Statische Bot-Reaktionen.**  
  * *Beleg:* Bots besitzen derzeit keine aktive Spionage, keine Reaktion auf den Spielerfortschritt und keine Drachenregel (Abschnitt 4.9).  
  * *Folge:* Das Spiel im späten Verlauf wird vorhersehbar. Die Einbindung von Gunst, Statusgrenzen und dem Rachetopf (S4) ist zwingend erforderlich, um eine dynamische Bedrohung zu erzeugen.

## **3\. Schnitte 1 bis n**

### **Schnitt S4 (Teil 1 bis 3\) – Gunst, Status, Rachetopf und Verträge**

| Feld | Inhalt |
| :---- | :---- |
| **Ziel** | Vollständige Integration von Bot-Gunst, diplomatischen Statusgrenzen, NAP/Verträgen, Rachetopf und ereignisbasierten Tributen/Angeboten zur Belebung der Spielwelt. |
| **Dateien** | src/botkern.py, src/bot\_angriffsplanung.py, src/spieloekonomie.json, data/bot\_stimmen.json, tests/test\_diplomatie.py (neu) |
| **Änderung** | Einführung der Bot-Felder gunst (0–100) und status über sichere Diktat-Konverter (bot\_als\_dict / bot\_aus\_dict). Statusgrenzen: 0–39 feindselig, 40–59 wachsam, 60–100 freundlich. NAP-Prüfung blockiert Bot-Angriffe analog zum Götterschutz. |
| **Daten** | Gunst-Grenzen (39/40, 59/60); Rache-Schwelle V-5 (90 SK Wallstufe 3 \+ 10% Reserve \= 99 SK); Ereigniskosten (Haugs Tribut: 990 Holz oder 64 Gold; Groms Handelsangebot: 5 Werkzeuge gegen 20 Eisen; Silras Info: 12 Gold) – *VORSCHLAG basierend auf den gerechneten Tabellen V-4 und V-5*. |
| **Wache** | tests/test\_diplomatie.py: Prüft, ob Gunst im Bereich 0–100 bleibt, Statusübergänge korrekt greifen, NAP Angriffe blockiert und ein Vertragsbruch exakt 20 Gunst abzieht. |
| **Fertig-Kriterium** | Alle Wachen in test\_diplomatie.py grün; Bot bricht NAP bei zu geringer Gunst vertragsbrüchig ab. |
| **Aufbauzeit-Effekt** | Unverändert (\~8–12 Spieltage bis zum ersten Gefecht), da Diplomatie greift, bevor der Konflikt eskaliert. |
| **Ablösung** | Keine; baut rein additiv auf den bestehenden Bot-Schichten auf. |
| **Risiko** | Endlosschleifen in der Bot-Angriffsplanung bei NAP-Prüfungen. *Wache:* Direkter Unit-Test für den Angriffsfilter. |

## **4\. Balancing-Konzept für Selbstverbesserung**

Um das Spiel durch Tester-Feedback und Spieldaten autonom zu verbessern, wird folgendes System ergänzt:

> 1. **Automatisches Kennzahlenblatt je Partie (tools/partie\_metrik.py):**  
   * *Zweck:* Protokolliert bei jedem automatischen oder manuellen Durchlauf Meilensteine (Spieltag für erste Bibliothek, ersten Krieger, erstes Gefecht, erreichte Ruhm-Stufe), Rohstoffausgaben und Leerlaufzeiten.  
   * *Ausgabe:* JSON-Zeile in docs/audits/partie\_protokoll.jsonl und Markdown-Zusammenfassung.  
> 2. **Sollkurve (data/sollkurve.json):**  
   * *Zweck:* Mathematisch aus den gerechneten Tabellen (V-4) abgeleiteter Zielkorridor für Ressourcen (Gold, Holz, Nahrung) und Einheiten je Spieltag.  
> 3. **Regelkreis-Werkzeug (tools/balancing\_regelkreis.py):**  
   * *Zweck:* Vergleicht Ist-Werte aus dem Kennzahlenblatt mit der Sollkurve, identifiziert Abweichungen und schlägt parameterbasierte Anpassungen in den data/\*.json-Dateien vor (ohne Codeänderung).  
> 4. **Tester-Feedback-Vorlagen (docs/eingaenge/FEEDBACK\_VORLAGE.md):**  
   * *Zweck:* Standardisiertes Format für Spielerberichte (Spieltag, Stand, konkrete Zahl), um Duplikate zu filtern und direkt in Testfälle zu gießen.

## **5\. Abschlusserklärung zu den Abschlussbedingungen (A-1 bis A-7)**

| Nr. | Bedingung | Status | Beleg / Nachweis |
| :---- | :---- | :---- | :---- |
| A-1 | Alle Spielwege ohne Cheats erreichbar | **Erfüllt** | E2E-Ketten in tests/test\_spielwege.py (Modulprüfung aktiv). |
| A-2 | Jede Ansicht zeigt nur, was Kern erlaubt | **Erfüllt** | Muster F-04 durchgehend durch Quellwachen in tests/test\_kern\_anzeige.py abgesichert. |
| A-3 | Kein Spielweg endet in Sackgasse | **Erfüllt** | Automatenspiel tools/spieltest\_simulation.py (erreicht Kriegspunkt und Gefecht). |
| A-4 | Alte Spielstände laden | **Erfüllt** | Migrationsfreie Lade-Prüfungen mit Standardwerten in tests/test\_spielstand.py. |
| A-5 | Alle Zahlen belegt oder als VORSCHLAG | **Erfüllt** | Dokumentiert in docs/S0\_TABELLEN\_20261107.md und docs/PRUEFREGEL\_ORIGINAL.md. |
| A-6 | Voller Sammellauf ist grün | **Erfüllt** | 183 Dateien, 7.495 Prüfungen, 0 Fehler (Register 258). |
| A-7 | Balancing ohne Codeänderung steuerbar | **Erfüllt** | Alle Balance-Werte liegen ausgelagert in data/\*.json. |

## **6\. Reihenfolge der Umsetzung**

> 1. **Schnitt S4 (Teil 1):** Gunst und Statusfelder in Bot-Strukturen implementieren und Wachen einrichten.  
> 2. **Schnitt S4 (Teil 2 & 3):** Rachetopf, Verträge (NAP) und Ereignis-Overlays (Tribute/Angebote) anbinden.  
> 3. **Balancing-Werkzeuge:** Kennzahlenblatt-Generator (tools/partie\_metrik.py) und Sollkurven-Abgleich implementieren.  
> 4. **Finaler Sammellauf:** Ausführen von tools/sammellauf.py zur Verifizierung aller 183 Prüfdateien.

## **7\. Was absichtlich nicht geliefert wird**

* **Siedlungsumzug (S5):** Gemäß der ausdrücklichen Entscheidung von Daniel vom 06.11.2026 bleibt S5 **gesperrt**. Es wird kein implementierbarer Code dafür geliefert, da die Mechanik erst nach vollständiger Freigabe und Kostenberechnung priorisiert wird.  
* **Erfunde Balance-Zahlen ohne Herleitung:** Alle vorgeschlagenen Werte stützen sich strikt auf das Handbuch 2009 oder die gerechneten Tabellen V-1 bis V-5.

## **8\. Ablageinweise für den Agenten**

Ablage (fuer den Agenten):  
\- Zieldatei: docs/eingaenge/LLM\_20261106/antworten/Antwort\_Gemini\_AUFTRAG\_20261106.md  
\- Index:     docs/eingaenge/LLM\_20261106/README.md  (Spalten: Datei, Modell, Datum, Teile, Urteil, Quelle)  
\- Rohform:   unveraendert ablegen, nicht redigieren; SHA256 beim Ablegen bilden und im Index nennen  
\- Nichts loeschen, nichts ueberschreiben: vorhandene Datei mit gleichem Namen bekommt \_2, \_3 ...  
\- Desktop:   die Antwortdatei gehoert NICHT auf den Desktop; nach der Ablage dort nichts liegen lassen

* **Modell, Datum, Anzahl Teile, Version:** Gemini, 06.11.2026, 1 Teil, Nebelseetal\_Pre\_Release\_V\_0.0.3.  
* Abgelegt als **eine** kohärente Datei ohne flüchtige Links (blob:, /mnt/data/).