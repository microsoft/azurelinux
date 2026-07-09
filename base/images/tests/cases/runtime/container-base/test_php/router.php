<?php
// router.php
// Exercises the php-pecl-zip extension by creating, writing and
// extracting a zip archive, then verifying the round-trip.
if (preg_match('/\.(?:png|jpg|jpeg|gif)$/', $_SERVER["REQUEST_URI"])) {
    return false;    // serve the requested resource as-is.
} else {
    $zip = new ZipArchive();
    $testFolder = shell_exec("mktemp -d | tr -d '\n'");
    $filename = "$testFolder/test_archive.zip";
    if ($zip->open($filename, ZipArchive::CREATE) !== TRUE) {
        exit("cannot open <$filename>\n");
    }
    $zip->addFromString("testfilephp.txt", "#1 This is a test string added as testfilephp.txt.\n");
    $zip->addFromString("testfilephp2.txt", "#2 This is a test string added as testfilephp2.txt.\n");
    $zip->addFile("/app/router.php", "router.php");
    $zip->close();
    if (file_exists($filename)) {
        shell_exec("unzip $filename -d $testFolder/test_folder");
        foreach (array("testfilephp.txt", "testfilephp2.txt", "router.php") as $testFile) {
            if (!file_exists("$testFolder/test_folder/$testFile")) return false;
        }
        shell_exec("rm -rf $testFolder");
        echo file_get_contents(__DIR__ . "/response.txt");
    } else {
        exit("Zip archive not created, server reached though.");
    }
}
?>
