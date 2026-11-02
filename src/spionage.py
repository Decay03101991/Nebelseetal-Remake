"""Spionage: Schalter, Aufklaerungswert, Bericht und Nachricht (Stufe B-5, 02.11.2026).

VORGABE Daniel 02.11.2026 (Vorbild Lords Mobile): ein fremdes Dorf zeigt offen nur Position,
Fraktion, Namen, Hauptdorf und die bekannten Volkswerte. Wallstufe, Wallzustand, aktive Taktik,
stationierte Truppen, Vorraete, Karte und Ertrag stehen NUR in einem Spionagebericht. Die Grenze
selbst steht im Spielstand (`main.GameState.bot_doerfer_uebersicht` offen,
`main.GameState.bot_doerfer_spionagebericht` verdeckt); dieses Modul macht daraus die Nachricht.

VORGABE Daniel 02.11.2026 (Ergaenzung im laufenden Schritt): "spionage muss mit den werten der
einheiten gekoppelt werden. Gauner Diebe usw sind sozusagen Spionageeinheiten". Also:
- Es reisen SPIONAGEEINHEITEN - die sechs Kundschafter der Diebesgilde (Streuner, Gauner, Dieb,
  Meisterdieb, Kundschafter, Waldlaeufer; `einheiten.ist_kundschafter`).
- WIE VIEL der Bericht aufdeckt, rechnet `aufklaerungswert` aus den BELEGTEN Werten dieser
  Einheiten (SI Sinnesschaerfe + HE Heimlichkeit, `data/units.json`), und `aufgedeckt` vergleicht
  ihn mit den Schwellen je Berichtsteil aus `data/spionage.json`.
- Wie schnell sie reisen, entscheidet ihr GS-Wert - das rechnet schon `auftraege.reisezeit_sekunden`
  (Fanpage 2007: "Pferde machen Spione schneller").

Vier Zusagen, die dieses Modul traegt
-------------------------------------
1. **Kein Bericht ohne Auftrag.** Nachrichten dieses Typs entstehen ausschliesslich bei der ANKUNFT
   eines Auftrags der Art `spionieren` (`main.GameState.auftraege_fortschreiben`). Es gibt keine
   Funktion, die einen Bericht aus dem Nichts baut: `bericht_nachricht` braucht einen Bericht.
2. **Kein Bericht ueber das eigene Dorf.** Das prueft der Auftragskern (`auftraege.starten`), weil
   dort das Ziel als fremd oder eigen bekannt ist - nicht die Anzeige.
3. **Ein Bericht verraet nie mehr, als die Aufklaerung deckt.** `bericht_zeilen` schreibt fuer jeden
   nicht gedeckten Teil "nicht aufgeklaert" samt Schwelle - der Text ist die Anzeige, und er haelt
   sich an dieselbe Rechnung wie der Kern.
4. **Ein Bericht wird nicht alt** (Vorgabe Daniel 02.11.2026: "ein Spionagebericht ist immer aktuell
   ausser man hat einen neuen ueber das gleiche dorf"). Er traegt den Spielzeitpunkt seiner Ankunft
   und sagt selbst, dass Truppen, die DANACH im Dorf eintreffen, nicht enthalten sind. `veraltet`
   bleibt als Mechanik vorhanden (Frist 0 = nie veraltet), damit eine freiwillige Frist in
   `data/spionage.json` ohne Codeaenderung moeglich ist.

Alle Zahlen (Frist, Formel, Schwellen) stehen in `data/spionage.json`; fehlt die Datei, gilt
`VORGABE`. Die Quellen beziffern den Einfluss von SI und HE nicht ("hat im Moment noch keinen
Einfluss", Handbuch) - deshalb ist die Rechnung ausdruecklich VORSCHLAG (siehe `offene_luecken`).

Aufruf:  python -X utf8 -c "import sys;sys.path.insert(0,'src');import spionage"
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import einheiten   # die sechs Kundschafter und ihre belegten Werte (SI, HE, GS)
import hilfen      # aufzaehlung: die eine Schreibweise fuer Mengen
import spieldaten  # projektwurzel: Wo liegen die Datendateien (Quelltext und EXE)?

# Die Berichtsteile in der Reihenfolge, in der sie aufgedeckt werden (leicht zu schwer).
TEILE = ("truppen", "vorraete", "wall", "karte", "taktik")

# Rueckfall, wenn `data/spionage.json` fehlt oder kaputt ist (Spiel laeuft weiter).
VORGABE: Dict[str, Any] = {
    "aktiv": True,                                  # Spionage eingeschaltet
    # Keine Frist (Vorgabe Daniel 02.11.2026): ein Bericht wird NICHT alt. Er gilt, bis ein NEUER
    # Bericht ueber dasselbe Dorf kommt - 0 heisst genau das (veraltet() liefert dann immer False).
    "bericht_gueltig_stunden": 0.0,
    "kundschafter_pflicht": True,                   # ohne Spionageeinheit kein Auftrag
    "kundschafter_anzahl": 1,                       # VORSCHLAG: so viele schickt die Anzeige mit
    "aufklaerung_formel": "SI+HE",                  # VORSCHLAG: diese Werte je Einheit zusammen zaehlen
    "schwellen": {                                  # VORSCHLAG: Aufklaerungswert je Berichtsteil
        "truppen": 25,                              # Streuner (60) deckt das schon auf
        "vorraete": 50,                             # Streuner (60) auch
        "wall": 75,                                 # ab Gauner (95)
        "karte": 100,                               # ab Dieb (135)
        "taktik": 150,                              # ab Meisterdieb (150)
    },
    "abwehr_je_wallstufe": 20.0,                    # VORSCHLAG: Wall stufe x 20 muss die Truppe schlagen
    "verlust_prozent_bei_abwehr": 50.0,             # VORSCHLAG: so viel geht beim Abprallen verloren
}


def einstellungen() -> Dict[str, Any]:
    """Liest `data/spionage.json` - die EINE Stelle fuer Schalter, Frist, Formel und Schwellen.

    Fehlt die Datei oder ist sie kaputt, gilt `VORGABE`; das Spiel laeuft weiter. Die Datei hat
    Vorrang, unbekannte Schluessel bleiben erhalten (Daniel kann Zahlen ohne Codeaenderung stellen).
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "spionage.json")   # Datendatei
    try:                                                                        # Datei lesen
        with open(pfad, encoding="utf-8") as f:                                 # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                                # Inhalt als dict
    except (OSError, ValueError):                                               # fehlt oder ist kaputt
        return dict(VORGABE)                                                    # dann die Vorgabe
    if not isinstance(daten, dict):                                             # unerwarteter Inhalt
        return dict(VORGABE)                                                    # dann die Vorgabe
    werte = dict(VORGABE)                                                       # Vorgabe als Grundlage
    werte.update(daten)                                                         # Datei hat Vorrang
    if not isinstance(werte.get("schwellen"), dict) or not werte.get("schwellen"):   # kaputte Schwellen
        werte["schwellen"] = dict(VORGABE["schwellen"])                         # dann die Vorgabe
    return werte                                                                # fertige Einstellungen


