// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package speakuputils

import (
	"github.com/bendahl/uinput"
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
