// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package attendedinstaller

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/speakuputils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/confirmview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/diskview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/encryptview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/eulaview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/finishview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/hostnameview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/installationview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/installerview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/progressview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/userview"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"github.com/bendahl/uinput"
	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
)

// UI constants.
const (
	defaultGridWeight = 1

	textRow        = 3
	textColumn     = 0
	textRowSpan    = 1
	textColumnSpan = 1
	textMinSize    = 0

	helpTextPadding       = 2
	helpTextProportion    = 0
	versionTextMinSize    = 0
	versionTextProportion = 1

	titleTextProportion = 1
	titleRow            = 0
	titleColumn         = 0
	titleRowSpan        = 1
	titleColumnSpan     = 1

	primaryContentRow        = 1
	primaryContentColumn     = 0
	primaryContentRowSpan    = 1
	primaryContentColumnSpan = 1
	primaryContentMinSize    = 0
	primaryContentGridWeight = -100
)

// AttendedInstaller contains the attended installer configuration
type AttendedInstaller struct {
	app               *tview.Application
	exitModal         *tview.Modal
	grid              *tview.Grid
	pauseCustomInput  bool
	pauseSpeakupInput bool
	currentView       int
	allViews          []views.View
	backdropStyle     tview.Theme
	titleText         *tview.TextView
	keyboard          uinput.Keyboard

	installationFunc     func(configuration.Config, chan int, chan string) error
	calamaresInstallFunc func() error
	installationError    error
	installationTime     time.Duration
	userQuitInstallation bool

	systemConfig *configuration.SystemConfig

	templateConfig configuration.Config
	finalConfig    configuration.Config
}

// New creates and returns a new AttendedInstaller.
func New(cfg configuration.Config, installationFunc func(configuration.Config, chan int, chan string) error, calamaresInstallFunc func() error) (attendedInstaller *AttendedInstaller, err error) {
	finalConfig := configuration.Config{
		SystemConfigs: []configuration.SystemConfig{
			configuration.SystemConfig{},
		},
	}

	attendedInstaller = &AttendedInstaller{
		templateConfig:       cfg,
		finalConfig:          finalConfig,
		systemConfig:         &finalConfig.SystemConfigs[0],
		installationFunc:     installationFunc,
		calamaresInstallFunc: calamaresInstallFunc,
	}

	err = attendedInstaller.initializeUI()
	return
}

// Run shows the attended installer UI on the current thread.
// When the user completes the installer, the function will return.
func (ai *AttendedInstaller) Run() (config configuration.Config, installationQuit bool, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("unexpected failure: %v", r)
		}
	}()

	// Close virtual keyboard when installer exits, if we have a keyboard
	if ai.keyboard != nil {
		defer ai.keyboard.Close()
	}

	// Backup the original stderr writer and replace it will a null writer.
	// If the logger prints to the console while the UI is shown, it will conflict
	// with the TUI (terminal UI) and result in undefined behavior.
	// The log hooks that enable file logging will remain intact and still record
	// logs.
	originalStderrWriter := logger.ReplaceStderrWriter(ioutil.Discard)
	defer func() {
		logger.ReplaceStderrWriter(originalStderrWriter)
	}()

	err = ai.app.SetRoot(ai.grid, true).Run()
	if err != nil {
		return
	}

	installationQuit = ai.userQuitInstallation
	if ai.userQuitInstallation {
		return
	}

	err = ai.installationError
	if err != nil {
		return
	}

	ai.finalConfig.SetDefaultConfig()

	config = ai.finalConfig

	return
}

func (ai *AttendedInstaller) nextPage() {
	ai.app.QueueUpdateDraw(func() {
		err := ai.switchToView(ai.currentView + 1)
		logger.PanicOnError(err, "Failed to go to next page")
	})
}

func (ai *AttendedInstaller) previousPage() {
	ai.app.QueueUpdateDraw(func() {
		err := ai.switchToView(ai.currentView - 1)
		logger.PanicOnError(err, "Failed to go to previous page")
	})
}

