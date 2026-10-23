#!/usr/bin/env python3
"""Arma somosmdl.com en dist/: home, landings, blog, sitemap, RSS, llms.txt.

Uso: python3 build.py            (Cloudflare Pages: comando de build, carpeta de salida dist)
Notas nuevas: un archivo .md en content/blog/ con encabezado entre líneas ---.
"""
import datetime as dt
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import markdown
import yaml

import blog

ROOT = Path(__file__).resolve().parent
SRC, DIST, CONTENT = ROOT / "src", ROOT / "dist", ROOT / "content" / "blog"
SITE = "https://somosmdl.com"
ORG = {"@id": f"{SITE}/#org"}
AUTHOR = {"@type": "Person", "@id": f"{SITE}/#matias", "name": "Matías de la Llera",
          "jobTitle": "Fundador de MDL", "url": f"{SITE}/"}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
TODAY = dt.date.today()

# Servicios: fuente única para la home, el llms.txt y el sitemap
SERVICES = [
    ("/chatgpt/", "Anuncios en ChatGPT", "Campañas dentro de ChatGPT, como partner oficial de OpenAI."),
    ("/servicios/meta-ads/", "Publicidad en Meta Ads", "Campañas en Instagram y Facebook que llevan a WhatsApp, web o local."),
    ("/servicios/google-ads/", "Google Ads y YouTube", "Búsqueda, Display y YouTube con conversiones medidas."),
    ("/servicios/agentes-ia/", "Agentes de IA", "Asistentes que responden y califican consultas las 24 horas."),
    ("/social-media/", "Gestión de redes sociales", "Calendario, diseño, publicaciones y comunidad."),
    ("/webdesign/", "Diseño web", "Sitios y landing pages rápidos, pensados para convertir."),
    ("/servicios/seo-geo/", "SEO y GEO", "Posicionamiento en Google y en asistentes de IA como ChatGPT, Gemini y Perplexity."),
]


def fecha(d):
    return f"{d.day} {MESES[d.month - 1]} {d.year}"


def esc(s):
    return html.escape(str(s), quote=True)


def slugify(s):
    s = s.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def write(rel, text):
    p = DIST / rel.lstrip("/")
    if rel.endswith("/"):
        p = p / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# ---------- notas ----------
def load_posts():
    posts = []
    for f in sorted(CONTENT.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"{f.name}: falta el encabezado entre ---")
        meta, body = yaml.safe_load(m.group(1)), m.group(2)
        for k in ("title", "description", "date", "category"):
            if not meta.get(k):
                raise SystemExit(f"{f.name}: falta '{k}'")
        if meta.get("draft"):
            continue
        d = meta["date"] if isinstance(meta["date"], dt.date) else dt.date.fromisoformat(str(meta["date"]))
        if d > TODAY:
            continue  # programada: sale el día que corresponde
        upd = meta.get("updated") or d
        upd = upd if isinstance(upd, dt.date) else dt.date.fromisoformat(str(upd))
        url = meta.get("url") or f"/blog/{f.stem}/"
        if not meta.get("image") and (SRC / "static" / "img" / "blog" / f"{f.stem}.jpg").exists():
            meta["image"] = f"/img/blog/{f.stem}.jpg"
        posts.append({**meta, "slug": f.stem, "date": d, "updated": upd, "url": url,
                      "html": markdown.markdown(body, extensions=["tables", "smarty"]), "body": body,
                      "words": len(re.findall(r"\w+", body))})
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def page(title, desc, path, body, jsonld, robots="index,follow", og_type="website", head_extra=""):
    tpl = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")
    rep = {"{{TITLE}}": esc(title), "{{DESC}}": esc(desc), "{{CANONICAL}}": SITE + path,
           "{{ROBOTS}}": robots, "{{OG_TYPE}}": og_type, "{{OG_IMAGE}}": f"{SITE}/img/og-mdl.png",
           "{{JSONLD}}": json.dumps(jsonld, ensure_ascii=False), "{{BODY}}": body,
           "{{HEAD_EXTRA}}": head_extra, "{{YEAR}}": str(TODAY.year)}
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    return tpl


