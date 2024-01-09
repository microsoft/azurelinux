// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package globals

import (
	"fmt"

	"github.com/alecthomas/kong"
)

type VersionFlag string

func (v VersionFlag) Decode(ctx *kong.DecodeContext) error { return nil }
func (v VersionFlag) IsBool() bool                         { return true }
func (v VersionFlag) BeforeApply(ctx *kong.Context, vars kong.Vars) error {
	fmt.Println(vars["version"])
	ctx.Exit(0)
	return nil
}

type Globals struct {
	LogFile       string      `help:"Where to write log to" type:"path"`
	LogLevel      string      `enum:"panic,fatal,error,warn,info,debug,trace" default:"info" help:"Log level (${enum})"`
	TimestampFile string      `help:"File that stores timestamp data for this program" type:"path"`
	Version       VersionFlag `help:"Print version information and quit"`
}
