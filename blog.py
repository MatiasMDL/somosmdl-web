"""Páginas del blog: listado (/blog/), cada nota y el RSS. Lo llama build.py (B = build).

Estilos en src/static/css/blog.css. Imágenes de las notas: scripts/imagenes.py.
"""
import datetime as dt
import re

import markdown

B = None  # build.py se asigna acá antes de usar el módulo

CAT_IDS = {"Inteligencia artificial": "ia", "Publicidad digital": "publicidad", "Redes sociales": "redes",
           "Negocios y pymes": "negocios", "Web y SEO": "web"}
CSS = '<link rel="stylesheet" href="/css/blog.css">'


def minutos(p):
    return max(2, round(p["words"] / 220))


def render(body):
    """Markdown a HTML con ids en los subtítulos (para el índice) e imágenes como figuras con epígrafe."""
    md = markdown.Markdown(extensions=["tables", "smarty", "toc"],
                           extension_configs={"toc": {"slugify": lambda s, sep: B.slugify(s), "toc_depth": "2"}})
    html = md.convert(body)
    toc = [(t["id"], t["name"]) for t in md.toc_tokens]

    def fig(m):
        tag = m.group(1)
        alt = re.search(r'alt="([^"]*)"', tag)
        src = re.search(r'src="([^"]*)"', tag).group(1)
        title = re.search(r'title="([^"]*)"', tag)
        cap = f"<figcaption>{title.group(1)}</figcaption>" if title else ""
        return (f'<figure class="fig"><img src="{src}" alt="{alt.group(1) if alt else ""}" loading="lazy" decoding="async">'
                f"{cap}</figure>")
    html = re.sub(r"<p>(<img [^>]+>)</p>", fig, html)
    html = html.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    return html, toc


