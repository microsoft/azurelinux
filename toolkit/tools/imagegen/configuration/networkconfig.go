// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's Networks configuration schema.

package configuration

import (
	"encoding/json"
	"fmt"
	"strings"
	"regexp"
	"net"
	
	"microsoft.com/pkggen/internal/logger"
)

type Network struct {
	BootProto           string   `json:"BootProto"`
	GateWay             string   `json:"GateWay"`
	Ip      			string   `json:"Ip"`
	NetMask            	string   `json:"NetMask"`
	OnBoot 				bool     `json:"OnBoot"`
	HostName      		string   `json:"HostName"`
	NameServer          []string `json:"NameServer"`
	Device     			string   `json:"Device"`
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

func getSupportedNetworkDeviceList(nm gonetworkmanager.NetworkManager) (available_devices map[string]gonetworkmanager.Device, err error) {
	var (
		all_devices []gonetworkmanager.Device
		device_name string
	)
	
	available_devices = make(map[string]gonetworkmanager.Device)

	all_devices, err = nm.GetDevices()
	if err != nil {
		return
	}

	for _, network_device := range all_devices {
		device_name, err = network_device.GetInterface()
		logger.Log.Infof("Network device name: %s", device_name)
		if err != nil {
			return
		}

		available_devices[device_name] = network_device
	}

	return 
}

func findDeviceNameFromHwAddr(nm gonetworkmanager.NetworkManager, hwAddr string) (device_name string, err error) {
	var (
		devices []gonetworkmanager.Device
		deviceType gonetworkmanager.NmDeviceType
		deviceName string
	)
	
	ifaces, err := net.Interfaces()
	if err != nil {
		return
	}

	devices, err = nm.GetDevices()
	if err != nil {
		return
	}

	for _, device := range devices {
		deviceType, err = device.GetDeviceType()
		if err != nil {
			return
		}

		deviceName, err = device.GetInterface()
		if err != nil {
			return
		}

		if deviceType == gonetworkmanager.NmDeviceTypeEthernet || deviceType == gonetworkmanager.NmDeviceTypeWifi {
			// Loop through all network interfaces
			for _, iface := range ifaces {
				if deviceName == iface.Name {
					address := iface.HardwareAddr.String()
					
					if address != "" && strings.ToUpper(address) == strings.ToUpper(hwAddr) {
						device_name = deviceName
						return
					}
				}
			}
		}

	}

	return
}

func getDeviceNameFromNetworkData(network_data Network,nm gonetworkmanager.NetworkManager, supported_devices map[string]gonetworkmanager.Device) (deviceName string, err error) {
	// Device setting by device name
	if len(supported_devices) > 0 {
		// Check if the device name is available
		_, ok := supported_devices[network_data.Device] 
		if ok {
			logger.Log.Infof("Existing device found: %s", network_data.Device)
			deviceName = network_data.Device
			return
		}
	} else if strings.Contains(network_data.Device, ":") {
		// Device setting by MAC address
		deviceName, err = findDeviceNameFromHwAddr(nm, network_data.Device)
	} else if strings.Contains(network_data.Device, "bootif") {
		// ------- TODO: Where to read bootif value
	}

	if deviceName != "" {
		_, ok := supported_devices[deviceName]
		if !ok {
			logger.Log.Infof("device found (%s) is not supported", deviceName)
			deviceName = ""
		}
	}

	return
}

func findConnectionofNetworkInterface(nm gonetworkmanager.NetworkManager, deviceName string) (connections []gonetworkmanager.Connection) {
	return
}

func ConfigureNetwork(systemConfig SystemConfig) (err error) {
	// Create a network manager instance
	nm, err := gonetworkmanager.NewNetworkManager()
	if err != nil {
		return
	}

	supported_devices, err := getSupportedNetworkDeviceList(nm)
	if err != nil {
		return fmt.Errorf("Failed to find all supported network devices: %s", err)
	}

	_, err = findDeviceNameFromHwAddr(nm, "00:15:5d:b9:2e:3d")

	// Process the network data
	for _, network_data := range systemConfig.Networks {
		device_name, err := getDeviceNameFromNetworkData(network_data, nm, supported_devices) 
		if err != nil || device_name == "" {
			continue
		}

		connection := findConnectionofNetworkInterface(nm, device_name)

	}


	return
}