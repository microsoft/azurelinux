package filewatcher

import (
	"github.com/fsnotify/fsnotify"
	"k8s.io/klog/v2"
)

// EventHandler is called when a fsnotify event occurs.
type EventHandler func(fsnotify.Event)

// ErrorHandler is called when a fsnotify error occurs.
type ErrorHandler func(error)

// ClientInt is a file watcher abstraction based on fsnotify.
type ClientInt interface {
	Add(path string) error
	Start(exit <-chan struct{})
}

// client is an implementation of ClientInt.
type client struct {
	watcher      *fsnotify.Watcher
	eventHandler EventHandler
	errorHandler ErrorHandler
}

var _ ClientInt = &client{}

// NewFileWatcher returns an implementation of ClientInt that continuously listens
// for fsnotify events and calls the event handler as soon as an event is received.
func NewFileWatcher(eventHandler EventHandler, errorHandler ErrorHandler) (ClientInt, error) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil, err
	}

	return &client{
		watcher:      watcher,
		eventHandler: eventHandler,
		errorHandler: errorHandler,
	}, nil
}

// Add adds a file path to watch.
func (c *client) Add(path string) error {
	return c.watcher.Add(path)
}

// Start starts watching all registered files for events.
func (c *client) Start(exit <-chan struct{}) {
	go func() {
		defer c.watcher.Close()
		for {
			select {
			case <-exit:
				return
			case event := <-c.watcher.Events:
				klog.Infof("detected file modification: %s", event.String())
				if c.eventHandler != nil {
					c.eventHandler(event)
				}
			case err := <-c.watcher.Errors:
				if c.errorHandler != nil {
					c.errorHandler(err)
				}
			}
		}
	}()
}
