# AUFTRAG Nr. 3 AN CLAUDE (Opus) - DAS DESIGNPAKET FÜR NEBELSEETAL

Stand 12.11.2026, 00:2x - von Hermes für Daniel Kössl

WAS ICH VON DIR WILL
Ein Gestaltungs-Handbuch, mit dem eine Bild-KI (Pollinations, SDXL, ComfyUI, Flux) ein
VOLLSTÄNDIGES Bildpaket für unser Spiel erzeugen kann - nicht sechs schöne Einzelbilder,
sondern ein System, das überall im Spiel denselben Stil trägt.

Du lieferst KEINEN Code, KEINE Bilder und KEINE Änderung an unserem Repo. Du lieferst ein
Dokument in drei Teilen (siehe Abschnitt 6).

WAS DAS SPIEL IST
- Eigenes Einzelspieler-Remake eines alten Browserspiels ("Nebelseetal"). Python + tkinter,
  Windows-EXE, offline, kostenlos. Kein Netz, kein Server, keine Käufe.
- Fenster im Betrieb typisch 1440 x 900 bis 1920 x 1080, oft maximiert. Alles muss bei 100 %,
  125 % und 150 % Windows-Skalierung lesbar bleiben.
- Sechs Fraktionen ("Häuser"), jedes Spiel beginnt mit der Wahl eines Hauses:
    Haus Silberbach   Menschen  Midgard     Weinrot und Gold
    Haus Hammerhall   Zwerge    Armageddon  Nachtblau, Grau und Gold
    Haus Sternenwacht Elfen     Valhalla    Dunkelgrün und Gold
    Haus Schattenfaust Trolle   Utgard      Violett, Schwarz und Gold
    Haus Knochenmoor  Ghule     Ragnaroek   Blau, Silber und Gold
    Haus Flickwerk    Gnome     Limbus      Karminrot, Silber und Gold
  Diese Namen und Farben sind belegt (data/haeuser.json, Quelle: unsere Chronik der Welt).
- Sechs Weltkarten mit je 20 x 20 = 400 Feldern, neun Rohstoffe (Holz, Stein, Metall, Mana,
  Nahrung, Gold, Wolle, Leder, Pferde) plus Siedler und Punkte.
- Heutige Farben der Oberfläche (belegt, src/main.py, Skin "standard"):
    Hintergrund #2a0605, Fläche #3e1c1a, Kopf-/Seitenleiste #1a0a09, Knopf #3e2723,
    Knopf aktiv #5D4037, Rahmen #4a1512, Gold #FFCC33, Rot #e53935, Text #FFFF99,
    Untertitel #FF6600. Es gibt zwei weitere Skins ("wald", "feuer") - die drei müssen
    als Varianten weiter funktionieren.

WAS DANIEL VERWORFEN HAT (seine Worte, nicht meine Deutung)
- "hässlich ist fast das gesamte spiel noch" - braunes, flaches Feld ohne Tiefe.
- Hintergrundbilder: "gut gewählt aber leider unscharf" - ein weichgezeichnetes Bild als
  Fläche ist keine Gestaltung.
- Ressourcenleiste: "total hässlich, der stil ist jetzt komplett weg" - eine im Code
  gezeichnete Leiste aus Text und Zahl ersetzt kein gemaltes Band.
- Portalansicht: "sehr sehr viel braune Hintergrundfarbe", die Karte soll "schön in die
  mitte des Spielfensters" und "die angaben drumherum gestaltet" werden.
- Angriffsfläche: "viel zu klein gestaltet. ich erkenne kaum die dörfer oder bots ... alles
  braun und lieblos ... hier müssen Erlfische kampfreihen in einer Kaserne oder sowas zu
  sehen sein, mit den kräftigen farben".
- Lage-Band (Forschung/Götterschutz/Wallbau): "völlig lieblos gestaltet", ging rechts über
  den Hintergrund hinaus.
- Menü-Icons: "erkennen Ja und auch relativ gut aber leider sind sie verschoben".
- Grundsatz: "es muss endlich einheitlich werden und es muss von uns selbst sein."

DIE HARTE REGEL: EIGENES WERK
Nichts aus dem alten Spiel kopieren, kein Bild aus dem Netz, keine fremde Marke, keine
bekannten Gesichter. Alles wird neu erzeugt. Die vorhandenen Wappen sind selbst gemalt und
dürfen als Stil-Anker beschrieben, aber nicht nachgebaut werden. Chris' bearbeitete Panoramen
sind die Stilreferenz für Farbe und Licht (kräftige, warme Farben, gemalt, nicht fotorealistisch).

TEIL 1 - DAS SYSTEM (das ist der Kern)
1.1 Stildefinition in Worten, die eine Bild-KI versteht: Materialien, Licht, Perspektive,
    Kontur, Korn, wie Metall und Stein aussehen, wie ein Rahmen gebaut ist. Ein Absatz, den
    man wörtlich in jeden Prompt kopieren kann ("Stil-Block").
