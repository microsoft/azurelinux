# static IP address management plugin

## Overview

static IPAM is very simple IPAM plugin that assigns IPv4 and IPv6 addresses statically to container. This will be useful in debugging purpose and in case of assign same IP address in different vlan/vxlan to containers.


## Example configuration

```
{
	"ipam": {
		"type": "static",
		"addresses": [
			{
				"address": "10.10.0.1/24",
				"gateway": "10.10.0.254"
			},
			{
				"address": "3ffe:ffff:0:01ff::1/64",
				"gateway": "3ffe:ffff:0::1"
			}
		],
		"routes": [
			{ "dst": "0.0.0.0/0" },
			{ "dst": "192.168.0.0/16", "gw": "10.10.5.1" },
			{ "dst": "3ffe:ffff:0:01ff::1/64" }
		],
		"dns": {
			"nameservers" : ["8.8.8.8"],
			"domain": "example.com",
			"search": [ "example.com" ]
		}
	}
}
```

## Network configuration reference

* `type` (string, required): "static"
* `addresses` (array, optional): an array of ip address objects:
	* `address` (string, required): CIDR notation IP address.
	* `gateway` (string, optional): IP inside of "subnet" to designate as the gateway.
* `routes` (string, optional): list of routes add to the container namespace. Each route is a dictionary with "dst" and optional "gw" fields. If "gw" is omitted, value of "gateway" will be used.
* `dns` (string, optional): the dictionary with "nameservers", "domain" and "search".

## Supported arguments

The following [CNI_ARGS](https://github.com/containernetworking/cni/blob/master/SPEC.md#parameters) are supported:

* `IP`: request a specific CIDR notation IP addresses, comma separated
* `GATEWAY`: request a specific gateway address

    (example: CNI_ARGS="IP=10.10.0.1/24;GATEWAY=10.10.0.254")
