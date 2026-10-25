<?php
// Va en public_html/sincronizar-blog.php del servidor de MDL (no se publica desde dist/).
// GitHub Actions lo llama después de armar el sitio. Baja de la rama "publicado" del repo
// SOLO los archivos que cambiaron desde la última vez y los copia a public_html.
// Nunca borra nada y nunca escribe .htaccess, archivos .php, wp-content/ ni video/.
// No usa contraseñas: el repo es público y el contenido es el mismo que ya se ve en la web.

header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex');

$REPO = 'MatiasMDL/somosmdl-web';
$RAMA = 'publicado';
$WEB = __DIR__;
$PRIV = dirname(__DIR__);                       // /home/somosmdl, fuera de la web
$ESTADO = $PRIV . '/.sincronizar-blog.sha';
$LOG = $PRIV . '/sincronizar-blog.log';

function traer($url) {
    if (function_exists('curl_init')) {
        $c = curl_init($url);
        curl_setopt_array($c, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_TIMEOUT => 60,
            CURLOPT_USERAGENT => 'somosmdl-sync', CURLOPT_HTTPHEADER => ['Accept: application/vnd.github+json']]);
        $r = curl_exec($c);
        $code = curl_getinfo($c, CURLINFO_HTTP_CODE);
        curl_close($c);
        return ($r !== false && $code === 200) ? $r : null;
    }
    $ctx = stream_context_create(['http' => ['header' => "User-Agent: somosmdl-sync\r\nAccept: application/vnd.github+json\r\n", 'timeout' => 60]]);
    $r = @file_get_contents($url, false, $ctx);
    return $r === false ? null : $r;
}

function anotar($msg) {
    global $LOG;
    @file_put_contents($LOG, date('Y-m-d H:i:s') . ' ' . $msg . "\n", FILE_APPEND);
    echo $msg . "\n";
}

$lock = fopen($PRIV . '/.sincronizar-blog.lock', 'c');
if (!$lock || !flock($lock, LOCK_EX | LOCK_NB)) { echo "ocupado\n"; exit; }

$info = json_decode((string) traer("https://api.github.com/repos/$REPO/commits/$RAMA"), true);
if (empty($info['sha'])) { http_response_code(502); anotar('error: no pude leer GitHub'); exit; }
$nuevo = $info['sha'];
$viejo = is_file($ESTADO) ? trim(file_get_contents($ESTADO)) : '';

if ($viejo === '') $viejo = '8b4566e77dd4a90788ab3663875deb55e4ec052d';  // versión que estaba en vivo el 23/10 00:55
if ($viejo === $nuevo) { echo "al día\n"; exit; }

$cmp = json_decode((string) traer("https://api.github.com/repos/$REPO/compare/$viejo...$nuevo"), true);
if (!isset($cmp['files'])) { http_response_code(502); anotar('error: no pude comparar versiones'); exit; }

$n = 0;
foreach ($cmp['files'] as $f) {
    $ruta = $f['filename'];
    if (!in_array($f['status'], ['added', 'modified', 'renamed', 'changed'], true)) continue;
    if (!preg_match('#^[A-Za-z0-9._/-]+$#', $ruta) || strpos($ruta, '..') !== false) continue;
    if (preg_match('#(^|/)\.htaccess$|\.php$|^wp-content/|^video/|^\.nojekyll$#', $ruta)) continue;
    $datos = traer("https://raw.githubusercontent.com/$REPO/$nuevo/$ruta");
    if ($datos === null) { http_response_code(502); anotar("error bajando $ruta, reintento la próxima vez"); exit; }
    $destino = $WEB . '/' . $ruta;
    if (!is_dir(dirname($destino))) mkdir(dirname($destino), 0755, true);
    $tmp = $destino . '.tmp-sync';
    file_put_contents($tmp, $datos);
    rename($tmp, $destino);
    $n++;
}
file_put_contents($ESTADO, $nuevo);
anotar(substr($nuevo, 0, 7) . ": $n archivos actualizados");