func (ai *AttendedInstaller) switchToView(newView int) (err error) {
	if newView == len(ai.allViews) {
		ai.app.Stop()
		return
	} else if newView == -1 {
		ai.quit()
		return
	}

	ai.grid.RemoveItem(ai.allViews[ai.currentView].Primitive())
	err = ai.showView(newView)
	return
}

func (ai *AttendedInstaller) showView(newView int) (err error) {
	view := ai.allViews[newView]

	logger.Log.Debugf("Showing view: %s", view.Name())

	// Clear the text-to-speech buffer when we change pages
	ai.pauseSpeakupInput = true
	err = speakuputils.ClearSpeakupBuffer(ai.keyboard)
	if err != nil {
		logger.Log.Warnf("Error clearing speakup buffer")
		err = nil
	}
	ai.pauseSpeakupInput = false

	err = view.Reset()
	if err != nil {
		return
	}

	ai.grid.AddItem(view.Primitive(), primaryContentRow, primaryContentColumn, primaryContentRowSpan, primaryContentColumnSpan, primaryContentMinSize, primaryContentMinSize, true)
	ai.app.SetFocus(ai.grid)
	ai.currentView = newView
	view.OnShow()
	ai.refreshTitle()

	return
}

func (ai *AttendedInstaller) refreshTitle() {
	ai.titleText.SetText(ai.allViews[ai.currentView].Title())
}

func (ai *AttendedInstaller) quit() {
	ai.pauseCustomInput = true
	// Set focus on the cancel option
	ai.exitModal.SetFocus(1)
	ai.grid.AddItem(ai.exitModal, primaryContentRow, primaryContentColumn, primaryContentRowSpan, primaryContentColumnSpan, primaryContentMinSize, primaryContentMinSize, true)
	ai.app.SetFocus(ai.exitModal)
}

func (ai *AttendedInstaller) globalInputCapture(event *tcell.EventKey) *tcell.EventKey {
	// If we're clearing the speakup buffer, don't process keypresses
	// tcell has no easy way of differentiating between keypad enter (speakup clear) and enter
	if ai.pauseSpeakupInput && event.Key() == tcell.KeyEnter {
		return nil
	}
	if !ai.pauseCustomInput {
		event = ai.allViews[ai.currentView].HandleInput(event)
		if event == nil {
			return nil
		}
	}

	switch event.Key() {
	case tcell.KeyCtrlC:
		event = nil
		ai.app.QueueUpdateDraw(func() {
			ai.quit()
		})
	}

	return event
}

