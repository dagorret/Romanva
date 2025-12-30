<?php
/* gestoresapp/index.php */
declare(strict_types=1);
date_default_timezone_set('America/Argentina/Cordoba');

/* ===== Sesión endurecida (USAR SIEMPRE ESTE NOMBRE) ===== */
session_name('GA_SESSID');
$secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off');

session_set_cookie_params([
  'lifetime' => 0,
  'path'     => '/gestoresapp',
  'domain'   => '',
  'secure'   => $secure,
  'httponly' => true,
  'samesite' => 'Lax',
]);

session_start();

/* Logout */
if (isset($_GET['logout'])) {
  $_SESSION = [];

  if (ini_get('session.use_cookies')) {
    $p = session_get_cookie_params();
    setcookie(
      session_name(),
      '',
      time() - 42000,
      $p['path'],
      $p['domain'],
      $p['secure'],
      $p['httponly']
    );
  }

  session_destroy();
  header('Location: ./');
  exit;
}

/* Si ya está logueado, ir directo al panel */
if (!empty($_SESSION['gestoresapp'])) {
  header('Location: ./panel.php');
  exit;
}

/* ===== Credenciales DB seguras ===== */
require '/etc/gestoresapp/_private/config.php';

function cfg_pick(array $names): ?string {
  foreach ($names as $k) {
    if (defined($k)) {
      return (string) constant($k);
    }
    if (isset($GLOBALS[$k])) {
      return (string) $GLOBALS[$k];
    }
  }
  return null;
}

function db(): PDO {
  static $pdo = null;

  if ($pdo === null) {
    $dsn = 'mysql:host=' . cfg_pick(['DB_HOST', 'dbhost'])
         . ';dbname=' . cfg_pick(['DB_NAME', 'dbname'])
         . ';charset=utf8mb4';

    $pdo = new PDO(
      $dsn,
      cfg_pick(['DB_USER', 'dbuser']),
      cfg_pick(['DB_PASS', 'dbpass']),
      [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
      ]
    );
  }

  return $pdo;
}

/* CSRF mínimo */
if (empty($_SESSION['csrf'])) {
  $_SESSION['csrf'] = bin2hex(random_bytes(32));
}

/* Procesar login */
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  header('Cache-Control: no-store, no-cache, must-revalidate');
  header('Pragma: no-cache');

  $csrf = $_POST['csrf'] ?? '';
  $user = trim((string) ($_POST['username'] ?? ''));
  $pass = (string) ($_POST['password'] ?? '');

  if (!hash_equals($_SESSION['csrf'], $csrf)) {
    $error = 'Token inválido. Recargá la página.';
  } elseif ($user === '' || $pass === '') {
    $error = 'Completá usuario y contraseña.';
  } else {
    // AJUSTAR tabla/campos si hiciera falta
    $st = db()->prepare(
      'SELECT id, username, pass_hash, activo
       FROM gestores_login
       WHERE username = :u
       LIMIT 1'
    );
    $st->execute([':u' => $user]);
    $row = $st->fetch();

    if (!$row || (int) $row['activo'] !== 1) {
      $error = 'Usuario o contraseña inválidos.';
    } elseif (!password_verify($pass, $row['pass_hash'])) {
      $error = 'Usuario o contraseña inválidos.';
    } else {
      session_regenerate_id(true);
      $_SESSION['gestoresapp'] = [
        'id'       => (int) $row['id'],
        'username' => $row['username'],
        'login_at' => time(),
      ];

      db()->prepare(
        'UPDATE gestores_login
         SET last_login_at = NOW()
         WHERE id = :id'
      )->execute([':id' => $row['id']]);

      // ⇠ redirección inmediata al panel
      header('Location: ./panel.php');
      exit;
    }
  }
}

function h(string $s): string {
  return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}
?>
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>Gestores de Aprendizaje – Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
      :root { color-scheme: light dark; }

      body {
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        margin: 0;
        display: grid;
        place-items: center;
        min-height: 100dvh;
        background: #f6f7f9;
        color: #111827;
      }

      .card {
        background: #fff;
        max-width: 420px;
        width: 100%;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
      }

      h1 {
        font-size: 20px;
        margin: 0 0 14px;
        color: #111827;
      }

      .row {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 12px;
      }

      label {
        font-weight: 600;
        color: #111827;
      }

      input {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #d0d4dc;
        border-radius: 10px;
        font-size: 14px;
        background-color: #fff;
        box-sizing: border-box;
        min-height: 44px;
        color: #111827;
      }

      button {
        width: 100%;
        padding: 12px 14px;
        border: 0;
        border-radius: 10px;
        background: #0d6efd;
        color: #fff;
        font-weight: 700;
        cursor: pointer;
      }

      .error {
        background: #ffe4e6;
        color: #b00020;
        padding: 10px 12px;
        border-radius: 10px;
        margin-bottom: 10px;
      }

      .muted {
        color: #374151;
        font-size: 13px;
      }

      /* ===== Responsive ===== */
      @media (max-width: 560px) {
        body { padding: 16px; }
        .card { padding: 20px; border-radius: 14px; }
        h1 { font-size: 18px; margin-bottom: 12px; }
        input, button { font-size: 16px; }
      }

      @media (max-width: 360px) {
        .card { padding: 16px; border-radius: 12px; }
        h1 { font-size: 16px; }
      }
    </style>
  </head>

  <body>
    <div class="card">
      <h1>Ingreso – Gestores de Aprendizaje</h1>

      <?php if ($error): ?>
        <div class="error"><?= h($error) ?></div>
      <?php endif; ?>

      <form method="post" action="">
        <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">

        <div class="row">
          <label for="username">Usuario</label>
          <input id="username" name="username" autocomplete="username" required>
        </div>

        <div class="row">
          <label for="password">Contraseña</label>
          <input id="password" type="password" name="password" autocomplete="current-password" required>
        </div>

        <button type="submit">Ingresar</button>
      </form>

      <p class="muted" style="margin-top: 10px;">
        La cookie de sesión se emite solo para <code>/gestoresapp</code>.
      </p>
    </div>
  </body>
</html>
