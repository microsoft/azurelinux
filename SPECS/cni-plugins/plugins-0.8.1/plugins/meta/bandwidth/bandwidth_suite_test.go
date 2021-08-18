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
	"bytes"
	"fmt"
	"io"
	"net"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"testing"

	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/onsi/gomega/gbytes"
	"github.com/onsi/gomega/gexec"

	"github.com/vishvananda/netlink"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func TestTBF(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "plugins/meta/bandwidth")
}

var echoServerBinaryPath string

var _ = SynchronizedBeforeSuite(func() []byte {
	binaryPath, err := gexec.Build("github.com/containernetworking/plugins/pkg/testutils/echosvr")
	Expect(err).NotTo(HaveOccurred())
	return []byte(binaryPath)
}, func(data []byte) {
	echoServerBinaryPath = string(data)
})

var _ = SynchronizedAfterSuite(func() {}, func() {
	gexec.CleanupBuildArtifacts()
})

func startInNetNS(binPath string, netNS ns.NetNS) (*gexec.Session, error) {
	baseName := filepath.Base(netNS.Path())
	// we are relying on the netNS path living in /var/run/netns
	// where `ip netns exec` can find it
	cmd := exec.Command("ip", "netns", "exec", baseName, binPath)

	session, err := gexec.Start(cmd, GinkgoWriter, GinkgoWriter)
	return session, err
}

func startEchoServerInNamespace(netNS ns.NetNS) (int, *gexec.Session, error) {
	session, err := startInNetNS(echoServerBinaryPath, netNS)
	Expect(err).NotTo(HaveOccurred())

	// wait for it to print it's address on stdout
	Eventually(session.Out).Should(gbytes.Say("\n"))
	_, portString, err := net.SplitHostPort(strings.TrimSpace(string(session.Out.Contents())))
	Expect(err).NotTo(HaveOccurred())

	port, err := strconv.Atoi(portString)
	Expect(err).NotTo(HaveOccurred())

	go func() {
		// print out echoserver output to ginkgo to capture any errors that might be occurring.
		io.Copy(GinkgoWriter, io.MultiReader(session.Out, session.Err))
	}()

	return port, session, nil
}

func makeTcpClientInNS(netns string, address string, port int, numBytes int) {
	message := bytes.Repeat([]byte{'a'}, numBytes)

	bin, err := exec.LookPath("nc")
	Expect(err).NotTo(HaveOccurred())
	var cmd *exec.Cmd
	if netns != "" {
		netns = filepath.Base(netns)
		cmd = exec.Command("ip", "netns", "exec", netns, bin, "-v", address, strconv.Itoa(port))
	} else {
		cmd = exec.Command("nc", address, strconv.Itoa(port))
	}
	cmd.Stdin = bytes.NewBuffer([]byte(message))
	cmd.Stderr = GinkgoWriter
	out, err := cmd.Output()

	Expect(err).NotTo(HaveOccurred())
	Expect(string(out)).To(Equal(string(message)))
}

