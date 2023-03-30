// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"os"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/file"
	"github.com/stretchr/testify/assert"
)

var (
	validNetworks = []Network{
		{
			BootProto: "static",
			GateWay:   "10.154.214.130",
			Ip:        "10.154.214.158",
			NetMask:   "255.255.255.0",
			OnBoot:    false,
			NameServers: []string{
				"10.159.32.34",
			},
			Device: "eth1",
		},
	}

	validNetworkFileContent = []string{
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
	for _, inputNetwork := range validNetworks {
		var checkedNetwork Network
		assert.NoError(t, inputNetwork.IsValid())
		err := remarshalJSON(inputNetwork, &checkedNetwork)
		assert.NoError(t, err)
		assert.Equal(t, inputNetwork, checkedNetwork)
	}
}

func TestShouldFailParsingInvalidBootProto_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := validNetworks[0]
	testNetwork.BootProto = "abcd"

	err := testNetwork.bootProtoIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid input for bootproto (abcd), bootproto can only be one of dhcp, bootp, ibft and static", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: invalid input for bootproto (abcd), bootproto can only be one of dhcp, bootp, ibft and static", err.Error())
}

func TestShouldFailParsingInvalidGateWay_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := validNetworks[0]
	testNetwork.GateWay = "abcd"

	err := testNetwork.ipAddressesAreValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid input for gateway: invalid IP address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: invalid input for gateway: invalid IP address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidIp_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := validNetworks[0]
	testNetwork.Ip = "abcd"

	err := testNetwork.ipAddressesAreValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid input for IP: invalid IP address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: invalid input for IP: invalid IP address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidNetMask_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := validNetworks[0]
	testNetwork.NetMask = "abcd"

	err := testNetwork.ipAddressesAreValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid input for netmask: invalid IP address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: invalid input for netmask: invalid IP address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidNameServer_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := validNetworks[0]
	testNetwork.NameServers = []string{"abcd"}

	err := testNetwork.ipAddressesAreValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid input for nameserver: invalid IP address (abcd)", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: invalid input for nameserver: invalid IP address (abcd)", err.Error())
}

func TestShouldFailParsingInvalidDevice_Network(t *testing.T) {
	var checkedNetwork Network
	testNetwork := validNetworks[0]
	testNetwork.Device = " "

	err := testNetwork.deviceIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid input for device, device cannot be empty", err.Error())

	err = remarshalJSON(testNetwork, &checkedNetwork)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Network]: invalid input for device, device cannot be empty", err.Error())
}

func TestShouldPassCreatingNetworkFile_Network(t *testing.T) {
	const (
		networkFileDir  = "/etc/systemd/network"
		testNetworkFile = "/etc/systemd/network/10-static-eth1.network"
	)

	// Some systems may not have systemd-networkd service configured, and thus
	// /etc/systemd/network may not exist. For this test case, manually create this directory
	// if it does not exist
	exists, err := file.DirExists(networkFileDir)
	assert.NoError(t, err)
	if !exists {
		err = os.Mkdir(networkFileDir, os.ModePerm)
		assert.NoError(t, err)
		t.Cleanup(func() {
			err = os.RemoveAll(networkFileDir)
			assert.NoError(t, err)
		})
	}

	testNetwork := validNetworks[0]

	err = createNetworkConfigFile(nil, testNetwork, "eth1")
	assert.NoError(t, err)
	t.Cleanup(func() {
		os.Remove(testNetworkFile)
	})

	// Check whether the contents in the network file is correct
	testContents, err := file.ReadLines(testNetworkFile)
	assert.NoError(t, err)
	assert.Equal(t, testContents, validNetworkFileContent)
}
