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
	"fmt"
	"net"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("portmapping configuration", func() {
	netName := "testNetName"
	containerID := "icee6giejonei6sohng6ahngee7laquohquee9shiGo7fohferakah3Feiyoolu2pei7ciPhoh7shaoX6vai3vuf0ahfaeng8yohb9ceu0daez5hashee8ooYai5wa3y"

	Context("config parsing", func() {
		It("Correctly parses an ADD config", func() {
			configBytes := []byte(`{
	"name": "test",
	"type": "portmap",
	"cniVersion": "0.3.1",
	"runtimeConfig": {
		"portMappings": [
			{ "hostPort": 8080, "containerPort": 80, "protocol": "tcp"},
			{ "hostPort": 8081, "containerPort": 81, "protocol": "udp"}
		]
	},
	"snat": false,
	"conditionsV4": ["a", "b"],
	"conditionsV6": ["c", "d"],
	"prevResult": {
		"interfaces": [
			{"name": "host"},
			{"name": "container", "sandbox":"netns"}
		],
		"ips": [
			{
				"version": "4",
				"address": "10.0.0.1/24",
				"gateway": "10.0.0.1",
				"interface": 0
			},
			{
				"version": "6",
				"address": "2001:db8:1::2/64",
				"gateway": "2001:db8:1::1",
				"interface": 1
			},
			{
				"version": "4",
				"address": "10.0.0.2/24",
				"gateway": "10.0.0.1",
				"interface": 1
			}
		]
	}
}`)
			c, _, err := parseConfig(configBytes, "container")
			Expect(err).NotTo(HaveOccurred())
			Expect(c.CNIVersion).To(Equal("0.3.1"))
			Expect(c.ConditionsV4).To(Equal(&[]string{"a", "b"}))
			Expect(c.ConditionsV6).To(Equal(&[]string{"c", "d"}))
			fvar := false
			Expect(c.SNAT).To(Equal(&fvar))
			Expect(c.Name).To(Equal("test"))

			Expect(c.ContIPv4).To(Equal(net.ParseIP("10.0.0.2")))
			Expect(c.ContIPv6).To(Equal(net.ParseIP("2001:db8:1::2")))
		})

		It("Correctly parses a DEL config", func() {
			// When called with DEL, neither runtimeConfig nor prevResult may be specified
			configBytes := []byte(`{
	"name": "test",
	"type": "portmap",
	"cniVersion": "0.3.1",
	"snat": false,
	"conditionsV4": ["a", "b"],
	"conditionsV6": ["c", "d"]
}`)
			c, _, err := parseConfig(configBytes, "container")
			Expect(err).NotTo(HaveOccurred())
			Expect(c.CNIVersion).To(Equal("0.3.1"))
			Expect(c.ConditionsV4).To(Equal(&[]string{"a", "b"}))
			Expect(c.ConditionsV6).To(Equal(&[]string{"c", "d"}))
			fvar := false
			Expect(c.SNAT).To(Equal(&fvar))
			Expect(c.Name).To(Equal("test"))
		})

		It("fails with invalid mappings", func() {
			configBytes := []byte(`{
	"name": "test",
	"type": "portmap",
	"cniVersion": "0.3.1",
	"snat": false,
	"conditionsV4": ["a", "b"],
	"conditionsV6": ["c", "d"],
	"runtimeConfig": {
		"portMappings": [
			{ "hostPort": 0, "containerPort": 80, "protocol": "tcp"}
		]
	}
}`)
			_, _, err := parseConfig(configBytes, "container")
			Expect(err).To(MatchError("Invalid host port number: 0"))
		})

		It("Does not fail on missing prevResult interface index", func() {
			configBytes := []byte(`{
	"name": "test",
	"type": "portmap",
	"cniVersion": "0.3.1",
	"runtimeConfig": {
		"portMappings": [
			{ "hostPort": 8080, "containerPort": 80, "protocol": "tcp"}
		]
	},
	"conditionsV4": ["a", "b"],
	"prevResult": {
		"interfaces": [
			{"name": "host"}
		],
		"ips": [
			{
				"version": "4",
				"address": "10.0.0.1/24",
				"gateway": "10.0.0.1"
			}
		]
	}
}`)
			_, _, err := parseConfig(configBytes, "container")
			Expect(err).NotTo(HaveOccurred())
		})
	})

	Describe("Generating chains", func() {
		Context("for DNAT", func() {
			It("generates a correct standard container chain", func() {
				ch := genDnatChain(netName, containerID)

				Expect(ch).To(Equal(chain{
					table:       "nat",
					name:        "CNI-DN-bfd599665540dd91d5d28",
					entryChains: []string{TopLevelDNATChainName},
				}))
				configBytes := []byte(`{
	"name": "test",
	"type": "portmap",
	"cniVersion": "0.3.1",
	"runtimeConfig": {
		"portMappings": [
			{ "hostPort": 8080, "containerPort": 80, "protocol": "tcp"},
			{ "hostPort": 8081, "containerPort": 80, "protocol": "tcp"},
			{ "hostPort": 8080, "containerPort": 81, "protocol": "udp"},
			{ "hostPort": 8082, "containerPort": 82, "protocol": "udp"}
		]
	},
	"snat": true,
	"conditionsV4": ["a", "b"],
	"conditionsV6": ["c", "d"]
}`)

				conf, _, err := parseConfig(configBytes, "foo")
				Expect(err).NotTo(HaveOccurred())
				conf.ContainerID = containerID

				ch = genDnatChain(conf.Name, containerID)
				Expect(ch).To(Equal(chain{
					table:       "nat",
					name:        "CNI-DN-67e92b96e692a494b6b85",
					entryChains: []string{"CNI-HOSTPORT-DNAT"},
				}))

				fillDnatRules(&ch, conf, net.ParseIP("10.0.0.2"))

				Expect(ch.entryRules).To(Equal([][]string{
					{"-m", "comment", "--comment",
						fmt.Sprintf("dnat name: \"test\" id: \"%s\"", containerID),
						"-m", "multiport",
						"-p", "tcp",
						"--destination-ports", "8080,8081",
						"a", "b"},
					{"-m", "comment", "--comment",
						fmt.Sprintf("dnat name: \"test\" id: \"%s\"", containerID),
						"-m", "multiport",
						"-p", "udp",
						"--destination-ports", "8080,8082",
						"a", "b"},
				}))

				Expect(ch.rules).To(Equal([][]string{
					{"-p", "tcp", "--dport", "8080", "-s", "10.0.0.2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "tcp", "--dport", "8080", "-s", "127.0.0.1", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "tcp", "--dport", "8080", "-j", "DNAT", "--to-destination", "10.0.0.2:80"},
					{"-p", "tcp", "--dport", "8081", "-s", "10.0.0.2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "tcp", "--dport", "8081", "-s", "127.0.0.1", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "tcp", "--dport", "8081", "-j", "DNAT", "--to-destination", "10.0.0.2:80"},
					{"-p", "udp", "--dport", "8080", "-s", "10.0.0.2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "udp", "--dport", "8080", "-s", "127.0.0.1", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "udp", "--dport", "8080", "-j", "DNAT", "--to-destination", "10.0.0.2:81"},
					{"-p", "udp", "--dport", "8082", "-s", "10.0.0.2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "udp", "--dport", "8082", "-s", "127.0.0.1", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "udp", "--dport", "8082", "-j", "DNAT", "--to-destination", "10.0.0.2:82"},
				}))

				ch.rules = nil
				ch.entryRules = nil

				fillDnatRules(&ch, conf, net.ParseIP("2001:db8::2"))

				Expect(ch.rules).To(Equal([][]string{
					{"-p", "tcp", "--dport", "8080", "-s", "2001:db8::2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "tcp", "--dport", "8080", "-j", "DNAT", "--to-destination", "[2001:db8::2]:80"},
					{"-p", "tcp", "--dport", "8081", "-s", "2001:db8::2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "tcp", "--dport", "8081", "-j", "DNAT", "--to-destination", "[2001:db8::2]:80"},
					{"-p", "udp", "--dport", "8080", "-s", "2001:db8::2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "udp", "--dport", "8080", "-j", "DNAT", "--to-destination", "[2001:db8::2]:81"},
					{"-p", "udp", "--dport", "8082", "-s", "2001:db8::2", "-j", "CNI-HOSTPORT-SETMARK"},
					{"-p", "udp", "--dport", "8082", "-j", "DNAT", "--to-destination", "[2001:db8::2]:82"},
				}))

				// Disable snat, generate rules
				ch.rules = nil
				ch.entryRules = nil
				fvar := false
				conf.SNAT = &fvar

				fillDnatRules(&ch, conf, net.ParseIP("10.0.0.2"))
				Expect(ch.rules).To(Equal([][]string{
					{"-p", "tcp", "--dport", "8080", "-j", "DNAT", "--to-destination", "10.0.0.2:80"},
					{"-p", "tcp", "--dport", "8081", "-j", "DNAT", "--to-destination", "10.0.0.2:80"},
					{"-p", "udp", "--dport", "8080", "-j", "DNAT", "--to-destination", "10.0.0.2:81"},
					{"-p", "udp", "--dport", "8082", "-j", "DNAT", "--to-destination", "10.0.0.2:82"},
				}))
			})

			It("generates a correct chain with external mark", func() {
				ch := genDnatChain(netName, containerID)

				Expect(ch).To(Equal(chain{
					table:       "nat",
					name:        "CNI-DN-bfd599665540dd91d5d28",
					entryChains: []string{TopLevelDNATChainName},
				}))
				configBytes := []byte(`{
	"name": "test",
	"type": "portmap",
	"cniVersion": "0.3.1",
	"runtimeConfig": {
		"portMappings": [
			{ "hostPort": 8080, "containerPort": 80, "protocol": "tcp"}
		]
	},
	"externalSetMarkChain": "PLZ-SET-MARK",
	"conditionsV4": ["a", "b"],
	"conditionsV6": ["c", "d"]
}`)

				conf, _, err := parseConfig(configBytes, "foo")
				Expect(err).NotTo(HaveOccurred())
				conf.ContainerID = containerID

				ch = genDnatChain(conf.Name, containerID)
				fillDnatRules(&ch, conf, net.ParseIP("10.0.0.2"))
				Expect(ch.rules).To(Equal([][]string{
					{"-p", "tcp", "--dport", "8080", "-s", "10.0.0.2", "-j", "PLZ-SET-MARK"},
					{"-p", "tcp", "--dport", "8080", "-s", "127.0.0.1", "-j", "PLZ-SET-MARK"},
					{"-p", "tcp", "--dport", "8080", "-j", "DNAT", "--to-destination", "10.0.0.2:80"},
				}))
			})

			It("generates a correct top-level chain", func() {
				ch := genToplevelDnatChain()

				Expect(ch).To(Equal(chain{
					table:       "nat",
					name:        "CNI-HOSTPORT-DNAT",
					entryChains: []string{"PREROUTING", "OUTPUT"},
					entryRules:  [][]string{{"-m", "addrtype", "--dst-type", "LOCAL"}},
				}))
			})

			It("generates the correct mark chains", func() {
				masqBit := 5
				ch := genSetMarkChain(masqBit)
				Expect(ch).To(Equal(chain{
					table: "nat",
					name:  "CNI-HOSTPORT-SETMARK",
					rules: [][]string{{
						"-m", "comment",
						"--comment", "CNI portfwd masquerade mark",
						"-j", "MARK",
						"--set-xmark", "0x20/0x20",
					}},
				}))

				ch = genMarkMasqChain(masqBit)
				Expect(ch).To(Equal(chain{
					table:       "nat",
					name:        "CNI-HOSTPORT-MASQ",
					entryChains: []string{"POSTROUTING"},
					entryRules: [][]string{{
						"-m", "comment",
						"--comment", "CNI portfwd requiring masquerade",
					}},
					rules: [][]string{{
						"-m", "mark",
						"--mark", "0x20/0x20",
						"-j", "MASQUERADE",
					}},
					prependEntry: true,
				}))
			})
		})
	})
})
