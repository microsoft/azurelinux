// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"net/url"
	"strings"
)

var PxeIsoDownloadProtocols = []string{"ftp://", "http://", "https://", "nfs://", "tftp://"}

// Iso defines how the generated iso media should be configured.
type Pxe struct {
	IsoImageBaseUrl string `yaml:"isoImageBaseUrl"`
	IsoImageFileUrl string `yaml:"isoImageFileUrl"`
}

func IsValidPxeUrl(urlString string) error {
	if urlString == "" {
		return nil
	}

	_, err := url.Parse(urlString)
	if err != nil {
		return fmt.Errorf("invalid URL value (%s):\n%w", urlString, err)
	}

	protocolFound := false
	for _, protocol := range PxeIsoDownloadProtocols {
		if strings.HasPrefix(urlString, protocol) {
			protocolFound = true
			break
		}
	}
	if !protocolFound {
		return fmt.Errorf("unsupported iso image URL protocol in (%s). One of (%v) is expected.", urlString, PxeIsoDownloadProtocols)
	}

	return nil
}

func (p *Pxe) IsValid() error {
	if p.IsoImageBaseUrl != "" && p.IsoImageFileUrl != "" {
		return fmt.Errorf("cannot specify both 'isoImageBaseUrl' and 'isoImageFileUrl' at the same time.")
	}
	err := IsValidPxeUrl(p.IsoImageBaseUrl)
	if err != nil {
		return fmt.Errorf("invalid 'isoImageBaseUrl' field value (%s):\n%w", p.IsoImageBaseUrl, err)
	}
	err = IsValidPxeUrl(p.IsoImageFileUrl)
	if err != nil {
		return fmt.Errorf("invalid 'isoImageFileUrl' field value (%s):\n%w", p.IsoImageFileUrl, err)
	}
	return nil
}
