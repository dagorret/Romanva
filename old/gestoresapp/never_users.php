<?php
/* gestoresapp/never_users.php */
declare(strict_types=1);
date_default_timezone_set('America/Argentina/Cordoba');

session_name('GA_SESSID');
session_start();
if (empty($_SESSION['gestoresapp'])) { header('Location: ./index.php'); exit; }

require_once __DIR__.'/lib_ndjson.php';   // trae e() y ndjson_iter()
require_once __DIR__.'/inc_header.php';

function iter_safe(string $file): iterable {
  try { foreach (ndjson_iter($file) as $row) yield $row; } catch (Throwable $e) { return; }
}

$courseid = isset($_GET['courseid']) ? (int)$_GET['courseid'] : 0;
$groupid  = isset($_GET['groupid'])  ? (int)$_GET['groupid']  : 0;
$weekEnd  = isset($_GET['end'])      ? (int)$_GET['end']      : 0;
$fromStr  = $_GET['from'] ?? '';
$toStr    = $_GET['to']   ?? '';

if (!$courseid || !$groupid || !$weekEnd) { http_response_code(400); exit('Parámetros inválidos'); }

/* A) Usuarios del grupo */
$groupUsers=[];
foreach (iter_safe('groups_members.ndjson') as $gm) {
  if ((int)($gm['groupid'] ?? 0) === $groupid) $groupUsers[(int)($gm['userid'] ?? 0)]=true;
}

/* B) Inscriptos al curso */
$enrolToCourse=[]; foreach (iter_safe('enrol.ndjson') as $e) $enrolToCourse[(int)($e['id'] ?? 0)]=(int)($e['courseid'] ?? 0);
$courseUser=[];
foreach (iter_safe('user_enrolments.ndjson') as $ue) {
  $eid=(int)($ue['enrolid'] ?? 0); $uid=(int)($ue['userid'] ?? 0);
  if (($enrolToCourse[$eid] ?? 0) === $courseid) $courseUser[$uid]=true;
}

/* C) target = grupo ∩ inscriptos */
$targetSet = array_intersect_key($groupUsers, $courseUser);

/* D) Último acceso */
$last=[];
foreach (iter_safe('user_lastaccess.ndjson') as $la) {
  if ((int)($la['courseid'] ?? 0) !== $courseid) continue;
  $uid=(int)($la['userid'] ?? 0); if (!isset($targetSet[$uid])) continue;
  $t=(int)($la['timeaccess'] ?? 0); if (!isset($last[$uid]) || $t>$last[$uid]) $last[$uid]=$t;
}

/* E) Faltantes a la semana */
$missing=[];
foreach ($targetSet as $uid=>$_) if (!isset($last[$uid]) || $last[$uid] > $weekEnd) $missing[(int)$uid]=true;

/* F) Datos de usuarios */
$users=[];
foreach (iter_safe('users.ndjson') as $u) {
  $id=(int)($u['id'] ?? 0);
  if (!isset($missing[$id])) continue;
  $users[]=[
    'lastname'=>$u['lastname'] ?? '',
    'firstname'=>$u['firstname'] ?? '',
    'email'=>$u['email'] ?? '',
    'username'=>$u['username'] ?? '',
    'id'=>$id,
  ];
}
usort($users, fn($a,$b)=>[$a['lastname'],$a['firstname']] <=> [$b['lastname'],$b['firstname']]);

$weekLabel = date('Y-m-d', $weekEnd - 6*86400).' → '.date('Y-m-d', $weekEnd);
?>
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Usuarios sin acceso – <?= e($weekLabel) ?></title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:0;padding:24px;background:#f6f7f9}
.wrap{max-width:980px;margin:0 auto}
.card{background:#fff;border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
table{width:100%;border-collapse:collapse;margin-top:14px}
th,td{border:1px solid #e5e7eb;padding:8px;text-align:left}
th{background:#f3f4f6}
.muted{color:#6b7280;font-size:12px}
a.btn{display:inline-block;padding:8px 12px;border-radius:10px;background:#0d6efd;color:#fff;text-decoration:none;font-weight:700}
</style>
</head>
<body>
<div class="wrap">
  <?php ga_header('Usuarios sin acceso — '.e($weekLabel), [
    'Descargar CSV' => 'never_users_csv.php?courseid='.$courseid.'&groupid='.$groupid.'&end='.$weekEnd,
    'Volver al panel' => 'panel.php?courseid='.$courseid.'&groupid='.$groupid.'&from='.rawurlencode($fromStr).'&to='.rawurlencode($toStr),
  ]); ?>

  <div class="card">
    <p class="muted">Total: <strong><?= count($users) ?></strong></p>
    <table>
      <tr><th>Apellido</th><th>Nombre</th><th>Email</th><th>Usuario</th><th>ID</th></tr>
      <?php foreach ($users as $u): ?>
        <tr>
          <td><?= e($u['lastname']) ?></td>
          <td><?= e($u['firstname']) ?></td>
          <td><?= e($u['email']) ?></td>
          <td><?= e($u['username']) ?></td>
          <td><?= (int)$u['id'] ?></td>
        </tr>
      <?php endforeach; ?>
    </table>
    <?php if (!count($users)): ?><p class="muted">No hay usuarios en esta condición para esa semana.</p><?php endif; ?>
  </div>
</div>
</body>
</html>
