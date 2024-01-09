// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"

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
	var cli CLI

	ctx := kong.Parse(&cli,
		kong.Name("boilerplate"),
		kong.Description("A sample golang tool for Mariner."),
		kong.UsageOnError(),
		kong.ConfigureHelp(kong.HelpOptions{Compact: true}),
		kong.Configuration(kong.JSON, "/datadrive/projects/CBL-Mariner/toolkit/default_build_configs.json"),
		kong.Vars{"version": exe.ToolkitVersion})

	fmt.Println(cli.LogFile)
	fmt.Println(cli.LogLevel)

	logger.InitBestEffort(cli.LogFile, cli.LogLevel)

	err := ctx.Run(&cli.Globals)
	ctx.FatalIfErrorf(err)
}
