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
	"strings"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"
	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/containernetworking/plugins/pkg/testutils"

	"github.com/vishvananda/netlink"

	"github.com/coreos/go-iptables/iptables"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func findChains(chains []string) (bool, bool) {
	var foundAdmin, foundPriv bool
	for _, ch := range chains {
		if ch == "CNI-ADMIN" {
			foundAdmin = true
		} else if ch == "CNI-FORWARD" {
			foundPriv = true
		}
	}
	return foundAdmin, foundPriv
}

func findForwardJumpRules(rules []string) (bool, bool) {
	var foundAdmin, foundPriv bool
	for _, rule := range rules {
		if strings.Contains(rule, "-j CNI-ADMIN") {
			foundAdmin = true
		} else if strings.Contains(rule, "-j CNI-FORWARD") {
			foundPriv = true
		}
	}
	return foundAdmin, foundPriv
}

func findForwardAllowRules(rules []string, ip string) (bool, bool) {
	var foundOne, foundTwo bool
	for _, rule := range rules {
		if !strings.HasSuffix(rule, "-j ACCEPT") {
			continue
		}
		if strings.Contains(rule, fmt.Sprintf(" -s %s ", ip)) {
			foundOne = true
		} else if strings.Contains(rule, fmt.Sprintf(" -d %s ", ip)) && strings.Contains(rule, "RELATED,ESTABLISHED") {
			foundTwo = true
		}
	}
	return foundOne, foundTwo
}

func getPrevResult(bytes []byte) *current.Result {
	type TmpConf struct {
		types.NetConf
		RawPrevResult map[string]interface{} `json:"prevResult,omitempty"`
		PrevResult    *current.Result        `json:"-"`
	}

	conf := &TmpConf{}
	err := json.Unmarshal(bytes, conf)
	Expect(err).NotTo(HaveOccurred())
	if conf.RawPrevResult == nil {
		return nil
	}

	resultBytes, err := json.Marshal(conf.RawPrevResult)
	Expect(err).NotTo(HaveOccurred())
	res, err := version.NewResult(conf.CNIVersion, resultBytes)
	Expect(err).NotTo(HaveOccurred())
	prevResult, err := current.NewResultFromResult(res)
	Expect(err).NotTo(HaveOccurred())

	return prevResult
}

func validateFullRuleset(bytes []byte) {
	prevResult := getPrevResult(bytes)

	for _, ip := range prevResult.IPs {
		ipt, err := iptables.NewWithProtocol(protoForIP(ip.Address))
		Expect(err).NotTo(HaveOccurred())

		// Ensure chains
		chains, err := ipt.ListChains("filter")
		Expect(err).NotTo(HaveOccurred())
		foundAdmin, foundPriv := findChains(chains)
		Expect(foundAdmin).To(Equal(true))
		Expect(foundPriv).To(Equal(true))

		// Look for the FORWARD chain jump rules to our custom chains
		rules, err := ipt.List("filter", "FORWARD")
		Expect(err).NotTo(HaveOccurred())
		Expect(len(rules)).Should(BeNumerically(">", 1))
		_, foundPriv = findForwardJumpRules(rules)
		Expect(foundPriv).To(Equal(true))

		// Look for the allow rules in our custom FORWARD chain
		rules, err = ipt.List("filter", "CNI-FORWARD")
		Expect(err).NotTo(HaveOccurred())
		Expect(len(rules)).Should(BeNumerically(">", 1))
		foundAdmin, _ = findForwardJumpRules(rules)
		Expect(foundAdmin).To(Equal(true))

		// Look for the IP allow rules
		foundOne, foundTwo := findForwardAllowRules(rules, ipString(ip.Address))
		Expect(foundOne).To(Equal(true))
		Expect(foundTwo).To(Equal(true))
	}
}

func validateCleanedUp(bytes []byte) {
	prevResult := getPrevResult(bytes)

	for _, ip := range prevResult.IPs {
		ipt, err := iptables.NewWithProtocol(protoForIP(ip.Address))
		Expect(err).NotTo(HaveOccurred())

		// Our private and admin chains don't get cleaned up
		chains, err := ipt.ListChains("filter")
		Expect(err).NotTo(HaveOccurred())
		foundAdmin, foundPriv := findChains(chains)
		Expect(foundAdmin).To(Equal(true))
		Expect(foundPriv).To(Equal(true))

		// Look for the FORWARD chain jump rules to our custom chains
		rules, err := ipt.List("filter", "FORWARD")
		Expect(err).NotTo(HaveOccurred())
		_, foundPriv = findForwardJumpRules(rules)
		Expect(foundPriv).To(Equal(true))

		// Look for the allow rules in our custom FORWARD chain
		rules, err = ipt.List("filter", "CNI-FORWARD")
		Expect(err).NotTo(HaveOccurred())
		foundAdmin, _ = findForwardJumpRules(rules)
		Expect(foundAdmin).To(Equal(true))

		// Expect no IP address rules for this IP
		foundOne, foundTwo := findForwardAllowRules(rules, ipString(ip.Address))
		Expect(foundOne).To(Equal(false))
		Expect(foundTwo).To(Equal(false))
	}
}

