package exe

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestParseListArgument(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected []string
	}{
		{
			name:     "empty input",
			input:    "",
			expected: []string{},
		},
		{
			name:     "single value",
			input:    "value",
			expected: []string{"value"},
		},
		{
			name:     "multiple values",
			input:    "value1 value2 value3",
			expected: []string{"value1", "value2", "value3"},
		},
		{
			name:     "leading/trailing spaces",
			input:    "  value1  value2  value3  ",
			expected: []string{"value1", "value2", "value3"},
		},
		{
			name:     "extra spaces",
			input:    "value1  value2   value3",
			expected: []string{"value1", "value2", "value3"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := ParseListArgument(tt.input)
			assert.Equal(t, tt.expected, actual)
		})
	}
}