def _als_int(wert: Any) -> int:
    """Eine Zahl roh und sicher - alles Unbrauchbare zaehlt 0, nie ein Absturz."""
    try:                                                                        # Umwandlung versuchen
        return int(float(wert))                                                 # Zahl (auch "12.0")
    except (TypeError, ValueError):                                             # Text oder None
        return 0                                                                # dann 0


def _als_zahl(wert: Any, vorgabe: float = 0.0) -> float:
    """Eine Kommazahl roh und sicher - alles Unbrauchbare zaehlt die Vorgabe, nie ein Absturz."""
    try:                                                                        # Umwandlung versuchen
        return float(wert)                                                      # Zahl als float
    except (TypeError, ValueError):                                             # Text oder None
        return float(vorgabe)                                                   # dann die Vorgabe


def frist_stunden(einstellungen_werte: Optional[dict] = None) -> float:
    """Die Gueltigkeitsfrist eines Berichts in Spielstunden (nie negativ, 0 = keine Frist)."""
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    try:                                                                        # Zahl aus der Datei
        wert = float(e.get("bericht_gueltig_stunden") or 0.0)                   # Stunden als Zahl
    except (TypeError, ValueError):                                             # kaputter Wert
        wert = float(VORGABE["bericht_gueltig_stunden"])                        # dann der Vorschlag
    return max(0.0, wert)                                                       # nie negativ


