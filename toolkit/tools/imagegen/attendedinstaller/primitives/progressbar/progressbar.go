// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package progressbar

import (
	"github.com/gdamore/tcell"
	"github.com/rivo/tview"
)

const (
	minProgressBarHeight = 2
)

// ProgressBar represents a progressbar primitive.
type ProgressBar struct {
	*tview.Box

	labelColor tcell.Color
	fillColor  tcell.Color

	progress int
	status   string

	// An optional function which is called when the status or progress changes.
	changed func()
}

// NewProgressBar returns a new progress bar.
func NewProgressBar() *ProgressBar {
	const (
		xPadding = 5
		yPadding = 0
	)

	return &ProgressBar{
		Box:        tview.NewBox().SetBorderPadding(yPadding, yPadding, xPadding, xPadding),
		labelColor: tview.Styles.PrimaryTextColor,
		fillColor:  tview.Styles.GraphicsColor,
	}
}

// SetFillColor sets the color of progress bar itself.
func (p *ProgressBar) SetFillColor(color tcell.Color) *ProgressBar {
	p.fillColor = color
	return p
}

// SetLabelColor sets the color of text in the progress bar primitive.
func (p *ProgressBar) SetLabelColor(color tcell.Color) *ProgressBar {
	p.labelColor = color
	return p
}

// GetHeight returns the height of the progressbar.
func (p *ProgressBar) GetHeight() int {
	return minProgressBarHeight
}

// SetStatus sets the status label of the progressbar.
func (p *ProgressBar) SetStatus(status string) {
	p.status = status
	if p.changed != nil {
		p.changed()
	}
}

// SetProgress sets the completed progress of the progressbar.
func (p *ProgressBar) SetProgress(progress int) {
	p.progress = progress
	if p.changed != nil {
		p.changed()
	}
}

// SetChangedFunc sets a callback that will be invoked when the status
// or progress changes for the progressbar.
func (p *ProgressBar) SetChangedFunc(handler func()) *ProgressBar {
	p.changed = handler
	return p
}

// Draw renders this primitive onto the screen.
func (p *ProgressBar) Draw(screen tcell.Screen) {
	const (
		emptyRune     = "░"
		fillRune      = "█"
		textAlign     = tview.AlignLeft
		statusYOffset = 1
	)

	// Draw a transparent bounding box. On Draw size calculations are updated.
	p.Box.Draw(screen)

	// Determine the bounding dimensions.
	x, y, width, _ := p.GetInnerRect()
	endX := x + width

	filledInWidth := int(float32(width) * (float32(p.progress) / 100))
	filledInX := x + filledInWidth

	for i := x; i < endX; i++ {
		var toPrint string
		if i < filledInX {
			toPrint = fillRune
		} else {
			toPrint = emptyRune
		}

		tview.Print(screen, toPrint, i, y, len(toPrint), textAlign, p.fillColor)
	}
}
