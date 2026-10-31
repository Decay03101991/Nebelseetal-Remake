"""Papier-Mockup der Siedlungsansicht (A-5) aus dem ECHTEN Spielstand bauen.

Aufruf:  python -X utf8 tools/konzept_mockup.py
Ausgabe: docs/design/SIEDLUNG_KONZEPT_20261101.html
Reine Anzeige - kein Spielcode, keine erfundenen Zahlen: alles kommt aus
`~/.nebelseetal/savegame_slot1.json` (Gebaeude, Stufen, Ertraege, Siedlerreserve).
Links Menue, Mitte Karte, rechts Berater-Panel - Daniels Vorgabe 31.10.2026:
"versuch detailiert das orginal zu treffen, benutzerfreundlich, uebersichtlich,
jedes Menue und jeder Button genug Platz". Reine Anzeige, kein Spielcode.
"""
import json
import os
import sys
import sys as _s

PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s.path.insert(0, os.path.join(PROJEKT, "src"))
import gelaende        # noqa: E402
import wirtschaft      # noqa: E402
import spieloekonomie  # noqa: E402

SKIN = {"bg": "#2a0605", "panel": "#3e1c1a", "gold": "#FFCC33", "red": "#e53935",
        "text": "#FFFF99", "topbar": "#1a0a09", "sidebar": "#1a0a09",
        "button": "#3e2723", "button_active": "#5D4037", "border": "#4a1512",
        "subhead": "#FF6600"}

SPEICHER = os.path.join(os.path.expanduser("~"), ".nebelseetal", "savegame_slot1.json")
with open(SPEICHER, encoding="utf-8") as f:
    stand = json.load(f)
siedlung = stand["settlements"][0]
karte = siedlung["karte"]
raster = karte["raster"]
bauten = siedlung.get("bauten") or {}
stufen = siedlung.get("stufen") or {}

forschung = {k: int((v or {}).get("level", 0) if isinstance(v, dict) else v)
             for k, v in (stand.get("research") or {}).items()}
if not forschung:
    forschung = {k: int(v.get("level", 0)) for k, v in
                 (stand.get("forschungsstaende") or {}).items()}

ueb = wirtschaft.dorf_uebersicht(siedlung, forschung)
reserve = spieloekonomie.siedler_reserve(siedlung, forschung)

MOTIVE = {"haus": "motiv_1.png", "erzmine": "motiv_7.png", "kriegerakademie": "motiv_5.png"}
FAMILIE = {"holzfaeller": "#4e7d3a", "steinmetz": "#7d7d7d", "erzmine": "#8d6e63",
           "tempel": "#8e6bb5", "farm": "#c9a227", "goldmine": "#d4af37",
           "schafszucht": "#dcdcdc", "rinderfarm": "#a1887f", "pferdezucht": "#8d6e63",
           "jaeger": "#2e5d34", "schmiede": "#b05a20", "bogenbauer": "#a0522d",
           "naehstube": "#b06a8a", "kriegerakademie": "#8b3a3a", "diebesgilde": "#5d4037",
           "stellmacher": "#6d4c41", "bibliothek": "#3a5f8b", "haus": "#c8a165",
           "lager": "#7a5c3a", "verteidigungswall": "#4a4a4a"}

felder = []
for i, art in enumerate(raster):
    gebaut = bauten.get(str(i))
    if gebaut:
        stufe = int(stufen.get(str(i), 1) or 1)
        farbe = FAMILIE.get(gebaut, "#555")
        name = gelaende.gebaeude_name(gebaut)
        motiv = MOTIVE.get(gebaut)
        bild = (f'<img src="../../assets/icons/gebaeude/{motiv}" alt="{name}">' if motiv else "")
        felder.append(f'<div class="feld belegt" style="--farbe:{farbe}" title="{name} Stufe {stufe}">'
                      f'{bild}<span class="pips">{"●" * min(stufe, 5)}</span></div>')
    else:
        felder.append(f'<div class="feld {art}" title="{gelaende.name(art)}">'
                      f'<span class="grund"></span></div>')