def formel_felder(formel: Any = None) -> List[str]:
    """Die Wertnamen der Formel ('SI+HE' -> ['SI', 'HE']); leer heisst: keine Aufklaerung."""
    text = str(formel or VORGABE["aufklaerung_formel"])                         # Formel als Text
    return [teil.strip().upper() for teil in text.split("+") if teil.strip()]   # Felder einzeln


def aufklaerungswert(einheiten_werte: Any, formel: Any = None) -> int:
    """Der Aufklaerungswert einer Truppe - EINE Rechenstelle fuer Kern und Anzeige (F-04).

    Gezaehlt wird JE EINHEIT der Wert der Formel (Vorgabe: SI + HE aus `data/units.json`) mal
    Anzahl, und zwar NUR fuer Spionageeinheiten (`einheiten.ist_kundschafter`). Kaempfer, Karren
    und Belagerungswaffen reisen zwar mit, klaeren aber nichts auf - Gauner und Diebe sind die
    Spionageeinheiten (Vorgabe Daniel 02.11.2026). Unbekannte Namen zaehlen 0.
    """
    alle = einheiten.alle()                                                     # alle Einheiten mit Werten
    felder = formel_felder(formel)                                              # welche Werte zaehlen
    summe = 0                                                                   # Ergebnis
    if not isinstance(einheiten_werte, dict):                                   # keine Truppe uebergeben
        return 0                                                                # dann 0 Aufklaerung
    for name, anzahl in einheiten_werte.items():                                # je mitgeschickter Einheit
        if not einheiten.ist_kundschafter(str(name)):                           # keine Spionageeinheit
            continue                                                            # zaehlt nicht mit
        werte = (alle.get(str(name)) or {}).get("werte") or {}                  # ihre belegten Werte
        je = sum(max(0, _als_int(werte.get(feld))) for feld in felder)          # Formel je Einheit
        summe += max(0, _als_int(anzahl)) * je                                  # mal Anzahl
    return summe                                                                # fertiger Wert


def spionageeinheiten(einheiten_werte: Any) -> Dict[str, int]:
    """Nur die Spionageeinheiten aus einer Truppe - was der Auftrag wirklich aufklaert."""
    if not isinstance(einheiten_werte, dict):                                   # keine Truppe
        return {}                                                               # dann nichts
    return {str(n): max(0, _als_int(a)) for n, a in einheiten_werte.items()      # Name und Anzahl
            if einheiten.ist_kundschafter(str(n)) and _als_int(a) > 0}          # nur Kundschafter > 0


def schwellen(einstellungen_werte: Optional[dict] = None) -> Dict[str, int]:
    """Die Schwelle je Berichtsteil (fehlende Teile bekommen 0 = immer aufgedeckt)."""
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    roh = e.get("schwellen") if isinstance(e.get("schwellen"), dict) else {}
    return {teil: max(0, _als_int(roh.get(teil, 0))) for teil in TEILE}          # je Teil eine Zahl


def aufgedeckt(aufklaerung: Any, einstellungen_werte: Optional[dict] = None) -> Dict[str, bool]:
    """Welche Berichtsteile diese Aufklaerung deckt - je Teil ein Wahrheitswert."""
    wert = max(0, _als_int(aufklaerung))                                        # Aufklaerung als Zahl
    grenzen = schwellen(einstellungen_werte)                                    # Schwelle je Teil
    return {teil: wert >= grenzen[teil] for teil in TEILE}                       # erreicht oder nicht


