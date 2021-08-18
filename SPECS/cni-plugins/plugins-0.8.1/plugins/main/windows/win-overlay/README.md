# win-overlay plugin

## Overview

With win-overlay plugin, all containers (on the same host) are plugged into an Overlay network based on VXLAN encapsulation. 

## Example configuration
```
{
	"name": "mynet",
	"type": "win-overlay",
	"ipMasq": true,
	"endpointMacPrefix": "0E-2A",
	"ipam": {
		"type": "host-local",
		"subnet": "10.10.0.0/16"
	}
    "capabilites": {
        "dns": true
    }

}
```

## Network configuration reference

* `name` (string, required): the name of the network.
* `type` (string, required): "win-overlay".
* `ipMasq` (bool, optional): the inverse of `$FLANNEL_IPMASQ`, setup NAT for the hnsNetwork subnet.
* `dns` (dictionary, optional): dns config to be used.
 * `Nameservers` (list, optional): list of strings to be used for dns nameservers.
 * `Search` (list, optional): list of stings to be used for dns search.
* `endpointMacPrefix` (string, optional): set to the MAC prefix configured for Flannel.
* `Policies` (list, optional): List of hns policies to be used.
* `ipam` (dictionary, required): IPAM configuration to be used for this network.
* `capabilities` (dictionary, optional): runtime capabilities to be parsed and injected by runtime.
 * `dns` (boolean, optional): if true will take the dns config supplied by the runtime and override other settings.