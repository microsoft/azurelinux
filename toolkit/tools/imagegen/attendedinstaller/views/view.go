// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package views

import (
	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
)

// View is the interface for different "pages" in the attended installer.
type View interface {
	// Initialize initializes the view.
	Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) error

	// HandleInput handles custom input.
	HandleInput(event *tcell.EventKey) *tcell.EventKey

	// Reset resets the page, undoing any user input.
	Reset() error

	// OnShow gets called when the view is shown to the user
	OnShow()

	// Name returns the friendly name of the view.
	Name() string

	// Title returns the title of the view.
	Title() string

	// Primitive returns the primary primitive to be rendered for the view.
	Primitive() tview.Primitive
}
