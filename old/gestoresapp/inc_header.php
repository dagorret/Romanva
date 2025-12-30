<?php
declare(strict_types=1);

if (!function_exists('ga_header')) {
  function ga_header(string $title, array $right = []): void {
    $uname = htmlspecialchars($_SESSION['gestoresapp']['username'] ?? '', ENT_QUOTES, 'UTF-8');
    echo <<<HTML
<div class="ga-topbar">
  <div class="ga-brand">$title</div>
  <div class="ga-actions">
HTML;
    foreach ($right as $label => $href) {
      $L = htmlspecialchars($label, ENT_QUOTES, 'UTF-8');
      $H = htmlspecialchars($href,  ENT_QUOTES, 'UTF-8');
      echo '<a class="ga-btn" href="'.$H.'">'.$L.'</a>';
    }
    echo '<a class="ga-btn danger" href="index.php?logout=1">Cerrar sesión</a>';
    echo <<<HTML
  </div>
</div>
<style>
.ga-topbar{display:flex;justify-content:space-between;align-items:center;background:#fff;border-radius:16px;
  padding:14px 16px;box-shadow:0 10px 30px rgba(0,0,0,.08);margin-bottom:16px}
.ga-brand{font-size:28px;font-weight:800}
.ga-actions{display:flex;gap:10px}
.ga-btn{display:inline-block;padding:10px 14px;border-radius:10px;background:#0d6efd;color:#fff;text-decoration:none;font-weight:700}
.ga-btn.danger{background:#ef4444}
</style>
HTML;
  }
}
