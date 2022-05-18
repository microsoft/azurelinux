// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"os"
	"strings"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/stretchr/testify/assert"
)

var (
	ValidNetworks = []Network{
		{
			BootProto: "static",
			GateWay:   "10.154.214.130",
			Ip:        "10.154.214.158",
			NetMask:   "255.255.255.0",
			OnBoot:    false,
			HostName:  "mariner-test",
			NameServer: []string{
				"10.159.32.34",
			},
			Device: "eth1",
		},
	}

	ValidNetWorkFileContent = []string{
		"[Match]",
		"Name=eth1",
		"",
		"[Network]",
		"Address=10.154.214.158/24",
		"Gateway=10.154.214.130",
		"DNS=10.159.32.34",
	}
)

// TestMain found in configuration_test.go.

func TestShouldPassParsingValidNetworks_Network(t *testing.T) {
	for _, b := range ValidNetworks {
		var checkedNetwork Network
		assert.NoError(t, b.IsValid())
		err := remarshalJSON(b, &checkedNetwork)
		assert.NoError(t, err)
		assert.Equal(t, b, checkedNetwork)
	}
}

func TestShouldFailParsingInvalidBootProto_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.BootProto = "abcd"

	err := testNetwork.BootProtoIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --bootproto (abcd), bootproto can only be one of dhcp, bootp, ibft and static", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --bootproto (abcd), bootproto can only be one of dhcp, bootp, ibft and static", err.Error())
}

func TestShouldFailParsingInvalidGateWay_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.GateWay = "abcd"

	err := testNetwork.IPAddrIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --gateway: Invalid ip address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --gateway: Invalid ip address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidIp_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.Ip = "abcd"

	err := testNetwork.IPAddrIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --ip: Invalid ip address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --ip: Invalid ip address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidNetMask_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.NetMask = "abcd"

	err := testNetwork.IPAddrIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --netmask: Invalid ip address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --netmask: Invalid ip address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidHostName_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.HostName = "**??"

	err := testNetwork.HostNameIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --hostname (**??)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --hostname (**??)", err.Error())
}

func TestShouldFailParsingInvalidNameServer_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.NameServer = []string{"abcd"}

	err := testNetwork.IPAddrIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --nameserver: Invalid ip address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --nameserver: Invalid ip address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidDevice_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := ValidNetworks[0]
	testNetwork.Device = " "

	err := testNetwork.DeviceIsValid()
	assert.Error(t, err)
	assert.Equal(t, "Invalid input for --device (), device cannot be empty", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: Invalid input for --device (), device cannot be empty", err.Error())
}

func TestShouldPassCreatingNetworkFile_Network(t *testing.T) {
	const networkFile = "/etc/systemd/network/10-static-eth1.network"
	testNetwork := ValidNetworks[0]

	// Remove the file it already exists
	if exists, _ := file.PathExists(networkFile); exists {
		err := os.Remove(networkFile)
		assert.NoError(t, err)
	}

	err := createNetworkConfigFile(nil, testNetwork, "eth1")
	assert.NoError(t, err)

	// Check whether the contents in the network file is correct
	testContents, err := file.ReadLines(networkFile)
	assert.NoError(t, err)
	assert.Equal(t, testContents, ValidNetWorkFileContent)
}

func TestShouldSucceedSettingHostName_Network(t *testing.T) {
	const hostnameFile = "/etc/hostname"
	testNetwork := ValidNetworks[0]

	err := updateHostName(testNetwork.HostName)
	assert.NoError(t, err)

	// Check whether the hostname is set correctly
	setHostName, err := file.ReadLines(hostnameFile)
	assert.NoError(t, err)
	assert.Equal(t, strings.Trim(setHostName[0], " "), strings.Trim(testNetwork.HostName, " "))
}
