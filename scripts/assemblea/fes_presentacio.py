"""Genera la presentació (HTML amb diapositives) a partir de fitxa.json."""
import json
import os

import os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fitxa.json")))
DESTI = "/home/nex/Documents/teatre/Assemblea_2026_presentacio.html"

ing_escola = 6525.50
ing_subv = 3619.80 + 250.00
ing_taquilla = 2183.00 + 2292.49 + 988.00 + 1886.72
AJUST = -12.00
net_amb = D["tot_net"] + AJUST


def eur(x, signe=False):
    s = f"{abs(x):,.2f}".replace(",", "·").replace(".", ",").replace("·", ".")
    if x < 0:
        return "−" + s + " €"
    return ("+" if signe and x > 0 else "") + s + " €"


def num(x):
    return f"{x:,.0f}".replace(",", ".")


obres = [o for o in D["obres"]]
# 1.000 € de la subvenció municipal corresponen al Teatre Sènior: es traslladen
# de la línia "Subvenció 2026" a la seva obra, perquè cada obra mostri el seu compte.
TRASPAS = 1000.00
for o in obres:
    if o["nom"] == "Teatre Senior 2026":
        o["ing"] += TRASPAS
        o["net"] += TRASPAS
    elif o["nom"] == "Subvenció 2026":
        o["ing"] -= TRASPAS
        o["net"] -= TRASPAS
obres.sort(key=lambda o: o["net"], reverse=True)
maxnet = max(abs(o["net"]) for o in obres) or 1


MINI = {"Teatre Senior 2026": "1.000 € de subvenció municipal",
        "Subvenció 2026": "resta de la subvenció (no assignada a una obra)"}

NOMS = {"Costes financeres 2025": "Costes nov-des 2025",
        "Costes administratives 2026": "Costes administratius 2026",
        "Subvenció 2025*": "Subvenció 2025 (cobrada el 2025)"}


def barra(net, maxim):
    amplada = max(2.5, abs(net) / maxim * 100)
    color = "var(--gold)" if net >= 0 else "var(--vi2)"
    return (f'<div class="b"><span style="width:{amplada:.1f}%;background:{color}"></span></div>')


guanyen = [o for o in obres if o["net"] >= 0]
perden = [o for o in obres if o["net"] < 0]
max_pos = max([abs(o["net"]) for o in guanyen] or [1])
max_neg = max([abs(o["net"]) for o in perden] or [1])


def _fila(o):
    ing = eur(o["ing"]) if o["ing"] else "—"
    desp = eur(o["desp"]) if o["desp"] else "—"
    res_cls = "pos" if o["net"] >= 0 else "neg"
    nom = NOMS.get(o["nom"], o["nom"])
    if o["nom"] in MINI:
        nom += f'<span class="mini">{MINI[o["nom"]]}</span>'
    return (f'<div class="lin"><div class="nom">{nom}</div>' 
            f'<div class="x ing{" buit" if not o["ing"] else ""}">{ing}</div>'
            f'<div class="x des{" buit" if not o["desp"] else ""}">{desp}</div>'
            f'<div class="x res {res_cls}">{eur(o["net"], True)}</div></div>')


ORDRE_OBRES = ["Total Pastorets 2025", "Criatures 2026", "Pervertimento 2026", "Engrunes 2026",
               "Teatre Senior 2026", "Escola Teatre 2026", "Somnis d'institut 2026"]
ORDRE_RESTA = ["Subvenció 2026", "Subvenció 2025*", "Costes financeres 2025",
               "Inversions 2026", "Costes administratives 2026"]
PER_NOM = {o["nom"]: o for o in obres}

CAP = ('<div class="cap"><div>Obra o activitat</div><div class="x">Ingressos</div>'
       '<div class="x">Despeses</div><div class="x">Resultat</div></div>')

suma_ing = sum(PER_NOM[n]["ing"] for n in ORDRE_OBRES if n in PER_NOM)
suma_desp = sum(PER_NOM[n]["desp"] for n in ORDRE_OBRES if n in PER_NOM)
suma_net = suma_ing + suma_desp

files_obres = ('<div class="taula">' + CAP
               + "".join(_fila(PER_NOM[n]) for n in ORDRE_OBRES if n in PER_NOM)
               + f'<div class="lin tot"><div class="nom">Subtotal de les obres</div>'
                 f'<div class="x ing">{eur(suma_ing)}</div>'
                 f'<div class="x des">{eur(suma_desp)}</div>'
                 f'<div class="x res {"pos" if suma_net >= 0 else "neg"}">{eur(suma_net, True)}</div></div>'
               + '</div>')

files_resta = ('<div class="taula">' + CAP
               + "".join(_fila(PER_NOM[n]) for n in ORDRE_RESTA if n in PER_NOM)
               + '<div class="lin ajust"><div class="nom">Ajust de tancament 2025</div>'
                 '<div class="x ing buit">—</div><div class="x des">−12,00 €</div>'
                 '<div class="x res neg">−12,00 €</div></div>'
               + f'<div class="lin tot"><div class="nom">TOTAL DEL CICLE</div>'
                 f'<div class="x ing">{eur(D["tot_ing"])}</div>'
                 f'<div class="x des">{eur(D["tot_desp"] + AJUST)}</div>'
                 f'<div class="x res pos">{eur(net_amb, True)}</div></div>'
               + '</div>')




# ---- dades de la Memòria d'activitats 2025-2026 ----
OBRES_MEM = [
    ("Engrunes de teatre 2025", "11 d'octubre de 2025", 143, "Obertura de temporada"),
    ("Pastorets 2025", "26, 27 i 28 de desembre", 317, "Les funcions de Nadal"),
    ("Criatures", "20 i 21 de març de 2026", 357, "Dins del Cap Butaca Buida"),
    ("Pervertimento", "25 i 26 d'abril de 2026", 131, "Sanchis Sinisterra"),
    ("La Companyia de la Fantasia", "13 de juny de 2026", 155, "Musical de l'escola"),
    ("Gente Bien", "20 i 21 de juny de 2026", 224, "El muntatge del grup Sènior"),
    ("Engrunes: racons de Po(e)r", "30 d'octubre de 2026", 72, "Biblioteca el Castell"),
]
TOTAL_ENTRADES = sum(o[2] for o in OBRES_MEM)
DIES_FUNCIO = 12

