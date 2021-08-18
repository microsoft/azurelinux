# firewall plugin

## Overview

This plugin creates firewall rules to allow traffic to/from container IP address via the host network .
It does not create any network interfaces and therefore does not set up connectivity by itself.
It is intended to be used as a chained plugins.

## Operation
The following network configuration file

```json
{
    "cniVersion": "0.3.1",
    "name": "bridge-firewalld",
    "plugins": [
      {
        "type": "bridge",
        "bridge": "cni0",
        "isGateway": true,
        "ipMasq": true,
        "ipam": {
            "type": "host-local",
            "subnet": "10.88.0.0/16",
            "routes": [
                { "dst": "0.0.0.0/0" }
            ]
        }
      },
      {
        "type": "firewall",
      }
    ]
}
```

will allow any IP addresses configured by earlier plugins to send/receive traffic via the host.

A successful result would simply be an empty result, unless a previous plugin passed a previous result, in which case this plugin will return that previous result.

## Backends

This plugin supports multiple firewall backends that implement the desired functionality.
Available backends include `iptables` and `firewalld` and may be selected with the `backend` key.
If no `backend` key is given, the plugin will use firewalld if the service exists on the D-Bus system bus.
If no firewalld service is found, it will fall back to iptables.

## firewalld backend rule structure
When the `firewalld` backend is used, this example will place the IPAM allocated address for the container (e.g. 10.88.0.2) into firewalld's `trusted` zone, allowing it to send/receive traffic.


A sample standalone config list (with the file extension .conflist) using firewalld backend might
look like:

```json
{
    "cniVersion": "0.3.1",
    "name": "bridge-firewalld",
    "plugins": [
      {
        "type": "bridge",
        "bridge": "cni0",
        "isGateway": true,
        "ipMasq": true,
        "ipam": {
            "type": "host-local",
            "subnet": "10.88.0.0/16",
            "routes": [
                { "dst": "0.0.0.0/0" }
            ]
        }
      },
      {
        "type": "firewall",
	"backend": "firewalld"
      }
    ]
}
```


`FORWARD_IN_ZONES_SOURCE` chain:
- `-d 10.88.0.2 -j FWDI_trusted`

`CNI_FORWARD_OUT_ZONES_SOURCE` chain:
- `-s 10.88.0.2 -j FWDO_trusted`


## iptables backend rule structure

A sample standalone config list (with the file extension .conflist) using iptables backend might
look like:

```json
{
    "cniVersion": "0.3.1",
    "name": "bridge-firewalld",
    "plugins": [
      {
        "type": "bridge",
        "bridge": "cni0",
        "isGateway": true,
        "ipMasq": true,
        "ipam": {
            "type": "host-local",
            "subnet": "10.88.0.0/16",
            "routes": [
                { "dst": "0.0.0.0/0" }
            ]
        }
      },
      {
        "type": "firewall",
	"backend": "iptables"
      }
    ]
}
```

When the `iptables` backend is used, the above example will create two new iptables chains in the `filter` table and add rules that allow the given interface to send/receive traffic.

### FORWARD
A new chain, CNI-FORWARD is added to the FORWARD chain.  CNI-FORWARD is the chain where rules will be added
when containers are created and from where rules will be removed when containers terminate.

`FORWARD` chain:
- `-j CNI-FORWARD`

CNI-FORWARD will have a pair of rules added, one for each direction, using the IPAM assigned IP address
of the container as shown:

`CNI_FORWARD` chain:
- `-s 10.88.0.2 -m conntrack --ctstate RELATED,ESTABLISHED -j CNI-FORWARD`
- `-d 10.88.0.2 -j CNI-FORWARD`

