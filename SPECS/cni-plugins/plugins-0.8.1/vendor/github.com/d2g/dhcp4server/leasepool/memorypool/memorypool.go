package memorypool

import (
	"bytes"
	"errors"
	"github.com/d2g/dhcp4server/leasepool"
	"net"
	"sync"
)

type MemoryPool struct {
	pool     []leasepool.Lease
	poolLock sync.Mutex
}

//Add A Lease To The Pool
func (t *MemoryPool) AddLease(newLease leasepool.Lease) error {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	if t.pool == nil {
		t.pool = make([]leasepool.Lease, 0)
	}

	for i := range t.pool {
		if t.pool[i].IP.Equal(newLease.IP) {
			//Lease Already Exists In Pool
			return errors.New("Error: Lease IP \"" + newLease.IP.String() + "\" alreay exists in Pool")
		}
	}

	t.pool = append([]leasepool.Lease{newLease}, t.pool...)
	return nil
}

//Remove a Lease From The Pool
func (t *MemoryPool) RemoveLease(leaseIP net.IP) error {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	for i := range t.pool {
		if t.pool[i].IP.Equal(leaseIP) {

			//Move the Last Element to This Position.
			t.pool[i] = t.pool[len(t.pool)-1]

			//Shortern the Pool By One.
			t.pool = t.pool[0:(len(t.pool) - 1)]
			return nil
		}
	}

	return errors.New("Error: Lease IP \"" + leaseIP.String() + "\" Is Not In The Pool")
}

//Remove All Leases from the Pool (Required for Persistant LeaseManagers)
func (t *MemoryPool) PurgeLeases() error {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	t.pool = nil
	t.pool = make([]leasepool.Lease, 0)
	return nil
}

/*
 * Get the Lease
 * -Found
 * -Copy Of the Lease
 * -Any Error
 */
func (t *MemoryPool) GetLease(leaseIP net.IP) (bool, leasepool.Lease, error) {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	for i := range t.pool {
		if t.pool[i].IP.Equal(leaseIP) {
			return true, t.pool[i], nil
		}
	}
	return false, leasepool.Lease{}, nil
}

func makeKey(macAddress net.HardwareAddr, clientID []byte) []byte {
	key := []byte(macAddress)
	if len(clientID) > 0 {
		key = append(key, clientID...)
	}
	return key
}

//Get the lease already in use by that hardware address and/or client identifier.
func (t *MemoryPool) GetLeaseForClient(macAddress net.HardwareAddr, clientID []byte) (bool, leasepool.Lease, error) {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	needleKey := makeKey(macAddress, clientID)
	for i := range t.pool {
		haystackKey := makeKey(t.pool[i].MACAddress, t.pool[i].ClientID)
		if bytes.Equal(needleKey, haystackKey) {
			return true, t.pool[i], nil
		}
	}
	return false, leasepool.Lease{}, nil
}

/*
 * -Lease Available
 * -Lease
 * -Error
 */
func (t *MemoryPool) GetNextFreeLease() (bool, leasepool.Lease, error) {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	//Loop Through the elements backwards.
	for i := (len(t.pool) - 1); i >= 0; i-- {
		//If the Lease Is Free
		if t.pool[i].Status == leasepool.Free {
			//Take the Element
			iLease := t.pool[i]
			//Shrink the Pool By 1
			t.pool = t.pool[:(len(t.pool) - 1)]
			//Place the Lease At the Begining (This saves us having some sort of counter...)
			t.pool = append([]leasepool.Lease{iLease}, t.pool...)
			return true, iLease, nil
		}
	}
	return false, leasepool.Lease{}, nil
}

/*
 * Return All Leases
 */
func (t *MemoryPool) GetLeases() ([]leasepool.Lease, error) {
	return t.pool, nil
}

/*
 * Update Lease
 * - Has Updated
 * - Error
 */
func (t *MemoryPool) UpdateLease(lease leasepool.Lease) (bool, error) {
	t.poolLock.Lock()
	defer t.poolLock.Unlock()

	for i := range t.pool {
		if t.pool[i].IP.Equal(lease.IP) {

			t.pool[i].MACAddress = lease.MACAddress
			t.pool[i].ClientID = lease.ClientID
			t.pool[i].Hostname = lease.Hostname
			t.pool[i].Expiry = lease.Expiry
			t.pool[i].Status = lease.Status

			return true, nil
		}
	}
	return false, nil
}
