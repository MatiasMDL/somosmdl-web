<?php
// Recibe los formularios de somosmdl.com y las landings, y los manda a hola@somosmdl.com.
date_default_timezone_set('America/Argentina/Buenos_Aires');
$destino = 'hola@somosmdl.com';
$gracias = '/gracias-por-escribirnos/';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /#contacto', true, 303); exit; }

// Antispam: el campo "web" está oculto para personas; si viene lleno, es un robot.
// Y nadie completa un formulario en menos de 3 segundos.
$ts = isset($_POST['ts']) ? (int)$_POST['ts'] : 0;
if (!empty($_POST['web']) || ($ts && time() - (int)($ts / 1000) < 3)) { header('Location: ' . $gracias, true, 303); exit; }

function campo($k, $max = 500) {
  $v = isset($_POST[$k]) ? $_POST[$k] : '';
  if (is_array($v)) $v = implode(', ', $v);
  $v = trim(str_replace(["\r", "\0"], '', (string)$v));
  return mb_substr($v, 0, $max);
}

$nombre   = campo('nombre', 120);
$contacto = campo('contacto', 160);
$tel      = campo('tel', 60);
$email    = campo('email', 160);
$empresa  = campo('empresa', 160);
$rubro    = campo('rubro', 160);
$servicio = campo('servicio', 200);
$interes  = campo('interes', 300);
$inversion= campo('inversion', 100);
$msg      = campo('msg', 3000);
$pagina   = campo('pagina', 200);

if ($contacto !== '') {
  if (filter_var($contacto, FILTER_VALIDATE_EMAIL)) $email = $email ?: $contacto; else $tel = $tel ?: $contacto;
}
if ($nombre === '' || ($tel === '' && $email === '')) { header('Location: ' . ($pagina ?: '/') . '#contacto', true, 303); exit; }

$lineas = [
  'Nombre' => $nombre, 'WhatsApp / teléfono' => $tel, 'Email' => $email, 'Empresa' => $empresa,
  'Rubro' => $rubro, 'Le interesa' => trim($servicio . ($servicio && $interes ? ', ' : '') . $interes),
  'Inversión mensual aprox.' => $inversion, 'Mensaje' => $msg, 'Página' => $pagina,
];
$cuerpo = "Nueva consulta desde somosmdl.com\n\n";
foreach ($lineas as $k => $v) if ($v !== '') $cuerpo .= $k . ': ' . $v . "\n";
if ($tel !== '') {
  $num = preg_replace('/\D/', '', $tel);
  if (strlen($num) >= 8) $cuerpo .= "\nResponder por WhatsApp: https://wa.me/" . (strpos($num, '54') === 0 ? $num : '549' . ltrim($num, '0')) . "\n";
}
$cuerpo .= "\nFecha: " . date('d/m/Y H:i') . "\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n";

$asunto = 'Consulta web: ' . $nombre . ($empresa ? ' (' . $empresa . ')' : '');
$host = preg_replace('/^www\./', '', $_SERVER['HTTP_HOST'] ?? 'somosmdl.com');
$headers = [
  'From: MDL Web <no-reply@' . $host . '>',
  'Content-Type: text/plain; charset=UTF-8',
  'X-Mailer: somosmdl.com',
];
if ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)) $headers[] = 'Reply-To: ' . $email;

@mail($destino, '=?UTF-8?B?' . base64_encode($asunto) . '?=', $cuerpo, implode("\r\n", $headers), '-fno-reply@' . $host);
header('Location: ' . $gracias, true, 303);
exit;
