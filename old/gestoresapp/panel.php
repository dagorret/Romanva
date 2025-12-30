<?php
/* gestoresapp/panel.php */
declare(strict_types=1);
date_default_timezone_set('America/Argentina/Cordoba');

/* ===== MISMA SESIÓN QUE EN index.php ===== */
session_name('GA_SESSID');
session_start();

if (empty($_SESSION['gestoresapp'])) { header('Location: ./index.php'); exit; }
$user = $_SESSION['gestoresapp']['username'] ?? 'gestor';

/* NDJSON utils (define e() y ndjson_iter()) */
require __DIR__.'/lib_ndjson.php';
require __DIR__.'/inc_header.php';

/* ------------------------ Robustez y helpers ------------------------ */
$errors = [];
function iter_safe(string $file): iterable {
  try { foreach (ndjson_iter($file) as $row) yield $row; }
  catch (Throwable $e) { return; }
}

/* ------------------- Cursos (solo categoría “Grado” y últimos 12 meses) --------------- */

/* Cargar categorías (si existe el NDJSON) */
$cats = [];
foreach (iter_safe('categories.ndjson') as $cat) {
  $cats[(int)($cat['id'] ?? 0)] = $cat;
}

/* IDs raíz cuyo nombre sea “Grado” (case-insensitive) */
$gradoRoots = [];
foreach ($cats as $id => $c) {
  if (strcasecmp(trim($c['name'] ?? ''), 'Grado') === 0) { $gradoRoots[] = $id; }
}

/* Conjunto permitido: Grado + descendientes */
$allowedCat = [];
if ($gradoRoots) {
  foreach ($cats as $id => $c) {
    $path = (string)($c['path'] ?? ''); // ej: "/20/21"
    foreach ($gradoRoots as $gid) {
      if ($id === $gid || ($path !== '' && strpos($path, "/$gid/") !== false)) {
        $allowedCat[$id] = true;
        break;
      }
    }
  }
}

/* Parámetro de búsqueda simple por código (shortname) */
$courseSearch = trim((string)($_GET['q'] ?? ''));

/* Filtros por año / fecha:
   - Queremos mostrar SOLO cursos del último año (desde hoy hacia atrás 12 meses).
   - Si el nombre del curso tiene año (20xx) al inicio o al final, usamos ese año.
   - Si no tiene año en el nombre, usamos startdate (si existe). */
$yearPrefix      = '/^\s*(20\d{2})\s*[-–—]/u';     // "2025 - Derecho..."
$yearSuffixParen = '/\(\s*(20\d{2})\s*\)\s*$/u';  // "Derecho (2025)"

$currentYear = (int)date('Y');
$minYear     = $currentYear - 1;      // año actual y el anterior
$nowTs       = time();
$minStartTs  = strtotime('-1 year', $nowTs); // ventana de 12 meses hacia atrás

/* Cargar cursos aplicando filtros */
$courses = [];
foreach (iter_safe('courses.ndjson') as $r) {
  $cid   = (int)($r['id'] ?? 0);
  $catid = (int)($r['category'] ?? 0);

  // Solo categorías permitidas (si tenemos categories.ndjson)
  if ($cats && empty($allowedCat[$catid])) continue;

  $short = (string)($r['shortname'] ?? '');
  $full  = (string)($r['fullname']  ?? '');
  $start = (int)($r['startdate']   ?? 0);

  // Detectar año en el nombre (si lo hay)
  $courseYear = null;
  if (preg_match($yearPrefix, $full, $m) || preg_match($yearPrefix, $short, $m)) {
    $courseYear = (int)$m[1];
  } elseif (preg_match($yearSuffixParen, $full, $m) || preg_match($yearSuffixParen, $short, $m)) {
    $courseYear = (int)$m[1];
  }

  $skip = false;

  if ($courseYear !== null) {
    // Si el nombre tiene año, solo aceptamos cursos del año actual o el anterior
    if ($courseYear < $minYear || $courseYear > $currentYear) {
      $skip = true;
    }
  } elseif ($start > 0) {
    // Si no hay año en el nombre pero hay startdate, aplicamos ventana de 12 meses
    if ($start < $minStartTs || $start > $nowTs) {
      $skip = true;
    }
  }
  // Si no hay ni año ni startdate, los dejamos pasar para no perder cursos raros.

  // Filtro adicional: búsqueda por código (shortname) si se indicó algo en q
  if (!$skip && $courseSearch !== '') {
    if (stripos($short, $courseSearch) === false) {
      $skip = true;
    }
  }

  if ($skip) continue;

  $courses[$cid] = $r;
}

