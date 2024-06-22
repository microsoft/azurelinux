// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package eulaview

import (
	"fmt"
	"io/ioutil"
	"os"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
)

// Resource constants.
const (
	eulaFile = "./EULA.txt"
)

// UI constants.
const (
	// default to <Accept>
	defaultNavButton = 1
	heightPadding    = 1
	widthPadding     = 10

	textHeight     = 0
	textProportion = 1

	navBarProportion = 0
)

// EulaView contains the EULA UI
type EulaView struct {
	flex   *tview.Flex
	text   *tview.TextView
	navBar *navigationbar.NavigationBar
}

// New creates and returns a new EulaView.
func New() *EulaView {
	return &EulaView{}
}

// Initialize initializes the view.
func (ev *EulaView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	ev.text = tview.NewTextView().
		SetWordWrap(true).
		SetChangedFunc(func() {
			app.Draw()
		})

	err = populateEULA(eulaFile, ev.text)
	if err != nil {
		return
	}

	ev.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.ButtonAccept, nextPage).
		SetAlign(tview.AlignRight)

	ev.flex = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(ev.text, textHeight, textProportion, true).
		AddItem(ev.navBar, ev.navBar.GetHeight(), navBarProportion, false)

	// Box styling
	ev.text.SetBorderPadding(heightPadding, heightPadding, widthPadding, widthPadding)
	ev.flex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (ev *EulaView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	if ev.navBar.UnfocusedInputHandler(event) {
		return nil
	}

	return event
}

// Reset resets the page, undoing any user input.
func (ev *EulaView) Reset() (err error) {
	ev.navBar.ClearUserFeedback()
	ev.text.ScrollToBeginning()
	ev.navBar.SetSelectedButton(defaultNavButton)

	return
}

// Name returns the friendly name of the view.
func (ev *EulaView) Name() string {
	return "EULA"
}

// Title returns the title of the view.
func (ev *EulaView) Title() string {
	return uitext.EulaTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (ev *EulaView) Primitive() tview.Primitive {
	return ev.flex
}

// OnShow gets called when the view is shown to the user
func (ev *EulaView) OnShow() {
}

func populateEULA(eulaFile string, text *tview.TextView) (err error) {
	file, err := os.Open(eulaFile)
	if err != nil {
		return
	}
	defer file.Close()

	b, err := ioutil.ReadAll(file)
	if err != nil {
		return
	}

	fmt.Fprintf(text, "%s", b)

	return
}
