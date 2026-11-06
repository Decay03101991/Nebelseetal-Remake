# Einordnung: Gemini-Vorschlaege vom 06.11.2026, 05:43

**Quelle:** `GEMINI_WEITERE_VORSCHLAEGE_20261106.txt` (17.570 Byte, 60 Zeilen), von Daniel am
06.11.2026 um 05:43 auf den Desktop gelegt mit dem Auftrag: aufnehmen, auswerten, vom Desktop nehmen.
**Diese Datei ist die Auswertung. Gebaut ist daraus NICHTS.**

## Was brauchbar ist

| Teil | Urteil | Wofuer |
|---|---|---|
| Balancing-Leitfaden (Zwei-Saeulen-Prinzip, Nahrung als Taktgeber, ortsgebundene Logistik, Wachstum 1 Siedler/Stunde) | **BRAUCHBAR als Rahmen** | Bestaetigt unsere eigenen Messungen (Nahrung 8 je Einheit und Spieltag, Siedlerdeckel, Karren als Engpass). Keine neuen Zahlen. |
| Einheiten nach fuenf Rollen (Nahkampf, Fernkampf, Kundschafter, Karren, Belagerung) mit Ressourcenprofil | **BRAUCHBAR** | Gute Gliederung fuer die Balancing-Tabelle; die Rollen stehen so schon in `data/units.json` (`kategorie`, `rolle`). |
| Vier Chokepoint-Testbereiche (Nahrung/Siedler, Wegzeiten und Karren, Reparatur/Heilung, Wirtschaft) | **BRAUCHBAR als Testfokus** | Deckt sich mit A2 (Messpflicht) und dem Balancing-Werkzeug. Kein Test gebaut. |
| Hinweis: Rechenwege und Testwerte nur aus `data/`, `.get()`-Fallback, int()-Deckel gegen negative Werte | **SCHON REGEL** | Steht so in unseren Pruefstand-Konventionen und in Querschnittsregel 3/4 des Plans. |

## Was FALSCH ist (nicht uebernehmen)

1. **Die Reparaturformel ist um Faktor 10 falsch.** Der Text nennt `16 * Stufe / 10` je Prozentpunkt.
   Belegt und in S2 gebaut ist `16 * Stufe / 100` (V-1: eine Reparatur von 0 auf 100 kostet genau den
   Wallpreis mal Stufe, Stufe 1 = 16/16). Mit `/10` kostete Stufe 5 fuer 10 Prozent 80 Holz statt 8.
2. **Der Codeblock hat einen Syntaxfehler:** `assert gesamt_holz_stein == 80, fErwartet 80, ...` -
   das oeffnende Anfuehrungszeichen fehlt, so laeuft keine Zeile davon.
3. **Ein zweiter Sammellauf ist unnoetig.** `tools/sammellauf.py` existiert und faehrt 182 Pruefdateien
   (7448 Pruefungen). Ein `tools/test_sammellauf.py` daneben waere ein zweites Messgeraet mit eigenen
   Wahrheiten - genau das Muster, das wir am 31.10. bei `ware_voraussetzung` aufgeloest haben.
4. **„Der Agent aktualisiert seine Skills selbst"** ist bei uns nicht automatisch: jede Skill- oder
   Regeländerung braucht eine Zeile im `SKILL_UND_REGEL_PROTOKOLL.md` und Daniels Freigabe, wo sie
   eine bestehende Regel ersetzt.

## Was daraus folgt

Nichts wird gebaut. Fuer die naechste Sitzung ist die Datei Material fuer **A2 (Messpflicht-Tabelle)**
und fuer das Balancing nach S4 - dort mit eigenen Messungen, nicht mit diesen Zahlen.
