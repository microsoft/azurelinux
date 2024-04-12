// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package diskview

import (
	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/diskview/autopartitionwidget"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/views/diskview/manualpartitionwidget"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// UI constants.
const (
	resizeWidgetes         = true
	defaultToAutoPartition = true
)

// DiskView contains the disk selection UI
type DiskView struct {
	systemDevices         []diskutils.SystemBlockDevice
	pages                 *tview.Pages
	autoPartitionMode     bool
	autoPartitionWidget   *autopartitionwidget.AutoPartitionWidget
	manualPartitionWidget *manualpartitionwidget.ManualPartitionWidget

	refreshTitle func()
}

// New creates and returns a new DiskView.
func New() *DiskView {
	return &DiskView{}
}

// Initialize initializes the view.
func (dv *DiskView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	err = dv.populateBlockDeviceOptions()
	if err != nil {
		return
	}

	bootType := configuration.SystemBootType()
	logger.Log.Infof("Boot type detected: %s", bootType)
	dv.autoPartitionWidget = autopartitionwidget.New(dv.systemDevices, bootType)
	err = dv.autoPartitionWidget.Initialize(backButtonText, sysConfig, cfg, app, dv.switchMode, nextPage, previousPage, quit, refreshTitle)
	if err != nil {
		return
	}

	dv.manualPartitionWidget = manualpartitionwidget.New(dv.systemDevices, bootType)
	err = dv.manualPartitionWidget.Initialize(backButtonText, sysConfig, cfg, app, dv.switchMode, nextPage, previousPage, quit, refreshTitle)
	if err != nil {
		return
	}

	dv.pages = tview.NewPages()
	dv.pages.AddPage(dv.autoPartitionWidget.Name(), dv.autoPartitionWidget.Primitive(), resizeWidgetes, defaultToAutoPartition)
	dv.pages.AddPage(dv.manualPartitionWidget.Name(), dv.manualPartitionWidget.Primitive(), resizeWidgetes, !defaultToAutoPartition)

	dv.autoPartitionMode = defaultToAutoPartition
	dv.refreshTitle = refreshTitle

	return
}

// HandleInput handles custom input.
func (dv *DiskView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	if dv.autoPartitionMode {
		return dv.autoPartitionWidget.HandleInput(event)
	}

	return dv.manualPartitionWidget.HandleInput(event)
}

// Reset resets the page, undoing any user input.
func (dv *DiskView) Reset() (err error) {
	err = dv.manualPartitionWidget.Reset()
	if err != nil {
		return
	}

	err = dv.autoPartitionWidget.Reset()
	if err != nil {
		return
	}

	if dv.autoPartitionMode != defaultToAutoPartition {
		dv.switchMode()
	}

	return
}

// Name returns the friendly name of the view.
func (dv *DiskView) Name() string {
	return "DISK"
}

// Title returns the title of the view.
func (dv *DiskView) Title() string {
	if dv.autoPartitionMode {
		return dv.autoPartitionWidget.Title()
	} else {
		return dv.manualPartitionWidget.Title()
	}
}

// Primitive returns the primary primitive to be rendered for the view.
func (dv *DiskView) Primitive() tview.Primitive {
	return dv.pages
}

func (dv *DiskView) switchMode() {
	if dv.autoPartitionMode {
		selectedBlockDevice := dv.autoPartitionWidget.SelectedSystemDevice()

		dv.manualPartitionWidget.Reset()
		dv.manualPartitionWidget.SetSystemDeviceIndex(selectedBlockDevice)
		dv.pages.SwitchToPage(dv.manualPartitionWidget.Name())
	} else {
		dv.autoPartitionWidget.Reset()
		dv.pages.SwitchToPage(dv.autoPartitionWidget.Name())
	}
	dv.autoPartitionMode = !dv.autoPartitionMode
	dv.refreshTitle()
}

// OnShow gets called when the view is shown to the user
func (dv *DiskView) OnShow() {
}

func (dv *DiskView) populateBlockDeviceOptions() (err error) {
	dv.systemDevices, err = diskutils.SystemBlockDevices()
	return
}
