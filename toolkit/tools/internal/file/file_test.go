// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	retVal := m.Run()
	os.Exit(retVal)
}

// testFileName returns a file name in a temporary directory. This path will
// be different for EVERY call to this function.
func testFileName(t *testing.T) string {
	return filepath.Join(t.TempDir(), t.Name())
}

func TestRemoveFileIfExistsValid(t *testing.T) {
	fileName := testFileName(t)
	// Create a file to remove
	err := Write("test", fileName)
	assert.NoError(t, err)

	err = RemoveFileIfExists(fileName)
	assert.NoError(t, err)

	exists, err := PathExists(fileName)
	assert.NoError(t, err)
	assert.False(t, exists)
}

func TestRemoveFileDoesNotExist(t *testing.T) {
	fileName := testFileName(t)
	err := RemoveFileIfExists(fileName)
	assert.NoError(t, err)
}
func TestCompareFileByteStreams(t *testing.T) {
	type args struct {
		in1 io.Reader
		in2 io.Reader
	}
	tests := []struct {
		name    string
		args    args
		want    bool
		wantErr bool
	}{
		{
			name: "Same content",
			args: args{
				in1: strings.NewReader("Hello, world!"),
				in2: strings.NewReader("Hello, world!"),
			},
			want:    true,
			wantErr: false,
		},
		{
			name: "Different content",
			args: args{
				in1: strings.NewReader("Hello, world!"),
				in2: strings.NewReader("Goodbye, world!"),
			},
			want:    false,
			wantErr: false,
		},
		{
			name: "Error reading from input 1",
			args: args{
				in1: &errorReader{},
				in2: strings.NewReader("Hello, world!"),
			},
			want:    false,
			wantErr: true,
		},
		{
			name: "Error reading from input 2",
			args: args{
				in1: strings.NewReader("Hello, world!"),
				in2: &errorReader{},
			},
			want:    false,
			wantErr: true,
		},
		{
			name: "Same input longer than buff size",
			args: args{
				in1: strings.NewReader(strings.Repeat("a", compareBufferSize*1.5)),
				in2: strings.NewReader(strings.Repeat("a", compareBufferSize*1.5)),
			},
			want:    true,
			wantErr: false,
		},
		{
			name: "Different input longer than buff size",
			args: args{
				in1: strings.NewReader(strings.Repeat("a", compareBufferSize*1.5)),
				in2: strings.NewReader(strings.Repeat("a", (compareBufferSize*1.5)-1) + "b"),
			},
			want:    false,
			wantErr: false,
		},
		{
			name: "Input longer than buff size, one shorter",
			args: args{
				in1: strings.NewReader(strings.Repeat("a", compareBufferSize*1.5)),
				in2: strings.NewReader(strings.Repeat("a", compareBufferSize*0.5)),
			},
			want:    false,
			wantErr: false,
		},
		{
			name: "Input longer than buff size, one shorter - reversed",
			args: args{
				in1: strings.NewReader(strings.Repeat("a", compareBufferSize*0.5)),
				in2: strings.NewReader(strings.Repeat("a", compareBufferSize*1.5)),
			},
			want:    false,
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := compareFileByteStreams(tt.args.in1, tt.args.in2)
			if (err != nil) != tt.wantErr {
				t.Errorf("compareFileByteStreams() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if got != tt.want {
				t.Errorf("compareFileByteStreams() = %v, want %v", got, tt.want)
			}
		})
	}
}

type errorReader struct{}

func (er *errorReader) Read(p []byte) (n int, err error) {
	return 0, fmt.Errorf("error reading from input")
}
