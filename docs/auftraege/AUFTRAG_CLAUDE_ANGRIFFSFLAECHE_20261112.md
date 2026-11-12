AUFTRAG NR. 4 AN CLAUDE (Klasse Opus 5.5): DIE ANGRIFFSFLAECHE (T07) MIT DEN ECHTEN MASSEN
Stand: 12.11.2026, 10:0x. Von: Hermes Agent, Projekt Nebelseetal Remake. Fuer: Daniel Koessl.
Dieses Dokument ist eine .txt-Datei mit UTF-8 und BOM; Umlaute stehen als echte Umlaute drin.

=====================================================================================
0. WORUM ES GEHT - UND WAS DU ZUERST WISSEN MUSST
=====================================================================================

Du hast am 11.11.2026 ein Gestaltungs-Handbuch fuer dieses Spiel geliefert (19 Orte, sechs
Fraktionspaletten, Kontraste, Prompts). Wir haben es nachgerechnet: 86 von 86 Kontrastwerten
stimmen, die drei Vorab-Befunde stimmen, zwoelf Repo-Belege sind vorhanden. Das Handbuch ist
die Grundlage dieses Auftrags - du musst es nicht neu schreiben.

EINE SACHE WAR DAMALS OFFEN, UND DU HAST SIE SELBST BENANNT (Handbuch, Abschnitt »Was ich nicht
geprueft habe«): die echten Flaechenmasse im laufenden Fenster. Genau die haben wir jetzt
gemessen. Dabei kam heraus, dass dein Eintrag T07 (Angriffsflaeche, 1280 x 720) nicht zur
Wirklichkeit des Spiels passt - nicht in der Groesse und nicht in der Bauart.

Dieser Auftrag schliesst diese Luecke. Er verlangt kein neues Gesamtkonzept, sondern Teil 2 zu
EINEM Ort: der Angriffsflaeche, also der Karte, auf der Doerfer als Marker stehen und angeklickt
werden.

=====================================================================================
1. WAS IN DER ZWISCHENZEIT GEBAUT UND ENTSCHIEDEN WURDE (Stand 12.11.2026)
=====================================================================================

1.1 Die Gebaeudeflaeche ist entschieden: 1142 x 1120 Pixel, Seitenverhaeltnis 1:1.
    Daniel hat am 12.11.2026 auf unsere Empfehlung hin 1142 gewaehlt, deine 1152 sind damit
    abgeloest. Grund: die Flaeche misst im laufenden Fenster genau 1142 px; ein 1152er Bild
    muesste beschnitten oder skaliert werden. Ein Vielfaches von 8 hat in Tkinter keine Wirkung.
    -> ALLE Gebaeudehintergruende werden in 1142 x 1120 gemalt, 1:1 angezeigt.
    -> T07 als Hintergrundflaeche haelt sich an dasselbe Mass.

1.2 Die Portalansicht ist seit 11.11.2026 zweispaltig: links die sechs Weltkarten, rechts die
    Karte mit den Doerfern. Vorher stand die Karte allein in der Mitte eines grossen braunen
    Feldes - das war einer von Daniels Befunden.

1.3 Das Lager (T10) ist gebaut und gemessen: feste Kacheln, grosses Symbol, eigenes Zahlenband.
    Der Befund dort war nicht die Groesse, sondern die Ordnung. Diese Lehre gilt fuer alle
    Kachelflaechen: gleiche Masse, klare Trennung, nichts springt.

1.4 Deine Ressourcenleiste (T08, 1440 x 140) ist noch nicht gebaut. Daniel hat entschieden, dass
    sie aus dem Designpaket kommt und nicht mehr im Code gezeichnet wird.
    -> T08 ist NICHT Teil dieses Auftrags. T07 ist es.

=====================================================================================
2. DIE GEMESSENEN ZAHLEN - DAS IST DER KERN DES AUFTRAGS
=====================================================================================

Alle Zahlen sind am 12.11.2026 im laufenden Programm gemessen, nicht geschaetzt.