menue = [("Dorfzentrum", "🏰"), ("Lager", "📦"), ("Kaserne", "⚔"), ("Marktplatz", "⚖"),
         ("Gilde", "🛡"), ("Forschung", "📖"), ("Portal", "🌀"), ("Karten", "🗺"),
         ("Nachrichten", "✉"), ("Diplomatie", "🤝"), ("Ruhmeshalle", "🏆"),
         ("Einstellungen", "⚙")]
menue_html = "".join(
    f'<div class="menu-punkt{" aktiv" if n == "Dorfzentrum" else ""}">'
    f'<span class="mi">{i}</span><span class="mt">{n}</span></div>' for n, i in menue)

gebaeude_zeilen = "".join(
    f'<tr><td>{g["name"]}</td><td class="num">{g["anzahl"]}</td>'
    f'<td class="num">{g["stufen_text"].replace("Stufe ", "").replace("Stufen ", "")}</td>'
    f'<td class="ertrag">{g["ertrag_text"] or "—"}</td>'
    f'<td class="num">{g["anteil"] * 100:.0f} %</td></tr>'
    for g in ueb["gebaeude"][:12])

ertraege = ", ".join(f'{r} {v:g}/h' for r, v in ueb["summe"]["ertrag"].items())

HTML = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<title>Siedlungsansicht — Papier (A-5)</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:{SKIN['bg']}; color:{SKIN['text']};
         font-family:"Segoe UI", Arial, sans-serif; font-size:14px; }}
  .kopf {{ height:64px; display:flex; align-items:center; gap:18px; padding:0 24px;
           background:{SKIN['topbar']}; border-bottom:2px solid {SKIN['border']}; }}
  .kopf h1 {{ margin:0; font-size:22px; color:{SKIN['gold']}; letter-spacing:.5px; }}
  .kopf .dorf {{ color:{SKIN['subhead']}; font-size:15px; }}
  .leiste {{ display:flex; gap:22px; margin-left:auto; font-size:14px; }}
  .leiste b {{ color:{SKIN['gold']}; font-weight:600; }}
  .rahmen {{ display:flex; align-items:flex-start; gap:16px; padding:16px 20px; }}
  /* ---------------- links: Menue, einheitlich ---------------- */
  .menue {{ width:236px; flex:0 0 236px; background:{SKIN['sidebar']};
            border:1px solid {SKIN['border']}; border-radius:6px; padding:8px; }}
  .menue h2 {{ margin:4px 8px 10px; font-size:12px; letter-spacing:1.2px;
               color:#9a8a6a; font-weight:600; }}
  .menu-punkt {{ display:flex; align-items:center; gap:10px; height:44px; padding:0 12px;
                 margin-bottom:4px; border-radius:5px; background:{SKIN['button']};
                 border:1px solid transparent; cursor:pointer; }}
  .menu-punkt .mi {{ width:22px; text-align:center; font-size:16px; }}
  .menu-punkt .mt {{ font-size:14px; }}
  .menu-punkt.aktiv {{ background:{SKIN['button_active']}; border-color:{SKIN['gold']};
                       color:#fff; font-weight:600; }}
  /* ---------------- Mitte: Karte ---------------- */
  .mitte {{ flex:1 1 auto; min-width:0; }}
  .kartenkopf {{ display:flex; align-items:center; gap:14px; margin-bottom:10px; }}
  .kartenkopf h2 {{ margin:0; font-size:18px; color:{SKIN['gold']}; }}
  .tabs {{ margin-left:auto; display:flex; gap:6px; }}
  .tab {{ height:32px; padding:0 14px; display:flex; align-items:center; border-radius:4px;
          background:{SKIN['button']}; border:1px solid {SKIN['border']}; font-size:13px; }}
  .tab.aktiv {{ background:{SKIN['button_active']}; color:#fff; }}
  .karte {{ max-width:760px; margin:0 auto; background:#17212B; border:1px solid {SKIN['border']}; border-radius:6px;
            padding:12px; }}
  .gitter {{ display:grid; max-width:736px; margin:0 auto; grid-template-columns:repeat(10, 1fr); gap:3px; }}
  .feld {{ position:relative; aspect-ratio:1/1; border-radius:4px; overflow:hidden;
           border:1px solid rgba(0,0,0,.35); }}
  .feld .grund {{ position:absolute; inset:0; }}
  .grasland .grund {{ background:#4a6b3a; }} .wald .grund {{ background:#2e5228; }}
  .steppe .grund {{ background:#7d7a4a; }} .huegel .grund {{ background:#6b6b52; }}
  .berg .grund {{ background:#5a5a5a; }} .wasser .grund {{ background:#2b5876; }}
  .nebelsee .grund {{ background:#3d5a6c; }} .sumpf .grund {{ background:#3b4432; }}
  .feld.belegt {{ background:var(--farbe); display:flex; align-items:center;
                  justify-content:center; }}
  .feld.belegt img {{ width:88%; height:88%; object-fit:contain;
                      filter:drop-shadow(0 1px 1px rgba(0,0,0,.6)); }}
  .feld .pips {{ position:absolute; bottom:1px; left:50%; transform:translateX(-50%);
                 font-size:7px; color:#FFD966; letter-spacing:1px; }}
  .legende {{ display:flex; gap:16px; margin-top:10px; font-size:12px; color:#bfb08c; }}
  .punkt {{ display:inline-block; width:10px; height:10px; border-radius:2px;
            margin-right:5px; vertical-align:-1px; }}
  /* ---------------- rechts: Berater ---------------- */
  .berater {{ width:360px; flex:0 0 360px; display:flex; flex-direction:column; gap:12px; }}
  .karte-panel {{ background:{SKIN['panel']}; border:1px solid {SKIN['border']};
                  border-radius:6px; padding:12px 14px; }}
  .karte-panel h3 {{ margin:0 0 8px; font-size:13px; letter-spacing:1px; color:{SKIN['gold']};
                     text-transform:uppercase; }}
  .zeile {{ display:flex; justify-content:space-between; gap:10px; padding:5px 0;
            border-bottom:1px dotted #5a3a30; font-size:13px; }}
  .zeile:last-child {{ border-bottom:0; }}
  .zeile b {{ color:{SKIN['gold']}; font-weight:600; }}
  .warnung {{ margin-top:8px; padding:8px 10px; border-radius:5px; font-size:12.5px;
              background:#5a2a12; border:1px solid #b06a2a; color:#FFD9A8; }}
  .engpass {{ color:{SKIN['red']}; font-weight:700; }}
  table {{ width:100%; border-collapse:collapse; font-size:12px; }}
  th {{ text-align:left; color:#9a8a6a; font-weight:600; padding:3px 2px; font-size:11px; }}
  td {{ padding:3px 2px; border-top:1px solid #4a2a22; }}
  td.num {{ text-align:right; }} td.ertrag {{ color:{SKIN['gold']}; }}
  .hinweis {{ font-size:11.5px; color:#8a7a5a; margin-top:8px; line-height:1.35; }}
  /* Schmale Fenster: der Berater rutscht UNTER die Karte, statt sie zu ueberdecken.
     Daniels Vorgabe: jedes Menue und jeder Button braucht genug Platz. */
  @media (max-width: 1420px) {{
    .rahmen {{ flex-wrap: wrap; }}
    .berater {{ width:auto; flex:1 1 100%; flex-direction:row; align-items:flex-start; }}
    .berater .karte-panel {{ flex:1 1 0; }}
  }}
  @media (max-width: 900px) {{
    .menue {{ width:100%; flex:1 1 100%; }}
    .berater {{ flex-direction:column; }}
  }}
  .knopf {{ height:40px; display:flex; align-items:center; justify-content:center;
            background:{SKIN['button']}; border:1px solid {SKIN['gold']};
            border-radius:5px; color:{SKIN['gold']}; font-size:13.5px; margin-top:10px; }}
</style></head>
<body>
  <div class="kopf">
    <h1>Nebelseetal</h1><span class="dorf">{siedlung['name']}</span>
    <div class="leiste">
      <span>Spieltag <b>{stand.get('day', '?')}</b></span>
      <span>Siedler <b>{reserve['frei']:.1f}/{reserve['grenze']}</b></span>
      <span>Gebäude <b>{ueb['summe']['anzahl']}</b></span>
    </div>
  </div>
  <div class="rahmen">
    <nav class="menue"><h2>MENÜ</h2>{menue_html}</nav>
    <main class="mitte">
      <div class="kartenkopf">
        <h2>Siedlungskarte</h2>
        <div class="tabs">
          <div class="tab aktiv">Karte</div><div class="tab">Dorfübersicht</div>
          <div class="tab">Weltkarte</div>
        </div>
      </div>
      <div class="karte"><div class="gitter">{''.join(felder)}</div></div>
      <div class="legende">
        <span><i class="punkt" style="background:#4a6b3a"></i>Grasland</span>
        <span><i class="punkt" style="background:#2e5228"></i>Wald</span>
        <span><i class="punkt" style="background:#5a5a5a"></i>Berg</span>
        <span><i class="punkt" style="background:#2b5876"></i>Wasser</span>
        <span><i class="punkt" style="background:#3b4432"></i>Sumpf</span>
        <span>Punkte unter einem Gebäude = Ausbaustufe</span>
      </div>
    </main>
    <aside class="berater">
      <div class="karte-panel">
        <h3>Berater</h3>
        <div class="zeile"><span>Engpass</span><span class="engpass">Gold {ueb['summe']['ertrag'].get('Gold', 0):g}/h</span></div>
        <div class="zeile"><span>Ertrag gesamt</span><b>{ertraege}</b></div>
        <div class="zeile"><span>Siedlerreserve</span><b>{reserve['frei']:.1f}</b></div>
        <div class="zeile"><span>Nachwuchs</span><b>{reserve['zuwachs_stunde']:.1f}/h</b></div>
        {'<div class="warnung">⚠ ' + reserve['text'] + '</div>' if reserve['text'] else ''}
      </div>
      <div class="karte-panel">
        <h3>Offene Bedingungen</h3>
        <div class="zeile"><span>Nahrungsnot</span><span>keine</span></div>
        <div class="zeile"><span>Bibliothek</span><span>1 von 2</span></div>
        <div class="zeile"><span>Ausbildungsstätten</span><span>3 vor Ort</span></div>
        <div class="knopf">Zum Dorfzentrum</div>
      </div>
      <div class="karte-panel">
        <h3>Gebäude ({ueb['summe']['anzahl']})</h3>
        <table><tr><th>Gebäude</th><th class="num">Anz.</th><th class="num">Stufe</th>
        <th>je Stunde</th><th class="num">Anteil</th></tr>{gebaeude_zeilen}</table>
        <div class="hinweis">Anteil = Summe aller Rohstoffe dieses Gebäudetyps geteilt durch den
        Gesamtertrag des Ortes. Bauten binden keine Siedler (Entscheidung 31.10.2026).</div>
      </div>
    </aside>
  </div>
</body></html>
"""

ZIEL = os.path.join(PROJEKT, "docs", "design")
os.makedirs(ZIEL, exist_ok=True)
pfad = os.path.join(ZIEL, "SIEDLUNG_KONZEPT_20261101.html")
with open(pfad, "w", encoding="utf-8") as f:
    f.write(HTML)
print("geschrieben:", pfad, len(HTML), "Zeichen")
print("Gebaeude:", ueb["summe"]["anzahl"], "| Siedler:", round(reserve["frei"], 2),
      "| Motive:", len(MOTIVE))
