// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package hello

import "github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"

// World is a sample public (starts with a capital letter, must be commented) function.
func World() string {
	timestamp.StartEvent("hello world", nil)
	defer timestamp.StopEvent(nil)

	return "Hello, world!"
}
