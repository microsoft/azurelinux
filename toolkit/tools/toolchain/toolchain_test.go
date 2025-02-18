package main

import (
	"strings"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

// config = buildConfig{
// 	doBuild:                 false,
// 	doDeltaBuild:            false,
// 	doDownload:              false,
// 	doCache:                 !disableCache,
// 	doUpdateManifestArchive: false,
// 	doUpdateManifestPMC:     false,
// 	doUpdateManifestLocal:   false,
// 	doArchive:               false,
// }

// test main to enable logging
func TestMain(m *testing.M) {
	logger.InitStderrLog()
	m.Run()
}

func FuzzValidateConfig(f *testing.F) {
	f.Add("auto", "/toolchain.tar.gz", true, true)
	f.Add("fast", "/toolchain.tar.gz", true, false)
	f.Add("force", "", false, true)
	f.Add("never", "", true, true)

	f.Fuzz(func(t *testing.T, rebuild string, archive string, latest bool, cache bool) {
		config, err := validateConfigOptions(rebuild, archive, latest, cache)
		// err should NEVER contain "unhandled build inputs ..."
		if err != nil && strings.Contains(err.Error(), "unhandled build inputs") {
			t.Errorf("Expected error to NOT contain 'unhandled build inputs', has %s", err.Error())
		}

		if err != nil {
			t.Skip()
		}

		// sanity check the config state
		if !config.doBuild && config.doDeltaBuild {
			t.Errorf("Expected doBuild to be true when doDeltaBuild is true")
		}

		if config.doUpdateManifestArchive && (config.doUpdateManifestPMC || config.doUpdateManifestLocal) {
			t.Errorf("Expected doUpdateManifestArchive to be true when doUpdateManifestPMC and doUpdateManifestLocal are false")
		}

		if archive == "" {
			if rebuild != "never" && !config.doBuild {
				t.Errorf("Expected doBuild to be true when rebuild is not 'never'")
			}
		} else {
			if config.doBuild {
				t.Errorf("Expected doBuild to be false when archive is set")
			}

			if config.doDeltaBuild && !config.doDownload {
				t.Errorf("Expected doDownload to be true when doDeltaBuild is true")
			}
		}
	})
}
