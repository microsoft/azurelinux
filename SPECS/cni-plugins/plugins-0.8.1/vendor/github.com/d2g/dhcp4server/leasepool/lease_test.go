package leasepool

import (
	"encoding/json"
	"net"
	"testing"
	"time"
)

/*
 * The Leases are Marshalled and Unmarshalled for storage.
 * I JSON Marshal these for gvklite
 */
func TestMarshaling(test *testing.T) {
	var err error

	startLease := Lease{}
	startLease.IP = net.IPv4(192, 168, 0, 1)
	startLease.Hostname = "ExampleHostname"
	startLease.Status = Active
	startLease.Expiry = time.Now()
	startLease.MACAddress, err = net.ParseMAC("01:23:45:67:89:ab")
	if err != nil {
		test.Error("Error Parsing Mac Address:" + err.Error())
	}
	startLease.ClientID = []byte("adsfasdfasf")

	byteStartLease, err := json.Marshal(startLease)
	if err != nil {
		test.Error("Error Marshaling to JSON:" + err.Error())
	}

	test.Log("StartLease As JSON:" + string(byteStartLease))

	endLease := Lease{}
	err = json.Unmarshal(byteStartLease, &endLease)
	if err != nil {
		test.Error("Error Unmarshaling to JSON:" + err.Error())
	}

	test.Logf("End Lease Object:%v\n", endLease)

	if !startLease.Equal(endLease) {
		byteEndLease, err := json.Marshal(endLease)
		if err != nil {
			test.Error("Can't Marshal End Lease For Debuging:" + err.Error())
		}
		test.Log("End Lease as JSON:" + string(byteEndLease))
		test.Error("Starting Lease Doesn't Match End Lease")
	}

}