/* Orden por código corto */
uasort($courses, fn($a,$b)=>strcmp($a['shortname'] ?? '', $b['shortname'] ?? ''));


/* ------------------------- Parámetros ------------------------------ */
$courseid = isset($_GET['courseid']) ? (int)$_GET['courseid'] : 0;
$groupid  = isset($_GET['groupid'])  ? (int)$_GET['groupid']  : 0;
$fromStr  = $_GET['from'] ?? '';
$toStr    = $_GET['to']   ?? '';
$from = $fromStr ? strtotime($fromStr.' 00:00:00') : null;
$to   = $toStr   ? strtotime($toStr.' 23:59:59')   : null;

/* Rango por defecto: últimos 30 días */
if (!$from && !$to) {
  $to = time();
  $from = strtotime('-30 days', $to);
  $fromStr = date('Y-m-d', $from);
  $toStr   = date('Y-m-d', $to);
}
if ($from && $to && $from > $to) { [$from, $to] = [$to, $from]; }

/* ---------------------- Validaciones curso/grupo -------------------- */
if ($courseid && !isset($courses[$courseid])) { $errors[]='Curso inválido.'; $courseid=0; $groupid=0; }

function groups_for_course(int $cid): array {
  $out=[];
  foreach (iter_safe('groups.ndjson') as $g)
    if ((int)($g['courseid'] ?? 0) === $cid) $out[(int)$g['id']]=$g;
  uasort($out, fn($a,$b)=>strcmp($a['name']??'', $b['name']??''));
  return $out;
}
$groups = $courseid ? groups_for_course($courseid) : [];

if ($courseid && $groupid) {
  $g = $groups[$groupid] ?? null;
  if (!$g || (int)($g['courseid'] ?? 0) !== $courseid) { $errors[]='El grupo no pertenece al curso.'; $groupid=0; }
}

/* ------------------------ Cálculo del informe ---------------------- */
$report = null;
$weeklyEnds = []; // guardamos los timestamps de fin de semana para armar los links

