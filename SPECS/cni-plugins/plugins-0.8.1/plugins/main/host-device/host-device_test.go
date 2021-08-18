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
	"math/rand"
	"net"
	"strings"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	types020 "github.com/containernetworking/cni/pkg/types/020"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/containernetworking/plugins/pkg/testutils"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	"github.com/vishvananda/netlink"
)

type Net struct {
	Name          string                 `json:"name"`
	CNIVersion    string                 `json:"cniVersion"`
	Type          string                 `json:"type,omitempty"`
	Device        string                 `json:"device"`     // Device-Name, something like eth0 or can0 etc.
	HWAddr        string                 `json:"hwaddr"`     // MAC Address of target network interface
	KernelPath    string                 `json:"kernelpath"` // Kernelpath of the device
	PCIAddr       string                 `json:"pciBusID"`   // PCI Address of target network device
	IPAM          *IPAMConfig            `json:"ipam,omitempty"`
	DNS           types.DNS              `json:"dns"`
	RawPrevResult map[string]interface{} `json:"prevResult,omitempty"`
	PrevResult    current.Result         `json:"-"`
}

type IPAMConfig struct {
	Name      string
	Type      string         `json:"type"`
	Routes    []*types.Route `json:"routes"`
	Addresses []Address      `json:"addresses,omitempty"`
	DNS       types.DNS      `json:"dns"`
}

type IPAMEnvArgs struct {
	types.CommonArgs
	IP      types.UnmarshallableString `json:"ip,omitempty"`
	GATEWAY types.UnmarshallableString `json:"gateway,omitempty"`
}

type Address struct {
	AddressStr string `json:"address"`
	Gateway    net.IP `json:"gateway,omitempty"`
	Address    net.IPNet
	Version    string
}

// canonicalizeIP makes sure a provided ip is in standard form
func canonicalizeIP(ip *net.IP) error {
	if ip.To4() != nil {
		*ip = ip.To4()
		return nil
	} else if ip.To16() != nil {
		*ip = ip.To16()
		return nil
	}
	return fmt.Errorf("IP %s not v4 nor v6", *ip)
}

// LoadIPAMConfig creates IPAMConfig using json encoded configuration provided
// as `bytes`. At the moment values provided in envArgs are ignored so there
// is no possibility to overload the json configuration using envArgs
func LoadIPAMConfig(bytes []byte, envArgs string) (*IPAMConfig, string, error) {
	n := Net{}
	if err := json.Unmarshal(bytes, &n); err != nil {
		return nil, "", err
	}

	if n.IPAM == nil {
		return nil, "", fmt.Errorf("IPAM config missing 'ipam' key")
	}

	// Validate all ranges
	numV4 := 0
	numV6 := 0

	for i := range n.IPAM.Addresses {
		ip, addr, err := net.ParseCIDR(n.IPAM.Addresses[i].AddressStr)
		if err != nil {
			return nil, "", fmt.Errorf("invalid CIDR %s: %s", n.IPAM.Addresses[i].AddressStr, err)
		}
		n.IPAM.Addresses[i].Address = *addr
		n.IPAM.Addresses[i].Address.IP = ip

		if err := canonicalizeIP(&n.IPAM.Addresses[i].Address.IP); err != nil {
			return nil, "", fmt.Errorf("invalid address %d: %s", i, err)
		}

		if n.IPAM.Addresses[i].Address.IP.To4() != nil {
			n.IPAM.Addresses[i].Version = "4"
			numV4++
		} else {
			n.IPAM.Addresses[i].Version = "6"
			numV6++
		}
	}

	if envArgs != "" {
		e := IPAMEnvArgs{}
		err := types.LoadArgs(envArgs, &e)
		if err != nil {
			return nil, "", err
		}

		if e.IP != "" {
			for _, item := range strings.Split(string(e.IP), ",") {
				ipstr := strings.TrimSpace(item)

				ip, subnet, err := net.ParseCIDR(ipstr)
				if err != nil {
					return nil, "", fmt.Errorf("invalid CIDR %s: %s", ipstr, err)
				}

				addr := Address{Address: net.IPNet{IP: ip, Mask: subnet.Mask}}
				if addr.Address.IP.To4() != nil {
					addr.Version = "4"
					numV4++
				} else {
					addr.Version = "6"
					numV6++
				}
				n.IPAM.Addresses = append(n.IPAM.Addresses, addr)
			}
		}

		if e.GATEWAY != "" {
			for _, item := range strings.Split(string(e.GATEWAY), ",") {
				gwip := net.ParseIP(strings.TrimSpace(item))
				if gwip == nil {
					return nil, "", fmt.Errorf("invalid gateway address: %s", item)
				}

				for i := range n.IPAM.Addresses {
					if n.IPAM.Addresses[i].Address.Contains(gwip) {
						n.IPAM.Addresses[i].Gateway = gwip
					}
				}
			}
		}
	}

	// CNI spec 0.2.0 and below supported only one v4 and v6 address
	if numV4 > 1 || numV6 > 1 {
		for _, v := range types020.SupportedVersions {
			if n.CNIVersion == v {
				return nil, "", fmt.Errorf("CNI version %v does not support more than 1 address per family", n.CNIVersion)
			}
		}
	}

	// Copy net name into IPAM so not to drag Net struct around
	n.IPAM.Name = n.Name

	return n.IPAM, n.CNIVersion, nil
}

