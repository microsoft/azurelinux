package framework

import (
	"time"
)

const (
	// Timeout represents the duration it waits until a long-running operation times out.
	Timeout = 5 * time.Minute

	// Polling represents the polling interval for a long-running operation.
	Polling = 10 * time.Second
)
