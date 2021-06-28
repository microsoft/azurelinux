package filewatcher

import (
	"io/ioutil"
	"os"
	"testing"
	"time"

	"github.com/fsnotify/fsnotify"
	"github.com/stretchr/testify/assert"
)

func TestFileWatcher(t *testing.T) {
	tempFile, err := ioutil.TempFile("", "")
	if err != nil {
		t.Fatal(err)
	}
	defer func() {
		err := os.Remove(tempFile.Name())
		assert.NoError(t, err)
	}()

	writeCh := make(chan string, 1)
	errCh := make(chan error, 1)
	fw, err := NewFileWatcher(
		func(event fsnotify.Event) {
			if event.Op&fsnotify.Write == fsnotify.Write {
				writeCh <- event.Name
			}
		}, func(err error) {
			errCh <- err
		})
	assert.NoError(t, err)

	fw.Start(make(chan struct{}))
	_, err = tempFile.Write([]byte("test0"))
	assert.NoError(t, err)
	assert.Len(t, errCh, 0)
	assert.Len(t, writeCh, 0)

	err = fw.Add(tempFile.Name())
	assert.NoError(t, err)
	assert.Len(t, errCh, 0)
	assert.Len(t, writeCh, 0)

	_, err = tempFile.Write([]byte("test1"))
	assert.NoError(t, err)
	assert.Len(t, errCh, 0)
	select {
	case f := <-writeCh:
		assert.Equal(t, tempFile.Name(), f)
	case <-time.After(100 * time.Millisecond):
		t.Fatal("Timeout waiting for a fsnotify event")
	}
}
