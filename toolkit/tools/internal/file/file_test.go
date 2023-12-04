// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"encoding/hex"
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

func TestGenerateSHA1String(t *testing.T) {
	// Create a temporary file with some content
	tmpFilePath := testFileName(t)
	tmpFile, err := os.Create(tmpFilePath)
	if err != nil {
		t.Fatal(err)
	}
	defer tmpFile.Close()

	content := "Hello, world!"
	if _, err := tmpFile.WriteString(content); err != nil {
		t.Fatal(err)
	}

	// Generate the SHA256 hash of the temporary file
	hash, err := GenerateSHA1String(tmpFile.Name())
	if err != nil {
		t.Fatal(err)
	}

	// Verify that the generated hash matches the expected hash
	expectedHash := "943a702d06f34599aee1f8da8ef9f7296031d699"
	if hash != expectedHash {
		t.Errorf("Generated hash does not match the expected hash. Got: %s, Expected: %s", hash, expectedHash)
	}
}

func TestGenerateSHA1StringInvalidPath(t *testing.T) {
	// Generate the SHA256 hash of a non-existent file
	_, err := GenerateSHA256String("/path/to/nonexistent/file")
	if err == nil {
		t.Error("Expected an error, but got nil")
	}
}

func TestGenerateSHA256String(t *testing.T) {
	// Create a temporary file with some content
	tmpFilePath := testFileName(t)
	tmpFile, err := os.Create(tmpFilePath)
	if err != nil {
		t.Fatal(err)
	}
	defer tmpFile.Close()

	content := "Hello, world!"
	if _, err := tmpFile.WriteString(content); err != nil {
		t.Fatal(err)
	}

	// Generate the SHA256 hash of the temporary file
	hash, err := GenerateSHA256String(tmpFile.Name())
	if err != nil {
		t.Fatal(err)
	}

	// Verify that the generated hash matches the expected hash
	expectedHash := "315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3"
	if hash != expectedHash {
		t.Errorf("Generated hash does not match the expected hash. Got: %s, Expected: %s", hash, expectedHash)
	}
}

func TestGenerateSHA256StringInvalidPath(t *testing.T) {
	// Generate the SHA256 hash of a non-existent file
	_, err := GenerateSHA256String("/path/to/nonexistent/file")
	if err == nil {
		t.Error("Expected an error, but got nil")
	}
}

func TestSHA1MultipleFiles(t *testing.T) {
	// Create a temporary file with some content
	tempFileNames := []string{}
	for i := 'a'; i <= 'c'; i++ {
		tmpFilePath := testFileName(t) + string(i)
		tempFileNames = append(tempFileNames, tmpFilePath)
		tmpFile, err := os.Create(tmpFilePath)
		if err != nil {
			t.Fatal(err)
		}
		defer tmpFile.Close()

		content := string(i)
		if _, err := tmpFile.WriteString(content); err != nil {
			t.Fatal(err)
		}
	}

	// Generate the SHA256 hash of the temporary file
	rawHash, err := CalculateSHA1Bytes(tempFileNames)
	if err != nil {
		t.Fatal(err)
	}

	hash := hex.EncodeToString(rawHash)
	// Verify that the generated hash matches the expected hash
	expectedHash := "a9993e364706816aba3e25717850c26c9cd0d89d"
	if hash != expectedHash {
		t.Errorf("Generated hash does not match the expected hash. Got: %s, Expected: %s", hash, expectedHash)
	}
}

func TestSHA256MultipleFiles(t *testing.T) {
	// Create a temporary file with some content
	tempFileNames := []string{}
	for i := 'a'; i <= 'c'; i++ {
		tmpFilePath := testFileName(t) + string(i)
		tempFileNames = append(tempFileNames, tmpFilePath)
		tmpFile, err := os.Create(tmpFilePath)
		if err != nil {
			t.Fatal(err)
		}
		defer tmpFile.Close()

		content := string(i)
		if _, err := tmpFile.WriteString(content); err != nil {
			t.Fatal(err)
		}
	}

	// Generate the SHA256 hash of the temporary file
	rawHash, err := CalculateSHA256Bytes(tempFileNames)
	if err != nil {
		t.Fatal(err)
	}

	hash := hex.EncodeToString(rawHash)
	// Verify that the generated hash matches the expected hash
	expectedHash := "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
	if hash != expectedHash {
		t.Errorf("Generated hash does not match the expected hash. Got: %s, Expected: %s", hash, expectedHash)
	}
}