var _ = Describe("firewall plugin iptables backend", func() {
	var originalNS, targetNS ns.NetNS
	const IFNAME string = "dummy0"

	fullConf := []byte(`{
		"name": "test",
		"type": "firewall",
		"backend": "iptables",
		"ifName": "dummy0",
		"cniVersion": "0.3.1",
		"prevResult": {
			"interfaces": [
				{"name": "dummy0"}
			],
			"ips": [
				{
					"version": "4",
					"address": "10.0.0.2/24",
					"interface": 0
				},
				{
					"version": "6",
					"address": "2001:db8:1:2::1/64",
					"interface": 0
				}
			]
		}
	}`)

	BeforeEach(func() {
		// Create a new NetNS so we don't modify the host
		var err error
		originalNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			err = netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: IFNAME,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			_, err = netlink.LinkByName(IFNAME)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		targetNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
	})

	AfterEach(func() {
		Expect(originalNS.Close()).To(Succeed())
		Expect(targetNS.Close()).To(Succeed())
	})

	It("passes prevResult through unchanged", func() {
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   fullConf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			r, _, err := testutils.CmdAdd(targetNS.Path(), args.ContainerID, IFNAME, fullConf, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			result, err := current.GetResult(r)
			Expect(err).NotTo(HaveOccurred())

			Expect(len(result.Interfaces)).To(Equal(1))
			Expect(result.Interfaces[0].Name).To(Equal(IFNAME))
			Expect(len(result.IPs)).To(Equal(2))
			Expect(result.IPs[0].Address.String()).To(Equal("10.0.0.2/24"))
			Expect(result.IPs[1].Address.String()).To(Equal("2001:db8:1:2::1/64"))
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("installs the right iptables rules on the host", func() {
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   fullConf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			_, _, err := testutils.CmdAdd(targetNS.Path(), args.ContainerID, IFNAME, fullConf, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			validateFullRuleset(fullConf)
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("correctly handles a custom IptablesAdminChainName", func() {
		conf := []byte(`{
	"name": "test",
	"type": "firewall",
	"backend": "iptables",
	"ifName": "dummy0",
	"cniVersion": "0.3.1",
	"iptablesAdminChainName": "CNI-foobar",
	"prevResult": {
		"interfaces": [
			{"name": "dummy0"}
		],
		"ips": [
			{
				"version": "4",
				"address": "10.0.0.2/24",
				"interface": 0
			},
			{
				"version": "6",
				"address": "2001:db8:1:2::1/64",
				"interface": 0
			}
		]
	}
}`)

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   conf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			_, _, err := testutils.CmdAdd(targetNS.Path(), args.ContainerID, IFNAME, conf, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			var ipt *iptables.IPTables
			for _, proto := range []iptables.Protocol{iptables.ProtocolIPv4, iptables.ProtocolIPv6} {
				ipt, err = iptables.NewWithProtocol(proto)
				Expect(err).NotTo(HaveOccurred())

				// Ensure custom admin chain name
				chains, err := ipt.ListChains("filter")
				Expect(err).NotTo(HaveOccurred())
				var foundAdmin bool
				for _, ch := range chains {
					if ch == "CNI-foobar" {
						foundAdmin = true
					}
				}
				Expect(foundAdmin).To(Equal(true))
			}

			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("cleans up on delete", func() {
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   fullConf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			_, _, err := testutils.CmdAdd(targetNS.Path(), args.ContainerID, IFNAME, fullConf, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())
			validateFullRuleset(fullConf)

			err = testutils.CmdDel(targetNS.Path(), args.ContainerID, IFNAME, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			validateCleanedUp(fullConf)
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("installs the right iptables rules on the host v4.0.x and check is successful", func() {
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   fullConf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			_, _, err := testutils.CmdAdd(targetNS.Path(), args.ContainerID, IFNAME, fullConf, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			validateFullRuleset(fullConf)
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("cleans up on delete v4.0.x", func() {
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   fullConf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			_, _, err := testutils.CmdAdd(targetNS.Path(), args.ContainerID, IFNAME, fullConf, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())
			validateFullRuleset(fullConf)

			err = testutils.CmdDel(targetNS.Path(), args.ContainerID, IFNAME, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			validateCleanedUp(fullConf)
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})
})

var _ = Describe("firewall plugin iptables backend v0.4.x", func() {
	var originalNS, targetNS ns.NetNS
	const IFNAME string = "dummy0"

	fullConf := []byte(`{
		"name": "test",
		"type": "firewall",
		"backend": "iptables",
		"ifName": "dummy0",
		"cniVersion": "0.4.0",
		"prevResult": {
			"interfaces": [
				{"name": "dummy0"}
			],
			"ips": [
				{
					"version": "4",
					"address": "10.0.0.2/24",
					"interface": 0
				},
				{
					"version": "6",
					"address": "2001:db8:1:2::1/64",
					"interface": 0
				}
			]
		}
	}`)

	BeforeEach(func() {
		// Create a new NetNS so we don't modify the host
		var err error
		originalNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			err = netlink.LinkAdd(&netlink.Dummy{
				LinkAttrs: netlink.LinkAttrs{
					Name: IFNAME,
				},
			})
			Expect(err).NotTo(HaveOccurred())
			_, err = netlink.LinkByName(IFNAME)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		targetNS, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())
	})

	AfterEach(func() {
		Expect(originalNS.Close()).To(Succeed())
		Expect(targetNS.Close()).To(Succeed())
	})

	It("installs iptables rules, Check rules then cleans up on delete using v4.0.x", func() {
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      IFNAME,
			StdinData:   fullConf,
		}

		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			r, _, err := testutils.CmdAddWithArgs(args, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			_, err = current.GetResult(r)
			Expect(err).NotTo(HaveOccurred())

			err = testutils.CmdCheckWithArgs(args, func() error {
				return cmdCheck(args)
			})
			Expect(err).NotTo(HaveOccurred())
			validateFullRuleset(fullConf)

			err = testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
			Expect(err).NotTo(HaveOccurred())
			validateCleanedUp(fullConf)
			return nil
		})
		Expect(err).NotTo(HaveOccurred())
	})
})
