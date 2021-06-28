package version

import (
	"fmt"
	"strings"
	"testing"
)

func TestVersion(t *testing.T) {
	BuildDate = "Now"
	GitCommit = "Commit"
	NMIVersion = "NMI version"
	expectedUserAgentStr := fmt.Sprintf("aad-pod-identity/%s/%s/%s/%s", "NMI", NMIVersion, GitCommit, BuildDate)
	gotUserAgentStr := GetUserAgent("NMI", NMIVersion)
	if !strings.EqualFold(expectedUserAgentStr, gotUserAgentStr) {
		t.Fatalf("got unexpected user agent string: %s. Expected: %s.", gotUserAgentStr, expectedUserAgentStr)
	}
}
