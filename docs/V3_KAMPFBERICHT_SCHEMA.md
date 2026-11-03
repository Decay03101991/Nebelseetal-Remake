# V-3 Vollstaendiger Kampfbericht - Datenschema (Entwurf des starken Modells, 03.11.2026)

**Herkunft:** erstellt von einem starken Modell auf Auftrag `AUFTRAG_V3_KAMPFBERICHT.md`
(16.483 Token, 121 s, 8.794 Zeichen). **Bearbeitet fuer das Projekt:** die Feldnamen standen englisch
(`report_id`, `attacker_troops`, `outcome`) - das Projekt fuehrt deutsche Bezeichner
(`verluste_angreifer`, `mauer_zustand`, `ausgang`). Sie sind deshalb eingedeutscht; wo der Bestand
schon ein Feld kennt (`verluste_angreifer`, `verluste_verteidiger`, `ausgang`, `wall_stufe`), bleibt
genau dieser Name, damit nichts bricht.

**Rang:** VORSCHLAG, nicht Vorgabe. Umsetzung erst nach Daniels Wort zu den drei offenen Fragen, die
das Verhalten aendern (Beute-Verteilung, Fluchtformel, Mauerschaden der Tuerme).

## Kurzfassung

Das Schema ist ein zentraler, strukturierter Kampfdatensatz, der alle Informationen zum Zeitpunkt des Angriffs enthält. Jede Seite (Angreifer und Verteidiger) erhält eine eigene Sicht aus demselben Datensatz, ohne dass Felder ausgeblendet werden. Die Garnison des Verteidigers und seine Ausbildungswarteschlange werden strikt getrennt erfasst; die Warteschlange kämpft nicht mit. Offene Kampfregeln werden als `unsicher: true` markiert und nicht stillschweigend gefüllt. Der Bot kann aus Beute, Restverteidigung, Mauerzustand und Warteschlange ableiten, ob ein weiterer Angriff lohnt – der Bericht selbst spricht keine Empfehlung aus.

## Das Schema

