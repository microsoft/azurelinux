// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package exe defines QoL functions to simplify and unify creating executables
package exe

import (
	"fmt"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"gopkg.in/alecthomas/kingpin.v2"
)

// ToolkitVersion specifies the version of the toolkit and the reported version of all tools in it.
var ToolkitVersion = ""

// InputFlag registers an input flag for k with documentation doc and returns the passed value
func InputFlag(k *kingpin.Application, doc string) *string {
	return k.Flag("input", doc).Required().ExistingFile()
}

// InputStringFlag registers an input flag for k with documentation doc and returns the passed value
func InputStringFlag(k *kingpin.Application, doc string) *string {
	return k.Flag("input", doc).Required().String()
}

// InputDirFlag registers an input flag for k with documentation doc and returns the passed value
func InputDirFlag(k *kingpin.Application, doc string) *string {
	return k.Flag("dir", doc).Required().ExistingDir()
}

// OutputFlag registers an output flag for k with documentation doc and returns the passed value
func OutputFlag(k *kingpin.Application, doc string) *string {
	return k.Flag("output", doc).Required().String()
}

// OutputDirFlag registers an output flag for k with documentation doc and returns the passed value
func OutputDirFlag(k *kingpin.Application, doc string) *string {
	return k.Flag("output-dir", doc).Required().String()
}

func SetupLogFlags(k *kingpin.Application) *logger.LogFlags {
	lf := &logger.LogFlags{}
	lf.LogColor = k.Flag(logger.ColorFlag, logger.ColorFlagHelp).PlaceHolder(logger.ColorsPlaceholder).Enum(logger.Colors()...)
	lf.LogFile = k.Flag(logger.FileFlag, logger.FileFlagHelp).String()
	lf.LogLevel = k.Flag(logger.LevelsFlag, logger.LevelsHelp).PlaceHolder(logger.LevelsPlaceholder).Enum(logger.Levels()...)
	return lf
}

// PlaceHolderize takes a list of available inputs and returns a corresponding placeholder
func PlaceHolderize(thing []string) string {
	return fmt.Sprintf("(%s)", strings.Join(thing, "|"))
}

// ParseListArgument takes a user provided string list that is space seperated
// and returns a slice of the split and trimmed elements.
func ParseListArgument(input string) (results []string) {
	const delimiter = " "

	trimmedInput := strings.TrimSpace(input)
	if trimmedInput != "" {
		results = strings.Split(trimmedInput, delimiter)
	}
	return
}

type ProfileFlags struct {
	EnableCpuProf *bool
	EnableMemProf *bool
	EnableTrace   *bool
	CpuProfFile   *string
	MemProfFile   *string
	TraceFile     *string
}

func SetupProfileFlags(k *kingpin.Application) *ProfileFlags {
	p := &ProfileFlags{}
	p.EnableCpuProf = k.Flag("enable-cpu-prof", "Enable CPU pprof data collection.").Bool()
	p.EnableMemProf = k.Flag("enable-mem-prof", "Enable Memory pprof data collection.").Bool()
	p.EnableTrace = k.Flag("enable-trace", "Enable trace data collection.").Bool()
	p.CpuProfFile = k.Flag("cpu-prof-file", "File that stores CPU pprof data.").String()
	p.MemProfFile = k.Flag("mem-prof-file", "File that stores Memory pprof data.").String()
	p.TraceFile = k.Flag("trace-file", "File that stores trace data.").String()
	return p
}
