// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

var PxeIsoDownloadProtocols = []string{"http://"}

// Iso defines how the generated iso media should be configured.
type Pxe struct {
	IsoImageUrl string `yaml:"isoImageUrl"`
}

func (p *Pxe) IsValid() error {
	if p.IsoImageUrl != "" {
		protocolFound := false
		for _, protocol := range PxeIsoDownloadProtocols {
			if strings.HasPrefix(p.IsoImageUrl, protocol) {
				protocolFound = true
				break
			}
		}
		if !protocolFound {
			return fmt.Errorf("unsupported iso image URL protocol in (%s). One of (%v) is expected.", p.IsoImageUrl, PxeIsoDownloadProtocols)
		}
	}
	return nil
}
