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
	"context"
	"encoding/json"
	"fmt"
	"net"
	"time"

	"github.com/vishvananda/netlink"

	"github.com/containernetworking/cni/pkg/invoke"
	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/containernetworking/plugins/pkg/testutils"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	"github.com/onsi/gomega/gexec"
)

func buildOneConfig(name, cniVersion string, orig *PluginConf, prevResult types.Result) (*PluginConf, []byte, error) {
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
		return nil, nil, err
	}

	err = json.Unmarshal(confBytes, &config)
	if err != nil {
		return nil, nil, fmt.Errorf("unmarshal existing network bytes: %s", err)
	}

	for key, value := range inject {
		config[key] = value
	}

	newBytes, err := json.Marshal(config)
	if err != nil {
		return nil, nil, err
	}

	conf := &PluginConf{}
	if err := json.Unmarshal(newBytes, &conf); err != nil {
		return nil, nil, fmt.Errorf("error parsing configuration: %s", err)
	}

	return conf, newBytes, nil

}

var _ = Describe("bandwidth test", func() {
	var (
		hostNs          ns.NetNS
		containerNs     ns.NetNS
		ifbDeviceName   string
		hostIfname      string
		containerIfname string
		hostIP          net.IP
		containerIP     net.IP
		hostIfaceMTU    int
	)

	BeforeEach(func() {
		var err error

		hostIfname = "host-veth"
		containerIfname = "container-veth"

		hostNs, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		containerNs, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		hostIP = net.IP{169, 254, 0, 1}
		containerIP = net.IP{10, 254, 0, 1}
		hostIfaceMTU = 1024
		ifbDeviceName = "5b6c"

		createVeth(hostNs.Path(), hostIfname, containerNs.Path(), containerIfname, hostIP, containerIP, hostIfaceMTU)
	})

	AfterEach(func() {
		containerNs.Close()
		hostNs.Close()
	})

	Describe("cmdADD", func() {
		It("Works with a Veth pair using 0.3.0 config", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 8,
	"ingressBurst": 8,
	"egressRate": 16,
	"egressBurst": 8,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()
				r, out, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))
				result, err := current.GetResult(r)
				Expect(err).NotTo(HaveOccurred())

				Expect(result.Interfaces).To(HaveLen(3))
				Expect(result.Interfaces[2].Name).To(Equal(ifbDeviceName))
				Expect(result.Interfaces[2].Sandbox).To(Equal(""))

				ifbLink, err := netlink.LinkByName(ifbDeviceName)
				Expect(err).NotTo(HaveOccurred())
				Expect(ifbLink.Attrs().MTU).To(Equal(hostIfaceMTU))

				qdiscs, err := netlink.QdiscList(ifbLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(1))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(ifbLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(2)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(1)))

				hostVethLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscFilters, err := netlink.FilterList(hostVethLink, netlink.MakeHandle(0xffff, 0))
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscFilters).To(HaveLen(1))
				Expect(qdiscFilters[0].(*netlink.U32).Actions[0].(*netlink.MirredAction).Ifindex).To(Equal(ifbLink.Attrs().Index))

				return nil
			})).To(Succeed())

			Expect(hostNs.Do(func(n ns.NetNS) error {
				defer GinkgoRecover()

				ifbLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscs, err := netlink.QdiscList(ifbLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(2))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(ifbLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(1)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(1)))
				return nil
			})).To(Succeed())

		})

		It("Does not apply ingress when disabled", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 0,
	"ingressBurst": 0,
	"egressRate": 8000,
	"egressBurst": 80,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, out, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, ifbDeviceName, []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))

				_, err = netlink.LinkByName(ifbDeviceName)
				Expect(err).NotTo(HaveOccurred())
				return nil
			})).To(Succeed())

			Expect(hostNs.Do(func(n ns.NetNS) error {
				defer GinkgoRecover()

				containerIfLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscs, err := netlink.QdiscList(containerIfLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(2))
				Expect(qdiscs[0]).NotTo(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[1]).NotTo(BeAssignableToTypeOf(&netlink.Tbf{}))

				return nil
			})).To(Succeed())

		})

		It("Does not apply egress when disabled", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"egressRate": 0,
	"egressBurst": 0,
	"ingressRate": 8000,
	"ingressBurst": 80,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, out, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, ifbDeviceName, []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))

				_, err = netlink.LinkByName(ifbDeviceName)
				Expect(err).To(HaveOccurred())
				return nil
			})).To(Succeed())

			Expect(hostNs.Do(func(n ns.NetNS) error {
				defer GinkgoRecover()

				containerIfLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscs, err := netlink.QdiscList(containerIfLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(1))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(containerIfLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(1000)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(35)))
				return nil
			})).To(Succeed())

		})

		It("fails an invalid ingress config", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 0,
	"ingressBurst": 123,
	"egressRate": 123,
	"egressBurst": 123,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())

			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      "eth0",
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, _, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).To(MatchError("if burst is set, rate must also be set"))
				return nil
			})).To(Succeed())
		})

		It("Works with a Veth pair using runtime config", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"runtimeConfig": {
		"bandWidth": {
			"ingressRate": 8,
			"ingressBurst": 8,
			"egressRate": 16,
			"egressBurst": 9
		}
	},
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()
				r, out, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))
				result, err := current.GetResult(r)
				Expect(err).NotTo(HaveOccurred())

				Expect(result.Interfaces).To(HaveLen(3))
				Expect(result.Interfaces[2].Name).To(Equal(ifbDeviceName))
				Expect(result.Interfaces[2].Sandbox).To(Equal(""))

				ifbLink, err := netlink.LinkByName(ifbDeviceName)
				Expect(err).NotTo(HaveOccurred())
				Expect(ifbLink.Attrs().MTU).To(Equal(hostIfaceMTU))

				qdiscs, err := netlink.QdiscList(ifbLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(1))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(ifbLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(2)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(1)))

				hostVethLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscFilters, err := netlink.FilterList(hostVethLink, netlink.MakeHandle(0xffff, 0))
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscFilters).To(HaveLen(1))
				Expect(qdiscFilters[0].(*netlink.U32).Actions[0].(*netlink.MirredAction).Ifindex).To(Equal(ifbLink.Attrs().Index))

				return nil
			})).To(Succeed())

			Expect(hostNs.Do(func(n ns.NetNS) error {
				defer GinkgoRecover()

				ifbLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscs, err := netlink.QdiscList(ifbLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(2))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(ifbLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(1)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(1)))
				return nil
			})).To(Succeed())

		})

		It("Should apply static config when both static config and runtime config exist", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 0,
	"ingressBurst": 123,
	"egressRate": 123,
	"egressBurst": 123,
	"runtimeConfig": {
		"bandWidth": {
			"ingressRate": 8,
			"ingressBurst": 8,
			"egressRate": 16,
			"egressBurst": 9
		}
	},
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())

			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      "eth0",
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, _, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).To(MatchError("if burst is set, rate must also be set"))
				return nil
			})).To(Succeed())
		})
	})

	Describe("cmdDEL", func() {
		It("Works with a Veth pair using 0.3.0 config", func() {
			conf := `{
	"cniVersion": "0.3.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 8,
	"ingressBurst": 8,
	"egressRate": 9,
	"egressBurst": 9,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			conf = fmt.Sprintf(conf, hostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()
				_, out, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))

				err = testutils.CmdDel(containerNs.Path(), args.ContainerID, "", func() error { return cmdDel(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))

				_, err = netlink.LinkByName(ifbDeviceName)
				Expect(err).To(HaveOccurred())

				return nil
			})).To(Succeed())

		})
	})

	Describe("Getting the host interface which plugin should work on from veth peer of container interface", func() {
		It("Should work with multiple host veth interfaces", func() {
			conf := `{
	"cniVersion": "0.4.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 8,
	"ingressBurst": 8,
	"egressRate": 16,
	"egressBurst": 8,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			// create veth peer in host ns
			vethName, peerName := "host-veth-peer1", "host-veth-peer2"
			createVethInOneNs(hostNs.Path(), vethName, peerName)

			conf = fmt.Sprintf(conf, vethName, peerName, hostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()
				r, out, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))
				result, err := current.GetResult(r)
				Expect(err).NotTo(HaveOccurred())

				Expect(result.Interfaces).To(HaveLen(5))
				Expect(result.Interfaces[4].Name).To(Equal(ifbDeviceName))
				Expect(result.Interfaces[4].Sandbox).To(Equal(""))

				ifbLink, err := netlink.LinkByName(ifbDeviceName)
				Expect(err).NotTo(HaveOccurred())
				Expect(ifbLink.Attrs().MTU).To(Equal(hostIfaceMTU))

				qdiscs, err := netlink.QdiscList(ifbLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(1))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(ifbLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(2)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(1)))

				hostVethLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscFilters, err := netlink.FilterList(hostVethLink, netlink.MakeHandle(0xffff, 0))
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscFilters).To(HaveLen(1))
				Expect(qdiscFilters[0].(*netlink.U32).Actions[0].(*netlink.MirredAction).Ifindex).To(Equal(ifbLink.Attrs().Index))

				return nil
			})).To(Succeed())

			Expect(hostNs.Do(func(n ns.NetNS) error {
				defer GinkgoRecover()

				ifbLink, err := netlink.LinkByName(hostIfname)
				Expect(err).NotTo(HaveOccurred())

				qdiscs, err := netlink.QdiscList(ifbLink)
				Expect(err).NotTo(HaveOccurred())

				Expect(qdiscs).To(HaveLen(2))
				Expect(qdiscs[0].Attrs().LinkIndex).To(Equal(ifbLink.Attrs().Index))

				Expect(qdiscs[0]).To(BeAssignableToTypeOf(&netlink.Tbf{}))
				Expect(qdiscs[0].(*netlink.Tbf).Rate).To(Equal(uint64(1)))
				Expect(qdiscs[0].(*netlink.Tbf).Limit).To(Equal(uint32(1)))
				return nil
			})).To(Succeed())

		})

		It("Should fail when container interface has no veth peer", func() {
			conf := `{
	"cniVersion": "0.4.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 8,
	"ingressBurst": 8,
	"egressRate": 16,
	"egressBurst": 8,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			// create a macvlan device to be container interface
			macvlanContainerIfname := "container-macv"
			createMacvlan(containerNs.Path(), containerIfname, macvlanContainerIfname)

			conf = fmt.Sprintf(conf, hostIfname, macvlanContainerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      macvlanContainerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, _, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).To(HaveOccurred())

				return nil
			})).To(Succeed())
		})

		It("Should fail when preResult has no interfaces", func() {
			conf := `{
	"cniVersion": "0.4.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 8,
	"ingressBurst": 8,
	"egressRate": 16,
	"egressBurst": 8,
	"prevResult": {
		"interfaces": [],
		"ips": [],
		"routes": []
	}
}`

			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      "eth0",
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, _, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).To(HaveOccurred())

				return nil
			})).To(Succeed())
		})

		It("Should fail when veth peer of container interface does not match any of host interfaces in preResult", func() {
			conf := `{
	"cniVersion": "0.4.0",
	"name": "cni-plugin-bandwidth-test",
	"type": "bandwidth",
	"ingressRate": 8,
	"ingressBurst": 8,
	"egressRate": 16,
	"egressBurst": 8,
	"prevResult": {
		"interfaces": [
			{
				"name": "%s",
				"sandbox": ""
			},
			{
				"name": "%s",
				"sandbox": "%s"
			}
		],
		"ips": [
			{
				"version": "4",
				"address": "%s/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		],
		"routes": []
	}
}`

			// fake a non-exist host interface name
			fakeHostIfname := fmt.Sprintf("%s-fake", hostIfname)

			conf = fmt.Sprintf(conf, fakeHostIfname, containerIfname, containerNs.Path(), containerIP.String())
			args := &skel.CmdArgs{
				ContainerID: "dummy",
				Netns:       containerNs.Path(),
				IfName:      containerIfname,
				StdinData:   []byte(conf),
			}

			Expect(hostNs.Do(func(netNS ns.NetNS) error {
				defer GinkgoRecover()

				_, _, err := testutils.CmdAdd(containerNs.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).To(HaveOccurred())

				return nil
			})).To(Succeed())
		})
	})

	Context("when chaining bandwidth plugin with PTP using 0.3.0 config", func() {
		var ptpConf string
		var rateInBits int
		var burstInBits int
		var packetInBytes int
		var containerWithoutTbfNS ns.NetNS
		var containerWithTbfNS ns.NetNS
		var portServerWithTbf int
		var portServerWithoutTbf int

		var containerWithTbfRes types.Result
		var containerWithoutTbfRes types.Result
		var echoServerWithTbf *gexec.Session
		var echoServerWithoutTbf *gexec.Session

		BeforeEach(func() {
			rateInBytes := 1000
			rateInBits = rateInBytes * 8
			burstInBits = rateInBits * 2
			packetInBytes = rateInBytes * 25

			ptpConf = `{
    "cniVersion": "0.3.0",
    "name": "mynet",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 512,
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`

			containerWithTbfIFName := "ptp0"
			containerWithoutTbfIFName := "ptp1"

			var err error
			containerWithTbfNS, err = testutils.NewNS()
			Expect(err).NotTo(HaveOccurred())

			containerWithoutTbfNS, err = testutils.NewNS()
			Expect(err).NotTo(HaveOccurred())

			By("create two containers, and use the bandwidth plugin on one of them")
			Expect(hostNs.Do(func(ns.NetNS) error {
				defer GinkgoRecover()

				containerWithTbfRes, _, err = testutils.CmdAdd(containerWithTbfNS.Path(), "dummy", containerWithTbfIFName, []byte(ptpConf), func() error {
					r, err := invoke.DelegateAdd(context.TODO(), "ptp", []byte(ptpConf), nil)
					Expect(r.Print()).To(Succeed())

					return err
				})
				Expect(err).NotTo(HaveOccurred())

				containerWithoutTbfRes, _, err = testutils.CmdAdd(containerWithoutTbfNS.Path(), "dummy2", containerWithoutTbfIFName, []byte(ptpConf), func() error {
					r, err := invoke.DelegateAdd(context.TODO(), "ptp", []byte(ptpConf), nil)
					Expect(r.Print()).To(Succeed())

					return err
				})
				Expect(err).NotTo(HaveOccurred())

				containerWithTbfResult, err := current.GetResult(containerWithTbfRes)
				Expect(err).NotTo(HaveOccurred())
				tbfPluginConf := PluginConf{}
				tbfPluginConf.RuntimeConfig.Bandwidth = &BandwidthEntry{
					IngressBurst: burstInBits,
					IngressRate:  rateInBits,
					EgressBurst:  burstInBits,
					EgressRate:   rateInBits,
				}
				tbfPluginConf.Name = "mynet"
				tbfPluginConf.CNIVersion = "0.3.0"
				tbfPluginConf.Type = "bandwidth"
				tbfPluginConf.RawPrevResult = map[string]interface{}{
					"ips":        containerWithTbfResult.IPs,
					"interfaces": containerWithTbfResult.Interfaces,
				}

				tbfPluginConf.PrevResult = &current.Result{
					IPs:        containerWithTbfResult.IPs,
					Interfaces: containerWithTbfResult.Interfaces,
				}
				conf, err := json.Marshal(tbfPluginConf)
				Expect(err).NotTo(HaveOccurred())

				args := &skel.CmdArgs{
					ContainerID: "dummy3",
					Netns:       containerWithTbfNS.Path(),
					IfName:      containerWithTbfIFName,
					StdinData:   []byte(conf),
				}

				_, out, err := testutils.CmdAdd(containerWithTbfNS.Path(), args.ContainerID, "", []byte(conf), func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))

				return nil
			})).To(Succeed())

			By("starting a tcp server on both containers")
			portServerWithTbf, echoServerWithTbf, err = startEchoServerInNamespace(containerWithTbfNS)
			Expect(err).NotTo(HaveOccurred())
			portServerWithoutTbf, echoServerWithoutTbf, err = startEchoServerInNamespace(containerWithoutTbfNS)
			Expect(err).NotTo(HaveOccurred())
		})

		AfterEach(func() {
			containerWithTbfNS.Close()
			containerWithoutTbfNS.Close()
			if echoServerWithoutTbf != nil {
				echoServerWithoutTbf.Kill()
			}
			if echoServerWithTbf != nil {
				echoServerWithTbf.Kill()
			}
		})

		Measure("limits ingress traffic on veth device", func(b Benchmarker) {
			var runtimeWithLimit time.Duration
			var runtimeWithoutLimit time.Duration

			By("gather timing statistics about both containers")
			By("sending tcp traffic to the container that has traffic shaped", func() {
				runtimeWithLimit = b.Time("with tbf", func() {
					result, err := current.GetResult(containerWithTbfRes)
					Expect(err).NotTo(HaveOccurred())

					makeTcpClientInNS(hostNs.Path(), result.IPs[0].Address.IP.String(), portServerWithTbf, packetInBytes)
				})
			})

			By("sending tcp traffic to the container that does not have traffic shaped", func() {
				runtimeWithoutLimit = b.Time("without tbf", func() {
					result, err := current.GetResult(containerWithoutTbfRes)
					Expect(err).NotTo(HaveOccurred())

					makeTcpClientInNS(hostNs.Path(), result.IPs[0].Address.IP.String(), portServerWithoutTbf, packetInBytes)
				})
			})

			Expect(runtimeWithLimit).To(BeNumerically(">", runtimeWithoutLimit+1000*time.Millisecond))
		}, 1)
	})

	Context("when chaining bandwidth plugin with PTP using 0.4.0 config", func() {
		var ptpConf string
		var rateInBits int
		var burstInBits int
		var packetInBytes int
		var containerWithoutTbfNS ns.NetNS
		var containerWithTbfNS ns.NetNS
		var portServerWithTbf int
		var portServerWithoutTbf int

		var containerWithTbfRes types.Result
		var containerWithoutTbfRes types.Result
		var echoServerWithTbf *gexec.Session
		var echoServerWithoutTbf *gexec.Session

		BeforeEach(func() {
			rateInBytes := 1000
			rateInBits = rateInBytes * 8
			burstInBits = rateInBits * 2
			packetInBytes = rateInBytes * 25

			ptpConf = `{
    "cniVersion": "0.4.0",
    "name": "myBWnet",
    "type": "ptp",
    "ipMasq": true,
    "mtu": 512,
    "ipam": {
        "type": "host-local",
        "subnet": "10.1.2.0/24"
    }
}`

			containerWithTbfIFName := "ptp0"
			containerWithoutTbfIFName := "ptp1"

			var err error
			containerWithTbfNS, err = testutils.NewNS()
			Expect(err).NotTo(HaveOccurred())

			containerWithoutTbfNS, err = testutils.NewNS()
			Expect(err).NotTo(HaveOccurred())

			By("create two containers, and use the bandwidth plugin on one of them")
			Expect(hostNs.Do(func(ns.NetNS) error {
				defer GinkgoRecover()

				containerWithTbfRes, _, err = testutils.CmdAdd(containerWithTbfNS.Path(), "dummy", containerWithTbfIFName, []byte(ptpConf), func() error {
					r, err := invoke.DelegateAdd(context.TODO(), "ptp", []byte(ptpConf), nil)
					Expect(r.Print()).To(Succeed())

					return err
				})
				Expect(err).NotTo(HaveOccurred())

				containerWithoutTbfRes, _, err = testutils.CmdAdd(containerWithoutTbfNS.Path(), "dummy2", containerWithoutTbfIFName, []byte(ptpConf), func() error {
					r, err := invoke.DelegateAdd(context.TODO(), "ptp", []byte(ptpConf), nil)
					Expect(r.Print()).To(Succeed())

					return err
				})
				Expect(err).NotTo(HaveOccurred())

				containerWithTbfResult, err := current.GetResult(containerWithTbfRes)
				Expect(err).NotTo(HaveOccurred())

				tbfPluginConf := &PluginConf{}
				err = json.Unmarshal([]byte(ptpConf), &tbfPluginConf)
				Expect(err).NotTo(HaveOccurred())

				tbfPluginConf.RuntimeConfig.Bandwidth = &BandwidthEntry{
					IngressBurst: burstInBits,
					IngressRate:  rateInBits,
					EgressBurst:  burstInBits,
					EgressRate:   rateInBits,
				}
				tbfPluginConf.Type = "bandwidth"
				cniVersion := "0.4.0"
				_, newConfBytes, err := buildOneConfig("myBWnet", cniVersion, tbfPluginConf, containerWithTbfResult)
				Expect(err).NotTo(HaveOccurred())

				args := &skel.CmdArgs{
					ContainerID: "dummy3",
					Netns:       containerWithTbfNS.Path(),
					IfName:      containerWithTbfIFName,
					StdinData:   newConfBytes,
				}

				result, out, err := testutils.CmdAdd(containerWithTbfNS.Path(), args.ContainerID, "", newConfBytes, func() error { return cmdAdd(args) })
				Expect(err).NotTo(HaveOccurred(), string(out))

				// Do CNI Check
				checkConf := &PluginConf{}
				err = json.Unmarshal([]byte(ptpConf), &checkConf)
				Expect(err).NotTo(HaveOccurred())

				checkConf.RuntimeConfig.Bandwidth = &BandwidthEntry{
					IngressBurst: burstInBits,
					IngressRate:  rateInBits,
					EgressBurst:  burstInBits,
					EgressRate:   rateInBits,
				}
				checkConf.Type = "bandwidth"

				_, newCheckBytes, err := buildOneConfig("myBWnet", cniVersion, checkConf, result)
				Expect(err).NotTo(HaveOccurred())

				args = &skel.CmdArgs{
					ContainerID: "dummy3",
					Netns:       containerWithTbfNS.Path(),
					IfName:      containerWithTbfIFName,
					StdinData:   newCheckBytes,
				}

				err = testutils.CmdCheck(containerWithTbfNS.Path(), args.ContainerID, "", newCheckBytes, func() error { return cmdCheck(args) })
				Expect(err).NotTo(HaveOccurred())

				return nil
			})).To(Succeed())

			By("starting a tcp server on both containers")
			portServerWithTbf, echoServerWithTbf, err = startEchoServerInNamespace(containerWithTbfNS)
			Expect(err).NotTo(HaveOccurred())
			portServerWithoutTbf, echoServerWithoutTbf, err = startEchoServerInNamespace(containerWithoutTbfNS)
			Expect(err).NotTo(HaveOccurred())
		})

		AfterEach(func() {
			containerWithTbfNS.Close()
			containerWithoutTbfNS.Close()
			if echoServerWithoutTbf != nil {
				echoServerWithoutTbf.Kill()
			}
			if echoServerWithTbf != nil {
				echoServerWithTbf.Kill()
			}
		})

		Measure("limits ingress traffic on veth device", func(b Benchmarker) {
			var runtimeWithLimit time.Duration
			var runtimeWithoutLimit time.Duration

			By("gather timing statistics about both containers")
			By("sending tcp traffic to the container that has traffic shaped", func() {
				runtimeWithLimit = b.Time("with tbf", func() {
					result, err := current.GetResult(containerWithTbfRes)
					Expect(err).NotTo(HaveOccurred())

					makeTcpClientInNS(hostNs.Path(), result.IPs[0].Address.IP.String(), portServerWithTbf, packetInBytes)
				})
			})

			By("sending tcp traffic to the container that does not have traffic shaped", func() {
				runtimeWithoutLimit = b.Time("without tbf", func() {
					result, err := current.GetResult(containerWithoutTbfRes)
					Expect(err).NotTo(HaveOccurred())

					makeTcpClientInNS(hostNs.Path(), result.IPs[0].Address.IP.String(), portServerWithoutTbf, packetInBytes)
				})
			})

			Expect(runtimeWithLimit).To(BeNumerically(">", runtimeWithoutLimit+1000*time.Millisecond))
		}, 1)
	})

})
