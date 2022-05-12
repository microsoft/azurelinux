// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's Networks configuration schema.

package configuration

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"regexp"
	"path/filepath"
	"strconv"
	"strings"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/shell"
	"microsoft.com/pkggen/internal/safechroot"
)

type Network struct {
	BootProto  string   `json:"BootProto"`
	GateWay    string   `json:"GateWay"`
	Ip         string   `json:"Ip"`
	NetMask    string   `json:"NetMask"`
	OnBoot     bool     `json:"OnBoot"`
	HostName   string   `json:"HostName"`
	NameServer []string `json:"NameServer"`
	Device     string   `json:"Device"`
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
	err = n.BootProtoIsValid()
	if err != nil {
		return
	}

	err = n.HostNameIsValid()
	if err != nil {
		return
	}

	err = n.IPAddrIsValid()
	if err != nil {
		return
	}

	err = n.DeviceIsValid()
	if err != nil {
		return
	}

	return
}

// BootProtoIsValid returns an error if input bootproto is invalid
func (n *Network) BootProtoIsValid() (err error) {
	switch strings.TrimSpace(n.BootProto) {
	case "", "dhcp", "bootp", "ibft", "static":
		return
	default:
		return fmt.Errorf("invalid value for --bootproto (%s), bootproto can only be one of dhcp, bootp, ibft and static", n.BootProto)
	}
}

// HostNameIsValid returns an error if input hostanme is invalid
func (n *Network) HostNameIsValid() (err error) {
	hostname := strings.Trim(n.HostName, " ")
	re, _ := regexp.Compile(`^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$`)

	if !re.MatchString(hostname) {
		return fmt.Errorf("Invalid value for --hostname (%s)", hostname)
	}

	return
}

func validateIPAddress(ip string) (err error) {
	if net.ParseIP(ip) == nil {
		return fmt.Errorf("Invalid ip address (%s)", ip)
	}

	return
}

// IPAddrIsValid returns an error if ip, gateway, netmask or nameserver inputs are invalid ip addresses
func (n *Network) IPAddrIsValid() (err error) {
	ip := strings.Trim(n.Ip, " ")
	if err = validateIPAddress(ip); err != nil {
		return fmt.Errorf("Invalid input for --ip: %s", err)
	}

	netmask := strings.Trim(n.NetMask, " ")
	if err = validateIPAddress(netmask); err != nil {
		return fmt.Errorf("Invalid input for --netmask: %s", err)
	}

	gateway := strings.Trim(n.GateWay, " ")
	if err = validateIPAddress(gateway); err != nil {
		return fmt.Errorf("Invalid input for --gateway: %s", err)
	}

	for _, nameserver := range n.NameServer {
		if err = validateIPAddress(strings.Trim(nameserver, " ")); err != nil {
			return fmt.Errorf("Invalid input for --nameserver: %s", err)
		}
	}

	return
}

// DeviceIsValid returns an error if the Device name is empty
func (n *Network) DeviceIsValid() (err error) {
	if strings.TrimSpace(n.Device) == "" {
		return fmt.Errorf("invalid input for --device (%s), device cannot be empty", n.Device)
	}
	return
}

func findBootIfValue() (deviceAddr string) {
	const (
		kernelArgFile = "/proc/cmdline"
		startIndex    = 7
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
			deviceAddr = kernelArg[7:len(kernelArg)]
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

	for _, iface := range ifaces {
		if networkData.Device == iface.Name {
			deviceName = networkData.Device
			return
		} else {
			ifaceAddr := iface.HardwareAddr.String()

			if strings.Contains(networkData.Device, ":") {
				if ifaceAddr != "" && strings.ToUpper(ifaceAddr) == strings.ToUpper(networkData.Device) {
					deviceName = iface.Name
					return
				}
			} else if networkData.Device == "bootif" {
				// deviceAddress := findBootIfValue()
				//if ifaceAddr != "" && strings.ToUpper(ifaceAddr) == strings.ToUpper(deviceAddress) {
					if iface.Name == "eth0" {
						deviceName = iface.Name
						return
					}
				//}
			}
		}
	}

	return
}

func populateMatchSection(networkData Network, fileName, deviceName string) (err error) {
	const (
		id            = "[Match]\n"
		NameField     = "Name="
	)

	matchSection := id + NameField + deviceName + "\n"
	err = file.Append(matchSection+"\n", fileName)
	if err != nil {
		logger.Log.Infof("Failed to write [Match] section: %s", err)
	}

	return
}

func populateNetworkSection(networkData Network, fileName string) (err error) {
	const (
		id           = "[Network]\n"
		ipField      = "Address="
		gateWayField = "Gateway="
		dnsField     = "DNS="
	)

	// Obtain the cidr prefix length of netmask
	stringMask := net.IPMask(net.ParseIP(networkData.NetMask).To4())
	cidrPrefix, _ := stringMask.Size()
	ipAddr := networkData.Ip + "/" + strconv.Itoa(cidrPrefix)

	networkSection := id + ipField + ipAddr + "\n" + gateWayField + networkData.GateWay + "\n"

	for _, nameserver := range networkData.NameServer {
		dnsSetting := dnsField + nameserver + "\n"
		networkSection = networkSection + dnsSetting
	}

	err = file.Append(networkSection, fileName)
	if err != nil {
		logger.Log.Infof("Failed to write [Network] section: %s", err)
	}

	return
}

func createNetworkConfigFile(installChroot *safechroot.Chroot, networkData Network, deviceName string) (err error) {
	const (
		networkFileDir = "/etc/systemd/network/"
		filePrefix     = "10-"
	)

	if exists, ferr := file.DirExists(networkFileDir); ferr != nil {
		logger.Log.Errorf("Error accessing /etc/systemd/network/")
		err = ferr
		return
	} else if !exists {
		err = fmt.Errorf("/etc/systemd/network/: no such path or directory")
		return
	}

	logger.Log.Infof("Start creating network file")

	networkFileName := networkFileDir + filePrefix + networkData.BootProto + "-" + deviceName + ".network"
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

	// Determinw whether to activate this device on boot
	if networkData.OnBoot {
		installNetworkFile := filepath.Join(installChroot.RootDir(), networkFileName)
		err = file.Copy(networkFileName, installNetworkFile)
	}

	return
}

func ConfigureNetwork(installChroot *safechroot.Chroot, systemConfig SystemConfig) (err error) {
	const squashErrors = false
	var dnsUpdate bool

	for _, networkData := range systemConfig.Networks {
		deviceName, err := checkNetworkDeviceAvailability(networkData)
		if err != nil || deviceName == "" {
			logger.Log.Errorf("Could not find matching network device in the system")
			break
		}

		err = createNetworkConfigFile(installChroot, networkData, deviceName)
		if err != nil {
			break
		}

		if len(networkData.NameServer) > 0 {
			dnsUpdate = true
		}

		// Set hostname
		hostname := strings.TrimSpace(networkData.HostName)
		if hostname != "" {
			err = shell.ExecuteLive(squashErrors, "hostname", hostname)
			if err != nil {
				logger.Log.Errorf("Unable to set hostname: %s", err)
				return err
			}
		}
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
