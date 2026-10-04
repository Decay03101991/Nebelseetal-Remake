# Auftrags- und Botschaftersystem — Entwurf (geprüft)

**Quelle:** `deepseek-v4-pro`, 4 m 16 s, Rohantwort in `docs/audits/design_auftraege.txt`.
**Prüfung:** Jede Seitenangabe habe ich anschließend im Handbuch nachgeschlagen. Ergebnis unten.
Alles, was nicht belegt ist, steht ausdrücklich als **VORSCHLAG** — diese Teile brauchen Daniels
Entscheidung.

---

## Auftragsarten und was gespeichert wird

| Auftrag | Belegte Regeln (Handbuch) |
|---|---|
| **Stationieren** | In **fremden** Siedlungen verboten (S. 19, wörtlich: „nicht möglich, Einheiten in fremden Siedlungen zu stationieren"). Waren nur mit Karren mitnehmbar. |
| **Spionage** | Kundschafter sehen sich um; ein Bericht kommt immer zurück (S. 24). Die Werte SI/HE haben laut Handbuch „noch keinen Einfluss auf das Spiel" (S. 18). |
| **Transportieren** | Nur Handkarren (40), Einspänner (100), Zweispänner (250) — Ladung wörtlich in den Einheitentabellen. Rückkehr vorgesehen. |
| **Handeln** | Nur Handelskarawanen. Bestätigung oder Ablehnung; bei Ablehnung kehrt die Karawane **mit den Waren** zurück, das Gold wird nie übertragen (S. 20). |
| **Angriff** | Wall-Vorrunde, dann Kampfsequenzen (S. 21–22). Beute **nur**, wenn Transportkarren mitgeführt werden (S. 23, wörtlich: „Transportkarren in seiner Angriffstruppe mitführt, beginnen diese die Siedlung zu plündern"). |

Gemeinsam: Auftragsart, Status (laufend / abgeschlossen / gescheitert), Startsiedlung, Ziel,
Einheiten, Reisedauer, Geschwindigkeit (in 10-%-Schritten drosselbar, S. 20), Kosten in Gold und
Nahrung, **Mana nur bei fremden Zielen** (S. 20), und die Dauer gilt **für eine Strecke**
(S. 19, wörtlich: „Wenn also 2 Stunden angegeben sind, benötigen Deine Einheiten 2 Stunden").

## Ablauf

1. Start: Kosten werden sofort abgezogen, Einheiten reisen los.
2. Hinreise: die angegebene Dauer.
3. Handlung am Ziel: stationieren · spionieren · abladen · auf Bestätigung warten · angreifen.
4. Rückkehr: **doppelt so lange wie eine Strecke** (S. 19). Bericht im Nachrichtenmenü (S. 4).

## Bot-KI (übernimmt die anderen Spieler)

**Verteidigen:** deterministisch nach Handbuch — keine eigene Logik nötig (Wall-Vorrunde S. 21,
höchstens zehn Sequenzen S. 22).

**Angriffsregeln der Bot-KI:** Sie darf nur angreifen, wenn der Spieler im Bereich
**„eigene Punktzahl ± 20 %"** liegt (S. 6, wörtlich belegt — bei 100 Punkten also 80 bis 120).
Über die Grenze von 299 Punkten hinweg ist kein Angriff möglich, in keine Richtung (S. 6).

**VORSCHLAG (Entscheidung nötig):**
- Handel: Bot vergleicht den Kaufpreis mit seinem Referenzpreis (Beschaffungskosten × 1,2) —
  darunter lehnt er ab. Je Siedlung ein „Händler-Temperament", das die Schwelle um ±10 % verschiebt.
- Angriffstakt: Prüfung alle 6 bis 24 Stunden. Angriff nur, wenn die Schlagkraft den Wall
  übersteigt **und** die erwartete Beute mindestens das Doppelte der Portalkosten beträgt.
- Beutemenge: 50 % der lagernden Rohstoffe, gedeckelt durch die Ladekapazität der Karren.
  *Das Handbuch beziffert die Beutemenge nicht.*

## Beute und Verluste (nach Handbuch)

- Geflohene Einheiten zählen **nicht** als Verlust und stehen danach wieder zur Verfügung (S. 23).
- Fluchtchance 40 %, steigt um 5 % je Kampfsequenz (S. 23, wörtlich belegt).
- Bei unentschieden bleiben alle Karren und Belagerungswaffen erhalten, der Angreifer bekommt
  nichts (S. 23).

## Die drei Fälle, in denen ein Auftrag scheitert

1. **Wall nicht überwunden** → Truppen ziehen unverrichteter Dinge zurück, Kampf gilt als
   unentschieden (S. 21). Der Spieler sieht eine Meldung, keine Beute, Karren erhalten.
2. **Nach zehn Sequenzen unentschieden** → Rückzug ohne Beute (S. 22/23).
3. **Handel abgelehnt** → Karawane kehrt mit den Waren zurück, Gold nie übertragen (S. 20).

---

## Meine Nachprüfung — Seite für Seite

| Behauptung des Entwurfs | Nachgeschlagen | Befund |
|---|---|---|
| Stationieren in fremden Siedlungen verboten, S. 19 | Z. 1152 | **stimmt** |
| Dauer gilt für eine Strecke, S. 19 | Z. 1139 | **stimmt** |
| Drosselung in 10-%-Schritten, S. 20 | Z. 1191 | **stimmt** |
| Mana nur bei fremden Zielen, abhängig von Entfernung, S. 20 | Z. 1188/1189 | **stimmt** |
| Beute nur mit Transportkarren, S. 23 | Z. 1332 | **stimmt** |
| Flucht 40 % + 5 % je Sequenz, S. 23 | Z. 1336 | **stimmt** |
| SI und HE ohne Einfluss aufs Spiel, S. 18 | Z. 1095/1098 | **stimmt** |
| Götterschutz: eigene Punktzahl ± 20 %, Grenze 299, S. 6 | Z. 222–226 | **stimmt** (wörtlich) |
| Ladung 40 / 100 / 250 | Einheitentabellen | **stimmt** — aber Achtung: auf S. 17 nennen die Karren-Zeilen *Kriegspunkte* (1/2/3); die Ladung steht in den Einheitentabellen. Die Seitenangabe des Entwurfs ist dort ungenau, die **Zahlen sind richtig**. |
| „unentschieden → Karren bleiben erhalten", S. 23 | Z. 1277 | **stimmt** |

**Fazit:** Der Entwurf hält, was er verspricht — diesmal war nichts erfunden, nur eine
Seitenangabe leicht daneben.

## Was Daniel entscheiden muss

1. Handelsregel der Bots (Referenzpreis 1,2 · Beschaffungskosten, Temperament ±10 %)?
2. Angriffstakt der Bots (alle 6–24 Stunden, Beute ≥ doppelte Portalkosten)?
3. Beutemenge (50 % der Lager, gedeckelt durch Karrenladung)?
