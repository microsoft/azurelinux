// Copyright 2015-2018 CNI authors
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
	"os"
	"os/exec"
	"sync"
	"time"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/containernetworking/plugins/pkg/testutils"

	"github.com/vishvananda/netlink"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("DHCP Multiple Lease Operations", func() {
	var originalNS, targetNS ns.NetNS
	var dhcpServerStopCh chan bool
	var dhcpServerDone *sync.WaitGroup
	var clientCmd *exec.Cmd
	var socketPath string
	var tmpDir string
	var serverIP net.IPNet
	var err error

	BeforeEach(func() {
		dhcpServerStopCh, serverIP, socketPath, originalNS, targetNS, err = dhcpSetupOriginalNS()
		Expect(err).NotTo(HaveOccurred())

		// Move the container side to the container's NS
		err = targetNS.Do(func(_ ns.NetNS) error {
			defer GinkgoRecover()

			link, err := netlink.LinkByName(contVethName0)
			Expect(err).NotTo(HaveOccurred())
			err = netlink.LinkSetUp(link)
			Expect(err).NotTo(HaveOccurred())

			link1, err := netlink.LinkByName(contVethName1)
			Expect(err).NotTo(HaveOccurred())
			err = netlink.LinkSetUp(link1)
			Expect(err).NotTo(HaveOccurred())
			return nil
		})

		// Start the DHCP server
		dhcpServerDone, err = dhcpServerStart(originalNS, net.IPv4(192, 168, 1, 5), serverIP.IP, 2, dhcpServerStopCh)
		Expect(err).NotTo(HaveOccurred())

		// Start the DHCP client daemon
		dhcpPluginPath, err := exec.LookPath("dhcp")
		Expect(err).NotTo(HaveOccurred())
		clientCmd = exec.Command(dhcpPluginPath, "daemon", "-socketpath", socketPath)
		err = clientCmd.Start()
		Expect(err).NotTo(HaveOccurred())
		Expect(clientCmd.Process).NotTo(BeNil())

		// Wait up to 15 seconds for the client socket
		Eventually(func() bool {
			_, err := os.Stat(socketPath)
			return err == nil
		}, time.Second*15, time.Second/4).Should(BeTrue())
	})

	AfterEach(func() {
		dhcpServerStopCh <- true
		dhcpServerDone.Wait()
		clientCmd.Process.Kill()
		clientCmd.Wait()

		Expect(originalNS.Close()).To(Succeed())
		Expect(targetNS.Close()).To(Succeed())
		defer os.RemoveAll(tmpDir)
	})

	It("configures multiple links with multiple ADD/DEL", func() {
		conf := fmt.Sprintf(`{
	    "cniVersion": "0.3.1",
	    "name": "mynet",
	    "type": "bridge",
	    "bridge": "%s",
	    "ipam": {
	        "type": "dhcp",
		"daemonSocketPath": "%s"
	    }
	}`, hostBridgeName, socketPath)

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      contVethName0,
			StdinData:   []byte(conf),
		}

		var addResult *current.Result
		err := originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			r, _, err := testutils.CmdAddWithArgs(args, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			addResult, err = current.GetResult(r)
			Expect(err).NotTo(HaveOccurred())
			Expect(len(addResult.IPs)).To(Equal(1))
			Expect(addResult.IPs[0].Address.String()).To(Equal("192.168.1.5/24"))
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		args = &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      contVethName1,
			StdinData:   []byte(conf),
		}

		err = originalNS.Do(func(ns.NetNS) error {
			defer GinkgoRecover()

			r, _, err := testutils.CmdAddWithArgs(args, func() error {
				return cmdAdd(args)
			})
			Expect(err).NotTo(HaveOccurred())

			addResult, err = current.GetResult(r)
			Expect(err).NotTo(HaveOccurred())
			Expect(len(addResult.IPs)).To(Equal(1))
			Expect(addResult.IPs[0].Address.String()).To(Equal("192.168.1.6/24"))
			return nil
		})
		Expect(err).NotTo(HaveOccurred())

		args = &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      contVethName1,
			StdinData:   []byte(conf),
		}

		err = originalNS.Do(func(ns.NetNS) error {
			return testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
		})
		Expect(err).NotTo(HaveOccurred())

		args = &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNS.Path(),
			IfName:      contVethName0,
			StdinData:   []byte(conf),
		}

		err = originalNS.Do(func(ns.NetNS) error {
			return testutils.CmdDelWithArgs(args, func() error {
				return cmdDel(args)
			})
		})
		Expect(err).NotTo(HaveOccurred())
	})
})
