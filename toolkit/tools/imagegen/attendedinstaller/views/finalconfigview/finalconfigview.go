package finalconfigview

import (
	"fmt"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
)

// FinalConfigView displays the final configuration to the user.
type FinalConfigView struct {
	app         *tview.Application
	text        *tview.TextView
	navBar      *navigationbar.NavigationBar
	finalConfig *configuration.Config
	layout      *tview.Flex
}

// New creates and returns a new FinalConfigView.
func New() *FinalConfigView {
	return &FinalConfigView{}
}

// Initialize initializes the view.
func (fcv *FinalConfigView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	fcv.app = app
	fcv.finalConfig = cfg

	// Create the text view to display the final configuration
	fcv.text = tview.NewTextView().
		SetDynamicColors(true).
		SetText(fmt.Sprintf("Final Configuration:\n\n%+v", *fcv.finalConfig)).
		SetWrap(true)

	// Create the navigation bar
	fcv.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.ButtonNext, nextPage)

	// Create the layout
	fcv.layout = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(fcv.text, 0, 1, false).
		AddItem(fcv.navBar, 1, 0, true)

	return
}

// Primitive returns the primary primitive to be rendered for the view.
func (fcv *FinalConfigView) Primitive() tview.Primitive {
	return fcv.layout
}

// OnShow gets called when the view is shown to the user.
func (fcv *FinalConfigView) OnShow() {
	// Update the text view with the latest finalConfig
	fcv.text.SetText(fmt.Sprintf("Final Configuration:\n\n%+v", *fcv.finalConfig))
}

// Reset resets the page, undoing any user input.
func (fcv *FinalConfigView) Reset() (err error) {
	// No state to reset for this view
	return nil
}

// Name returns the friendly name of the view.
func (fcv *FinalConfigView) Name() string {
	return "FINAL CONFIG"
}

// Title returns the title of the view.
func (fcv *FinalConfigView) Title() string {
	return "Review Final Configuration"
}

// HandleInput handles custom input for the view.
func (fcv *FinalConfigView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	// If no custom input handling is needed, just return the event as-is.
	return event
}
