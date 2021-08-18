package leasepool

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net"
	"time"
)

type LeaseStatus int

const (
	Free     LeaseStatus = 0
	Reserved LeaseStatus = 1
	Active   LeaseStatus = 2
)

type Lease struct {
	IP         net.IP           //The IP of the Lease
	Status     LeaseStatus      //Are Reserved, Active or Free
	MACAddress net.HardwareAddr //Mac Address of the Device
	ClientID   []byte           //ClientID of the request
	Hostname   string           //Hostname From option 12
	Expiry     time.Time        //Expiry Time
}

//leaseMarshal is a mirror of Lease used for marshalling, since
//net.HardwareAddr has no native marshalling capability.
type leaseMarshal struct {
	IP         string
	Status     int
	MACAddress string
	ClientID   string
	Hostname   string
	Expiry     time.Time
}

func (this Lease) MarshalJSON() ([]byte, error) {
	return json.Marshal(leaseMarshal{
		IP:         this.IP.String(),
		Status:     int(this.Status),
		MACAddress: this.MACAddress.String(),
		ClientID:   hex.EncodeToString(this.ClientID),
		Hostname:   this.Hostname,
		Expiry:     this.Expiry,
	})
}

func (this *Lease) UnmarshalJSON(data []byte) error {
	stringUnMarshal := leaseMarshal{}
	err := json.Unmarshal(data, &stringUnMarshal)
	if err != nil {
		return err
	}

	this.IP = net.ParseIP(stringUnMarshal.IP)
	this.Status = LeaseStatus(stringUnMarshal.Status)
	if stringUnMarshal.MACAddress != "" {
		this.MACAddress, err = net.ParseMAC(stringUnMarshal.MACAddress)
		if err != nil {
			return fmt.Errorf("error parsing MAC address: %v", err)
		}
	}
	this.ClientID, err = hex.DecodeString(stringUnMarshal.ClientID)
	if err != nil {
		return fmt.Errorf("error decoding clientID: %v", err)
	}
	this.Hostname = stringUnMarshal.Hostname
	this.Expiry = stringUnMarshal.Expiry

	return nil
}

func (this Lease) Equal(other Lease) bool {
	if !this.IP.Equal(other.IP) {
		return false
	}

	if int(this.Status) != int(other.Status) {
		return false
	}

	if this.MACAddress.String() != other.MACAddress.String() {
		return false
	}

	if !bytes.Equal(this.ClientID, other.ClientID) {
		return false
	}

	if this.Hostname != other.Hostname {
		return false
	}

	if !this.Expiry.Equal(other.Expiry) {
		return false
	}

	return true
}
