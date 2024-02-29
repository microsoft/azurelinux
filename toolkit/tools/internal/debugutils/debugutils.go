// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package debugutils

import (
	"bufio"
	"os"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// These are functions which are useful for adding breakpoints into code running in a chroot, while running
// at elevated permissions, or other unusual states which make traditional debugging very challenging. These
// can be used similarly to a normal breakpoint.

func ic(i *int) {
	*i++
}

// WaitForDebugger busy loops until manually broken out of.
// Useful for breaking in with a debugger when running privileged code.
func WaitForDebugger(tag string) {
	i := 1
	logger.Log.Errorf("Freezing at %s for debugger", tag)
	logger.Log.Errorf("Use 'break ic', then 'c' to jump to the busy loop")

	for i != 0 {
		logger.Log.Errorf("Waiting for debugger %d, once broken in run `so` to step out, `set i=0`, then `c`", i)
		// Intentionally use a pointer here so nothing gets optimized.
		ic(&i)
		time.Sleep(time.Second)
	}
}

// WaitForUser freezes until the user presses a key
func WaitForUser(tag string) {
	logger.Log.Warnf("Freezing at %s, press [ENTER] to thaw", tag)
	bufio.NewReader(os.Stdin).ReadString('\n')
	logger.Log.Warn("Thawing chroot")
}