2.1 Fenster und Inhaltsflaeche
    Testfenster 1460 x 940 logische Pixel.
    Inhaltsflaeche: 1037 px breit.
    In einem 900 px hohen Fenster bleiben 589 px Hoehe fuer den Inhalt.
    Schmales Fenster (Daniels Fenster ist oft kleiner): 691 px Inhaltsbreite.

2.2 Die Karte der Angriffsflaeche
    Die Karte ist ein Raster aus 20 x 20 Feldern (400 Felder).
    Sie wird als EIN gemaltes Bild gezeichnet, Feld fuer Feld, in gerader Draufsicht.
    Heute: rechte Spalte 449 px breit -> 22 px je Feld -> Karte 440 x 440 px.
    Im Code steht ein Deckel von 46 px je Feld (= 920 px Karte); der greift nur in einem
    hoeheren Fenster. In einem 900-px-Fenster bleibt es bei 440 x 440.

2.3 Die Marker (das ist Daniels Hauptkritik)
    Jedes Dorf ist heute eine Burg mit einem Wappenabzeichen:
      Burg  = 92 Prozent der Feldgroesse  -> bei 22 px Feld: 20 x 20 px
      Wappen = 40 Prozent der Feldgroesse -> bei 22 px Feld: 9 x 9 px
      Am Deckel (46 px Feld): Burg 42 px, Wappen 18 px.
    Daniel sagt dazu: »viel zu klein, ich erkenne kaum die doerfer«.
    Im Teststand standen 4 fremde Doerfer und 3 eigene Doerfer auf der Karte.

2.4 Die Gelaendefarben (dein Befund »alles braun« ist damit belegt)
    Die sieben Gelaendearten haben heute diese Fuellfarben:
      Grasland  #64794A      Steppe   #A98A5C      Wald   #2E4527
      Huegel    #6B563E      Berg     #8E93A6      Nebelsee #41597A
      Sumpf     #474A34
    Vier von sieben liegen im Braun-Oliv-Bereich; der Hintergrund des Spiels ist #2a0605.
    Die Palette ist NICHT belegt (kein Original nennt Farben), sie ist eine Setzung und darf
    ersetzt werden.

2.5 Wer auf der Karte steht
    Sechs Fraktionen (Voelker) mit je einer Burg und einem Wappen:
      menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome.
    Der Spieler traegt das Paar SEINER Fraktion; nach der Voelkerwahl hat kein Bot dieselbe
    Fraktion. Hauptdorf und Nebendoerfer eines Bots tragen dasselbe Paar.
    Dazu kommen auf derselben Karte: Drachen (Figur, nach dem Sieg eine Ruine), laufende
    Maersche (Linie mit Start- und Zielmarke) und die Legende der sieben Gelaendearten.

2.6 Die sechs Haeuser (Spielerhaeuser)
    Sie stehen in data/haeuser.json und bleiben UNBERUEHRT. Die Fraktionen der Bots sind eine
    andere Achse als die Haeuser; verwechsle beide nicht.

=====================================================================================
3. WAS DANIEL SAGT (woertlich, damit du den Massstab kennst)
=====================================================================================

Zu dieser Flaeche, Testbogen V_0.0.4 vom 11.11.2026:
  »die angriffsflaeche ist viel zu klein, ich erkenne kaum die doerfer«
  »alles braun«
  »ich will fraktionsgestaltung«

Zum Lager (gleicher Bogen, inzwischen gebaut):
  »besser aber immer noch nicht uebersichtlich und schoen genug gestaltet«

Zum Stil, aus deinem eigenen Handbuch uebernommen und von uns akzeptiert:
  digitale Malerei, stylized realism, warmes Gegenlicht, kuehle Schatten, Nebel,
  hoher Materialdetailgrad, keine schwarzen Konturen, kein 3D-Render.

=====================================================================================
4. DEIN AUFTRAG - FUENF TEILE, ALLE MIT MASSEN
=====================================================================================

