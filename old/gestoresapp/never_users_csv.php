<?php
/* Exporta CSV con usuarios que AÚN no habían ingresado al cierre de una semana */
declare(strict_types=1);
date_default_timezone_set('America/Argentina/Cordoba');

/* MISMA SESIÓN */
session_name('GA_SESSID');
session_start();
if (empty($_SESSION['gestoresapp'])) { http_response_code(403); exit; }

require_once __DIR__.'/lib_ndjson.php';

function iter_safe(string $file): iterable {
  try { foreach (ndjson_iter($file) as $row) yield $row; }
  catch (Throwable $e) { return; }
}

/* Parámetros */
$courseid = isset($_GET['courseid']) ? (int)$_GET['courseid'] : 0;
$groupid  = isset($_GET['groupid'])  ? (int)$_GET['groupid']  : 0;
$weekEnd  = isset($_GET['end'])      ? (int)$_GET['end']      : 0;
if (!$courseid || !$groupid || !$weekEnd) { http_response_code(400); exit('Parámetros inválidos'); }

try {
  /* A) Usuarios del grupo */
  $groupUsers = [];
  foreach (iter_safe('groups_members.ndjson') as $gm) {
    if ((int)($gm['groupid'] ?? 0) === $groupid) $groupUsers[(int)($gm['userid'] ?? 0)] = true;
  }

  /* B) Inscriptos al curso */
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

  /* C) target */
  $targetSet = array_intersect_key($groupUsers, $courseUser);

  /* D) Último acceso por curso */
  $last = [];
  foreach (iter_safe('user_lastaccess.ndjson') as $la) {
    if ((int)($la['courseid'] ?? 0) !== $courseid) continue;
    $uid = (int)($la['userid'] ?? 0);
    if (!isset($targetSet[$uid])) continue;
    $t = (int)($la['timeaccess'] ?? 0);
    if (!isset($last[$uid]) || $t > $last[$uid]) $last[$uid] = $t;
  }

  /* E) IDs que aún no habían ingresado a esa fecha */
  $missing = [];
  foreach ($targetSet as $uid => $_) {
    if (!isset($last[$uid]) || $last[$uid] > $weekEnd) $missing[(int)$uid] = true;
  }

  /* F) CSV (UTF-8 con BOM) */
  if (function_exists('ob_get_level')) { while (ob_get_level() > 0) ob_end_clean(); }
  header('Content-Type: text/csv; charset=UTF-8');
  header('Content-Disposition: attachment; filename="usuarios_sin_ingreso_'.$courseid.'_'.$groupid.'_'.$weekEnd.'.csv"');

  $fh = fopen('php://output', 'w');
  fwrite($fh, "\xEF\xBB\xBF"); // BOM para Excel

  fputcsv($fh, ['Apellido','Nombre','Email','Usuario','ID']);

  foreach (iter_safe('users.ndjson') as $u) {
    $id = (int)($u['id'] ?? 0);
    if (!isset($missing[$id])) continue;
    fputcsv($fh, [
      $u['lastname']  ?? '',
      $u['firstname'] ?? '',
      $u['email']     ?? '',
      $u['username']  ?? '',
      $id
    ]);
  }
  fclose($fh);
  exit;
}
catch (Throwable $ex) {
  error_log('[never_users_csv] '.$ex->getMessage().' @ '.$ex->getFile().':'.$ex->getLine());
  http_response_code(500);
  echo "Error interno";
  exit;
}
