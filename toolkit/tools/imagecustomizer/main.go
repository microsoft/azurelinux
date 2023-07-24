// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"log"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerlib"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("imagecustomizer", "Customizes a pre-built CBL-Mariner image")

	buildDir        = app.Flag("build-dir", "Directory to run build out of.").Required().String()
	imageFile       = app.Flag("image-file", "Path of the base CBL-Mariner image which the customization will be applied to.").Required().String()
	outputImageFile = app.Flag("output-image-file", "Path to write the customized image to.").Required().String()
	configFile      = app.Flag("config-file", "Path of the image customization config file.").Required().String()
	logFile         = exe.LogFileFlag(app)
	logLevel        = exe.LogLevelFlag(app)
)

func main() {
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel)

	err := customizeImage()
	if err != nil {
		log.Fatalf("image customization failed: %v", err)
	}
}

func customizeImage() error {
	var err error

	_, _, err = shell.Execute("qemu-img", "convert", "-O", "qcow2", *imageFile, *outputImageFile)
	if err != nil {
		return fmt.Errorf("failed to load nbd kernel module: %w", err)
	}

	err = imagecustomizerlib.CustomizeImageWithConfigFile(*buildDir, *configFile, *outputImageFile)
	if err != nil {
		return err
	}

	return nil
}
