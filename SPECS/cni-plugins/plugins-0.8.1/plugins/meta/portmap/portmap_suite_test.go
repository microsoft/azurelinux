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
	"math/rand"
	"net"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/containernetworking/plugins/pkg/ns"

	. "github.com/onsi/ginkgo"
	"github.com/onsi/ginkgo/config"
	. "github.com/onsi/gomega"
	"github.com/onsi/gomega/gbytes"
	"github.com/onsi/gomega/gexec"

	"testing"
)

func TestPortmap(t *testing.T) {
	rand.Seed(config.GinkgoConfig.RandomSeed)

	RegisterFailHandler(Fail)
	RunSpecs(t, "plugins/meta/portmap")
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

func StartEchoServerInNamespace(netNS ns.NetNS) (int, *gexec.Session, error) {
	session, err := startInNetNS(echoServerBinaryPath, netNS)
	Expect(err).NotTo(HaveOccurred())

	// wait for it to print it's address on stdout
	Eventually(session.Out).Should(gbytes.Say("\n"))
	_, portString, err := net.SplitHostPort(strings.TrimSpace(string(session.Out.Contents())))
	Expect(err).NotTo(HaveOccurred())

	port, err := strconv.Atoi(portString)
	Expect(err).NotTo(HaveOccurred())
	return port, session, nil
}
