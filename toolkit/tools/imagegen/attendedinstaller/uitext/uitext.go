// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package uitext

// "]" is a special character for the TUI text, escape it with "[]"

// Navigation text.
const (
	ButtonAccept  = "[Accept[]"
	ButtonCancel  = "[Cancel[]"
	ButtonConfirm = "[Confirm[]"
	ButtonGoBack  = "[Go Back[]"
	ButtonNext    = "[Next[]"
	ButtonYes     = "[Yes[]"
	ButtonQuit    = "[Quit[]"
	ButtonRestart = "[Restart[]"
)

// AttendedInstaller wrapper text.
const (
	NavigationHelp = "Arrow keys make selections. Enter activates."
	ExitModalTitle = "Do you want to quit setup?"
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
	DiskHelp  = "Please select a disk to install CBL-Mariner on."
	DiskTitle = "Select a Disk"

	// Custom Partition
	DiskAdvanceTitleFmt   = "Partitions for: %v"
	DiskAddPartitionTitle = "Add Partition"
	DiskFormatLabel       = "Format"
	DiskMountPointLabel   = "Mount Point"
	DiskNameLabel         = "Name"
	DiskSpaceLeftFmt      = "Remaining space: %v"
	DiskSizeLabel         = "Size"
	DiskSizeLabelMaxHelp  = "(* for max)"
	DiskSizeUnitLabel     = "Unit size"

	// Errors
	InvalidBootPartitionErrorFmt       = "Invalid boot partition: first partition must be of type '%s'"
	InvalidRootPartitionErrorFmt       = "Must specify a partition to have the mount point '%s'"
	InvalidRootPartitionErrorFormatFmt = "Root partition cannot be %s"
	MountPointAlreadyInUseError        = "Mount point is already in use"
	MountPointStartError               = "Mount point must start with `/`"
	MountPointInvalidCharacterError    = "Mount point only supports alphanumeric characters and `/`"
	NameInvalidCharacterError          = "Name only supports alphanumeric characters"
	NoFormatSelectedError              = "A format must be selected"
	NoPartitionsError                  = "Must specify at least one boot and one root partition"
	NoPartitionSelectedError           = "No partition selected"
	NoSizeSpecifiedError               = "Size must be specified"
	NotEnoughDiskSpaceError            = "Not enough space left on disk"
	NoUnitOfSizeSelectedError          = "A unit of size must be selected"
	PartitionExceedsDiskErrorFmt       = "Device space exceeded by partition (%d)"
	SizeStartError                     = "Size can not start with `0`"
	SizeInvalidCharacterError          = "Size must be a number"
	UnexpectedPartitionErrorFmt        = "Unexpected partition size '%s'"
)

// EncryptView text.
const (
	EncryptTitle                = "Enter Disk Encryption Password"
	SkipEncryption              = "[Skip Disk Encryption[]"
	EncryptPasswordLabel        = "Disk Encryption Password"
	ConfirmEncryptPasswordLabel = "Confirm Disk Encryption Password"
)

// InstallerView text.
const (
	InstallerExperienceTitle = "Select Installation Experience"
	InstallerTerminalOption  = "Terminal Installer"
	InstallerGraphicalOption = "Graphical Installer"
)

// EulaView text.
const (
	EulaTitle = "Welcome to the CBL-Mariner Installer"
)

// HostNameView text.
const (
	HostNameTitle      = "Choose the Hostname for Your System"
	HostNameInputLabel = "HostName:"

	HostNameSegment   = "hostname"
	DomainNameSegment = "domain name"

	FQDNEmptyErrorFmt         = "empty %s is not allowed"
	FQDNEndsInDashErrorFmt    = "%s should not end with '-'"
	FQDNInvalidRuneErrorFmt   = "%s should only contain alpha-numeric, '.' and '-' characters"
	FQDNInvalidStartErrorFmt  = "%s should start with an alpha character"
	FQDNInvalidLengthErrorFmt = "hostname must be <= %d characters"
)

// InstallationView text.
const (
	InstallationTitle = "Select Installation Type"
)

// UserView text.
const (
	SetupUserTitle = "Setup User Account"

	PasswordInputLabel        = "Password"
	ConfirmPasswordInputLabel = "Confirm Password"
	UserNameInputLabel        = "User Name"

	PasswordMismatchFeedback = "Passwords do not match"

	UserNameEmptyError            = "user name cannot be empty"
	UserNameInvalidRuneError      = "user name should only contain alpha-numeric and '-', '.' or '_' characters"
	UserNameInvalidStartError     = "user name should start with an alpha-numeric character"
	UserNameInvalidLengthErrorFmt = "user name must be <= %d characters"
)

// ProgressView text.
const (
	ProgressTitle      = "Installing CBL-Mariner OS"
	ProgressSpinnerFmt = "Installing CBL-Mariner, please wait %v"
)

// FinishView text.
const (
	FinishTitle   = "CBL-Mariner Installation Complete"
	FinishTextFmt = "Total installation time: %v seconds."
)

// Common for input validation.
const (
	AlphaNumeric = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
)
