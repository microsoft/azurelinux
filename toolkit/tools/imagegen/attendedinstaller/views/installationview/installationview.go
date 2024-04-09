// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installationview

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/customshortcutlist"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
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

// InstallationView contains the package list UI
type InstallationView struct {
	optionList     *customshortcutlist.List
	navBar         *navigationbar.NavigationBar
	flex           *tview.Flex
	centeredFlex   *tview.Flex
	installOptions []string
	needsToPrompt  bool

	templateConfig configuration.Config
}

// New creates and returns a new InstallationView.
func New(sysConfig *configuration.SystemConfig, templateConfig configuration.Config) *InstallationView {
	const defaultSysConfig = 0

	iv := &InstallationView{
		templateConfig: templateConfig,
	}

	iv.installOptions = make([]string, len(iv.templateConfig.SystemConfigs))
	iv.needsToPrompt = (len(iv.installOptions) != 1)

	if iv.needsToPrompt {
		for i, systemConfig := range iv.templateConfig.SystemConfigs {
			iv.installOptions[i] = systemConfig.Name
		}
	} else {
		iv.applyConfiguration(sysConfig, defaultSysConfig)
	}

	return iv
}

// Initialize initializes the view.
func (iv *InstallationView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	iv.navBar = navigationbar.NewNavigationBar().
		AddButton(uitext.ButtonGoBack, previousPage).
		AddButton(uitext.ButtonNext, func() {
			iv.applyConfiguration(sysConfig, iv.optionList.GetCurrentItem())
			nextPage()
		}).
		SetAlign(tview.AlignCenter)

	iv.optionList = customshortcutlist.NewList().
		ShowSecondaryText(false)

	err = iv.populateInstallOptions()
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
func (iv *InstallationView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	if iv.navBar.UnfocusedInputHandler(event) {
		return nil
	}

	return event
}

// NeedsToPrompt returns true if this view should be shown to the user so a system configuration can be selected.
func (iv *InstallationView) NeedsToPrompt() bool {
	return iv.needsToPrompt
}

// Reset resets the page, undoing any user input.
func (iv *InstallationView) Reset() (err error) {
	iv.navBar.ClearUserFeedback()
	iv.navBar.SetSelectedButton(defaultNavButton)

	iv.optionList.SetCurrentItem(0)

	return
}

// Name returns the friendly name of the view.
func (iv *InstallationView) Name() string {
	return "INSTALLATION"
}

// Title returns the title of the view.
func (iv *InstallationView) Title() string {
	return uitext.InstallationTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (iv *InstallationView) Primitive() tview.Primitive {
	return iv.centeredFlex
}

// OnShow gets called when the view is shown to the user
func (iv *InstallationView) OnShow() {
}

func (iv *InstallationView) applyConfiguration(sysConfig *configuration.SystemConfig, selectedConfigIndex int) {
	selectedConfig := iv.templateConfig.SystemConfigs[selectedConfigIndex]
	sysConfig.Name = selectedConfig.Name
	sysConfig.IsDefault = true
	sysConfig.PackageLists = selectedConfig.PackageLists
	sysConfig.KernelOptions = selectedConfig.KernelOptions
	sysConfig.KernelCommandLine = selectedConfig.KernelCommandLine
	sysConfig.ReadOnlyVerityRoot = selectedConfig.ReadOnlyVerityRoot
	sysConfig.AdditionalFiles = selectedConfig.AdditionalFiles
	sysConfig.PostInstallScripts = selectedConfig.PostInstallScripts
	sysConfig.FinalizeImageScripts = selectedConfig.FinalizeImageScripts
	sysConfig.EnableGrubMkconfig = selectedConfig.EnableGrubMkconfig
}

func (iv *InstallationView) populateInstallOptions() (err error) {
	if len(iv.installOptions) == 0 {
		return fmt.Errorf("no install options found in base configuration")
	}

	for _, option := range iv.installOptions {
		iv.optionList.AddItem(option, "", 0, nil)
	}

	return
}