func (ai *AttendedInstaller) initializeUI() (err error) {
	ai.keyboard, err = speakuputils.CreateVirtualKeyboard()
	if err != nil {
		// Non-fatal - results in a slightlydegraded experience due to the lack of a
		// text-to-speech buffer clear between views, but not bad enough to exit outright
		logger.Log.Warnf("Failed to initialize virtual keyboard via uinput")
		err = nil
	}
	err = speakuputils.SetHighlightTrackingMode(ai.keyboard)
	if err != nil {
		logger.Log.Warnf("Error setting highlight tracking mode for speakup")
		err = nil
	}

	const osReleaseFile = "/etc/os-release"

	// For "bright" colors, we need to manually specify RGB values
	// As they do not nhave
	ai.backdropStyle = tview.Theme{
		PrimitiveBackgroundColor:    tcell.ColorBlack,
		ContrastBackgroundColor:     tcell.ColorWhite,
		MoreContrastBackgroundColor: tcell.ColorDarkBlue,
		BorderColor:                 tcell.ColorBlack,
		TitleColor:                  tcell.ColorWhite,
		GraphicsColor:               tcell.ColorWhite,
		PrimaryTextColor:            tcell.ColorWhite,
		SecondaryTextColor:          tcell.ColorBlack,
		TertiaryTextColor:           tcell.ColorRed,
		InverseTextColor:            tcell.ColorGreen,
		ContrastSecondaryTextColor:  tcell.ColorWhite,
	}

	tview.Styles = tview.Theme{
		PrimitiveBackgroundColor:    tcell.ColorBlack,
		ContrastBackgroundColor:     tcell.ColorBlack,
		MoreContrastBackgroundColor: tcell.ColorGreen,
		BorderColor:                 tcell.ColorRed,
		TitleColor:                  tcell.ColorWhite,
		GraphicsColor:               tcell.ColorGreen,
		PrimaryTextColor:            tcell.ColorWhite,
		SecondaryTextColor:          tcell.ColorDarkCyan,
		TertiaryTextColor:           tcell.ColorRed,
		InverseTextColor:            tcell.ColorBlack,
		ContrastSecondaryTextColor:  tcell.ColorGreen,
	}

	ai.app = tview.NewApplication()

	helpText := tview.NewTextView().
		SetTextColor(ai.backdropStyle.PrimaryTextColor).
		SetText(uitext.NavigationHelp).
		SetChangedFunc(func() {
			ai.app.Draw()
		})

	releaseVer, err := releaseVersion(osReleaseFile)
	if err != nil {
		return
	}

	osVersionText := tview.NewTextView().
		SetTextAlign(tview.AlignRight).
		SetTextColor(ai.backdropStyle.PrimaryTextColor).
		SetText(releaseVer).
		SetChangedFunc(func() {
			ai.app.Draw()
		})

	ai.titleText = tview.NewTextView().
		SetTextColor(ai.backdropStyle.PrimaryTextColor).
		SetTextAlign(tview.AlignCenter).
		SetChangedFunc(func() {
			ai.app.Draw()
		})

	err = ai.initializeViews()
	if err != nil {
		return
	}

	// Create a flex box to hold all global text in the same grid space
	helpTextMinSize := tview.TaggedStringWidth(helpText.GetText(false)) + helpTextPadding
	textFlex := tview.NewFlex().
		SetDirection(tview.FlexColumn).
		AddItem(helpText, helpTextMinSize, helpTextProportion, false).
		AddItem(osVersionText, versionTextMinSize, versionTextProportion, false)

	titleFlex := tview.NewFlex().
		SetDirection(tview.FlexColumn).
		AddItem(ai.titleText, textMinSize, titleTextProportion, false)

	ai.grid = tview.NewGrid().
		SetRows(defaultGridWeight, primaryContentGridWeight, defaultGridWeight).
		SetColumns(primaryContentGridWeight).
		AddItem(titleFlex, titleRow, titleColumn, titleRowSpan, titleColumnSpan, textMinSize, helpTextMinSize, false).
		AddItem(textFlex, textRow, textColumn, textRowSpan, textColumnSpan, textMinSize, textMinSize, false)

	ai.exitModal = tview.NewModal().
		SetText(uitext.ExitModalTitle).
		AddButtons([]string{uitext.ButtonQuitWhiteBold, uitext.ButtonCancelWhiteBold}).
		SetBackgroundColor(ai.backdropStyle.TertiaryTextColor).
		SetButtonBackgroundColor(ai.backdropStyle.TertiaryTextColor).
		SetTextColor(ai.backdropStyle.ContrastSecondaryTextColor).
		SetButtonTextColor(ai.backdropStyle.PrimitiveBackgroundColor).
		SetDoneFunc(func(buttonIndex int, buttonLabel string) {
			if buttonLabel == uitext.ButtonQuitWhiteBold {
				ai.userQuitInstallation = true
				ai.app.Stop()
			} else {
				ai.grid.RemoveItem(ai.exitModal)
				ai.app.SetFocus(ai.grid)
				ai.pauseCustomInput = false
			}
		})

	helpText.SetBackgroundColor(ai.backdropStyle.ContrastBackgroundColor)
	osVersionText.SetBackgroundColor(ai.backdropStyle.ContrastBackgroundColor)
	textFlex.SetBackgroundColor(ai.backdropStyle.ContrastBackgroundColor)
	titleFlex.SetBackgroundColor(ai.backdropStyle.ContrastBackgroundColor)
	ai.titleText.SetBackgroundColor(ai.backdropStyle.ContrastBackgroundColor)

	helpText.SetTextColor(ai.backdropStyle.SecondaryTextColor)
	osVersionText.SetTextColor(ai.backdropStyle.SecondaryTextColor)
	ai.titleText.SetTextColor(ai.backdropStyle.SecondaryTextColor)

	ai.showView(ai.currentView)
	ai.app.SetInputCapture(ai.globalInputCapture)

	return
}