def cover(p, cls, eager=False, sizes="(max-width: 900px) 100vw, 33vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    if p.get("image"):
        return f'<span class="{cls}"><img src="{p["image"]}" alt="" width="1600" height="1000" sizes="{sizes}" {load}></span>'
    return f'<span class="{cls} {cls}--none" aria-hidden="true"><b>{B.esc(p["category"])}</b></span>'


def card(p, tag="h3"):
    return (f'<a class="bcard" href="{p["url"]}" data-cat="{CAT_IDS.get(p["category"], "otros")}">'
            f'{cover(p, "bimg")}'
            f'<span class="bmeta"><span class="chip">{B.esc(p["category"])}</span><span>{minutos(p)} min</span></span>'
            f'<{tag}>{B.esc(p["title"])}</{tag}><p>{B.esc(p["description"])}</p>'
            f'<time datetime="{p["date"].isoformat()}">{B.fecha(p["date"])}</time></a>')


def autor_mini(p):
    return (f'<span class="by"><span class="av" aria-hidden="true">MdL</span><span><b>Matías de la Llera</b>'
            f'<small><time datetime="{p["date"].isoformat()}">{B.fecha(p["date"])}</time> · {minutos(p)} min de lectura</small></span></span>')


def build_post(p, posts):
    esc = B.esc
    html, toc = render(p["body"])
    sources = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["title"])}</a></li>'
                      for s in p.get("sources") or [])
    related = ([q for q in posts if q is not p and q["category"] == p["category"]] +
               [q for q in posts if q is not p and q["category"] != p["category"]])[:3]
    svc = next((s for s in B.SERVICES if s[0] == p.get("service")), None)
    url = B.SITE + p["url"]
    share_txt = f'{p["title"]} {url}'
    toc_html = ("<nav class=\"toc\" aria-label=\"En esta nota\"><b>En esta nota</b><ol>" +
                "".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in toc) + "</ol></nav>") if len(toc) >= 3 else ""
    upd = (f'<p class="upd">Actualizado el <time datetime="{p["updated"].isoformat()}">{B.fecha(p["updated"])}</time></p>'
           if p["updated"] != p["date"] else "")
    body = f'''<div class="readbar" aria-hidden="true"><i></i></div>
<article class="note">
<header class="wrap nhead">
<nav class="crumbs" aria-label="Ruta"><a href="/blog/">Blog</a><span aria-hidden="true">/</span><a href="/blog/#{CAT_IDS.get(p["category"], "")}">{esc(p["category"])}</a></nav>
<h1>{esc(p["title"])}</h1>
<p class="dek">{esc(p["description"])}</p>
{autor_mini(p)}
</header>
<div class="wrap">{cover(p, "ncover", eager=True, sizes="(max-width: 1180px) 100vw, 1140px")}</div>
<div class="wrap nbody">
<aside class="nside">{toc_html}
<div class="share"><b>Compartir</b>
<a href="https://wa.me/?text={esc(B.quote(share_txt))}" target="_blank" rel="noopener">WhatsApp</a>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={esc(B.quote(url))}" target="_blank" rel="noopener">LinkedIn</a>
<button type="button" class="copy" data-url="{esc(url)}">Copiar enlace</button></div></aside>
<div class="ncol">
{f'<div class="tldr"><strong>En corto</strong><p>{esc(p["tldr"])}</p></div>' if p.get("tldr") else ""}
<div class="prose">{html}</div>
{upd}
{f'<div class="sources"><b>Fuentes</b><ol>{sources}</ol></div>' if sources else ""}
<div class="author"><span class="av" aria-hidden="true">MdL</span><div><b>Matías de la Llera</b><p>Fundador de MDL. Hace más de 10 años que arma campañas, redes y webs para pymes e industrias de Argentina. Escribe acá lo que ve funcionar en las cuentas que maneja.</p></div></div>
<div class="cta-box"><span class="kick">{esc(svc[1]) if svc else "MDL Marketing Digital"}</span><h2>¿Querés aplicarlo en tu negocio?</h2><p>Escribinos y te hacemos un diagnóstico gratis de tus redes y campañas.</p>
<div class="cta-row"><a class="btn" href="https://wa.me/5493489565444?text={esc(B.quote("Hola, leí la nota: " + p["title"]))}" target="_blank" rel="noopener">Escribinos por WhatsApp</a>{f'<a class="btn ghost" href="{svc[0]}">Ver el servicio</a>' if svc else ""}</div></div>
</div></div>
{f'<section class="wrap more"><h2>Seguí leyendo</h2><div class="bgrid">{"".join(card(q) for q in related)}</div></section>' if related else ""}
</article>
<script>(function(){{var b=document.querySelector('.readbar i'),a=document.querySelector('.prose');
function f(){{var r=a.getBoundingClientRect(),h=r.height-innerHeight*.6,v=Math.min(1,Math.max(0,-r.top/(h>0?h:1)));b.style.transform='scaleX('+v+')'}}
addEventListener('scroll',f,{{passive:true}});f();
var c=document.querySelector('.copy');if(c)c.addEventListener('click',function(){{var u=c.dataset.url;
(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){{c.textContent='Enlace copiado'}},function(){{prompt('Copiá el enlace',u)}})}});
var ls=[].slice.call(document.querySelectorAll('.toc a'));if(ls.length&&'IntersectionObserver'in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting)ls.forEach(function(l){{l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)}})}})}},{{rootMargin:'0px 0px -70% 0px'}});
ls.forEach(function(l){{var t=document.getElementById(l.getAttribute('href').slice(1));if(t)io.observe(t)}})}}}})();</script>'''
    img = B.SITE + (p.get("image") or "/img/og-mdl.png")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": url + "#post", "headline": p["title"],
         "description": p["description"], "datePublished": p["date"].isoformat(),
         "dateModified": p["updated"].isoformat(), "inLanguage": "es-AR", "articleSection": p["category"],
         "author": B.AUTHOR, "publisher": B.ORG, "mainEntityOfPage": url,
         "image": {"@type": "ImageObject", "url": img, "width": 1600, "height": 1000}, "wordCount": p["words"],
         "timeRequired": f"PT{minutos(p)}M",
         **({"abstract": p["tldr"]} if p.get("tldr") else {}),
         **({"citation": [s["url"] for s in p["sources"]]} if p.get("sources") else {})},
        B.crumbs(("Inicio", "/"), ("Blog", "/blog/"), (p["title"], p["url"]))]}
    head = CSS + (f'\n<meta property="article:published_time" content="{p["date"].isoformat()}">'
                  f'\n<meta property="article:modified_time" content="{p["updated"].isoformat()}">'
                  f'\n<meta property="article:section" content="{esc(p["category"])}">')
    doc = B.page(f'{p["title"]} | MDL', p["description"], p["url"], body, ld, og_type="article", head_extra=head)
    if p.get("image"):
        doc = doc.replace(f'content="{B.SITE}/img/og-mdl.png"', f'content="{img}"', 1)
    B.write(p["url"], doc)