def abwehr_eines_dorfes(wall_stufe: Any, wall_zustand_prozent: Any = 100.0,
                        einstellungen_werte: Optional[dict] = None) -> float:
    """Die Abwehr eines Dorfes gegen Spione - die Schlagkraft, die eine Truppe ueberwinden muss.

    VORGABE Daniel 02.11.2026: "dann benoetigt es eine gewisse schlagkraft von spionageinheiten um
    einen wall zu ueberwinden und auszuspionieren." Deshalb dieselbe Mechanik wie die Wall-Vorrunde
    im Kampf (`kampfbericht.vorrunde`): je Wallstufe eine Schwelle, und eine beschaedigte Mauer
    verlangt - woertlich Handbuch - "prozentual weniger", also Faktor Zustand/100. Ohne Wall
    (Stufe 0) gibt es nichts zu ueberwinden: Abwehr 0.
    """
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    stufe = max(0, _als_int(wall_stufe))                                        # Wallstufe, nie negativ
    if stufe <= 0:                                                              # kein Wall
        return 0.0                                                              # also keine Abwehr
    je_stufe = max(0.0, _als_zahl(e.get("abwehr_je_wallstufe"), 0.0))            # Schwelle je Stufe
    zustand = max(0.0, min(100.0, _als_zahl(wall_zustand_prozent, 100.0)))       # Zustand 0..100
    return round(je_stufe * stufe * (zustand / 100.0), 2)                        # Stufe x Faktor


def abwehr_pruefung(aufklaerung: Any, wall_stufe: Any, wall_zustand_prozent: Any = 100.0,
                    einstellungen_werte: Optional[dict] = None) -> Dict[str, Any]:
    """Ueberwindet diese Spionagetruppe den Wall? (Analogie zu `kampfbericht.vorrunde`)

    Rueckgabe wie die Wall-Vorrunde: {'bestanden', 'vorhanden', 'erforderlich', 'wall_stufe',
    'grund'}. `bestanden` False heisst: der Auftrag prallt ab - Verluste statt Bericht
    (`verlust_der_truppe`). Ein Dorf ohne Wall kann immer ausspioniert werden.
    """
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    vorhanden = max(0, _als_int(aufklaerung))                                   # Aufklaerung der Truppe
    stufe = max(0, _als_int(wall_stufe))                                        # Wallstufe des Dorfes
    erforderlich = abwehr_eines_dorfes(stufe, wall_zustand_prozent, e)           # seine Abwehr
    bestanden = vorhanden >= erforderlich                                       # ueberwunden?
    if stufe <= 0:                                                              # kein Wall
        grund = "Kein Wall vorhanden - es gibt keine Abwehr zu ueberwinden."
    elif bestanden:                                                             # Wall geschlagen
        grund = ("Die Spionageeinheiten ueberwinden den Wall %d (Aufklaerung %d gegen Abwehr %d)."
                 % (stufe, vorhanden, int(round(erforderlich))))
    else:                                                                       # abgeprallt
        grund = ("Die Spionageeinheiten prallen am Wall %d ab (Aufklaerung %d gegen Abwehr %d)."
                 % (stufe, vorhanden, int(round(erforderlich))))
    return {"bestanden": bool(bestanden), "vorhanden": int(vorhanden),
            "erforderlich": float(erforderlich), "wall_stufe": int(stufe), "grund": grund}


def verlust_der_truppe(einheiten_werte: Any,
                       einstellungen_werte: Optional[dict] = None) -> Dict[str, int]:
    """Was von einer abgeprallten Spionagetruppe uebrig bleibt (Anteil aus der Datendatei).

    Es wird ABGERUNDET, damit nie mehr Einheiten zurueckkommen als entsandt wurden; eine Einheit,
    die auf 0 faellt, faellt aus dem dict. Negative oder unsinnige Werte zaehlen nie mit.
    """
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    anteil = max(0.0, min(100.0, _als_zahl(e.get("verlust_prozent_bei_abwehr"), 0.0)))   # Prozent
    rest: Dict[str, int] = {}                                                   # Ergebnis
    if not isinstance(einheiten_werte, dict):                                   # keine Truppe
        return rest                                                             # dann nichts
    for name, anzahl in einheiten_werte.items():                                # je entsandte Einheit
        a = max(0, _als_int(anzahl))                                            # Anzahl als Zahl
        uebrig = int(a * (100.0 - anteil) / 100.0)                              # Anteil bleibt
        if uebrig > 0:                                                          # nur was uebrig ist
            rest[str(name)] = uebrig                                            # in das Ergebnis
    return rest                                                                 # fertige Resttruppe


def bericht_titel(bericht: Any) -> str:
    """Die Ueberschrift eines Berichts - Bot und Dorf, sonst 'unbekannt'."""
    b = bericht if isinstance(bericht, dict) else {}                            # Bericht als dict
    dorf = _dorf(b)                                                             # Dorfteil
    return "Spionagebericht: %s, %s" % (str(dorf.get("name") or "unbekannt"),
                                        str(b.get("bot") or "unbekannt"))


