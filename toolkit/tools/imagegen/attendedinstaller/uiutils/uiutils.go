// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package uiutils

import (
	"strings"
	"unicode"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/customshortcutlist"

	"github.com/rivo/tview"
)

const (
	autoSize        = 0
	equalProportion = 1

	listRunePrefix   = 4
	primitivePadding = 1
	formLabelPadding = 2
)

// Center returns a new primitive which shows the provided primitive in its
// center, given the provided primitive's size.
func Center(width, height int, p tview.Primitive) *tview.Flex {
	return tview.NewFlex().
		AddItem(tview.NewBox(), autoSize, equalProportion, false).
		AddItem(tview.NewFlex().
			SetDirection(tview.FlexRow).
			AddItem(tview.NewBox(), autoSize, equalProportion, false).
			AddItem(p, height, equalProportion, true).
			AddItem(tview.NewBox(), autoSize, equalProportion, false), width, equalProportion, true).
		AddItem(tview.NewBox(), autoSize, equalProportion, false)
}

// CenterHorizontally returns a new primitive which shows the provided primitive in its
// horizontal center, given the provided primitive's width.
func CenterHorizontally(width int, p tview.Primitive) *tview.Flex {
	return tview.NewFlex().
		AddItem(tview.NewBox(), autoSize, equalProportion, false).
		AddItem(p, width, equalProportion, true).
		AddItem(tview.NewBox(), autoSize, equalProportion, false)
}

// CenterVertically returns a new primitive which shows the provided primitive in its
// vertical center, given the provided primitive's height.
func CenterVertically(height int, p tview.Primitive) *tview.Flex {
	return tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(tview.NewBox(), autoSize, equalProportion, false).
		AddItem(p, height, equalProportion, true).
		AddItem(tview.NewBox(), autoSize, equalProportion, false)
}

// CenterVerticallyDynamically returns a new primitive which shows the provided primitive in its
// vertical center based on its render size, will dynamically update with the element.
func CenterVerticallyDynamically(p tview.Primitive) *tview.Flex {
	return tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(tview.NewBox(), autoSize, equalProportion, false).
		AddItem(p, autoSize, equalProportion, true).
		AddItem(tview.NewBox(), autoSize, equalProportion, false)
}

// MinListSize returns a minimum width and height needed for a list.
// Does not yet handle secondary text.
func MinListSize(list *customshortcutlist.List) (width, height int) {
	var (
		neededWidth  int
		neededHeight int
	)

	itemCount := list.GetItemCount()

	for i := 0; i < itemCount; i++ {
		mainText, _ := list.GetItemText(i)

		textWidth := tview.TaggedStringWidth(mainText)
		lineLen := textWidth + listRunePrefix + primitivePadding

		if lineLen > neededWidth {
			neededWidth = lineLen
		}
	}

	// Add an extra line to the list for its item padding
	neededHeight = (itemCount + 1) * primitivePadding

	return neededWidth + primitivePadding, neededHeight + primitivePadding
}

// MinTextViewWithNoWrapSize returns the minimum width and height needed for a textview.
// This does not yet handle wrapping.
func MinTextViewWithNoWrapSize(textView *tview.TextView) (width, height int) {
	var (
		neededWidth  int
		neededHeight int
	)

	text := textView.GetText(false)

	allLines := strings.Split(text, "\n")
	neededHeight = len(allLines)

	for _, line := range allLines {
		currentLineLen := tview.TaggedStringWidth(line) + primitivePadding
		if currentLineLen > neededWidth {
			neededWidth = currentLineLen
		}
	}

	return neededWidth + primitivePadding, neededHeight + primitivePadding
}

// MinFormSize returns a minimum width and height needed for a form.
// This does not yet handle buttons or horizontal forms.
func MinFormSize(form *tview.Form) (width, height int) {
	var (
		neededWidth  int
		neededHeight int
	)

	itemCount := form.GetFormItemCount()

	for i := 0; i < itemCount; i++ {
		item := form.GetFormItem(i)
		itemWidth := item.GetFieldWidth() + formLabelPadding + tview.TaggedStringWidth(item.GetLabel())

		if itemWidth > neededWidth {
			neededWidth = itemWidth
		}
	}

	// Add an extra line to the form for the space between items and buttons (present even when there are no buttons)
	neededHeight = (itemCount + 1) * primitivePadding

	return neededWidth + primitivePadding, neededHeight + primitivePadding
}

// ErrorToUserFeedback will convert an error object into a user-friendly message.
func ErrorToUserFeedback(err error) (feedback string) {
	errorMsg := err.Error()
	if errorMsg == "" {
		return
	}

	// Make the first rune upper case
	errRunes := []rune(errorMsg)
	errRunes[0] = unicode.ToUpper(errRunes[0])

	feedback = string(errRunes)
	return
}
