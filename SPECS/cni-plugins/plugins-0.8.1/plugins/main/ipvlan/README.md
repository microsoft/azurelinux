# ipvlan plugin

## Overview

ipvlan is a new [addition](https://lwn.net/Articles/620087/) to the Linux kernel.
Like its cousin macvlan, it virtualizes the host interface.
However unlike macvlan which generates a new MAC address for each interface, ipvlan devices all share the same MAC.
The kernel driver inspects the IP address of each packet when making a decision about which virtual interface should process the packet.

Because all ipvlan interfaces share the MAC address with the host interface, DHCP can only be used in conjunction with ClientID (currently not supported by DHCP plugin).

## Example configuration

```
{
	"name": "mynet",
	"type": "ipvlan",
	"master": "eth0",
	"ipam": {
		"type": "host-local",
		"subnet": "10.1.2.0/24"
	}
}
```

## Network configuration reference

* `name` (string, required): the name of the network.
* `type` (string, required): "ipvlan".
* `master` (string, required unless chained): name of the host interface to enslave.
* `mode` (string, optional): one of "l2", "l3", "l3s". Defaults to "l2".
* `mtu` (integer, optional): explicitly set MTU to the specified value. Defaults to the value chosen by the kernel.
* `ipam` (dictionary, required unless chained): IPAM configuration to be used for this network.

## Notes

* `ipvlan` does not allow virtual interfaces to communicate with the master interface.
Therefore the container will not be able to reach the host via `ipvlan` interface.
Be sure to also have container join a network that provides connectivity to the host (e.g. `ptp`).
* A single master interface can not be enslaved by both `macvlan` and `ipvlan`.
* For IP allocation schemes that cannot be interface agnostic, the ipvlan plugin
can be chained with an earlier plugin that handles this logic. If `master` is
omitted, then the previous Result must contain a single interface name for the
ipvlan plugin to enslave. If `ipam` is omitted, then the previous Result is used
to configure the ipvlan interface.
