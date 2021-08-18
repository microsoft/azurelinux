// Copyright 2018 CNI authors
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

package main

import (
	"crypto/sha1"
	"encoding/json"
	"fmt"

	"github.com/vishvananda/netlink"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"

	"github.com/containernetworking/plugins/pkg/ip"
	"github.com/containernetworking/plugins/pkg/ns"
	bv "github.com/containernetworking/plugins/pkg/utils/buildversion"
)

// BandwidthEntry corresponds to a single entry in the bandwidth argument,
// see CONVENTIONS.md
type BandwidthEntry struct {
	IngressRate  int `json:"ingressRate"`  //Bandwidth rate in bps for traffic through container. 0 for no limit. If ingressRate is set, ingressBurst must also be set
	IngressBurst int `json:"ingressBurst"` //Bandwidth burst in bits for traffic through container. 0 for no limit. If ingressBurst is set, ingressRate must also be set

	EgressRate  int `json:"egressRate"`  //Bandwidth rate in bps for traffic through container. 0 for no limit. If egressRate is set, egressBurst must also be set
	EgressBurst int `json:"egressBurst"` //Bandwidth burst in bits for traffic through container. 0 for no limit. If egressBurst is set, egressRate must also be set
}

func (bw *BandwidthEntry) isZero() bool {
	return bw.IngressBurst == 0 && bw.IngressRate == 0 && bw.EgressBurst == 0 && bw.EgressRate == 0
}

type PluginConf struct {
	types.NetConf

	RuntimeConfig struct {
		Bandwidth *BandwidthEntry `json:"bandwidth,omitempty"`
	} `json:"runtimeConfig,omitempty"`

	*BandwidthEntry
}

// parseConfig parses the supplied configuration (and prevResult) from stdin.
func parseConfig(stdin []byte) (*PluginConf, error) {
	conf := PluginConf{}

	if err := json.Unmarshal(stdin, &conf); err != nil {
		return nil, fmt.Errorf("failed to parse network configuration: %v", err)
	}

	bandwidth := getBandwidth(&conf)
	if bandwidth != nil {
		err := validateRateAndBurst(bandwidth.IngressRate, bandwidth.IngressBurst)
		if err != nil {
			return nil, err
		}
		err = validateRateAndBurst(bandwidth.EgressRate, bandwidth.EgressBurst)
		if err != nil {
			return nil, err
		}
	}

	if conf.RawPrevResult != nil {
		var err error
		if err = version.ParsePrevResult(&conf.NetConf); err != nil {
			return nil, fmt.Errorf("could not parse prevResult: %v", err)
		}

		_, err = current.NewResultFromResult(conf.PrevResult)
		if err != nil {
			return nil, fmt.Errorf("could not convert result to current version: %v", err)
		}
	}

	return &conf, nil

}

func getBandwidth(conf *PluginConf) *BandwidthEntry {
	if conf.BandwidthEntry == nil && conf.RuntimeConfig.Bandwidth != nil {
		return conf.RuntimeConfig.Bandwidth
	}
	return conf.BandwidthEntry
}

func validateRateAndBurst(rate int, burst int) error {
	switch {
	case burst < 0 || rate < 0:
		return fmt.Errorf("rate and burst must be a positive integer")
	case burst == 0 && rate != 0:
		return fmt.Errorf("if rate is set, burst must also be set")
	case rate == 0 && burst != 0:
		return fmt.Errorf("if burst is set, rate must also be set")
	}

	return nil
}

func getIfbDeviceName(networkName string, containerId string) (string, error) {
	hash := sha1.New()
	_, err := hash.Write([]byte(networkName + containerId))
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", hash.Sum(nil))[:4], nil
}

func getMTU(deviceName string) (int, error) {
	link, err := netlink.LinkByName(deviceName)
	if err != nil {
		return -1, err
	}

	return link.Attrs().MTU, nil
}

