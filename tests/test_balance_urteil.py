"""B-2 Regelkreis und A/B-Urteil (Ablauf Schritt 9, 07.11.2026): Pruefungen des Werkzeugs.

Geprueft wird, was der Schnitt zusagt (die fuenf Wachen aus dem Ablauf, A bis E, plus Belege):
  A. Zwei IDENTISCHE Messungen ergeben NICHT angenommen (keine Verbesserung = kein Urteil).
  B. Ziel 50 Prozent besser, aber eine andere Groesse verlaesst den Korridor: abgelehnt
     MIT NENNUNG der Groesse.
  C. Ungleiche Startwert-Reihenfolge ist ein Fehler, keine stille Rechnung.
  D. `tag_erstes_gefecht = null` wird uebergangen, nicht als Tag 0 gezaehlt.
  E. Zwei gleiche Meldungen ergeben ein Buendel mit Zaehler 2; ab drei: Messauftrag.
  F. Die drei Schwellen kommen aus `data/regelkreis.json` (Datei geaendert = Urteil geaendert).
  G. BELEGT-Werte werden nie vorgeschlagen, Schrittweite bleibt unter 10 Prozent.
  H. Der A/B-Lauf schreibt NICHTS in `data/` (Hash vorher/nachher) und laeuft deterministisch.
  I. Die Urteilsdatei wird fortlaufend nummeriert und nie ueberschrieben.

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['punkte']
PRUEF_DATEN = ['baupreise.json', 'regelkreis.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import hashlib
import io
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HIER, "tools"))
import balance_kreis as BK  # noqa: E402

REGELKREIS = BK.lade_regelkreis(HIER)


# ------------------------------------------------------------------ Hilfen
def _mess(saaten, punkte_ende, rohstoff, tage=10, gefecht=None, stil="breit"):
    """Eine Messung im Format von `BK.messung` - ohne Spiel, damit das Urteil pruefbar ist."""
    laeufe = []
    for nummer, saat in enumerate(saaten):
        wert = float(rohstoff[nummer]) if isinstance(rohstoff, (list, tuple)) else float(rohstoff)
        tage_liste = [{"tag": tag,
                       "ressourcen": {"holz": wert, "stein": wert, "nahrung": wert, "gold": wert},
                       "punkte": 0} for tag in range(int(tage) + 1)]
        laeufe.append({"saat": int(saat), "tage": tage_liste,
                       "tag_erstes_gefecht": gefecht[nummer] if gefecht else None,
                       "punkte_ende": float(punkte_ende[nummer]), "uebersprungen": 0})
    return {"saaten": [int(s) for s in saaten], "tage": float(tage), "stil": stil, "laeufe": laeufe}


def _kurve(unten, oben, tage=10, ziel=3.3):
    """Eine Sollkurve im Format von `BK.sollkurve` - konstantes Band, damit die Lage klar ist."""
    zeilen = []
    for tag in range(int(tage) + 1):
        zeile = {"tag": tag, "siedler": 10, "gebaeude": 1}
        for groesse in ("holz", "stein", "nahrung", "gold"):
            zeile[groesse] = {"ideal": 100.0, "unten": float(unten), "oben": float(oben)}
        zeilen.append(zeile)
    return {"tage": zeilen, "punkte_ziel_je_spieltag": {"wert": float(ziel)},
            "korridorgroessen": ["holz", "stein", "nahrung", "gold"],
            "baender": {"unten": 0.7, "oben": 1.1}}


def _hash_data():
    """SHA256 ueber alle Dateien in data/ - belegt, ob der A/B-Lauf etwas geschrieben hat."""
    summe = hashlib.sha256()
    for name in sorted(os.listdir(os.path.join(HIER, "data"))):
        pfad = os.path.join(HIER, "data", name)
        if os.path.isfile(pfad):
            with open(pfad, "rb") as f:
                summe.update(name.encode("utf-8"))
                summe.update(f.read())
    return summe.hexdigest()


# ------------------------------------------------------------------ A. identische Listen
abschnitt("A. Zwei identische Messungen ergeben NICHT angenommen")
_kurve_a = _kurve(70, 110, tage=10)
_mess_a = _mess([1, 2, 3], [33.0, 33.0, 33.0], 100.0, tage=10, gefecht=[3.0, 3.0, 3.0])
_urteil_a = BK.urteil({"vorher": _mess_a, "nachher": _mess_a, "vorschlag": {"status": "keiner"}},
                      _kurve_a, REGELKREIS)
check("identische Messungen werden abgelehnt", _urteil_a["angenommen"] is False,
      "angenommen=%s" % _urteil_a["angenommen"])
check("der Grund nennt das Ziel",
      any("Ziel" in str(g) for g in _urteil_a["gruende"]), str(_urteil_a["gruende"]))
check("das Ziel ist bei 33 Punkten auf 10 Tage genau erreicht (3,3 je Tag)",
      abs(float(_urteil_a["ziel_vorher"]["ist"]) - 3.3) < 0.011,
      str(_urteil_a["ziel_vorher"]["ist"]))

# ------------------------------------------------------------------ B. Ziel besser, andere Groesse schlechter
abschnitt("B. Ziel besser, aber Holz verlaesst den Korridor - abgelehnt MIT NENNUNG")
_vor_b = _mess([1, 2, 3], [20.0, 20.0, 20.0], 100.0, tage=10, gefecht=[3.0, 3.0, 3.0])
_nach_b = _mess([1, 2, 3], [31.0, 31.0, 31.0], 500.0, tage=10, gefecht=[3.0, 3.0, 3.0])
_urteil_b = BK.urteil({"vorher": _vor_b, "nachher": _nach_b, "vorschlag": {"status": "vorschlag"}},
                      _kurve_a, REGELKREIS)
check("das Ziel ist deutlich besser (2,0 -> 3,1 Punkte je Tag)", _urteil_b["ziel_ok"] is True,
      "%s -> %s Prozent" % (_urteil_b["ziel_vorher"]["abweichung_prozent"],
                            _urteil_b["ziel_nachher"]["abweichung_prozent"]))
check("das Urteil ist trotzdem Ablehnung", _urteil_b["angenommen"] is False,
      "angenommen=%s" % _urteil_b["angenommen"])
check("die Ablehnung nennt die Groesse beim Namen",
      any("holz" in str(g) for g in _urteil_b["gruende"]), str(_urteil_b["gruende"]))
check("Holz gilt vorher als im Korridor und nachher nicht",
      _urteil_b["korridore"]["holz"]["war_im_korridor"] is True
      and _urteil_b["korridore"]["holz"]["ist_im_korridor"] is False,
      str(_urteil_b["korridore"]["holz"]))

# ------------------------------------------------------------------ C. Startwert-Reihenfolge
abschnitt("C. Ungleiche Startwert-Reihenfolge ist ein Fehler")
try:
    BK.urteil({"vorher": _mess([1, 2, 3], [33.0] * 3, 100.0),
               "nachher": _mess([2, 1, 3], [40.0] * 3, 100.0)}, _kurve_a, REGELKREIS)
    _geworfen = False
except ValueError as fehler:
    _geworfen = "Startwerte" in str(fehler)
check("ValueError mit dem Wort Startwerte", _geworfen, "Reihenfolge 1,2,3 gegen 2,1,3")
try:
    BK.urteil({"vorher": _mess([1, 2], [33.0] * 2, 100.0, tage=10),
               "nachher": _mess([1, 2], [33.0] * 2, 100.0, tage=12)}, _kurve_a, REGELKREIS)
    _geworfen2 = False
except ValueError:
    _geworfen2 = True
check("verschiedene Laengen sind ebenfalls ein Fehler", _geworfen2, "10 gegen 12 Spieltage")

# ------------------------------------------------------------------ D. null beim ersten Gefecht
abschnitt("D. tag_erstes_gefecht = null wird uebergangen, nicht als 0 gezaehlt")
check("ein null faellt aus dem Mittel heraus (4,0 bleibt 4,0)",
      BK._gefecht_mittel({"laeufe": [{"tag_erstes_gefecht": None},
                                     {"tag_erstes_gefecht": 4.0}]}) == 4.0,
      str(BK._gefecht_mittel({"laeufe": [{"tag_erstes_gefecht": None},
                                         {"tag_erstes_gefecht": 4.0}]})))
check("nur null ergibt None, nicht 0",
      BK._gefecht_mittel({"laeufe": [{"tag_erstes_gefecht": None}]}) is None,
      str(BK._gefecht_mittel({"laeufe": [{"tag_erstes_gefecht": None}]})))
_urteil_d = BK.urteil({"vorher": _mess([1, 2], [31.0, 31.0], 100.0, gefecht=[None, 4.0]),
                       "nachher": _mess([1, 2], [33.0, 33.0], 100.0, gefecht=[4.0, None])},
                      _kurve_a, REGELKREIS)
check("gleiches Gefecht trotz null auf beiden Seiten: kein Verstoss", _urteil_d["gefecht_ok"] is True,
      "%s gegen %s" % (_urteil_d["gefecht_vorher"], _urteil_d["gefecht_nachher"]))
_urteil_d2 = BK.urteil({"vorher": _mess([1, 2], [20.0, 20.0], 100.0, gefecht=[None, 4.0]),
                        "nachher": _mess([1, 2], [31.0, 31.0], 100.0, gefecht=[None, 5.0])},
                       _kurve_a, REGELKREIS)
check("ein spaeteres Gefecht wird erkannt und abgelehnt", _urteil_d2["gefecht_ok"] is False
      and any("Gefecht" in str(g) for g in _urteil_d2["gruende"]),
      "%s gegen %s" % (_urteil_d2["gefecht_vorher"], _urteil_d2["gefecht_nachher"]))

# ------------------------------------------------------------------ E. Buendel der Meldungen
abschnitt("E. Zwei gleiche Meldungen ergeben ein Buendel mit Zaehler 2")
_meldungen = [{"was": "Holz am Anfang", "wann": "Tag 2", "stand": "ef57bf1", "zahl": "12", "gefuehl": 2},
              {"was": " holz am anfang ", "wann": "Tag 3", "stand": "ef57bf1", "zahl": "8", "gefuehl": 4}]
_buendel = BK.buendeln(_meldungen, 3)
check("es entsteht genau ein Buendel", len(_buendel) == 1, str(len(_buendel)))
check("der Zaehler steht auf 2", _buendel[0]["zaehler"] == 2, str(_buendel[0]["zaehler"]))
check("das Gefuehl wird gemittelt (2 und 4 ergibt 3,0)", _buendel[0]["gefuehl_schnitt"] == 3.0,
      str(_buendel[0]["gefuehl_schnitt"]))
check("zwei Meldungen sind noch KEIN Messauftrag", _buendel[0]["messauftrag"] is False,
      str(_buendel[0]["messauftrag"]))
_drei = BK.buendeln(_meldungen + [{"was": "Holz am Anfang", "gefuehl": 3}], 3)
check("drei gleiche Meldungen ergeben einen Messauftrag", _drei[0]["messauftrag"] is True,
      "Zaehler %s" % _drei[0]["zaehler"])

# ------------------------------------------------------------------ F. Schwellen aus der Datei
abschnitt("F. Die drei Schwellen kommen aus data/regelkreis.json")
check("data/regelkreis.json liegt im Projekt",
      os.path.isfile(os.path.join(HIER, "data", "regelkreis.json")), "data/regelkreis.json")
check("20 Prozent Verbesserung stehen in der Datei",
      float(REGELKREIS["schwellen"]["verbesserung_prozent"]) == 20.0,
      str(REGELKREIS["schwellen"]["verbesserung_prozent"]))
check("10 Prozent Schrittweite stehen in der Datei",
      float(REGELKREIS["schwellen"]["schrittweite_prozent"]) == 10.0,
      str(REGELKREIS["schwellen"]["schrittweite_prozent"]))
check("3 Meldungen je Buendel stehen in der Datei",
      int(REGELKREIS["schwellen"]["meldungen_je_buendel"]) == 3,
      str(REGELKREIS["schwellen"]["meldungen_je_buendel"]))
check("die Quelle nennt F-17", "F-17" in str(REGELKREIS.get("_quelle")),
      str(REGELKREIS.get("_quelle"))[:60])
_tmpf = tempfile.mkdtemp(prefix="regelkreis_datei_")
try:
    shutil.copytree(os.path.join(HIER, "data"), os.path.join(_tmpf, "data"))
    _pfad = os.path.join(_tmpf, "data", "regelkreis.json")
    with io.open(_pfad, encoding="utf-8") as f:
        _datei = json.load(f)
    _datei["schwellen"]["verbesserung_prozent"] = 5
    with io.open(_pfad, "w", encoding="utf-8", newline="\n") as f:
        json.dump(_datei, f, ensure_ascii=False, indent=2)
    _streng = BK.lade_regelkreis(_tmpf)
    check("eine geaenderte Datei ergibt eine geaenderte Schwelle",
          float(_streng["schwellen"]["verbesserung_prozent"]) == 5.0,
          str(_streng["schwellen"]["verbesserung_prozent"]))
    _urteil_f = BK.urteil({"vorher": _mess([1, 2, 3], [20.0] * 3, 100.0),
                           "nachher": _mess([1, 2, 3], [31.0] * 3, 100.0)}, _kurve_a, _streng)
    check("mit 5 Prozent Schwelle wird dasselbe A/B angenommen (20 haette abgelehnt)",
          _urteil_f["angenommen"] is True and _urteil_f["ziel_ok"] is True,
          str(_urteil_f["gruende"]))
finally:
    shutil.rmtree(_tmpf, ignore_errors=True)

# ------------------------------------------------------------------ G. Vorschlag
abschnitt("G. BELEGT wird nie vorgeschlagen, Schrittweite bleibt unter 10 Prozent")
_kandidaten = BK._preis_kandidaten(HIER)
_belegte = ("holzfaeller", "steinmetz", "jaeger", "haus")
check("kein BELEGTES Gebaeude ist Kandidat",
      not any(k["gebaeude"] in _belegte for k in _kandidaten),
      str(sorted({k["gebaeude"] for k in _kandidaten})[:5]))
_lage_g = _mess([1, 2], [33.0] * 2, 10.0, tage=10)          # Holz 10 liegt unter 70
_vorschlag_g = BK.vorschlag(_lage_g, _kurve_a, REGELKREIS, HIER)
check("es gibt einen Vorschlag", _vorschlag_g["status"] == "vorschlag", str(_vorschlag_g))
if _vorschlag_g["status"] == "vorschlag":
    check("hoechstens 10 Prozent Schrittweite",
          float(_vorschlag_g["schrittweite_prozent"]) <= 10.0,
          "%s Prozent" % _vorschlag_g["schrittweite_prozent"])
    check("der Vorschlag betrifft genau EIN Feld",
          isinstance(_vorschlag_g.get("feld"), str) and _vorschlag_g.get("gebaeude") not in _belegte,
          "%s/%s" % (_vorschlag_g.get("gebaeude"), _vorschlag_g.get("feld")))
    check("zu wenig Rohstoff senkt den Preis", _vorschlag_g["richtung"] == "senken"
          and float(_vorschlag_g["neu"]) < float(_vorschlag_g["alt"]),
          "%s -> %s" % (_vorschlag_g["alt"], _vorschlag_g["neu"]))
    check("die Richtung passt zur Lage (Holz zu wenig)",
          _vorschlag_g["groesse"] == "holz", _vorschlag_g["groesse"])
_lage_ok = _mess([1, 2], [33.0] * 2, 100.0, tage=10)        # alles im Korridor
check("im Korridor gibt es keinen Vorschlag",
      BK.vorschlag(_lage_ok, _kurve_a, REGELKREIS, HIER)["status"] == "keiner",
      BK.vorschlag(_lage_ok, _kurve_a, REGELKREIS, HIER).get("grund"))

# ------------------------------------------------------------------ H. A/B schreibt nichts
abschnitt("H. Der A/B-Lauf schreibt nichts in data/ und ist deterministisch")
_hash_vorher = _hash_data()
_mess1 = BK.messung(HIER, REGELKREIS, saaten=[1], tage=2)
_mess2 = BK.messung(HIER, REGELKREIS, saaten=[1], tage=2)
check("zwei Messlaeufe mit demselben Startwert sind gleich", _mess1 == _mess2,
      "Saaten %s" % _mess1["saaten"])
check("die Messung hat Tagesstaende", len((_mess1["laeufe"][0]["tage"])) >= 2,
      str(len(_mess1["laeufe"][0]["tage"])))
_lauf_h = BK.ab(HIER, _vorschlag_g, REGELKREIS, saaten=[1], tage=2)
check("der A/B-Lauf liefert beide Seiten",
      bool(_lauf_h["vorher"]["laeufe"]) and bool(_lauf_h["nachher"]["laeufe"]), "vorher und nachher")
check("die Startwerte sind auf beiden Seiten gleich",
      _lauf_h["vorher"]["saaten"] == _lauf_h["nachher"]["saaten"], str(_lauf_h["vorher"]["saaten"]))
check("data/ ist nach dem A/B unveraendert (gleicher Hash)", _hash_data() == _hash_vorher,
      "Hash verglichen")
with io.open(os.path.join(HIER, "data", "baupreise.json"), encoding="utf-8") as _f:
    _preise_jetzt = json.load(_f).get("preise") or {}
_alt_jetzt = ((_preise_jetzt.get(str(_vorschlag_g.get("gebaeude"))) or {})
              .get(str(_vorschlag_g.get("feld"))))
check("der Projektwert steht nach dem Lauf noch auf dem alten Wert",
      _alt_jetzt == _vorschlag_g.get("alt"),
      "%s/%s steht auf %s" % (_vorschlag_g.get("gebaeude"), _vorschlag_g.get("feld"), _alt_jetzt))
_bewertung_h = BK.urteil(_lauf_h, _kurve_a, REGELKREIS)
check("das Urteil ueber den Mini-Lauf ist ein dict mit Begruendung",
      isinstance(_bewertung_h.get("gruende"), list), str(_bewertung_h["gruende"])[:80])

# ------------------------------------------------------------------ I. Urteilsdatei
abschnitt("I. Die Urteilsdatei wird fortlaufend nummeriert")
_nummer_vorher = BK.naechste_urteil_nummer(HIER)
check("die naechste Nummer ist eine ganze Zahl groesser 0", isinstance(_nummer_vorher, int)
      and _nummer_vorher >= 1, str(_nummer_vorher))
_tmpo = tempfile.mkdtemp(prefix="regelkreis_urteil_")
try:
    os.makedirs(os.path.join(_tmpo, "docs", "balancing"))
    for _n in (1, 2, 7):
        open(os.path.join(_tmpo, "docs", "balancing", "URTEIL_%d.md" % _n), "w").close()
    check("nach 1, 2 und 7 kommt 8", BK.naechste_urteil_nummer(_tmpo) == 8,
          str(BK.naechste_urteil_nummer(_tmpo)))
    _pfad_i = BK.urteil_schreiben(_tmpo, _lauf_h, _bewertung_h, _kurve_a, REGELKREIS)
    check("die geschriebene Datei ist URTEIL_8.md", os.path.basename(_pfad_i) == "URTEIL_8.md",
          os.path.basename(_pfad_i))
    _text_i = io.open(_pfad_i, encoding="utf-8").read()
    check("die Datei nennt das Urteil", "ANGENOMMEN" in _text_i or "ABGELEHNT" in _text_i,
          _text_i.splitlines()[0] if _text_i else "leer")
    check("die Datei sagt, dass nichts uebernommen wurde", "Nichts wurde uebernommen" in _text_i,
          "Schlussabsatz vorhanden")
finally:
    shutil.rmtree(_tmpo, ignore_errors=True)

bericht()