def crumbs(*items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


# post_card, build_post y build_blog viven en blog.py


def build_home(posts):
    s = (SRC / "index.html").read_text(encoding="utf-8")
    fonts = "".join(f'@font-face{{font-family:Poppins;font-weight:{w};font-display:swap;src:url(/fonts/poppins-latin-{w}-normal.woff2) format("woff2")}}'
                    for w in (400, 500, 600, 700, 800, 900))
    fonts += "".join(f'@font-face{{font-family:"JetBrains Mono";font-weight:{w};font-display:swap;src:url(/fonts/jetbrains-mono-latin-{w}-normal.woff2) format("woff2")}}'
                     for w in (400, 500))
    s = re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', "", s)
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    s = s.replace("<style>", "<style>" + fonts, 1)
    s = s.replace("{{LOGO_SRC}}", "/img/mdl-logo-blanco.png")
    s = s.replace("{{BENTO}}", bento()).replace("/*{{BENTO_CSS}}*/", (SRC / "partials" / "bento.css").read_text(encoding="utf-8"))
    s = s.replace("{{OAITEXT}}", (SRC / "partials" / "oai-text.svg").read_text()).replace("{{OAI}}", (SRC / "partials" / "oai.svg").read_text())
    if posts:  # las 3 notas más nuevas reemplazan los ejemplos
        cards = "".join(f'<a class="post rv" href="{p["url"]}">' + (f'<span class="pimg"><img src="{p["image"]}" alt="" width="1200" height="750" loading="lazy"></span>' if p.get("image") else "") + f'<span class="mono">{esc(p["category"])}</span><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><time datetime="{p["date"].isoformat()}">{fecha(p["date"])}</time></a>' for p in posts[:3])
        s = re.sub(r'<div class="posts">.*?</div>\s*<p class="note">.*?</p>', f'<div class="posts">{cards}</div>', s, flags=re.S)
    else:
        s = re.sub(r'<section class="blog".*?</section>\s*', "", s, flags=re.S)
    head, body = s.split("</style>", 1)
    doc = ('<!doctype html>\n<html lang="es-AR">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           '<meta name="theme-color" content="#0B0612">\n<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
           '<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">\n'
           '<link rel="alternate" type="application/rss+xml" title="Blog de MDL" href="/blog/feed.xml">\n'
           '<meta property="og:image" content="https://somosmdl.com/img/og-mdl.png">\n'
           '<link rel="preload" href="/fonts/poppins-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
           + head + "</style>\n</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n")
    write("/", doc)


def build_simple():
    priv = '''<div class="wrap"><div class="article"><header class="page-head"><span class="mono">Legal</span><h1>Política de privacidad</h1></header><div class="prose">
<p>MDL Marketing Digital (en adelante, MDL) usa los datos que nos dejás (nombre, teléfono, email, empresa y tu consulta) solo para responderte y, si lo pedís, enviarte una propuesta. No los vendemos ni los compartimos con terceros, salvo los proveedores que usamos para operar (por ejemplo, WhatsApp o el correo electrónico).</p>
<p>El sitio usa herramientas de medición (Google Analytics y el píxel de Meta) para saber cuántas personas lo visitan y qué anuncios funcionan. Podés bloquearlas desde la configuración de tu navegador.</p>
<p>Podés pedir acceso, corrección o eliminación de tus datos escribiendo a hola@somosmdl.com, conforme a la Ley 25.326 de Protección de los Datos Personales de la República Argentina. La Agencia de Acceso a la Información Pública es el órgano de control de esa ley.</p>
<p>Última actualización: octubre de 2026.</p></div></div></div>'''
    write("/politicas-de-privacidad/", page("Política de privacidad | MDL", "Cómo usa MDL los datos que dejás en somosmdl.com.",
                                             "/politicas-de-privacidad/", priv, {"@context": "https://schema.org", **crumbs(("Inicio", "/"), ("Privacidad", "/politicas-de-privacidad/"))}))
    thanks = '<div class="wrap"><header class="page-head"><span class="mono">Recibido</span><h1>Gracias por escribirnos.</h1><p>Te respondemos en el día por WhatsApp. Si es urgente, escribinos al +54 9 3489 56-5444.</p></header><a class="btn" href="/">Volver al inicio</a></div>'
    write("/gracias-por-escribirnos/", page("Gracias por escribirnos | MDL", "Recibimos tu consulta.", "/gracias-por-escribirnos/", thanks,
                                            {"@context": "https://schema.org", "@type": "WebPage"}, robots="noindex,follow"))
    nf = '<div class="wrap"><header class="page-head"><span class="mono">Error 404</span><h1>Esta página no existe.</h1><p>Puede que la hayamos movido con el rediseño. Probá desde el inicio o escribinos.</p></header><a class="btn" href="/">Ir al inicio</a></div>'
    (DIST / "404.html").write_text(page("Página no encontrada | MDL", "La página que buscás no existe.", "/404.html", nf,
                                        {"@context": "https://schema.org", "@type": "WebPage"}, robots="noindex"), encoding="utf-8")


def bento():
    """Grilla de casos: video si existe en src/static/video/casos/<slug>.mp4 (+ .jpg de portada), si no el chat animado."""
    cases = json.loads((SRC / "data" / "casos.json").read_text(encoding="utf-8"))
    vdir = SRC / "static" / "video" / "casos"
    tiles = []
    for c in cases:
        has = (vdir / f"{c['slug']}.mp4").exists()
        poster = f"/video/casos/{c['slug']}.jpg" if (vdir / f"{c['slug']}.jpg").exists() else ""
        if has:
            media = (f'<video muted loop playsinline preload="none" data-src="/video/casos/{c["slug"]}.mp4"'
                     + (f' poster="{poster}"' if poster else "") + ' aria-hidden="true"></video>')
        else:
            chat = "".join(f"<span>{esc(m)}</span>" for m in c["chat"] * 2)
            media = f'<div class="flow" aria-hidden="true"><div>{chat}</div></div>'
        tiles.append(f'<a class="tile {c["shape"]} {c["tone"]}{" has-media" if has else ""} rv" href="/casos/#{c["slug"]}">{media}'
                     f'<span class="go" aria-hidden="true">↗</span><span class="cap"><span class="m">{esc(c["metric"])}</span>'
                     f'<span class="l">{esc(c["label"])}</span><span class="n"><b>{esc(c["name"])}</b><span>{esc(c["services"])}</span></span></span></a>')
    js = ("<script>addEventListener('DOMContentLoaded',function(){var v=[].slice.call(document.querySelectorAll('.tile video,video.lazy-v'));if(!v.length)return;"
          "var io=new IntersectionObserver(function(es){es.forEach(function(e){var x=e.target;"
          "if(e.isIntersecting){if(!x.src)x.src=x.dataset.src;x.play().catch(function(){})}else x.pause()})},{rootMargin:'120px'});"
          "v.forEach(function(x){io.observe(x)})});</script>")
    return '<div class="bento">' + "".join(tiles) + "</div>" + js


def build_casos():
    body = (SRC / "pages" / "casos.html").read_text(encoding="utf-8").replace("{{BENTO}}", bento())
    names = re.findall(r'<article class="case-full" id="([^"]+)">.*?<h2>([^<]+)</h2>', body, re.S)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": f"{SITE}/casos/#page", "name": "Casos de éxito de MDL", "url": f"{SITE}/casos/",
         "inLanguage": "es-AR", "about": ORG,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": t, "url": f"{SITE}/casos/#{a}"} for i, (a, t) in enumerate(names)]}},
        crumbs(("Inicio", "/"), ("Casos", "/casos/"))]}
    write("/casos/", page("Casos de éxito | MDL Marketing Digital",
                          "Más de 16.700 conversaciones de WhatsApp para nuestros clientes, +40% de ventas con un agente de IA y más. Casos reales de MDL.",
                          "/casos/", body, ld,
                          head_extra="<style>" + (SRC / "partials" / "bento.css").read_text(encoding="utf-8") + ".bento{margin-bottom:12px}.bento-note{color:var(--muted);font-size:13px;margin:0 0 56px}</style>"))