def _dorf(bericht: Any) -> Dict[str, Any]:
    """Der Dorfteil eines Berichts - fehlt er, ein leeres dict (Anzeige stuerzt nie ab)."""
    b = bericht if isinstance(bericht, dict) else {}                            # Bericht als dict
    dorf = b.get("dorf")                                                       # der Dorfteil
    return dorf if isinstance(dorf, dict) else {}                               # nie None


def _verdeckt(teil: str, aufklaerung: int, grenzen: Dict[str, int]) -> str:
    """Der Text eines NICHT aufgedeckten Teils - samt dem, was fehlt (nie eine leere Zeile)."""
    return "nicht aufgeklaert (Aufklaerung %d von %d noetig)" % (aufklaerung, grenzen.get(teil, 0))


def bericht_zeilen(bericht: Any, aufklaerung: Any = None,
                   einstellungen_werte: Optional[dict] = None) -> List[str]:
    """Die Zeilen eines Spionageberichts - EINE Stelle fuer Kern, Postfach und Pruefung.

    Eingabe ist der Bericht aus `main.GameState.bot_dorf_spionagebericht` (ein Dorf) und der
    Aufklaerungswert der entsandten Spionageeinheiten. Position, Fraktion, Name und Hauptdorf sind
    offen sichtbar und stehen immer da; die fuenf verdeckten Teile erscheinen nur, wenn die
    Aufklaerung ihre Schwelle erreicht. Fehlt ein Wert, steht dort "unbekannt" - nie eine erfundene
    Zahl. Ohne Aufklaerung (0) bleibt jeder verdeckte Teil verdeckt.
    """
    b = bericht if isinstance(bericht, dict) else {}                            # Bericht als dict
    dorf = _dorf(b)                                                             # Dorfteil
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    wert = max(0, _als_int(aufklaerung))                                        # Aufklaerung als Zahl
    grenzen = schwellen(e)                                                      # Schwelle je Teil
    zeilen: List[str] = []                                                      # Ergebniszeilen
    try:                                                                        # Position als Zahlen
        x = int(dorf.get("x") or 0)                                             # Spalte im Raster
        y = int(dorf.get("y") or 0)                                             # Zeile im Raster
    except (TypeError, ValueError):                                             # kaputte Werte
        x, y = 0, 0                                                             # dann 0/0
    zeilen.append("Dorf %s von %s auf Position %d/%d, Fraktion %s."
                  % (str(dorf.get("name") or "unbekannt"), str(b.get("bot") or "unbekannt"),
                     x, y, str(b.get("fraktion") or "unbekannt")))
    zeilen.append("Aufklaerung: %d (aus den Werten der Spionageeinheiten, VORSCHLAG-Formel)." % wert)
    # --- Truppen ---------------------------------------------------------------
    if wert >= grenzen["truppen"]:                                              # Schwelle erreicht
        zeilen.append("Stationierte Truppen: %s." % hilfen.aufzaehlung(dorf.get("truppen")))
    else:                                                                       # zu wenig Aufklaerung
        zeilen.append("Stationierte Truppen: " + _verdeckt("truppen", wert, grenzen) + ".")
    # --- Vorraete --------------------------------------------------------------
    if wert >= grenzen["vorraete"]:                                             # Schwelle erreicht
        zeilen.append("Vorraete im Dorflager: %s." % hilfen.aufzaehlung(dorf.get("vorraete")))
    else:                                                                       # zu wenig Aufklaerung
        zeilen.append("Vorraete im Dorflager: " + _verdeckt("vorraete", wert, grenzen) + ".")
    # --- Wall ------------------------------------------------------------------
    if wert >= grenzen["wall"]:                                                 # Schwelle erreicht
        try:                                                                    # Wallstufe als Zahl
            stufe = int(dorf.get("wall_stufe") or 0)                            # Stufe des Walls
        except (TypeError, ValueError):                                         # kaputter Wert
            stufe = 0                                                           # dann 0
        try:                                                                    # Zustand in Prozent
            zustand = float(dorf.get("wall_zustand"))                           # 0 bis 100
        except (TypeError, ValueError):                                         # kaputter Wert
            zustand = 100.0                                                     # dann heil
        zeilen.append("Wall: Stufe %d, Zustand %d %%." % (stufe, int(round(zustand))))
    else:                                                                       # zu wenig Aufklaerung
        zeilen.append("Wall: " + _verdeckt("wall", wert, grenzen) + ".")
    # --- Karte und Ertrag ------------------------------------------------------
    if wert >= grenzen["karte"]:                                                # Schwelle erreicht
        karte = str(dorf.get("karte") or "")                                    # Karte des Dorfes
        info = dorf.get("karte_info") if isinstance(dorf.get("karte_info"), dict) else {}
        staerkster = str(info.get("staerkster") or "")                           # der starke Rohstoff
        kategorie = str(info.get("kategorie") or "")                            # beste/mittlere/schlechte
        if karte:                                                               # Karte bekannt
            zeilen.append("Karte: %s%s%s." % (
                karte, " (%s)" % kategorie if kategorie else "",
                ", staerkster Rohstoff %s" % staerkster if staerkster else ""))
        else:                                                                   # alter Stand ohne Karte
            zeilen.append("Karte: unbekannt.")
        ertrag = dorf.get("ertrag_pro_stunde") if isinstance(dorf.get("ertrag_pro_stunde"), dict) else {}
        zeilen.append("Ertrag je Stunde: %s." % hilfen.aufzaehlung(ertrag))
    else:                                                                       # zu wenig Aufklaerung
        zeilen.append("Karte und Ertrag: " + _verdeckt("karte", wert, grenzen) + ".")
    # --- Taktik ----------------------------------------------------------------
    if wert >= grenzen["taktik"]:                                               # Schwelle erreicht
        zeilen.append("Aktive Taktik: %s." % (str(dorf.get("taktik") or "unbekannt")))
    else:                                                                       # zu wenig Aufklaerung
        zeilen.append("Aktive Taktik: " + _verdeckt("taktik", wert, grenzen) + ".")
    # --- Stand statt Frist (Vorgabe Daniel 02.11.2026) -------------------------
    # Ein Bericht wird nicht alt; er zeigt den Stand der ANKUNFT und wird nur durch einen neuen
    # Bericht ueber dasselbe Dorf ueberholt. Was er nicht wissen kann, steht ausdruecklich da.
    try:                                                                        # Ankunft als Spielzeit
        stand = float(b.get("zeit_spielsekunden") or 0.0) / 3600.0              # Spielstunden
    except (TypeError, ValueError):                                             # kaputter Wert
        stand = 0.0                                                             # dann ohne Zahl
    zeilen.append("Stand: Spielstunde %.1f (Ankunft der Spione)." % stand)
    zeilen.append("Der Bericht bleibt gueltig, bis ein NEUER Bericht ueber dieses Dorf kommt - "
                  "Truppen, die erst danach im Dorf eintreffen, sind hier NICHT enthalten.")
    frist = frist_stunden(e)                                                    # freiwillige Frist
    if frist > 0:                                                               # nur wenn eingestellt
        zeilen.append("Zusaetzlich eingestellte Frist: %d Spielstunden." % int(frist))
    return zeilen                                                               # fertige Zeilen


