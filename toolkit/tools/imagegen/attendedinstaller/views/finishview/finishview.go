// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package finishview

import (
	"fmt"
	"time"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// UI constants.
const (
	// default to <Restart>
	defaultNavButton = 0
	defaultPadding   = 1

	textProportion = 0

	navBarHeight     = 0
	navBarProportion = 1
)

// FinishView contains the confirmation UI
type FinishView struct {
	// UI elements
	app          *tview.Application
	flex         *tview.Flex
	centeredFlex *tview.Flex
	text         *tview.TextView
	navBar       *navigationbar.NavigationBar

	// Generate state
	alreadyShown bool

	// Callbacks
	updateInstallationTime func() time.Duration
}

// New creates and returns a new FinishView.
func New(updateInstallationTime func() time.Duration) *FinishView {
	return &FinishView{
		updateInstallationTime: updateInstallationTime,
	}
}

// Initialize initializes the view.
func (fv *FinishView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	fv.app = app

	fv.text = tview.NewTextView().
		SetWordWrap(true).
		SetChangedFunc(func() {
			app.Draw()
		})

	fv.navBar = navigationbar.NewNavigationBar().
		AddButton(uitext.ButtonRestart, nextPage).
		SetAlign(tview.AlignCenter)

	fv.flex = tview.NewFlex()
	fv.centeredFlex = uiutils.CenterVerticallyDynamically(fv.flex)

	// Box styling
	fv.text.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)
	fv.centeredFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (fv *FinishView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	switch event.Key() {
	// Prevent exiting the UI here as installation has already finished
	case tcell.KeyCtrlC:
		return nil
	}

	return event
}

// Reset resets the page, undoing any user input.
func (fv *FinishView) Reset() (err error) {
	fv.navBar.ClearUserFeedback()
	fv.navBar.SetSelectedButton(defaultNavButton)

	return
}

// Name returns the friendly name of the view.
func (fv *FinishView) Name() string {
	return "FINISH"
}

// Title returns the title of the view.
func (fv *FinishView) Title() string {
	return uitext.FinishTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (fv *FinishView) Primitive() tview.Primitive {
	return fv.centeredFlex
}

// OnShow gets called when the view is shown to the user
func (fv *FinishView) OnShow() {
	if fv.alreadyShown {
		logger.Log.Panicf("FinishView shown more than once, unsupported behavior.")
	}
	fv.alreadyShown = true

	installationDuration := fv.updateInstallationTime()
	roundedDuration := installationDuration.Round(time.Second)

	fv.text.SetText(fmt.Sprintf(uitext.FinishTextFmt, roundedDuration.Seconds()))
	fv.updateTextSize()

	// Unlike other views, FinishView will complete UI initialization in OnShow
	// since the installation time is not known during Initialize().
	// Force a focus change as the flex box has just been initialized in updateTextSize().
	fv.app.SetFocus(fv.centeredFlex)
}

func (fv *FinishView) updateTextSize() {
	textWidth, textHeight := uiutils.MinTextViewWithNoWrapSize(fv.text)
	centeredText := uiutils.Center(textWidth, textHeight, fv.text)

	fv.flex.
		SetDirection(tview.FlexRow).
		AddItem(centeredText, textHeight, textProportion, false).
		AddItem(fv.navBar, navBarHeight, navBarProportion, true)
}
