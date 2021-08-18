package main_test

import (
	"fmt"
	"io/ioutil"
	"net"
	"os/exec"
	"strings"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	"github.com/onsi/gomega/gbytes"
	"github.com/onsi/gomega/gexec"
)

var binaryPath string

var _ = SynchronizedBeforeSuite(func() []byte {
	binaryPath, err := gexec.Build("github.com/containernetworking/plugins/pkg/testutils/echosvr")
	Expect(err).NotTo(HaveOccurred())
	return []byte(binaryPath)
}, func(data []byte) {
	binaryPath = string(data)
})

var _ = SynchronizedAfterSuite(func() {}, func() {
	gexec.CleanupBuildArtifacts()
})

var _ = Describe("Echosvr", func() {
	var session *gexec.Session
	BeforeEach(func() {
		var err error
		cmd := exec.Command(binaryPath)
		session, err = gexec.Start(cmd, GinkgoWriter, GinkgoWriter)
		Expect(err).NotTo(HaveOccurred())
	})

	AfterEach(func() {
		session.Kill().Wait()
	})

	It("starts and doesn't terminate immediately", func() {
		Consistently(session).ShouldNot(gexec.Exit())
	})

	tryConnect := func() (net.Conn, error) {
		programOutput := session.Out.Contents()
		addr := strings.TrimSpace(string(programOutput))

		conn, err := net.Dial("tcp", addr)
		if err != nil {
			return nil, err
		}
		return conn, err
	}

	It("prints its listening address to stdout", func() {
		Eventually(session.Out).Should(gbytes.Say("\n"))
		conn, err := tryConnect()
		Expect(err).NotTo(HaveOccurred())
		conn.Close()
	})

	It("will echo data back to us", func() {
		Eventually(session.Out).Should(gbytes.Say("\n"))
		conn, err := tryConnect()
		Expect(err).NotTo(HaveOccurred())
		defer conn.Close()

		fmt.Fprintf(conn, "hello\n")
		Expect(ioutil.ReadAll(conn)).To(Equal([]byte("hello")))
	})
})
