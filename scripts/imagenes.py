"""Genera las imágenes de las notas del blog: portada y figuras (gráficos, datos, pasos).

Uso: python3 scripts/imagenes.py <slug> [<slug> ...]   (o --todas para las que no tienen portada)
Lee content/blog/<slug>.md y escribe en src/static/img/blog/:
  <slug>.jpg      portada 1600x1000 (se usa en el listado, la nota, la home y al compartir)
  <slug>-N.jpg    figura N de la lista "figuras" del encabezado (1600 de ancho)

Encabezado de la nota (todo opcional salvo lo que pide build.py):
  portada:
    frase: "Tus anuncios ahora en ChatGPT"     # 3 a 7 palabras, va grande en la portada
    escena: "¿Qué agencia me recomendás?"       # texto dentro del dibujo (chat, buscador, anuncio...)
    dato: "+40%"                                 # opcional: número protagonista
    dato_texto: "más ventas"
  figuras:
    - tipo: barras        (titulo, datos: [[etiqueta, número], ...], unidad, fuente)
    - tipo: dato          (dato, texto, fuente)
    - tipo: pasos         (titulo, pasos: [texto, ...])
    - tipo: comparacion   (titulo, columnas: [a, b], filas: [[x, y], ...])
En el texto se insertan con ![descripción](/img/blog/<slug>-1.jpg "Pie de imagen").
Necesita Chromium (en la nube de Claude ya está) y `pip install playwright`.
"""
import glob, html, re, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "static" / "img" / "blog"
FONTS = ROOT / "src" / "static" / "fonts"
LOGO = ROOT / "src" / "static" / "img" / "mdl-logo-blanco.png"
esc = html.escape

# Cada categoría tiene su mundo: color de fondo, tinta y el objeto que se dibuja.
TEMAS = {
    "Inteligencia artificial": {"bg": "#6220AF", "fg": "#FFFFFF", "ac": "#C9A8FF", "card": "#FFFFFF", "ink": "#150E1F", "motivo": "chat"},
    "Publicidad digital": {"bg": "#0B0612", "fg": "#F4F1F8", "ac": "#C9A8FF", "card": "#FFFFFF", "ink": "#150E1F", "motivo": "anuncio"},
    "Redes sociales": {"bg": "#C9A8FF", "fg": "#150E1F", "ac": "#6220AF", "card": "#0B0612", "ink": "#FFFFFF", "motivo": "reel"},
    "Negocios y pymes": {"bg": "#F4F1F8", "fg": "#150E1F", "ac": "#6220AF", "card": "#FFFFFF", "ink": "#150E1F", "motivo": "barras"},
    "Web y SEO": {"bg": "#150E1F", "fg": "#F4F1F8", "ac": "#C9A8FF", "card": "#FFFFFF", "ink": "#150E1F", "motivo": "buscador"},
}


def fuentes():
    return "".join(f'@font-face{{font-family:P;font-weight:{w};src:url("{(FONTS / f"poppins-latin-{w}-normal.woff2").as_uri()}")}}'
                   for w in (400, 500, 600, 700, 800, 900)) + \
        f'@font-face{{font-family:M;src:url("{(FONTS / "jetbrains-mono-latin-400-normal.woff2").as_uri()}")}}'


