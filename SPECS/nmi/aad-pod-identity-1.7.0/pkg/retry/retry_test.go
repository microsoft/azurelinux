package retry

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDo(t *testing.T) {
	r := NewRetryClient(2, 0)
	r.RegisterRetriableErrors("err1")

	ran := 0
	err := r.Do(func() error {
		ran++
		return nil
	}, func(err error) bool {
		return true
	})
	// Targeted function ran once since there is no error occurred
	assert.Equal(t, 1, ran)
	assert.NoError(t, err)

	ran = 0
	err = r.Do(func() error {
		ran++
		return errors.New("err1 occurred")
	}, func(err error) bool {
		return true
	})
	// Targeted function ran 3 times (1 initial run and 2 retries)
	assert.Equal(t, 3, ran)
	assert.Error(t, err)

	ran = 0
	err = r.Do(func() error {
		ran++
		return errors.New("err1 occurred")
	}, func(err error) bool {
		return false
	})
	// Targeted function ran once since shouldRetryFunc returned false
	assert.Equal(t, 1, ran)
	assert.Error(t, err)

	ran = 0
	err = r.Do(func() error {
		ran++
		return errors.New("err2 occurred")
	}, func(err error) bool {
		return true
	})
	// Targeted function only ran once since err2 was not registered
	assert.Equal(t, 1, ran)
	assert.Error(t, err)
}
