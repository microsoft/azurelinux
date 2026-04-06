<?php

error_reporting(1803);

if (ini_get('date.timezone') === '') {
    date_default_timezone_set('UTC');
}

$pear_dir = dirname(__FILE__);
ini_set('include_path', '');
if (function_exists('mb_internal_encoding')) {
    mb_internal_encoding('ASCII');
}
set_time_limit(0);
include_once 'PEAR.php';
include_once 'PEAR/Installer.php';
include_once 'PEAR/Registry.php';
include_once 'PEAR/PackageFile.php';
include_once 'PEAR/Downloader/Package.php';
include_once 'PEAR/Frontend.php';
$a = true;
if (!PEAR::loadExtension('xml')) {
    $a = false;
    echo "[PEAR] xml extension is required\n";
}
if (!PEAR::loadExtension('pcre')) {
    $a = false;
    echo "[PEAR] pcre extension is required\n";
}
if (!$a) {
    return -1;
}

$force = false;
$install_files = array();
array_shift($argv);
$debug = false;
for ($i = 0; $i < sizeof($argv); $i++) {
    $arg = $argv[$i];
    $bn = basename($arg);
    if (preg_match('/package-(.*)\.xml$/', $bn, $matches) ||
        preg_match('/([A-Za-z0-9_:]+)-.*\.(tar|tgz)$/', $bn, $matches)) {
        $install_files[$matches[1]] = $arg;
    } elseif ($arg == '-a' || $arg == '--cache') {
        $cache_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '--force') {
        $force = true;
    } elseif ($arg == '-dp') {
        $prefix = $argv[$i+1];
        $i++;
    } elseif ($arg == '-ds') {
        $suffix = $argv[$i+1];
        $i++;
    } elseif ($arg == '-d' || $arg == '--dir') {
        $with_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-b' || $arg == '--bin') {
        $bin_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-c' || $arg == '--config') {
        $cfg_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-w' || $arg == '--www') {
        $www_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-p' || $arg == '--php') {
        $php_bin = $argv[$i+1];
        $i++;
    } elseif ($arg == '-o' || $arg == '--download') {
        $download_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-m' || $arg == '--metadata') {
        $metadata_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-t' || $arg == '--temp') {
        $temp_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-A' || $arg == '--data') {
        $data_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-D' || $arg == '--doc') {
        $doc_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '-T' || $arg == '--test') {
        $test_dir = $argv[$i+1];
        $i++;
    } elseif ($arg == '--debug') {
        $debug = 1;
    } elseif ($arg == '--extremedebug') {
        $debug = 2;
    } elseif ($arg == '-M' || $arg == '--man') {
        $man_dir = $argv[$i+1];
        $i++;
    }
}

$config = PEAR_Config::singleton();

if (PEAR::isError($config)) {
    $locs = PEAR_Config::getDefaultConfigFiles();
    die("ERROR: One of $locs[user] or $locs[system] is corrupt, please remove them and try again");
}

// make sure we use only default values
$config_layers = $config->getLayers();
foreach ($config_layers as $layer) {
    if ($layer == 'default') continue;
    $config->removeLayer($layer);
}
$keys = $config->getKeys();
if ($debug) {
    $config->set('verbose', 5, 'default');
} else {
    $config->set('verbose', 0, 'default');
}
// PEAR executables
if (!empty($bin_dir)) {
    $config->set('bin_dir', $bin_dir, 'default');
}

// Cache files
if (!empty($cache_dir)) {
    $config->set('cache_dir', $cache_dir, 'default');
}

// Config files
if (!empty($cfg_dir)) {
    $config->set('cfg_dir', $cfg_dir, 'default');
}

// Web files
if (!empty($www_dir)) {
    $config->set('www_dir', $www_dir, 'default');
}

// Manual pages
if (!empty($man_dir)) {
    $config->set('man_dir', $man_dir, 'default');
}

// Downloaded files
if (!empty($download_dir)) {
    $config->set('download_dir', $download_dir, 'default');
}

// Temporary files
if (!empty($temp_dir)) {
    $config->set('temp_dir', $temp_dir, 'default');
}

// Documentation files
if (!empty($doc_dir)) {
    $config->set('doc_dir', $doc_dir, 'default');
}

// Data files
if (!empty($data_dir)) {
    $config->set('data_dir', $data_dir, 'default');
}

// Unit tests
if (!empty($test_dir)) {
    $config->set('test_dir', $test_dir, 'default');
}

// User supplied a dir prefix
if (!empty($with_dir)) {
    $ds = DIRECTORY_SEPARATOR;
    $config->set('php_dir', $with_dir, 'default');

    // Metadata
    if (!empty($metadata_dir)) {
        $config->set('metadata_dir', $metadata_dir, 'default');
    }
    if (empty($doc_dir)) {
        $config->set('doc_dir', $with_dir . $ds . 'doc', 'default');
    }
    if (empty($data_dir)) {
        $config->set('data_dir', $with_dir . $ds . 'data', 'default');
    }
    if (empty($test_dir)) {
        $config->set('test_dir', $with_dir . $ds . 'test', 'default');
    }
    if (empty($www_dir)) {
        $config->set('www_dir', $with_dir . $ds . 'htdocs', 'default');
    }
    if (empty($cfg_dir)) {
        $config->set('cfg_dir', $with_dir . $ds . 'cfg', 'default');
    }
    if (empty($man_dir)) {
        $config->set('man_dir', $with_dir . $ds . 'local' . $ds . 'man', 'default');
    }
    if (!is_writable($config->get('cache_dir'))) {
        include_once 'System.php';
        $cdir = System::mktemp(array('-d', 'pear'));
        if (PEAR::isError($cdir)) {
            $ui->outputData("[PEAR] cannot make new temporary directory: " . $cdir);
            die(1);
        }
        $oldcachedir = $config->get('cache_dir');
        $config->set('cache_dir', $cdir);
    }
}

