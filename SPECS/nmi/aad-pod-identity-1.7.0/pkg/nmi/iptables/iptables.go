package iptables

import (
	"errors"
	"strings"

	"github.com/coreos/go-iptables/iptables"
	"k8s.io/klog/v2"
)

var (
	tablename       = "nat"
	customchainname = "aad-metadata"
	localhost       = "127.0.0.1/32"
)

// AddCustomChain adds the rule to the host's nat table custom chain
// all tcp requests NOT originating from localhost destined to
// destIp:destPort are routed to targetIP:targetPort
func AddCustomChain(destIP, destPort, targetip, targetport string) error {
	if destIP == "" {
		return errors.New("destIP must be set")
	}
	if destPort == "" {
		return errors.New("destPort must be set")
	}
	if targetip == "" {
		return errors.New("targetip must be set")
	}
	if targetport == "" {
		return errors.New("targetport must be set")
	}

	ipt, err := iptables.New()
	if err != nil {
		return err
	}
	if err := ensureCustomChain(ipt, destIP, destPort, targetip, targetport); err != nil {
		return err
	}
	if err := placeCustomChainInChain(ipt, tablename, "PREROUTING"); err != nil {
		return err
	}

	return nil
}

// LogCustomChain logs added rules to the custom chain
func LogCustomChain() error {
	ipt, err := iptables.New()
	if err != nil {
		return err
	}
	rules, err := ipt.List(tablename, customchainname)
	if err != nil {
		return err
	}
	klog.V(5).Infof("rules for table(%s) chain(%s) rules(%+v)", tablename, customchainname, strings.Join(rules, ", "))

	return nil
}

//	iptables -t nat -I "chain" 1 -j "customchainname"
func placeCustomChainInChain(ipt *iptables.IPTables, table, chain string) error {
	exists, err := ipt.Exists(table, chain, "-j", customchainname)
	if err != nil || !exists {
		if err := ipt.Insert(table, chain, 1, "-j", customchainname); err != nil {
			return err
		}
	}

	return nil
}

func ensureCustomChain(ipt *iptables.IPTables, destIP, destPort, targetip, targetport string) error {
	rules, err := ipt.List(tablename, customchainname)
	if err != nil {
		err = ipt.NewChain(tablename, customchainname)
		if err != nil {
			return err
		}
	}

	/*
		iptables -t nat -S aad-metadata returns 3 rules
			-N aad-metadata
			-A aad-metadata ! -s 127.0.0.1/32 -d 169.254.169.254/32 -p tcp -m tcp --dport 80 -j DNAT --to-destination 127.0.0.1:<nmi port>
			-A aad-metadata -j RETURN

		For this reason we check if the length of rules is 3. If not 3, then we flush and create chain again.
	*/

	expectedRules := map[string]struct{}{
		"-N aad-metadata": {},
		"-A aad-metadata ! -s 127.0.0.1/32 -d " + destIP + "/32 -p tcp -m tcp --dport " + destPort + " -j DNAT --to-destination " + targetip + ":" + targetport: {},
		"-A aad-metadata -j RETURN": {},
	}

	matchingRules := 0
	// ensure all the rules are as expected with the right IPs
	// if any rule has been changed, then we need to flush the
	// entire chain and reconcile with the correct IPs
	for _, rule := range rules {
		if _, ok := expectedRules[rule]; !ok {
			break
		}
		matchingRules++
	}
	// all the required rules exist, so no need to flush custom chain
	if matchingRules == len(expectedRules) {
		return nil
	}

	if err := flushCreateCustomChainrules(ipt, destIP, destPort,
		targetip, targetport); err != nil {
		return err
	}

	return nil
}

func flushCreateCustomChainrules(ipt *iptables.IPTables, destIP, destPort, targetip, targetport string) error {
	klog.Warning("flushing iptables to add aad-metadata custom chains")
	if err := ipt.ClearChain(tablename, customchainname); err != nil {
		return err
	}
	if err := ipt.AppendUnique(
		tablename, customchainname, "-p", "tcp", "!", "-s", localhost, "-d", destIP, "--dport", destPort,
		"-j", "DNAT", "--to-destination", targetip+":"+targetport); err != nil {
		return err
	}
	if err := ipt.AppendUnique(
		tablename, customchainname, "-j", "RETURN"); err != nil {
		return err
	}

	return nil
}

// DeleteCustomChain removes the custom chain aad-metadata reference from PREROUTING
// chain and then removes the chain aad-metadata from nat table
func DeleteCustomChain() error {
	ipt, err := iptables.New()
	if err != nil {
		return err
	}
	if err := removeCustomChainReference(ipt, tablename, "PREROUTING"); err != nil {
		return err
	}
	if err := removeCustomChain(ipt, tablename); err != nil {
		return err
	}
	return nil
}

// removeCustomChainReference - iptables -t "table" -D "chain" -j "customchainname"
func removeCustomChainReference(ipt *iptables.IPTables, table, chain string) error {
	exists, err := ipt.Exists(table, chain, "-j", customchainname)
	if err == nil && exists {
		return ipt.Delete(table, chain, "-j", customchainname)
	}
	return nil
}

// removeCustomChain -  flush and then delete custom chain
// iptables -t "table" -F "customchainname"
// iptables -t "table" -X "customchainname"
func removeCustomChain(ipt *iptables.IPTables, table string) error {
	if err := ipt.ClearChain(table, customchainname); err != nil {
		return err
	}
	if err := ipt.DeleteChain(table, customchainname); err != nil {
		return err
	}
	return nil
}
