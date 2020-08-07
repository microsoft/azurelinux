// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package autopartitionwidget

import (
	"fmt"

	"microsoft.com/pkggen/imagegen/attendedinstaller/primitives/customshortcutlist"
	"microsoft.com/pkggen/imagegen/attendedinstaller/primitives/navigationbar"
	"microsoft.com/pkggen/imagegen/attendedinstaller/uitext"
	"microsoft.com/pkggen/imagegen/attendedinstaller/uiutils"
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/diskutils"
	"microsoft.com/pkggen/internal/logger"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
)

// UI constants.
const (
	nextButtonIndex = 2
	defaultPadding  = 1

	textProportion = 0
	listProportion = 0

	navBarHeight     = 0
	navBarProportion = 1
)

// AutoPartitionWidget contains the disk selection UI
type AutoPartitionWidget struct {
	navBar       *navigationbar.NavigationBar
	flex         *tview.Flex
	centeredFlex *tview.Flex
	deviceList   *customshortcutlist.List
	helpText     *tview.TextView

	systemDevices []diskutils.SystemBlockDevice
	bootType      string
}

// New creates and returns a new AutoPartitionWidget.
func New(systemDevices []diskutils.SystemBlockDevice, bootType string) *AutoPartitionWidget {
	return &AutoPartitionWidget{
		systemDevices: systemDevices,
		bootType:      bootType,
	}
}

// Initialize initializes the view.
func (ap *AutoPartitionWidget) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, switchMode, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	ap.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.DiskButtonCustom, switchMode).
		AddButton(uitext.ButtonNext, func() {
			ap.mustUpdateConfiguration(sysConfig, cfg)
			nextPage()
		}).
		SetAlign(tview.AlignCenter)

	ap.deviceList = customshortcutlist.NewList().
		ShowSecondaryText(false)
	ap.populateBlockDeviceOptions()

	ap.helpText = tview.NewTextView().
		SetText(uitext.DiskHelp)

	textWidth, textHeight := uiutils.MinTextViewWithNoWrapSize(ap.helpText)
	centeredText := uiutils.Center(textWidth, textHeight, ap.helpText)

	listWidth, listHeight := uiutils.MinListSize(ap.deviceList)
	centeredList := uiutils.Center(listWidth, listHeight, ap.deviceList)

	ap.flex = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(centeredText, textHeight, textProportion, false).
		AddItem(centeredList, listHeight, listProportion, true).
		AddItem(ap.navBar, navBarHeight, navBarProportion, false)

	ap.centeredFlex = uiutils.CenterVerticallyDynamically(ap.flex)

	// Box styling
	ap.helpText.SetBorderPadding(defaultPadding, defaultPadding, defaultPadding, defaultPadding)
	ap.centeredFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (ap *AutoPartitionWidget) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	if ap.navBar.UnfocusedInputHandler(event) {
		return nil
	}

	return event
}

// Reset resets the page, undoing any user input.
func (ap *AutoPartitionWidget) Reset() (err error) {
	ap.deviceList.SetCurrentItem(0)
	ap.navBar.ClearUserFeedback()
	ap.navBar.SetSelectedButton(nextButtonIndex)

	return
}

// Name returns the friendly name of the view.
func (ap *AutoPartitionWidget) Name() string {
	return "AUTOPARTITIONWIDGET"
}

// Title returns the title of the view.
func (ap *AutoPartitionWidget) Title() string {
	return uitext.DiskTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (ap *AutoPartitionWidget) Primitive() tview.Primitive {
	return ap.centeredFlex
}

// SelectedSystemDevice returns the index of the currently selected system device.
func (ap *AutoPartitionWidget) SelectedSystemDevice() int {
	return ap.deviceList.GetCurrentItem()
}

func (ap *AutoPartitionWidget) mustUpdateConfiguration(sysConfig *configuration.SystemConfig, cfg *configuration.Config) {
	const (
		targetDiskType     = "path"
		partitionTableType = "gpt"

		bootPartitionName     = "boot"
		bootPartitionFsType   = "fat32"
		bootPartitionStartMiB = 1
		bootPartitionEndMiB   = 9

		rootPartitionName = "rootfs"
		rootFsType        = "ext4"
		rootMountPoint    = "/"
	)

	bootMountPoint, bootMountOptions, bootFlags, err := diskutils.BootPartitionConfig(ap.bootType)
	if err != nil {
		logger.Log.Panic(err)
	}

	partitions := []configuration.Partition{
		configuration.Partition{
			ID:     bootPartitionName,
			Name:   bootPartitionName,
			Start:  bootPartitionStartMiB,
			End:    bootPartitionEndMiB,
			FsType: bootPartitionFsType,
			Flags:  bootFlags,
		},
		configuration.Partition{
			ID:     rootPartitionName,
			Name:   rootPartitionName,
			Start:  bootPartitionEndMiB,
			End:    diskutils.AutoEndSize,
			FsType: rootFsType,
		},
	}

	partitionSettings := []configuration.PartitionSetting{
		configuration.PartitionSetting{
			ID:           bootPartitionName,
			MountPoint:   bootMountPoint,
			MountOptions: bootMountOptions,
		},
		configuration.PartitionSetting{
			ID:         rootPartitionName,
			MountPoint: rootMountPoint,
		},
	}

	disk := configuration.Disk{}
	disk.PartitionTableType = partitionTableType
	disk.TargetDisk = configuration.TargetDisk{
		Type:  targetDiskType,
		Value: ap.systemDevices[ap.deviceList.GetCurrentItem()].DevicePath,
	}
	disk.Partitions = partitions

	sysConfig.BootType = ap.bootType
	sysConfig.PartitionSettings = partitionSettings
	cfg.Disks = []configuration.Disk{disk}
}

func (ap *AutoPartitionWidget) populateBlockDeviceOptions() {
	for i, disk := range ap.systemDevices {
		formattedSize := diskutils.BytesToSizeAndUnit(disk.RawDiskSize)
		diskRepresentation := fmt.Sprintf("%s - %s @ %s", disk.Model, formattedSize, disk.DevicePath)
		currentRune := rune(i + 'a')
		ap.deviceList.AddItem(diskRepresentation, "", currentRune, nil)
	}
}
