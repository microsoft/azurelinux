// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installerview

import (
	"fmt"
	"os/exec"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/customshortcutlist"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/speakuputils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// UI constants.
const (
	// default to <Next>
	defaultNavButton = 1
	defaultPadding   = 1

	listProportion = 0

	navBarHeight     = 0
	navBarProportion = 1
)

const (
	terminalUISpeechOption = iota
	terminalUINoSpeechOption
	calamaresUIOption
)

// InstallerView contains the installer selection UI.
type InstallerView struct {
	optionList       *customshortcutlist.List
	navBar           *navigationbar.NavigationBar
	flex             *tview.Flex
	centeredFlex     *tview.Flex
	installerOptions []string
	needsToPrompt    bool

	calamaresInstallFunc func()
}

// New creates and returns a new InstallerView.
func New(calamaresInstallFunc func()) *InstallerView {
	const calamaresToolName = "calamares"

	iv := &InstallerView{
		calamaresInstallFunc: calamaresInstallFunc,
	}

	iv.installerOptions = []string{uitext.InstallerTerminalOption, uitext.InstallerTerminalNoSpeechOption}

	_, err := exec.LookPath(calamaresToolName)
	if err != nil {
		logger.Log.Debugf("Calamares not found, defaulting to terminal based installer")
	} else {
		iv.installerOptions = append(iv.installerOptions, uitext.InstallerGraphicalOption)
	}

	iv.needsToPrompt = (len(iv.installerOptions) != 1)

	return iv
}

// Initialize initializes the view.
func (iv *InstallerView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	iv.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.ButtonNext, func() {
			iv.onNextButton(nextPage)
		}).
		SetAlign(tview.AlignCenter)

	iv.optionList = customshortcutlist.NewList().
		ShowSecondaryText(false)

	err = iv.populateInstallerOptions()
	if err != nil {
		return
	}

	listWidth, listHeight := uiutils.MinListSize(iv.optionList)
	centeredList := uiutils.Center(listWidth, listHeight, iv.optionList)

	iv.flex = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(centeredList, listHeight, listProportion, true).
		AddItem(iv.navBar, navBarHeight, navBarProportion, false)

	iv.centeredFlex = uiutils.CenterVerticallyDynamically(iv.flex)

	// Box styling
	iv.optionList.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)

	iv.centeredFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (iv *InstallerView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	if iv.navBar.UnfocusedInputHandler(event) {
		return nil
	}

	return event
}

// NeedsToPrompt returns true if this view should be shown to the user so an installer can be selected.
func (iv *InstallerView) NeedsToPrompt() bool {
	return iv.needsToPrompt
}

// Reset resets the page, undoing any user input.
func (iv *InstallerView) Reset() (err error) {
	iv.navBar.ClearUserFeedback()
	iv.navBar.SetSelectedButton(defaultNavButton)

	iv.optionList.SetCurrentItem(0)

	return
}

// Name returns the friendly name of the view.
func (iv *InstallerView) Name() string {
	return "INSTALLER"
}

// Title returns the title of the view.
func (iv *InstallerView) Title() string {
	return uitext.InstallerExperienceTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (iv *InstallerView) Primitive() tview.Primitive {
	return iv.centeredFlex
}

// OnShow gets called when the view is shown to the user
func (iv *InstallerView) OnShow() {
	err := speakuputils.StartSpeakup()
	if err != nil {
		logger.Log.Warnf("Failed to start speakup, continuing")
		err = nil
	}
}

func (iv *InstallerView) onNextButton(nextPage func()) {
	switch iv.optionList.GetCurrentItem() {
	case terminalUINoSpeechOption:
		err := speakuputils.StopSpeakup()
		if err != nil {
			logger.Log.Warnf("Failed to stop speakup, continuing")
			err = nil
		}
		fallthrough
	case terminalUISpeechOption:
		nextPage()
	case calamaresUIOption:
		iv.calamaresInstallFunc()
	default:
		logger.Log.Panicf("Unknown installer option: %d", iv.optionList.GetCurrentItem())
	}
}

func (iv *InstallerView) populateInstallerOptions() (err error) {
	if len(iv.installerOptions) == 0 {
		return fmt.Errorf("no installer options found")
	}

	for _, option := range iv.installerOptions {
		iv.optionList.AddItem(option, "", 0, nil)
	}

	return
}
