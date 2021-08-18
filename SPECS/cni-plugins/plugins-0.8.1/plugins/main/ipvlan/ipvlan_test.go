// Copyright 2015 CNI authors
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
	"net"
	"syscall"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/containernetworking/plugins/pkg/testutils"

	"github.com/vishvananda/netlink"

	"github.com/containernetworking/plugins/plugins/ipam/host-local/backend/allocator"
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

const MASTER_NAME = "eth0"

type Net struct {
	Name          string                 `json:"name"`
	CNIVersion    string                 `json:"cniVersion"`
	Type          string                 `json:"type,omitempty"`
	Master        string                 `json:"master"`
	Mode          string                 `json:"mode"`
	IPAM          *allocator.IPAMConfig  `json:"ipam"`
	DNS           types.DNS              `json:"dns"`
	RawPrevResult map[string]interface{} `json:"prevResult,omitempty"`
	PrevResult    current.Result         `json:"-"`
}

func buildOneConfig(netName string, cniVersion string, master string, orig *Net, prevResult types.Result) (*Net, error) {
	var err error

	inject := map[string]interface{}{
		"name":       netName,
		"cniVersion": cniVersion,
	}
	// Add previous plugin result
	if prevResult != nil {
		inject["prevResult"] = prevResult
	}
	if orig.IPAM == nil {
		inject["master"] = master
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

func ipvlanAddDelTest(conf, IFNAME string, originalNS ns.NetNS) {
	targetNs, err := testutils.NewNS()
	Expect(err).NotTo(HaveOccurred())
	defer targetNs.Close()

	args := &skel.CmdArgs{
		ContainerID: "dummy",
		Netns:       targetNs.Path(),
		IfName:      IFNAME,
		StdinData:   []byte(conf),
	}

	var result *current.Result
	err = originalNS.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		r, _, err := testutils.CmdAddWithArgs(args, func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())

		result, err = current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		Expect(len(result.Interfaces)).To(Equal(1))
		Expect(result.Interfaces[0].Name).To(Equal(IFNAME))
		Expect(len(result.IPs)).To(Equal(1))
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	// Make sure ipvlan link exists in the target namespace
	err = targetNs.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		link, err := netlink.LinkByName(IFNAME)
		Expect(err).NotTo(HaveOccurred())
		Expect(link.Attrs().Name).To(Equal(IFNAME))

		hwaddr, err := net.ParseMAC(result.Interfaces[0].Mac)
		Expect(err).NotTo(HaveOccurred())
		Expect(link.Attrs().HardwareAddr).To(Equal(hwaddr))

		addrs, err := netlink.AddrList(link, syscall.AF_INET)
		Expect(err).NotTo(HaveOccurred())
		Expect(len(addrs)).To(Equal(1))
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	err = originalNS.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		err = testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	// Make sure ipvlan link has been deleted
	err = targetNs.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		link, err := netlink.LinkByName(IFNAME)
		Expect(err).To(HaveOccurred())
		Expect(link).To(BeNil())
		return nil
	})
	Expect(err).NotTo(HaveOccurred())
}

func ipvlanAddCheckDelTest(conf string, netName string, IFNAME string, originalNS ns.NetNS) {
	targetNs, err := testutils.NewNS()
	Expect(err).NotTo(HaveOccurred())
	defer targetNs.Close()

	args := &skel.CmdArgs{
		ContainerID: "dummy",
		Netns:       targetNs.Path(),
		IfName:      IFNAME,
		StdinData:   []byte(conf),
	}

	var result *current.Result
	err = originalNS.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		r, _, err := testutils.CmdAddWithArgs(args, func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())

		result, err = current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		Expect(len(result.Interfaces)).To(Equal(1))
		Expect(result.Interfaces[0].Name).To(Equal(IFNAME))
		Expect(len(result.IPs)).To(Equal(1))
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	// Make sure ipvlan link exists in the target namespace
	err = targetNs.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		link, err := netlink.LinkByName(IFNAME)
		Expect(err).NotTo(HaveOccurred())
		Expect(link.Attrs().Name).To(Equal(IFNAME))

		hwaddr, err := net.ParseMAC(result.Interfaces[0].Mac)
		Expect(err).NotTo(HaveOccurred())
		Expect(link.Attrs().HardwareAddr).To(Equal(hwaddr))

		addrs, err := netlink.AddrList(link, syscall.AF_INET)
		Expect(err).NotTo(HaveOccurred())
		Expect(len(addrs)).To(Equal(1))
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	n := &Net{}
	err = json.Unmarshal([]byte(conf), &n)
	Expect(err).NotTo(HaveOccurred())

	if n.IPAM != nil {
		n.IPAM, _, err = allocator.LoadIPAMConfig([]byte(conf), "")
		Expect(err).NotTo(HaveOccurred())
	}

	cniVersion := "0.4.0"
	newConf, err := buildOneConfig(netName, cniVersion, MASTER_NAME, n, result)
	Expect(err).NotTo(HaveOccurred())

	confString, err := json.Marshal(newConf)
	Expect(err).NotTo(HaveOccurred())

	args.StdinData = confString

	// CNI Check on macvlan in the target namespace
	err = originalNS.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		err := testutils.CmdCheckWithArgs(args, func() error {
			return cmdCheck(args)
		})
		Expect(err).NotTo(HaveOccurred())
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	err = originalNS.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		err = testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	// Make sure ipvlan link has been deleted
	err = targetNs.Do(func(ns.NetNS) error {
		defer GinkgoRecover()

		link, err := netlink.LinkByName(IFNAME)
		Expect(err).To(HaveOccurred())
		Expect(link).To(BeNil())
		return nil
	})
	Expect(err).NotTo(HaveOccurred())
}

