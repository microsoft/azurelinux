// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's Networks configuration schema.

package configuration

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

type Network struct {
	BootProto   string   `json:"BootProto"`
	GateWay     string   `json:"GateWay"`
	Ip          string   `json:"Ip"`
	NetMask     string   `json:"NetMask"`
	OnBoot      bool     `json:"OnBoot"`
	NameServers []string `json:"NameServer"`
	Device      string   `json:"Device"`
}

// valid network boot protocols supported
var validBootProtos = map[string]bool{
	"dhcp":   true,
	"static": true,
	"bootp":  true,
	"ibft":   true,
	"":       true,
}

// UnmarshalJSON Unmarshals a Network entry
func (n *Network) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeNetwork Network
	err = json.Unmarshal(b, (*IntermediateTypeNetwork)(n))
	if err != nil {
		return fmt.Errorf("failed to parse [Network]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = n.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [Network]: %w", err)
	}
	return
}

// IsValid returns an error if the Network struct is not valid
func (n *Network) IsValid() (err error) {
	err = n.bootProtoIsValid()
	if err != nil {
		return
	}

	err = n.ipAddrIsValid()
	if err != nil {
		return
	}

	err = n.deviceIsValid()
	if err != nil {
		return
	}

	return
}

// ConfigureNetwork performs network configuration during the kickstart unattended installation process
func ConfigureNetwork(installChroot *safechroot.Chroot, systemConfig SystemConfig) (err error) {
	const squashErrors = false
	var dnsUpdate bool

	for _, networkData := range systemConfig.Networks {
		deviceName, err := checkNetworkDeviceAvailability(networkData)
		if err != nil {
			return err
		} else if deviceName == "" {
			err = fmt.Errorf("The input network device is currently not supported on this system")
			return err
		}

		err = createNetworkConfigFile(installChroot, networkData, deviceName)
		if err != nil {
			return err
		}

		dnsUpdate = len(networkData.NameServers) > 0
	}

	err = shell.ExecuteLive(squashErrors, "systemctl", "restart", "systemd-networkd")
	if err != nil {
		logger.Log.Errorf("Unable to restart systemd-networkd: %s", err)
		return
	}

	if dnsUpdate {
		err = shell.ExecuteLive(squashErrors, "systemctl", "restart", "systemd-resolved")
		if err != nil {
			logger.Log.Errorf("Unable to restart systemd-resolved: %s", err)
		}
	}

	return
}

// bootProtoIsValid returns an error if input bootproto is invalid
func (n *Network) bootProtoIsValid() (err error) {
	n.BootProto = strings.TrimSpace(n.BootProto)
	if validBootProtos[n.BootProto] {
		return
	}

	return fmt.Errorf("invalid input for bootproto (%s), bootproto can only be one of dhcp, bootp, ibft and static", n.BootProto)
}

func (n *Network) validateIPAddress(ip string) (err error) {
	if ip == "" && (n.BootProto == "" || n.BootProto == "dhcp") {
		return
	} else if net.ParseIP(ip) == nil {
		return fmt.Errorf("invalid ip address (%s)", ip)
	}

	return
}

// ipAddrIsValid returns an error if ip, gateway, netmask or nameserver inputs are invalid ip addresses
func (n *Network) ipAddrIsValid() (err error) {
	if err = n.validateIPAddress(n.Ip); err != nil {
		return fmt.Errorf("invalid input for ip: %w", err)
	}

	if err = n.validateIPAddress(n.NetMask); err != nil {
		return fmt.Errorf("invalid input for netmask: %w", err)
	}

	if err = n.validateIPAddress(n.GateWay); err != nil {
		return fmt.Errorf("invalid input for gateway: %w", err)
	}

	for _, nameserver := range n.NameServers {
		if err = n.validateIPAddress(nameserver); err != nil {
			return fmt.Errorf("invalid input for nameserver: %w", err)
		}
	}

	return
}

// deviceIsValid returns an error if the Device name is empty
func (n *Network) deviceIsValid() (err error) {
	n.Device = strings.TrimSpace(n.Device)
	if n.Device == "" {
		return fmt.Errorf("invalid input for device, device cannot be empty")
	}
	return
}

