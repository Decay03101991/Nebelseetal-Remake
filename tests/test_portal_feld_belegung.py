# -*- coding: ascii -*-
"""Wache fuer die Belegungskarte des Portalraums (Schnitte S-1 und S-2, 08.11.2026).

Daniels Entscheidung F-26 = A: ein belegtes Feld wird ABGELEHNT, und die Meldung nennt den
Grund (docs/design/PORTAL_MODELL_20261108.md Abschnitt 6). Diese Datei prueft die reine
Funktion `portalraum.feld_status` - sie liest KEINEN Spielstand, hereingereicht werden nur
die belegten Felder - und die Klaerung S-2: `Settlement.welt_x`/`welt_y` traegt die
Portalposition, `x`/`y` bleibt die Siedlungskarte, die Kennung bleibt stabil, und
`GameState._ort_feld` loest "Ort -> Feld" weiter an EINER Stelle auf.

Geprueft werden drei Antworten (frei / belegt / ausserhalb), der Grund im Satz, zwei Orte auf
einem Feld, zwei Welten mit demselben Feld, der Ausschluss des eigenen Dorfes, die feste
Bot-Position aus `bottaktik.dorf_position` und die S-2-Felder samt Rueckfall fuer Altstaende.

Aufruf: python -X utf8 tests/test_portal_feld_belegung.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import bottaktik as B        # noqa: E402
import main as M             # noqa: E402
import portalraum as P       # noqa: E402


def erwarte_valueerror(name, fn):
    """Die Pflicht-Ausnahme selbst pruefen - `harness.ausnahme` zaehlt jede Ausnahme als Fehler."""
    try:
        fn()
    except ValueError:
        check(name, True)
    except Exception as e:                                    # falsche Ausnahme ist auch ein Fehler
        check(name, False, "falsche Ausnahme: %r" % (e,))
    else:
        check(name, False, "es kam gar keine Ausnahme")


class _Ort:
    """Stellvertreter fuer `_ort_feld`: nur die drei Methoden, die die Aufloesung braucht."""

    _feld_im_raster = M.NebelseetalApp._feld_im_raster
    _siedlung_nach_namen = M.NebelseetalApp._siedlung_nach_namen
    _bot_doerfer_im_raster = M.NebelseetalApp._bot_doerfer_im_raster
    _ort_feld = M.NebelseetalApp._ort_feld

    def __init__(self, siedlungen):
        lage = type("Lage", (), {"settlements": siedlungen, "bots": [],
                                 "eigene_dimension": 1})
        self.state = lage()


def main_() -> int:
    # -----------------------------------------------------------------------
    abschnitt("Ohne Belegung ist jedes Feld frei")
    alle_frei = sum(1 for x in range(20) for y in range(20)
                    if P.feld_status(0, x, y).get("frei"))
    check("alle 400 Felder einer Welt sind ohne Belegung frei", alle_frei == 400, str(alle_frei))
    leer = P.feld_status(0, 3, 4)
    check("ein freies Feld meldet 'frei'", leer.get("status") == P.FELD_FREI,
          str(leer.get("status")))
    check("der Grund nennt das Feld und die Weltkarte",
          "3/4" in leer.get("grund", "") and bool(leer.get("weltname")), leer.get("grund", ""))
    check("ein freies Feld hat keinen Belegt-von-Eintrag", leer.get("belegt_von") == [])

    # -----------------------------------------------------------------------
    abschnitt("Ein belegtes Feld wird mit Grund abgelehnt (F-26 = A)")
    eigene = [P.feld_eintrag("siedlung", "Eschenhain", 0, 3, 4)]
    belegt = P.feld_status(0, 3, 4, eigene)
    check("ein belegtes Feld meldet 'belegt'", belegt.get("status") == P.FELD_BELEGT,
          str(belegt.get("status")))
    check("das Feld ist nicht frei", belegt.get("frei") is False)
    check("der Grund nennt den Ort beim Namen", "Eschenhain" in belegt.get("grund", ""),
          belegt.get("grund", ""))
    check("der Eintrag steht in belegt_von", len(belegt.get("belegt_von") or []) == 1)

    fremde = [P.feld_eintrag("botdorf", "Groms Lager", 0, 9, 2)]
    check("auch ein Bot-Dorf belegt sein Feld",
          P.feld_status(0, 9, 2, fremde).get("status") == P.FELD_BELEGT)
    check("das Nachbarfeld desselben Bot-Dorfes bleibt frei",
          P.feld_status(0, 9, 3, fremde).get("frei") is True)

    # -----------------------------------------------------------------------
    abschnitt("Zwei Orte auf einem Feld werden erkannt")
    doppelt = [P.feld_eintrag("siedlung", "Dorf A", 1, 5, 5),
               P.feld_eintrag("botdorf", "Dorf B", 1, 5, 5)]
    st = P.feld_status(1, 5, 5, doppelt)
    check("beide Eintraege stehen in belegt_von", len(st.get("belegt_von") or []) == 2)
    check("beide Namen stehen im Grund",
          "Dorf A" in st.get("grund", "") and "Dorf B" in st.get("grund", ""),
          st.get("grund", ""))
    check("der Grund sagt, dass zwei Orte dort stehen", "2 Orte" in st.get("grund", ""))
    karte = P.belegungs_karte(doppelt)
    check("belegungs_karte behaelt beide Eintraege", len(karte.get((1, 5, 5), [])) == 2)

    # -----------------------------------------------------------------------
    abschnitt("Zwei Welten mit demselben Feld kollidieren NICHT")
    beide = [P.feld_eintrag("siedlung", "Dorf A", 0, 7, 12),
             P.feld_eintrag("siedlung", "Dorf B", 1, 7, 12)]
    a = P.feld_status(0, 7, 12, beide)
    b = P.feld_status(1, 7, 12, beide)
    check("Welt 0 kennt nur ihren eigenen Ort",
          [e["name"] for e in a.get("belegt_von") or []] == ["Dorf A"])
    check("Welt 1 kennt nur ihren eigenen Ort",
          [e["name"] for e in b.get("belegt_von") or []] == ["Dorf B"])
    check("dasselbe Feld auf einer dritten Welt ist frei",
          P.feld_status(2, 7, 12, beide).get("frei") is True)

    # -----------------------------------------------------------------------
    abschnitt("Ausserhalb des Rasters und unbekannte Welt")
    hoch = P.feld_status(0, 20, 0)
    tief = P.feld_status(0, 0, -1)
    check("x = 20 liegt ausserhalb", hoch.get("status") == P.FELD_AUSSERHALB,
          str(hoch.get("status")))
    check("y = -1 liegt ausserhalb", tief.get("status") == P.FELD_AUSSERHALB,
          str(tief.get("status")))
    check("ein Feld ausserhalb ist nicht frei", hoch.get("frei") is False)
    check("der Grund nennt die Feldnummer und die Weltkarte",
          "20/0" in hoch.get("grund", "") and "Weltkarte" in hoch.get("grund", ""),
          hoch.get("grund", ""))
    check("eine unbekannte Weltkarte gilt als ausserhalb",
          P.feld_status(6, 0, 0).get("status") == P.FELD_AUSSERHALB)
    check("ein Randfeld 19/19 ist dagegen gueltig",
          P.feld_status(P.dim_zahl() - 1, 19, 19).get("status") == P.FELD_FREI)

    # -----------------------------------------------------------------------
    abschnitt("Das eigene Dorf blockiert sich nicht selbst")
    eigen = [P.feld_eintrag("siedlung", "Umzieher", 3, 2, 2)]
    check("mit Ausschluss ist das eigene Feld frei",
          P.feld_status(3, 2, 2, eigen, ausschluss="Umzieher").get("frei") is True)
    check("ohne Ausschluss ist dasselbe Feld belegt",
          P.feld_status(3, 2, 2, eigen).get("frei") is False)
    check("ein anderer Name schliesst nichts aus",
          P.feld_status(3, 2, 2, eigen, ausschluss="Fremder").get("frei") is False)
    gemischt = [P.feld_eintrag("siedlung", "Umzieher", 3, 2, 2),
                P.feld_eintrag("botdorf", "Bot", 3, 2, 2)]
    check("ein zweiter Ort auf dem Feld blockiert trotz Ausschluss",
          P.feld_status(3, 2, 2, gemischt, ausschluss="Umzieher").get("frei") is False)

    # -----------------------------------------------------------------------
    abschnitt("Eintraege: ein Feld ausserhalb wird nicht stillschweigend fallen gelassen")
    erwarte_valueerror("feld_eintrag wirft bei x = 20",
                       lambda: P.feld_eintrag("siedlung", "X", 0, 20, 0))
    erwarte_valueerror("feld_eintrag wirft bei y = -1",
                       lambda: P.feld_eintrag("siedlung", "X", 0, 0, -1))
    erwarte_valueerror("feld_eintrag wirft bei unbekannter Welt",
                       lambda: P.feld_eintrag("siedlung", "X", 6, 0, 0))
    gut = P.feld_eintrag("siedlung", "Rand", 5, 19, 19)
    check("feld_eintrag nimmt das Randfeld 19/19 an",
          (gut["welt"], gut["x"], gut["y"], gut["name"]) == (5, 19, 19, "Rand"))

    # -----------------------------------------------------------------------
    abschnitt("Bot-Positionen kommen aus bottaktik.dorf_position")
    bx, by = B.dorf_position("Grom", 1, 20)
    bot_eintrag = P.feld_eintrag("botdorf", "Grom", 0, bx, by)
    check("die feste Bot-Position belegt ihr Feld",
          P.feld_status(0, bx, by, [bot_eintrag]).get("status") == P.FELD_BELEGT)
    check("dieselbe Position kommt immer wieder (kein Zufall aus der Uhr)",
          B.dorf_position("Grom", 1, 20) == (bx, by))
    check("die Bot-Position liegt im 20er-Raster", 0 <= bx < 20 and 0 <= by < 20,
          "%r" % ((bx, by),))

    # -----------------------------------------------------------------------
    abschnitt("S-2: Portalposition im Settlement, Kennung bleibt stabil")
    alt = M.Settlement(name="Altstand", map_id="kontinent", x=3, y=3)
    check("neue Siedlungen sind noch nicht im Portal verortet",
          getattr(alt, "welt_x", "fehlt") is None and getattr(alt, "welt_y", "fehlt") is None)
    neu = M.Settlement(name="Neu", map_id="kontinent", x=3, y=3,
                       id=M.siedlung_kennung("spieler", "kontinent", 3, 3),
                       welt_x=7, welt_y=12)
    app = _Ort([neu, alt])
    check("_ort_feld liest die Portalposition", app._ort_feld("Neu", "", 20) == (7, 12),
          str(app._ort_feld("Neu", "", 20)))
    check("_ort_feld faellt fuer alte Staende auf x/y zurueck",
          app._ort_feld("Altstand", "", 20) == (3, 3),
          str(app._ort_feld("Altstand", "", 20)))
    check("die Kennung haengt nicht an der Portalposition", neu.id == "spieler:kontinent:3:3",
          neu.id)
    weit = M.Settlement(name="Weit", map_id="kontinent", x=3, y=3, welt_x=25, welt_y=3)
    app2 = _Ort([weit])
    check("eine Portalposition ausserhalb des Rasters wird NICHT durch x/y ersetzt",
          app2._ort_feld("Weit", "", 20) is None, str(app2._ort_feld("Weit", "", 20)))
    check("ein unbekannter Ortsname bleibt unaufloesbar",
          app._ort_feld("Gibt es nicht", "", 20) is None)

    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