if ($courseid && $groupid && $from && $to) {
  // A) usuarios del grupo
  $groupUsers=[];
  foreach (iter_safe('groups_members.ndjson') as $gm)
    if ((int)($gm['groupid'] ?? 0) === $groupid) $groupUsers[(int)($gm['userid'] ?? 0)]=true;

  // B) inscriptos al curso
  $enrolToCourse=[]; foreach (iter_safe('enrol.ndjson') as $e) $enrolToCourse[(int)($e['id'] ?? 0)]=(int)($e['courseid'] ?? 0);
  $courseUser=[];
  foreach (iter_safe('user_enrolments.ndjson') as $ue) {
    $eid=(int)($ue['enrolid'] ?? 0); $uid=(int)($ue['userid'] ?? 0);
    if (($enrolToCourse[$eid] ?? 0) === $courseid) $courseUser[$uid]=true;
  }

  // C) target = intersección
  $targetSet   = array_intersect_key($groupUsers, $courseUser);
  $targetUsers = array_keys($targetSet);
  $totalGroup  = count($targetUsers);

  // D) último acceso por curso
  $last=[];
  foreach (iter_safe('user_lastaccess.ndjson') as $la) {
    if ((int)($la['courseid'] ?? 0) !== $courseid) continue;
    $uid=(int)($la['userid'] ?? 0); if (!isset($targetSet[$uid])) continue;
    $t=(int)($la['timeaccess'] ?? 0); if (!isset($last[$uid]) || $t>$last[$uid]) $last[$uid]=$t;
  }

  // E) serie semanal
  $series=[];
  $weekStart = strtotime('monday this week', $from); if ($weekStart > $from) $weekStart -= 7*86400;
  for ($end = $weekStart + 6*86400 + 86399; $end <= $to; $end += 7*86400) {
    $stillNever=0;
    foreach ($targetUsers as $uid) if (!isset($last[$uid]) || $last[$uid] > $end) $stillNever++;
    $label = date('Y-m-d', $end-6*86400).' → '.date('Y-m-d', $end);
    $series[]=['week'=>$label,'never'=>$stillNever,'end_ts'=>$end];
    $weeklyEnds[] = $end;
  }

  $report=['series'=>$series,'total_group'=>$totalGroup];
}
?>
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Panel – Gestores</title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:0;padding:24px;background:#f6f7f9}
.wrap{max-width:980px;margin:0 auto}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
a.btn{display:inline-block;padding:10px 14px;border-radius:10px;background:#0d6efd;color:#fff;text-decoration:none;font-weight:700;text-align:center}
a.btn-sm{padding:6px 10px;font-size:12px;border-radius:8px}
.card{background:#fff;border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.grid{
  display:grid;
  grid-template-columns:1fr 1fr 1fr 1fr;
  column-gap:24px;  /* separación horizontal un poco mayor */
  row-gap:14px;     /* separación vertical suave */
}
label{font-weight:600;font-size:14px}
select,input[type=date],input[type=text]{width:100%;padding:8px 10px;border:1px solid #d0d4dc;border-radius:10px}
button{padding:10px 14px;border:0;border-radius:10px;background:#10b981;color:#fff;font-weight:700;cursor:pointer}
table{width:100%;border-collapse:collapse;margin-top:14px}
th,td{border:1px solid #e5e7eb;padding:8px;text-align:left}
th{background:#f3f4f6}
.muted{color:#6b7280;font-size:12px}
</style>
</head>
<body>
<div class="wrap">
  <?php ga_header('Panel de reportes', ['Volver al sitio' => '../index.php']); ?>
  
  <div class="card">
    <?php if (!empty($errors)): ?>
      <div style="background:#fee2e2;color:#991b1b;padding:10px;border-radius:10px;margin-bottom:10px">
        <?= e(implode(' · ', $errors)) ?>
      </div>
    <?php endif; ?>

    <form method="get">
      <div class="grid">
        <label>Curso
          <input type="text" name="q" placeholder="Buscar por código (ej: 300)" value="<?= e($courseSearch) ?>" autocomplete="off" style="margin-bottom:6px">
          <select name="courseid" onchange="this.form.submit()">
            <option value="">-- Elegir --</option>
            <?php foreach ($courses as $cid=>$c): ?>
              <option value="<?= $cid ?>" <?= $cid===$courseid?'selected':'' ?>>
                <?= e(($c['shortname']??'').' - '.($c['fullname']??'')) ?>
              </option>
            <?php endforeach; ?>
          </select>
        </label>

        <label>Grupo
          <select name="groupid" <?= $courseid? '' : 'disabled' ?>>
            <option value="">-- Elegir --</option>
            <?php if ($courseid): foreach ($groups as $gid=>$g): ?>
              <option value="<?= $gid ?>" <?= $gid===$groupid?'selected':'' ?>>
                <?= e($g['name']??'') ?>
              </option>
            <?php endforeach; endif; ?>
          </select>
        </label>

        <label>Desde
          <input type="date" name="from" value="<?= e($fromStr) ?>">
        </label>
        <label>Hasta
          <input type="date" name="to" value="<?= e($toStr) ?>">
        </label>
      </div>

      <div style="margin-top:12px">
        <button type="submit">Calcular</button>
        <?php if ($courseid && $groupid && $from && $to && file_exists(__DIR__.'/report_csv.php')): ?>
          <a class="btn" style="background:#6366f1"
             href="report_csv.php?courseid=<?= $courseid ?>&groupid=<?= $groupid ?>&from=<?= e($fromStr) ?>&to=<?= e($toStr) ?>">
             Descargar CSV
          </a>
        <?php endif; ?>
      </div>
    </form>

    <?php if ($report): ?>
      <h3 style="margin-top:16px">Integrantes del grupo que aún no ingresaron (por semana)</h3>
      <p class="muted">Total integrantes del grupo: <strong><?= (int)$report['total_group'] ?></strong></p>

      <table>
        <tr>
          <th>Semana</th>
          <th>Aún no ingresaron</th>
          <th>Usuarios</th>
        </tr>
        <?php foreach ($report['series'] as $row): ?>
          <tr>
            <td><?= e($row['week']) ?></td>
            <td><?= (int)$row['never'] ?></td>
            <td>
              <a class="btn btn-sm" style="background:#0ea5e9"
                 href="never_users.php?courseid=<?= $courseid ?>&groupid=<?= $groupid ?>&end=<?= (int)$row['end_ts'] ?>&from=<?= rawurlencode($fromStr) ?>&to=<?= rawurlencode($toStr) ?>">
                 Ver usuarios
              </a>
            </td>
          </tr>
        <?php endforeach; ?>
      </table>
      <p class="muted">Se usa <code>user_lastaccess</code> del curso; sin registro se considera “nunca ingresó”.</p>
    <?php elseif ($courseid && $groupid): ?>
      <p class="muted" style="margin-top:16px">Elegí un rango de fechas y presioná <strong>Calcular</strong>.</p>
    <?php endif; ?>
  </div>
</div>
</body>
</html>
