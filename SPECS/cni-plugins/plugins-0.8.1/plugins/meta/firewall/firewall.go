// Copyright 2016 CNI authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This is a "meta-plugin". It reads in its own netconf, it does not create
// any network interface but just changes the network sysctl.

package main

import (
	"encoding/json"
	"fmt"
	"net"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"

	"github.com/containernetworking/plugins/pkg/ns"
	bv "github.com/containernetworking/plugins/pkg/utils/buildversion"
)

// FirewallNetConf represents the firewall configuration.
type FirewallNetConf struct {
	types.NetConf

	// Backend is the firewall type to add rules to.  Allowed values are
	// 'iptables' and 'firewalld'.
	Backend string `json:"backend"`

	// IptablesAdminChainName is an optional name to use instead of the default
	// admin rules override chain name that includes the interface name.
	IptablesAdminChainName string `json:"iptablesAdminChainName,omitempty"`

	// FirewalldZone is an optional firewalld zone to place the interface into.  If
	// the firewalld backend is used but the zone is not given, it defaults
	// to 'trusted'
	FirewalldZone string `json:"firewalldZone,omitempty"`
}

type FirewallBackend interface {
	Add(*FirewallNetConf, *current.Result) error
	Del(*FirewallNetConf, *current.Result) error
	Check(*FirewallNetConf, *current.Result) error
}

func ipString(ip net.IPNet) string {
	if ip.IP.To4() == nil {
		return ip.IP.String() + "/128"
	}
	return ip.IP.String() + "/32"
}

func parseConf(data []byte) (*FirewallNetConf, *current.Result, error) {
	conf := FirewallNetConf{}
	if err := json.Unmarshal(data, &conf); err != nil {
		return nil, nil, fmt.Errorf("failed to load netconf: %v", err)
	}

	// Parse previous result.
	if conf.RawPrevResult == nil {
		return nil, nil, fmt.Errorf("missing prevResult from earlier plugin")
	}

	// Parse previous result.
	var result *current.Result
	var err error
	if err = version.ParsePrevResult(&conf.NetConf); err != nil {
		return nil, nil, fmt.Errorf("could not parse prevResult: %v", err)
	}

	result, err = current.NewResultFromResult(conf.PrevResult)
	if err != nil {
		return nil, nil, fmt.Errorf("could not convert result to current version: %v", err)
	}

	// Default the firewalld zone to trusted
	if conf.FirewalldZone == "" {
		conf.FirewalldZone = "trusted"
	}

	return &conf, result, nil
}

func getBackend(conf *FirewallNetConf) (FirewallBackend, error) {
	switch conf.Backend {
	case "iptables":
		return newIptablesBackend(conf)
	case "firewalld":
		return newFirewalldBackend(conf)
	}

	// Default to firewalld if it's running
	if isFirewalldRunning() {
		return newFirewalldBackend(conf)
	}

	// Otherwise iptables
	return newIptablesBackend(conf)
}

func cmdAdd(args *skel.CmdArgs) error {
	conf, result, err := parseConf(args.StdinData)
	if err != nil {
		return err
	}

	backend, err := getBackend(conf)
	if err != nil {
		return err
	}

	if err := backend.Add(conf, result); err != nil {
		return err
	}

	if result == nil {
		result = &current.Result{}
	}
	return types.PrintResult(result, conf.CNIVersion)
}

func cmdDel(args *skel.CmdArgs) error {
	conf, result, err := parseConf(args.StdinData)
	if err != nil {
		return err
	}

	backend, err := getBackend(conf)
	if err != nil {
		return err
	}

	// Tolerate errors if the container namespace has been torn down already
	containerNS, err := ns.GetNS(args.Netns)
	if err == nil {
		defer containerNS.Close()
	}

	// Runtime errors are ignored
	if err := backend.Del(conf, result); err != nil {
		return err
	}

	return nil
}

func main() {
	skel.PluginMain(cmdAdd, cmdCheck, cmdDel, version.PluginSupports("0.4.0"), bv.BuildString("firewall"))
}

func cmdCheck(args *skel.CmdArgs) error {
	conf, result, err := parseConf(args.StdinData)
	if err != nil {
		return err
	}

	// Ensure we have previous result.
	if result == nil {
		return fmt.Errorf("Required prevResult missing")
	}

	backend, err := getBackend(conf)
	if err != nil {
		return err
	}

	if err := backend.Check(conf, result); err != nil {
		return err
	}

	return nil
}