func buildOneConfig(name, cniVersion string, orig *Net, prevResult types.Result) (*Net, error) {
	var err error

	inject := map[string]interface{}{
		"name":       name,
		"cniVersion": cniVersion,
	}
	// Add previous plugin result
	if prevResult != nil {
		inject["prevResult"] = prevResult
	}

	// Ensure every config uses the same name and version
	config := make(map[string]interface{})

	confBytes, err := json.Marshal(orig)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(confBytes, &config)
	if err != nil {
		return nil, fmt.Errorf("unmarshal existing network bytes: %s", err)
	}

	for key, value := range inject {
		config[key] = value
	}

	newBytes, err := json.Marshal(config)
	if err != nil {
		return nil, err
	}

	conf := &Net{}
	if err := json.Unmarshal(newBytes, &conf); err != nil {
		return nil, fmt.Errorf("error parsing configuration: %s", err)
	}

	return conf, nil

}

var _ = Describe("base functionality", func() {
	var originalNS ns.NetNS
	var ifname string

	BeforeEach(func() {
		var err error
		originalNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		ifname = fmt.Sprintf("dummy-%x", rand.Int31())
	})

	AfterEach(func() {
		originalNS.Close()
	})

	It("Works with a valid config without IPAM", func() {
		var origLink netlink.Link

		// prepare ifname in original namespace
		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err := netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: ifname,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			origLink, err = netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			err = netlink.LinkSetUp(origLink)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// call CmdAdd
		targetNS, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		cniName := "eth0"
		conf := fmt.Sprintf(`{
			"cniVersion": "0.3.0",
			"name": "cni-plugin-host-device-test",
			"type": "host-device",
			"device": %q
		}`, ifname)
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      cniName,
			StdinData:   []byte(conf),
		}
		var resI types.Result
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			var err error
			resI, _, err = testutils.CmdAddWithArgs(args, func() error { return cmdAdd(args) })
			return err
		})
		Expect(err).NotTo(HaveOccurred())

		// check that the result was sane
		res, err := current.NewResultFromResult(resI)
		Expect(err).NotTo(HaveOccurred())
		Expect(res.Interfaces).To(Equal([]*current.Interface{
			{
				Name:    cniName,
				Mac:     origLink.Attrs().HardwareAddr.String(),
				Sandbox: targetNS.Path(),
			},
		}))

		// assert that dummy0 is now in the target namespace
		err = targetNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			link, err := netlink.LinkByName(cniName)
			Expect(err).NotTo(HaveOccurred())
			Expect(link.Attrs().HardwareAddr).To(Equal(origLink.Attrs().HardwareAddr))
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// assert that dummy0 is now NOT in the original namespace anymore
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			_, err := netlink.LinkByName(ifname)
			Expect(err).To(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// Check that deleting the device moves it back and restores the name
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err = testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())

			_, err := netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

	})

	It("Works with a valid config with IPAM", func() {
		var origLink netlink.Link

		// prepare ifname in original namespace
		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err := netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: ifname,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			origLink, err = netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			err = netlink.LinkSetUp(origLink)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// call CmdAdd
		targetNS, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		targetIP := "10.10.0.1/24"
		cniName := "eth0"
		conf := fmt.Sprintf(`{
			"cniVersion": "0.3.0",
			"name": "cni-plugin-host-device-test",
			"type": "host-device",
			"ipam": {
				"type": "static",
				"addresses": [
					{
					"address":"`+targetIP+`",
					"gateway": "10.10.0.254"
				}]
			},
			"device": %q
		}`, ifname)
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      cniName,
			StdinData:   []byte(conf),
		}
		var resI types.Result
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			var err error
			resI, _, err = testutils.CmdAddWithArgs(args, func() error { return cmdAdd(args) })
			return err
		})
		Expect(err).NotTo(HaveOccurred())

		// check that the result was sane
		res, err := current.NewResultFromResult(resI)
		Expect(err).NotTo(HaveOccurred())
		Expect(res.Interfaces).To(Equal([]*current.Interface{
			{
				Name:    cniName,
				Mac:     origLink.Attrs().HardwareAddr.String(),
				Sandbox: targetNS.Path(),
			},
		}))

		// assert that dummy0 is now in the target namespace
		err = targetNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			link, err := netlink.LinkByName(cniName)
			Expect(err).NotTo(HaveOccurred())
			Expect(link.Attrs().HardwareAddr).To(Equal(origLink.Attrs().HardwareAddr))

			//get the IP address of the interface in the target namespace
			addrs, err := netlink.AddrList(link, netlink.FAMILY_V4)
			Expect(err).NotTo(HaveOccurred())
			addr := addrs[0].IPNet.String()
			//assert that IP address is what we set
			Expect(addr).To(Equal(targetIP))

			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// assert that dummy0 is now NOT in the original namespace anymore
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			_, err := netlink.LinkByName(ifname)
			Expect(err).To(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// Check that deleting the device moves it back and restores the name
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err = testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())

			_, err := netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

	})

	It("fails an invalid config", func() {
		conf := `{
			"cniVersion": "0.3.0",
			"name": "cni-plugin-host-device-test",
			"type": "host-device"
		}`

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       originalNS.Path(),
			IfName:      ifname,
			StdinData:   []byte(conf),
		}
		_, _, err := testutils.CmdAddWithArgs(args, func() error { return cmdAdd(args) })
		Expect(err).To(MatchError(`specify either "device", "hwaddr", "kernelpath" or "pciBusID"`))

	})

	It("Works with a valid 0.4.0 config without IPAM", func() {
		var origLink netlink.Link

		// prepare ifname in original namespace
		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err := netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: ifname,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			origLink, err = netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			err = netlink.LinkSetUp(origLink)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// call CmdAdd
		targetNS, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		cniName := "eth0"
		conf := fmt.Sprintf(`{
			"cniVersion": "0.4.0",
			"name": "cni-plugin-host-device-test",
			"type": "host-device",
			"device": %q
		}`, ifname)
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      cniName,
			StdinData:   []byte(conf),
		}
		var resI types.Result
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			var err error
			resI, _, err = testutils.CmdAddWithArgs(args, func() error { return cmdAdd(args) })
			return err
		})
		Expect(err).NotTo(HaveOccurred())

		// check that the result was sane
		res, err := current.NewResultFromResult(resI)
		Expect(err).NotTo(HaveOccurred())
		Expect(res.Interfaces).To(Equal([]*current.Interface{
			{
				Name:    cniName,
				Mac:     origLink.Attrs().HardwareAddr.String(),
				Sandbox: targetNS.Path(),
			},
		}))

		// assert that dummy0 is now in the target namespace
		err = targetNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			link, err := netlink.LinkByName(cniName)
			Expect(err).NotTo(HaveOccurred())
			Expect(link.Attrs().HardwareAddr).To(Equal(origLink.Attrs().HardwareAddr))
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// assert that dummy0 is now NOT in the original namespace anymore
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			_, err := netlink.LinkByName(ifname)
			Expect(err).To(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// call CmdCheck
		n := &Net{}
		err = json.Unmarshal([]byte(conf), &n)
		Expect(err).NotTo(HaveOccurred())

		cniVersion := "0.4.0"
		newConf, err := buildOneConfig("testConfig", cniVersion, n, res)
		Expect(err).NotTo(HaveOccurred())

		confString, err := json.Marshal(newConf)
		Expect(err).NotTo(HaveOccurred())

		args.StdinData = confString

		// CNI Check host-device in the target namespace

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			var err error
			err = testutils.CmdCheckWithArgs(args, func() error { return cmdCheck(args) })
			return err
		})
		Expect(err).NotTo(HaveOccurred())

		// Check that deleting the device moves it back and restores the name
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err = testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())

			_, err := netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

	})

	It("Works with a valid 0.4.0 config with IPAM", func() {
		var origLink netlink.Link

		// prepare ifname in original namespace
		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err := netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: ifname,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			origLink, err = netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			err = netlink.LinkSetUp(origLink)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// call CmdAdd
		targetNS, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		targetIP := "10.10.0.1/24"
		cniName := "eth0"
		conf := fmt.Sprintf(`{
			"cniVersion": "0.4.0",
			"name": "cni-plugin-host-device-test",
			"type": "host-device",
			"ipam": {
				"type": "static",
				"addresses": [
					{
					"address":"`+targetIP+`",
					"gateway": "10.10.0.254"
				}]
			},
			"device": %q
		}`, ifname)
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      cniName,
			StdinData:   []byte(conf),
		}
		var resI types.Result
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			var err error
			resI, _, err = testutils.CmdAddWithArgs(args, func() error { return cmdAdd(args) })
			return err
		})
		Expect(err).NotTo(HaveOccurred())

		// check that the result was sane
		res, err := current.NewResultFromResult(resI)
		Expect(err).NotTo(HaveOccurred())
		Expect(res.Interfaces).To(Equal([]*current.Interface{
			{
				Name:    cniName,
				Mac:     origLink.Attrs().HardwareAddr.String(),
				Sandbox: targetNS.Path(),
			},
		}))

		// assert that dummy0 is now in the target namespace
		err = targetNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			link, err := netlink.LinkByName(cniName)
			Expect(err).NotTo(HaveOccurred())
			Expect(link.Attrs().HardwareAddr).To(Equal(origLink.Attrs().HardwareAddr))

			//get the IP address of the interface in the target namespace
			addrs, err := netlink.AddrList(link, netlink.FAMILY_V4)
			Expect(err).NotTo(HaveOccurred())
			addr := addrs[0].IPNet.String()
			//assert that IP address is what we set
			Expect(addr).To(Equal(targetIP))

			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// assert that dummy0 is now NOT in the original namespace anymore
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			_, err := netlink.LinkByName(ifname)
			Expect(err).To(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// call CmdCheck
		n := &Net{}
		err = json.Unmarshal([]byte(conf), &n)
		Expect(err).NotTo(HaveOccurred())

		n.IPAM, _, err = LoadIPAMConfig([]byte(conf), "")
		Expect(err).NotTo(HaveOccurred())

		cniVersion := "0.4.0"
		newConf, err := buildOneConfig("testConfig", cniVersion, n, res)
		Expect(err).NotTo(HaveOccurred())

		confString, err := json.Marshal(newConf)
		Expect(err).NotTo(HaveOccurred())

		args.StdinData = confString

		// CNI Check host-device in the target namespace

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			var err error
			err = testutils.CmdCheckWithArgs(args, func() error { return cmdCheck(args) })
			return err
		})
		Expect(err).NotTo(HaveOccurred())

		// Check that deleting the device moves it back and restores the name
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()
			err = testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())

			_, err := netlink.LinkByName(ifname)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

	})

})