// get the veth peer of container interface in host namespace
func getHostInterface(interfaces []*current.Interface, containerIfName string, netns ns.NetNS) (*current.Interface, error) {
	if len(interfaces) == 0 {
		return nil, fmt.Errorf("no interfaces provided")
	}

	// get veth peer index of container interface
	var peerIndex int
	var err error
	_ = netns.Do(func(_ ns.NetNS) error {
		_, peerIndex, err = ip.GetVethPeerIfindex(containerIfName)
		return nil
	})
	if peerIndex <= 0 {
		return nil, fmt.Errorf("container interface %s has no veth peer: %v", containerIfName, err)
	}

	// find host interface by index
	link, err := netlink.LinkByIndex(peerIndex)
	if err != nil {
		return nil, fmt.Errorf("veth peer with index %d is not in host ns", peerIndex)
	}
	for _, iface := range interfaces {
		if iface.Sandbox == "" && iface.Name == link.Attrs().Name {
			return iface, nil
		}
	}

	return nil, fmt.Errorf("no veth peer of container interface found in host ns")
}

func cmdAdd(args *skel.CmdArgs) error {
	conf, err := parseConfig(args.StdinData)
	if err != nil {
		return err
	}

	bandwidth := getBandwidth(conf)
	if bandwidth == nil || bandwidth.isZero() {
		return types.PrintResult(conf.PrevResult, conf.CNIVersion)
	}

	if conf.PrevResult == nil {
		return fmt.Errorf("must be called as chained plugin")
	}

	result, err := current.NewResultFromResult(conf.PrevResult)
	if err != nil {
		return fmt.Errorf("could not convert result to current version: %v", err)
	}

	netns, err := ns.GetNS(args.Netns)
	if err != nil {
		return fmt.Errorf("failed to open netns %q: %v", netns, err)
	}
	defer netns.Close()

	hostInterface, err := getHostInterface(result.Interfaces, args.IfName, netns)
	if err != nil {
		return err
	}

	if bandwidth.IngressRate > 0 && bandwidth.IngressBurst > 0 {
		err = CreateIngressQdisc(bandwidth.IngressRate, bandwidth.IngressBurst, hostInterface.Name)
		if err != nil {
			return err
		}
	}

	if bandwidth.EgressRate > 0 && bandwidth.EgressBurst > 0 {
		mtu, err := getMTU(hostInterface.Name)
		if err != nil {
			return err
		}

		ifbDeviceName, err := getIfbDeviceName(conf.Name, args.ContainerID)
		if err != nil {
			return err
		}

		err = CreateIfb(ifbDeviceName, mtu)
		if err != nil {
			return err
		}

		ifbDevice, err := netlink.LinkByName(ifbDeviceName)
		if err != nil {
			return err
		}

		result.Interfaces = append(result.Interfaces, &current.Interface{
			Name: ifbDeviceName,
			Mac:  ifbDevice.Attrs().HardwareAddr.String(),
		})
		err = CreateEgressQdisc(bandwidth.EgressRate, bandwidth.EgressBurst, hostInterface.Name, ifbDeviceName)
		if err != nil {
			return err
		}
	}

	return types.PrintResult(result, conf.CNIVersion)
}

func cmdDel(args *skel.CmdArgs) error {
	conf, err := parseConfig(args.StdinData)
	if err != nil {
		return err
	}

	ifbDeviceName, err := getIfbDeviceName(conf.Name, args.ContainerID)
	if err != nil {
		return err
	}

	if err := TeardownIfb(ifbDeviceName); err != nil {
		return err
	}

	return nil
}

func main() {
	skel.PluginMain(cmdAdd, cmdCheck, cmdDel, version.PluginSupports("0.3.0", "0.3.1", version.Current()), bv.BuildString("bandwidth"))
}

