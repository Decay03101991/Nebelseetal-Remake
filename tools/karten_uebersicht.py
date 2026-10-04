"""
Kartenuebersicht erzeugen: zeigt die Siedlungskarten als Bild und als HTML-Seite.

Erzeugt:
  docs/karten_vorschau/uebersicht.html   — alle Kartentypen farbig mit Beschriftung
  docs/karten_vorschau/<typ>.png         — je Kartentyp ein Rasterbild
  docs/karten_vorschau/spielverlauf.png  — fuenf nacheinander gegruendete Siedlungen

Bilder werden mit reiner Standardbibliothek geschrieben (zlib + struct), damit das
Projekt ohne Zusatzpakete auskommt.

Aufruf:  python tools/karten_uebersicht.py
"""
from __future__ import annotations

import os
import struct
import sys
import zlib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "src"))
import gelaende as G  # noqa: E402
import main as M  # noqa: E402

ZIEL = WURZEL / "docs" / "karten_vorschau"

FELD = 34          # Kantenlaenge einer Kachel in Pixeln
RAHMEN = 1         # Rahmen zwischen den Feldern
HINTERGRUND = (16, 16, 18)


def farbe_zu_rgb(hexfarbe: str):
    h = hexfarbe.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def png_schreiben(pfad: Path, breite: int, hoehe: int, bild) -> None:
    """Schreibt ein RGB-PNG ohne Fremdbibliothek."""
    roh = b"".join(b"\x00" + bytes(v for pixel in zeile for v in pixel) for zeile in bild)

    def chunk(typ: bytes, daten: bytes) -> bytes:
        return (struct.pack(">I", len(daten)) + typ + daten
                + struct.pack(">I", zlib.crc32(typ + daten) & 0xFFFFFFFF))

    kopf = struct.pack(">IIBBBBB", breite, hoehe, 8, 2, 0, 0, 0)
    pfad.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", kopf)
                     + chunk(b"IDAT", zlib.compress(roh, 9)) + chunk(b"IEND", b""))


def rasterbild(karten: list, spalten_anordnung: int = 1):
    """Bild mit einem oder mehreren Kartenrastern untereinander."""
    breite_karte = karten[0]["spalten"] * FELD + 1
    hoehe_karte = karten[0]["zeilen"] * FELD + 1
    b = breite_karte
    h = len(karten) * hoehe_karte + (len(karten) - 1) * 10
    bild = [[HINTERGRUND for _ in range(b)] for _ in range(h)]
    y0 = 0
    for karte in karten:
        for reihe, zeile in enumerate(karte["zeilen_raster"]):
            for spalte, art in enumerate(zeile):
                farbe = farbe_zu_rgb(G.farbe(art))
                for y in range(FELD):
                    ziel_y = y0 + reihe * FELD + y
                    if ziel_y >= h:
                        break
                    for x in range(FELD):
                        ziel_x = spalte * FELD + x
                        if ziel_x >= b:
                            break
                        bild[ziel_y][ziel_x] = farbe
        y0 += hoehe_karte + 10
    return b, h, bild


def main() -> int:
    ZIEL.mkdir(parents=True, exist_ok=True)
    einsaetze = [
        (20261004, "waldreich"), (20261005, "bergreich"), (20261006, "weideland"),
        (20261007, "nebelseeufer"), (20261008, "gemischt"),
    ]
    karten = [G.siedlungskarte_erzeugen(saat, typ_id=typ) for saat, typ in einsaetze]

    print("Kartentypen im Vergleich")
    print("=" * 78)
    for (saat, _), karte in zip(einsaetze, karten):
        print()
        print(f"{karte['typ_name']}  (Saat {karte['seed']})")
        print(f"  Vorteil: {karte['vorteil']}")
        print(f"  {G.karte_beschreiben(karte)}")
        profil = ", ".join(f"{k}={v}" for k, v in sorted(karte["profil"].items(), key=lambda x: -x[1]))
        print(f"  Höchstertrag/Stunde: {profil}")
        for zeile in G.karte_als_text(karte).splitlines():
            print(f"    {zeile}")
        breite, hoehe, bild = rasterbild([karte])
        png_schreiben(ZIEL / f"{karte['typ']}.png", breite, hoehe, bild)

    # Ein echter Spielverlauf: fuenf nacheinander gegruendete Siedlungen
    print()
    print("=" * 78)
    print("Fuenf Siedlungen eines Spielverlaufs (Handbuch S. 313: keine zwei gleichen Karten)")
    print("=" * 78)
    vergeben = []
    for _ in range(5):
        vergeben.append(M.neue_siedlungskarte(vergeben))
    for i, k in enumerate(vergeben, 1):
        print(f"  Siedlung {i}: {k['typ_name']:<20} Saat {k['seed']:<10} "
              f"Wald {k['zaehlung']['wald']:>2} Berg {k['zaehlung']['berg']:>2} "
              f"Gras {k['zaehlung']['grasland']:>2} See {k['zaehlung']['nebelsee']:>2} "
              f"Sumpf {k['zaehlung']['sumpf']:>2} | {k['vorteil'][:44]}")
    check = len({M.karten_signatur(k) for k in vergeben})
    print(f"  -> {check} verschiedene Karten von 5 (muss 5 sein)")
    breite, hoehe, bild = rasterbild(vergeben)
    png_schreiben(ZIEL / "spielverlauf.png", breite, hoehe, bild)

    # HTML-Uebersicht
    def karte_html(karte: dict, nummer: str) -> str:
        felder = []
        for i, art in enumerate(karte["raster"]):
            felder.append(
                f'<div class="feld" style="background:{G.farbe(art)}" '
                f'title="{G.name(art)} (Feld {i})">{i}</div>')
        profil = "".join(
            f"<span class='p'>{k} {v}</span>"
            for k, v in sorted(karte["profil"].items(), key=lambda x: -x[1]) if v > 0)
        return (f'<section><h2>{nummer} {karte["typ_name"]}</h2>'
                f'<p class="vorteil">{karte["vorteil"]}</p>'
                f'<p class="maße">{karte["spalten"]}×{karte["zeilen"]} Felder · '
                f'Saat {karte["seed"]} · {karte["beschreibung"]}</p>'
                f'<div class="raster">{"".join(felder)}</div>'
                f'<div class="profil">{profil}</div></section>')

    legende = "".join(
        f'<span class="l"><i style="background:{G.farbe(a)}"></i>{G.name(a)}'
        f'{"" if G.ist_bebaubar(a) else " (nicht bebaubar)"}</span>'
        for a in G.GELAENDEARTEN)

    html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Siedlungskarten — Nebelseetal Remake</title>
