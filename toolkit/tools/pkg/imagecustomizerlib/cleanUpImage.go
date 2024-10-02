package imagecustomizerlib

import (
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

func cleanUpImage(imageChroot *safechroot.Chroot) error {

	// // Function to log disk space usage
	// logDiskSpace := func() error {
	// 	logger.Log.Infof("Disk space usage:")
	// 	return shell.NewExecBuilder("du", "-h", "--max-depth=2").
	// 		// Pipe("sort", "-rh").
	// 		// Pipe("head", "-n", "20").
	// 		LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
	// 		Execute()
	// }

	// // Remove symlink if it exists
	// removeSymlink := func() error {
	// 	if _, err := os.Lstat("/srv"); err == nil {
	// 		logger.Log.Infof("Removing /srv symlink")
	// 		return shell.NewExecBuilder("rm", "/srv").
	// 			LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
	// 			Execute()
	// 	} else {
	// 		logger.Log.Infof("/srv symlink does not exist")
	// 	}
	// 	return nil
	// }

	// // Remove Python __pycache__ directories
	// removePyCache := func() error {
	// 	return shell.NewExecBuilder("find", "/usr/lib/python*", "-type", "d", "-name", "__pycache__", "-exec", "rm", "-rf", "{}", "+").
	// 		LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
	// 		Execute()
	// }

	// // Remove documentation
	// removeDocs := func() error {
	// 	err1 := shell.NewExecBuilder("rm", "-rf", "/usr/share/doc/*").
	// 		LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
	// 		Execute()
	// 	err2 := shell.NewExecBuilder("rm", "-rf", "/usr/share/man/*").
	// 		LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
	// 		Execute()
	// 	if err1 != nil || err2 != nil {
	// 		return fmt.Errorf("failed to remove documentation")
	// 	}
	// 	return nil
	// }

	logger.Log.Infof("Cleaning up image")

	// clear tdnf cache
	tdnfClean := func() error {
		tdnfArgs := []string{
			"-v", "clean", "all",
		}
		stdoutCallback := func(line string) {
			logger.Log.Trace(line)
		}
		return shell.NewExecBuilder("tdnf", tdnfArgs...).
			StdoutCallback(stdoutCallback).
			LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
	}

	// Clear journal logs
	clearJournalLogs := func() error {
		return shell.NewExecBuilder("journalctl", "--vacuum-time=1s").
			LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
			Execute()
	}

	// Run all cleanup tasks inside the chroot environment
	return imageChroot.UnsafeRun(func() error {
		if err := tdnfClean(); err != nil {
			return err
		}
		if err := clearJournalLogs(); err != nil {
			return err
		}
		return nil
	})
}
