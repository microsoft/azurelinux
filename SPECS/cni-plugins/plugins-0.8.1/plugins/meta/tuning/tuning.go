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
	"io/ioutil"
	"net"
	"path/filepath"
	"strings"

	"github.com/vishvananda/netlink"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"

	"github.com/containernetworking/plugins/pkg/ns"
	bv "github.com/containernetworking/plugins/pkg/utils/buildversion"
)

// TuningConf represents the network tuning configuration.
type TuningConf struct {
	types.NetConf
	SysCtl  map[string]string `json:"sysctl"`
	Mac     string            `json:"mac,omitempty"`
	Promisc bool              `json:"promisc,omitempty"`
	Mtu     int               `json:"mtu,omitempty"`
}

type MACEnvArgs struct {
	types.CommonArgs
	MAC types.UnmarshallableString `json:"mac,omitempty"`
}

func parseConf(data []byte, envArgs string) (*TuningConf, error) {
	conf := TuningConf{Promisc: false}
	if err := json.Unmarshal(data, &conf); err != nil {
		return nil, fmt.Errorf("failed to load netconf: %v", err)
	}

	// Parse custom MAC from both env args
	if envArgs != "" {
		e := MACEnvArgs{}
		err := types.LoadArgs(envArgs, &e)
		if err != nil {
			return nil, err
		}

		if e.MAC != "" {
			conf.Mac = string(e.MAC)
		}
	}

	return &conf, nil
}

func changeMacAddr(ifName string, newMacAddr string) error {
	addr, err := net.ParseMAC(newMacAddr)
	if err != nil {
		return fmt.Errorf("invalid args %v for MAC addr: %v", newMacAddr, err)
	}

	link, err := netlink.LinkByName(ifName)
	if err != nil {
		return fmt.Errorf("failed to get %q: %v", ifName, err)
	}

	err = netlink.LinkSetDown(link)
	if err != nil {
		return fmt.Errorf("failed to set %q down: %v", ifName, err)
	}
	err = netlink.LinkSetHardwareAddr(link, addr)
	if err != nil {
		return fmt.Errorf("failed to set %q address to %q: %v", ifName, newMacAddr, err)
	}
	return netlink.LinkSetUp(link)
}

func updateResultsMacAddr(config TuningConf, ifName string, newMacAddr string) {
	// Parse previous result.
	if config.PrevResult == nil {
		return
	}

	version.ParsePrevResult(&config.NetConf)
	result, _ := current.NewResultFromResult(config.PrevResult)

	for _, i := range result.Interfaces {
		if i.Name == ifName {
			i.Mac = newMacAddr
		}
	}
}

func changePromisc(ifName string, val bool) error {
	link, err := netlink.LinkByName(ifName)
	if err != nil {
		return fmt.Errorf("failed to get %q: %v", ifName, err)
	}

	if val {
		return netlink.SetPromiscOn(link)
	}
	return netlink.SetPromiscOff(link)
}

func changeMtu(ifName string, mtu int) error {
	link, err := netlink.LinkByName(ifName)
	if err != nil {
		return fmt.Errorf("failed to get %q: %v", ifName, err)
	}
	return netlink.LinkSetMTU(link, mtu)
}

