// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

// import (
// 	"testing"
// 	"os"

// 	"github.com/stretchr/testify/assert"
// )

//TestMain found in configuration_test.go.

// var (
// 	validDisks = Disk{
//     	PartitionTableType: "gpt",
// 		TargetDisk: TargetDisk{
// 			Type:  "path",
// 			Value: "/dev/sda",
// 		},
//         Partitions: []Partition{
//         	{
//                 ID: "boot",
//                 Flags: []PartitionFlag {
//                     "grub",
// 				},
//                 Start: 1,
//                 End: 9,
//                 FsType: "fat32",
//             },
//             {
//                 ID: "rootfs",
//                 Start: 9,
//                 End: 0,
//                 FsType: "ext4",
//             },
//         },
// 	}

// 	validPartitionSettings = []PartitionSetting{
// 		{
// 			ID:	"boot",
// 			MountPoint:	"",
// 		},
// 		{
// 			ID:	"rootfs",
// 			MountPoint:	"/",
// 		},
// 	}

// 	validPartitionCommands = []string {
// 		"part biosboot --fstype=biosboot --size=8 --ondisk=/dev/sda",
// 		"part / --fstype=ext4 --size=2000 --grow --ondisk=/dev/sda",
// 	}
// )

// func TestShouldPassParsingTestPartition_parse_partition(t *testing.T) {
// 	testConfig := expectedConfiguration
// 	testConfig.Disks = []Disk{}
// 	testConfig.SystemConfigs[0].PartitionSettings = []PartitionSetting{}

// 	// Create a testing partition file
// 	f, err := os.Create("/tmp/test-part")
//     if err != nil {
// 		assert.Error(t, err)
// 	}

// 	defer f.Close()

// 	// Write valid test partition commands into /tmp/test-part
// 	for _, c := range validPartitionCommands {
// 		_, err = f.WriteString(c)
// 		if err != nil {
// 			assert.Error(t, err)
// 		}
// 	}

// 	f.Sync()

// 	err = ParseKickStartPartitionScheme(&testConfig, "/tmp/test-part")
// 	if err != nil {
// 		t.Log("Entered here????")
// 		assert.Error(t, err)
// 	}

// 	assert.Equal(t, validDisks, testConfig.Disks[0])
// 	assert.Equal(t, validPartitionSettings, testConfig.SystemConfigs[0].PartitionSettings)
// }