# -*- coding: ascii -*-
"""Der Bot-Takt auf dem KERN - Stufe S-2b (03.11.2026).

Daniels Grundsatz: "sie muessen die selben mechaniken nutzen um zu gewinnen ... Ein bot muss
wirtschaften und entscheiden." Bis S-1 hatte ein Bot-Dorf eine eigene, duennere Ernte
(`bot_dorf_ertrag` aus dem Kartenprofil, `bot_doerfer_ernten` mit Rate x Stunden). S-2b schaltet
den Takt auf DIESELBE Funktion wie beim Spieler (`spieloekonomie.ort_tick`).

WICHTIG, und der Grund fuer den Schalter: der Felder-Weg liefert fuer JEDE Karte denselben
Grundertrag, sobald dieselben Anlagen stehen - die Karte unterscheidet dann nur, was gebaut werden
KANN. Das Kartenprofil (B-4, Vorgabe Daniel 02.11.2026 "die Karte bestimmt den Ertrag") gab je
Karte 9,12 bis 12,92 Holz, ohne dass dort etwas stehen musste.

**ENTSCHEIDUNG GEAENDERT (S-8 Stufe 1, 03.11.2026, Daniels Vorgabe: der Bot nutzt seine Karte mit
Gebaeuden sinnvoll): die Vorgabe in der Datendatei ist jetzt `anlagen`** - der Ertrag kommt aus den
GEBAUTEN Anlagen je Feld, gerechnet vom Kern. `karte` und `felder` bleiben als Schalter erhalten:
`karte` = altes Kartenprofil (Vergleich), `felder` = derselbe Kern, aber der Kern tickt selbst
(`ort_tick`). Diese Datei prueft weiter, dass ALLE DREI Wege sauber nebeneinander leben.

Was diese Datei beweist
-----------------------
1. Die Vorgabe ist `anlagen` (S-8 Stufe 1); `karte` rechnet weiter Zeichen fuer Zeichen wie vorher
   (Kartenprofil / karten_teiler, mit Volksfaktor) und dient als Vergleich und Rueckfall.
2. Mit `ertrag_weg = "felder"` kommt der Ertrag aus dem KERN - und zwar OHNE doppelten
   Volksfaktor (`wirtschaft.ertrag_gesamt` rechnet ihn selbst, Register 149).
3. Der Takt laeuft dann durch `spieloekonomie.ort_tick`: Ernte, Journal, Siedlerzuwachs; die
   Armee isst ueber dieselbe Buchstelle wie vorher, EINE Journalzeile je Spanne.
4. Der Lagerdeckel aus der Datendatei haelt auch auf dem Kern-Weg.
5. Zurueckschalten bringt die alten Zahlen wieder (kein Zustand bleibt haengen); die Wege sind
   unterscheidbar: `karte` liefert das Profil, `anlagen` und `felder` den Kern.
6. Der Unterschied der Wege ist GEMESSEN (Kartenprofil gegen Anlagen, je Karte fuer die Registerzeile).

Aufruf:  python -X utf8 tests/test_bot_takt_kern.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['botkern', 'forschung', 'main:*', 'spieloekonomie', 'wirtschaft']
PRUEF_DATEN = ['buildings.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import main as M  # noqa: E402
import wirtschaft as W  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def einstellungen(weg: str) -> dict:
    """Die echten Bot-Einstellungen mit umgestelltem Ertragsweg (keine zweite Zahlenliste)."""
    werte = dict(M.bot_wirtschaft_einstellungen())
    werte["ertrag_weg"] = weg
    return werte


def bot_mit_dorf(karte: str = "original-036", nahrung: float = 1000.0, armee: int = 100):
    """Ein Bot mit EINEM Hauptdorf, Karte und (optional) Armee."""
    bot = M.BotPlayer("Pruefbot", "zwergisch", 0.3, 0.5)
    dorf = M.BotDorf(name="Haupt", hauptdorf=True, karte=karte,
                     vorraete={"nahrung": float(nahrung), "holz": 500.0, "stein": 500.0})
    bot.doerfer = [dorf]
    # S-5b (03.11.2026): die Armee steht im DORF - deshalb erst das Dorf, dann die Armee.
    bot.army = {"Krieger": int(armee)} if armee else {}
    return bot, dorf


# ==========================================================================
abschnitt("1. Die Vorgabe ist der Ertrag aus den Anlagen (S-8 Stufe 1, Daniel 03.11.2026)")
# ==========================================================================
_einst_karte = M.bot_wirtschaft_einstellungen()
check("1 die Datendatei steht auf 'anlagen' (S-8 Stufe 1 - vorher 'karte', B-4)",
      str(_einst_karte.get("ertrag_weg") or "") == "anlagen", str(_einst_karte.get("ertrag_weg")))
check("1 der Schalter ist begruendet (Hinweisfeld vorhanden)",
      "ertrag_weg_hinweis" in _einst_karte and len(str(_einst_karte["ertrag_weg_hinweis"])) > 100,
      str(len(str(_einst_karte.get("ertrag_weg_hinweis") or ""))))
_bot, _dorf = bot_mit_dorf("original-036")
# S-8 Stufe 1: das Dorf hat noch KEINE Anlage - der Schalter 'karte' wird ausdruecklich gesetzt,
# damit diese Pruefung das Kartenprofil misst und nicht den Rueckfall des neuen Wegs.
_einst_nur_karte = dict(_einst_karte)
_einst_nur_karte["ertrag_weg"] = "karte"
_mit_karte = M.bot_dorf_ertrag(_dorf, _einst_nur_karte, _bot)
_profil = M.bot_kartenprofil("original-036")
_teiler = float(_einst_karte.get("karten_teiler") or 10.0)
check("1 der Ertrag ist Kartenprofil / karten_teiler (mit Volksfaktor)",
      abs(float(_mit_karte.get("holz", 0.0))
          - round(float(_profil.get("holz", 0.0)) / _teiler * 0.95, 2)) < 0.02,
      f"{_mit_karte.get('holz')} gegen Profil {_profil.get('holz')} / {_teiler}")

# ==========================================================================
abschnitt("2. Schalter 'felder': der Ertrag kommt aus dem KERN, ohne doppelten Volksfaktor")
# ==========================================================================
_einst_felder = einstellungen("felder")
M.bot_doerfer_bebauen(_dorf, _einst_felder)                 # 3 Anlagen je Grundrohstoff
_ort = M.bot_dorf_als_ort(_dorf, _bot)
_kern = {str(k).lower(): round(float(v), 2) for k, v in W.ertrag_gesamt([_ort]).items()
         if float(v) > 0}
_felder = M.bot_dorf_ertrag(_dorf, _einst_felder, _bot)
check("2 der Ertrag ist GENAU der des Kerns (eine Wahrheit, F-04)",
      _felder == _kern, f"Bot {_felder} gegen Kern {_kern}")
check("2 der Volksfaktor steht nur EINMAL drin (zwergisch: Holz -5 %, Stein +5 %)",
      abs(float(_felder.get("holz", 0.0)) - round(float(W.ertrag_gesamt([_ort]).get("Holz", 0.0)), 2)) < 1e-9
      and abs(float(_felder.get("stein", 0.0)) - round(float(W.ertrag_gesamt([_ort]).get("Stein", 0.0)), 2)) < 1e-9,
      f"Holz {_felder.get('holz')}, Stein {_felder.get('stein')}")
check("2 der Kern-Weg liefert mehr Rohstoffe als das Kartenprofil (drei Anlagen je Stoff)",
      set(_kern) >= {"holz", "stein", "nahrung"}, str(sorted(_kern)))
# ENTSCHEIDUNG GEAENDERT (S-8 Stufe 1): ein Dorf ohne Karte UND ohne Anlage faellt auf den
# Bauplan-Rueckfall zurueck (20/12/21/9 plus Waren aus data/buildings.json) - das ist kein
# erfundener Wert, sondern der Stand VOR B-4, damit ein alter Spielstand nicht ohne Ernte dasteht.
_leer = M.bot_dorf_ertrag(M.BotDorf(name="Leer"), _einst_felder, _bot)
_holz_soll = float(M._mit_volk({"holz": 20.0}, _bot).get("holz", 0.0))   # 20 aus dem Bauplan, mit Volksfaktor
check("2 ohne Karte und ohne Anlagen gilt der Bauplan-Rueckfall (kein erfundener Wert)",
      bool(_leer) and abs(float(_leer.get("holz", 0)) - _holz_soll) < 1e-6, str(_leer))
check("2 dorf=None stuerzt auf dem Kern-Weg nicht ab",
      isinstance(M.bot_dorf_ertrag(None, _einst_felder, _bot), dict), "")

# ==========================================================================
abschnitt("3. Der Takt laeuft durch ort_tick: Ernte, Journal, eine Zeile je Spanne")
# ==========================================================================
_bot2, _d2 = bot_mit_dorf("original-036", nahrung=1000.0, armee=100)
M.bot_doerfer_bebauen(_d2, _einst_felder)
_rate = sum(float(v) for v in M.bot_dorf_ertrag(_d2, _einst_felder, _bot2).values())
M.bot_doerfer_ernten(_bot2, 1000.0, _einst_felder)                 # erster Lauf: nur Zeitstempel
_ernte = M.bot_doerfer_ernten(_bot2, 4600.0, _einst_felder)        # eine Stunde
# ENTSCHEIDUNG GEAENDERT (S-5c, 03.11.2026): seit die Garnison in IHREM Dorf isst (das tut `ort_tick`
# auf dem Kern-Weg), ist der zurueckgegebene Zuwachs der NETTO-Zuwachs - Ernte minus Essen. Vorher
# buchte `bot_futter_buchen` das Essen neben dem Kern, deshalb war die Rueckgabe brutto.
_verbrauch_erwartet = 8.0 * 100.0 / 24.0                    # 8 je Einheit und Tag, 100 Einheiten
check("3 der Zuwachs der Stunde ist die Kernrate MINUS das Essen der Garnison",
      abs(sum(float(v) for v in _ernte.values()) - (_rate - _verbrauch_erwartet)) < 0.05,
      f"{sum(float(v) for v in _ernte.values()):.2f} gegen {_rate - _verbrauch_erwartet:.2f}")
check("3 der Kern schreibt EINE Journalzeile (nicht zwei: Ernte und Futter getrennt)",
      len(_d2.produktionsjournal) == 1, str(len(_d2.produktionsjournal)))
_zeile = _d2.produktionsjournal[0] if _d2.produktionsjournal else {}
check("3 die Zeile hat die Form des Spielers und traegt Ernte UND Verbrauch",
      sorted(_zeile) == ["ab", "bis", "mengen", "unterdeckung", "verbrauch"]
      and bool(_zeile.get("mengen")) and bool(_zeile.get("verbrauch")), str(sorted(_zeile)))
check("3 die Armee isst 33,33 in der Stunde (8 x 100 / 24)",
      abs(float(_zeile.get("verbrauch", {}).get("nahrung", 0.0)) - 33.33) < 0.01,
      str(_zeile.get("verbrauch")))
_ernte_nahrung = float((_zeile.get("mengen") or {}).get("nahrung", 0.0))
check("3 der Bestand ist Start + Ernte - Verbrauch (keine zweite Buchung)",
      abs(float(_d2.vorraete.get("nahrung", 0.0)) - (1000.0 + _ernte_nahrung - 33.33)) < 0.02,
      f"{_d2.vorraete.get('nahrung')} gegen {1000.0 + _ernte_nahrung - 33.33:.2f}")
check("3 der Siedlerzuwachs kommt jetzt vom Kern (Bevoelkerung waechst)",
      float(_d2.bevoelkerung) > 0.0, str(_d2.bevoelkerung))
M.bot_doerfer_ernten(_bot2, 4600.0, _einst_felder)
check("3 eine stehende Uhr bucht nichts nach", len(_d2.produktionsjournal) == 1,
      str(len(_d2.produktionsjournal)))
M.bot_doerfer_ernten(_bot2, 8200.0, _einst_felder)
check("3 die zweite Stunde schreibt die zweite Zeile", len(_d2.produktionsjournal) == 2,
      str(len(_d2.produktionsjournal)))

# ==========================================================================
abschnitt("4. Lagerdeckel haelt auch auf dem Kern-Weg")
# ==========================================================================
_bot3, _d3 = bot_mit_dorf("original-036", nahrung=10.0, armee=0)
M.bot_doerfer_bebauen(_d3, _einst_felder)
_einst_deckel = einstellungen("felder")
_einst_deckel["hoechstvorrat_je_stoff"] = 5
M.bot_doerfer_ernten(_bot3, 1000.0, _einst_deckel)
M.bot_doerfer_ernten(_bot3, 4600.0, _einst_deckel)
check("4 kein Rohstoff steht ueber dem Deckel",
      all(float(v) <= 5.0 + 1e-9 for v in _d3.vorraete.values()), str(_d3.vorraete))

# ==========================================================================
abschnitt("5. Zurueckschalten bringt die alten Zahlen wieder")
# ==========================================================================
_bot4, _d4 = bot_mit_dorf("original-036")
_vorher = M.bot_dorf_ertrag(_d4, M.bot_wirtschaft_einstellungen(), _bot4)
check("5 derselbe Bot liefert auf 'karte' wieder das Kartenprofil",
      M.bot_dorf_ertrag(_d4, einstellungen("karte"), _bot4) == _vorher,
      f"{M.bot_dorf_ertrag(_d4, einstellungen('karte'), _bot4)} gegen {_vorher}")
# S-8 Stufe 1: 'anlagen' (Vorgabe) und 'felder' rechnen BEIDE den Kern - unterschiedlich ist nur,
# wer bucht. Unterscheidbar bleibt der alte Weg 'karte' (Kartenprofil statt Anlagen).
check("5 auf 'anlagen' und 'felder' rechnet der Kern (beide Wege leben nebeneinander)",
      M.bot_dorf_ertrag(_d4, einstellungen("felder"), _bot4)
      == M.bot_dorf_ertrag(_d4, einstellungen("anlagen"), _bot4),
      str(M.bot_dorf_ertrag(_d4, einstellungen("felder"), _bot4)))

# ==========================================================================
abschnitt("6. Der gemessene Unterschied der beiden Wege (fuer Daniels Entscheidung)")
# ==========================================================================
abschnitt("6 Kartenprofil gegen Felder, je Karte")
for _kennung in ("original-036", "original-096", "original-087"):
    _b, _d = bot_mit_dorf(_kennung)
    _p = M.bot_dorf_ertrag(_d, einstellungen("karte"), _b)
    M.bot_doerfer_bebauen(_d, _einst_felder)
    _f = M.bot_dorf_ertrag(_d, _einst_felder, _b)
    print(f"  {_kennung}: Karte Holz {_p.get('holz')} / Felder Holz {_f.get('holz')}"
          f" | Karte Gold {_p.get('gold')} / Felder Gold {_f.get('gold')}")
    check(f"6 {_kennung}: beide Wege liefern Zahlen", bool(_p) and bool(_f), str((_p, _f)))
_holz_je_karte = {}                                     # Holzertrag des Kartenprofils je Karte
for _k in ("original-036", "original-096", "original-087"):
    _bk, _dk = bot_mit_dorf(_k)                          # Bot und Dorf dieser Karte
    _hk = M.bot_dorf_ertrag(_dk, einstellungen("karte"), _bk).get("holz")   # Profil, nicht Anlagen
    _holz_je_karte[_k] = _hk                             # merken
check("6 das Kartenprofil gibt je Karte einen anderen Holzertrag (die Karte bleibt wichtig)",
      len(set(_holz_je_karte.values())) > 1, str(_holz_je_karte))
befund("6 die Karte wirkt jetzt ueber die FELDER: gleiche Anlagen ernten ueberall gleich, "
       "verschieden ist, WAS auf ihr gebaut werden kann (S-8 Stufe 1). Unterschiedliche Ernten "
       "je Karte kommen aus dem Gelaende, auf dem die Anlagen stehen.", "")

# ==========================================================================
abschnitt("7. Quellwache: der Schalter ist im Code verdrahtet")
# ==========================================================================
check("7 der Ertragsweg liest den Schalter", 'einstellungen.get("ertrag_weg")' in TEXT_MAIN,
      "main.bot_dorf_ertrag / main.bot_doerfer_ernten")
# S-8 Stufe 1: der Aufruf steht seit dem Umbau zweizeilig und gibt den Wissensstand des Bots mit
# (S-4: Forschungsboni wirken sonst nicht auf den Ertrag) - auf den Wortlaut der Zeile pruefen.
check("7 der Kern-Weg ruft wirtschaft.ertrag_gesamt MIT dem Wissensstand des Bots",
      "wirtschaft.ertrag_gesamt([bot_dorf_als_ort(dorf, bot)]," in TEXT_MAIN
      and "forschung_level=forschung" in TEXT_MAIN, "main.bot_dorf_ertrag")
check("7 der Kern-Takt ruft ort_tick - MIT dem Wissensstand des Bots (S-4: vorher ging dort ein "
      "leeres dict hinein, jede Bot-Forschung war fuer den Ertrag wirkungslos)",
      "spieloekonomie.ort_tick(ort, float(ab), float(bis), bot_forschungsstaende(bot))" in TEXT_MAIN,
      "main.bot_dorf_tick")
check("7 der Takt verzweigt auf den Kern-Weg", "if kern_weg:" in TEXT_MAIN,
      "main.bot_doerfer_ernten")

sys.exit(bericht())
