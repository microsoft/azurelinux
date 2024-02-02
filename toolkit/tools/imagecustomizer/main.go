// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"log"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagecustomizerlib"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("imagecustomizer", "Customizes a pre-built CBL-Mariner image")

	buildDir                    = app.Flag("build-dir", "Directory to run build out of.").Required().String()
	imageFile                   = app.Flag("image-file", "Path of the base CBL-Mariner image which the customization will be applied to.").Required().String()
	outputImageFile             = app.Flag("output-image-file", "Path to write the customized image to.").Required().String()
	outputImageFormat           = app.Flag("output-image-format", "Format of output image. Supported: vhd, vhdx, qcow2, raw, iso.").Enum("vhd", "vhdx", "qcow2", "raw", "iso")
	outputSplitPartitionsFormat = app.Flag("output-split-partitions-format", "Format of partition files. Supported: raw, raw-zstd").Enum("raw", "raw-zstd")
	configFile                  = app.Flag("config-file", "Path of the image customization config file.").Required().String()
	rpmSources                  = app.Flag("rpm-source", "Path to a RPM repo config file or a directory containing RPMs.").Strings()
	disableBaseImageRpmRepos    = app.Flag("disable-base-image-rpm-repos", "Disable the base image's RPM repos as an RPM source").Bool()
	enableShrinkFilesystems     = app.Flag("shrink-filesystems", "Enable shrinking of filesystems to minimum size. Supports ext2, ext3, ext4 filesystem types.").Bool()
	logFile                     = exe.LogFileFlag(app)
	logLevel                    = exe.LogLevelFlag(app)
	profFlags                   = exe.SetupProfileFlags(app)
	timestampFile               = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	var err error

	app.Version(imagecustomizerlib.ToolVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	if *outputSplitPartitionsFormat == "" && *outputImageFormat == "" {
		kingpin.Fatalf("Either --output-image-format or --output-split-partitions-format must be specified.")
	}

	logger.InitBestEffort(*logFile, *logLevel)

	if *enableShrinkFilesystems && *outputSplitPartitionsFormat == "" {
		logger.Log.Fatalf("--output-split-partitions-format must be specified to use --shrink-filesystems.")
	}

	if *enableShrinkFilesystems && *outputImageFormat != "" {
		logger.Log.Fatalf("--output-image-format cannot be used with --shrink-filesystems enabled.")
	}

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("imagecustomizer", *timestampFile)
	defer timestamp.CompleteTiming()

	err = customizeImage()
	if err != nil {
		log.Fatalf("image customization failed: %v", err)
	}
}

func customizeImage() error {
	var err error

	err = imagecustomizerlib.CustomizeImageWithConfigFile(*buildDir, *configFile, *imageFile,
		*rpmSources, *outputImageFile, *outputImageFormat, *outputSplitPartitionsFormat, !*disableBaseImageRpmRepos, *enableShrinkFilesystems)
	if err != nil {
		return err
	}

	return nil
}
