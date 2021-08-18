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
	"net"
	"strings"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/plugins/pkg/testutils"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("static Operations", func() {
	It("allocates and releases addresses with ADD/DEL", func() {
		const ifname string = "eth0"
		const nspath string = "/some/where"

		conf := `{
			"cniVersion": "0.3.1",
			"name": "mynet",
			"type": "ipvlan",
			"master": "foo0",
			"ipam": {
				"type": "static",
				"addresses": [ {
						"address": "10.10.0.1/24",
						"gateway": "10.10.0.254"
					},
					{
						"address": "3ffe:ffff:0:01ff::1/64",
						"gateway": "3ffe:ffff:0::1"
					}],
				"routes": [
					{ "dst": "0.0.0.0/0" },
					{ "dst": "192.168.0.0/16", "gw": "10.10.5.1" },
					{ "dst": "3ffe:ffff:0:01ff::1/64" }],
				"dns": {
					"nameservers" : ["8.8.8.8"],
					"domain": "example.com",
					"search": [ "example.com" ]
				}
			}
		}`

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       nspath,
			IfName:      ifname,
			StdinData:   []byte(conf),
		}

		// Allocate the IP
		r, raw, err := testutils.CmdAddWithArgs(args, func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(strings.Index(string(raw), "\"version\":")).Should(BeNumerically(">", 0))

		result, err := current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		// Gomega is cranky about slices with different caps
		Expect(*result.IPs[0]).To(Equal(
			current.IPConfig{
				Version: "4",
				Address: mustCIDR("10.10.0.1/24"),
				Gateway: net.ParseIP("10.10.0.254"),
			}))

		Expect(*result.IPs[1]).To(Equal(
			current.IPConfig{
				Version: "6",
				Address: mustCIDR("3ffe:ffff:0:01ff::1/64"),
				Gateway: net.ParseIP("3ffe:ffff:0::1"),
			},
		))
		Expect(len(result.IPs)).To(Equal(2))

		Expect(result.Routes).To(Equal([]*types.Route{
			{Dst: mustCIDR("0.0.0.0/0")},
			{Dst: mustCIDR("192.168.0.0/16"), GW: net.ParseIP("10.10.5.1")},
			{Dst: mustCIDR("3ffe:ffff:0:01ff::1/64")},
		}))

		// Release the IP
		err = testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("doesn't error when passed an unknown ID on DEL", func() {
		const ifname string = "eth0"
		const nspath string = "/some/where"

		conf := `{
			"cniVersion": "0.3.0",
			"name": "mynet",
			"type": "ipvlan",
			"master": "foo0",
			"ipam": {
				"type": "static",
				"addresses": [ {
					"address": "10.10.0.1/24",
					"gateway": "10.10.0.254"
				},
				{
					"address": "3ffe:ffff:0:01ff::1/64",
					"gateway": "3ffe:ffff:0::1"
				}],
				"routes": [
				{ "dst": "0.0.0.0/0" },
				{ "dst": "192.168.0.0/16", "gw": "10.10.5.1" },
				{ "dst": "3ffe:ffff:0:01ff::1/64" }],
				"dns": {
					"nameservers" : ["8.8.8.8"],
					"domain": "example.com",
					"search": [ "example.com" ]
				}}}`

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       nspath,
			IfName:      ifname,
			StdinData:   []byte(conf),
		}

		// Release the IP
		err := testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("allocates and releases addresses with ADD/DEL, with ENV variables", func() {
		const ifname string = "eth0"
		const nspath string = "/some/where"

		conf := `{
			"cniVersion": "0.3.1",
			"name": "mynet",
			"type": "ipvlan",
			"master": "foo0",
			"ipam": {
				"type": "static",
				"routes": [
					{ "dst": "0.0.0.0/0" },
					{ "dst": "192.168.0.0/16", "gw": "10.10.5.1" }],
				"dns": {
					"nameservers" : ["8.8.8.8"],
					"domain": "example.com",
					"search": [ "example.com" ]
				}
			}
		}`

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       nspath,
			IfName:      ifname,
			StdinData:   []byte(conf),
			Args:        "IP=10.10.0.1/24;GATEWAY=10.10.0.254",
		}

		// Allocate the IP
		r, raw, err := testutils.CmdAddWithArgs(args, func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(strings.Index(string(raw), "\"version\":")).Should(BeNumerically(">", 0))

		result, err := current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		// Gomega is cranky about slices with different caps
		Expect(*result.IPs[0]).To(Equal(
			current.IPConfig{
				Version: "4",
				Address: mustCIDR("10.10.0.1/24"),
				Gateway: net.ParseIP("10.10.0.254"),
			}))

		Expect(len(result.IPs)).To(Equal(1))

		Expect(result.Routes).To(Equal([]*types.Route{
			{Dst: mustCIDR("0.0.0.0/0")},
			{Dst: mustCIDR("192.168.0.0/16"), GW: net.ParseIP("10.10.5.1")},
		}))

		// Release the IP
		err = testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
	})

	It("allocates and releases multiple addresses with ADD/DEL, with ENV variables", func() {
		const ifname string = "eth0"
		const nspath string = "/some/where"

		conf := `{
			"cniVersion": "0.3.1",
			"name": "mynet",
			"type": "ipvlan",
			"master": "foo0",
			"ipam": {
				"type": "static"
			}
		}`

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       nspath,
			IfName:      ifname,
			StdinData:   []byte(conf),
			Args:        "IP=10.10.0.1/24,11.11.0.1/24;GATEWAY=10.10.0.254",
		}

		// Allocate the IP
		r, raw, err := testutils.CmdAddWithArgs(args, func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(strings.Index(string(raw), "\"version\":")).Should(BeNumerically(">", 0))

		result, err := current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		// Gomega is cranky about slices with different caps
		Expect(*result.IPs[0]).To(Equal(
			current.IPConfig{
				Version: "4",
				Address: mustCIDR("10.10.0.1/24"),
				Gateway: net.ParseIP("10.10.0.254"),
			}))
		Expect(*result.IPs[1]).To(Equal(
			current.IPConfig{
				Version: "4",
				Address: mustCIDR("11.11.0.1/24"),
				Gateway: nil,
			}))

		Expect(len(result.IPs)).To(Equal(2))

		// Release the IP
		err = testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
	})
})

func mustCIDR(s string) net.IPNet {
	ip, n, err := net.ParseCIDR(s)
	n.IP = ip
	if err != nil {
		Fail(err.Error())
	}

	return *n
}
