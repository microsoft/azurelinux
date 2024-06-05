// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package network

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"errors"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestDownloadFile(t *testing.T) {
	const (
		cancelDelay      = 1000 * time.Millisecond
		noCancelDelay    = 100 * time.Millisecond
		validFile        = "VALID.md"
		doesNotExistFile = "DOESNOTEXIST.md"
		bogusFile        = "BOGUS.md"
	)
	fileServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch {
		case r.URL.Path == "/"+validFile:
			fmt.Fprintf(w, "Valid file")
		case r.URL.Path == "/"+doesNotExistFile:
			w.WriteHeader(http.StatusNotFound)
		case r.URL.Path == "/"+bogusFile:
			w.WriteHeader(http.StatusInternalServerError)
		default:
			t.Fatal("Unexpected URL")
		}
	}))
	defer fileServer.Close()
	validUrl := fmt.Sprintf("%s/%s", fileServer.URL, validFile)
	doesNotExistUrl := fmt.Sprintf("%s/%s", fileServer.URL, doesNotExistFile)
	bogusUrl := fmt.Sprintf("%s/%s", fileServer.URL, bogusFile)

	type args struct {
		_ctx     context.Context // Build dynamically in test. Set via useCtx.
		srcUrl   string
		dstFile  string
		caCerts  *x509.CertPool
		tlsCerts []tls.Certificate
		timeout  time.Duration
	}
	tests := []struct {
		name             string
		args             args
		useCtx           bool
		wantWasCancelled bool
		wantErr          bool
		expectedErr      error
		expectedTime     time.Duration
	}{
		{
			name: "TestDownloadFile",
			args: args{
				srcUrl:   validUrl,
				dstFile:  validFile,
				caCerts:  nil,
				tlsCerts: nil,
			},
			useCtx:           false,
			wantWasCancelled: false,
			wantErr:          false,
			expectedTime:     noCancelDelay,
		},
		{
			name: "TestDownloadWithCancel",
			args: args{
				srcUrl:   validUrl,
				dstFile:  validFile,
				caCerts:  nil,
				tlsCerts: nil,
			},
			useCtx:           true,
			wantWasCancelled: false,
			wantErr:          false,
			expectedTime:     noCancelDelay,
		},
		{
			name: "TestDownload404",
			args: args{
				srcUrl:   doesNotExistUrl,
				dstFile:  doesNotExistFile,
				caCerts:  nil,
				tlsCerts: nil,
			},
			useCtx:           false,
			wantWasCancelled: false,
			wantErr:          true,
			expectedErr:      ErrDownloadFileInvalidResponse404,
			expectedTime:     noCancelDelay, // 404 is not retried, should fail immediately.
		},
		{
			name: "TestDownloadWithBogusCerts",
			args: args{
				srcUrl:  bogusUrl,
				dstFile: bogusFile,
			},
			useCtx:           true,
			wantWasCancelled: true,
			wantErr:          true,
			expectedErr:      ErrDownloadFileOther,
			expectedTime:     cancelDelay + (100 * time.Millisecond), // Will retry for a long time, cancel after 2 seconds.
		},
		{
			name: "TestDownloadWithBogusCertsTimeout",
			args: args{
				srcUrl:  bogusUrl,
				dstFile: bogusFile,
				timeout: cancelDelay,
			},
			useCtx:           false,
			wantWasCancelled: true,
			wantErr:          true,
			expectedErr:      ErrDownloadFileOther,
			expectedTime:     cancelDelay + (100 * time.Millisecond), // Will retry for a long time, cancel after 2 seconds.
		},
		{
			name: "TestDownloadWithBadTimeout",
			args: args{
				srcUrl:   validUrl,
				dstFile:  validFile,
				caCerts:  nil,
				tlsCerts: nil,
				timeout:  -1,
			},
			useCtx:           false,
			wantWasCancelled: false,
			wantErr:          true,
			expectedErr:      ErrDownloadFileInvalidTimeout,
			expectedTime:     noCancelDelay,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			dstDir := t.TempDir()
			tt.args.dstFile = filepath.Join(dstDir, tt.args.dstFile)
			if tt.useCtx {
				var cancelFunc context.CancelFunc
				tt.args._ctx, cancelFunc = context.WithTimeout(context.Background(), cancelDelay)
				defer cancelFunc()
			} else {
				tt.args._ctx = context.Background()
			}

			startTime := time.Now()
			gotWasCancelled, err := DownloadFileWithRetry(tt.args._ctx, tt.args.srcUrl, tt.args.dstFile, tt.args.caCerts, tt.args.tlsCerts, tt.args.timeout)
			endTime := time.Now()
			if (err != nil) != tt.wantErr {
				t.Errorf("DownloadFile() error = %v, wantErr %v", err, tt.wantErr)
			}
			if tt.expectedErr != nil {
				if !errors.Is(err, tt.expectedErr) {
					t.Errorf("DownloadFile() error = %v, wantErr %v", err, tt.expectedErr)
				}
			}
			if gotWasCancelled != tt.wantWasCancelled {
				t.Errorf("DownloadFile() = %v, want %v", gotWasCancelled, tt.wantWasCancelled)
			}

			if endTime.Sub(startTime) > tt.expectedTime {
				t.Errorf("DownloadFile() time = %v, want %v", endTime.Sub(startTime), tt.expectedTime)
			}

			if !tt.wantErr {
				if _, err := os.Stat(tt.args.dstFile); err != nil {
					t.Errorf("DownloadFile() failed to download file %s", tt.args.dstFile)
				}
			} else {
				if _, err := os.Stat(tt.args.dstFile); err == nil {
					t.Errorf("DownloadFile() should have failed to download file %s", tt.args.dstFile)
				}
			}
		})
	}
}

func TestDownloadWithRetryNilContext(t *testing.T) {
	dstDir := t.TempDir()
	dstFile := filepath.Join(dstDir, "README.md")
	//lint:ignore SA1012 We intentionally want to test the error case of a nil context
	_, err := DownloadFileWithRetry(nil, "https://raw.githubusercontent.com/microsoft/azurelinux/HEAD/README.md", dstFile, nil, nil, 0)
	if err == nil {
		t.Errorf("DownloadFile() should have failed with nil context")
	}
}