var _ = Describe("ipvlan Operations", func() {
	var originalNS ns.NetNS

	BeforeEach(func() {
		// Create a new NetNS so we don't modify the host
		var err error
		originalNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			// Add master
			err = netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: MASTER_NAME,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			_, err = netlink.LinkByName(MASTER_NAME)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	AfterEach(func() {
		Expect(originalNS.Close()).To(Succeed())
	})

	It("creates an ipvlan link in a non-default namespace", func() {
		conf := &NetConf{
			NetConf: types.NetConf{
				CNIVersion: "0.3.1",
				Name:       "testConfig",
				Type:       "ipvlan",
			},
			Master: MASTER_NAME,
			Mode:   "l2",
			MTU:    1500,
		}

		// Create ipvlan in other namespace
		targetNs, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		defer targetNs.Close()

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			_, err := createIpvlan(conf, "foobar0", targetNs)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})

		Expect(err).NotTo(HaveOccurred())

		// Make sure ipvlan link exists in the target namespace
		err = targetNs.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			link, err := netlink.LinkByName("foobar0")
			Expect(err).NotTo(HaveOccurred())
			Expect(link.Attrs().Name).To(Equal("foobar0"))
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("configures and deconfigures an iplvan link with ADD/DEL", func() {
		const IFNAME = "ipvl0"

		conf := fmt.Sprintf(`{
    "cniVersion": "0.3.1",
    "name": "mynet",
    "type": "ipvlan",
    "master": "%s",
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`, MASTER_NAME)

		ipvlanAddDelTest(conf, IFNAME, originalNS)
	})

	It("configures and deconfigures an iplvan link with ADD/DEL when chained", func() {
		const IFNAME = "ipvl0"

		conf := fmt.Sprintf(`{
    "cniVersion": "0.3.1",
    "name": "mynet",
    "type": "ipvlan",
    "prevResult": {
            "interfaces": [
                    {
                            "name": "%s"
                    }
            ],
            "ips": [
                    {
                            "version": "4",
                            "address": "10.1.2.2/24",
                            "gateway": "10.1.2.1",
                            "interface": 0
                    }
            ],
            "routes": []
    }
}`, MASTER_NAME)

		ipvlanAddDelTest(conf, IFNAME, originalNS)
	})

	It("deconfigures an unconfigured ipvlan link with DEL", func() {
		const IFNAME = "ipvl0"

		conf := fmt.Sprintf(`{
    "cniVersion": "0.3.0",
    "name": "mynet",
    "type": "ipvlan",
    "master": "%s",
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`, MASTER_NAME)

		targetNs, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		defer targetNs.Close()

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      IFNAME,
			StdinData:   []byte(conf),
		}

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			err = testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("configures and deconfigures a cniVersion 0.4.0 iplvan link with ADD/CHECK/DEL", func() {
		const IFNAME = "ipvl0"

		conf := fmt.Sprintf(`{
    "cniVersion": "0.4.0",
    "name": "ipvlanTest1",
    "type": "ipvlan",
    "master": "%s",
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`, MASTER_NAME)

		ipvlanAddCheckDelTest(conf, "ipvlanTest1", IFNAME, originalNS)
	})

	It("configures and deconfigures a cniVersion 0.4.0 iplvan link with ADD/CHECK/DEL when chained", func() {
		const IFNAME = "ipvl0"

		conf := fmt.Sprintf(`{
	       "cniVersion": "0.4.0",
	       "name": "ipvlanTest2",
	       "type": "ipvlan",
	       "prevResult": {
	               "interfaces": [
	                       {
	                               "name": "%s"
	                       }
	               ],
	               "ips": [
	                       {
	                               "version": "4",
	                               "address": "10.1.2.2/24",
	                               "gateway": "10.1.2.1",
	                               "interface": 0
	                       }
	               ],
	               "routes": []
	       }
	   }`, MASTER_NAME)

		ipvlanAddCheckDelTest(conf, "ipvlanTest2", IFNAME, originalNS)
	})
})
