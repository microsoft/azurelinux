// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/unravel/formats"
)

const (
	formatLinear         = "linear"
	formatMakefile       = "makefile"
	defaultRetryAttempts = "1"
)

var (
	app                  = kingpin.New("unravel", "A tool to process dependency graph to build order representation.")
	input                = exe.InputFlag(app, "DOT(graphviz) file representing the dependency graph")
	output               = exe.OutputFlag(app, "File which will be filled with build order representation.")
	logFile              = exe.LogFileFlag(app)
	logLevel             = exe.LogLevelFlag(app)
	stopOnFailure        = app.Flag("stop-on-failure", "Halt the builds on a failure").Bool()
	runCheck             = app.Flag("run-check", "Sets whether or not pkgworker should run builds with check").Default("n").String()
	distTag              = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	cacheDir             = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from the CBL-Mariner Base").Required().String()
	distroReleaseVersion = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with").Required().String()
	distroBuildNumber    = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with").Required().String()
	retryAttempts        = app.Flag("retry-attempts", "Sets the number of times pkgworker will retry building the package").Default(defaultRetryAttempts).Int()

	legalFormats = []string{formatLinear, formatMakefile}
	format       = app.Flag("format", "Output format").PlaceHolder(exe.PlaceHolderize(legalFormats)).Required().Enum(legalFormats...)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	g := pkggraph.NewPkgGraph()
	err := pkggraph.ReadDOTGraphFile(g, *input)
	logger.PanicOnError(err, "Failed to read graph file file '%s'.", *input)

	var u formats.Unravel
	switch *format {
	case formatLinear:
		u = formats.NewLinear(g)
	case formatMakefile:
		const (
			pkgWorkerCommandFmt      = `MAKEFLAGS= $(go-pkgworker) --input=%s --retry-attempts=%d --cache-dir=%s %s --work-dir=$(CHROOT_DIR) --worker-tar=$(chroot_worker) --repo-file=$(pkggen_local_repo) --rpms-dir=$(RPMS_DIR) --srpms-dir=$(SRPMS_DIR) --rpmmacros-file=$(TOOLCHAIN_MANIFESTS_DIR)/macros.override --dist-tag=%s --distro-release-version=%s --distro-build-number=%s --log-file=$(LOGS_DIR)/pkggen/rpmbuilding/%s.log`
			continueOnFailurePostfix = ` || echo "%s" >> $(LOGS_DIR)/pkggen/failures.txt`
			stopOnFailurePostfix     = ` || { echo "%s" >> $(LOGS_DIR)/pkggen/failures.txt ; echo "--stop-on-failure set, halting on package build failure" ; exit 1 ; }`
		)

		var postfix string
		var checkSetting string

		if *stopOnFailure {
			postfix = stopOnFailurePostfix
		} else {
			postfix = continueOnFailurePostfix
		}

		if *runCheck == "y" {
			checkSetting = " --run-check "
		} else {
			checkSetting = " "
		}

		u = formats.NewMakefile(g, func(srpmPath string) string {
			srpmName := filepath.Base(srpmPath)
			return fmt.Sprintf(pkgWorkerCommandFmt+postfix, srpmPath, *retryAttempts, *cacheDir, checkSetting, *distTag, *distroReleaseVersion, *distroBuildNumber, srpmName, srpmName)
		})
	default:
		logger.Log.Panicf("Wrong output format encountered: %s. Allowed: %s", *format, legalFormats)
	}

	out, err := os.Create(*output)
	logger.PanicOnError(err, "Failed to create output file '%s'.", *output)
	defer out.Close()

	err = u.Save(out)
	logger.PanicOnError(err, "Failed to unravel the graph.")

	logger.Log.Infof(`Successfully finished converting to format "%s" - output file "%s".`, *format, *output)
}
