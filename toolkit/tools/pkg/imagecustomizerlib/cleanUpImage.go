package imagecustomizerlib

import (
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

func cleanTdnfCache(imageChroot *safechroot.Chroot) error {

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

	// Run all cleanup tasks inside the chroot environment
	return imageChroot.UnsafeRun(func() error {
		err := tdnfClean()
		if err != nil {
			return err
		}
		return nil
	})
}
