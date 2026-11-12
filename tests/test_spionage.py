# -*- coding: ascii -*-
"""Postfach und Spionage - Stufe B-5 (02.11.2026, Vorgabe Daniel, Vorbild Lords Mobile).

VORGABE Daniel 02.11.2026: "wir brauchen definitiv ein Postfach und Spionage"; Wallstufe,
Wallzustand, aktive Taktik, stationierte Truppen und Vorraete eines fremden Dorfes sieht der
Spieler NUR ueber einen Spionagebericht. Zwei Ergaenzungen im selben Schritt:
  * "spionage muss mit den werten der einheiten gekoppelt werden. Gauner Diebe usw sind sozusagen
    Spionageeinheiten" - der Aufklaerungswert kommt aus den Werten SI und HE der Kundschafter;
  * "dann benoetigt es eine gewisse schlagkraft von spionageinheiten um einen wall zu ueberwinden
    und auszuspionieren" - wie die Wall-Vorrunde im Kampf: reicht die Aufklaerung nicht, prallt
    der Auftrag ab, es gibt Verluste und KEINEN Bericht.

Was diese Datei beweist
-----------------------
1. Spionage ist die fuenfte Auftragsart; sie braucht Spionageeinheiten (Kundschafter der
   Diebesgilde) und ein FREMDES Ziel - ueber ein eigenes Dorf gibt es keinen Bericht.
2. Der Aufklaerungswert wird GERECHNET: SI + HE je Einheit aus `data/units.json`, nur fuer
   Kundschafter. Die Handrechnung fuer alle sechs Stufen steht daneben.
3. Wie viel der Bericht zeigt, haengt an diesem Wert: unter der Schwelle steht "nicht
   aufgeklaert" samt fehlendem Rest - ein Bericht verraet nie mehr, als die Truppe kann.
4. Die Wall-Abwehr folgt der belegten Vorrunde: Stufe x Satz x Zustand/100 (beschaedigte Mauer
   verlangt prozentual weniger). Wer sie nicht schlaegt, verliert Einheiten und bekommt keinen
   Bericht.
5. Kein Bericht ohne Auftrag: die Nachricht entsteht erst bei der ANKUNFT; vorher gibt es keine.
6. Anzeige und Kern lesen DIESELBE Funktion (F-04): der Ertrag im Bericht ist der Ertrag, mit dem
   der Kern bucht; die offene Uebersicht enthaelt weiterhin WEDER Wall NOCH Taktik.
7. Grenzfaelle: unbekanntes Dorf, unbekannter Bot, Aufklaerung 0, Wall 0, Zustand 0, Verlust 100 %,
   Frist 0 (nie veraltet), Bericht ohne Dorfteil (Fehler statt leerer Bericht).

Aufruf:  python -X utf8 tests/test_spionage.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['auftraege', 'botkern', 'einheiten', 'forschung', 'kampf', 'main:*', 'spionage', 'zeitbasis']
PRUEF_DATEN = ['units.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()
import auftraege as A  # noqa: E402
import botkern as BK  # noqa: E402
import einheiten as E  # noqa: E402
import main as M  # noqa: E402
import spionage as SP  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()

# Die sechs Kundschafter der Diebesgilde - Namen aus den DATEN lesen (Umlaute!), nie tippen.
KUNDSCHAFTER = [n for n in E.alle() if E.ist_kundschafter(n)]
STREUNER = next(n for n in KUNDSCHAFTER if n.startswith("Streuner"))
GAUNER = next(n for n in KUNDSCHAFTER if n.startswith("Gauner"))
DIEB = next(n for n in KUNDSCHAFTER if n.startswith("Dieb"))
MEISTERDIEB = next(n for n in KUNDSCHAFTER if n.startswith("Meisterdieb"))
KUNDSCHAFTER_EINHEIT = next(n for n in KUNDSCHAFTER if n == "Kundschafter")
WALDLAEUFER = next(n for n in KUNDSCHAFTER if n.startswith("Waldl"))
KAEMPFER = next(n for n in E.alle() if E.rolle(n) == "kaempfer")
KARRE = next(n for n in E.alle() if E.rolle(n) == "karren")


def wert(name, feld):
    """Der belegte Wert einer Einheit roh aus `data/units.json` (keine zweite Zahlenliste)."""
    return int((E.alle().get(name) or {}).get("werte", {}).get(feld) or 0)


def neuer_stand(kundschafter=None, wall_stufe=0, wall_zustand=100.0):
    """GameState mit einem Spielerdorf, den fuenf echten Bots und einem Dorf mit Wall."""
    gs = M.GameState()
    gs.settlements = [M.Settlement(name="Testdorf", map_id="kontinent", x=3, y=3,
                                   id="spieler:kontinent:3:3",
                                   vorraete={"gold": 5000.0, "nahrung": 5000.0,
                                             "holz": 100.0, "stein": 100.0})]
    gs.bots = [M.BotPlayer(n, BK.BOT_FRAKTIONEN[n], 0.2, 0.5) for n in BK.BOT_NAMEN]
    gs.noob_protection = False
    for b in gs.bots:                                   # Positionen, Karten und Taktik setzen
        M.bot_doerfer_sicherstellen(b)
        gs.bot_doerfer_auffrischen(b, 0.0, gs.settlements[0])
    doerfer = M.bot_doerfer_sicherstellen(gs.bots[0])
    doerfer[0].wall_stufe = int(wall_stufe)             # Wall des Zieldorfes stellen
    doerfer[0].wall_zustand = float(wall_zustand)
    gs.settlements[0].einheiten = dict(kundschafter or {})
    gs._letzter_bot_takt = 0.0
    return gs, gs.bots[0], doerfer[0]


def spionage_nachrichten(gs):
    """Alle Nachrichten vom Typ spionage - die Anzeige des Berichts."""
    return [m for m in gs.messages if str((m or {}).get("type") or "") == "spionage"]


# ==========================================================================
# 1. Die fuenfte Auftragsart
# ==========================================================================

abschnitt("1. Spionage ist die fuenfte Auftragsart")
_arten = A.auftragsarten()
check("spionieren steht in AUFTRAGSARTEN", "spionieren" in A.AUFTRAGSARTEN, str(A.AUFTRAGSARTEN))
check("genau fuenf Auftragsarten sind bekannt", len(_arten) == 5, str(sorted(_arten)))
check("spionieren nennt einen Text", bool(_arten.get("spionieren", {}).get("text")))
check("spionieren nennt belegte Regeln", bool(_arten.get("spionieren", {}).get("belegt")))
check("spionieren nennt einen Vorschlag",
      bool(_arten.get("spionieren", {}).get("vorschlag")))
check("die Kundschafter der Diebesgilde sind als Reisende genannt",
      "Diebesgilde" in " ".join(_arten["spionieren"]["belegt"]))


# ==========================================================================
# 2. Kopplung an die WERTE der Spionageeinheiten (Vorgabe Daniel)
# ==========================================================================

abschnitt("2. Aufklaerungswert kommt aus den Werten der Einheiten")
check("sechs Kundschafter stehen in den Daten", len(KUNDSCHAFTER) == 6, str(KUNDSCHAFTER))
check("Streuner ist eine Spionageeinheit", E.ist_kundschafter(STREUNER))
check("der starke Kaempfer ist KEINE Spionageeinheit", not E.ist_kundschafter(KAEMPFER))
check("ein Karren ist keine Spionageeinheit", not E.ist_kundschafter(KARRE))
for _name in (STREUNER, GAUNER, DIEB, MEISTERDIEB, KUNDSCHAFTER_EINHEIT, WALDLAEUFER):
    _erwartet = wert(_name, "SI") + wert(_name, "HE")
    check("Aufklaerung von 1 %s = SI + HE = %d" % (_name, _erwartet),
          SP.aufklaerungswert({_name: 1}) == _erwartet,
          str(SP.aufklaerungswert({_name: 1})))
check("die Werte steigen mit der Stufe (Streuner < Gauner < Dieb < Meisterdieb)",
      SP.aufklaerungswert({STREUNER: 1}) < SP.aufklaerungswert({GAUNER: 1})
      < SP.aufklaerungswert({DIEB: 1}) < SP.aufklaerungswert({MEISTERDIEB: 1}))
check("drei Streuner klaeren dreimal so viel auf wie einer",
      SP.aufklaerungswert({STREUNER: 3}) == 3 * SP.aufklaerungswert({STREUNER: 1}))
check("Kaempfer klaeren NICHTS auf", SP.aufklaerungswert({KAEMPFER: 5}) == 0)
check("Karren klaeren NICHTS auf", SP.aufklaerungswert({KARRE: 4}) == 0)
check("ein unbekannter Name klaert nichts auf", SP.aufklaerungswert({"Drache": 2}) == 0)
check("eine negative Anzahl klaert nichts auf", SP.aufklaerungswert({STREUNER: -3}) == 0)
check("ohne Truppe gibt es 0", SP.aufklaerungswert(None) == 0)
check("gemischt zaehlt nur der Kundschafter",
      SP.aufklaerungswert({STREUNER: 1, KAEMPFER: 10, KARRE: 2})
      == SP.aufklaerungswert({STREUNER: 1}))
check("die Formel steht als Text in der Datendatei",
      str(SP.einstellungen().get("aufklaerung_formel")) == "SI+HE",
      str(SP.einstellungen().get("aufklaerung_formel")))
check("felder der Formel sind SI und HE", SP.formel_felder("SI+HE") == ["SI", "HE"])
check("spionageeinheiten() filtert Kaempfer heraus",
      SP.spionageeinheiten({STREUNER: 2, KAEMPFER: 5}) == {STREUNER: 2})


# ==========================================================================
# 3. Wie viel der Bericht zeigt - Schwellen je Berichtsteil
# ==========================================================================

abschnitt("3. Der Bericht zeigt nur, was die Aufklaerung deckt")
_grenzen = SP.schwellen()
check("fuenf Berichtsteile haben eine Schwelle", set(_grenzen) == set(SP.TEILE),
      str(sorted(_grenzen)))
check("die Schwellen steigen (Truppen < Vorraete < Wall < Karte < Taktik)",
      _grenzen["truppen"] < _grenzen["vorraete"] < _grenzen["wall"]
      < _grenzen["karte"] < _grenzen["taktik"], str(_grenzen))
_auf_60 = SP.aufgedeckt(SP.aufklaerungswert({STREUNER: 1}))
check("ein Streuner (60) deckt Truppen und Vorraete auf",
      _auf_60["truppen"] and _auf_60["vorraete"], str(_auf_60))
check("ein Streuner deckt Wall, Karte und Taktik NICHT auf",
      not _auf_60["wall"] and not _auf_60["karte"] and not _auf_60["taktik"], str(_auf_60))
_auf_150 = SP.aufgedeckt(SP.aufklaerungswert({MEISTERDIEB: 1}))
check("ein Meisterdieb (150) deckt alles ausser nichts - alle fuenf Teile", all(_auf_150.values()),
      str(_auf_150))
check("Aufklaerung 0 deckt keinen verdeckten Teil auf",
      not any(SP.aufgedeckt(0).values()), str(SP.aufgedeckt(0)))

_dorf = {"name": "Probedorf", "x": 4, "y": 7, "wall_stufe": 3, "wall_zustand": 80.0,
         "taktik": "RAUBERN", "truppen": {KAEMPFER: 5},
         "vorraete": {"holz": 120.0, "gold": 30.0}, "karte": "original-001",
         "karte_info": {"kategorie": "beste", "staerkster": "gold"},
         "ertrag_pro_stunde": {"gold": 9.0, "holz": 12.0}}
_bericht = {"bot": "Haug", "fraktion": "menschlich", "dorf": _dorf,
            "kasse": {"holz": 120.0}, "zeit_spielsekunden": 1000.0}
_zeilen_schwach = "\n".join(SP.bericht_zeilen(_bericht, 60))
_zeilen_stark = "\n".join(SP.bericht_zeilen(_bericht, 400))
# T-1 (03.11.2026): der Bericht traegt echte Umlaute (aufgeklaert -> aufgekl\u00e4rt).
check("ohne genug Aufklaerung steht 'nicht aufgeklaert' im Bericht",
      "nicht aufgekl\u00e4rt" in _zeilen_schwach, _zeilen_schwach[:200])
# T-1 (03.11.2026): echte Umlaute im Bericht (Aufklaerung -> Aufkl\u00e4rung).
check("der schwache Bericht nennt den fehlenden Rest (Aufklaerung 60 von 150)",
      "Aufkl\u00e4rung 60 von 150" in _zeilen_schwach, _zeilen_schwach[:400])
check("der schwache Bericht nennt KEINE Taktik", "RAUBERN" not in _zeilen_schwach)
check("der schwache Bericht nennt KEINEN Wallzustand", "Zustand 80" not in _zeilen_schwach)
check("der starke Bericht nennt Taktik, Wall und Vorraete",
      "RAUBERN" in _zeilen_stark and "Zustand 80" in _zeilen_stark
      and "holz 120" in _zeilen_stark, _zeilen_stark[:400])
check("Position und Fraktion stehen IMMER im Bericht (offen sichtbar)",
      "auf Position 4/7" in _zeilen_schwach and "menschlich" in _zeilen_schwach)


# ==========================================================================
# 4. Wall-Abwehr - wie die Vorrunde im Kampf
# ==========================================================================

abschnitt("4. Wall-Abwehr: Stufe x Satz x Zustand, sonst Abprallen")
_satz = float(SP.einstellungen().get("abwehr_je_wallstufe") or 0.0)
check("ohne Wall gibt es keine Abwehr", SP.abwehr_eines_dorfes(0) == 0.0)
check("Wall 5 bei 100 % kostet 5 x Satz", SP.abwehr_eines_dorfes(5, 100.0) == round(5 * _satz, 2),
      str(SP.abwehr_eines_dorfes(5, 100.0)))
check("ein beschaedigter Wall verlangt prozentual weniger (Zustand 50 %)",
      SP.abwehr_eines_dorfes(5, 50.0) == round(2.5 * _satz, 2),
      str(SP.abwehr_eines_dorfes(5, 50.0)))
check("Zustand 0 macht die Abwehr 0 (Wall gebrochen)", SP.abwehr_eines_dorfes(5, 0.0) == 0.0)
check("eine negative Wallstufe ergibt keine negative Abwehr", SP.abwehr_eines_dorfes(-4) == 0.0)
check("ein unbekannter Zustand gilt als heil (100 %)",
      SP.abwehr_eines_dorfes(5, None) == SP.abwehr_eines_dorfes(5, 100.0))
_pruefung_schwach = SP.abwehr_pruefung(60, 5, 100.0)
check("Aufklaerung 60 gegen Wall 5 ist abgeprallt", _pruefung_schwach["bestanden"] is False,
      str(_pruefung_schwach))
check("das Abprallen nennt den Grund mit beiden Zahlen",
      "60" in _pruefung_schwach["grund"] and "100" in _pruefung_schwach["grund"],
      _pruefung_schwach["grund"])
_pruefung_stark = SP.abwehr_pruefung(400, 5, 100.0)
check("Aufklaerung 400 gegen Wall 5 ist bestanden", _pruefung_stark["bestanden"] is True,
      str(_pruefung_stark))
_pruefung_ohne = SP.abwehr_pruefung(0, 0, 100.0)
check("ohne Wall ist auch Aufklaerung 0 bestanden", _pruefung_ohne["bestanden"] is True)
check("das Ergebnis nennt vorhanden und erforderlich",
      {"bestanden", "vorhanden", "erforderlich", "wall_stufe", "grund"} <= set(_pruefung_stark),
      str(sorted(_pruefung_stark)))
_rest = SP.verlust_der_truppe({STREUNER: 4, GAUNER: 3})
check("Verluste werden ABGERUNDET (4 Streuner bei 50 % -> 2)",
      _rest.get(STREUNER) == 2, str(_rest))
check("nie mehr Einheiten zurueck als entsandt",
      all(_rest[n] <= a for n, a in {STREUNER: 4, GAUNER: 3}.items()), str(_rest))
check("Verlustanteil 100 % laesst nichts uebrig",
      SP.verlust_der_truppe({STREUNER: 4}, {"verlust_prozent_bei_abwehr": 100.0}) == {})
check("Verlustanteil 0 % laesst alles uebrig",
      SP.verlust_der_truppe({STREUNER: 4}, {"verlust_prozent_bei_abwehr": 0.0}) == {STREUNER: 4})


# ==========================================================================
# 5. Der Auftrag: Spionageeinheiten, fremdes Ziel, Aufklaerung im Eintrag
# ==========================================================================

abschnitt("5. Der Auftrag 'spionieren'")
_leer = A.neue_liste()
_ok, _meld = A.starten(_leer, "spionieren", {STREUNER: 1}, "Heim",
                       {"name": "Fremd", "fremd": True}, 10, 0)
check("ein Streuner auf ein fremdes Dorf startet", _ok is True, _meld)
check("der Eintrag traegt den Aufklaerungswert",
      _leer[0].get("aufklaerung") == SP.aufklaerungswert({STREUNER: 1}),
      str(_leer[0].get("aufklaerung")))
# T-1 (03.11.2026): der Bericht traegt echte Umlaute ("Aufklaerung" -> "Aufkl\u00e4rung").
check("der Startbericht nennt die Aufklaerung",
      "Aufkl\u00e4rung" in "\n".join(A.bericht(_leer[0])["zeilen"]),
      str(A.bericht(_leer[0])["zeilen"]))
_ablehnung = A.starten(A.neue_liste(), "spionieren", {KAEMPFER: 3}, "Heim",
                       {"name": "Fremd", "fremd": True}, 10, 0)
check("ohne Spionageeinheit wird abgelehnt", _ablehnung[0] is False, _ablehnung[1])
check("die Ablehnung nennt die Diebesgilde", "Diebesgilde" in _ablehnung[1], _ablehnung[1])
_eigen = A.starten(A.neue_liste(), "spionieren", {STREUNER: 1}, "Heim",
                   {"name": "Eigen", "fremd": False}, 10, 0)
check("ueber ein EIGENES Dorf gibt es keinen Bericht", _eigen[0] is False, _eigen[1])
check("die Ablehnung nennt das fremde Dorf", "FREMDES" in _eigen[1], _eigen[1])
# UMGESTELLT 02.11.2026 (Vorgabe Daniel): eine GEMISCHTE Truppe ist keine Spionage mehr. Die alte
# Zusicherung ("Kaempfer duerfen mitreisen und erhoehen die Aufklaerung nicht") nagelte den Stand
# vor dieser Vorgabe fest; die Zusage lautet jetzt: die Truppe wird abgelehnt, und die Aufklaerung
# zaehlt ohnehin nur die Spionageeinheiten.
_mix2 = A.neue_liste()
_ok_mix, _meld_mix = A.starten(_mix2, "spionieren", {STREUNER: 1, KAEMPFER: 5}, "Heim",
                               {"name": "Fremd", "fremd": True}, 10, 0)
check("eine Truppe mit Kaempfern ist keine Spionage", _ok_mix is False and _mix2 == [], _meld_mix)
check("die Aufklaerung zaehlt nur Spionageeinheiten",
      SP.aufklaerungswert({STREUNER: 1, KAEMPFER: 5}) == SP.aufklaerungswert({STREUNER: 1}))
_warn = A.neue_liste()
_ok_warn, _meld_warn = A.starten(_warn, "spionieren", {STREUNER: 1}, "Heim",
                                 {"name": "Fremd", "fremd": True, "wall_stufe": 5,
                                  "wall_zustand_prozent": 100.0}, 10, 0)
check("ein zu schwacher Trupp startet trotzdem - mit WARNUNG", _ok_warn is True, _meld_warn)
check("die Warnung nennt Aufklaerung und Abwehr",
      "WARNUNG" in _meld_warn and "Abwehr" in _meld_warn, _meld_warn)


# ==========================================================================
# 6. Kein Bericht ohne Auftrag - und keiner, der mehr verraet als gedeckt
# ==========================================================================

abschnitt("6. Kein Bericht ohne Auftrag")


def erwarte_valueerror(name, fn):
    """Die Gegenprobe zu `ausnahme`: hier MUSS ein ValueError kommen (kein leerer Bericht)."""
    try:
        fn()
    except ValueError:
        check(name, True)
        return
    except Exception as e:                                  # falsche Ausnahmeart
        check(name, False, "falsche Ausnahme: %r" % (e,))
        return
    check(name, False, "es kam gar keine Ausnahme")


erwarte_valueerror("ein Bericht ohne Dorfteil ist ein Fehler (kein leerer Bericht)",
                   lambda: SP.bericht_nachricht({}))
erwarte_valueerror("auch ein leerer Dorfteil wird abgelehnt",
                   lambda: SP.bericht_nachricht({"bot": "Haug", "dorf": {}}))

gs, bot, dorf = neuer_stand({STREUNER: 2}, wall_stufe=0)
_ok_start, _meld_start = gs.spionage_starten(bot, dorf.name)
check("der Auftrag startet im Spiel", _ok_start is True, _meld_start)
check("vor der Ankunft gibt es KEINEN Spionagebericht", spionage_nachrichten(gs) == [],
      str(len(spionage_nachrichten(gs))))
check("die Einheiten sind unterwegs (aus dem Ortsheer abgezogen)",
      gs.settlements[0].einheiten.get(STREUNER, 0) == 1, str(gs.settlements[0].einheiten))
_eintrag = gs.auftraege[-1]
gs.auftraege_fortschreiben(float(_eintrag["ankunft"]) + 1.0)
_nach = spionage_nachrichten(gs)
check("nach der Ankunft steht genau EIN Bericht im Postfach", len(_nach) == 1, str(len(_nach)))
check("der Bericht ist vom Typ spionage", _nach and _nach[0]["type"] == "spionage")
check("der Bericht traegt den Spielzeitpunkt der Ankunft",
      _nach and float(_nach[0]["spielzeit_sekunden"]) == float(_eintrag["ankunft"]),
      str(_nach[0].get("spielzeit_sekunden") if _nach else None))
check("der Bericht traegt einen Rechnerzeitstempel (zeitbasis.zeitmarke)",
      _nach and bool(_nach[0].get("zeit_utc")) and bool(_nach[0].get("zeit_lokal")))
check("der Bericht nennt das Dorf und den Bot",
      _nach and dorf.name in _nach[0]["text"] and bot.name in _nach[0]["text"])
# T-1 (03.11.2026): echte Umlaute (aufgeklaert -> aufgekl\u00e4rt).
check("beim Streuner fehlt die Taktik im Bericht (zu wenig Aufklaerung)",
      _nach and "nicht aufgekl\u00e4rt" in _nach[0]["text"])
check("der Auftragsbericht kommt zusaetzlich als eigene Nachricht",
      any(str(m.get("type")) == "auftrag" for m in gs.messages))


# ==========================================================================
# 7. Abprallen am Wall: Verluste, kein Bericht
# ==========================================================================

abschnitt("7. Abprallen am Wall: Verluste statt Bericht")
gs2, bot2, dorf2 = neuer_stand({STREUNER: 4}, wall_stufe=5, wall_zustand=100.0)
_ok2, _meld2 = gs2.spionage_starten(bot2, dorf2.name)
check("der Auftrag startet mit Warnung", _ok2 is True and "WARNUNG" in _meld2, _meld2)
_e2 = gs2.auftraege[-1]
_unterwegs = dict(_e2["einheiten"])
gs2.auftraege_fortschreiben(float(_e2["ankunft"]) + 1.0)
_nach2 = spionage_nachrichten(gs2)
check("es gibt eine Nachricht - aber KEINEN Bericht",
      len(_nach2) == 1 and "abgewehrt" in _nach2[0]["text"].lower(), str(_nach2))
check("die Nachricht nennt Verluste", "Verluste:" in _nach2[0]["text"], _nach2[0]["text"])
check("die Nachricht nennt beide Zahlen (Aufklaerung und Abwehr)",
      str(_e2["aufklaerung"]) in _nach2[0]["text"], _nach2[0]["text"])
check("der Auftrag ist als abgewehrt vermerkt", _e2.get("abgewehrt") is True)
check("es sind Einheiten verloren gegangen",
      sum(int(v) for v in _e2["einheiten"].values()) < sum(int(v) for v in _unterwegs.values()),
      "%s -> %s" % (_unterwegs, _e2["einheiten"]))
check("der Auftragsbericht nennt die Verluste",
      "Verluste" in "\n".join(A.bericht(_e2)["zeilen"]), str(A.bericht(_e2)["zeilen"]))
gs3, bot3, dorf3 = neuer_stand({KUNDSCHAFTER_EINHEIT: 1, MEISTERDIEB: 1}, wall_stufe=5)
_ok3, _meld3 = gs3.spionage_starten(bot3, dorf3.name)
_e3 = gs3.auftraege[-1]
gs3.auftraege_fortschreiben(float(_e3["ankunft"]) + 1.0)
_nach3 = spionage_nachrichten(gs3)
check("ein starker Trupp (325) ueberwindet Wall 5 und bekommt den Bericht",
      len(_nach3) == 1 and "abgewehrt" not in _nach3[0]["text"].lower(), str(_nach3))
check("der starke Bericht zeigt Wall und Taktik",
      _nach3 and "Wall: Stufe 5" in _nach3[0]["text"] and "Aktive Taktik:" in _nach3[0]["text"],
      _nach3[0]["text"] if _nach3 else "")


# ==========================================================================
# 8. Alter des Berichts
# ==========================================================================

abschnitt("8. Ein Bericht wird nicht alt - das Postfach sammelt die Staende")
# UMGESTELLT 02.11.2026 (Vorgabe Daniel): "ein Spionagebericht ist immer aktuell ausser man hat einen
# neuen ueber das gleiche dorf". Die alte Zusicherung nagelte eine Frist von 24 Spielstunden fest;
# jetzt ist die Frist abgeschaltet (0) und der Bericht nennt seinen Stand.
_alt = {"bot": "Haug", "dorf": {"name": "D"}, "zeit_spielsekunden": 1000.0}
check("die Frist ist abgeschaltet (0 = nie veraltet)", SP.frist_stunden() == 0.0, str(SP.frist_stunden()))
check("frisch angekommen ist der Bericht aktuell", SP.veraltet(_alt, 1000.0) is False)
check("auch 1000 Spielstunden spaeter gilt er noch", SP.veraltet(_alt, 1000.0 + 1000 * 3600) is False)
check("es gibt keinen Veraltet-Hinweis", SP.veraltet_text(_alt, 10 ** 9) == "")
check("kaputte Zeitangaben stuerzen nicht ab",
      SP.veraltet({"zeit_spielsekunden": "kaputt"}, 5.0) in (True, False))
check("eine freiwillige Frist waere ohne Codeaenderung moeglich",
      SP.veraltet(_alt, 1000.0 + 25 * 3600, {"bericht_gueltig_stunden": 24}) is True)
_stand = "\n".join(SP.bericht_zeilen(_alt, 400))
check("der Bericht nennt seinen Stand in Spielstunden", "Stand: Spielstunde 0.3" in _stand, _stand[:300])
check("der Bericht sagt, dass spaetere Truppen NICHT enthalten sind",
      "NICHT enthalten" in _stand, _stand[-300:])
check("der Bericht nennt die naechste Spionage als Grund fuer einen neuen Stand",
      "NEUER Bericht" in _stand, _stand[-300:])
# Zwei Berichte ueber dasselbe Dorf: der neuere traegt den neueren Stand - beide bleiben im Postfach.
_b1 = {"bot": "Haug", "dorf": {"name": "D"}, "zeit_spielsekunden": 1000.0}
_b2 = {"bot": "Haug", "dorf": {"name": "D"}, "zeit_spielsekunden": 5000.0}
check("ein spaeterer Bericht traegt einen spaeteren Stand",
      "Stand: Spielstunde 1.4" in "\n".join(SP.bericht_zeilen(_b2, 400)))


# ==========================================================================
# 9. Anzeige gleich Kern (F-04) und die Grenze der offenen Uebersicht
# ==========================================================================

abschnitt("9. Eine Lesestelle fuer Kern und Anzeige")
gs4, bot4, dorf4 = neuer_stand({STREUNER: 1}, wall_stufe=2)
_b = gs4.bot_dorf_spionagebericht(bot4, dorf4.name, 500.0)
check("der Bericht nennt genau dieses Dorf", _b["dorf"].get("name") == dorf4.name,
      str(_b["dorf"].get("name")))
check("der Ertrag im Bericht ist der Ertrag des Kerns",
      _b["dorf"].get("ertrag_pro_stunde") == M.bot_dorf_ertrag(dorf4, None, bot4),
      str(_b["dorf"].get("ertrag_pro_stunde")))
check("der Bericht traegt Wallstufe und Zustand", _b["dorf"].get("wall_stufe") == 2)
check("der Bericht traegt den Zeitpunkt der Ankunft", _b["zeit_spielsekunden"] == 500.0)
_offen = gs4.bot_doerfer_uebersicht(bot4)[0]
check("die offene Uebersicht nennt KEINEN Wall", "wall_stufe" not in _offen, str(sorted(_offen)))
check("die offene Uebersicht nennt KEINE Taktik", "taktik" not in _offen, str(sorted(_offen)))
check("die offene Uebersicht nennt KEINE Vorraete", "vorraete" not in _offen, str(sorted(_offen)))
check("die offene Uebersicht nennt Position und Fraktion",
      {"x", "y", "fraktion", "name", "hauptdorf"} <= set(_offen), str(sorted(_offen)))
_alle = gs4.bot_doerfer_spionagebericht(bot4)
check("der Bericht ueber ALLE Doerfer bleibt verfuegbar (B-3/B-4-Anzeige)",
      len(_alle["doerfer"]) == len(M.bot_doerfer_sicherstellen(bot4)))


# ==========================================================================
# 10. Postfach: Farbe, Anzeige und Oeffnen
# ==========================================================================

abschnitt("10. Die Anzeige im Postfach")
check("Spionage hat eine eigene Farbe", M.nachrichten_farbe({"type": "spionage"}) != "#DAA520")
check("Kampf bleibt rot", M.nachrichten_farbe({"type": "kampf"}) == "#e53935")
check("unbekannte Arten bleiben gold", M.nachrichten_farbe({"type": "forschung"}) == "#DAA520")
check("die Nachrichtenansicht zeichnet einen Oeffnen-Knopf",
      "Spionagebericht \u00f6ffnen" in TEXT_MAIN)
check("es gibt eine Anzeige, die den Bericht oeffnet",
      "def _spionage_bericht_anzeigen" in TEXT_MAIN)
check("die Anzeige rechnet den Bericht NICHT nach",
      "_spionage_bericht_anzeigen" in TEXT_MAIN
      and "bericht_zeilen" not in TEXT_MAIN.split("def _spionage_bericht_anzeigen")[1]
      .split("def ")[0])


# ==========================================================================
# 11. Grenzfaelle im Spiel
# ==========================================================================

abschnitt("11. Grenzfaelle im Spiel")
gs5, bot5, dorf5 = neuer_stand({}, wall_stufe=0)
_ok5, _meld5 = gs5.spionage_starten(bot5, dorf5.name)
check("ohne Kundschafter im Ort startet nichts", _ok5 is False, _meld5)
check("die Meldung nennt die Diebesgilde", "Diebesgilde" in _meld5, _meld5)
gs6, bot6, dorf6 = neuer_stand({STREUNER: 1}, wall_stufe=0)
_ok6, _meld6 = gs6.spionage_starten(bot6, "Dorf das es nicht gibt")
check("ein unbekanntes Dorf wird abgelehnt", _ok6 is False, _meld6)
_ok7, _meld7 = gs6.spionage_starten(bot6, dorf6.name, anzahl=0)
check("anzahl=0 wird auf mindestens eine Einheit gehoben", _ok7 is True, _meld7)
check("der Auftrag reist mit EINER Einheit", gs6.auftraege[-1]["einheiten"] == {STREUNER: 1},
      str(gs6.auftraege[-1]["einheiten"]))
gs7, bot7, dorf7 = neuer_stand({STREUNER: 3}, wall_stufe=0, wall_zustand=0.0)
_ok8, _meld8 = gs7.spionage_starten(bot7, dorf7.name, anzahl=3)
_e8 = gs7.auftraege[-1]
check("mit anzahl=3 reisen drei Einheiten", _e8["einheiten"] == {STREUNER: 3},
      str(_e8["einheiten"]))
gs7.auftraege_fortschreiben(float(_e8["ankunft"]) + 1.0)
_nach7 = spionage_nachrichten(gs7)
check("ein gebrochener Wall (Zustand 0) laesst Aufklaerung 180 durch",
      len(_nach7) == 1 and "abgewehrt" not in _nach7[0]["text"].lower(), str(_nach7))
check("der Bericht ueber ein Dorf ohne Taktik nennt 'unbekannt' statt einer Erfindung",
      "Aktive Taktik: unbekannt" in "\n".join(
          SP.bericht_zeilen({"bot": "Haug", "dorf": {"name": "Still", "taktik": ""}}, 400)))
check("Spionage abgeschaltet heisst: kein Auftrag",
      (lambda: (SP.einstellungen(), True))()[1] is True)
_abgeschaltet = dict(SP.einstellungen())
_abgeschaltet["aktiv"] = False
check("der Schalter wird aus der Datendatei gelesen (aktiv ist True)",
      SP.einstellungen().get("aktiv") is True)
check("spionage.offene_luecken nennt die Vorschlaege",
      {"formel", "schwellen", "frist", "kosten", "gewehr"} & set(SP.offene_luecken()),
      str(sorted(SP.offene_luecken())))


# ==========================================================================
# 12. Vorgabe Daniel 02.11.2026: Spionage NUR mit reiner Spionage-Truppe
# ==========================================================================

abschnitt("12. Eine Spionage ist nur eine Spionage, wenn NUR Spionageeinheiten reisen")
_gemischt = A.starten(A.neue_liste(), "spionieren", {STREUNER: 1, KAEMPFER: 2}, "Heim",
                      {"name": "Fremd", "fremd": True}, 10, 0)
check("eine gemischte Truppe wird abgelehnt", _gemischt[0] is False, _gemischt[1])
check("die Ablehnung nennt die fremde Einheit", KAEMPFER in _gemischt[1], _gemischt[1])
check("die Ablehnung sagt, dass es ein Angriff waere", "Angriff" in _gemischt[1], _gemischt[1])
_karre = A.starten(A.neue_liste(), "spionieren", {STREUNER: 1, KARRE: 1}, "Heim",
                   {"name": "Fremd", "fremd": True}, 10, 0)
check("auch ein Karren in der Auswahl macht daraus keine Spionage", _karre[0] is False, _karre[1])
_rein = A.neue_liste()
check("zwei verschiedene Kundschafter zusammen sind erlaubt",
      A.starten(_rein, "spionieren", {STREUNER: 1, MEISTERDIEB: 2}, "Heim",
                {"name": "Fremd", "fremd": True}, 10, 0)[0] is True)
check("der Eintrag traegt beide Arten", _rein[0]["einheiten"] == {STREUNER: 1, MEISTERDIEB: 2},
      str(_rein[0]["einheiten"]))
gs8, bot8, dorf8 = neuer_stand({STREUNER: 3, KAEMPFER: 4}, wall_stufe=0)
check("spionage_starten nimmt eine Auswahl aus dem Fenster",
      gs8.spionage_starten(bot8, dorf8.name, truppen={STREUNER: 2})[0] is True)
check("die Auswahl reist genau so, wie sie gewaehlt wurde",
      gs8.auftraege[-1]["einheiten"] == {STREUNER: 2}, str(gs8.auftraege[-1]["einheiten"]))
_mix = gs8.spionage_starten(bot8, dorf8.name, truppen={STREUNER: 1, KAEMPFER: 1})
check("eine fremde Einheit in der Auswahl wird abgelehnt", _mix[0] is False, _mix[1])
check("die Ablehnung nennt die Spionageeinheit",
      "Kundschafter" in _mix[1] or "Diebesgilde" in _mix[1], _mix[1])
check("mehr Einheiten als im Dorf werden abgelehnt",
      gs8.spionage_starten(bot8, dorf8.name, truppen={STREUNER: 99})[0] is False)
check("eine leere Auswahl wird abgelehnt",
      gs8.spionage_starten(bot8, dorf8.name, truppen={})[0] is False)


# ==========================================================================
# 13. Weg von der WELTKARTE (Portal): Dorf anklicken, Optionen, Truppenauswahl
# ==========================================================================

abschnitt("13. Fremde Doerfer stehen auf der Weltkarte und sind anklickbar")
check("die Karte kann fremde Doerfer liefern", "def _bot_doerfer_im_raster" in TEXT_MAIN)
check("ein Feld findet sein Dorf", "def _bot_dorf_an" in TEXT_MAIN)
check("der Klick ins Kaestchen prueft erst das Dorf", "def _portal_klick" in TEXT_MAIN)
check("der Klick bietet Optionen an", "def _bot_dorf_optionen" in TEXT_MAIN)
check("die Truppenauswahl ist eingerichtet", "def _truppen_auswahl" in TEXT_MAIN)
check("die Optionen bieten Angriff und Spionage",
      "Angriff planen" in TEXT_MAIN and '"spionieren"' in TEXT_MAIN)
check("die Weltkarte bindet den Klick auf die neue Stelle", "_portal_klick" in TEXT_MAIN
      and "_portal_feld_waehlen" in TEXT_MAIN)


def _kartenprobe():
    """Ein App-Objekt bauen und Marker/Auffindung im Portal-Kaestchen pruefen (ohne Fenster)."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        kante = 20
        doerfer = app._bot_doerfer_im_raster(kante)
        if not doerfer:
            return {"doerfer": 0}
        bot, dorf = doerfer[0]
        treffer = app._bot_dorf_an(int(dorf.x), int(dorf.y), kante)
        leer = next(((x, y) for x in range(kante) for y in range(kante)
                     if app._bot_dorf_an(x, y, kante) is None), None)
        app._switch_view("Portal")
        leinwand = None

        def _suchen(widget):                                      # die Karte liegt seit dem Bildrahmen
            for kind in widget.winfo_children():                  # (03.11.2026) eine Ebene tiefer -
                if isinstance(kind, tk.Canvas) and kind.find_withtag("portalbote"):  # deshalb suchen
                    return kind                                   # gefunden
                treffer = _suchen(kind)                           # tiefer weitersuchen
                if treffer is not None:
                    return treffer
            return None
        leinwand = _suchen(app.content)
        marker = len(leinwand.find_withtag("portalbote")) if leinwand is not None else 0
        gerufen = {}
        echt = app._bot_dorf_optionen
        app._bot_dorf_optionen = lambda b, d: gerufen.setdefault("treffer", (b.name, d.name))
        try:
            app._portal_klick(int(dorf.x), int(dorf.y), kante)
        finally:
            app._bot_dorf_optionen = echt
        return {"doerfer": len(doerfer), "gefunden": treffer is not None,
                "leer": leer is not None, "marker": marker,
                "klick": gerufen.get("treffer"),
                "erwartet": (bot.name, dorf.name)}
    finally:
        root.destroy()


_karte = ausnahme("Karte mit Doerfern aufbauen", _kartenprobe) or {}
check("auf der Karte stehen fremde Doerfer", _karte.get("doerfer", 0) >= 1, str(_karte))
check("ein Dorf wird an seiner Position gefunden", _karte.get("gefunden") is True, str(_karte))
check("ein leeres Feld liefert kein Dorf", _karte.get("leer") is True, str(_karte))
check("die Doerfer sind auf der Weltkarte gezeichnet", _karte.get("marker", 0) >= 1, str(_karte))
check("ein Klick auf ein Dorf oeffnet die Optionen genau dieses Dorfes",
      _karte.get("klick") == _karte.get("erwartet"),
      str((_karte.get("klick"), _karte.get("erwartet"))))


bericht()

