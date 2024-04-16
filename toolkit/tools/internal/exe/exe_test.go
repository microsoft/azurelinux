package exe

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestToolkitVersionIsNotEmpty(t *testing.T) {
	assert.NotEmpty(t, ToolkitVersion)
}
