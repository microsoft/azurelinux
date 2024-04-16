// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package navigationbar

import (
	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
)

const (
	navbarHeight   = 4
	feedbackHeight = 2
)

// NavigationBar is transparent horizontal form for navigation that always has a button selected.
//
// Unlike a typical Primitive, NavigationBar is meant to consume input and appear in focus
// alongside other infocus elements.
type NavigationBar struct {
	*tview.Box

	// The buttons of the navigationbar.
	buttons []*tview.Button

	// The label color.
	labelColor tcell.Color

	// The label color when a button is selected.
	labelColorActivated tcell.Color

	// The background color.
	backgroundColor tcell.Color

	// The background color when a button is selected.
	backgroundColorActivated tcell.Color

	// The label color of feedback messages.
	feedbackColor tcell.Color

	// The index of the button which is selected.
	selectedButton int

	// The alignment of the buttons.
	align int

	// Feedback to provide to the user. This could be an error message from input validation.
	feedback string

	// A callback invoked when the user leaves the navigation bar when it is a form item.
	onFinished func(tcell.Key)

	// A callback invoked when this primitive receives focus.
	onFocus func()

	// A callback invoked when this primitive loses focus.
	onBlur func()
}

// NewNavigationBar returns a new navigation bar.
func NewNavigationBar() *NavigationBar {
	return &NavigationBar{
		Box:                      tview.NewBox().SetBorderPadding(0, 1, 1, 1),
		backgroundColor:          tview.Styles.PrimitiveBackgroundColor,
		backgroundColorActivated: tview.Styles.GraphicsColor,
		labelColor:               tview.Styles.PrimaryTextColor,
		labelColorActivated:      tview.Styles.InverseTextColor,
	}
}

// SetAlign sets how the buttons align horizontally.
// Options include:
// - AlignLeft (default)
// - AlignCenter
// - AlignRight
func (n *NavigationBar) SetAlign(align int) *NavigationBar {
	n.align = align
	return n
}

// SetLabelColor sets the color of button text.
func (n *NavigationBar) SetLabelColor(color tcell.Color) *NavigationBar {
	n.labelColor = color
	return n
}

// SetLabelColorActivated sets the color of button text when the button is
// selected.
func (n *NavigationBar) SetLabelColorActivated(color tcell.Color) *NavigationBar {
	n.labelColorActivated = color
	return n
}

// SetNavBackgroundColor sets the background color.
func (n *NavigationBar) SetNavBackgroundColor(color tcell.Color) *NavigationBar {
	n.backgroundColor = color
	return n
}

// SetBackgroundColorActivated sets the background color of the button text when
// the button is selected.
func (n *NavigationBar) SetBackgroundColorActivated(color tcell.Color) *NavigationBar {
	n.backgroundColorActivated = color
	return n
}

// AddButton adds a new button to the navigationbar. The "selected" function is called
// when the user selects this button. It may be nil.
func (n *NavigationBar) AddButton(label string, selected func()) *NavigationBar {
	n.buttons = append(n.buttons, tview.NewButton(label).SetSelectedFunc(selected))
	return n
}

// SetSelectedButton sets which button is currently selected.
func (n *NavigationBar) SetSelectedButton(selected int) *NavigationBar {
	n.selectedButton = selected
	return n
}

// GetHeight returns the height of the navbar.
func (n *NavigationBar) GetHeight() int {
	return navbarHeight
}

// ClearUserFeedback removes any currently showing feedback.
func (n *NavigationBar) ClearUserFeedback() *NavigationBar {
	n.feedback = ""
	return n
}

// SetUserFeedback sets a message for the user in a given color.
func (n *NavigationBar) SetUserFeedback(feedback string, color tcell.Color) *NavigationBar {
	n.feedback = uitext.BoldPrefix + feedback
	n.feedbackColor = color
	return n
}

