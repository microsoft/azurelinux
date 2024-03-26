// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package interfaceutils

import (
	"io"
	"fmt"
    "os"
	"os/exec"
)

// buildStatus checks if spec needs to be rebuilt
// reasons for rebuild:
//					- spec has never been built
//					- there is a change in spec from last build
//					- there is a change in toolchain manifest
//					- user wants to rebuild spec
func buildStatus() (err error) {
	fmt.Println("in buildStatus")
	return

}

// buildStatusToolchain checks if toolchain should be (re)built
// returns true if
//					- toolchain rpms have never been built
//					- there is a change in toolchain spec(s)
//					- there is a change in toolchain manifest
//					- user wants to rebuild toolchain
func buildStatusToolchain() (rebuildOpt bool, err error) {
	err = buildStatus()
	// added if change in manifest files
	return false, nil
}

func execCommands(app, dir string, args ...string) (err error) {
	cmd := exec.Command(app, args...)
	if dir != "" {
		cmd.Dir = dir
	}
	cmd.Stdout = io.MultiWriter(os.Stdout)
	cmd.Stderr = io.MultiWriter(os.Stderr)

	err = cmd.Start()
	if err != nil {
		fmt.Printf("failed to exec cmd.Start():\n%w", err)
        return
	}
	err = cmd.Wait()
	if err != nil {
		fmt.Printf("failed to exec cmd.Run():\n%w", err)
        return
	}
    return
}
