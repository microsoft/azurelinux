// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A boilerplate for Mariner go tools

package main

import (
	"path"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/boilerplate/hello"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/globals"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"

	"github.com/alecthomas/kong"
)

type HelloCmd struct {
	Name string `arg:"" help:"Name" default:"Mariner"`
}

func (cmd *HelloCmd) Run(globals *globals.Globals) error {
	logger.Log.Info(hello.Name(cmd.Name))
	return nil
}

type CLI struct {
	globals.Globals

	Hello HelloCmd `cmd:"" help:"Say hello to Name"`
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
	timestamp.BeginTiming("boilerplate", cli.TimestampFile)
	defer timestamp.CompleteTiming()

	err := ctx.Run(&cli.Globals)
	ctx.FatalIfErrorf(err)

	logger.Log.Info(hello.World())
}
