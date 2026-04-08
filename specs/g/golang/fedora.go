//go:build rpm_crashtraceback
// +build rpm_crashtraceback

// Copyright 2017 The Fedora Project Contributors. All rights reserved.
// Use of this source code is governed by the MIT license.

package runtime

func init() {
	setTraceback("crash")
}
