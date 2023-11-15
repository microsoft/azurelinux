// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app               = kingpin.New("isomaker", "Tool to generate ISO images.")
	unattendedInstall = app.Flag("unattended-install", "Set this flag, if the ISO should install the default system configuration without user's interaction.").Bool()
	baseDirPath       = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	buildDirPath      = app.Flag("build-dir", "Directory to store temporary files while building.").Required().String()
	configFilePath    = exe.InputFlag(app, "Path to the image config file.")
	initrdPath        = app.Flag("initrd-path", "Path to the ISO's initrd file.").Required().ExistingFile()
	isoRepoDirPath    = app.Flag("iso-repo", "Path to repo with fetched RPMs required by the ISO installer.").Required().ExistingDir()
	releaseVersion    = app.Flag("release-version", "The repository OS release version").Required().String()
	resourcesDirPath  = app.Flag("resources", "Path to 'resources' directory").Required().ExistingDir()
	outputDir         = app.Flag("output-dir", "Path to directory to place final image").Required().String()

	imageTag = app.Flag("image-tag", "Tag (text) appended to the image name. Empty by default.").String()

	logFilePath = exe.LogFileFlag(app)
	logLevel    = exe.LogLevelFlag(app)
	logColor    = exe.LogColorFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel, *logColor)

	isoMaker := NewIsoMaker(
		*unattendedInstall,
		*baseDirPath,
		*buildDirPath,
		*releaseVersion,
		*resourcesDirPath,
		*configFilePath,
		*initrdPath,
		*isoRepoDirPath,
		*outputDir,
		*imageTag)
	isoMaker.Make()
}
