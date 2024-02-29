// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package confirmview

import (
	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
)

// UI constants.
const (
	navButtonGoBack = iota
	navButtonYes    = iota
)

const (
	defaultNavButton = navButtonYes
	defaultPadding   = 1

	textProportion = 0

	navBarHeight     = 0
	navBarProportion = 1
)

// ConfirmView contains the confirmation UI
type ConfirmView struct {
	text         *tview.TextView
	navBar       *navigationbar.NavigationBar
	flex         *tview.Flex
	centeredFlex *tview.Flex
}

// New creates and returns a new ConfirmView.
func New() *ConfirmView {
	return &ConfirmView{}
}

// Initialize initializes the view.
func (cv *ConfirmView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	cv.text = tview.NewTextView().
		SetText(uitext.ConfirmPrompt)

	cv.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.ButtonYes, nextPage).
		SetAlign(tview.AlignCenter)

	textWidth, textHeight := uiutils.MinTextViewWithNoWrapSize(cv.text)
	centeredText := uiutils.Center(textWidth, textHeight, cv.text)

	cv.flex = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(centeredText, textHeight, textProportion, false).
		AddItem(cv.navBar, navBarHeight, navBarProportion, true)

	cv.centeredFlex = uiutils.CenterVerticallyDynamically(cv.flex)

	// Box styling
	cv.text.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)
	cv.centeredFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	err = cv.Reset()
	return
}

// HandleInput handles custom input.
func (cv *ConfirmView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	// Navbar is the only input element on this page, so it is in focus already.
	return event
}

// Reset resets the page, undoing any user input.
func (cv *ConfirmView) Reset() (err error) {
	cv.navBar.ClearUserFeedback()
	cv.navBar.SetSelectedButton(defaultNavButton)

	return
}

// Name returns the friendly name of the view.
func (cv *ConfirmView) Name() string {
	return "CONFIRM"
}

// Title returns the title of the view.
func (cv *ConfirmView) Title() string {
	return uitext.ConfirmTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (cv *ConfirmView) Primitive() tview.Primitive {
	return cv.centeredFlex
}

// OnShow gets called when the view is shown to the user
func (cv *ConfirmView) OnShow() {
}
