// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"path"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/bldtracker"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/depsearch"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/globals"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"

	"github.com/alecthomas/kong"
)

type CLI struct {
	globals.Globals

	Depsearch  depsearch.DepSearchCmd   `cmd:"" help:"Returns a list of everything that depends on a given package or spec"`
	Bldtracker bldtracker.BldTrackerCmd `cmd:"" help:"Track build time of different steps in a makefile"`
}

func main() {
	var defaultBuildConfigsFile = path.Join(exe.ToolkitRootDir, "default_build_configs.json")
	var cli CLI

	ctx := kong.Parse(&cli,
		kong.Name("boilerplate"),
		kong.Description("A sample golang tool for Mariner."),
		kong.UsageOnError(),
		kong.ConfigureHelp(kong.HelpOptions{Compact: true}),
		kong.Configuration(kong.JSON, defaultBuildConfigsFile),
		kong.Vars{"version": exe.ToolkitVersion})

	logger.InitBestEffort(cli.LogFile, cli.LogLevel)

	err := ctx.Run(&cli.Globals)
	ctx.FatalIfErrorf(err)
}