files_mem = "\n".join(
    f'<div class="lin"><div class="nom">{o}</div><div class="dat">{d}</div>'
    f'<div class="x ent">{n}</div><div class="nota">{nota}</div></div>'
    for o, d, n, nota in OBRES_MEM)


# ---- opinions del públic 2026 ----
CITES = [["Fantàstic, ho han fet molt bé, hem passat una estona molt divertida. L'escenografia molt original. I com hem rigut.", "Montse Bruach", "Criatures", 10], ["Tota una gran aventura entre llibres. Tot de la mà d'un guia que et porta per diferents espais de la biblioteca on ens esperen diverses històries de por. Molt bona ambientació entre llibres i foscor.", "Montserrat Prior", "Engrunes de Po(e)r", 10], ["Una obra divertida plena de bons moments, actors i actrius esplèndids, una escenografia molt cuidada i una direcció de 10.", "Anna Martínez", "Criatures", 10], ["Molt original i interessant. La qualitat del so baixa i no s'escolta prou bé.", "Jose M. Córcoles", "Criatures", 8], ["Molt bona presentació, amb photo-call inclòs. Vestuari i decorats acurats. Actuació irregular però molt entranyable!", "Carme", "Gente bien", 7], ["Un esdeveniment molt treballat per les persones que van participar en l'organització, les interpretacions molt bones i el lloc espectacular.", "Andrés Parejo", "Engrunes de Po(e)r", 10], ["Va ser una obra genial!!! Divertida, dinàmica i espectacular.", "Anna Vives", "La companyia de la fantasia", 10], ["Una obra densa i molt ben interpretada. Felicitats.", "Isabel Díaz", "Pervertimento", 9]]


# ---- pressupost 2027 (pestanya «Pressupost 2027» del full de comptes) ----
ING_27 = [("Escola de Teatre", 5145.00), ("Pastorets 2026", 2240.00), ("Lectura de Lorca", 1080.00),
          ("Enemic del poble", 1540.00), ("Jocs Florals", 1680.00), ("Somnis d'institut", 2800.00),
          ("Subvenció de l'Ajuntament", 3696.00), ("Subvenció sènior", 250.00), ("Altres", 300.00)]
DESP_27 = [("Escola de Teatre", 4725.00), ("Pastorets 2026", 1750.00), ("Lectura de Lorca", 1100.00),
           ("Enemic del poble", 1700.00), ("Jocs Florals", 1350.00), ("Somnis d'institut", 3200.00),
           ("Engrunes 2027", 350.00), ("Costes administratius", 1530.00), ("Hisenda", 850.00),
           ("Formació interna", 300.00), ("Sortides de teatre", 2000.00), ("Imprevistos (5 %)", 942.75)]
TOT_ING_27 = sum(v for _, v in ING_27)
TOT_DESP_27 = sum(v for _, v in DESP_27)
RES_27 = TOT_ING_27 - TOT_DESP_27
INV_27 = 2100.00
SALDO_27 = 3801.64


def files_dos(llista, signe=False):
    return "\n".join(
        f'<div class="fila"><div class="n">{n}</div><div class="v">{eur(v, signe)}</div></div>'
        for n, v in llista)

# ingressos per origen
origen = [
    ("Escola de Teatre", ing_escola, "36,8%"),
    ("Taquilla de les obres", ing_taquilla, "41,4%"),
    ("Subvencions de l'Ajuntament", ing_subv, "21,8%"),
]
files_origen = "\n".join(
    f'<div class="fila"><div class="n">{n}</div><div class="v pos">{eur(v)}</div>'
    f'<div class="b"><span style="width:{v / D["tot_ing"] * 100:.1f}%;background:var(--gold)"></span></div></div>'
    for n, v, _ in origen
)

CITES_JS = json.dumps(CITES, ensure_ascii=False)