func SafeQdiscList(link netlink.Link) ([]netlink.Qdisc, error) {
	qdiscs, err := netlink.QdiscList(link)
	if err != nil {
		return nil, err
	}
	result := []netlink.Qdisc{}
	for _, qdisc := range qdiscs {
		// filter out pfifo_fast qdiscs because
		// older kernels don't return them
		_, pfifo := qdisc.(*netlink.PfifoFast)
		if !pfifo {
			result = append(result, qdisc)
		}
	}
	return result, nil
}

func cmdCheck(args *skel.CmdArgs) error {
	bwConf, err := parseConfig(args.StdinData)
	if err != nil {
		return err
	}

	if bwConf.PrevResult == nil {
		return fmt.Errorf("must be called as a chained plugin")
	}

	result, err := current.NewResultFromResult(bwConf.PrevResult)
	if err != nil {
		return fmt.Errorf("could not convert result to current version: %v", err)
	}

	netns, err := ns.GetNS(args.Netns)
	if err != nil {
		return fmt.Errorf("failed to open netns %q: %v", netns, err)
	}
	defer netns.Close()

	hostInterface, err := getHostInterface(result.Interfaces, args.IfName, netns)
	if err != nil {
		return err
	}
	link, err := netlink.LinkByName(hostInterface.Name)
	if err != nil {
		return err
	}

	bandwidth := getBandwidth(bwConf)

	if bandwidth.IngressRate > 0 && bandwidth.IngressBurst > 0 {
		rateInBytes := bandwidth.IngressRate / 8
		burstInBytes := bandwidth.IngressBurst / 8
		bufferInBytes := buffer(uint64(rateInBytes), uint32(burstInBytes))
		latency := latencyInUsec(latencyInMillis)
		limitInBytes := limit(uint64(rateInBytes), latency, uint32(burstInBytes))

		qdiscs, err := SafeQdiscList(link)
		if err != nil {
			return err
		}
		if len(qdiscs) == 0 {
			return fmt.Errorf("Failed to find qdisc")
		}

		for _, qdisc := range qdiscs {
			tbf, isTbf := qdisc.(*netlink.Tbf)
			if !isTbf {
				break
			}
			if tbf.Rate != uint64(rateInBytes) {
				return fmt.Errorf("Rate doesn't match")
			}
			if tbf.Limit != uint32(limitInBytes) {
				return fmt.Errorf("Limit doesn't match")
			}
			if tbf.Buffer != uint32(bufferInBytes) {
				return fmt.Errorf("Buffer doesn't match")
			}
		}
	}

	if bandwidth.EgressRate > 0 && bandwidth.EgressBurst > 0 {
		rateInBytes := bandwidth.EgressRate / 8
		burstInBytes := bandwidth.EgressBurst / 8
		bufferInBytes := buffer(uint64(rateInBytes), uint32(burstInBytes))
		latency := latencyInUsec(latencyInMillis)
		limitInBytes := limit(uint64(rateInBytes), latency, uint32(burstInBytes))

		ifbDeviceName, err := getIfbDeviceName(bwConf.Name, args.ContainerID)
		if err != nil {
			return err
		}

		ifbDevice, err := netlink.LinkByName(ifbDeviceName)
		if err != nil {
			return fmt.Errorf("get ifb device: %s", err)
		}

		qdiscs, err := SafeQdiscList(ifbDevice)
		if err != nil {
			return err
		}
		if len(qdiscs) == 0 {
			return fmt.Errorf("Failed to find qdisc")
		}

		for _, qdisc := range qdiscs {
			tbf, isTbf := qdisc.(*netlink.Tbf)
			if !isTbf {
				break
			}
			if tbf.Rate != uint64(rateInBytes) {
				return fmt.Errorf("Rate doesn't match")
			}
			if tbf.Limit != uint32(limitInBytes) {
				return fmt.Errorf("Limit doesn't match")
			}
			if tbf.Buffer != uint32(bufferInBytes) {
				return fmt.Errorf("Buffer doesn't match")
			}
		}
	}

	return nil
}
