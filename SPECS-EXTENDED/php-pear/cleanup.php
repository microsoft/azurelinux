<?php 

#
# Usage: php cleanup.php /path/to/pear.conf /usr/share
# 
$file = $_SERVER['argv'][1];
$data = $_SERVER['argv'][2];

# Keys to be removed if exists
$remove = [
  'ext_dir',
  'http_proxy',
];
# Keys to be added
$add = [
  '__channels' => [
    'pecl.php.net' => [
      'doc_dir'  => "$data/doc/pecl",
      'test_dir' => "$data/tests/pecl",
    ]
  ]
];

$input = file_get_contents($file);
list($header, $config) = explode("\n", $input);
$config = unserialize($config);

foreach ($remove as $key) unset($config[$key]);
$config = array_merge($config, $add);
$config = serialize($config);

file_put_contents($file, "$header\n$config");