HTML = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Assemblea 2026 · Grup de Teatre Jove de Vacarisses</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    /* tema clar: el de projecció */
    --bg: #FFFFFF; --bg2: #F3EFE6; --ink: #05060B;
    --gold: #6E4A06; --gold-clar: #5F3F04; --vi: #6E1430; --vi2: #8A1B29;
    --muted: rgba(5,6,11,.86);
    --line: rgba(13,14,27,.20); --line-fort: rgba(13,14,27,.30);
    --track: rgba(13,14,27,.13); --weak: rgba(13,14,27,.45);
    --accent-soft: rgba(162,112,26,.4); --aigua: rgba(162,112,26,.10);
  }}
  html[data-tema="fosc"] {{
    --bg: #101126; --bg2: #23254a; --ink: #f7f2e8;
    --gold: #e2b654; --gold-clar: #e2b654; --vi: #98192f; --vi2: #c2455c;
    --muted: rgba(247,242,232,.58);
    --line: rgba(255,255,255,.13); --line-fort: rgba(255,255,255,.22);
    --track: rgba(255,255,255,.09); --weak: rgba(255,255,255,.28);
    --accent-soft: rgba(226,182,84,.35); --aigua: rgba(226,182,84,.07);
  }}
  html, body {{ height: 100%; }}
  body {{
    background: var(--bg); color: var(--ink);
    font-family: "Helvetica Neue", Inter, system-ui, -apple-system, "Segoe UI", sans-serif;
    overflow: hidden;
  }}
  .deck {{ position: relative; width: 100vw; height: 100vh; }}
  .slide {{
    position: absolute; inset: 0; padding: 3.6vh 4.4vw 5.4vh;
    display: flex; flex-direction: column; justify-content: center;
    opacity: 0; pointer-events: none; transition: opacity .4s ease;
    background: var(--bg);
  }}
  .slide.on {{ opacity: 1; pointer-events: auto; }}
  .kicker {{ font-size: clamp(15.5px, 1.42vw, 21px); letter-spacing: .16em;
    text-transform: uppercase; color: var(--gold); margin-bottom: 2.2vh; }}
  h1 {{ font-family: Georgia, "Times New Roman", serif; font-weight: 400;
    font-size: clamp(34px, 5.5vw, 84px); line-height: 1.05; letter-spacing: -.01em; }}
  h2 {{ font-family: Georgia, "Times New Roman", serif; font-weight: 400;
    font-size: clamp(38px, 5.3vw, 86px); line-height: 1.06; margin-bottom: 3.6vh; }}
  .sub {{ color: var(--muted); font-size: clamp(21px, 2.05vw, 32px); line-height: 1.55; max-width: 62ch; }}
  .rule {{ width: 92px; height: 3px; background: var(--gold); margin: 3.4vh 0; }}

  /* portada */
  .portada {{ display: block; overflow: hidden; }}
  .portada .cos {{ position: absolute; left: 8vw; right: 8vw; top: 50%; transform: translateY(-50%); }}
  .portada .any {{ position: absolute; right: 3vw; top: 3vh; z-index: 0;
    font-family: Georgia, serif; font-size: clamp(70px, 15.5vw, 200px);
    line-height: .8; color: var(--aigua); letter-spacing: -.05em; }}
  .portada h1, .portada .kicker, .portada .sub, .portada .meta, .portada .rule {{ position: relative; z-index: 1; }}
  .meta {{ margin-top: 4vh; display: flex; gap: 3.2rem; flex-wrap: wrap; color: var(--muted);
    font-size: clamp(12px, 1.1vw, 16px); letter-spacing: .04em; }}
  .meta b {{ color: var(--ink); font-weight: 500; }}
  .junta {{ margin-top: 3.2vh; padding-top: 2.6vh; border-top: 1px solid var(--line);
    display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 1.4rem 1.8rem; }}
  .junta .carrec {{ display: block; font-size: clamp(9.5px,.82vw,11.5px); letter-spacing: .18em;
    text-transform: uppercase; color: var(--gold); opacity: .85; margin-bottom: .5em; }}
  .junta b {{ font-size: clamp(16.5px, 1.42vw, 21px); font-weight: 500; color: var(--ink); }}

  /* xifres grans */
  .grid3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.2vw; align-items: start; }}
  .xifra .l {{ font-size: clamp(16px, 1.4vw, 21px); letter-spacing: .12em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 1.4vh; }}
  .xifra .v {{ font-family: Georgia, serif; font-size: clamp(33px, 4.15vw, 62px); line-height: 1.03;
    white-space: nowrap; font-variant-numeric: tabular-nums; letter-spacing: -.01em; }}
  .xifra .v.pos {{ color: var(--gold); }}
  .xifra .v.neg {{ color: var(--vi2); }}
  .xifra .d {{ color: var(--muted); font-size: clamp(16.5px, 1.42vw, 21px); margin-top: 1.2vh; }}

  /* llistes amb barres */
  .llista {{ display: flex; flex-direction: column; gap: clamp(6px, .95vh, 14px); }}
  .fila {{ display: grid; grid-template-columns: 1fr 9.5em; gap: 1.4vw; align-items: center;
    font-size: clamp(20px, 2.1vw, 30px); }}
  .fila .n {{ color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .fila .v {{ text-align: right; font-variant-numeric: tabular-nums; font-weight: 500; }}
  .fila .v.pos {{ color: var(--gold); }} .fila .v.neg {{ color: var(--vi2); }}
  .b {{ grid-column: 1 / -1; height: 6px; background: var(--track); border-radius: 4px;
    overflow: hidden; margin-top: -2px; }}
  .b span {{ display: block; height: 100%; border-radius: 4px; }}

  .taula-mem .cap, .taula-mem .lin {{ display: grid;
    grid-template-columns: minmax(0,1.15fr) 13.5rem 5.2rem minmax(0,1fr);
    gap: 1rem; align-items: center; }}
  .taula-mem .cap {{ font-size: clamp(9px,.82vw,11px); letter-spacing: .16em; text-transform: uppercase;
    color: var(--muted); padding-bottom: 1.1vh; border-bottom: 1px solid rgba(255,255,255,.14); }}
  .taula-mem .lin {{ font-size: clamp(15.5px, 1.52vw, 21.5px); padding: .55vh 0;
    border-bottom: 1px solid var(--line); }}
  .taula-mem .dat {{ color: var(--muted); }}
  .taula-mem .ent {{ text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; color: var(--ink); }}
  .taula-mem .nota {{ color: var(--muted); font-size: clamp(15px, 1.34vw, 19.5px); }}
  .taula-mem .tot {{ border-top: 1px solid var(--gold-clar); margin-top: .4vh; padding-top: 1.1vh;
    font-weight: 600; border-bottom: 0; }}
  .taula-mem .tot .ent {{ color: var(--gold); }}

  /* opinions */
  #opinions {{ justify-content: center; }}
  .cita {{ transition: opacity .45s ease; min-height: 30vh; display: flex; flex-direction: column; justify-content: center; }}
  .cita blockquote {{ font-family: Georgia, "Times New Roman", serif; font-size: clamp(28px, 3.5vw, 52px);
    line-height: 1.38; max-width: 54ch; letter-spacing: -.005em; }}
  .cita blockquote::before {{ content: "«"; color: var(--gold); }}
  .cita blockquote::after {{ content: "»"; color: var(--gold); }}
  .cita .autor {{ margin-top: 2.4vh; font-size: clamp(13.5px, 1.2vw, 18px); color: var(--muted); letter-spacing: .05em; }}
  .cita .autor b {{ color: var(--ink); font-weight: 500; }}
  .cita .estrelles {{ color: var(--gold); letter-spacing: .1em; margin-left: .5em; }}
  .barra-dades {{ display: flex; gap: 3vw; margin-top: 4vh; padding-top: 2.6vh;
    border-top: 1px solid var(--line); flex-wrap: wrap; }}
  .barra-dades div {{ font-size: clamp(11px, .95vw, 14px); color: var(--muted); letter-spacing: .14em; text-transform: uppercase; }}
  .barra-dades b {{ display: block; font-family: Georgia, serif; font-size: clamp(22px, 2.3vw, 34px);
    color: var(--gold); letter-spacing: 0; text-transform: none; margin-bottom: .35em; }}

  .densa h2 {{ font-size: clamp(27px, 3.5vw, 54px); margin-bottom: 2.2vh; }}
  .densa .taula .lin {{ font-size: clamp(15px, 1.5vw, 21px); padding: .3vh 0; }}
  .densa .taula .grup {{ padding: 1vh 0 .3vh; font-size: clamp(11.5px, 1vw, 14px); }}
  .densa .taula .tot {{ padding-top: .9vh; }}

  .estret .dues .fila {{ font-size: clamp(14.5px, 1.4vw, 20px); }}
  .estret .dues .llista {{ gap: 2px; }}
  .estret h2 {{ font-size: clamp(30px, 4vw, 60px); margin-bottom: 2vh; }}

  .grid3.dues-xifres {{ grid-template-columns: repeat(2, minmax(0, 1fr)); max-width: 44rem; }}

  /* notes */
  .notes {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.8vw 2.8vw; margin-top: .4vh; }}
  .notes div {{ border-left: 2px solid var(--accent-soft); padding-left: 1.1em; }}
  .notes b {{ display: block; color: var(--gold); font-weight: 500; font-size: clamp(16px,1.36vw,21px);
    letter-spacing: .1em; text-transform: uppercase; margin-bottom: .6em; }}
  .notes p {{ color: var(--muted); font-size: clamp(17.5px, 1.58vw, 23.5px); line-height: 1.5; }}

  /* navegació */
  .dots {{ position: fixed; bottom: 3.2vh; left: 8vw; display: flex; gap: 9px; z-index: 10; }}
  .dots i {{ width: 7px; height: 7px; border-radius: 50%; background: var(--track); transition: .25s; }}
  .dots i.on {{ background: var(--gold); transform: scale(1.35); }}
  .hint {{ position: fixed; bottom: 3.2vh; right: 8vw; color: var(--weak);
    font-size: 11px; letter-spacing: .12em; text-transform: uppercase; z-index: 10; }}
  .btn {{ position: fixed; top: 3.2vh; right: 8vw; z-index: 10; background: none; border: 1px solid var(--line-fort);
    color: var(--muted); font-size: 11px; letter-spacing: .14em; text-transform: uppercase;
    padding: .55em 1em; border-radius: 2px; cursor: pointer; }}
  .btn:hover {{ color: var(--gold); border-color: var(--gold); }}
  .btn-tema {{ left: auto; right: calc(8vw + 178px); top: 3.2vh; }}

  .taula {{ display: flex; flex-direction: column; max-width: 57rem; }}
  .taula .cap, .taula .lin {{ display: grid; grid-template-columns: minmax(0,1fr) 9rem 9rem 9.6rem;
    gap: .8rem; align-items: center; }}
  .taula .grup {{ font-size: clamp(9px,.84vw,11.5px); letter-spacing: .2em; text-transform: uppercase;
    color: var(--gold); opacity: .8; padding: 1.5vh 0 .5vh; }}
  .taula .grup:first-of-type {{ padding-top: .2vh; }}
  .taula .cap {{ font-size: clamp(10.5px,.96vw,13.5px); letter-spacing: .14em; text-transform: uppercase;
    color: var(--muted); padding-bottom: 1.1vh; border-bottom: 1px solid var(--line-fort); margin-bottom: .6vh; }}
  .taula .lin {{ font-size: clamp(17.5px, 1.72vw, 24px); padding: .5vh 0;
    border-bottom: 1px solid var(--line); }}
  .taula .lin:last-child {{ border-bottom: 0; }}
  .taula .x {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
  .taula .nom {{ white-space: normal; line-height: 1.18; }}
  .taula .mini {{ display: block; font-size: .68em; color: var(--muted); font-weight: 400; letter-spacing: 0; }}
  .taula .ing {{ color: var(--ink); }}
  .taula .des {{ color: var(--vi2); }}
  .taula .res {{ font-weight: 600; }}
  .taula .res.pos {{ color: var(--gold); }} .taula .res.neg {{ color: var(--vi2); }}
  .taula .buit, .taula .x:only-child {{ color: var(--weak); }}
  .taula .ajust {{ color: var(--muted); font-size: clamp(10.5px,1vw,14px); }}
  .taula .tot {{ border-top: 1px solid var(--gold-clar); margin-top: .5vh; padding-top: 1.1vh;
    font-weight: 600; font-size: clamp(12px,1.16vw,17px); }}

  .dues {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3.4vw; align-items: start; }}
  .dues h3 {{ font-size: clamp(12px, 1.1vw, 16px); letter-spacing: .18em; text-transform: uppercase;
    color: var(--muted); font-weight: 500; margin-bottom: 1.8vh; }}
  .dues .fila {{ font-size: clamp(16px, 1.5vw, 21.5px); grid-template-columns: 1fr 8.2em; }}
  .dues .llista {{ gap: clamp(4px, .62vh, 9px); }}
  .dues .fila.tot {{ border-top: 1px solid var(--gold-clar); margin-top: .6vh; padding-top: .8vh;
    font-weight: 600; }}
  .dues .fila.tot .v {{ color: var(--gold); }}

  /* navegació tàctil */
  .navega {{ display: none; }}
  @media (max-width: 820px) {{
    .slide {{ padding: 5vh 6vw 14vh; height: 100dvh; overflow-y: auto;
      justify-content: flex-start; }}
    .slide::-webkit-scrollbar {{ display: none; }}
    .grid3, .notes, .dues {{ grid-template-columns: 1fr !important; gap: 2.2vh; }}
    .junta {{ grid-template-columns: repeat(2, minmax(0,1fr)); gap: 1.2rem; }}
    .kicker {{ margin: 2vh 0 1.2vh; }}
    h1 {{ font-size: clamp(28px, 8.6vw, 44px); }}
    h2 {{ font-size: clamp(20px, 6.4vw, 30px); margin-bottom: 2.4vh; }}
    .sub {{ font-size: 14px; }}
    .xifra .v {{ font-size: clamp(22px, 7vw, 34px); }}
    .xifra .l, .xifra .d {{ font-size: 11px; }}
    .rule {{ margin: 2vh 0; }}
    .portada .cos {{ position: static; transform: none; padding-top: 6vh; }}
    .portada .any {{ font-size: 44vw; right: -6vw; top: 2vh; }}
    .cita blockquote {{ font-size: 17px; }}
    .barra-dades {{ gap: 1.4rem; }}
    .barra-dades b {{ font-size: 22px; }}

    /* taules → fitxes */
    .taula, .taula-mem {{ max-width: 100%; }}
    .taula .cap, .taula-mem .cap {{ display: none; }}
    .taula-mem .lin {{ display: grid; grid-template-columns: 1fr auto;
      grid-template-areas: "nom ent" "dat dat" "nota nota"; gap: .3rem .8rem;
      padding: 1.2vh 0; font-size: 13px; }}
    .taula-mem .nom {{ grid-area: nom; font-weight: 600; white-space: normal; }}
    .taula-mem .ent {{ grid-area: ent; }}
    .taula-mem .dat {{ grid-area: dat; font-size: 12px; }}
    .taula-mem .nota {{ grid-area: nota; font-size: 11.5px; }}
    .taula .lin {{ display: grid; grid-template-columns: 1fr auto;
      grid-template-areas: "nom res" "ing ing" "des des"; gap: .2rem .8rem;
      padding: 1vh 0; font-size: 12.5px; }}
    .taula .nom {{ grid-area: nom; white-space: normal; }}
    .taula .res {{ grid-area: res; }}
    .taula .ing {{ grid-area: ing; text-align: left; }}
    .taula .des {{ grid-area: des; text-align: left; }}
    .taula .ing::before {{ content: "Ingressos: "; color: var(--muted); }}
    .taula .des::before {{ content: "Despeses: "; color: var(--muted); }}
    .taula .buit::before, .taula .des.buit::before {{ color: var(--muted); }}
    .taula .grup {{ padding-top: 1.6vh; }}

    .btn {{ display: none; }}
    .hint {{ display: none; }}
    .dots {{ left: 6vw; bottom: 3vh; }}
    .navega {{ display: flex; position: fixed; right: 5vw; bottom: 3vh; gap: 10px; z-index: 20; }}
    .navega button {{ width: 48px; height: 48px; border-radius: 50%; background: rgba(255,255,255,.08);
      border: 1px solid rgba(255,255,255,.22); color: var(--ink); font-size: 20px; line-height: 1;
      cursor: pointer; display: grid; place-items: center; -webkit-tap-highlight-color: transparent; }}
    .navega button:active {{ background: var(--gold); color: #191426; }}
  }}
  @media print {{
    @page {{ size: 1280px 720px; margin: 0; }}
    body {{ overflow: visible; }}
    .slide {{ position: relative; opacity: 1 !important; height: 720px; width: 1280px;
      page-break-after: always; break-after: page; }}
    .slide:last-of-type {{ page-break-after: auto; break-after: auto; }}
    .dots, .hint, .btn {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="deck">

  <!-- 1 -->
  <section class="slide on portada">
    <div class="any">2026</div>
    <div class="cos">
    <h1>Assemblea General<br>Ordinària</h1>
    <div class="rule"></div>
    <div class="sub">Memòria d'activitats i estat de comptes<br>Cicle 2025-2026 · octubre de 2025 – novembre de 2026</div>
    <div class="meta">
      <span><b>Dissabte 7 de novembre de 2026</b><br>15:30 h (2a convocatòria 16:00 h)</span>
      <span><b>Sala dels Cups</b><br>Biblioteca el Castell</span>
    </div>
    <div class="junta">
      <div><span class="carrec">President</span><b>Joan Ustrell Gan</b></div>
      <div><span class="carrec">Secretària</span><b>Montserrat Piqué González</b></div>
      <div><span class="carrec">Tresorer</span><b>Joan Teixidó Arquer</b></div>
      <div><span class="carrec">Vocal</span><b>Albert Rubí</b></div>
      <div><span class="carrec">Vocal</span><b>Sílvia Serveto</b></div>
    </div>
    </div>
  </section>

  <!-- memòria 1 -->
  <section class="slide">
    <div class="kicker">Primera part · El curs 2025-2026</div>
    <h2>Set produccions, i més gent a tot arreu.</h2>
    <div class="grid3">
      <div class="xifra"><div class="l">Produccions</div><div class="v">7</div>
        <div class="d">Estrenades o en marxa</div></div>
      <div class="xifra"><div class="l">Entrades</div><div class="v pos">{num(TOTAL_ENTRADES)}</div>
        <div class="d">En {DIES_FUNCIO} dies de funció</div></div>
      <div class="xifra"><div class="l">Escola de teatre</div><div class="v">2</div>
        <div class="d">Grups, tots dos de musical</div></div>
    </div>
    <div class="sub" style="margin-top:3.4vh">Una mitjana de 118 persones per dia de representació, sense comptar les Engrunes,
      que tenen un format de recorregut i no es poden mesurar igual.</div>
  </section>

  <!-- memòria 2 -->
  <section class="slide">
    <div class="kicker">Les obres</div>
    <h2>Una per una</h2>
    <div class="taula-mem">
      <div class="cap"><div>Obra</div><div>Dates</div><div class="x">Entrades</div><div>Notes</div></div>
      {files_mem}
      <div class="lin tot"><div class="nom">TOTAL</div><div class="dat">{DIES_FUNCIO} dies de funció</div>
        <div class="x ent">{num(TOTAL_ENTRADES)}</div><div class="nota"></div></div>
    </div>
  </section>

  <!-- opinions -->
  <section class="slide" id="opinions">
    <div class="kicker">El públic</div>
    <h2>Què en diu la gent</h2>
    <div class="cita" id="cita">
      <blockquote id="cita-text">Fantàstic, ho han fet molt bé, hem passat una estona molt divertida. L'escenografia molt original. I com hem rigut.</blockquote>
      <div class="autor" id="cita-autor"><b>Montse Bruach</b> · Criatures<span class="estrelles">★★★★★★★★★★</span></div>
    </div>
    <div class="barra-dades">
      <div><b>43</b> opinions rebudes el 2026</div>
      <div><b>9,6</b> de nota mitjana</div>
      <div><b>86 %</b> puntuen amb 9 o 10</div>
      <div><b>1.399</b> entrades al curs</div>
    </div>
  </section>

  <!-- memòria 3 -->
  <section class="slide">
    <div class="kicker">Formació</div>
    <h2>L'escola: dos grups, tots dos de musical</h2>
    <div class="notes">
      <div><b>Curs 2025-2026</b><p>Dos grups, de gener a juny: iniciació (I5 a 2n de primària) amb sis
        alumnes i musical amb deu o onze. Van tancar amb «La Companyia de la Fantasia», 155 entrades.</p></div>
      <div><b>Curs 2026-2027</b><p>Dos grups, tots dos de musical: el de petits, els dilluns, i el de mitjans,
        els dissabtes. Set mesos de curs, 35 € al mes i 75 € el dissabte.</p></div>
      <div><b>Teatre Sènior</b><p>El curs per a gent gran, conduït per Jan Prats, és el motor de «Gente Bien»
        i una de les línies estables del grup.</p></div>
      <div><b>Formació interna</b><p>Jornada de pedagogia del teatre el 7 de novembre (10-13 h), oberta a
        tothom, i un monogràfic per trimestre amb el suport de Judith Josa.</p></div>
    </div>
  </section>

  <!-- memòria 4 -->
  <section class="slide">
    <div class="kicker">Més enllà de l'escenari</div>
    <h2>El que també hem fet</h2>
    <div class="notes">
      <div><b>Reis 2026</b><p>Organització dels patges de la cavalcada del 5 de gener, amb la Glòria Miralles
        i en Joan Teixidó al capdavant.</p></div>
      <div><b>Cap Butaca Buida</b><p>Les funcions de «Criatures» es van fer dins aquesta iniciativa d'abast
        català que omple els teatres el tercer cap de setmana de març.</p></div>
      <div><b>Berenar de Pastorets</b><p>13 de setembre, al Casal de la Gent Gran, amb socis, actors i
        famílies: el tret de sortida de la temporada.</p></div>
      <div><b>Lliga del Llumillu</b><p>Durant la Festa Major, membres del grup van formar part del jurat
        d'aquesta gimcana, que enguany feia deu anys i va aplegar dotze equips.</p></div>
      <div><b>Amb l'Ajuntament</b><p>Reunió amb la regidora de Cultura, Olga Serra, per demanar més espai per
        al material i un pany al vestidor del teatre.</p></div>
      <div><b>Federació</b><p>Soci de la Federació Amateur; assemblea del 14 de març de 2026. La quota anual
        ha passat de 150 a 160 €.</p></div>
    </div>
  </section>

  <!-- memòria 5 -->
  <section class="slide">
    <div class="kicker">El que ve</div>
    <h2>Projectes en marxa i properes cites</h2>
    <div class="notes">
      <div><b>Somnis d'institut</b><p>El musical del curs 2026-2027. Càsting al juny i primera lectura el
        18 d'octubre a la Sala Neus Català; les cançons ja estan enllestides.</p></div>
      <div><b>Pastorets 2026</b><p>Berenar el 13 de setembre, assajos des del 27, i funcions el 26 i 27
        de desembre.</p></div>
      <div><b>Enemic del poble</b><p>3 i 4 d'abril de 2027.</p></div>
      <div><b>Lectura de Lorca</b><p>20 i 21 de febrer de 2027, amb el grup Sènior i altres poetes.</p></div>
      <div><b>Jocs Florals</b><p>5 i 6 de juny de 2027.</p></div>
      <div><b>Pessebre vivent</b><p>Proposta de fer-lo amb altres entitats del poble, amb la Fresera com a
        possible escenari.</p></div>
    </div>
  </section>

  <!-- 2 -->
  <section class="slide">
    <div class="kicker">Segona part · Els comptes</div>
    <h2>Hem gastat menys del que hem ingressat,<br>i el marge és petit.</h2>
    <div class="grid3">
      <div class="xifra"><div class="l">Ingressos</div><div class="v">{eur(D["tot_ing"])}</div>
        <div class="d">Quotes, taquilla i subvencions</div></div>
      <div class="xifra"><div class="l">Despeses</div><div class="v neg">{eur(D["tot_desp"])}</div>
        <div class="d">Obres, escola i administració</div></div>
      <div class="xifra"><div class="l">Resultat</div><div class="v pos">{eur(net_amb, True)}</div>
        <div class="d">Un 8,4 % sobre els ingressos</div></div>
    </div>
  </section>

  <!-- 3 -->
  <section class="slide">
    <div class="kicker">Tresoreria</div>
    <h2>On són els diners</h2>
    <div class="grid3">
      <div class="xifra"><div class="l">Compte SumUp</div><div class="v">{eur(D["banc"])}</div>
        <div class="d">Compte operatiu del grup</div></div>
      <div class="xifra"><div class="l">Caixa</div><div class="v">{eur(D["efectiu"])}</div>
        <div class="d">Repartida en dues caixes</div></div>
      <div class="xifra"><div class="l">Total</div><div class="v pos">{eur(D["final"])}</div>
        <div class="d">A 6 de novembre de 2026</div></div>
    </div>
    <div class="rule"></div>
    <div class="sub">El compte de La Caixa queda a zero: tota l'operativa passa pel compte de SumUp.
      A l'inici del cicle el grup tenia {eur(D["inici"])}.</div>
  </section>

  <!-- 4 -->
  <section class="slide">
    <div class="kicker">Ingressos</div>
    <h2>D'on vénen els {eur(D["tot_ing"])}</h2>
    <div class="llista">
      {files_origen}
    </div>
    <div class="rule"></div>
    <div class="sub">L'escola és el motor estable; la taquilla depèn de cada obra; la subvenció municipal
      ha arribat en quatre pagaments al llarg de l'any.</div>
  </section>

  <!-- 5 -->
  <section class="slide">
    <div class="kicker">Resultat per obra</div>
    <h2>Cada obra, el seu compte</h2>
    {files_obres}
  </section>

  <section class="slide">
    <div class="kicker">Resultat per obra</div>
    <h2>Subvencions, costes i ajustos</h2>
    {files_resta}
  </section>

  <!-- 6 -->
  <section class="slide">
    <div class="kicker">Lectura</div>
    <h2>El que ens ha funcionat</h2>
    <div class="grid3">
      <div class="xifra"><div class="l">Escola de Teatre</div><div class="v pos">+1.401,47 €</div>
        <div class="d">112 moviments: el motor del grup</div></div>
      <div class="xifra"><div class="l">Pastorets 2025</div><div class="v pos">+505,17 €</div>
        <div class="d">Es va pagar sol</div></div>
      <div class="xifra"><div class="l">Subvencions</div><div class="v pos">+3.869,80 €</div>
        <div class="d">Un 21,8 % dels ingressos</div></div>
    </div>
  </section>

  <!-- 7 -->
  

  <!-- 8 -->
  <section class="slide">
    <div class="kicker">Compte de resultats</div>
    <h2>Del resultat a la caixa</h2>
    <div class="grid3">
      <div class="xifra"><div class="l">Saldo inicial 1/11/2025</div><div class="v">{eur(D["inici"])}</div></div>
      <div class="xifra"><div class="l">+ Resultat del cicle</div><div class="v pos">{eur(net_amb, True)}</div></div>
      <div class="xifra"><div class="l">Saldo final 6/11/2026</div><div class="v pos">{eur(D["final"])}</div></div>
    </div>
    <div class="rule"></div>
    <div class="sub">Les obres sumen {eur(D["tot_net"], True)}; s'hi ha aplicat un ajust de
      {eur(AJUST)} corresponent a una diferència de tancament del curs anterior, que queda
      registrada amb una línia pròpia al full de comptes.</div>
  </section>

  <!-- pressupost 2027 -->
  <section class="slide">
    <div class="kicker">Pressupost 2027</div>
    <h2>El curs que ve, en tres números</h2>
    <div class="grid3">
      <div class="xifra"><div class="l">Ingressos previstos</div><div class="v">{eur(TOT_ING_27)}</div>
        <div class="d">Escola, taquilla i subvencions</div></div>
      <div class="xifra"><div class="l">Despeses previstes</div><div class="v neg">{eur(-TOT_DESP_27)}</div>
        <div class="d">Amb un 5 % d'imprevistos</div></div>
      <div class="xifra"><div class="l">Resultat previst</div><div class="v neg">{eur(RES_27, True)}</div>
        <div class="d">Amb les colònies del grup incloses</div></div>
    </div>
    <div class="dues" style="margin-top:3.2vh">
      <div class="col">
        <h3>Inversions 2027 (a part de la despesa)</h3>
        <div class="llista">
          <div class="fila"><div class="n">Ordinador</div><div class="v">{eur(600.0)}</div></div>
          <div class="fila"><div class="n">Mobles per al local nou</div><div class="v">{eur(1500.0)}</div></div>
          <div class="fila tot"><div class="n">Total inversions</div><div class="v">{eur(INV_27)}</div></div>
        </div>
      </div>
      <div class="col">
        <h3>Com acaba la tresoreria</h3>
        <div class="llista">
          <div class="fila"><div class="n">Saldo a 1 de novembre de 2026</div><div class="v">{eur(6968.39)}</div></div>
          <div class="fila"><div class="n">+ Resultat previst</div><div class="v">{eur(RES_27, True)}</div></div>
          <div class="fila"><div class="n">− Inversions</div><div class="v">{eur(INV_27)}</div></div>
          <div class="fila tot"><div class="n">Saldo a 31 d'octubre de 2027</div><div class="v">{eur(SALDO_27)}</div></div>
        </div>
      </div>
    </div>
  </section>

  <!-- detall pressupost -->
  <section class="slide estret">
    <div class="kicker">Pressupost 2027</div>
    <h2>D'on surt i on va cada euro</h2>
    <div class="dues">
      <div class="col">
        <h3>Ingressos · {eur(TOT_ING_27)}</h3>
        <div class="llista">
          {files_dos(ING_27)}
          <div class="fila tot"><div class="n">Total</div><div class="v">{eur(TOT_ING_27)}</div></div>
        </div>
      </div>
      <div class="col">
        <h3>Despeses · {eur(TOT_DESP_27)}</h3>
        <div class="llista">
          {files_dos(DESP_27)}
          <div class="fila tot"><div class="n">Total</div><div class="v">{eur(TOT_DESP_27)}</div></div>
        </div>
      </div>
    </div>
    <div class="sub" style="margin-top:3vh">A part, les inversions: <b style="color:var(--gold)">2.100 €</b>
      (ordinador 600 € i mobles per al local nou 1.500 €). No compten com a despesa de l'exercici.</div>
  </section>

  <!-- 9 -->
  <section class="slide">
    <div class="kicker">Nota metodològica</div>
    <h2>Com s'ha fet aquest número</h2>
    <div class="notes">
      <div><b>Període</b><p>De l'1 de novembre de 2025 al 6 de novembre de 2026, com marca el cicle anual del grup.</p></div>
      <div><b>Font</b><p>Full de comptes del grup, amb extracte bancari de SumUp creuat línia a línia.</p></div>
      <div><b>Caixa</b><p>Recompte a mà: 880,40 €, repartits en dues caixes. Els diners d'una altra associació s'han separat.</p></div>
      <div><b>Ajust</b><p>12 € d'una diferència de tancament de l'any anterior, registrats com a línia pròpia.</p></div>
    </div>
  </section>

  <!-- 10 -->
  <section class="slide portada">
    <div class="cos">
    <div class="kicker">Per acabar</div>
    <h1>Precs i preguntes</h1>
    <div class="rule"></div>
    <div class="sub">Gràcies per la feina de tot l'any. El que no quedi clar avui, ho mirem<br>amb els papers a la mà.</div>
    <div class="meta"><span><b>Grup de Teatre Jove de Vacarisses</b><br>grupteatrejove.cat</span></div>
    </div>
  </section>

</div>

<div class="dots" id="dots"></div>
<div class="hint">← → per passar</div>
<button class="btn btn-tema" id="tema" onclick="canviaTema()">Tema fosc</button>
<button class="btn" onclick="pantalla()">Pantalla completa</button>
<div class="navega">
  <button id="prev" aria-label="Diapositiva anterior">‹</button>
  <button id="next" aria-label="Diapositiva següent">›</button>
</div>

<script>
  const slides = [...document.querySelectorAll('.slide')];
  const dots = document.getElementById('dots');
  let i = 0;
  slides.forEach((_, k) => {{ const d = document.createElement('i'); if (!k) d.className = 'on'; dots.appendChild(d); }});
  pinta();
  function pinta() {{
    slides.forEach((s, k) => s.classList.toggle('on', k === i));
    [...dots.children].forEach((d, k) => d.classList.toggle('on', k === i));
  }}
  function ves(n) {{ i = Math.max(0, Math.min(slides.length - 1, n)); pinta(); }}
  const ARREL = document.documentElement;
  function pintaBotoTema() {{
    const b = document.getElementById('tema');
    if (b) b.textContent = ARREL.dataset.tema === 'fosc' ? 'Tema clar' : 'Tema fosc';
  }}
  function canviaTema() {{
    ARREL.dataset.tema = ARREL.dataset.tema === 'fosc' ? '' : 'fosc';
    try {{ localStorage.setItem('tema', ARREL.dataset.tema); }} catch (e) {{}}
    pintaBotoTema();
  }}
  try {{
    const desat = localStorage.getItem('tema');
    if (desat) ARREL.dataset.tema = desat;
  }} catch (e) {{}}
  pintaBotoTema();

  function pantalla() {{
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }}
  addEventListener('keydown', e => {{
    if (['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)) {{ e.preventDefault(); ves(i + 1); }}
    if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) {{ e.preventDefault(); ves(i - 1); }}
    if (e.key === 'f') pantalla();
    if (e.key === 'Home') ves(0);
    if (e.key === 'End') ves(slides.length - 1);
  }});
  addEventListener('click', e => {{
    if (e.target.closest('.btn') || e.target.closest('.navega')) return;
    if (e.clientX === undefined) return;
    ves(i + (e.clientX > innerWidth / 2 ? 1 : -1));
  }});
  const botoPrev = document.getElementById('prev');
  const botoNext = document.getElementById('next');
  if (botoPrev) botoPrev.addEventListener('click', e => {{ e.stopPropagation(); ves(i - 1); }});
  if (botoNext) botoNext.addEventListener('click', e => {{ e.stopPropagation(); ves(i + 1); }});
  // cites del públic: van passant mentre la diapositiva és visible
  const CITES = {CITES_JS};
  let ci = 1;
  function pintaCita() {{
    const capsa = document.getElementById('cita');
    const text = document.getElementById('cita-text');
    const autor = document.getElementById('cita-autor');
    if (!capsa) return;
    capsa.style.opacity = 0;
    setTimeout(() => {{
      const c = CITES[ci % CITES.length];
      ci++;
      text.textContent = c[0];
      autor.innerHTML = '<b>' + c[1] + '</b> · ' + c[2] +
        '<span class="estrelles">' + '★'.repeat(c[3]) + '</span>';
      capsa.style.opacity = 1;
    }}, 460);
  }}
  setInterval(() => {{
    const s = document.getElementById('opinions');
    if (s && s.classList.contains('on')) pintaCita();
  }}, 5800);

  let x0 = null, y0 = null, mogut = false;
  addEventListener('touchstart', e => {{
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; mogut = false;
  }}, {{ passive: true }});
  addEventListener('touchmove', e => {{
    if (x0 === null) return;
    if (Math.abs(e.touches[0].clientX - x0) > 12) mogut = true;
  }}, {{ passive: true }});
  addEventListener('touchend', e => {{
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    const dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 35 && Math.abs(dx) > Math.abs(dy)) {{
      ves(i + (dx < 0 ? 1 : -1));
      e.preventDefault();
    }}
    x0 = null;
  }});
</script>
</body>
</html>
"""

open(DESTI, "w", encoding="utf-8").write(HTML)
print("fet:", DESTI, len(HTML), "bytes |", HTML.count('class="slide'), "diapositives")
