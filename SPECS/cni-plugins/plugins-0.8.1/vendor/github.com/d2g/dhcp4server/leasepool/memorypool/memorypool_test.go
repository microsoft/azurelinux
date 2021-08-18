package memorypool

import (
	"github.com/d2g/dhcp4"
	"github.com/d2g/dhcp4server/leasepool"
	"net"
	"testing"
)

func TestLeaseCycle(test *testing.T) {
	myMemoryLeasePool := MemoryPool{}

	//Lets add a list of IPs to the pool these will be served to the clients so make sure they work for you.
	// So Create Array of IPs 192.168.1.1 to 192.168.1.30
	for i := 0; i < 30; i++ {
		err := myMemoryLeasePool.AddLease(leasepool.Lease{IP: dhcp4.IPAdd(net.IPv4(192, 168, 1, 1), i)})
		if err != nil {
			test.Error("Error Creating Lease:" + err.Error())
		}
	}

	for i := 0; i < 30; i++ {
		hasLease, iLease, err := myMemoryLeasePool.GetNextFreeLease()
		if err != nil {
			test.Error("Error Getting Lease:" + err.Error())
		}
		if !hasLease {
			test.Error("Failed to get get lease (none free?)")
		}

		if !dhcp4.IPAdd(net.IPv4(192, 168, 1, 1), i).Equal(iLease.IP) {
			test.Error("Expected Lease:" + dhcp4.IPAdd(net.IPv4(192, 168, 1, 1), i).String() + " Received:" + iLease.IP.String())
		}
	}
}

func TestSingleLease(test *testing.T) {
	myMemoryLeasePool := MemoryPool{}

	err := myMemoryLeasePool.AddLease(leasepool.Lease{IP: dhcp4.IPAdd(net.IPv4(192, 168, 1, 5), 0)})
	if err != nil {
		test.Error("Error Creating Lease:" + err.Error())
	}

	hasLease, iLease, err := myMemoryLeasePool.GetNextFreeLease()
	if err != nil {
		test.Error("Error Getting Lease:" + err.Error())
	}
	if !hasLease {
		test.Error("Failed to get get lease (none free?)")
	}

	if !dhcp4.IPAdd(net.IPv4(192, 168, 1, 5), 0).Equal(iLease.IP) {
		test.Error("Expected Lease:" + dhcp4.IPAdd(net.IPv4(192, 168, 1, 5), 0).String() + " Received:" + iLease.IP.String())
	}
}