func (ai *AttendedInstaller) initializeViews() (err error) {
	installerView := installerview.New(ai.installWithCalamaresWrapper)
	if installerView.NeedsToPrompt() {
		ai.allViews = append(ai.allViews, installerView)
	}

	ai.allViews = append(ai.allViews, eulaview.New())

	installationView := installationview.New(ai.systemConfig, ai.templateConfig)
	if installationView.NeedsToPrompt() {
		ai.allViews = append(ai.allViews, installationView)
	}

	ai.allViews = append(ai.allViews, diskview.New())
	ai.allViews = append(ai.allViews, encryptview.New())
	ai.allViews = append(ai.allViews, hostnameview.New())
	ai.allViews = append(ai.allViews, userview.New())
	ai.allViews = append(ai.allViews, confirmview.New())
	ai.allViews = append(ai.allViews, progressview.New(ai.installationWrapper))
	ai.allViews = append(ai.allViews, finishview.New(ai.recordedInstallationTime))

	for i, view := range ai.allViews {
		var backButtonText string

		if i == 0 {
			backButtonText = uitext.ButtonCancel
		} else {
			backButtonText = uitext.ButtonGoBack
		}

		err = view.Initialize(backButtonText, ai.systemConfig, &ai.finalConfig, ai.app, ai.nextPage, ai.previousPage, ai.quit, ai.refreshTitle)
		if err != nil {
			return
		}
	}

	return
}

func (ai *AttendedInstaller) installWithCalamaresWrapper() {
	ai.app.Stop()
	ai.installationError = ai.calamaresInstallFunc()
}

func (ai *AttendedInstaller) installationWrapper(progress chan int, status chan string) {
	defer func() {
		if r := recover(); r != nil {
			ai.installationError = fmt.Errorf("unexptected failure: %v", r)
			ai.app.Stop()
		}
	}()

	startTime := time.Now()
	ai.installationError = ai.installationFunc(ai.finalConfig, progress, status)
	ai.installationTime = time.Since(startTime)

	// On error, gracefully stop the installation
	if ai.installationError != nil {
		ai.app.Stop()
	}
}

func (ai *AttendedInstaller) recordedInstallationTime() time.Duration {
	return ai.installationTime
}

func releaseVersion(releaseFile string) (version string, err error) {
	const attributeName = "VERSION"

	logger.Log.Debug("Searching release file for version")
	logger.Log.Debugf("releaseFile = %s", releaseFile)
	logger.Log.Debugf("attributeName = %s", attributeName)

	file, err := os.Open(releaseFile)
	if err != nil {
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// format: FIELD=VALUE
		line := strings.TrimSpace(scanner.Text())

		if !strings.HasPrefix(line, attributeName) {
			continue
		}

		attribute := strings.Split(line, "=")
		if len(attribute) != 2 {
			logger.Log.Warnf("Unexpected format found, skipping: %s", line)
			continue
		}

		attributeValue := strings.TrimSpace(attribute[1])
		// Remove any wrapping double quotes.
		if len(attributeValue) > 1 && strings.HasPrefix(attributeValue, `"`) {
			version = attributeValue[1 : len(attributeValue)-1]
		} else {
			version = attributeValue
		}

		return
	}

	err = fmt.Errorf("unable to find release version in file (%s)", releaseFile)
	return
}
