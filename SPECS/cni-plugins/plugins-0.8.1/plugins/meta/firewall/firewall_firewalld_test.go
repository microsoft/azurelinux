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
	"bufio"
	"fmt"
	"os/exec"
	"strings"
	"sync"
	"syscall"

	"github.com/containernetworking/cni/pkg/invoke"
	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/plugins/pkg/ns"
	"github.com/containernetworking/plugins/pkg/testutils"

	"github.com/godbus/dbus"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

const (
	confTmpl = `{
  "cniVersion": "0.3.1",
  "name": "firewalld-test",
  "type": "firewall",
  "backend": "firewalld",
  "zone": "trusted",
  "prevResult": {
    "cniVersion": "0.3.0",
    "interfaces": [
      {"name": "%s", "sandbox": "%s"}
    ],
    "ips": [
      {
        "version": "4",
        "address": "10.0.0.2/24",
        "gateway": "10.0.0.1",
        "interface": 0
      }
    ]
  }
}`
	ifname = "eth0"
)

type fakeFirewalld struct {
	zone   string
	source string
}

func (f *fakeFirewalld) clear() {
	f.zone = ""
	f.source = ""
}

func (f *fakeFirewalld) AddSource(zone, source string) (string, *dbus.Error) {
	f.zone = zone
	f.source = source
	return "", nil
}

func (f *fakeFirewalld) RemoveSource(zone, source string) (string, *dbus.Error) {
	f.zone = zone
	f.source = source
	return "", nil
}

func (f *fakeFirewalld) QuerySource(zone, source string) (bool, *dbus.Error) {
	if f.zone != zone {
		return false, nil
	}
	if f.source != source {
		return false, nil
	}
	return true, nil
}

func spawnSessionDbus(wg *sync.WaitGroup) (string, *exec.Cmd) {
	// Start a private D-Bus session bus
	path, err := invoke.FindInPath("dbus-daemon", []string{
		"/bin", "/sbin", "/usr/bin", "/usr/sbin",
	})
	Expect(err).NotTo(HaveOccurred())
	cmd := exec.Command(path, "--session", "--print-address", "--nofork", "--nopidfile")
	stdout, err := cmd.StdoutPipe()
	Expect(err).NotTo(HaveOccurred())
	err = cmd.Start()
	Expect(err).NotTo(HaveOccurred())

	// Wait for dbus-daemon to print the bus address
	bytes, err := bufio.NewReader(stdout).ReadString('\n')
	Expect(err).NotTo(HaveOccurred())
	busAddr := strings.TrimSpace(string(bytes))
	Expect(strings.HasPrefix(busAddr, "unix:abstract")).To(BeTrue())

	var startWg sync.WaitGroup
	wg.Add(1)
	startWg.Add(1)
	go func() {
		defer GinkgoRecover()

		startWg.Done()
		err = cmd.Wait()
		Expect(err).NotTo(HaveOccurred())
		wg.Done()
	}()

	startWg.Wait()
	return busAddr, cmd
}