def build_blog(posts):
    esc = B.esc
    if posts:
        top, rest = posts[0], posts[1:]
        cats = [c for c in CAT_IDS if any(q["category"] == c for q in posts)]
        chips = '<a href="#todas" data-f="todas" aria-current="true">Todas</a>' + "".join(
            f'<a href="#{CAT_IDS[c]}" data-f="{CAT_IDS[c]}">{esc(c)}</a>' for c in cats)
        feat = (f'<a class="feat" href="{top["url"]}" data-cat="{CAT_IDS.get(top["category"], "otros")}">'
                f'{cover(top, "fimg", eager=True, sizes="(max-width: 900px) 100vw, 60vw")}'
                f'<span class="ftxt"><span class="bmeta"><span class="chip">{esc(top["category"])}</span><span>Lo último</span></span>'
                f'<h2>{esc(top["title"])}</h2><p>{esc(top.get("tldr") or top["description"])}</p>{autor_mini(top)}</span></a>')
        grid = f'<div class="bgrid" id="notas">{"".join(card(q, "h2") for q in rest)}</div>' if rest else ""
        content = f'''<nav class="cats" aria-label="Temas">{chips}</nav>{feat}{grid}
<p class="empty" hidden>Todavía no hay notas de este tema.</p>'''
    else:
        content = '<p class="empty">Las primeras notas salen esta semana. Mientras tanto, escribinos por WhatsApp.</p>'
    body = f'''<div class="wrap blog">
<header class="bhead"><span class="kick">Notas nuevas lunes, miércoles y viernes</span>
<h1>Lo que está cambiando en marketing, contado para los que venden.</h1>
<p>Publicidad digital, redes, inteligencia artificial y negocios, con pasos concretos para pymes de Argentina. Escribe Matías de la Llera.</p>
<a class="rss" href="/blog/feed.xml">Seguir por RSS</a></header>
{content}
<aside class="bcta"><div><h2>¿Te sirve lo que leés?</h2><p>Lo aplicamos en tu negocio. Diagnóstico gratis de tus redes y campañas.</p></div><a class="btn" href="https://wa.me/5493489565444?text=Hola%2C%20vengo%20del%20blog" target="_blank" rel="noopener">Escribinos por WhatsApp</a></aside>
</div>
<script>(function(){{var cs=[].slice.call(document.querySelectorAll('.cats a')),it=[].slice.call(document.querySelectorAll('.feat,.bcard')),em=document.querySelector('.empty[hidden],.empty');
function go(f){{var n=0;cs.forEach(function(c){{c.toggleAttribute('aria-current',c.dataset.f===f)}});
it.forEach(function(x){{var s=f==='todas'||x.dataset.cat===f;x.hidden=!s;if(s)n++}});if(em&&cs.length)em.hidden=n>0}}
cs.forEach(function(c){{c.addEventListener('click',function(e){{e.preventDefault();go(c.dataset.f);history.replaceState(null,'','#'+c.dataset.f)}})}});
var h=location.hash.slice(1);if(h&&cs.some(function(c){{return c.dataset.f===h}}))go(h)}})();</script>'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": f"{B.SITE}/blog/#blog", "name": "Blog de MDL", "url": f"{B.SITE}/blog/",
         "inLanguage": "es-AR", "publisher": B.ORG, "author": B.AUTHOR,
         "blogPost": [{"@id": B.SITE + p["url"] + "#post"} for p in posts[:20]]},
        B.crumbs(("Inicio", "/"), ("Blog", "/blog/"))]}
    B.write("/blog/", B.page("Blog de marketing digital e IA para pymes | MDL",
                             "Novedades de publicidad digital, redes sociales, inteligencia artificial y negocios, con pasos concretos para pymes de Argentina.",
                             "/blog/", body, ld, head_extra=CSS))
    items = "".join(f'''<item><title>{esc(p["title"])}</title><link>{B.SITE}{p["url"]}</link><guid>{B.SITE}{p["url"]}</guid>
<pubDate>{dt.datetime.combine(p["date"], dt.time(9)).strftime("%a, %d %b %Y %H:%M:%S -0300")}</pubDate><category>{esc(p["category"])}</category><description>{esc(p["description"])}</description>{f'<enclosure url="{B.SITE}{p["image"]}" type="image/jpeg" length="0"/>' if p.get("image") else ""}</item>''' for p in posts[:30])
    B.write("/blog/feed.xml", f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Blog de MDL</title><link>{B.SITE}/blog/</link><description>Marketing, publicidad e IA para vender más.</description><language>es-AR</language>{items}</channel></rss>''')
