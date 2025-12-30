<?php
const DB_HOST = 'localhost';
const DB_NAME = 'app3ecounrcedu_moodle';
const DB_USER = 'app3ecounrcedu_moodle';
const DB_PASS = 'Iphone#162024';

// Cinturón extra: si se ejecutara directo por error, no devuelve nada útil
if (php_sapi_name() !== 'cli' && basename($_SERVER['SCRIPT_NAME'] ?? '') === basename(__FILE__)) {
  http_response_code(403);
  exit;
}