func createVeth(hostNamespace string, hostVethIfName string, containerNamespace string, containerVethIfName string, hostIP []byte, containerIP []byte, hostIfaceMTU int) {
	vethDeviceRequest := &netlink.Veth{
		LinkAttrs: netlink.LinkAttrs{
			Name:  hostVethIfName,
			Flags: net.FlagUp,
			MTU:   hostIfaceMTU,
		},
		PeerName: containerVethIfName,
	}

	hostNs, err := ns.GetNS(hostNamespace)
	Expect(err).NotTo(HaveOccurred())

	err = hostNs.Do(func(_ ns.NetNS) error {
		if err := netlink.LinkAdd(vethDeviceRequest); err != nil {
			return fmt.Errorf("creating veth pair: %s", err)
		}

		containerVeth, err := netlink.LinkByName(containerVethIfName)
		if err != nil {
			return fmt.Errorf("failed to find newly-created veth device %q: %v", containerVethIfName, err)
		}

		containerNs, err := ns.GetNS(containerNamespace)
		if err != nil {
			return err
		}

		err = netlink.LinkSetNsFd(containerVeth, int(containerNs.Fd()))
		if err != nil {
			return fmt.Errorf("failed to move veth to container namespace: %s", err)
		}

		localAddr := &net.IPNet{
			IP:   hostIP,
			Mask: []byte{255, 255, 255, 255},
		}
		peerAddr := &net.IPNet{
			IP:   containerIP,
			Mask: []byte{255, 255, 255, 255},
		}
		addr, err := netlink.ParseAddr(localAddr.String())
		if err != nil {
			return fmt.Errorf("parsing address %s: %s", localAddr, err)
		}

		addr.Peer = peerAddr

		addr.Scope = int(netlink.SCOPE_LINK)
		hostVeth, err := netlink.LinkByName(hostVethIfName)
		if err != nil {
			return fmt.Errorf("failed to find newly-created veth device %q: %v", containerVethIfName, err)
		}

		err = netlink.AddrAdd(hostVeth, addr)
		if err != nil {
			return fmt.Errorf("adding IP address %s: %s", localAddr, err)
		}

		return nil
	})
	Expect(err).NotTo(HaveOccurred())

	containerNs, err := ns.GetNS(containerNamespace)
	Expect(err).NotTo(HaveOccurred())
	err = containerNs.Do(func(_ ns.NetNS) error {
		peerAddr := &net.IPNet{
			IP:   hostIP,
			Mask: []byte{255, 255, 255, 255},
		}
		localAddr := &net.IPNet{
			IP:   containerIP,
			Mask: []byte{255, 255, 255, 255},
		}
		addr, err := netlink.ParseAddr(localAddr.String())
		if err != nil {
			return fmt.Errorf("parsing address %s: %s", localAddr, err)
		}

		addr.Peer = peerAddr

		addr.Scope = int(netlink.SCOPE_LINK)
		containerVeth, err := netlink.LinkByName(containerVethIfName)
		if err != nil {
			return fmt.Errorf("failed to find newly-created veth device %q: %v", containerVethIfName, err)
		}
		err = netlink.AddrAdd(containerVeth, addr)
		if err != nil {
			return fmt.Errorf("adding IP address %s: %s", localAddr, err)
		}

		return nil
	})

	Expect(err).NotTo(HaveOccurred())
}

func createVethInOneNs(namespace, vethName, peerName string) {
	vethDeviceRequest := &netlink.Veth{
		LinkAttrs: netlink.LinkAttrs{
			Name:  vethName,
			Flags: net.FlagUp,
		},
		PeerName: peerName,
	}

	netNS, err := ns.GetNS(namespace)
	Expect(err).NotTo(HaveOccurred())

	err = netNS.Do(func(_ ns.NetNS) error {
		if err := netlink.LinkAdd(vethDeviceRequest); err != nil {
			return fmt.Errorf("failed to create veth pair: %v", err)
		}

		_, err := netlink.LinkByName(peerName)
		if err != nil {
			return fmt.Errorf("failed to find newly-created veth device %q: %v", peerName, err)
		}
		return nil
	})
	Expect(err).NotTo(HaveOccurred())
}

func createMacvlan(namespace, master, macvlanName string) {
	netNS, err := ns.GetNS(namespace)
	Expect(err).NotTo(HaveOccurred())

	err = netNS.Do(func(_ ns.NetNS) error {
		m, err := netlink.LinkByName(master)
		if err != nil {
			return fmt.Errorf("failed to lookup master %q: %v", master, err)
		}

		macvlanDeviceRequest := &netlink.Macvlan{
			LinkAttrs: netlink.LinkAttrs{
				MTU:         m.Attrs().MTU,
				Name:        macvlanName,
				ParentIndex: m.Attrs().Index,
			},
			Mode: netlink.MACVLAN_MODE_BRIDGE,
		}

		if err = netlink.LinkAdd(macvlanDeviceRequest); err != nil {
			return fmt.Errorf("failed to create macvlan device: %s", err)
		}

		_, err = netlink.LinkByName(macvlanName)
		if err != nil {
			return fmt.Errorf("failed to find newly-created macvlan device %q: %v", macvlanName, err)
		}
		return nil
	})
	Expect(err).NotTo(HaveOccurred())
}
