// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package network

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"errors"
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
	const cancelDelay = 2000 * time.Millisecond
	const noCancelDelay = 500 * time.Millisecond
	type args struct {
		srcUrl   string
		dstFile  string
		caCerts  *x509.CertPool
		tlsCerts []tls.Certificate
		_ctx     context.Context // Build dynamically in test. Set via useCtx.
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
				srcUrl:   "https://raw.githubusercontent.com/microsoft/azurelinux/HEAD/README.md",
				dstFile:  "README.md",
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
				srcUrl:   "https://raw.githubusercontent.com/microsoft/azurelinux/HEAD/README.md",
				dstFile:  "README.md",
				caCerts:  nil,
				tlsCerts: nil,
			},
			useCtx:           true,
			wantWasCancelled: false,
			wantErr:          false,
			expectedTime:     cancelDelay,
		},
		{
			name: "TestDownload404",
			args: args{
				srcUrl:   "https://raw.githubusercontent.com/microsoft/azurelinux/HEAD/DOESNOTEXIST.md",
				dstFile:  "DOESNOTEXIST.md",
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
				srcUrl:  "https://raw.githubusercontent.com/microsoft/azurelinux/HEAD/README.md",
				dstFile: "README.md",
				caCerts: x509.NewCertPool(),
				tlsCerts: []tls.Certificate{
					{
						Certificate: [][]byte{[]byte("bogus")},
					},
				},
			},
			useCtx:           true,
			wantWasCancelled: true,
			wantErr:          true,
			expectedErr:      ErrDownloadFileOther,
			expectedTime:     cancelDelay + (100 * time.Millisecond), // Will retry for a long time, cancel after 2 seconds.
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
			gotWasCancelled, err := DownloadFileWithRetry(tt.args._ctx, tt.args.srcUrl, tt.args.dstFile, tt.args.caCerts, tt.args.tlsCerts)
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
	_, err := DownloadFileWithRetry(nil, "https://raw.githubusercontent.com/microsoft/azurelinux/HEAD/README.md", dstFile, nil, nil)
	if err == nil {
		t.Errorf("DownloadFile() should have failed with nil context")
	}
}
