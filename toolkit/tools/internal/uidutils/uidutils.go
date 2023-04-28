// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utilities for managing unique IDs

package uidutils

import "math"

const (
	maxID = math.MaxInt64
)

var (
	currentMax int64 = 0
)

func NextUID() (uid int64) {
	if currentMax < maxID {
		uid = currentMax
		currentMax++
		return
	}
	panic("Ran out of uint64 to assign UID")
}

func Reset() {
	currentMax = 0
}