def bericht_nachricht(bericht: Any, aufklaerung: Any = None,
                      einstellungen_werte: Optional[dict] = None) -> Dict[str, Any]:
    """Die Postfach-Nachricht eines Berichts (`type` = spionage).

    Die Nachricht traegt den SPIELZEITPUNKT der Ankunft als `spielzeit_sekunden` (nicht die Uhr
    des Lesens) - daran misst `veraltet`. Den Rechner- und Ortszeitstempel setzt
    `zeitbasis.NachrichtenMitZeit` beim Anhaengen. Ohne Bericht entsteht KEINE Nachricht: die
    Funktion bricht dann mit einem klaren Fehler ab, statt einen leeren Bericht zu erfinden.
    """
    if not isinstance(bericht, dict) or not bericht.get("dorf"):
        raise ValueError("Ein Spionagebericht braucht einen Dorfteil - ohne Auftrag kein Bericht.")
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    titel = bericht_titel(bericht)                                              # Ueberschrift
    zeilen = bericht_zeilen(bericht, aufklaerung, e)                            # Inhalt nach Aufklaerung
    try:                                                                        # Ankunftszeit als Zahl
        zeit = float(bericht.get("zeit_spielsekunden") or 0.0)                   # Spielsekunden
    except (TypeError, ValueError):                                             # kaputter Wert
        zeit = 0.0                                                              # dann 0
    return {"type": "spionage",                                                 # Art der Nachricht
            "titel": titel,                                                     # Ueberschrift
            "aufklaerung": max(0, _als_int(aufklaerung)),                        # Guete des Berichts
            "text": titel + "\n" + "\n".join(zeilen),                           # der volle Bericht
            "spielzeit_sekunden": zeit}                                         # Zeitpunkt der Ankunft