1.2 Sechs Fraktionspaletten: je Haus 6 bis 8 Hex-Werte (Grund, Fläche, Rahmen, Akzent,
    Text, Warnung, Erfolg) mit dem Farbton aus der Wappentinktur. Für jedes Paar Text/Fläche
    den Kontrastwert nach WCAG angeben; unter 4,5 : 1 ist unbrauchbar.
1.3 Ein Regelwerk für Rahmen und Flächen (Ecken, Randbreiten in Pixeln, Innenabstand,
    wie ein Bild unter Text liegt, damit Text lesbar bleibt).
1.4 Was STANDARD bleibt (fraktionsneutral) und was je Fraktion anders wird:
    Standard: Hauptmenü/Tor, die linke Menüleiste, die Ressourcenleiste oben, Dialoge.
    Je Fraktion: Dorfansicht und Gebäudehintergründe, Karte, Portal, Angriffsfläche,
    Berichte, Marktplatz, Ruhmeshalle, Ladebild.

TEIL 2 - DIE INVENTARLISTE (das ist die Arbeit)
Eine Tabelle, eine Zeile je Bild. Spalten genau so:
  ID | Ort im Spiel | Dateiname-Vorschlag | Maße in px | Zweck in einem Satz |
  Was auf dem Bild NICHT drauf darf | Prompt (englisch, 1 bis 3 Sätze) | negativer Prompt
Mindestens diese Orte, je Fraktion wo sinnvoll:
  T01 Tor/Startbild (Standard)            1600 x 900
  T02 Ladebild (je Fraktion)              1600 x 900
  T03 Kopfband je Ansicht (Streifen)      Fensterbreite x 150, oben anschließend
  T04 Dorfansicht Hintergrund (je Fraktion, je Gebäude bis 20)   ein Bild je Gebäude
  T05 Karte: Rahmen (9-Slice, 64 x 64 Kachel) und Kachelfeld
  T06 Portal: Kopfband, Weltkartenliste, Kartenausschnitt
  T07 Angriffsfläche: Kasernen-Innenraum (je Fraktion), Feldmarkierung, Einheiten-Plaketten
  T08 Ressourcenleiste: gemaltes Band (Standard) mit 11 Fächern für die neun Rohstoffe,
      Siedler und Punkte - Symbole müssen bei 32 px erkennbar sein
  T09 Menü-Icons links, 32 x 32, neun Stück (Standard)
  T10 Lager: Kacheln für Waren (Holz, Stein, Metall, Mana, Nahrung, Gold, Wolle, Leder,
      Pferde) und Gebäude
  T11 Forschung: Buchrücken/Regal, Fortschrittsband
  T12 Kampfbericht: Kopf, Sieg/Niederlage, Beutezeile
  T13 Marktplatz, T14 Ruhmeshalle, T15 Gildenhalle, T16 Schlachtsimulator
  T17 Knöpfe und Zustände (hell, gedrückt, gesperrt mit Grund) als 9-Slice
  T18 Punkte-/Statusleisten
  T19 Sieg- und Niederlagebild
Für jede Zeile gilt: keine Schrift im Bild (Text zeichnet das Spiel, sonst wird er bei
125 % unscharf), keine Emojis, keine Fotorealistik, kein Wasserzeichen, kein Rahmen im Bild,
wenn das Spiel den Rahmen selbst setzt.

TEIL 3 - DIE PRÜFUNG (damit es nachrechenbar ist)
3.1 Je Bild ein messbares Abnahmekriterium (Kontrast, Mindestgröße eines Symbols,
    Helligkeitsbereich, wie viel tote Fläche erlaubt ist).
3.2 Eine Reihenfolge: welche 12 Bilder zuerst, damit man nach einer Stunde schon spielt
    und nicht erst nach hundert Bildern.
3.3 Eine Liste "das wird NICHT gebraucht" - damit keine Zeit in Bilder geht, die niemand sieht.

FORMAT DER LIEFERUNG
- Eine Datei, UTF-8 mit BOM, .txt, Zeilenenden CRLF, keine Tabellen mit Tabs (Leerzeichen).
- Deutsch, aber alle Bild-Prompts ENGLISCH (die Generatoren verstehen Englisch besser).
- Keine Behauptung über Daniel oder unser Spiel ohne Belegstelle. Wo du etwas vorschlägst,
  schreib "Vorschlag:" davor. Wo du etwas nicht weißt, schreib "weiß ich nicht".
- Keine Zusammenfassung am Anfang, kein Lob, keine Rückfragen ins Leere: wenn etwas fehlt,
  entscheide begründet und markiere die Entscheidung.

WAS DU NICHT TUN SOLLST
- Keine Bilder erzeugen, keine Prompts für Marken oder echte Personen.
- Keine Änderung an data/haeuser.json vorschlagen (Burg/Wappen-Zuordnung ist bewusst offen,
  bis das Paket da ist).
- Keine Ratschläge zur Spielmechanik. Es geht ausschließlich um Gestaltung.
