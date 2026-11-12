"""S4-3-Nachtrag: der Nichtangriffspakt hat einen Spielweg (08.11.2026, Daniels Entscheidung 1).

BEFUND (Uebergabe 07.11.2026, 23:58, Abschnitt 6): `diplomatie.vertrag_anbieten` (S4-3, Ablauf
Schritt 3) hatte in `src/main.py` KEINEN Aufrufer - Pakt, Handelsabkommen und Durchmarsch waren nur
ueber den Kern erreichbar. Die E2E-Kette 11 belegte deshalb den Kernweg und meldete den fehlenden
Spielweg als Befund. Daniel hat am 08.11.2026, 00:25 entschieden: einen kleinen Diplomatie-Block
bauen (Knopf "Pakt anbieten" je Bot), Bauform wie `_ereignis_annehmen`, keine zweite Mechanik.

Geprueft wird:
  A. EINE Pruefstelle: `diplomatie._vertrag_bedingungen` prueft, `vertrag_anbieten` bucht nur bei
     ok, `pakt_anbietbar` fragt dieselbe Funktion fuer die Ansicht. In der Ansicht steht keine
     Grenze und keine Rechnung (F-04-Muster).
  B. Die Ansicht Diplomatie zeigt je Bot einen Knopf "Pakt anbieten", wenn Gunst und Lage es
     zulassen - und KEINEN, wenn die Gunst zu niedrig ist oder Vertraege abgeschaltet sind.
  C. Ein Klick bucht den Pakt (Eintrag am Bot, Satz aus der Datendatei) und sperrt den
     Bot-Angriff (`diplomatie.angriff_gesperrt`).
  D. Ein zweiter Klick bucht NICHT doppelt: Beginn und Gunst bleiben unveraendert, und der Knopf
     ist danach weg.
  E. Die Anzeige veraendert den Spielstand NICHT: ein abgelaufener Pakt wird von `pakt_anbietbar`
     nur gelesen, nicht entfernt (`vertrag_aktiv(..., raeumen=False)`).
  F. Jeder Grund hat seinen Satz in `data/diplomatie.json` - im Code steht keine Spielermeldung.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['diplomatie', 'main:*']
PRUEF_DATEN = ['diplomatie.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect
import os
import random
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

import_src()
import diplomatie as D
import main

SAAT = 4711                                   # feste Saat: der Lauf ist wiederholbar
KNOPF = "Pakt anbieten"                       # der Anzeigetext aus der Ansicht


def _app_neu(saat=SAAT):
    """Eine frische Partie bis zur ersten Siedlung."""
    root = tk.Tk()
    root.withdraw()
    gesammelt = []
    root.report_callback_exception = lambda *a: gesammelt.append(a)
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    random.seed(saat)
    app._erste_siedlung_gruenden()
    return root, app, app.state, gesammelt


def _knoepfe(widget, text):
    """Alle Knoepfe mit genau diesem Anzeigetext (rekursiv durch den Widget-Baum)."""
    treffer = []
    for kind in widget.winfo_children():
        try:
            if kind.winfo_class() == "Button" and str(kind.cget("text")) == text:
                treffer.append(kind)
        except Exception:                                     # Widget schon zerstoert
            continue
        treffer.extend(_knoepfe(kind, text))
    return treffer


def _zahl_der_knoepfe(app):
    """Wie viele "Pakt anbieten"-Knoepfe die Ansicht Diplomatie gerade zeigt."""
    app._switch_view("Diplomatie")
    app.root.update_idletasks()
    return len(_knoepfe(app.content, KNOPF))


def _daten(gunst=50.0, vertraege=None):
    """Die dict-Form eines Bots fuer Kernpruefungen ohne Fenster."""
    return {"gunst": gunst, "vertraege": dict(vertraege or {})}


# ---------------------------------------------------------------------------
abschnitt("A. EINE Pruefstelle - die Ansicht fragt den Kern, sie rechnet nicht selbst")
# ---------------------------------------------------------------------------
quelle_pruef = inspect.getsource(D._vertrag_bedingungen)
check("die Pruefstelle existiert und nennt Schalter, Art, Gunst und laufenden Vertrag",
      all(w in quelle_pruef for w in ("vertraege_aktiv", "VERTRAGSARTEN", "min_gunst",
                                      "vertrag_aktiv")))
check("die Pruefstelle bucht NICHTS (keine Zuweisung in die Vertragstabelle)",
      "_bot_vertraege(bot_daten)[" not in quelle_pruef)
quelle_anbieten = inspect.getsource(D.vertrag_anbieten)
check("vertrag_anbieten fragt die EINE Pruefstelle",
      "_vertrag_bedingungen(" in quelle_anbieten, quelle_anbieten.splitlines()[0].strip())
check("vertrag_anbieten enthaelt keine zweite Gunstgrenze",
      "min_gunst" not in quelle_anbieten)
quelle_pakt = inspect.getsource(D.pakt_anbietbar)
check("pakt_anbietbar fragt dieselbe Pruefstelle (keine zweite Grenze in der Anzeige)",
      "_vertrag_bedingungen(" in quelle_pakt and "min_gunst" not in quelle_pakt)

quelle_render = inspect.getsource(main.NebelseetalApp._render_diplomacy)
check("die Ansicht fragt `diplomatie.pakt_anbietbar`", "pakt_anbietbar(" in quelle_render)
check("in der Ansicht steht KEINE Grenze (weder min_gunst noch die Zahl 40)",
      "min_gunst" not in quelle_render and "40" not in quelle_render)
quelle_klick = inspect.getsource(main.NebelseetalApp._pakt_anbieten)
check("der Knopf bucht ueber den Kern (`diplomatie.vertrag_anbieten`)",
      "diplomatie.vertrag_anbieten(" in quelle_klick)
check("der Knopf schreibt keine Vertragstabelle selbst",
      "vertraege[" not in quelle_klick)
check("der Satz zur Rueckgabe kommt aus der Datendatei",
      "vertrag_grund_text(" in quelle_klick)

# ---------------------------------------------------------------------------
abschnitt("B. Die Ansicht zeigt den Knopf nur, wenn das Angebot moeglich ist")
# ---------------------------------------------------------------------------
root, app, gs, gesammelt = _app_neu()
try:
    bots = list(gs.bots or [])
    check("die Partie hat Bots", len(bots) >= 1, "%d Bots" % len(bots))
    start = D.startwert()
    noetig = int(D.art_daten("nichtangriff").get("min_gunst"))
    check("der Startwert der Gunst liegt ueber der noetigen Gunst (Knopf ist von Anfang an da)",
          float(start) >= noetig, "Start %s, noetig %s" % (start, noetig))
    check("Vertraege sind eingeschaltet", D.vertraege_aktiv() is True)

    anzahl_bots = len(bots)
    check("je Bot genau EIN Knopf \"Pakt anbieten\"", _zahl_der_knoepfe(app) == anzahl_bots,
          "%d Knoepfe fuer %d Bots" % (_zahl_der_knoepfe(app), anzahl_bots))

    # Gunst unter die Grenze: der Knopf verschwindet.
    _alte_gunst = [float(b.gunst) for b in bots]
    for b in bots:
        b.gunst = float(noetig) - 1.0
    check("ohne genug Gunst erscheint KEIN Knopf", _zahl_der_knoepfe(app) == 0,
          "%d Knoepfe" % _zahl_der_knoepfe(app))
    for b, wert in zip(bots, _alte_gunst):
        b.gunst = wert
    check("mit genug Gunst ist der Knopf wieder da", _zahl_der_knoepfe(app) == anzahl_bots,
          "%d Knoepfe" % _zahl_der_knoepfe(app))

    # Schalter aus: kein Knopf, egal wie hoch die Gunst ist.
    _einst = D.daten()
    _kopie = {k: (dict(v) if isinstance(v, dict) else v) for k, v in _einst.items()}
    _kopie["vertraege"] = dict(_kopie.get("vertraege") or {})
    _kopie["vertraege"]["aktiv"] = False
    ok_aus, grund_aus = D.pakt_anbietbar(_daten(), 0.0, _kopie)
    check("Schalter aus: kein Angebot", ok_aus is False and grund_aus == "vertraege_aus",
          str(grund_aus))

    # -----------------------------------------------------------------------
    abschnitt("C. Ein Klick bucht den Pakt und sperrt den Bot-Angriff")
    # -----------------------------------------------------------------------
    ziel = bots[0]
    vorher_gesperrt, _ = D.angriff_gesperrt(gs.bot_als_dict(ziel), gs.spielsekunden)
    check("vor dem Pakt darf der Bot angreifen (keine Sperre)",
          vorher_gesperrt is False, str(vorher_gesperrt))
    _meldungen_vorher = len([m for m in gs.messages if m.get("type") == "diplomatie"])
    knoepfe = _knoepfe(app.content, KNOPF)
    check("der Knopf des ersten Bots ist auffindbar", len(knoepfe) >= 1, str(len(knoepfe)))
    if knoepfe:
        knoepfe[0].invoke()                                   # der echte Weg: Knopf druecken
    app.root.update_idletasks()
    eintrag = dict((ziel.vertraege or {}).get("nichtangriff") or {})
    check("der Pakt steht am Bot", bool(eintrag), str(ziel.vertraege))
    check("der Pakt beginnt bei der jetzigen Spielzeit",
          abs(float(eintrag.get("seit", -1)) - float(gs.spielsekunden)) < 1.0,
          "%s gegen %s" % (eintrag.get("seit"), gs.spielsekunden))
    dauer = float(D.art_daten("nichtangriff").get("dauer_sekunden"))
    check("der Pakt endet nach der Dauer aus der Datendatei",
          abs(float(eintrag.get("bis", 0)) - (float(gs.spielsekunden) + dauer)) < 1.0,
          "%s gegen %s" % (eintrag.get("bis"), float(gs.spielsekunden) + dauer))
    gesperrt, grund_gesperrt = D.angriff_gesperrt(gs.bot_als_dict(ziel), gs.spielsekunden)
    check("der Bot-Angriff ist jetzt gesperrt", gesperrt is True, str(grund_gesperrt))
    check("der Grund ist der Nichtangriffspakt", grund_gesperrt == "nichtangriffspakt",
          str(grund_gesperrt))
    neu = [m.get("text") for m in gs.messages if m.get("type") == "diplomatie"]
    check("genau EINE Meldung kam dazu", len(neu) - _meldungen_vorher == 1,
          str(len(neu) - _meldungen_vorher))
    check("die Meldung ist der Satz aus der Datendatei",
          bool(neu) and neu[-1] == D.vertrag_grund_text("vereinbart"), str(neu[-1:]))
    check("die Ansicht zeigt fuer diesen Bot keinen Knopf mehr",
          _zahl_der_knoepfe(app) == anzahl_bots - 1,
          "%d Knoepfe fuer %d Bots" % (_zahl_der_knoepfe(app), anzahl_bots))

    # -----------------------------------------------------------------------
    abschnitt("D. Ein zweiter Klick bucht NICHT doppelt")
    # -----------------------------------------------------------------------
    gunst_vorher = float(ziel.gunst)
    seit_vorher = float((ziel.vertraege or {}).get("nichtangriff", {}).get("seit", 0.0))
    ok_zweite = app._pakt_anbieten(ziel)                        # der zweite Klick
    check("der zweite Aufruf meldet False", ok_zweite is False, str(ok_zweite))
    eintrag2 = dict((ziel.vertraege or {}).get("nichtangriff") or {})
    check("der Beginn des Pakts ist unveraendert",
          abs(float(eintrag2.get("seit", -1)) - seit_vorher) < 1e-6,
          "%s gegen %s" % (eintrag2.get("seit"), seit_vorher))
    check("die Gunst ist unveraendert", abs(float(ziel.gunst) - gunst_vorher) < 1e-6,
          "%s gegen %s" % (ziel.gunst, gunst_vorher))
    ok_kern, grund_kern = D.vertrag_anbieten(gs.bot_als_dict(ziel), "nichtangriff",
                                             gs.spielsekunden)
    check("auch der Kern selbst lehnt den zweiten Pakt ab",
          ok_kern is False and grund_kern == "laeuft_bereits", str(grund_kern))

    check("keine Ausnahme im Fenster", not gesammelt, str(gesammelt[:1]))
finally:
    try:
        root.destroy()
    except Exception:
        pass

# ---------------------------------------------------------------------------
abschnitt("E. Die Anzeige liest nur - sie raeumt keinen abgelaufenen Pakt weg")
# ---------------------------------------------------------------------------
alt = {"nichtangriff": {"seit": 0.0, "bis": 1.0}}
daten_alt = _daten(vertraege=alt)
ok_alt, grund_alt = D.pakt_anbietbar(daten_alt, 5.0)          # Pakt ist abgelaufen
check("ein abgelaufener Pakt macht den Knopf wieder moeglich", ok_alt is True, str(grund_alt))
check("der abgelaufene Eintrag steht danach NOCH im dict (nichts geschrieben)",
      "nichtangriff" in (daten_alt.get("vertraege") or {}),
      str(daten_alt.get("vertraege")))
daten_alt2 = _daten(vertraege=alt)
D.vertrag_aktiv(daten_alt2, "nichtangriff", 5.0)               # der Kern raeumt auf
check("der Kern selbst raeumt den abgelaufenen Eintrag weg (raeumen=True bleibt die Vorgabe)",
      "nichtangriff" not in (daten_alt2.get("vertraege") or {}),
      str(daten_alt2.get("vertraege")))
daten_alt3 = _daten(vertraege=alt)
D.vertrag_aktiv(daten_alt3, "nichtangriff", 5.0, None, False)  # Anzeigeform
check("mit raeumen=False bleibt der Eintrag liegen",
      "nichtangriff" in (daten_alt3.get("vertraege") or {}),
      str(daten_alt3.get("vertraege")))

# ---------------------------------------------------------------------------
abschnitt("F. Jeder Grund hat seinen Satz in der Datendatei")
# ---------------------------------------------------------------------------
for grund in ("vereinbart", "laeuft_bereits", "gunst_zu_niedrig", "vertraege_aus",
              "art_ohne_daten", "unbekannte_art"):
    check("Satz vorhanden: %s" % grund, bool(D.vertrag_grund_text(grund)),
          D.vertrag_grund_text(grund)[:60])
check("ein unbekannter Grund ergibt einen leeren Satz (nichts erfunden)",
      D.vertrag_grund_text("gibt_es_nicht") == "")

sys.exit(bericht())
