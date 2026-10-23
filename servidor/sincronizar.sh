#!/bin/bash
# Corre en el servidor de MDL por cron cada 30 minutos.
# Baja la rama "publicado" de GitHub y copia a public_html SOLO los archivos que cambiaron desde la última vez.
# Nunca borra nada del servidor y nunca toca .htaccess, enviar.php, wp-content/ ni video/ (eso se sube a mano).
set -euo pipefail
REPO="$HOME/somosmdl-publicado"
WEB="$HOME/public_html"
LOG="$HOME/sincronizar-blog.log"
exec 9>"$HOME/.sincronizar.lock"; flock -n 9 || exit 0

cd "$REPO"
antes=$(git rev-parse HEAD)
git fetch -q origin publicado
despues=$(git rev-parse origin/publicado)
[ "$antes" = "$despues" ] && exit 0
git reset -q --hard "$despues"

n=0
while IFS= read -r f; do
  case "$f" in
    .htaccess|enviar.php|wp-content/*|video/*|.nojekyll) continue ;;
  esac
  mkdir -p "$WEB/$(dirname "$f")"
  cp -p "$f" "$WEB/$f"
  n=$((n+1))
done < <(git diff --name-only --diff-filter=AMR "$antes" "$despues")
echo "$(date '+%F %T') ${despues:0:7}: $n archivos actualizados" >> "$LOG"