<style>
 body {{ color: var(--foreground); font-family: inherit; margin: 0; }}
 h1 {{ font-size: 1.15rem; margin: 0 0 .3rem; }}
 h2 {{ font-size: 1rem; margin: 0 0 .2rem; }}
 .hinweis {{ color: var(--muted-foreground); font-size: .82rem; margin: 0 0 .8rem; }}
 section {{ margin: 0 0 1.1rem; }}
 .vorteil {{ margin: .1rem 0; font-size: .88rem; }}
 .maße {{ margin: .1rem 0 .4rem; color: var(--muted-foreground); font-size: .78rem; }}
 .raster {{ display: grid; grid-template-columns: repeat(8, 26px); gap: 1px; }}
 .feld {{ width: 26px; height: 26px; font-size: .55rem; color: rgba(0,0,0,.55);
          display: flex; align-items: center; justify-content: center; }}
 .legende {{ display: flex; flex-wrap: wrap; gap: .55rem; margin: .2rem 0 1rem;
             font-size: .78rem; color: var(--muted-foreground); }}
 .l {{ display: flex; align-items: center; gap: .3rem; }}
 .l i {{ width: 13px; height: 13px; display: inline-block; border: 1px solid var(--border); }}
 .profil {{ display: flex; flex-wrap: wrap; gap: .4rem; font-size: .76rem; margin-top: .35rem; }}
 .p {{ border: 1px solid var(--border); border-radius: 3px; padding: .05rem .3rem; }}
</style></head><body>
<h1>Siedlungskarten — fünf Typen mit verschiedenen Vorteilen</h1>
<p class="hinweis">Geländearten und Erträge aus dem Originalhandbuch; die Zahlen in den
Feldern sind die Feldnummern zum Bauen. Fünf Kartentypen nach deiner Vorgabe „mehrere Karten
mit verschiedenen Vorteilen". Der Vorteil ist aus den belegten Erträgen gerechnet.</p>
<div class="legende">{legende}</div>
{"".join(karte_html(k, f"{i+1}.") for i, k in enumerate(karten))}
</body></html>
"""
    (ZIEL / "uebersicht.html").write_text(html, encoding="utf-8")

    # Spielverlaufs-HTML
    html2 = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Fünf Siedlungen eines Spielverlaufs</title>
<style>
 body {{ color: var(--foreground); font-family: inherit; margin: 0; }}
 h1 {{ font-size: 1.15rem; margin: 0 0 .3rem; }}
 .hinweis {{ color: var(--muted-foreground); font-size: .82rem; margin: 0 0 .8rem; }}
 .zeile {{ display: flex; gap: .8rem; align-items: flex-start; margin: 0 0 .7rem; }}
 .raster {{ display: grid; grid-template-columns: repeat(8, 22px); gap: 1px; }}
 .feld {{ width: 22px; height: 22px; }}
 .text {{ font-size: .82rem; line-height: 1.35; }}
 .vorteil {{ color: var(--muted-foreground); }}
</style></head><body>
<h1>Fünf Siedlungen nacheinander — keine zwei Karten gleich</h1>
<p class="hinweis">Handbuch S. 313: „Einer neuen Siedlung wird per Zufall eine Karte zugewiesen.
Es werden niemals zwei Deiner Siedlungen die gleiche Karte bekommen." Genau so im Spiel umgesetzt.</p>
{"".join(
  f'<div class="zeile"><div class="raster">{"".join(f"<div class=feld style=background:{G.farbe(a)}></div>" for a in k["raster"])}</div>'
  f'<div class="text"><b>Siedlung {i}</b> — {k["typ_name"]}<br>'
  f'Wald {k["zaehlung"]["wald"]} · Berg {k["zaehlung"]["berg"]} · Gras {k["zaehlung"]["grasland"]} · '
  f'Hügel {k["zaehlung"]["huegel"]} · Steppe {k["zaehlung"]["steppe"]} · See {k["zaehlung"]["nebelsee"]} · Sumpf {k["zaehlung"]["sumpf"]}<br>'
  f'<span class="vorteil">{k["vorteil"]}</span></div></div>'
  for i, k in enumerate(vergeben, 1))}
</body></html>
"""
    (ZIEL / "spielverlauf.html").write_text(html2, encoding="utf-8")

    print()
    print(f"Geschrieben nach {ZIEL}:")
    for p in sorted(ZIEL.iterdir()):
        print(f"  {p.name:<22} {p.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
