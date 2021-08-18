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

package main

import (
	"encoding/json"
	"fmt"
	"runtime"
	"strings"
	"os"

	"github.com/Microsoft/hcsshim"
	"github.com/Microsoft/hcsshim/hcn"
	"github.com/juju/errors"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"

	"github.com/containernetworking/plugins/pkg/hns"
	"github.com/containernetworking/plugins/pkg/ipam"
	bv "github.com/containernetworking/plugins/pkg/utils/buildversion"
)

type NetConf struct {
	hns.NetConf

	IPMasqNetwork string `json:"ipMasqNetwork,omitempty"`
	ApiVersion    int    `json:"ApiVersion"`
}

func init() {
	// this ensures that main runs only on main thread (thread group leader).
	// since namespace ops (unshare, setns) are done for a single thread, we
	// must ensure that the goroutine does not jump from OS thread to thread
	runtime.LockOSThread()
}

func loadNetConf(bytes []byte) (*NetConf, string, error) {
	n := &NetConf{}
	if err := json.Unmarshal(bytes, n); err != nil {
		return nil, "", fmt.Errorf("failed to load netconf: %v", err)
	}
	return n, n.CNIVersion, nil
}

func ProcessEndpointArgs(args *skel.CmdArgs, n *NetConf) (*hns.EndpointInfo, error) {
	epInfo := new(hns.EndpointInfo)
	epInfo.NetworkName = n.Name
	epInfo.EndpointName = hns.ConstructEndpointName(args.ContainerID, args.Netns, epInfo.NetworkName)
	// It's not necessary to have have an IPAM in windows as hns can provide IP/GW
	if n.IPAM.Type != "" {
		r, err := ipam.ExecAdd(n.IPAM.Type, args.StdinData)
		if err != nil {
			return nil, errors.Annotatef(err, "error while ipam.ExecAdd")
		}

		// Convert whatever the IPAM result was into the current Result type
		result, err := current.NewResultFromResult(r)
		if err != nil {
			return nil, errors.Annotatef(err, "error while NewResultFromResult")
		} else {
			if len(result.IPs) == 0 {
				return nil, errors.New("IPAM plugin return is missing IP config")
			}
			epInfo.IpAddress = result.IPs[0].Address.IP
			epInfo.Gateway = result.IPs[0].Address.IP.Mask(result.IPs[0].Address.Mask)

			// Calculate gateway for bridge network (needs to be x.2)
			epInfo.Gateway[len(epInfo.Gateway)-1] += 2
		}
	}
	// NAT based on the the configured cluster network
	if len(n.IPMasqNetwork) != 0 {
		n.ApplyOutboundNatPolicy(n.IPMasqNetwork)
	}

	epInfo.DNS = n.GetDNS()

	return epInfo, nil
}

func cmdHnsAdd(args *skel.CmdArgs, n *NetConf) (*current.Result, error) {
	networkName := n.Name
	hnsNetwork, err := hcsshim.GetHNSNetworkByName(networkName)
	if err != nil {
		return nil, errors.Annotatef(err, "error while GETHNSNewtorkByName(%s)", networkName)
	}

	if hnsNetwork == nil {
		return nil, fmt.Errorf("network %v not found", networkName)
	}

	if !strings.EqualFold(hnsNetwork.Type, "L2Bridge") {
		return nil, fmt.Errorf("network %v is of an unexpected type: %v", networkName, hnsNetwork.Type)
	}

	epName := hns.ConstructEndpointName(args.ContainerID, args.Netns, n.Name)

	hnsEndpoint, err := hns.ProvisionEndpoint(epName, hnsNetwork.Id, args.ContainerID, args.Netns, func() (*hcsshim.HNSEndpoint, error) {
		epInfo, err := ProcessEndpointArgs(args, n)
		epInfo.NetworkId = hnsNetwork.Id
		if err != nil {
			return nil, errors.Annotatef(err, "error while ProcessEndpointArgs")
		}
		hnsEndpoint, err := hns.GenerateHnsEndpoint(epInfo, &n.NetConf)
		if err != nil {
			return nil, errors.Annotatef(err, "error while GenerateHnsEndpoint")
		}
		return hnsEndpoint, nil
	})
	if err != nil {
		return nil, errors.Annotatef(err, "error while ProvisionEndpoint(%v,%v,%v)", epName, hnsNetwork.Id, args.ContainerID)
	}

	result, err := hns.ConstructResult(hnsNetwork, hnsEndpoint)
	if err != nil {
		return nil, errors.Annotatef(err, "error while constructResult")
	}

	return result, nil

}