var _ = Describe("firewalld test", func() {
	var (
		targetNs ns.NetNS
		cmd      *exec.Cmd
		conn     *dbus.Conn
		wg       sync.WaitGroup
		fwd      *fakeFirewalld
		busAddr  string
	)

	BeforeEach(func() {
		var err error
		targetNs, err = testutils.NewNS()
		Expect(err).NotTo(HaveOccurred())

		// Start a private D-Bus session bus
		busAddr, cmd = spawnSessionDbus(&wg)
		conn, err = dbus.Dial(busAddr)
		Expect(err).NotTo(HaveOccurred())
		err = conn.Auth(nil)
		Expect(err).NotTo(HaveOccurred())
		err = conn.Hello()
		Expect(err).NotTo(HaveOccurred())

		// Start our fake firewalld
		reply, err := conn.RequestName(firewalldName, dbus.NameFlagDoNotQueue)
		Expect(err).NotTo(HaveOccurred())
		Expect(reply).To(Equal(dbus.RequestNameReplyPrimaryOwner))

		fwd = &fakeFirewalld{}
		// Because firewalld D-Bus methods start with lower-case, and
		// because in Go lower-case methods are private, we need to remap
		// Go public methods to the D-Bus name
		methods := map[string]string{
			"AddSource":    firewalldAddSourceMethod,
			"QuerySource":  firewalldQuerySourceMethod,
			"RemoveSource": firewalldRemoveSourceMethod,
		}
		conn.ExportWithMap(fwd, methods, firewalldPath, firewalldZoneInterface)

		// Make sure the plugin uses our private session bus
		testConn = conn
	})

	AfterEach(func() {
		_, err := conn.ReleaseName(firewalldName)
		Expect(err).NotTo(HaveOccurred())

		err = cmd.Process.Signal(syscall.SIGTERM)
		Expect(err).NotTo(HaveOccurred())

		wg.Wait()
	})

	It("works with a 0.3.1 config", func() {
		Expect(isFirewalldRunning()).To(BeTrue())

		conf := fmt.Sprintf(confTmpl, ifname, targetNs.Path())
		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      ifname,
			StdinData:   []byte(conf),
		}
		_, _, err := testutils.CmdAdd(targetNs.Path(), args.ContainerID, ifname, []byte(conf), func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(fwd.zone).To(Equal("trusted"))
		Expect(fwd.source).To(Equal("10.0.0.2/32"))
		fwd.clear()

		err = testutils.CmdDel(targetNs.Path(), args.ContainerID, ifname, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(fwd.zone).To(Equal("trusted"))
		Expect(fwd.source).To(Equal("10.0.0.2/32"))
	})

	It("defaults to the firewalld backend", func() {
		conf := `{
		  "cniVersion": "0.3.1",
		  "name": "firewalld-test",
		  "type": "firewall",
		  "zone": "trusted",
		  "prevResult": {
		    "cniVersion": "0.3.0",
		    "interfaces": [
		      {"name": "eth0", "sandbox": "/foobar"}
		    ],
		    "ips": [
		      {
			"version": "4",
			"address": "10.0.0.2/24",
			"gateway": "10.0.0.1",
			"interface": 0
		      }
		    ]
		  }
		}`

		Expect(isFirewalldRunning()).To(BeTrue())

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      ifname,
			StdinData:   []byte(conf),
		}
		_, _, err := testutils.CmdAdd(targetNs.Path(), args.ContainerID, ifname, []byte(conf), func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(fwd.zone).To(Equal("trusted"))
		Expect(fwd.source).To(Equal("10.0.0.2/32"))
	})

	It("passes through the prevResult", func() {
		conf := `{
		  "cniVersion": "0.3.1",
		  "name": "firewalld-test",
		  "type": "firewall",
		  "zone": "trusted",
		  "prevResult": {
		    "cniVersion": "0.3.0",
		    "interfaces": [
		      {"name": "eth0", "sandbox": "/foobar"}
		    ],
		    "ips": [
		      {
			"version": "4",
			"address": "10.0.0.2/24",
			"gateway": "10.0.0.1",
			"interface": 0
		      }
		    ]
		  }
		}`

		Expect(isFirewalldRunning()).To(BeTrue())

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      ifname,
			StdinData:   []byte(conf),
		}
		r, _, err := testutils.CmdAdd(targetNs.Path(), args.ContainerID, ifname, []byte(conf), func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())

		result, err := current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		Expect(len(result.Interfaces)).To(Equal(1))
		Expect(result.Interfaces[0].Name).To(Equal("eth0"))
		Expect(len(result.IPs)).To(Equal(1))
		Expect(result.IPs[0].Address.String()).To(Equal("10.0.0.2/24"))
	})

	It("works with a 0.4.0 config, including Check", func() {
		Expect(isFirewalldRunning()).To(BeTrue())

		conf := `{
			  "cniVersion": "0.4.0",
			  "name": "firewalld-test",
			  "type": "firewall",
			  "backend": "firewalld",
			  "zone": "trusted",
			  "prevResult": {
			    "cniVersion": "0.4.0",
			    "interfaces": [
			      {"name": "eth0", "sandbox": "/foobar"}
			    ],
			    "ips": [
			      {
				"version": "4",
				"address": "10.0.0.2/24",
				"gateway": "10.0.0.1",
				"interface": 0
			      }
			    ]
			  }
			}`

		args := &skel.CmdArgs{
			ContainerID: "dummy",
			Netns:       targetNs.Path(),
			IfName:      ifname,
			StdinData:   []byte(conf),
		}
		r, _, err := testutils.CmdAddWithArgs(args, func() error {
			return cmdAdd(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(fwd.zone).To(Equal("trusted"))
		Expect(fwd.source).To(Equal("10.0.0.2/32"))

		_, err = current.GetResult(r)
		Expect(err).NotTo(HaveOccurred())

		err = testutils.CmdCheckWithArgs(args, func() error {
			return cmdCheck(args)
		})
		Expect(err).NotTo(HaveOccurred())

		err = testutils.CmdDelWithArgs(args, func() error {
			return cmdDel(args)
		})
		Expect(err).NotTo(HaveOccurred())
		Expect(fwd.zone).To(Equal("trusted"))
		Expect(fwd.source).To(Equal("10.0.0.2/32"))
	})
})
