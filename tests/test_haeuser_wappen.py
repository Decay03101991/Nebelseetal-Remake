"""W-15: die sechs Haeuser und ihre Wappenbeschreibungen (Register 206, 05.11.2026).

Daniels Auftrag (05.11.2026, woertlich-nah): "Hausnamen und Wappenbeschreibungen auf die
gelieferten Bilder umschreiben." Diese Datei belegt, dass genau das geschehen ist und dass
es nicht zurueckrutscht:

  (a) `data/haeuser.json` traegt sechs Haeuser, deckungsgleich mit den Fraktionen in
      `data/voelker.json` - kein Volk doppelt, keines fehlt,
  (b) jedes Haus hat Name, Volk, Welt, Farben, Sitz und eine Wappenbeschreibung,
  (c) Burg und Wappen jedes Hauses EXISTIEREN als Bilddatei,
  (d) das Wappen im Hausdatensatz ist DASSELBE wie in `data/bot_wappen.json` - eine Quelle,
      keine zweite Wahrheit (sonst zeigen Karte und Chronik verschiedene Schilde),
  (e) BEIDE Chronik-Fassungen (Wurzel und `docs/`) beschreiben jedes Wappen aus dem Bild:
      sechs Saetze "Das Wappen fuehrt ..." und keiner der alten, erfundenen Motive,
  (f) die beiden Chronik-Fassungen sind hashgleich,
  (g) GEGENPROBE: ein erfundener Satz mit einem alten Motiv MUSS von der Wache erkannt werden -
      sonst ist die Liste blind und ihr Gruen bedeutet nichts.

Warum das noetig war: die frueheren Saetze nannten Motive, die auf keinem der zehn gelieferten
Bilder stehen (Wellenbalken, Hechtkamm, Widderhoerner, Schwanenfluegel, Stierhoerner,
Geierfaecher, Flickenmuster) und behaupteten einen Helm, den die Bilder nicht zeigen. Die
Bilder sind Daniels Lieferung, der Text hatte sich davon geloest.

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['haeuser', 'main:*', 'voelker', 'welt']
PRUEF_DATEN = ['bot_wappen.json', 'haeuser.json', 'voelker.json', 'welt_fraktionen.json', 'welten.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Das Wort, mit dem jeder neue Wappensatz beginnt (Umlaut als Escape, Datei bleibt ASCII).
WAPPEN_ANFANG = "Das Wappen f\u00fchrt"

# Motive, die auf KEINEM gelieferten Bild stehen - ihr Auftauchen ist ein Rueckfall.
ALTE_MOTIVE = [
    "Wellenbalken",                    # alter Text Menschen
    "Hechtkamm",                       # alter Text Menschen (Helmzier, die es nicht gibt)
    "Weizenb\u00fcndel",               # alter Text Menschen
    "Widderh\u00f6rner",               # alter Text Zwerge
    "Mei\u00dfel",                     # alter Text Zwerge
    "Schwanenfl\u00fcgel",             # alter Text Elfen
    "Stierh\u00f6rner",                # alter Text Trolle
    "Geierf\u00e4cher",                # alter Text Ghule
    "Flickenmuster",                   # alter Text Gnome
    "auf dem Helm",                    # die Behauptung eines Helms
    "Auf dem Helm",
]


def datei_hash(pfad: str) -> str:
    """SHA256 einer Datei als Beleg fuer die Gleichheit zweier Fassungen."""
    with open(pfad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def lies(pfad: str) -> str:
    """Textdatei zeilengetreu lesen (CRLF bleibt CRLF)."""
    with open(pfad, encoding="utf-8", newline="") as f:
        return f.read()


def motive_gefunden(text: str) -> list:
    """Alle alten Motive, die im Text noch vorkommen - die Messung der Wache."""
    return [m for m in ALTE_MOTIVE if m in text]


def main() -> int:
    """Prueft Datensatz, Bilder, Bindung und beide Chronik-Fassungen."""
    haeuser_pfad = os.path.join(ROOT, "data", "haeuser.json")
    voelker_pfad = os.path.join(ROOT, "data", "voelker.json")
    wappen_pfad = os.path.join(ROOT, "data", "bot_wappen.json")
    chronik = [
        os.path.join(ROOT, "CHRONIK_DER_WELT.md"),
        os.path.join(ROOT, "docs", "CHRONIK_DER_WELT_20261104.md"),
    ]

    for pfad in [haeuser_pfad, voelker_pfad, wappen_pfad] + chronik:
        if not os.path.isfile(pfad):
            check(f"Datei vorhanden: {os.path.relpath(pfad, ROOT)}", False, "fehlt")
            return bericht()

    with open(haeuser_pfad, encoding="utf-8") as f:
        haeuser = json.load(f)["je_haus"]
    with open(voelker_pfad, encoding="utf-8") as f:
        voelker = [e["kennung"] for e in json.load(f)["fraktionen"]]
    with open(wappen_pfad, encoding="utf-8") as f:
        bot_wappen = json.load(f)["je_fraktion"]

    # ---------------------------------------------------------------- (a) Abdeckung
    abschnitt("(a) sechs Haeuser, deckungsgleich mit den Fraktionen")
    check("Hausdatensatz hat sechs Haeuser", len(haeuser) == 6, f"{len(haeuser)} gefunden")
    check("kein Volk doppelt und keines fehlt", sorted(haeuser) == sorted(voelker),
          f"Haeuser {sorted(haeuser)} vs Voelker {sorted(voelker)}")
    check("jedes Haus hat ein Volk aus data/voelker.json",
          all(h.get("volk") for h in haeuser.values()))

    # ---------------------------------------------------------------- (b) Pflichtfelder
    abschnitt("(b) jedes Haus ist vollstaendig beschrieben")
    for kennung in sorted(haeuser):
        haus = haeuser[kennung]
        fehlt = [feld for feld in ("haus", "volk", "welt", "farben", "sitz", "wappen", "wappen_beschreibung")
                 if not str(haus.get(feld, "")).strip()]
        check(f"{kennung}: alle Felder gefuellt", not fehlt, f"fehlt: {fehlt}")
        check(f"{kennung}: Wappensatz beginnt mit '{WAPPEN_ANFANG}'",
              haus.get("wappen_beschreibung", "").startswith(WAPPEN_ANFANG),
              haus.get("wappen_beschreibung", "")[:40])
        check(f"{kennung}: Wappensatz nennt ausdruecklich, dass kein Helm gefuehrt wird",
              "Helm und eine Helmzier f\u00fchrt das Wappen nicht" in haus.get("wappen_beschreibung", ""))

    # ---------------------------------------------------------------- (c) Bilder existieren
    abschnitt("(c) Burg und Wappen existieren als Bilddatei")
    for kennung in sorted(haeuser):
        for art in ("burg", "wappen"):
            pfad = os.path.join(ROOT, haeuser[kennung][art].replace("/", os.sep))
            check(f"{kennung}: {art} liegt da", os.path.isfile(pfad), haeuser[kennung][art])

    # ---------------------------------------------------------------- (d) eine Quelle
    abschnitt("(d) dasselbe Wappen wie auf der Karte (data/bot_wappen.json)")
    for kennung in sorted(haeuser):
        soll = bot_wappen.get(kennung, {}).get("wappen", "")
        check(f"{kennung}: Wappen stimmt mit der Karte ueberein",
              haeuser[kennung]["wappen"] == soll,
              f"Haus {haeuser[kennung]['wappen']} vs Karte {soll}")

    # ---------------------------------------------------------------- (e) Chronik
    abschnitt("(e) beide Chronik-Fassungen beschreiben die gelieferten Bilder")
    for pfad in chronik:
        text = lies(pfad)
        name = os.path.relpath(pfad, ROOT)
        check(f"{name}: sechs neue Wappensaetze", text.count(WAPPEN_ANFANG) == 6,
              f"{text.count(WAPPEN_ANFANG)} gefunden")
        gefunden = motive_gefunden(text)
        check(f"{name}: keines der alten, erfundenen Motive", not gefunden, f"noch da: {gefunden}")
        check(f"{name}: jeder Hausname steht im Text",
              all(h["haus"].replace("Haus ", "") in text for h in haeuser.values()))

    # ---------------------------------------------------------------- (f) Fassungen gleich
    abschnitt("(f) die beiden Chronik-Fassungen sind hashgleich")
    check("Wurzel und docs/ sind identisch",
          datei_hash(chronik[0]) == datei_hash(chronik[1]),
          f"{datei_hash(chronik[0])[:12]} vs {datei_hash(chronik[1])[:12]}")

    # ---------------------------------------------------------------- (g) Gegenprobe
    abschnitt("(g) GEGENPROBE: die Wache erkennt einen alten Satz")
    probe = ("Der Herrschaftssitz ist die Burg Silberbach. Das Wappen zeigt einen silbernen "
             "Wellenbalken auf blauem Grund. Auf dem Helm sitzt ein Hechtkamm.")
    treffer = motive_gefunden(probe)
    check("erfundener Satz wird erkannt", len(treffer) >= 2, f"erkannt: {treffer}")
    check("sauberer Satz wird NICHT beanstandet", not motive_gefunden(haeuser["menschlich"]["wappen_beschreibung"]))
    if len(ALTE_MOTIVE) < 5:
        befund("Motivliste zu kurz", f"{len(ALTE_MOTIVE)} Eintraege")

    # ---------------------------------------------------------------- (h) Heimatwelt eine Quelle
    abschnitt("(h) die Heimatwelt jedes Hauses stimmt mit den Weltdaten ueberein")
    with open(os.path.join(ROOT, "data", "welt_fraktionen.json"), encoding="utf-8") as f:
        zuordnung = json.load(f)["zuordnung"]
    with open(os.path.join(ROOT, "data", "welten.json"), encoding="utf-8") as f:
        weltnamen = {d["kennung"]: d["name"] for d in json.load(f)["dimensionen"]}
    for kennung in sorted(haeuser):
        nummer = int(zuordnung.get(kennung, 0) or 0)
        soll = weltnamen.get(f"d{nummer:02d}", "")
        check(f"{kennung}: Welt passt zu welt_fraktionen.json", haeuser[kennung]["welt"] == soll,
              f"Haus {haeuser[kennung]['welt']} vs Daten {soll}")

    # ---------------------------------------------------------------- (i) Lesestelle im Spiel
    abschnitt("(i) das Spiel liest die Hausdaten ueber EINE Stelle (src/haeuser.py)")
    sys.path.insert(0, os.path.join(ROOT, "src"))
    haus_modul = __import__("haeuser")
    check("Modul liefert sechs Haeuser", len(haus_modul.alle()) == 6, f"{len(haus_modul.alle())}")
    check("Hausname der Menschen", haus_modul.hausname("menschlich") == "Haus Silberbach",
          haus_modul.hausname("menschlich"))
    check("unbekannte Fraktion gibt leeren Namen", haus_modul.hausname("gibt-es-nicht") == "")
    check("Wappenpfad der Trolle endet auf haus_schattenfaust.png",
          haus_modul.wappen("Trolle").endswith("haus_schattenfaust.png"), haus_modul.wappen("Trolle"))
    check("Kurzbeschreibung vorhanden", bool(haus_modul.wappen_kurz("elfisch")))
    check("kaputte Datei gibt ein leeres Dict statt eines Absturzes",
          haus_modul.alle(os.path.join(ROOT, "data", "gibt-es-nicht.json")) == {})
    with open(os.path.join(ROOT, "src", "main.py"), encoding="utf-8") as f:
        haupt = f.read()
    check("die Voelkerwahl zeigt den Hausnamen (main.py nutzt haeuser.hausname)",
          "haeuser.hausname(" in haupt)

    return bericht()


if __name__ == "__main__":
    sys.exit(main())
