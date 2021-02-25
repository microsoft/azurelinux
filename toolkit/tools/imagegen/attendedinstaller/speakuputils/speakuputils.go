// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package speakuputils

import (
	"github.com/bendahl/uinput"
)

func CreateVirtualKeyboard() (keyboard uinput.Keyboard, err error) {
	keyboard, err = uinput.CreateKeyboard("/dev/uinput", []byte("MarinerVirtualKeyboard"))
	return
}

func ClearSpeakupBuffer(k uinput.Keyboard) (err error) {
	if k == nil {
		return
	}
	err = k.KeyPress(uinput.KeyKpenter)
	if err != nil {
		return err
	}
	err = k.KeyPress(uinput.KeyKpenter)
	return
}
