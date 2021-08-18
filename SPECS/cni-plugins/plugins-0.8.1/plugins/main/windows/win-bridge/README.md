# win-bridge plugin

## Overview

With win-bridge plugin, all containers (on the same host) are plugged into an L2Bridge network that has one endpoint in the host namespace.

## Example configuration
```
{
	"name": "mynet",
	"type": "win-bridge",
	"ipMasqNetwork": "10.244.0.0/16",
	"ipam": {
		"type": "host-local",
		"subnet": "10.10.0.0/16"
	},
    "policies":[
        {
            "name":"EndpointPolicy",
            "value":{
                "Type":"ROUTE",
                "DestinationPrefix":"10.137.198.27/32",
                "NeedEncap":true
            }
        } 
    ],
    "HcnPolicyArgs": [
        {
            "Type": "SDNRoute"
            "Settings": {
                "DestinationPrefix": "11.0.0.0/8",
                "NeedEncap": true
            }
        }
    ].          
    "capabilities": {
        "dns": true
    }
}
```

## Network configuration reference

* `ApiVersion` (integer, optional): ApiVersion to use, will default to hns. If set to "2" will try to use hcn APIs.
* `name` (string, required): the name of the network.
* `type` (string, required): "win-bridge".
* `ipMasqNetwork` (string, optional): setup NAT if not empty.
* `dns` (dictionary, optional): dns config to be used.
 * `Nameservers` (list, optional): list of strings to be used for dns nameservers.
 * `Search` (list, optional): list of stings to be used for dns search.
* `ipam` (dictionary, optional): IPAM configuration to be used for this network.
* `Policies` (list, optional): List of hns policies to be used (only used when ApiVersion is < 2).
* `HcnPolicyArgs` (list, optional): List of hcn policies to be used (only used when ApiVersion is 2).
* `capabilities` (dictionary, optional): runtime capabilities to enable.
 * `dns` (boolean, optional): if true will take the dns config supplied by the runtime and override other settings.