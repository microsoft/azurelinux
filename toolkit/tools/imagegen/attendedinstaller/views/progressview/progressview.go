// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package progressview

import (
	"sync"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
	"github.com/sirupsen/logrus"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/progressbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// UI constants.
const (
	defaultPadding    = 1
	defaultProportion = 1
	defaultMoreDetail = false

	logTextHeight = 0
)

// ProgressView contains the Progress UI
type ProgressView struct {
	// UI elements
	app                 *tview.Application
	flex                *tview.Flex
	logText             *tview.TextView
	progressBar         *progressbar.ProgressBar
	centeredProgressBar *tview.Flex

	// Generate state
	alreadyShown bool
	moreDetails  bool

	// Callbacks
	performInstallation func(chan int, chan string)
	nextPage            func()
	quit                func()
}

// New creates and returns a new ProgressView.
func New(performInstallation func(chan int, chan string)) *ProgressView {
	return &ProgressView{
		moreDetails:         defaultMoreDetail,
		performInstallation: performInstallation,
	}
}

// Initialize initializes the view.
func (pv *ProgressView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	pv.app = app
	pv.nextPage = nextPage
	pv.quit = quit

	pv.logText = tview.NewTextView().
		SetWordWrap(true).
		SetScrollable(false).
		SetDynamicColors(true).
		SetChangedFunc(func() {
			app.Draw()
		})

	pv.progressBar = progressbar.NewProgressBar().
		SetChangedFunc(func() {
			app.Draw()
		})

	pv.centeredProgressBar = uiutils.CenterVertically(pv.progressBar.GetHeight(), pv.progressBar)

	pv.flex = tview.NewFlex().SetDirection(tview.FlexRow)

	pv.switchDetailLevel(pv.moreDetails)

	// Box styling
	pv.logText.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)

	pv.flex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (pv *ProgressView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	switch event.Key() {
	// Prevent exiting the UI here as installation has already begun.
	case tcell.KeyCtrlC:
		return nil
	case tcell.KeyCtrlA:
		pv.switchDetailLevel(!pv.moreDetails)
	}

	return event
}

// Reset resets the page, undoing any user input.
func (pv *ProgressView) Reset() (err error) {
	return
}

// Name returns the friendly name of the view.
func (pv *ProgressView) Name() string {
	return "PROGRESS"
}

// Title returns the title of the view.
func (pv *ProgressView) Title() string {
	return uitext.ProgressTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (pv *ProgressView) Primitive() tview.Primitive {
	return pv.flex
}

// OnShow gets called when the view is shown to the user.
func (pv *ProgressView) OnShow() {
	if pv.alreadyShown {
		logger.Log.Panicf("ProgressView shown more than once, unsupported behavior.")
	}

	pv.alreadyShown = true

	go pv.startInstallation()
}

func (pv *ProgressView) switchDetailLevel(moreDetail bool) {
	pv.moreDetails = moreDetail

	if moreDetail {
		pv.flex.RemoveItem(pv.centeredProgressBar)
		pv.flex.AddItem(pv.logText, logTextHeight, defaultProportion, true)
	} else {
		pv.flex.RemoveItem(pv.logText)
		pv.flex.AddItem(pv.centeredProgressBar, 0, defaultProportion, true)
	}
}

func (pv *ProgressView) startInstallation() {
	// Redirect the logger to the progress text
	originalStderrWriter := logger.ReplaceStderrWriter(pv.logText)
	originalFormatter := logger.ReplaceStderrFormatter(&logrus.TextFormatter{
		DisableColors: true,
		FullTimestamp: false,
	})

	defer func() {
		logger.ReplaceStderrWriter(originalStderrWriter)
		logger.ReplaceStderrFormatter(originalFormatter)
	}()

	progress := make(chan int)
	status := make(chan string)

	wg := new(sync.WaitGroup)
	wg.Add(2)

	go pv.monitorProgress(progress, wg)
	go pv.monitorStatus(status, wg)

	pv.performInstallation(progress, status)

	wg.Wait()

	pv.nextPage()
}

func (pv *ProgressView) monitorProgress(progress chan int, wg *sync.WaitGroup) {
	for progressUpdate := range progress {
		pv.progressBar.SetProgress(progressUpdate)
	}

	wg.Done()
}

func (pv *ProgressView) monitorStatus(status chan string, wg *sync.WaitGroup) {
	for statusUpdate := range status {
		pv.progressBar.SetStatus(statusUpdate)
	}

	wg.Done()
}