TEIL A - GELAENDEKACHELN STATT PANORAMA (wichtigste Korrektur)
    Die Karte ist KEIN einzelnes Panorama, sondern ein Raster aus 400 Feldern, das aus sieben
    Gelaendearten zusammengesetzt wird. Du brauchst also keine 1280-x-720-Szene, sondern
    sieben KACHELN, die sich nahtlos aneinanderlegen lassen.
    Liefere:
      A1  Sieben Gelaendekacheln (Grasland, Steppe, Wald, Huegel, Berg, Nebelsee, Sumpf),
          quadratisch, 64 x 64 px als Master, gedacht zur Anzeige bei 22 bis 46 px.
          Anforderungen: nahtlos kachelbar (Kanten muessen aneinander anschliessen),
          Unterscheidbarkeit auch bei 22 px, KEINE harten schwarzen Konturen, gedaempft
          genug, dass ein 20-px-Marker darauf noch auffaellt.
      A2  Fuer jede Kachel einen englischen Prompt (Stil-Block plus Motiv plus Negativ-Block)
          und eine Angabe, woran man erkennt, dass die Kachel gelungen ist.
      A3  Eine Empfehlung mit Zahlen: welche Fuellfarbe jede Kachel im Durchschnitt haben
          soll (Hexwert), damit die sieben Arten auch in der Legende als Farbquadrat von
          2 x 1 Zeichen unterscheidbar bleiben.

TEIL B - DAS MARKERSYSTEM (Daniels »ich erkenne kaum die doerfer«)
    Liefere ein System, das bei 20, 22, 30, 42 und 46 px Feldgroesse funktioniert:
      B1  Drei Groessenstufen des Markers mit exakten Pixelmassen: klein (Feld 22 px),
          mittel (Feld 30 px), gross (Feld 46 px). Sag fuer jede Stufe, welche Bestandteile
          WEGGELASSEN werden - nicht, wie man alles hineinquetscht.
      B2  Sechs Fraktionsmarker, unterscheidbar OHNE Farbe allein (Form oder Wappenform),
          damit es auch bei Farbsehschwaeche funktioniert. Nenne je Fraktion das Unterscheidungs-
          merkmal in einem Satz.
      B3  Der eigene Marker des Spielers muss auf einen Blick anders sein als jeder Bot-Marker
          (Vorschlag mit Begruendung).
      B4  Zwei Zustaende: ausgewaehlt (angeklickt) und bedroht (ein Marsch ist unterwegs).
          Beides muss bei 22 px noch sichtbar sein.
      B5  Ein Marschpfeil (Linie plus Spitze) und eine Drachenmarke, die sich von den sechs
          Fraktionsmarkern nicht verwechseln lassen.
      B6  Eine Regel fuer den Fall, dass zwei Marker auf einem Feld liegen (Dorf plus Drache,
          Dorf plus Marschziel): wer gewinnt die Anzeige, und was passiert beim Klick.

TEIL C - DAS LAYOUT DER ANGRIFFSFLAECHE MIT DEN ECHTEN MASSEN
    Entwirf die Ansicht fuer die gemessenen Flaechen, nicht fuer 1280 x 720:
      C1  Bei 1037 px Inhaltsbreite und 589 px Hoehe (Fenster 900 px hoch).
      C2  Bei 691 px Inhaltsbreite (schmales Fenster) - was entfaellt dann, was bleibt?
      C3  Nenne die Aufteilung in Pixeln: Kartenflaeche, Kopfzeile, Seitenleiste, Legende,
          Fusszeile. Sag ausdruecklich, was NICHT auf den Schirm darf.
      C4  Entscheide begruendet: Karte gross und Angaben drumherum, oder Karte plus Liste
          nebeneinander wie heute? Wenn du etwas ganz anderes fuer richtig haeltst, sag es -
          aber mit Zahlen und mit dem Preis (was der Spieler dann nicht sieht).
      C5  Der Weg zur Karte ist heute: Portal oeffnen, Bot-Dorf anklicken, »Angriff planen«
          waehlen. Wenn dein Layout diesen Weg aendert, beschreibe den neuen Weg in Schritten.

