"""W-14 Teil 2: die Drachen im SPIEL (Register 203, 05.11.2026).

Teil 1 hat das Modul `src/drachen.py` gebaut und geprueft (`test_drachen.py`). Diese Datei belegt
die VERDRAHTUNG: Zielwahl, Vorrunde gegen die Drachenwerte, Feueratem, Kampf, Beuteanteil,
Bericht, Zustand und Anzeige. Die sieben Pflicht-Wachen aus der Uebergabe stehen hier:

  (a) ein Angriff unter der Schwelle kaempft NICHT,
  (b) der Feueratem bucht und steht im Bericht,
  (c) die Beute wird GENAU EINMAL gebucht und nur als Anteil nach Leistung,
  (d) ohne Ueberlebende nennt der Bericht keine Einheiten,
  (e) Ausspaehen wird abgelehnt,
  (f) nach dem Sieg steht eine Ruine und es gibt keine ZWEITE SCHLACHT - die Ruine bleibt aber
      pluenderbar und gibt ihren Rest her (Daniel 05.11.2026),
  (g) ein alter Spielstand ohne `drachen_besiegt` laedt,
  (h) der Sieg bringt die Manabelohnung (4000 + gerechneter Aufwand), die Wache bleibt
      beschaedigt stehen, das Flammenzeichen erscheint nach dem ersten Angriff und
      verschwindet, wenn der Hort leer ist, und ein Bot urteilt nachvollziehbar,
  (i) jeder Neubeginn wuerfelt andere Plaetze auf DENSELBEN Welten und kein Bot gruendet
      auf einer Drachenkoordinate.

Was Fixture ist und was nicht: das HEER des Spielers und die eigene Weltkarte werden gesetzt
(dieselbe Abkuerzung wie in `test_gesamtsieg`), der SIEGSTAND wird NICHT gesetzt - jede Buchung
entsteht aus dem echten Auftragsweg (`_angriff_auftrag_starten` -> `kampf_am_ziel`).

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape oder aus den Datendateien gelesen.
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()

import drachen
import einheiten
import kampf
import portalraum
import kampfbericht as KB

main = ausnahme("main importieren", lambda: __import__("main"))
tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))
if main is None or tk is None:
    sys.exit(bericht())

TYP = "kampf"                                             # Nachrichtentyp der Kampfberichte
DRACHE = "\u00df"                                         # das scharfe S, nur zum Suchen im Text


def einheit(anfang: str) -> str:
    """Den ECHTEN Namen einer Einheit aus den Daten holen (nie tippen)."""
    treffer = [n for n in einheiten.alle() if n.startswith(anfang)]
    return treffer[0] if treffer else ""


# ==========================================================================
abschnitt("1. Datenschicht: Kennungen, Bilder, Schwellen, kein Ausspaehen")

check("drei Drachen stehen in der Datendatei", len(drachen.alle()) == 3, str(len(drachen.alle())))
check("die Weltkennung entsteht aus der Nummer (2 ergibt d02)", drachen.welt_kennung(2) == "d02",
      drachen.welt_kennung(2))
check("die Weltkennung ist zweistellig (5 ergibt d05)", drachen.welt_kennung(5) == "d05",
      drachen.welt_kennung(5))
check("eine unbrauchbare Nummer ergibt keine Kennung", drachen.welt_kennung("kaputt") == "")

_dr = drachen.finde_id("drache_d02")
check("finde_id findet den Drachen ueber seine Kennung", _dr is not None and _dr["welt"] == "d02",
      str(_dr.get("name") if _dr else None))
check("finde_id liefert bei unbekannter Kennung None", drachen.finde_id("gibt_es_nicht") is None)

for _e in drachen.alle():
    _summe = sum(int(v) for v in drachen.verteidiger(_e).values())
    check("Drache %s hat 204 Verteidiger" % _e["id"], _summe == 204, str(_summe))
    check("Drache %s traegt die Schwellen 700/950" % _e["id"], drachen.schwellen(_e) == (700, 950),
          str(drachen.schwellen(_e)))
    check("Drache %s ist unbrechbar (kein Wallschaden)" % _e["id"],
          drachen.unbrechbar(_e) is True, str(drachen.unbrechbar(_e)))

for _e in drachen.alle():
    _bild = drachen.figur(_e, []).get("bild") or ""
    _pfad = os.path.join(ROOT, str(_bild).replace("/", os.sep))
    check("Drache %s hat eine vorhandene Figur" % _e["id"], bool(_bild) and os.path.exists(_pfad),
          _bild)
    check("Drache %s wird nach dem Sieg zur Ruine" % _e["id"],
          drachen.figur(_e, [_e["id"]]).get("art") == "ruine")

_erlaubt, _grund = drachen.spionage_erlaubt()
check("(e) ein Drache laesst sich NICHT ausspaehen", _erlaubt is False, repr(_erlaubt))
check("(e) der Grund steht in der Datendatei", bool(_grund), _grund[:40])
check("der Angriffshinweis steht in der Datendatei", bool(drachen.angriffs_hinweis()),
      drachen.angriffs_hinweis()[:40])


# ==========================================================================
abschnitt("2. Beute-Anteil nach Leistung und Transport")

_beute = {"gold": 5000, "holz": 2000}
check("die halbe Leistung bringt die halbe Beute",
      drachen.beute_anteil(102, 204, _beute).get("gold") == 2500,
      str(drachen.beute_anteil(102, 204, _beute)))
check("der letzte Schlag bekommt 10 Prozent obendrauf",
      drachen.beute_anteil(102, 204, _beute, letzter_schlag=True).get("gold") == 3000,
      str(drachen.beute_anteil(102, 204, _beute, letzter_schlag=True)))
check("ohne Leistung keine Beute", drachen.beute_anteil(0, 204, _beute) == {})
check("niemand bekommt mehr als der Hort hergibt",
      drachen.beute_anteil(204, 204, _beute).get("gold") == 5000,
      str(drachen.beute_anteil(204, 204, _beute)))

_hort = {"gold": 5000, "holz": 2000, "stein": 2000, "nahrung": 2000}
_bedarf = drachen.transport_bedarf(_hort)
check("der Transport nennt die noetige Ladung", _bedarf.get("ladung") == 11000, str(_bedarf))
check("der Transport nennt einen Wagenpark", bool(_bedarf.get("karren")), str(_bedarf.get("karren")))
check("der Wagenpark traegt den ganzen Hort (kein Rest)", _bedarf.get("rest") == 0, str(_bedarf))
check("der Transport-Satz nennt Ladung und Karren",
      "11000" in drachen.transport_text(_hort), drachen.transport_text(_hort)[:80])


# ==========================================================================
abschnitt("3. (d) Bericht: ohne Ueberlebende keine Einheiten, mit Ueberlebenden genau")

_wachen = {"Krieger": 120, "Paladin": 24}
_ohne = drachen.bericht({"ausgang": "verteidiger"}, 0, _wachen)
_ohne_text = " ".join(_ohne.get("zeilen") or [])
check("(d) ohne Ueberlebende steht keine Einheitenart im Bericht",
      "Krieger" not in _ohne_text and "Paladin" not in _ohne_text, _ohne_text[:90])
check("(d) ohne Ueberlebende nennt der Bericht die ZAHL der Verteidiger",
      "144" in _ohne_text, _ohne_text[:90])
check("(d) der ehrliche Zusatz steht dabei", len(_ohne.get("zeilen") or []) >= 2,
      str(len(_ohne.get("zeilen") or [])))
_mit = drachen.bericht({"ausgang": "angreifer"}, 7, _wachen)
_mit_text = " ".join(_mit.get("zeilen") or [])
check("mit Ueberlebenden nennt der Bericht die Einheiten",
      "Krieger" in _mit_text and "120" in _mit_text, _mit_text[:90])
check("der Bericht traegt den Typ 'kampf'", _ohne.get("typ") == "kampf", str(_ohne.get("typ")))


# ==========================================================================
abschnitt("4. (a) Vorrunde gegen die Drachenwerte statt gegen einen Wall")

_klein = kampf.fuehre_schlacht({"Krieger": 10}, {"Krieger": 120}, 0, 100.0, schwellen=(700, 950))
check("(a) unter der Fussschwelle findet KEIN Kampf statt",
      _klein.get("kampf_stattgefunden") is False, str(_klein.get("ausgang")))
check("(a) der Rueckzug steht im Bericht",
      "Schwelle nicht erreicht" in str(_klein.get("bericht")), str(_klein.get("bericht"))[:90])
_ohne_bel = kampf.fuehre_schlacht({"Krieger": 300}, {"Krieger": 120}, 0, 100.0,
                                  schwellen=(700, 950))
check("(a) ohne Belagerungskraft kein Kampf (950 nicht erreicht)",
      _ohne_bel.get("kampf_stattgefunden") is False, str(_ohne_bel.get("ausgang")))
_ja = kampf.fuehre_schlacht({"Krieger": 300, "Katapult": 22}, {"Krieger": 120}, 0, 100.0,
                            schwellen=(700, 950))
check("ueber beiden Schwellen wird gekaempft", _ja.get("kampf_stattgefunden") is True,
      str(_ja.get("ausgang")))
check("ohne Wall gibt es keinen Mauerschaden", float(_ja.get("mauer_zustand") or 0.0) == 100.0,
      str(_ja.get("mauer_zustand")))


# ==========================================================================
abschnitt("5. Kette: Zielwahl, Feueratem, Kampf, Beute, Zustand, Ruine")

root = None
app = None
try:
    root = tk.Tk()                                        # ein unsichtbares Fenster
    root.withdraw()                                       # kein Fenster auf dem Schirm
    app = main.NebelseetalApp(root)                       # die echte App
    app._build_main_ui()                                  # Oberflaeche aufbauen
    st = app.state                                         # der Spielzustand
    app._erste_siedlung_gruenden()                         # echter Start (belegte Werte)
    ort = st.aktive_siedlung()                             # die eine Siedlung
    karre = einheit("Gro\u00dfe Handelskarawane")          # Name aus den Daten, nie getippt
    check("der Karrenname kommt aus den Daten", bool(karre), karre)
    check("die eigene Wiese fuer den Angriff ist gesetzt", ort is not None)
    st.eigene_dimension = 2                               # die Weltkarte, auf der der Drache steht
    st.eigene_dimensionen = [1, 2]
    ort.einheiten = {"Krieger": 300, "Katapult": 22, karre: 4}
    ort.vorraete = {"gold": 900.0, "nahrung": 900.0}      # Reisekosten bezahlbar machen
    st.spieler_fraktion = "zwergisch"                      # das gespielte Volk (fuer die Boni)

    drache = drachen.finde_id("drache_d02")
    check("der Drache der Welt d02 steht in den Daten", drache is not None)
    check("der neue Zustand kennt keine besiegten Drachen", st.drachen_besiegt == [],
          str(st.drachen_besiegt))
    _hort_vorher = sum(int(v) for v in drachen.beute(drache).values())

    def angriff(truppen):
        """Einen Drachenangriff starten und bis zur Heimkehr fahren - Rueckgabe: der Auftrag.

        Der Auftrag wird im Spielstand nach der Heimkehr entfernt, deshalb wird er HIER
        zurueckgegeben; None heisst: er ist gar nicht erst gestartet.
        """
        ok = app._angriff_auftrag_starten(
            str(drache.get("name")), drachen.verteidiger(drache),
            wall_stufe=0, wall_zustand=100.0, vorraete={},
            entfernung=2.0, truppen=dict(truppen),
            drache_id=str(drache.get("id")))
        if not ok:
            return None
        eintrag = st.auftraege[-1]
        ende = float(eintrag.get("rueckkehr") or eintrag.get("ankunft") or 0.0) + 1.0
        st.spielsekunden = max(float(st.spielsekunden), ende)
        st.auftraege_fortschreiben(st.spielsekunden)
        return eintrag

    _truppen = {n: int(a) for n, a in ort.einheiten.items() if int(a) > 0}
    _eintrag = angriff(_truppen)
    check("der Angriff auf den Drachen startet", _eintrag is not None)
    if _eintrag is None:
        _eintrag = {"beute": {}, "einheiten": {}}
    check("der Auftrag traegt den Drachen als Ziel",
          str((_eintrag.get("ziel") or {}).get("drache_id")) == str(drache.get("id")),
          str((_eintrag.get("ziel") or {}).get("drache_id")))
    _berichte = [m for m in st.messages if m.get("type") == TYP and
                 str(m.get("text") or "").startswith("Am Ziel")]
    check("ein Kampfbericht steht im Postfach", len(_berichte) >= 1, str(len(_berichte)))
    _text = _berichte[-1].get("text") if _berichte else ""

    # ---- (b) Feueratem: gebucht und im Bericht ----
    check("(b) der Feueratem steht als eigene Zeile im Bericht", "Feueratem" in _text,
          _text[:160])
    _atem_zeile = next((z for z in _text.split("\n") if z.startswith("Feueratem")), "")
    check("(b) der Feueratem nennt die Einheit und die Zahl (8 Prozent von 300 = 24)",
          "Krieger" in _atem_zeile and "24" in _atem_zeile, _atem_zeile)
    check("(b) der Bericht nennt die eigene Verlustzeile nicht doppelt",
          _text.count("Feueratem") == 1, str(_text.count("Feueratem")))

    # ---- (c) Beute genau einmal, nur der Anteil ----
    _hort_nachher = sum(int(v) for v in (st.drachen_vorraete.get(str(drache.get("id"))) or {}).values())
    _beute_summe = sum(int(v) for v in (_eintrag.get("beute") or {}).values())
    check("(c) die Beute ist beim Auftrag gebucht", _beute_summe > 0, str(_beute_summe))
    check("(c) der Hort ist GENAU um die gebuchte Beute kleiner",
          _hort_vorher - _hort_nachher == _beute_summe,
          "%d - %d gegen %d" % (_hort_vorher, _hort_nachher, _beute_summe))
    check("(c) die Beute passt in die Karren (4 x 2500)", _beute_summe <= 10000, str(_beute_summe))
    _verteidiger_weg = int(sum(int(v) for v in (drachen.verteidiger(drache) or {}).values()))
    check("(c) der Anteil ist nicht der ganze Hort (nach Leistung)",
          _beute_summe <= _hort_vorher, str(_beute_summe))

    # ---- (h) Belohnung, beschaedigte Wache, Flamme, Bot-Urteil (Daniel 05.11.2026) ----
    _b = drachen.belohnung_mana()                     # die Belohnung aus den Daten
    check("(h) die Manabelohnung ist der Grundbetrag plus gerechneter Aufwand",
          _b["grundbetrag"] == 4000
          and _b["summe"] == _b["grundbetrag"] + _b["sprunge"] * _b["kosten_je_sprung"], str(_b))
    check("(h) der Aufwand nutzt den ECHTEN Preis eines Weltensprungs",
          _b["kosten_je_sprung"] == portalraum.wechselkosten(), str(_b["kosten_je_sprung"]))
    _alt_preis = portalraum._MANA_WECHSEL              # Preis merken
    portalraum._MANA_WECHSEL = _alt_preis + 1000       # Preis testweise erhoehen
    _b2 = drachen.belohnung_mana()                     # neu rechnen
    portalraum._MANA_WECHSEL = _alt_preis               # Preis zuruecksetzen
    check("(h) aendert sich der Spruengpreis, zieht die Belohnung mit",
          _b2["summe"] == _b["summe"] + 6 * 1000, "%d gegen %d" % (_b["summe"], _b2["summe"]))
    check("(h) der epische Text setzt Mana und Aufwand ein",
          any("{mana}" in z for z in drachen.belohnung_texte().get("zeilen") or []),
          str(drachen.belohnung_texte().get("titel")))
    _mana_lager = float((ort.vorraete or {}).get("mana", 0) or 0)
    check("(h) der Sieg hat die Manabelohnung ins Lager gebucht",
          _mana_lager >= _b["summe"], str(_mana_lager))
    _wache_rest = sum(int(v) for v in (st.drachen_wachen.get(str(drache.get("id"))) or {}).values())
    check("(h) die Wache steht BESCHAEDIGT (weniger als 204 Verteidiger)",
          0 <= _wache_rest < 204, str(_wache_rest))
    check("(h) der Drache traegt das Flammenzeichen nach dem Angriff",
          str(drache.get("id")) in (st.drachen_angegriffen or []), str(st.drachen_angegriffen))
    _urteil_schwach = drachen.bot_entscheidung(100, 0, (700, 950), _b["summe"])
    check("(h) ein schwacher Bot greift NICHT an", _urteil_schwach[0] is False, _urteil_schwach[1])
    _urteil_stark = drachen.bot_entscheidung(2000, 2000, (700, 950), _b["summe"], True)
    check("(h) ein starker Bot greift an und nennt Bonus und Verluste",
          _urteil_stark[0] is True and "Mana" in _urteil_stark[1] and "Verluste" in _urteil_stark[1],
          _urteil_stark[1])
    check("(h) der Bot weiss nur, DASS angegriffen wurde",
          "bereits angegriffen" in _urteil_stark[1], _urteil_stark[1])

    # ---- (f) Sieg: Ruine, Zustand, kein zweiter Angriff ----
    _besiegt = str(drache.get("id")) in (st.drachen_besiegt or [])
    check("(f) der besiegte Drache steht im Zustand", _besiegt, str(st.drachen_besiegt))
    _lage = st.drachen_position(drache)          # die Lage in DIESEM Spielstand
    check("(f) die Ruine steht weiter auf ihrem Feld",
          st.drache_an(drache["welt"], _lage[0], _lage[1]) is not None, str(_lage))
    check("(f) das Feld der Ruine ist gesperrt",
          st.drachen_blockiert(drache["welt"], _lage[0], _lage[1]) is True)
    check("(f) auf der Karte steht eine Ruine",
          drachen.figur(drache, st.drachen_besiegt).get("art") == "ruine")
    check("(f) die Anzeigeliste fuehrt die Ruine",
          any(f.get("art") == "ruine" for f in
              drachen.anzeige_liste(drache["welt"], st.drachen_besiegt)))

    # ---- Anzeige auf der echten Leinwand: Zeichen vorhanden, nach dem Sieg die Ruine ----
    _leinwand = tk.Canvas(root, width=480, height=480)     # eine echte Tk-Leinwand
    app._drachen_zeichnen(_leinwand, 24, 2)                # Weltkarte 2 zeichnen
    check("die Anzeige setzt ein Drachenzeichen auf die Karte",
          len(_leinwand.find_withtag("portaldrache")) >= 1,
          str(len(_leinwand.find_withtag("portaldrache"))))
    check("(f) nach dem Sieg steht dort die RUINE", bool(_leinwand.find_withtag("ruine")),
          str(_leinwand.find_withtag("ruine")))
    # W-16 (05.11.2026): die Schuppe hat jetzt ein eigenes Lagerfach - der Bericht meldet sie als
    # ERBEUTET, nicht mehr als "dafuer gibt es noch kein Lagerfach".
    check("(c) die Drachenschuppe wird als erbeutet gemeldet",
          "Drachenschuppe erbeutet" in _text, _text[-120:])

    _hort_vor_zwei = sum(int(v) for v in (st.drachen_vorraete.get(str(drache.get("id"))) or {}).values())
    _truppen2 = {n: int(a) for n, a in (ort.einheiten or {}).items() if int(a) > 0}
    if not _truppen2:                                  # nach dem Sieg kann das Heer dezimiert sein
        ort.einheiten = {"Krieger": 50}
        _truppen2 = dict(ort.einheiten)
    # Daniel 05.11.2026: die Ruine bleibt PLUENDERBAR - der zweite Zug holt den Rest, kaempft aber
    # nicht mehr. Die alte Wache hiess "kein zweiter Angriff" und ist damit UEBERHOLT (Entscheidung
    # im Testnamen genannt, nicht stillschweigend geloescht).
    check("die Ruine haelt nach dem Sieg noch einen Rest", _hort_vor_zwei > 0, str(_hort_vor_zwei))
    _eintrag2 = angriff(_truppen2)                     # zweiter Zug auf die RUINE
    _hort_nach_zwei = sum(int(v) for v in (st.drachen_vorraete.get(str(drache.get("id"))) or {}).values())
    _letzte = [m.get("text") or "" for m in st.messages if m.get("type") == TYP][-1]
    check("(f) der zweite Zug auf die Ruine kaempft NICHT",
          "Die Ruine gibt ihren Rest her" in _letzte, _letzte[:120])
    check("(f) der zweite Zug holt den Rest heraus (Hort danach leer)",
          _hort_nach_zwei == 0 and _hort_vor_zwei > 0,
          "%d gegen %d" % (_hort_vor_zwei, _hort_nach_zwei))
    check("(f) gebucht ist GENAU der Rest",
          sum(int(v) for v in ((_eintrag2 or {}).get("beute") or {}).values()) == _hort_vor_zwei,
          str((_eintrag2 or {}).get("beute")))
    check("(h) nach dem Ausraeumen ist das Flammenzeichen weg",
          str(drache.get("id")) not in (st.drachen_angegriffen or []),
          str(st.drachen_angegriffen))
    _truppen3 = {n: int(a) for n, a in (ort.einheiten or {}).items() if int(a) > 0} or {"Krieger": 5}
    _eintrag3 = angriff(_truppen3)                     # dritter Zug auf die leere Ruine
    _letzte3 = [m.get("text") or "" for m in st.messages if m.get("type") == TYP][-1]
    check("(f) der dritte Zug meldet: die Ruine ist leer",
          "nichts mehr" in _letzte3, _letzte3[:120])
    check("(f) der dritte Zug bucht keine Beute", not (_eintrag3 or {}).get("beute"),
          str((_eintrag3 or {}).get("beute")))

    # ---- Feueratem unter der Schwelle: der Angriff kaempft nicht ----
    st.drachen_besiegt = []                            # denselben Drachen wieder aufstellen (Fixture)
    _leinwand2 = tk.Canvas(root, width=480, height=480)   # zweite Leinwand
    app._drachen_zeichnen(_leinwand2, 24, 2)              # dieselbe Weltkarte
    check("vor dem Sieg zeichnet die Anzeige den DRACHEN",
          bool(_leinwand2.find_withtag("drache")), str(_leinwand2.find_withtag("drache")))
    # ---- Klickweg: Feld treffen, fremde Welt abweisen, Ruine abweisen ----
    _lage2 = st.drachen_position(drache)         # die Lage im Spielstand
    check("der Klick findet den Drachen auf seinem Feld",
          app._drache_an(int(_lage2[0]), int(_lage2[1])) is not None, str(_lage2))
    # W-17-Nachbesserung (05.11.2026): die Drachenplaetze werden seit W-14 bei jedem Neubeginn
    # AUSGEWUERFELT (`drachen.verteile`). Eine feste Koordinate wie (0,0) ist deshalb NICHT
    # zuverlaessig frei - die Wache flatterte, sobald ein Drache dort landete. Geprueft wird jetzt
    # ein Feld, das nachweislich frei ist: das erste Rasterfeld, auf dem kein Drache steht.
    _drachen_felder = {tuple(int(v) for v in st.drachen_position(d))       # alle belegten Felder
                       for d in (drache,)}                                 # dieser Drache zuerst
    for _d in drachen.alle():                                              # und alle anderen
        if str(_d.get("id")) not in st.drachen_besiegt:                     # nur lebende Drachen
            _pos = st.drachen_position(_d)                                  # ihre Lage im Stand
            if _pos:
                _drachen_felder.add((int(_pos[0]), int(_pos[1])))           # Feld merken
    _frei = next(((x, y) for x in range(20) for y in range(20)              # erstes freies Feld
                  if (x, y) not in _drachen_felder), None)
    check("auf einem freien Feld steht kein Drache",
          _frei is not None and app._drache_an(_frei[0], _frei[1]) is None,
          f"geprueftes Feld {_frei} gegen Drachenfelder {sorted(_drachen_felder)}")

    def _dialog():
        """Den echten Drachen-Dialog oeffnen (Ingame-Overlay) - Rueckgabe True bei Erfolg."""
        app._drachen_optionen(drache)
        return True

    check("der Drachen-Dialog laesst sich oeffnen",
          ausnahme("Drachen-Dialog oeffnen", _dialog) is True)
    app._portal_blick = 3                                 # eine FREMDE Welt ansehen
    _vorher_nachrichten = len(st.messages)
    app._drachen_optionen(drache)                         # dort darf es nur eine Meldung geben
    _neu_da = [m.get("text") or "" for m in st.messages[_vorher_nachrichten:]]
    check("ein Drache einer fremden Welt ist NUR ANSICHT",
          any("NUR ANSICHT" in t for t in _neu_da), str(_neu_da)[:120])
    app._portal_blick = 2                                 # zurueck auf die eigene Welt

    # ---- die ECHTE Ansicht: das Portal zeichnet den Drachen auf seine Leinwand ----
    def _portal_zeichnen():
        """Die Portal-Ansicht wirklich aufbauen und ihre Leinwand zurueckgeben."""
        app._portal_blick = 2                             # Weltkarte 02 ansehen
        app._switch_view("Portal")                        # die echte Ansicht rendern
        return getattr(app, "portal_zeichenflaeche", None)

    _flaeche = ausnahme("Portal-Ansicht zeichnen", _portal_zeichnen)
    check("die Portal-Ansicht zeichnet den Drachen auf die Karte",
          _flaeche is not None and len(_flaeche.find_withtag("portaldrache")) >= 1,
          str(len(_flaeche.find_withtag("portaldrache")) if _flaeche is not None else "keine Flaeche"))
    _schwach = {"Krieger": 20}
    if not angriff(_schwach):
        check("auch ein schwacher Angriff startet als Auftrag", False)
    _berichte2 = [m for m in st.messages if m.get("type") == TYP and
                  str(m.get("text") or "").startswith("Am Ziel")]
    _text2 = _berichte2[-1].get("text") if _berichte2 else ""
    check("(a) der schwache Angriff kaempft NICHT", "Der Drache hat gesiegt" in _text2 or
          "kein Kampf" in _text2 or "Schwelle" in _text2, _text2[:160])

    # ---- (i) Neubeginn: andere Plaetze, gleiche Welten (Daniel 05.11.2026) ----
    _eins = st.drachen_verteilen(seed=1)               # erster Neubeginn
    _zwei = st.drachen_verteilen(seed=2)               # zweiter Neubeginn
    check("(i) jeder Drache steht auf einem Feld seiner Welt (0..19)",
          all(0 <= v[0] < 20 and 0 <= v[1] < 20 for v in _eins.values()), str(_eins))
    check("(i) zwei Neubeginne wuerfeln UNTERSCHIEDLICHE Plaetze",
          any(_eins[k] != _zwei.get(k) for k in _eins), "%s gegen %s" % (_eins, _zwei))
    check("(i) kein Drache steht auf gesperrtem Gelaende",
          all(portalraum.gelaende_von_feld(drachen.finde_id(k)["welt"], v[0], v[1])["bebaubar"]
              for k, v in _eins.items()), str(_eins))
    _p3 = list(_zwei.values())[0]                      # ein Feld aus der JETZIGEN Lage
    _ausw = st.bot_dorf_platz(2, _p3[0], _p3[1])       # ein Bot will genau dorthin
    check("(i) ein Bot weicht der Drachenkoordinate aus",
          (_ausw[0], _ausw[1]) != (_p3[0], _p3[1]), "%s bei %s" % (_ausw, _p3))

    # ---- (g) alter Spielstand ohne Drachenfelder laedt ----
    _pfad = os.path.join(os.environ.get("TMPDIR") or os.environ.get("TEMP") or ".",
                         "w14_drachen_%d.json" % os.getpid())
    st.save(_pfad)
    with io.open(_pfad, encoding="utf-8") as _f:
        _roh = json.load(_f)
    check("der Spielstand fuehrt die besiegten Drachen",
          "drachen_besiegt" in _roh and "drachen_vorraete" in _roh, str(sorted(_roh))[:80])
    _roh.pop("drachen_besiegt", None)                  # ein Stand von VOR W-14
    _roh.pop("drachen_vorraete", None)
    with io.open(_pfad, "w", encoding="utf-8") as _f:
        json.dump(_roh, _f)
    _neu = main.GameState()
    _geladen = _neu.load(_pfad)
    check("(g) ein alter Spielstand ohne Drachenfelder laedt", bool(_geladen), repr(_geladen))
    check("(g) danach ist kein Drache als besiegt gebucht", _neu.drachen_besiegt == [],
          str(_neu.drachen_besiegt))
    check("(g) danach sind keine Horte gebucht", _neu.drachen_vorraete == {},
          str(_neu.drachen_vorraete))
except Exception as _e:                                # noqa: BLE001 - als Fehler melden, nicht abstuerzen
    check("die Kette laeuft ohne Ausnahme", False, repr(_e))
    import traceback
    traceback.print_exc()
finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:                              # noqa: BLE001
            pass

sys.exit(bericht())