func findBootIfValue() (deviceAddr string) {
	const (
		kernelArgFile = "/proc/cmdline"
		startIndex    = 10
	)

	content, err := os.ReadFile(kernelArgFile)
	if err != nil {
		logger.Log.Errorf("failed to read from /proc/cmdline")
		return
	}

	// Find the location of BOOTIF
	kernelArgs := strings.Split(string(content), " ")
	for _, kernelArg := range kernelArgs {
		if strings.Contains(kernelArg, "BOOTIF") {
			// The bootif value in the cmdline set by pxelinux is of the following format:
			// bootif=01-MAC Address, where each byte value of the MAC address is separated
			// by dashes instead of colons. Therefore, we're reading from the 10th spot of the
			// string to obtain the MAC address and then replace the dashes with colons
			rawMACaddr := kernelArg[startIndex:len(kernelArg)]
			deviceAddr = strings.Replace(rawMACaddr, "-", ":", -1)
			return
		}
	}

	return
}

func checkNetworkDeviceAvailability(networkData Network) (deviceName string, err error) {
	ifaces, err := net.Interfaces()
	if err != nil {
		return
	}

	if networkData.Device == "bootif" {
		networkData.Device = findBootIfValue()
	}

	for _, iface := range ifaces {
		if networkData.Device == iface.Name {
			deviceName = networkData.Device
			return
		} else {
			ifaceAddr := strings.TrimSpace(iface.HardwareAddr.String())

			if strings.Contains(networkData.Device, ":") {
				if ifaceAddr != "" && strings.EqualFold(ifaceAddr, networkData.Device) {
					deviceName = iface.Name
					return
				}
			}
		}
	}

	return
}

func populateMatchSection(networkData Network, fileName, deviceName string) (err error) {
	matchSection := fmt.Sprintf("[Match]\nName=%s\n", deviceName)
	err = file.Append(matchSection+"\n", fileName)
	if err != nil {
		logger.Log.Errorf("Failed to write [Match] section: %s", err)
	}

	return
}

func populateNetworkSection(networkData Network, fileName string) (err error) {
	var networkSection strings.Builder

	// Write network section tag
	networkSection.WriteString("[Network]\n")

	// Currently only supports static IP setting
	// Write IP and netmask
	if networkData.NetMask != "" && networkData.Ip != "" {
		stringMask := net.IPMask(net.ParseIP(networkData.NetMask).To4())
		cidrPrefix, _ := stringMask.Size()
		networkSection.WriteString(fmt.Sprintf("Address=%s/%d\n", networkData.Ip, cidrPrefix))
	}

	// Write Gateway
	if networkData.GateWay != "" {
		networkSection.WriteString(fmt.Sprintf("Gateway=%s\n", networkData.GateWay))
	}

	// Write Nameserver
	for _, nameserver := range networkData.NameServers {
		networkSection.WriteString(fmt.Sprintf("DNS=%s\n", nameserver))
	}

	err = file.Append(networkSection.String(), fileName)
	if err != nil {
		logger.Log.Errorf("Failed to write [Network] section: %s", err)
	}

	return
}

func createNetworkConfigFile(installChroot *safechroot.Chroot, networkData Network, deviceName string) (err error) {
	const (
		networkFileDir = "/etc/systemd/network"
		filePrefix     = "10"
	)

	if exists, ferr := file.DirExists(networkFileDir); ferr != nil {
		logger.Log.Errorf("Error accessing /etc/systemd/network/")
		err = ferr
		return
	} else if !exists {
		err = fmt.Errorf("/etc/systemd/network/: no such path or directory")
		return
	}

	logger.Log.Debugf("Start creating network file")

	networkFileName := fmt.Sprintf("%s/%s-%s-%s.network", networkFileDir, filePrefix, networkData.BootProto, deviceName)
	if exists, _ := file.PathExists(networkFileName); exists {
		return fmt.Errorf("network file (%s) already exists", networkFileName)
	}

	err = file.Create(networkFileName, 0644)
	if err != nil {
		logger.Log.Errorf("Error creating file %s: %s", networkFileName, err)
		return
	}

	// Write the [match] field
	err = populateMatchSection(networkData, networkFileName, deviceName)
	if err != nil {
		return
	}

	// Write the [Network] field
	err = populateNetworkSection(networkData, networkFileName)
	if err != nil {
		return
	}

	// Determine whether to activate this device on boot
	// If yes, then also place a copy of the network file in the installer environment in addition to
	// the one on disk
	if networkData.OnBoot {
		installNetworkFile := filepath.Join(installChroot.RootDir(), networkFileName)
		err = file.Copy(networkFileName, installNetworkFile)
	}

	return
}
