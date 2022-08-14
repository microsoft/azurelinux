// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package diskutils

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Tests the validity of the blockDeviceInfo struct's data modeling of size as `json.Number`
// with respect to the ability of the standard json.Unmarshal function to handle input from
// old and new versions of lsblk.
func TestValidBlockDevicesOutputSizeVariance(t *testing.T) {
	// The first device, with size as a number, is typical output for lsblk from util-linux >= v2.33
	// The second device, with size as a quoted string, is typical output for lsblk from util-linux < v2.33
	const validSizeVarianceJSON = `{
		"blockdevices": [
		   {"name":"nvme0n1", "size":1000204886016, "model":"Super Cool NVMe SSD 1TB", "maj:min":"259:1"},
		   {"name":"nvme1n1", "size":"1000204886016", "model":"Super Cool NVMe SSD 1TB", "maj:min":"259:1"}
		]
	 }`

	expectedBlockDevicesOutput := blockDevicesOutput{
		Devices: []blockDeviceInfo{
			{
				Name:   "nvme0n1",
				Size:   "1000204886016",
				Model:  "Super Cool NVMe SSD 1TB",
				MajMin: "259:1",
			},
			{
				Name:   "nvme1n1",
				Size:   "1000204886016",
				Model:  "Super Cool NVMe SSD 1TB",
				MajMin: "259:1",
			},
		},
	}

	var blockDevices blockDevicesOutput
	bytes := []byte(validSizeVarianceJSON)
	err := json.Unmarshal(bytes, &blockDevices)
	assert.NoError(t, err)
	assert.EqualValues(t, expectedBlockDevicesOutput, blockDevices)
}
