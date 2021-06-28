package retry

import (
	"strings"
	"time"
)

// Func is a function that is being retried.
type Func func() error

// ShouldRetryFunc is a function that consumes the last-known error
// from the targeted function and determine if we should run it again
type ShouldRetryFunc func(error) bool

// RetriableError is an error that when occurred,
// we should retry targeted function.
type RetriableError string

// ClientInt is an abstraction that retries running a
// function based on what type of error has occurred
type ClientInt interface {
	Do(f Func, shouldRetry ShouldRetryFunc) error
	RegisterRetriableErrors(rerrs ...RetriableError)
	UnregisterRetriableErrors(rerrs ...RetriableError)
}

type client struct {
	retriableErrors map[RetriableError]bool
	maxRetry        int
	retryInterval   time.Duration
}

var _ ClientInt = &client{}

// NewRetryClient returns an implementation of ClientInt that retries
// running a given function based on the parameters provided.
func NewRetryClient(maxRetry int, retryInterval time.Duration) ClientInt {
	return &client{
		retriableErrors: make(map[RetriableError]bool),
		maxRetry:        maxRetry,
		retryInterval:   retryInterval,
	}
}

// Do runs the targeted function f and will retry running
// it if it returns an error and shouldRetry returns true.
func (c *client) Do(f Func, shouldRetry ShouldRetryFunc) error {
	// The original error
	err := f()
	if err == nil {
		return nil
	}

	// Error occurred when retrying
	rerr := err
	for i := 0; i < c.maxRetry; i++ {
		if rerr == nil || !c.isRetriable(rerr) || !shouldRetry(rerr) {
			break
		}

		time.Sleep(c.retryInterval)
		// We should retry if:
		// 1) the last known error is not nil
		// 2) the error is retriable
		// 3) shouldRetry returns true
		rerr = f()
	}

	// Return the original error from the first run,
	// indicating that we retried running the function
	return err
}

// RegisterRetriableErrors registers a retriable error to the retrier.
func (c *client) RegisterRetriableErrors(rerrs ...RetriableError) {
	for _, rerr := range rerrs {
		c.retriableErrors[rerr] = true
	}
}

// UnregisterRetriableErrors unregisters an error from the retrier.
func (c *client) UnregisterRetriableErrors(rerrs ...RetriableError) {
	for _, rerr := range rerrs {
		delete(c.retriableErrors, rerr)
	}
}

// isRetriable returns true if an error is retriable.
func (c *client) isRetriable(err error) bool {
	if err == nil {
		return false
	}

	for rerr := range c.retriableErrors {
		if strings.Contains(err.Error(), string(rerr)) {
			return true
		}
	}

	return false
}