TEIL D - FARBE UND KONTRAST
      D1  Bleib bei deiner Palette aus Teil 1.2 deines Handbuchs. Keine neuen Farben, ausser du
          begruendest eine und nennst ihren Kontrastwert.
      D2  Rechne die Kontraste fuer JEDEN Text und jede Marke gegen den Grund, auf dem sie
          liegt (Karte, Panel, Kopfzeile). Ziel: Text mindestens 4,5 zu 1, grafische Zeichen
          mindestens 3 zu 1.
      D3  Nenne fuer die sieben Gelaendekacheln je einen Kontrastwert gegen einen Marker in
          Gold und gegen einen Marker in Fraktionsfarbe. Wenn einer unter 3 zu 1 liegt, sag
          welcher und was du stattdessen vorschlaegst.

TEIL E - REIHENFOLGE UND ABNAHME
      E1  Eine Reihenfolge: welche Bilder zuerst, welche spaeter. Hoechstens acht Motive fuer
          den ersten Durchgang.
      E2  Fuenf bis zehn messbare Abnahmekriterien. Beispiele fuer die Art, die wir brauchen:
          »ein 22-px-Marker ist von einem 22-px-Marker einer anderen Fraktion ohne Farbe
          unterscheidbar«, »kein Text unter 4,5 zu 1 Kontrast«, »die Kachelkanten schliessen
          ohne sichtbare Naht aneinander«.
      E3  Sag zu jedem Kriterium, WIE man es prueft (Auge, Rechnung, Messung im Programm).

=====================================================================================
5. REGELN - WAS DU NICHT TUN DARFST
=====================================================================================

  5.1 KEIN Code. Keine Python-Zeilen, keine Tkinter-Anweisungen. Wir bauen, du gestaltest.
  5.2 KEINE Aenderung an data/haeuser.json und keine neuen Zahlen fuer Spielmechanik
      (Ertrate, Kosten, Kampfwerte, Zeiten). Die kommen aus dem Originalhandbuch.
  5.3 KEINE fremden Bilder, keine Marken, keine echten Personen, keine Gesichter im
      Vordergrund, kein Blut - das sind deine eigenen Negativ-Regeln, sie gelten weiter.
  5.4 KEINE erfundenen Massangaben. Wenn du etwas nicht weisst, schreib UNBEKANNT und sag,
      welche Zahl wir messen sollen. Eine geratene Zahl ist fuer uns schlimmer als eine Luecke.
  5.5 KEINE Dateien, keine Downloads. Antworte im Chat; wir schneiden den Text selbst.
  5.6 Verwechsle Haeuser (Spieler, sechs) und Voelker/Fraktionen (Bots, sechs) nicht.

=====================================================================================
6. WAS WIR MIT DEINER ANTWORT TUN
=====================================================================================

  - Wir rechnen jeden Kontrastwert nach (wie bei deinem Handbuch: 86 von 86). Abweichungen
    ueber 0,05 nennen wir beim Namen.
  - Wir messen jeden Groessenvorschlag im laufenden Fenster nach. Was bei 22 px nicht lesbar
    ist, geht zurueck an dich.
  - Was gebaut wird, entscheidet Daniel. Deine Empfehlung ist eine Empfehlung.

=====================================================================================
7. ANHANG - BELEGE UND PFADE
=====================================================================================

  Dein Handbuch:      docs/eingaenge/CLAUDE_20261112_DESIGNPAKET/
                      claude_designpaket_handbuch_20261112.md (62.411 Byte)
  Unsere Nachrechnung: docs/design/PRUEFUNG_CLAUDE_DESIGNPAKET_20261112.md (86/86 Kontraste)
  Gebaeudeflaeche:    1142 x 1120 px, Entscheidung Daniel 12.11.2026 (Register 469)
  Fraktionen/Marker:  data/bot_wappen.json (92 Prozent Burg, 40 Prozent Wappen, sechs Paare)
  Gelaendefarben:     data/gelaende.json und portalraum.legende() (sieben Arten)
  Haeuser:            data/haeuser.json (unberuehrt)
  Daniels Testbogen:  docs/audits/TESTBOGEN_V_0.0.4_20261111.txt
  Daniels Testbilder: docs/eingaenge/DANIEL_20261111_TEST_V004/screenshots/ (sieben PNG)
  Fraktionsbild:      docs/eingaenge/DANIEL_20261112_ALLE_FRAKTIONEN/ (1086 x 1448, hochkant)

Ende des Auftrags.
