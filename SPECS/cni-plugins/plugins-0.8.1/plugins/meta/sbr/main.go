// Copyright 2017 CNI authors
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

// This is the Source Based Routing plugin that sets up source based routing.
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"

	"github.com/alexflint/go-filemutex"
	"github.com/vishvananda/netlink"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"

	"github.com/containernetworking/plugins/pkg/ns"
	bv "github.com/containernetworking/plugins/pkg/utils/buildversion"
)

const firstTableID = 100

// PluginConf is the configuration document passed in.
type PluginConf struct {
	types.NetConf

	// This is the previous result, when called in the context of a chained
	// plugin. Because this plugin supports multiple versions, we'll have to
	// parse this in two passes. If your plugin is not chained, this can be
	// removed (though you may wish to error if a non-chainable plugin is
	// chained).
	RawPrevResult *map[string]interface{} `json:"prevResult"`
	PrevResult    *current.Result         `json:"-"`

	// Add plugin-specific flags here
}

// Wrapper that does a lock before and unlock after operations to serialise
// this plugin.
func withLockAndNetNS(nspath string, toRun func(_ ns.NetNS) error) error {
	// We lock on the network namespace to ensure that no other instance
	// clashes with this one.
	log.Printf("Network namespace to use and lock: %s", nspath)
	lock, err := filemutex.New(nspath)
	if err != nil {
		return err
	}

	err = lock.Lock()
	if err != nil {
		return err
	}

	err = ns.WithNetNSPath(nspath, toRun)

	if err != nil {
		return err
	}

	// Cleaner to unlock even though about to exit
	err = lock.Unlock()

	return err
}

// parseConfig parses the supplied configuration (and prevResult) from stdin.
func parseConfig(stdin []byte) (*PluginConf, error) {
	conf := PluginConf{}

	if err := json.Unmarshal(stdin, &conf); err != nil {
		return nil, fmt.Errorf("failed to parse network configuration: %v", err)
	}

	// Parse previous result.
	if conf.RawPrevResult != nil {
		resultBytes, err := json.Marshal(conf.RawPrevResult)
		if err != nil {
			return nil, fmt.Errorf("could not serialize prevResult: %v", err)
		}
		res, err := version.NewResult(conf.CNIVersion, resultBytes)
		if err != nil {
			return nil, fmt.Errorf("could not parse prevResult: %v", err)
		}
		conf.RawPrevResult = nil
		conf.PrevResult, err = current.NewResultFromResult(res)
		if err != nil {
			return nil, fmt.Errorf("could not convert result to current version: %v", err)
		}
	}
	// End previous result parsing

	return &conf, nil
}

// getIPCfgs finds the IPs on the supplied interface, returning as IPConfig structures
func getIPCfgs(iface string, prevResult *current.Result) ([]*current.IPConfig, error) {

	if len(prevResult.IPs) == 0 {
		// No IP addresses; that makes no sense. Pack it in.
		return nil, fmt.Errorf("No IP addresses supplied on interface: %s", iface)
	}

	// We do a single interface name, stored in args.IfName
	log.Printf("Checking for relevant interface: %s", iface)

	// ips contains the IPConfig structures that were passed, filtered somewhat
	ipCfgs := make([]*current.IPConfig, 0, len(prevResult.IPs))

	for _, ipCfg := range prevResult.IPs {
		// IPs have an interface that is an index into the interfaces array.
		// We assume a match if this index is missing.
		if ipCfg.Interface == nil {
			log.Printf("No interface for IP address %s", ipCfg.Address.IP)
			ipCfgs = append(ipCfgs, ipCfg)
			continue
		}

		// Skip all IPs we know belong to an interface with the wrong name.
		intIdx := *ipCfg.Interface
		if intIdx >= 0 && intIdx < len(prevResult.Interfaces) && prevResult.Interfaces[intIdx].Name != iface {
			log.Printf("Incorrect interface for IP address %s", ipCfg.Address.IP)
			continue
		}

		log.Printf("Found IP address %s", ipCfg.Address.IP.String())
		ipCfgs = append(ipCfgs, ipCfg)
	}

	return ipCfgs, nil
}

// cmdAdd is called for ADD requests
func cmdAdd(args *skel.CmdArgs) error {
	conf, err := parseConfig(args.StdinData)
	if err != nil {
		return err
	}

	log.Printf("Configure SBR for new interface %s - previous result: %v",
		args.IfName, conf.PrevResult)

	if conf.PrevResult == nil {
		return fmt.Errorf("This plugin must be called as chained plugin")
	}

	// Get the list of relevant IPs.
	ipCfgs, err := getIPCfgs(args.IfName, conf.PrevResult)
	if err != nil {
		return err
	}

	// Do the actual work.
	err = withLockAndNetNS(args.Netns, func(_ ns.NetNS) error {
		return doRoutes(ipCfgs, conf.PrevResult.Routes, args.IfName)
	})
	if err != nil {
		return err
	}

	// Pass through the result for the next plugin
	return types.PrintResult(conf.PrevResult, conf.CNIVersion)
}

