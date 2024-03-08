// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package uitext

// Useful prefix strings
const (
	RequiredInputMark = "* "
	BoldPrefix        = "[::b]"
	WhiteBoldPrefix   = "[#ffffff::b]"
)

// "]" is a special character for the TUI text, escape it with "[]"

// Navigation text.
const (
	ButtonAccept          = "[Accept[]"
	ButtonCancel          = "[Cancel[]"
	ButtonCancelWhiteBold = WhiteBoldPrefix + ButtonCancel
	ButtonConfirm         = "[Confirm[]"
	ButtonGoBack          = "[Go Back[]"
	ButtonNext            = "[Next[]"
	ButtonYes             = "[Yes[]"
	ButtonQuit            = "[Quit[]"
	ButtonQuitWhiteBold   = WhiteBoldPrefix + ButtonQuit
	ButtonRestart         = "[Restart[]"
)

// AttendedInstaller wrapper text.
const (
	NavigationHelp = "Arrow keys make selections. Enter activates."
	ExitModalTitle = BoldPrefix + "Do you want to quit setup?"
)

// ConfirmView text.
const (
	ConfirmTitle  = "Confirm"
	ConfirmPrompt = `Start installation?
All data on the selected disk will be lost.`
)

// DiskView text.
const (
	// Buttons
	DiskButtonAddPartition    = "[Add Partition[]"
	DiskButtonAuto            = "[Auto Partition[]"
	DiskButtonCustom          = "[Custom Partition[]"
	DiskButtonRemovePartition = "[Remove Partition[]"

	// Auto partition
	DiskHelp  = "Please select a disk to install Azure Linux on."
	DiskTitle = "Select a Disk"

	// Custom Partition
	DiskAdvanceTitleFmt      = "Partitions for: %v"
	DiskAddPartitionTitle    = "Add Partition"
	DiskFormatLabel          = "Format"
	DiskMountPointLabel      = "Mount Point"
	DiskNameLabel            = "Name"
	DiskSizeLabel            = "Size"
	DiskSpaceLeftFmt         = "Remaining space: %v"
	FormDiskSizeLabelMaxHelp = "(* for max)"
	FormDiskSizeUnitLabel    = "* Unit size"
	FormDiskFormatLabel      = RequiredInputMark + DiskFormatLabel
	FormDiskMountPointLabel  = RequiredInputMark + DiskMountPointLabel
	FormDiskNameLabel        = RequiredInputMark + DiskNameLabel
	FormDiskSizeLabel        = RequiredInputMark + DiskSizeLabel

	// Errors
	InvalidBootPartitionErrorFmt       = "Invalid boot partition: first partition must be of type (%s)"
	InvalidRootPartitionErrorFmt       = "Must specify a partition to have the mount point (%s)"
	InvalidRootDeviceMapperError       = "Must have a root to use with device mapper roots (Encryption, Read-Only)"
	InvalidRootPartitionErrorFormatFmt = "Root partition cannot be %s"
	MountPointAlreadyInUseError        = "Mount point is already in use"
	MountPointStartError               = "Mount point must start with `/`"
	MountPointInvalidCharacterError    = "Mount point only supports alphanumeric characters and `/`"
	NameInvalidCharacterError          = "Name only supports alphanumeric characters"
	NoPartitionsError                  = "Must specify at least one boot and one root partition"
	NoPartitionSelectedError           = "No partition selected"
	NoSizeSpecifiedError               = "Size must be specified"
	NotEnoughDiskSpaceError            = "Not enough space left on disk"
	PartitionExceedsDiskErrorFmt       = "Device space exceeded by partition (%d)"
	SizeStartError                     = "Size can not start with `0`"
	SizeInvalidCharacterError          = "Size must be a number"
	UnexpectedPartitionErrorFmt        = "Unexpected partition size (%s)"
)

// EncryptView text.
const (
	EncryptTitle                = "Enter Disk Encryption Password"
	SkipEncryption              = "[Skip Disk Encryption[]"
	EncryptPasswordLabel        = "* Disk Encryption Password"
	ConfirmEncryptPasswordLabel = "* Confirm Disk Encryption Password"
)

// InstallerView text.
const (
	InstallerExperienceTitle        = "Select Installation Experience"
	InstallerTerminalNoSpeechOption = "Terminal Installer"
	InstallerTerminalOption         = InstallerTerminalNoSpeechOption + " (Speech Enabled)"
	InstallerGraphicalOption        = "Graphical Installer"
)

// EulaView text.
const (
	EulaTitle = "Welcome to the Azure Linux Installer"
)

// HostNameView text.
const (
	HostNameTitle      = "Choose the Host Name for Your System"
	HostNameInputLabel = "* Host Name:"

	HostNameSegment   = "host name"
	DomainNameSegment = "domain name"

	FQDNEmptyErrorFmt         = "empty (%s) is not allowed"
	FQDNEndsInDashErrorFmt    = "(%s) should not end with '-'"
	FQDNInvalidRuneErrorFmt   = "(%s) should only contain alpha-numeric, '.' and '-' characters"
	FQDNInvalidStartErrorFmt  = "(%s) should start with an alpha character"
	FQDNInvalidLengthErrorFmt = "host name must be <= (%d) characters"
)

// InstallationView text.
const (
	InstallationTitle = "Select Installation Type"
)

// UserView text.
const (
	SetupUserTitle = "Set Up User Account"

	PasswordInputLabel        = "* Password"
	ConfirmPasswordInputLabel = "* Confirm Password"
	UserNameInputLabel        = "* User Name"

	PasswordMismatchFeedback = "Passwords do not match"
	EnumNavigationFeedback   = "Use left or right arrow keys to change the selection"

	EncryptionVerityIncompatible = "Encrypted and read-only roots are currently incompatible with each other"

	UserNameEmptyError            = "user name cannot be empty"
	UserNameInvalidRuneError      = "user name should only contain alpha-numeric and '-', '.' or '_' characters"
	UserNameInvalidStartError     = "user name should start with an alpha-numeric character"
	UserNameInvalidLengthErrorFmt = "user name must be <= (%d) characters"
)

// ProgressView text.
const (
	ProgressTitle      = "Installing Azure Linux OS"
	ProgressSpinnerFmt = "Installing Azure Linux, please wait (%v)"
)

// FinishView text.
const (
	FinishTitle   = "Azure Linux Installation Complete"
	FinishTextFmt = "Total installation time: (%v) seconds. Press Enter to restart."
)