def build_meta(posts):
    urls = [("/", TODAY, "1.0")] + [(u, TODAY, "0.9") for u, _, _ in SERVICES] + \
           [("/casos/", TODAY, "0.9"), ("/blog/", posts[0]["updated"] if posts else TODAY, "0.8"), ("/politicas-de-privacidad/", TODAY, "0.2")] + \
           [(p["url"], p["updated"], "0.7") for p in posts]
    write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{d.isoformat()}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls) + "</urlset>\n")
    svc = "\n".join(f"- [{n}]({SITE}{u}): {d}" for u, n, d in SERVICES)
    notes = "\n".join(f"- [{p['title']}]({SITE}{p['url']}): {p['description']}" for p in posts[:15])
    write("/llms.txt", f"""# MDL Marketing Digital

> Agencia de marketing digital de Argentina con más de 10 años de trayectoria, fundada por Matías de la Llera. Hace campañas en Meta, Google, YouTube y ChatGPT (partner oficial de OpenAI), gestión de redes, diseño web, SEO, GEO y agentes de IA para pymes e industrias. Clientes en toda Argentina.

Contacto: WhatsApp +54 9 3489 56-5444 · hola@somosmdl.com · Instagram @mdlagencia

## Servicios

{svc}

## Resultados

- Más de 16.700 conversaciones de WhatsApp generadas para clientes con Meta Ads (2023 a 2026).
- Cima Integral (salud, Escobar y Campana): 1.532 conversaciones de WhatsApp en 3 meses (jul a oct 2026).
- Reyes del Colchón (colchonería): +40% de ventas con un agente de IA que atiende y califica consultas 24/7, más un CRM.
- Sin Foto Multa (multas de tránsito, todo el país): 4.235 conversaciones de junio a octubre de 2026; Instagram verificado con 25,6 mil seguidores.
- Ifranet (internet): cliente desde 2023, costo por consulta un 65% menor que en 2024.
- Productos Válido (alimentos): producción audiovisual propia en la fábrica desde junio de 2026; las vistas por reel se multiplicaron por 2,8.
- Plus Aligners (ortodoncia invisible): reel de lanzamiento con 61,9 mil vistas.
- Wiber (fibra óptica, Mendoza): nueva identidad de marca y un reel de 130 mil vistas.
- De Contempo Muebles: reel de 66,2 mil vistas.
- Kualcos (laboratorio de medicina veterinaria): redes y marca.
- Supermix (hormigón e industria): web nueva, contenido en obra y 399 conversaciones en 2 meses.
- Casos completos: {SITE}/casos/

## Blog

- [Blog de MDL]({SITE}/blog/): notas sobre publicidad digital, redes, IA y negocios.
{notes}
""")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC / "static", DIST)
    shutil.copytree(SRC / "landings", DIST, dirs_exist_ok=True)
    posts = load_posts()
    build_home(posts)
    blog.B = sys.modules[__name__]  # el blog usa page(), write(), SERVICES, etc. de este archivo
    for p in posts:
        blog.build_post(p, posts)
    blog.build_blog(posts)
    build_simple()
    build_casos()
    build_meta(posts)
    print(f"OK: {len(posts)} notas, {sum(1 for _ in DIST.rglob('*.html'))} páginas en dist/")


if __name__ == "__main__":
    main()
