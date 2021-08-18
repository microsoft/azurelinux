package leasepool

import (
	"net"
)

/*
 * Lease.IP is the Key.
 */
type LeasePool interface {
	//Add A Lease To The Pool
	AddLease(Lease) error

	//Remove
	RemoveLease(net.IP) error

	//Remove All Leases from the Pool (Required for Persistant LeaseManagers)
	PurgeLeases() error

	/*
	 * Get the Lease
	 * -Found
	 * -Copy Of the Lease
	 * -Any Error
	 */
	GetLease(net.IP) (bool, Lease, error)

	//Get the lease already in use by that hardware address and/or client identifier.
	GetLeaseForClient(net.HardwareAddr, []byte) (bool, Lease, error)

	/*
	 * -Lease Available
	 * -Lease
	 * -Error
	 */
	GetNextFreeLease() (bool, Lease, error)

	/*
	 * Return All Leases
	 */
	GetLeases() ([]Lease, error)

	/*
	 * Update Lease
	 * - Has Updated
	 * - Error
	 */
	UpdateLease(Lease) (bool, error)
}