// doRoutes does all the work to set up routes and rules during an add.
func doRoutes(ipCfgs []*current.IPConfig, origRoutes []*types.Route, iface string) error {
	// Get a list of rules and routes ready.
	rules, err := netlink.RuleList(netlink.FAMILY_ALL)
	if err != nil {
		return fmt.Errorf("Failed to list all rules: %v", err)
	}

	routes, err := netlink.RouteList(nil, netlink.FAMILY_ALL)
	if err != nil {
		return fmt.Errorf("Failed to list all routes: %v", err)
	}

	// Pick a table ID to use. We pick the first table ID from firstTableID
	// on that has no existing rules mapping to it and no existing routes in
	// it.
	table := firstTableID
	for {
		foundExisting := false
		for _, rule := range rules {
			if rule.Table == table {
				foundExisting = true
				break
			}
		}

		for _, route := range routes {
			if route.Table == table {
				foundExisting = true
				break
			}
		}

		if foundExisting {
			table++
		} else {
			break
		}
	}

	log.Printf("First unreferenced table: %d", table)

	link, err := netlink.LinkByName(iface)
	if err != nil {
		return fmt.Errorf("Cannot find network interface %s: %v", iface, err)
	}

	linkIndex := link.Attrs().Index

	// Loop through setting up source based rules and default routes.
	for _, ipCfg := range ipCfgs {
		log.Printf("Set rule for source %s", ipCfg.String())
		rule := netlink.NewRule()
		rule.Table = table

		// Source must be restricted to a single IP, not a full subnet
		var src net.IPNet
		src.IP = ipCfg.Address.IP
		if ipCfg.Version == "4" {
			src.Mask = net.CIDRMask(32, 32)
		} else {
			src.Mask = net.CIDRMask(64, 64)
		}

		log.Printf("Source to use %s", src.String())
		rule.Src = &src

		if err = netlink.RuleAdd(rule); err != nil {
			return fmt.Errorf("Failed to add rule: %v", err)
		}

		// Add a default route, since this may have been removed by previous
		// plugin.
		if ipCfg.Gateway != nil {
			log.Printf("Adding default route to gateway %s", ipCfg.Gateway.String())

			var dest net.IPNet
			if ipCfg.Version == "4" {
				dest.IP = net.IPv4zero
				dest.Mask = net.CIDRMask(0, 32)
			} else {
				dest.IP = net.IPv6zero
				dest.Mask = net.CIDRMask(0, 64)
			}

			route := netlink.Route{
				Dst:       &dest,
				Gw:        ipCfg.Gateway,
				Table:     table,
				LinkIndex: linkIndex}

			err = netlink.RouteAdd(&route)
			if err != nil {
				return fmt.Errorf("Failed to add default route to %s: %v",
					ipCfg.Gateway.String(),
					err)
			}
		}
	}

	// Move all routes into the correct table. We are taking a shortcut; all
	// the routes have been added to the interface anyway but in the wrong
	// table, so instead of removing them we just move them to the table we
	// want them in.
	routes, err = netlink.RouteList(link, netlink.FAMILY_ALL)
	if err != nil {
		return fmt.Errorf("Unable to list routes: %v", err)
	}

	for _, route := range routes {
		log.Printf("Moving route %s from table %d to %d",
			route.String(), route.Table, table)

		err := netlink.RouteDel(&route)
		if err != nil {
			return fmt.Errorf("Failed to delete route: %v", err)
		}

		route.Table = table

		// We use route replace in case the route already exists, which
		// is possible for the default gateway we added above.
		err = netlink.RouteReplace(&route)
		if err != nil {
			return fmt.Errorf("Failed to readd route: %v", err)
		}
	}

	return nil
}

// cmdDel is called for DELETE requests
func cmdDel(args *skel.CmdArgs) error {
	// We care a bit about config because it sets log level.
	_, err := parseConfig(args.StdinData)
	if err != nil {
		return err
	}

	log.Printf("Cleaning up SBR for %s", args.IfName)
	err = withLockAndNetNS(args.Netns, func(_ ns.NetNS) error {
		return tidyRules(args.IfName)
	})

	return err
}

// Tidy up the rules for the deleted interface
func tidyRules(iface string) error {

	// We keep on going on rule deletion error, but return the last failure.
	var errReturn error

	rules, err := netlink.RuleList(netlink.FAMILY_ALL)
	if err != nil {
		log.Printf("Failed to list all rules to tidy: %v", err)
		return fmt.Errorf("Failed to list all rules to tidy: %v", err)
	}

	link, err := netlink.LinkByName(iface)
	if err != nil {
		log.Printf("Failed to get link %s: %v", iface, err)
		return fmt.Errorf("Failed to get link %s: %v", iface, err)
	}

	addrs, err := netlink.AddrList(link, netlink.FAMILY_ALL)
	if err != nil {
		log.Printf("Failed to list all addrs: %v", err)
		return fmt.Errorf("Failed to list all addrs: %v", err)
	}

RULE_LOOP:
	for _, rule := range rules {
		log.Printf("Check rule: %v", rule)
		if rule.Src == nil {
			continue
		}

		for _, addr := range addrs {
			if rule.Src.IP.Equal(addr.IP) {
				log.Printf("Delete rule %v", rule)
				err := netlink.RuleDel(&rule)
				if err != nil {
					errReturn = fmt.Errorf("Failed to delete rule %v", err)
					log.Printf("... Failed! %v", err)
				}
				continue RULE_LOOP
			}
		}

	}

	return errReturn
}

func main() {
	skel.PluginMain(cmdAdd, cmdCheck, cmdDel, version.All, bv.BuildString("sbr"))
}

func cmdCheck(args *skel.CmdArgs) error {
	return nil
}
