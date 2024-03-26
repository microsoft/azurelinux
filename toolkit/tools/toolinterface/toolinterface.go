// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/toolinterface/interfaceutils"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app          = kingpin.New("toolinterface", "A command-line interface for azurelinux toolkit")
	build        = app.Command("build", "Build azurelinux")
	setup        = app.Command("setup", "Setup machine")
	ready        = app.Command("ready", "Ready changes to contribute to opensource")

	buildPackage = build.Command("package", "Build package(s)")
	spec         = buildPackage.Flag("spec", "space separated \"\" enclosed name(s) of spec(s) to build").Default("").String()

	buildImage   = build.Command("image", "Build image(s)")
	config       = buildImage.Flag("config", "image config to build").Required().String()
	configDir    = buildImage.Flag("configDir", "directory containing image config").String()

	buildTool     = build.Command("tools", "Build tool(s)")

    buildToolchain = build.Command("toolchain", "Build toolchain")

  )

func main() {
	var err error
	// go run main.go
	// TODO: in each app we should check if the args are correct or not: upfront. first thing to do
	switch kingpin.MustParse(app.Parse(os.Args[1:])) {
		case buildPackage.FullCommand():
			fmt.Println("If this is your first time building Azure Linux, please consider running `setup` to set up your machine")
			fmt.Println("in build_package ")
			fmt.Println("spec list is ", *spec)
			err = interfaceutils.BuildPackage(*spec)
			if err != nil {
				fmt.Println("failed to build package %v", err)
			}
			fmt.Println("Please consider running `ready` before pushing your changes to upstream")
		case buildImage.FullCommand():
		  fmt.Println("in image ")
		  fmt.Println("config file is ", *config)
		  err = interfaceutils.BuildImage(*config)
		  if err != nil {
			fmt.Println("failed to build image %v", err)
		}
		fmt.Println("Please consider running `ready` before pushing your changes to upstream")
		case buildTool.FullCommand():
			fmt.Println("in tools ")
			fmt.Println("Please consider running `ready` before pushing your changes to upstream")
		case ready.FullCommand():
			fmt.Println("in ready ")
			err = interfaceutils.ReadyChanges()
			if err != nil {
				fmt.Println("failed to ready changes %v", err)
			}
		default:
			fmt.Println("Invalid call")
	}
}