def veraltet(bericht: Any, jetzt: Any, einstellungen_werte: Optional[dict] = None) -> bool:
    """Ist dieser Bericht aelter als die Frist? 0 oder fehlende Frist heisst: nie veraltet."""
    b = bericht if isinstance(bericht, dict) else {}                            # Bericht als dict
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    frist = frist_stunden(e)                                                    # Frist in Stunden
    if frist <= 0.0:                                                            # keine Frist gesetzt
        return False                                                            # also nie veraltet
    try:                                                                        # Zeitpunkte als Zahlen
        ankunft = float(b.get("zeit_spielsekunden") or 0.0)                      # Spielsekunden
        nun = float(jetzt)                                                      # aktueller Spielstand
    except (TypeError, ValueError):                                             # kaputte Werte
        return False                                                            # dann keine Aussage
    return (nun - ankunft) > frist * 3600.0                                     # aelter als die Frist


def veraltet_text(bericht: Any, jetzt: Any, einstellungen_werte: Optional[dict] = None) -> str:
    """Der Hinweis ueber der Anzeige: leer, solange der Bericht gilt."""
    if not veraltet(bericht, jetzt, einstellungen_werte):                       # noch aktuell
        return ""                                                               # kein Hinweis
    e = einstellungen_werte if isinstance(einstellungen_werte, dict) else einstellungen()
    return ("Dieser Bericht ist aelter als %d Spielstunden - die Zahlen koennen veraltet sein. "
            "Ein neuer Spionageauftrag bringt den aktuellen Stand." % int(frist_stunden(e)))


def offene_luecken() -> Dict[str, str]:
    """Jeder eigene Wert mit Grund - was die Quellen nicht hergeben, wird nicht erfunden."""
    return {
        "formel": ("'SI+HE' als Aufklaerungswert ist VORSCHLAG. Belegt sind die WERTE selbst "
                   "(SI Sinnesschaerfe, HE Heimlichkeit, data/units.json) und dass die Kundschafter "
                   "der Diebesgilde die Spionageeinheiten sind; das Handbuch sagt zu ihrem Einfluss "
                   "ausdruecklich 'hat im Moment noch keinen Einfluss'."),
        "schwellen": ("Die Schwellen je Berichtsteil (Truppen 25, Vorraete 50, Wall 75, Karte 100, "
                      "Taktik 150) sind VORSCHLAG, kalibriert an den belegten Werten der sechs "
                      "Kundschafter (30/30 bis 90/95). Die Quellen nennen keinen Felderumfang."),
        "frist": ("Es gibt KEINE Frist (Vorgabe Daniel 02.11.2026): ein Bericht bleibt aktuell, bis "
                  "ein neuer Bericht ueber dasselbe Dorf kommt. Die Mechanik einer freiwilligen Frist "
                  "steht bereit (`bericht_gueltig_stunden`, 0 = abgeschaltet)."),
        "kosten": ("Es gibt KEINEN eigenen Goldpreis fuer Spionage. Bezahlt werden die Reisekosten "
                   "aus auftraege.kosten_der_mission (VORSCHLAG-Saetze aus A2) und die entsandten "
                   "Spionageeinheiten selbst."),
        "gegenwehr": ("Nicht gebaut: eine Gegenwehr des Dorfes ueber die SI des Verteidigers (die "
                      "Quellen nennen keine). Der Bericht entsteht bei Ankunft; ob die Einheiten "
                      "zurueckkommen, regelt der Auftrag wie jede andere Art."),
    }
