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
	
	"github.com/phommel/gonetworkmanager"
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
		return fmt.Error("Invalid input for --ip: %s", err)
	}

	netmask := strings.Trim(n.NetMask, " ")
	if err = validateIPAddress(netmask); err != nil {
		return fmt.Error("Invalid input for --netmask: %s", err)
	}

	gateway := strings.Trim(n.GateWay, " ")
	if err = validateIPAddress(gateway); err != nil {
		return fmt.Error("Invalid input for --gateway: %s", err)
	}

	for _, nameserver := range n.NameServer {
		if err = validateIPAddress(strings.Trim(nameserver, " ")); err != nil {
			return fmt.Error("Invalid input for --nameserver: %s", err)
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

func InitializeNetwork(systemConfig SystemConfig) (err error) {
	return nil
}