// Draw renders this primitive onto the screen.
func (n *NavigationBar) Draw(screen tcell.Screen) {
	// Draw a transparent bounding box. On Draw size calculations are updated.
	n.Box.Draw(screen)

	// Determine the bounding dimensions.
	x, y, width, _ := n.GetInnerRect()
	rightLimit := x + width

	// Draw user feedback.
	if n.feedback != "" {
		tview.Print(screen, n.feedback, x, y, width, tview.AlignLeft, n.feedbackColor)
	}
	y += feedbackHeight

	// Determine how wide the buttons are.
	allButtonWidths := make([]int, len(n.buttons))
	buttonsWidth := 0
	for i, button := range n.buttons {
		w := tview.TaggedStringWidth(button.GetLabel()) + 4
		allButtonWidths[i] = w
		buttonsWidth += w + 1
	}

	// Trim the trailing padding from buttons
	if len(n.buttons) != 0 {
		buttonsWidth--
	}

	positions := make([]struct{ x, y, width, height int }, len(n.buttons))

	if n.align == tview.AlignRight {
		x = rightLimit - buttonsWidth
	} else if n.align == tview.AlignCenter {
		x = x + ((width - buttonsWidth) / 2)
	}

	// Calculate positions of buttons.
	for i, button := range n.buttons {
		space := rightLimit - x
		buttonWidth := allButtonWidths[i]

		if buttonWidth > space {
			buttonWidth = space
		}

		if n.selectedButton == i {
			button.SetLabelColor(n.labelColorActivated).
				SetBackgroundColor(n.backgroundColorActivated)
		} else {
			button.SetLabelColor(n.labelColor).
				SetBackgroundColor(n.backgroundColor)
		}

		positions[i].x = x
		positions[i].y = y
		positions[i].width = buttonWidth
		positions[i].height = 1

		x += buttonWidth + 1
	}

	// Draw buttons.
	for i, button := range n.buttons {
		// Set position.
		y := positions[i].y
		height := positions[i].height
		button.SetRect(positions[i].x, y, positions[i].width, height)

		// Draw button.
		button.Draw(screen)
	}
}

// UnfocusedInputHandler handles input even when this primitive is not in focus.
// Returns true if a key event was consumed.
func (n *NavigationBar) UnfocusedInputHandler(event *tcell.EventKey) bool {
	// Process key event.
	key := event.Key()
	switch key {
	case tcell.KeyEnter:
		if len(n.buttons) != 0 {
			buttonHandler := n.buttons[n.selectedButton].InputHandler()
			buttonHandler(event, nil)
		}
	case tcell.KeyEscape:
		n.selectedButton = 0
	case tcell.KeyLeft:
		if n.selectedButton > 0 {
			n.selectedButton--
		}
	case tcell.KeyRight:
		if n.selectedButton < len(n.buttons)-1 {
			n.selectedButton++
		}
	case tcell.KeyUp, tcell.KeyDown, tcell.KeyTab, tcell.KeyBacktab:
		if n.onFinished != nil {
			n.onFinished(key)
		} else {
			return false
		}
	default:
		return false
	}

	return true
}

// InputHandler returns the handler for this primitive.
func (n *NavigationBar) InputHandler() func(event *tcell.EventKey, setFocus func(p tview.Primitive)) {
	return n.WrapInputHandler(func(event *tcell.EventKey, setFocus func(p tview.Primitive)) {
		n.UnfocusedInputHandler(event)
	})
}

// GetLabel returns the text to be displayed before the input area.
func (n *NavigationBar) GetLabel() string {
	return ""
}

// GetFieldWidth returns this primitive's field screen width.
func (n *NavigationBar) GetFieldWidth() int {
	const (
		buttonPadding     = 1
		buttonTextPadding = 4
	)

	// Determine how wide the buttons are.
	buttonsWidth := 0
	for _, button := range n.buttons {
		w := tview.TaggedStringWidth(button.GetLabel()) + buttonTextPadding
		buttonsWidth += w + buttonPadding
	}

	// Trim the trailing padding from buttons
	if len(n.buttons) != 0 {
		buttonsWidth--
	}

	return buttonsWidth
}

// SetFormAttributes sets attributes shared by all form items.
func (n *NavigationBar) SetFormAttributes(labelWidth int, labelColor, bgColor, fieldTextColor, fieldBgColor tcell.Color) tview.FormItem {
	return n
}

// SetFinishedFunc sets a callback invoked when the user leaves this form item.
func (n *NavigationBar) SetFinishedFunc(handler func(key tcell.Key)) tview.FormItem {
	n.onFinished = handler
	return n
}

// SetOnFocusFunc sets a callback invoked when this primitive receives focus.
func (n *NavigationBar) SetOnFocusFunc(handler func()) *NavigationBar {
	n.onFocus = handler
	return n
}

// SetOnBlurFunc sets a callback invoked when this primitive loses focus.
func (n *NavigationBar) SetOnBlurFunc(handler func()) *NavigationBar {
	n.onBlur = handler
	return n
}

// Focus is called when this primitive receives focus.
func (n *NavigationBar) Focus(delegate func(p tview.Primitive)) {
	if n.onFocus != nil {
		n.onFocus()
	}

	n.Box.Focus(delegate)
}

// Blur is called when this primitive loses focus.
func (n *NavigationBar) Blur() {
	if n.onBlur != nil {
		n.onBlur()
	}

	n.Box.Blur()
}
