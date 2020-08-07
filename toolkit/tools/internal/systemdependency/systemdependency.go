// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package systemdependency

import (
	"fmt"
	"os/exec"
)

// GzipTool returns the gzip tool to use on the host
func GzipTool() (gzipTool string, err error) {
	toolsToCheck := []string{"pigz", "gzip"}

	for _, tool := range toolsToCheck {
		gzipTool, err = exec.LookPath(tool)
		if err == nil {
			break
		}
	}

	if gzipTool == "" {
		err = fmt.Errorf("failed to find a suitable gzip tool on the current system")
	}

	return
}
