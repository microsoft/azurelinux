// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package speakuputils

import (
	"github.com/bendahl/uinput"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

// Constants for start/stop speakup functions
const (
	squashError      = false
	systemctlProgram = "systemctl"
	espeakupService  = "espeakup.service"
)

// CreateVirtualKeyboard creates and returns a virtual keyboard from the uinput package
func CreateVirtualKeyboard() (keyboard uinput.Keyboard, err error) {
	keyboard, err = uinput.CreateKeyboard("/dev/uinput", []byte("MarinerVirtualKeyboard"))
	return
}

// SetHighlightTrackingMode is used once at startup to enable speakup's highlight tracking mode
func SetHighlightTrackingMode(k uinput.Keyboard) (err error) {
	if k == nil {
		return
	}
	err = k.KeyPress(uinput.KeyKpasterisk)
	return
}

// ClearSpeakupBuffer sends keypresses that will clear the speakup buffer
func ClearSpeakupBuffer(k uinput.Keyboard) (err error) {
	if k == nil {
		return
	}
	err = k.KeyPress(uinput.KeyKpenter)
	if err != nil {
		return err
	}
	// This could be any key that doesn't trigger input to a field
	err = k.KeyPress(uinput.KeyRightctrl)
	return
}

// StopSpeakup stops the espeakup connector daemon using systemctl
func StopSpeakup() (err error) {
	err = shell.ExecuteLive(squashError, systemctlProgram, []string{"disable", espeakupService}...)
	if err != nil {
		return
	}
	err = shell.ExecuteLive(squashError, systemctlProgram, []string{"stop", espeakupService}...)
	return
}

// StartSpeakup stops the espeakup connector daemon using systemctl
func StartSpeakup() (err error) {
	err = shell.ExecuteLive(squashError, systemctlProgram, []string{"enable", espeakupService}...)
	if err != nil {
		return
	}
	err = shell.ExecuteLive(squashError, systemctlProgram, []string{"start", espeakupService}...)
	return
}
