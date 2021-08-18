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
	"fmt"
	"strings"

	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/godbus/dbus"
)

const (
	dbusName               = "org.freedesktop.DBus"
	dbusPath               = "/org/freedesktop/DBus"
	dbusGetNameOwnerMethod = "GetNameOwner"

	firewalldName               = "org.fedoraproject.FirewallD1"
	firewalldPath               = "/org/fedoraproject/FirewallD1"
	firewalldZoneInterface      = "org.fedoraproject.FirewallD1.zone"
	firewalldAddSourceMethod    = "addSource"
	firewalldRemoveSourceMethod = "removeSource"
	firewalldQuerySourceMethod  = "querySource"

	errZoneAlreadySet = "ZONE_ALREADY_SET"
)

// Only used for testcases to override the D-Bus connection
var testConn *dbus.Conn

type fwdBackend struct {
	conn *dbus.Conn
}

// fwdBackend implements the FirewallBackend interface
var _ FirewallBackend = &fwdBackend{}

func getConn() (*dbus.Conn, error) {
	if testConn != nil {
		return testConn, nil
	}
	return dbus.SystemBus()
}

// isFirewalldRunning checks whether firewalld is running.
func isFirewalldRunning() bool {
	conn, err := getConn()
	if err != nil {
		return false
	}

	dbusObj := conn.Object(dbusName, dbusPath)
	var res string
	if err := dbusObj.Call(dbusName+"."+dbusGetNameOwnerMethod, 0, firewalldName).Store(&res); err != nil {
		return false
	}

	return true
}

func newFirewalldBackend(conf *FirewallNetConf) (FirewallBackend, error) {
	conn, err := getConn()
	if err != nil {
		return nil, err
	}

	backend := &fwdBackend{
		conn: conn,
	}
	return backend, nil
}

func (fb *fwdBackend) Add(conf *FirewallNetConf, result *current.Result) error {
	for _, ip := range result.IPs {
		ipStr := ipString(ip.Address)
		// Add a firewalld rule which assigns the given source IP to the given zone
		firewalldObj := fb.conn.Object(firewalldName, firewalldPath)
		var res string
		if err := firewalldObj.Call(firewalldZoneInterface+"."+firewalldAddSourceMethod, 0, conf.FirewalldZone, ipStr).Store(&res); err != nil {
			if !strings.Contains(err.Error(), errZoneAlreadySet) {
				return fmt.Errorf("failed to add the address %v to %v zone: %v", ipStr, conf.FirewalldZone, err)
			}
		}
	}
	return nil
}

func (fb *fwdBackend) Del(conf *FirewallNetConf, result *current.Result) error {
	for _, ip := range result.IPs {
		ipStr := ipString(ip.Address)
		// Remove firewalld rules which assigned the given source IP to the given zone
		firewalldObj := fb.conn.Object(firewalldName, firewalldPath)
		var res string
		firewalldObj.Call(firewalldZoneInterface+"."+firewalldRemoveSourceMethod, 0, conf.FirewalldZone, ipStr).Store(&res)
	}
	return nil
}

func (fb *fwdBackend) Check(conf *FirewallNetConf, result *current.Result) error {
	for _, ip := range result.IPs {
		ipStr := ipString(ip.Address)
		// Check for a firewalld rule for the given source IP to the given zone
		firewalldObj := fb.conn.Object(firewalldName, firewalldPath)
		var res bool
		if err := firewalldObj.Call(firewalldZoneInterface+"."+firewalldQuerySourceMethod, 0, conf.FirewalldZone, ipStr).Store(&res); err != nil {
			return fmt.Errorf("failed to find the address %v in %v zone", ipStr, conf.FirewalldZone)
		}
	}
	return nil
}