func cmdAdd(args *skel.CmdArgs) error {
	tuningConf, err := parseConf(args.StdinData, args.Args)
	if err != nil {
		return err
	}

	// Parse previous result.
	if tuningConf.RawPrevResult == nil {
		return fmt.Errorf("Required prevResult missing")
	}

	if err := version.ParsePrevResult(&tuningConf.NetConf); err != nil {
		return err
	}

	_, err = current.NewResultFromResult(tuningConf.PrevResult)
	if err != nil {
		return err
	}

	// The directory /proc/sys/net is per network namespace. Enter in the
	// network namespace before writing on it.

	err = ns.WithNetNSPath(args.Netns, func(_ ns.NetNS) error {
		for key, value := range tuningConf.SysCtl {
			fileName := filepath.Join("/proc/sys", strings.Replace(key, ".", "/", -1))
			fileName = filepath.Clean(fileName)

			// Refuse to modify sysctl parameters that don't belong
			// to the network subsystem.
			if !strings.HasPrefix(fileName, "/proc/sys/net/") {
				return fmt.Errorf("invalid net sysctl key: %q", key)
			}
			content := []byte(value)
			err := ioutil.WriteFile(fileName, content, 0644)
			if err != nil {
				return err
			}
		}

		if tuningConf.Mac != "" {
			if err = changeMacAddr(args.IfName, tuningConf.Mac); err != nil {
				return err
			}
			updateResultsMacAddr(*tuningConf, args.IfName, tuningConf.Mac)
		}

		if tuningConf.Promisc != false {
			if err = changePromisc(args.IfName, true); err != nil {
				return err
			}
		}

		if tuningConf.Mtu != 0 {
			if err = changeMtu(args.IfName, tuningConf.Mtu); err != nil {
				return err
			}
		}
		return nil
	})
	if err != nil {
		return err
	}

	return types.PrintResult(tuningConf.PrevResult, tuningConf.CNIVersion)
}

func cmdDel(args *skel.CmdArgs) error {
	// TODO: the settings are not reverted to the previous values. Reverting the
	// settings is not useful when the whole container goes away but it could be
	// useful in scenarios where plugins are added and removed at runtime.
	return nil
}

func main() {
	skel.PluginMain(cmdAdd, cmdCheck, cmdDel, version.All, bv.BuildString("tuning"))
}

func cmdCheck(args *skel.CmdArgs) error {
	tuningConf, err := parseConf(args.StdinData, args.Args)
	if err != nil {
		return err
	}

	// Parse previous result.
	if tuningConf.RawPrevResult == nil {
		return fmt.Errorf("Required prevResult missing")
	}

	if err := version.ParsePrevResult(&tuningConf.NetConf); err != nil {
		return err
	}

	_, err = current.NewResultFromResult(tuningConf.PrevResult)
	if err != nil {
		return err
	}

	err = ns.WithNetNSPath(args.Netns, func(_ ns.NetNS) error {
		// Check each configured value vs what's currently in the container
		for key, conf_value := range tuningConf.SysCtl {
			fileName := filepath.Join("/proc/sys", strings.Replace(key, ".", "/", -1))
			fileName = filepath.Clean(fileName)

			contents, err := ioutil.ReadFile(fileName)
			if err != nil {
				return err
			}
			cur_value := strings.TrimSuffix(string(contents), "\n")
			if conf_value != cur_value {
				return fmt.Errorf("Error: Tuning configured value of %s is %s, current value is %s", fileName, conf_value, cur_value)
			}
		}

		link, err := netlink.LinkByName(args.IfName)
		if err != nil {
			return fmt.Errorf("Cannot find container link %v", args.IfName)
		}

		if tuningConf.Mac != "" {
			if tuningConf.Mac != link.Attrs().HardwareAddr.String() {
				return fmt.Errorf("Error: Tuning configured Ethernet of %s is %s, current value is %s",
					args.IfName, tuningConf.Mac, link.Attrs().HardwareAddr)
			}
		}

		if tuningConf.Promisc {
			if link.Attrs().Promisc == 0 {
				return fmt.Errorf("Error: Tuning link %s configured promisc is %v, current value is %d",
					args.IfName, tuningConf.Promisc, link.Attrs().Promisc)
			}
		} else {
			if link.Attrs().Promisc != 0 {
				return fmt.Errorf("Error: Tuning link %s configured promisc is %v, current value is %d",
					args.IfName, tuningConf.Promisc, link.Attrs().Promisc)
			}
		}

		if tuningConf.Mtu != 0 {
			if tuningConf.Mtu != link.Attrs().MTU {
				return fmt.Errorf("Error: Tuning configured MTU of %s is %d, current value is %d",
					args.IfName, tuningConf.Mtu, link.Attrs().MTU)
			}
		}
		return nil
	})
	if err != nil {
		return err
	}

	return nil
}
