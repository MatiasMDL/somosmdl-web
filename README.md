# somosmdl.com

Sitio de MDL Marketing Digital en HTML estático, publicado en el servidor de MDL (hosting con Apache/LiteSpeed).

## Estructura

- `src/index.html`: home (fuente). `src/landings/`: páginas de servicio, cada una en `<ruta>/index.html`.
- `src/static/`: archivos que se copian tal cual (fuentes, imágenes, CSS, `robots.txt`, `.htaccess` con redirecciones 301, https sin www y encabezados).
- `content/blog/*.md`: notas del blog. Una nota con `date` futura se publica sola ese día con el próximo build; `draft: true` la oculta.
- `templates/page.html`: plantilla del blog y páginas secundarias.
- `build.py`: genera `dist/` con la home, notas, listado del blog, RSS, `sitemap.xml` y `llms.txt`.

## Publicar

- Armar: `pip install -r requirements.txt && python3 build.py` genera `dist/`.
- A mano: subir el contenido de `dist/` (incluido `.htaccess`) a `public_html`. Paso a paso en `../entrega/COMO-SUBIR-LA-WEB.md`.
- Automático: cada push a `main` arma el sitio en la rama `publicado` (`.github/workflows/subir-al-servidor.yml`); el servidor la baja cada 30 min con `servidor/sincronizar.sh` y copia solo lo que cambió (nunca borra ni toca `.htaccess`, `enviar.php`, `wp-content/`, `video/`).

## Blog automático

Ver `AUTOMATIZACION.md`.

## Local

`python3 build.py && python3 -m http.server -d dist 8000`
