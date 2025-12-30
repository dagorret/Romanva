<?php
declare(strict_types=1);
define('EXPORT_DIR', '/var/lib/moodle-exports');

function e(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

/** Lee NDJSON línea a línea (RAM constante) */
function ndjson_iter(string $file): Generator {
  $path = rtrim(EXPORT_DIR, '/').'/'.$file;
  $fh = @fopen($path, 'r');
  if (!$fh) throw new RuntimeException("No puedo abrir $path");
  while (($line = fgets($fh)) !== false) {
    $line = trim($line);
    if ($line==='') continue;
    $row = json_decode($line, true);
    if (is_array($row)) yield $row;
  }
  fclose($fh);
}