// PHP executable
if (!empty($php_bin)) {
    $config->set('php_bin', $php_bin);
}

// PHP prefix
if (isset($prefix)) {
    if ($prefix != 'a') {
        if ($prefix[0] == 'a') {
            $prefix = substr($prefix, 1);
        }
        $config->set('php_prefix', $prefix, 'system');
    }
}

// PHP suffix
if (isset($suffix)) {
    if ($suffix != 'a') {
        if ($suffix[0] == 'a') {
            $suffix = substr($suffix, 1);
        }
        $config->set('php_suffix', $suffix, 'system');
    }
}

/* Print PEAR Conf (useful for debugging do NOT REMOVE) */
if ($debug) {
    sort($keys);
    foreach ($keys as $key) {
        echo $key . '    ' .
            $config->getPrompt($key) . ": " . $config->get($key, null, 'default') . "\n";
    }
    if ($debug == 2) { // extreme debugging
        exit;
    }
}
// end print

$php_dir = $config->get('php_dir');
$options = array();
$options['upgrade'] = true;
$install_root = getenv('INSTALL_ROOT');
if (!empty($install_root)) {
    $options['packagingroot'] = $install_root;
    $reg = new PEAR_Registry($options['packagingroot'], false, false, $metadata_dir);
} else {
    $reg = $config->getRegistry('default');
}

$ui = PEAR_Frontend::singleton('PEAR_Frontend_CLI');
if (PEAR::isError($ui)) {
    die($ui->getMessage());
}
$installer = new PEAR_Installer($ui);
$pkg = new PEAR_PackageFile($config, $debug);

foreach ($install_files as $package => $instfile) {
    $info = $pkg->fromAnyFile($instfile, PEAR_VALIDATE_INSTALLING);
    if (PEAR::isError($info)) {
        if (is_array($info->getUserInfo())) {
            foreach ($info->getUserInfo() as $err) {
                $ui->outputData(sprintf("[PEAR] %s: %s", $package, $err['message']));
            }
        }
        $ui->outputData(sprintf("[PEAR] %s: %s", $package, $info->getMessage()));
        continue;
    }
    $new_ver = $info->getVersion();
    $downloaderpackage = new PEAR_Downloader_Package($installer);
    $err = $downloaderpackage->initialize($instfile);
    if (PEAR::isError($err)) {
        $ui->outputData(sprintf("[PEAR] %s: %s", $package, $err->getMessage()));
        continue;
    }
    if ($reg->packageExists($package)) {
        $old_ver = $reg->packageInfo($package, 'version');
        if (version_compare($new_ver, $old_ver, 'gt')) {
            $installer->setOptions($options);
            $dp = array($downloaderpackage);
            $installer->setDownloadedPackages($dp);
            $err = $installer->install($downloaderpackage, $options);
            if (PEAR::isError($err)) {
                $ui->outputData(sprintf("[PEAR] %s: %s", $package, $err->getMessage()));
                continue;
            }
            $ui->outputData(sprintf("[PEAR] %-15s- upgraded:  %s", $package, $new_ver));
        } else {
            if ($force) {
                $options['force'] = true;
                $installer->setOptions($options);
                $dp = array($downloaderpackage);
                $installer->setDownloadedPackages($dp);
                $err = $installer->install($downloaderpackage, $options);
                if (PEAR::isError($err)) {
                    $ui->outputData(sprintf("[PEAR] %s: %s", $package, $err->getMessage()));
                    continue;
                }
                $ui->outputData(sprintf("[PEAR] %-15s- installed: %s", $package, $new_ver));
            } else {
                $ui->outputData(sprintf("[PEAR] %-15s- already installed: %s", $package, $old_ver));
            }
        }
    } else {
        $options['nodeps'] = true;
        $installer->setOptions($options);
        $dp = array($downloaderpackage);
        $installer->setDownloadedPackages($dp);
        $err = $installer->install($downloaderpackage, $options);
        if (PEAR::isError($err)) {
            $ui->outputData(sprintf("[PEAR] %s: %s", $package, $err->getMessage()));
            continue;
        }
        $ui->outputData(sprintf("[PEAR] %-15s- installed: %s", $package, $new_ver));
    }
    if ($package == 'PEAR') {
        if (is_file($ufile = $config->getConfFile('user'))) {
            $ui->outputData('Warning! a PEAR user config file already exists from ' .
                            'a previous PEAR installation at ' .
                            "'$ufile'. You may probably want to remove it.");
        }
        $config->set('verbose', 1, 'default');
        if (isset($oldcachedir)) {
            $config->set('cache_dir', $oldcachedir);
        }
        $data = array();
        foreach ($config->getKeys() as $key) {
            $data[$key] = $config->get($key);
        }
        $cnf_file = $config->getConfFile('system');
        if (!empty($install_root)) {
            $cnf_file = $install_root . DIRECTORY_SEPARATOR . $cnf_file;
        }
        $config->writeConfigFile($cnf_file, 'system', $data);
        $ui->outputData('Wrote PEAR system config file at: ' . $cnf_file);
        $ui->outputData('You may want to add: ' . $config->get('php_dir') . ' to your php.ini include_path');
    }
}
?>
