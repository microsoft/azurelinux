// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Shared logger

package logger

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestFormatWarningBox(t *testing.T) {
	tests := []struct {
		name    string
		message []string
		want    []string
	}{
		{
			name:    "empty message",
			message: []string{},
			want: []string{
				"╔══╗",
				"╚══╝",
			},
		},
		{
			name:    "single line message",
			message: []string{"hello"},
			want: []string{
				"╔═══════╗",
				"║ hello ║",
				"╚═══════╝",
			},
		},
		{
			name:    "multi line message",
			message: []string{"hello", "world"},
			want: []string{
				"╔═══════╗",
				"║ hello ║",
				"║ world ║",
				"╚═══════╝",
			},
		},
		{
			name: "Different lenghts",
			message: []string{
				"this is a long message",
				"odd",
				"even",
			},
			want: []string{
				"╔════════════════════════╗",
				"║ this is a long message ║",
				"║          odd           ║",
				"║          even          ║",
				"╚════════════════════════╝",
			},
		},
		{
			name: "utf8 multirune",
			message: []string{
				"Hello",
				"世",  // ~"world"
				"世界", // "world"
			},
			// unicode characters can take up more than one character space, this is too complex to handle
			// so we just accept the inconsistency
			want: []string{
				"╔═══════╗",
				"║ Hello ║",
				"║   世   ║",
				"║  世界   ║",
				"╚═══════╝",
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			box := FormatMessageBox(tt.message)
			assert.Equal(t, tt.want, box)
		})
	}
}