| Feld | Typ | Bedeutung | Herkunft (Funktion/Datendatei) | Seite | unsicher? |
|---|---|---|---|---|---|
| bericht_id | string (UUID) | Eindeutige Kennung des Berichts | neu generiert | beide | nein |
| angriffsmoment | object | Zeitpunkt, Welt und Spielzustandskennung zum Angriffsmoment | Spieldaten / `spieldaten_anwenden()` | beide | nein |
| dorf_angreifer | string | Dorfname des Angreifers | Spieldaten | beide | nein |
| dorf_verteidiger | string | Dorfname des Verteidigers | Spieldaten | beide | nein |
| kennung_angreifer | string | ID des Angreifers | Spieldaten | beide | nein |
| kennung_verteidiger | string | ID des Verteidigers | Spieldaten | beide | nein |
| truppen_angreifer | object | Angreifertruppen zum Angriffsmoment | Kampfaufstellung / `spieldaten_anwenden()` | beide | ja (fussstruppen_begriff offen) |
| garnison_verteidiger | object | Garnison des Verteidigers zum Angriffsmoment (kämpft) | Spieldaten | beide | ja (fussstruppen_begriff offen) |
| warteschlange_verteidiger | array/object | Warteschlange in Ausbildung zum Angriffsmoment (kämpft nicht, läuft weiter) | Spieldaten | beide | nein |
| wall_stufe | int | Stufe der Mauer | Spieldaten | beide | nein |
| wall_name | string | Name der Mauer | Spieldaten | beide | nein |
| mauer_vorher | object | Mauerzustand vor dem Angriff | Spieldaten | beide | nein |
| mauer_nachher | object | Mauerzustand nach dem Angriff (entspricht `mauer_zustand`) | `mauer_schaden()`, `spieldaten_anwenden()` | beide | ja (belagerungsturm_mauerschaden, mauer_reparatur offen) |
| vorrunde | object | Ergebnis der Wallpruefung (Schwelle, Grund) | `vorrunde()` | beide | ja (vorrunde_wiederholung offen) |
| taktik_verteidiger | string/enum | Taktik des Verteidigers | Spieldaten | beide | nein |
| volk_verteidiger | string/enum | Volk des Verteidigers | Spieldaten | beide | nein |
| vorraete_verteidiger | object | Vorräte des Verteidigers vor dem Angriff (Beutegrundlage) | Spieldaten | beide | nein |
| beute_mitgenommen | object | tatsächlich mitgenommene Beute | `beute()`, `beute_staffel()`, `beute_am_ziel()`, `beute_lage()` | beide | ja (beute_verteilung, beute_reihenfolge, geraetebeute offen) |
| beute_liegengeblieben | object | liegen gebliebene Beute | `beute()`, `beute_lage()` | beide | ja (beute_verteilung, beute_reihenfolge, geraetebeute offen) |
| verluste_angreifer | object | Verluste des Angreifers (entspricht `verluste_angreifer`) | Kampfberechnung | beide | ja (fussstruppen_begriff, flucht_formel offen) |
| verluste_verteidiger | object | Verluste des Verteidigers (entspricht `verluste_verteidiger`) | Kampfberechnung | beide | ja (fussstruppen_begriff, flucht_formel offen) |
| device_verluste_angreifer | object/array | Geräteverluste des Angreifers (entspricht `geraete_verloren`) | Kampfberechnung | beide | ja (geraetebeute offen) |
| device_verluste_verteidiger | object/array | Geräteverluste des Verteidigers (entspricht `geraete_verloren_verteidiger`) | Kampfberechnung | beide | ja (geraetebeute offen) |
| ausgang | enum (sieg, niederlage, unentschieden, flucht) | Ausgang des Kampfes (entspricht `ausgang`, `unentschieden`, `geflohen`) | Kampfberechnung | beide | ja (flucht_formel offen; nur Wert `flucht` betroffen) |
| kampf | object | Interner Kampfverlauf (Runden, Vorrunde, Details) | `kampfbericht.py` | beide | ja (vorrunde_wiederholung offen) |
| unsicher | bool | Metafeld: true, wenn der Bericht unsichere Teile enthält | `offene_luecken()` | beide | nein |
| titel | string | Anzeigetitel für die jeweilige Sicht | `kampfbericht.py` | beide | nein |
| zeilen | array of string | Anzeigezeilen für die jeweilige Sicht | `kampfbericht.py` | beide | nein |

## Zwei Sichten

Beide Sichten werden aus demselben Datensatz erzeugt. Der Unterschied liegt in der Perspektive und der Beschriftung, nicht in der Feldverfügbarkeit:

- **Angreifersicht** zeigt `truppen_angreifer` als „Deine Truppen", `garnison_verteidiger` als „Verteidigergarnison", `vorraete_verteidiger` als „vorgefundene Vorräte" und `beute_mitgenommen` als „deine Beute".
- **Verteidigersicht** zeigt `garnison_verteidiger` als „Deine Verteidiger", `truppen_angreifer` als „Angreifertruppen", `vorraete_verteidiger` als „deine Vorräte vor dem Angriff" und `beute_mitgenommen` als „vom Angreifer erbeutet".

Bewusst nicht in den Sichttext aufgenommen werden:

- Keine fertige Empfehlung („Greif noch einmal an" oder „Verstärke dich").
- Keine Interpretation der offenen Punkte – unsichere Felder werden als „unsicher" markiert, aber nicht mit erfundenen Regeln gefüllt.
- Interne IDs (`bericht_id`, `kennung_angreifer`, `kennung_verteidiger`) sind im Datensatz enthalten, erscheinen aber nicht zwingend im Spielertext.

## Warteschlange und Angriffsmoment

**Empfehlung: ein Unterobjekt `angriffsmoment` mit drei Feldern.**

| Unterfeld | Typ | Bedeutung |
|---|---|---|
| spielsekunden | int | Spielsekunden zum Angriffsmoment |
| world | string | Welt/Dimension, in der der Angriff stattfand |
| stand_kennung | string | optionale Kennung des Spielzustands (zur Reproduzierbarkeit) |