func cmdHcnAdd(args *skel.CmdArgs, n *NetConf) (*current.Result, error) {
	networkName := n.Name
	hcnNetwork, err := hcn.GetNetworkByName(networkName)
	if err != nil {
		return nil, errors.Annotatef(err, "error while GetNetworkByName(%s)", networkName)
	}

	if hcnNetwork == nil {
		return nil, fmt.Errorf("network %v not found", networkName)
	}

	if  hcnNetwork.Type != hcn.L2Bridge {
		return nil, fmt.Errorf("network %v is of unexpected type: %v", networkName, hcnNetwork.Type)
	}

	epName := hns.ConstructEndpointName(args.ContainerID, args.Netns, n.Name)

	hcnEndpoint, err := hns.AddHcnEndpoint(epName, hcnNetwork.Id, args.Netns, func() (*hcn.HostComputeEndpoint, error) {
		epInfo, err := ProcessEndpointArgs(args, n)
		if err != nil {
			return nil, errors.Annotatef(err, "error while ProcessEndpointArgs")
		}
		epInfo.NetworkId = hcnNetwork.Id

		hcnEndpoint, err := hns.GenerateHcnEndpoint(epInfo, &n.NetConf)
		if err != nil {
			return nil, errors.Annotatef(err, "error while GenerateHcnEndpoint")
		}
		return hcnEndpoint, nil
	})
	if err != nil {
		return nil, errors.Annotatef(err, "error while AddHcnEndpoint(%v,%v,%v)", epName, hcnNetwork.Id, args.Netns)
	}

	result, err := hns.ConstructHcnResult(hcnNetwork, hcnEndpoint)
	if err != nil {
		return nil, errors.Annotatef(err, "error while ConstructHcnResult")
	}

	return result, nil
}

func cmdAdd(args *skel.CmdArgs) error {
	n, cniVersion, err := loadNetConf(args.StdinData)
	if err != nil {
		return errors.Annotate(err, "error while loadNetConf")
	}

	var result *current.Result
	if n.ApiVersion == 2 {
		result, err = cmdHcnAdd(args, n)
	} else {
		result, err = cmdHnsAdd(args, n)
	}

	if err != nil {
		os.Setenv("CNI_COMMAND", "DEL")
		ipam.ExecDel(n.IPAM.Type, args.StdinData)
		os.Setenv("CNI_COMMAND", "ADD")
		return errors.Annotate(err, "error while executing ADD command")
	}

	if (result == nil) {
		return errors.New("result for ADD not populated correctly")
	}
	return types.PrintResult(result, cniVersion)
}

func cmdDel(args *skel.CmdArgs) error {
	n, _, err := loadNetConf(args.StdinData)
	if err != nil {
		return err
	}

	if n.IPAM.Type != "" {
		if err := ipam.ExecDel(n.IPAM.Type, args.StdinData); err != nil {
			return err
		}
	}
	epName := hns.ConstructEndpointName(args.ContainerID, args.Netns, n.Name)

	if n.ApiVersion == 2 {
		return hns.RemoveHcnEndpoint(epName)
	} else {
		return hns.DeprovisionEndpoint(epName, args.Netns, args.ContainerID)
	}
}

func cmdCheck(_ *skel.CmdArgs) error {
	// TODO: implement
	return nil
}

func main() {
	skel.PluginMain(cmdAdd, cmdCheck, cmdDel, version.PluginSupports("0.1.0", "0.2.0", "0.3.0"), bv.BuildString("win-bridge"))
}
