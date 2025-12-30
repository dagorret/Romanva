<?php
declare(strict_types=1);
date_default_timezone_set('America/Argentina/Cordoba');

/* MISMA SESIÓN QUE EL RESTO */
session_name('GA_SESSID');
session_start();
if (empty($_SESSION['gestoresapp'])) { http_response_code(403); exit; }

require_once __DIR__.'/lib_ndjson.php';

/* Iterador seguro (si falta un NDJSON, devolvemos vacío) */
function iter_safe(string $f): iterable {
  try { foreach (ndjson_iter($f) as $r) yield $r; } catch (Throwable $e) { return; }
}

/* Parámetros */
$courseid = isset($_GET['courseid']) ? (int)$_GET['courseid'] : 0;
$groupid  = isset($_GET['groupid'])  ? (int)$_GET['groupid']  : 0;
$fromStr  = $_GET['from'] ?? '';
$toStr    = $_GET['to']   ?? '';

$from = $fromStr ? strtotime($fromStr.' 00:00:00') : null;
$to   = $toStr   ? strtotime($toStr.' 23:59:59')   : null;

if (!$courseid || !$groupid || !$from || !$to) { http_response_code(400); exit('Parámetros inválidos'); }
if ($from > $to) [$from, $to] = [$to, $from];

/* A) Usuarios del grupo */
$groupUsers = [];
foreach (iter_safe('groups_members.ndjson') as $gm) {
  if ((int)($gm['groupid'] ?? 0) === $groupid) $groupUsers[(int)($gm['userid'] ?? 0)] = true;
}

/* B) Inscriptos del curso (enrol ↔ user_enrolments) */
$enrolToCourse = [];
foreach (iter_safe('enrol.ndjson') as $e) {
  $enrolToCourse[(int)($e['id'] ?? 0)] = (int)($e['courseid'] ?? 0);
}
$courseUser = [];
foreach (iter_safe('user_enrolments.ndjson') as $ue) {
  $eid = (int)($ue['enrolid'] ?? 0);
  $uid = (int)($ue['userid'] ?? 0);
  if (($enrolToCourse[$eid] ?? 0) === $courseid) $courseUser[$uid] = true;
}

/* C) target = grupo ∩ inscriptos */
$targetSet   = array_intersect_key($groupUsers, $courseUser);
$targetUsers = array_keys($targetSet);

/* D) Último acceso por curso */
$last = [];
foreach (iter_safe('user_lastaccess.ndjson') as $la) {
  if ((int)($la['courseid'] ?? 0) !== $courseid) continue;
  $uid = (int)($la['userid'] ?? 0);
  if (!isset($targetSet[$uid])) continue;
  $t = (int)($la['timeaccess'] ?? 0);
  if (!isset($last[$uid]) || $t > $last[$uid]) $last[$uid] = $t;
}

/* E) Salida CSV (UTF-8 con BOM) */
if (function_exists('ob_get_level')) { while (ob_get_level() > 0) ob_end_clean(); }
header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="reporte_semanal_'.$courseid.'_'.$groupid.'.csv"');

$fh = fopen('php://output', 'w');
fwrite($fh, "\xEF\xBB\xBF"); // BOM para Excel

fputcsv($fh, ['Semana','Aún no habían ingresado']);

$weekStart = strtotime('monday this week', $from);
if ($weekStart > $from) $weekStart -= 7*86400;

for ($end = $weekStart + 6*86400 + 86399; $end <= $to; $end += 7*86400) {
  $stillNever = 0;
  foreach ($targetUsers as $uid) {
    if (!isset($last[$uid]) || $last[$uid] > $end) $stillNever++;
  }
  $label = date('Y-m-d', $end - 6*86400).'→'.date('Y-m-d', $end);
  fputcsv($fh, [$label, $stillNever]);
}

fclose($fh);
exit;