**Begründung:** Der Angriffsmoment ist der gemeinsame Bezugspunkt für sämtliche im Bericht enthaltenen Daten. Ein Unterobjekt stellt sicher, dass keine Vermischung von Zeitstempeln entsteht, wenn mehrere Berichte im Postfach verglichen werden (V-5). Drei flache Felder wären möglich, aber das Unterobjekt kapselt die Zeitbasis und erleichtert spätere Erweiterungen um z. B. Rundenzeitpunkte. Die Ausbildungswarteschlange wird als eigenes Feld `warteschlange_verteidiger` geführt und nie in die Kampftruppen einbezogen. Sie enthält Einheiten samt geplantem Fertigstellungszeitpunkt, damit der Bot erkennen kann, wann der Verteidiger wieder stärker wird.

## Was der Bot daraus schliessen kann (V-5)

Der Bot wertet folgende Felder aus, ohne dass der Bericht eine Empfehlung ausspricht:

| Feld | Nutzen für die Bot-Auswertung |
|---|---|
| ausgang | War der Angriff erfolgreich? |
| verluste_angreifer | Wie viel hat der Angriff gekostet? |
| verluste_verteidiger | Wie stark wurde der Verteidiger geschwächt? |
| garnison_verteidiger | Restgarnison des Verteidigers |
| warteschlange_verteidiger | Bald verfügbare Verstärkung des Verteidigers |
| mauer_nachher | Ist die Mauer zerstört oder intakt? |
| beute_mitgenommen | Welche Ressourcen wurden mitgenommen? |
| vorraete_verteidiger | Wie viel ist beim Verteidiger noch zu holen? |
| device_verluste_verteidiger | Sind Geräte des Verteidigers zerstört? |

Diese Felder liefern die Fakten. Die Entscheidung, ob ein weiterer Angriff lohnt, trifft die Bot-Logik in V-5 auf Basis dieser Werte – der Bericht selbst bleibt neutral.

## Offene Punkte

Alle offenen Punkte werden im Schema als `unsicher: true` markiert, bis der Auftraggeber die Regel festlegt. Pro Punkt die Empfehlung zuerst:

1. **fussstruppen_begriff**  
   *Empfehlung:* Definiere exakt, welche Einheiten als Fussstruppen gelten. Bis dahin sind `truppen_angreifer`, `garnison_verteidiger`, `verluste_angreifer` und `verluste_verteidiger` als unsicher zu markieren.

2. **flucht_formel**  
   *Empfehlung:* Lege fest, unter welchen Bedingungen eine Flucht ausgelöst wird. Bis dahin ist der Ausgangswert `flucht` unsicher; betroffen sind `ausgang`, `verluste_angreifer` und `verluste_verteidiger`.

3. **beute_verteilung**  
   *Empfehlung:* Entscheide, wie Beute auf Angreifer und Verteidiger verteilt wird. Bis dahin sind `beute_mitgenommen` und `beute_liegengeblieben` unsicher.

4. **beute_reihenfolge**  
   *Empfehlung:* Definiere die Reihenfolge, in der Ressourcen als Beute genommen werden. Bis dahin sind `beute_mitgenommen` und `beute_liegengeblieben` unsicher.

5. **belagerungsturm_mauerschaden**  
   *Empfehlung:* Bestimme, wie viel Schaden Belagerungstürme an der Mauer verursachen. Bis dahin ist `mauer_nachher` unsicher.

6. **mauer_reparatur**  
   *Empfehlung:* Kläre, ob und wann die Mauer nach dem Angriff repariert wird. Bis dahin ist `mauer_nachher` unsicher.

7. **vorrunde_wiederholung**  
   *Empfehlung:* Lege fest, ob die Wallpruefung wiederholt wird. Bis dahin sind `vorrunde` und `kampf` unsicher.

8. **geraetebeute**  
   *Empfehlung:* Entscheide, ob und wie Geräte erbeutet werden können. Bis dahin sind `beute_mitgenommen`, `beute_liegengeblieben`, `device_verluste_angreifer` und `device_verluste_verteidiger` unsicher.