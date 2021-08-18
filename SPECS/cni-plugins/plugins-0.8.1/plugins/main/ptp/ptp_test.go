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

type Net struct {
	Name          string                 `json:"name"`
	CNIVersion    string                 `json:"cniVersion"`
	Type          string                 `json:"type,omitempty"`
	IPMasq        bool                   `json:"ipMasq"`
	MTU           int                    `json:"mtu"`
	IPAM          *allocator.IPAMConfig  `json:"ipam"`
	DNS           types.DNS              `json:"dns"`
	RawPrevResult map[string]interface{} `json:"prevResult,omitempty"`
	PrevResult    current.Result         `json:"-"`
}

func buildOneConfig(netName string, cniVersion string, orig *Net, prevResult types.Result) (*Net, error) {
	var err error

	inject := map[string]interface{}{
		"name":       netName,
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

var _ = Describe("ptp Operations", func() {
	var originalNS ns.NetNS

	BeforeEach(func() {
		// Create a new NetNS so we don't modify the host
		var err error
		originalNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
	})

	AfterEach(func() {
		Expect(originalNS.Close()).To(Succeed())
	})

	doTest := func(conf string, numIPs int) {
		const IFNAME = "ptp0"

		targetNs, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		defer targetNs.Close()

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      IFNAME,
			StdinData:   []byte(conf),
		}

		var resI types.Result
		var res *current.Result

		// Execute the plugin with the ADD command, creating the veth endpoints
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			resI, _, err = testutils.CmdAddWithArgs(args, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		res, err = current.NewResultFromResult(resI)
		Expect(err).NotTo(HaveOccurred())

		// Make sure ptp link exists in the target namespace
		// Then, ping the gateway
		seenIPs := 0

		wantMac := ""
		err = targetNs.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			link, err := netlink.LinkByName(IFNAME)
			Expect(err).NotTo(HaveOccurred())
			wantMac = link.Attrs().HardwareAddr.String()

			for _, ipc := range res.IPs {
				if *ipc.Interface != 1 {
					continue
				}
				seenIPs += 1
				saddr := ipc.Address.IP.String()
				daddr := ipc.Gateway.String()
				fmt.Fprintln(GinkgoWriter, "ping", saddr, "->", daddr)

				if err := testutils.Ping(saddr, daddr, (ipc.Version == "6"), 30); err != nil {
					return fmt.Errorf("ping %s -> %s failed: %s", saddr, daddr, err)
				}
			}

			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		Expect(seenIPs).To(Equal(numIPs))

		// make sure the interfaces are correct
		Expect(res.Interfaces).To(HaveLen(2))

		Expect(res.Interfaces[0].Name).To(HavePrefix("veth"))
		Expect(res.Interfaces[0].Mac).To(HaveLen(17))
		Expect(res.Interfaces[0].Sandbox).To(BeEmpty())

		Expect(res.Interfaces[1].Name).To(Equal(IFNAME))
		Expect(res.Interfaces[1].Mac).To(Equal(wantMac))
		Expect(res.Interfaces[1].Sandbox).To(Equal(targetNs.Path()))

		// Call the plugins with the DEL command, deleting the veth endpoints
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			err := testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// Make sure ptp link has been deleted
		err = targetNs.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			link, err := netlink.LinkByName(IFNAME)
			Expect(err).To(HaveOccurred())
			Expect(link).To(BeNil())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	}

	doTestv4 := func(conf string, netName string, numIPs int) {
		const IFNAME = "ptp0"

		targetNs, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		defer targetNs.Close()

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      IFNAME,
			StdinData:   []byte(conf),
		}

		var resI types.Result
		var res *current.Result

		// Execute the plugin with the ADD command, creating the veth endpoints
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			resI, _, err = testutils.CmdAddWithArgs(args, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		res, err = current.NewResultFromResult(resI)
		Expect(err).NotTo(HaveOccurred())

		// Make sure ptp link exists in the target namespace
		// Then, ping the gateway
		seenIPs := 0

		wantMac := ""
		err = targetNs.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			link, err := netlink.LinkByName(IFNAME)
			Expect(err).NotTo(HaveOccurred())
			wantMac = link.Attrs().HardwareAddr.String()

			for _, ipc := range res.IPs {
				if *ipc.Interface != 1 {
					continue
				}
				seenIPs += 1
				saddr := ipc.Address.IP.String()
				daddr := ipc.Gateway.String()
				fmt.Fprintln(GinkgoWriter, "ping", saddr, "->", daddr)

				if err := testutils.Ping(saddr, daddr, (ipc.Version == "6"), 30); err != nil {
					return fmt.Errorf("ping %s -> %s failed: %s", saddr, daddr, err)
				}
			}

			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		Expect(seenIPs).To(Equal(numIPs))

		// make sure the interfaces are correct
		Expect(res.Interfaces).To(HaveLen(2))

		Expect(res.Interfaces[0].Name).To(HavePrefix("veth"))
		Expect(res.Interfaces[0].Mac).To(HaveLen(17))
		Expect(res.Interfaces[0].Sandbox).To(BeEmpty())

		Expect(res.Interfaces[1].Name).To(Equal(IFNAME))
		Expect(res.Interfaces[1].Mac).To(Equal(wantMac))
		Expect(res.Interfaces[1].Sandbox).To(Equal(targetNs.Path()))

		// call CmdCheck
		n := &Net{}
		err = json.Unmarshal([]byte(conf), &n)
		Expect(err).NotTo(HaveOccurred())

		n.IPAM, _, err = allocator.LoadIPAMConfig([]byte(conf), "")
		Expect(err).NotTo(HaveOccurred())

		cniVersion := "0.4.0"
		newConf, err := buildOneConfig(netName, cniVersion, n, res)
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

		args.StdinData = []byte(conf)

		// Call the plugins with the DEL command, deleting the veth endpoints
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			err := testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		// Make sure ptp link has been deleted
		err = targetNs.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			link, err := netlink.LinkByName(IFNAME)
			Expect(err).To(HaveOccurred())
			Expect(link).To(BeNil())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	}

	It("configures and deconfigures a ptp link with ADD/DEL", func() {
		conf := `{
    "cniVersion": "0.3.1",
    "name": "mynet",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 5000,
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`

		doTest(conf, 1)
	})

	It("configures and deconfigures a dual-stack ptp link with ADD/DEL", func() {
		conf := `{
    "cniVersion": "0.3.1",
    "name": "mynet",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 5000,
    "ipam": {
        "type": "host-local",
		"ranges": [
			[{ "subnet": "10.1.2.0/24"}],
			[{ "subnet": "2001:db8:1::0/66"}]
		]
    }
}`

		doTest(conf, 2)
	})

	It("deconfigures an unconfigured ptp link with DEL", func() {
		const IFNAME = "ptp0"

		conf := `{
    "cniVersion": "0.3.0",
    "name": "mynet",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 5000,
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`

		targetNs, err := testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
		defer targetNs.Close()

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      IFNAME,
			StdinData:   []byte(conf),
		}

		// Call the plugins with the DEL command. It should not error even though the veth doesn't exist.
		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			err := testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("configures and deconfigures a CNI V4 ptp link with ADD/DEL", func() {
		conf := `{
    "cniVersion": "0.4.0",
    "name": "ptpNetv4",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 5000,
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`

		doTestv4(conf, "ptpNetv4", 1)
	})

	It("configures and deconfigures a CNI V4 dual-stack ptp link with ADD/DEL", func() {
		conf := `{
    "cniVersion": "0.4.0",
    "name": "ptpNetv4ds",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 5000,
    "ipam": {
        "type": "host-local",
		"ranges": [
			[{ "subnet": "10.1.2.0/24"}],
			[{ "subnet": "2001:db8:1::0/66"}]
		]
    }
}`

		doTestv4(conf, "ptpNetv4ds", 2)
	})
})