def leer(slug):
    raw = (ROOT / "content" / "blog" / f"{slug}.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    return yaml.safe_load(m.group(1))


def motivo(t, meta, p):
    """El dibujo de la derecha. Usa la 'escena' de la nota para que cada portada sea distinta."""
    escena = esc(p.get("escena") or meta["title"])
    if t["motivo"] == "chat":
        return f'''<div class="phone"><div class="scr" style="background:#F4F1F8">
<div class="top">Asistente</div>
<div class="b me">{escena}</div>
<div class="b bot"><i></i><i></i><i style="width:60%"></i></div>
<div class="b bot"><i></i><i style="width:75%"></i></div>
<div class="inp">Escribí un mensaje</div></div></div>'''
    if t["motivo"] == "anuncio":
        return f'''<div class="phone"><div class="scr" style="background:#fff">
<div class="ig"><span class="av"></span><b>Tu marca</b><small>Publicidad</small></div>
<div class="media"><span>{escena}</span></div>
<div class="ctaw">Enviar mensaje <b>›</b></div>
<div class="lines"><i></i><i style="width:70%"></i></div></div></div>'''
    if t["motivo"] == "reel":
        return f'''<div class="phone"><div class="scr reel">
<div class="rtext">{escena}</div>
<div class="side"><span>♥<small>12,4 mil</small></span><span>●<small>318</small></span><span>➤<small>1.204</small></span></div>
<div class="prog"><i></i></div></div></div>'''
    if t["motivo"] == "buscador":
        return f'''<div class="browser"><div class="bbar"><i></i><i></i><i></i></div>
<div class="q">{escena}</div>
<div class="res hi"><small>somosmdl.com</small><b>Tu negocio, primero</b><i></i></div>
<div class="res"><small>otro-sitio.com</small><b></b><i></i></div>
<div class="res"><small>otro-sitio.com</small><b></b><i></i></div></div>'''
    # barras
    hs = [34, 48, 41, 63, 72, 96]
    return '<div class="chart">' + "".join(f'<i style="height:{h}%"></i>' for h in hs) + f'<span>{escena}</span></div>'


def portada(slug, meta):
    t = TEMAS.get(meta.get("category"), TEMAS["Publicidad digital"])
    p = meta.get("portada") or {}
    frase = esc(p.get("frase") or meta["title"])
    dato = (f'<div class="dato"><b>{esc(str(p["dato"]))}</b><span>{esc(p.get("dato_texto", ""))}</span></div>'
            if p.get("dato") else "")
    logo_filter = "none" if t["fg"].upper() in ("#FFFFFF", "#F4F1F8") else "brightness(0)"
    largo = len(frase)
    size = 128 if largo < 28 else 108 if largo < 44 else 88
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{fuentes()}
*{{box-sizing:border-box;margin:0}}
body{{width:1600px;height:1000px;background:{t["bg"]};color:{t["fg"]};font-family:P;overflow:hidden;position:relative}}
.l{{position:absolute;left:96px;top:92px;bottom:92px;width:820px;display:flex;flex-direction:column}}
.cat{{font:600 28px P;color:{t["ac"]}}}
h1{{font-weight:800;font-size:{size}px;line-height:.98;letter-spacing:-.045em;margin-top:34px;text-wrap:balance}}
.dato{{margin-top:40px;display:flex;align-items:baseline;gap:18px}}
.dato b{{font-size:150px;font-weight:900;letter-spacing:-.06em;line-height:.8;color:{t["ac"]}}}
.dato span{{font-size:32px;font-weight:600;max-width:260px;line-height:1.1}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:22px;font:500 22px P;opacity:.85}}
.foot img{{height:40px;filter:{logo_filter}}}
.r{{position:absolute;right:96px;top:0;bottom:0;width:540px;display:flex;align-items:center;justify-content:center}}
.phone{{width:420px;height:840px;border-radius:56px;background:{t["card"]};padding:14px;transform:rotate(4deg) translateY(70px);box-shadow:0 40px 80px rgba(0,0,0,.25)}}
.scr{{width:100%;height:100%;border-radius:44px;overflow:hidden;position:relative;padding:70px 26px 26px;display:flex;flex-direction:column;gap:18px;color:#150E1F}}
.top{{position:absolute;top:24px;left:0;right:0;text-align:center;font-weight:700;font-size:20px}}
.b{{border-radius:26px;padding:20px 24px;font-size:26px;font-weight:600;line-height:1.2;max-width:88%}}
.b.me{{align-self:flex-end;background:#6220AF;color:#fff;border-bottom-right-radius:8px}}
.b.bot{{background:#fff;border:2px solid #E2DBEA;width:80%;display:grid;gap:12px;border-bottom-left-radius:8px}}
.b.bot i,.lines i,.res i,.res b:empty{{display:block;height:14px;border-radius:7px;background:#E2DBEA;width:100%}}
.inp{{margin-top:auto;border:2px solid #E2DBEA;border-radius:999px;padding:16px 22px;color:#9C94A8;font-size:20px}}
.ig{{display:flex;align-items:center;gap:12px;font-size:20px}}.ig small{{color:#9C94A8;font-size:16px;margin-left:auto}}
.av{{width:44px;height:44px;border-radius:50%;background:#6220AF}}
.media{{height:420px;border-radius:20px;background:#6220AF;display:flex;align-items:flex-end;padding:28px;color:#fff;font-size:34px;font-weight:800;line-height:1.05;letter-spacing:-.03em}}
.ctaw{{display:flex;justify-content:space-between;background:#F4F1F8;border-radius:14px;padding:18px 20px;font-weight:700;font-size:20px}}
.lines{{display:grid;gap:12px}}
.reel{{background:#6220AF;color:#fff;justify-content:flex-end;padding:40px 30px}}
.rtext{{font-size:44px;font-weight:800;line-height:1.02;letter-spacing:-.03em;max-width:80%}}
.side{{position:absolute;right:22px;bottom:150px;display:grid;gap:30px;text-align:center;font-size:34px}}
.side small{{display:block;font-size:15px;font-weight:600}}
.prog{{height:6px;border-radius:3px;background:rgba(255,255,255,.35)}}.prog i{{display:block;height:100%;width:62%;background:#fff;border-radius:3px}}
.browser{{width:560px;background:#fff;border-radius:26px;padding:26px;display:grid;gap:22px;transform:rotate(-3deg);color:#150E1F;box-shadow:0 40px 80px rgba(0,0,0,.3)}}
.bbar{{display:flex;gap:9px}}.bbar i{{width:14px;height:14px;border-radius:50%;background:#E2DBEA}}
.q{{border:2px solid #E2DBEA;border-radius:999px;padding:16px 24px;font-size:24px;font-weight:600}}
.res{{display:grid;gap:8px;padding:18px;border-radius:16px}}.res small{{color:#5E5670;font-size:16px}}
.res b{{font-size:24px;color:#6220AF}}.res.hi{{background:#F1E9FF;outline:3px solid #6220AF}}
.chart{{width:520px;height:560px;background:{t["card"]};border-radius:32px;padding:40px;display:flex;align-items:flex-end;gap:18px;position:relative;box-shadow:0 30px 60px rgba(21,14,31,.12)}}
.chart i{{flex:1;background:#DCCEF3;border-radius:10px 10px 4px 4px}}.chart i:last-of-type{{background:#6220AF}}
.chart span{{position:absolute;left:40px;right:40px;top:36px;font-size:26px;font-weight:700;line-height:1.15;color:#150E1F}}
</style></head><body>
<div class="l"><div class="cat">{esc(meta.get("category", ""))}</div><h1>{frase}</h1>{dato}
<div class="foot"><img src="{LOGO.as_uri()}" alt=""><span>somosmdl.com/blog</span></div></div>
<div class="r">{motivo(t, meta, p)}</div></body></html>'''


def figura(meta, f):
    """Figura informativa en la paleta de la marca, fondo claro para que se lea dentro del texto."""
    tipo = f.get("tipo")
    titulo = esc(f.get("titulo", ""))
    fuente = f'<div class="src">Fuente: {esc(f["fuente"])}</div>' if f.get("fuente") else ""
    if tipo == "barras":
        datos = f["datos"]
        mx = max(float(v) for _, v in datos) or 1
        u = esc(f.get("unidad", ""))
        filas = "".join(
            f'<div class="row"><span class="lab">{esc(str(k))}</span><span class="track"><i style="width:{max(2, float(v) / mx * 100):.1f}%{";background:#6220AF" if float(v) == mx else ""}"></i></span>'
            f'<b>{str(v).replace(".", ",")}{u}</b></div>' for k, v in datos)
        cuerpo = f'<h2>{titulo}</h2><div class="bars">{filas}</div>'
    elif tipo == "dato":
        cuerpo = f'<div class="big">{esc(str(f["dato"]))}</div><p class="txt">{esc(f.get("texto", ""))}</p>'
    elif tipo == "pasos":
        cuerpo = f'<h2>{titulo}</h2><ol class="steps">' + "".join(f'<li><span>{i}</span><p>{esc(s)}</p></li>' for i, s in enumerate(f["pasos"], 1)) + "</ol>"
    elif tipo == "comparacion":
        a, b = f["columnas"]
        cuerpo = (f'<h2>{titulo}</h2><div class="cmp"><div class="h">{esc(a)}</div><div class="h hb">{esc(b)}</div>' +
                  "".join(f'<div>{esc(str(x))}</div><div class="cb">{esc(str(y))}</div>' for x, y in f["filas"]) + "</div>")
    else:
        raise SystemExit(f"figura de tipo desconocido: {tipo}")
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{fuentes()}
*{{box-sizing:border-box;margin:0}}
body{{width:1600px;background:#F7F5FA;color:#150E1F;font-family:P;padding:84px 96px 72px}}
.cat{{font:600 26px P;color:#6220AF;margin-bottom:22px}}
h2{{font-size:60px;font-weight:800;letter-spacing:-.04em;line-height:1.04;max-width:1250px;margin-bottom:56px}}
.bars{{display:grid;gap:26px}}
.row{{display:grid;grid-template-columns:380px 1fr 170px;align-items:center;gap:28px;font-size:28px}}
.lab{{font-weight:600;line-height:1.15}}.row b{{font-size:40px;font-weight:800;text-align:right;letter-spacing:-.03em}}
.track{{height:56px;background:#EAE3F3;border-radius:12px;overflow:hidden}}.track i{{display:block;height:100%;background:#A982E0;border-radius:12px}}
.big{{font-size:300px;font-weight:900;letter-spacing:-.07em;line-height:.85;color:#6220AF}}
.txt{{font-size:52px;font-weight:700;letter-spacing:-.03em;line-height:1.12;max-width:1250px;margin-top:40px}}
.steps{{list-style:none;padding:0;display:grid;gap:22px}}
.steps li{{display:grid;grid-template-columns:96px 1fr;gap:30px;align-items:center;background:#fff;border:2px solid #E2DBEA;border-radius:26px;padding:26px 34px}}
.steps span{{width:96px;height:96px;border-radius:50%;background:#6220AF;color:#fff;display:grid;place-items:center;font-size:44px;font-weight:800}}
.steps p{{font-size:34px;font-weight:600;line-height:1.2}}
.cmp{{display:grid;grid-template-columns:1fr 1fr;border-radius:26px;overflow:hidden;border:2px solid #E2DBEA;font-size:30px;line-height:1.25}}
.cmp div{{padding:26px 34px;background:#fff;border-top:2px solid #E2DBEA}}.cmp .h{{font-weight:800;font-size:34px;border-top:0;background:#EAE3F3}}
.cmp .hb{{background:#6220AF;color:#fff}}.cmp .cb{{background:#F1E9FF;font-weight:600}}
.foot{{margin-top:56px;display:flex;justify-content:space-between;align-items:center;font:500 22px P;color:#5E5670}}
.foot img{{height:34px;filter:brightness(0)}}
</style></head><body><div class="cat">{esc(meta.get("category", ""))}</div>{cuerpo}
<div class="foot">{fuente or "<span></span>"}<img src="{LOGO.as_uri()}" alt=""></div></body></html>'''


def chromium():
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome", "/opt/pw-browsers/chromium/chrome-linux/chrome"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None  # playwright usa su propio navegador si está instalado


def main(slugs):
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / ".imagenes-tmp.html"
    with sync_playwright() as pw:
        exe = chromium()
        br = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = br.new_page(viewport={"width": 1600, "height": 1000})

        def shot(doc, dest, full):
            tmp.write_text(doc, encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(dest), type="jpeg", quality=84, full_page=full)
            print("ok", dest.relative_to(ROOT))

        for slug in slugs:
            meta = leer(slug)
            shot(portada(slug, meta), OUT / f"{slug}.jpg", False)
            for i, f in enumerate(meta.get("figuras") or [], 1):
                pg.set_viewport_size({"width": 1600, "height": 600})
                shot(figura(meta, f), OUT / f"{slug}-{i}.jpg", True)
                pg.set_viewport_size({"width": 1600, "height": 1000})
        br.close()
    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--todas"]:
        args = [f.stem for f in sorted((ROOT / "content" / "blog").glob("*.md")) if not (OUT / f"{f.stem}.jpg").exists()]
    if not args:
        raise SystemExit(__doc__)
    main(args)
