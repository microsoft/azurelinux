# bandwidth plugin

## Overview

This plugin provides a way to use and configure Linux's Traffic control (tc) subystem. tc encompasses the sets of mechanisms and operations by which packets are queued for transmission/reception on a network interface.

This plugin configures a token bucket filter (tbf) queuing discipline (qdisc) on both ingress and egress traffic. Resulting in traffic being shaped when reading / writing.

Due to limitations on tc shaping rules for ingress, this plugin creates an Intermediate Functional Block device (ifb) to redirect packets from the host interface. tc tbf is then applied to the ifb device. The packets that were redirected to the ifb devices, are written OUT (and shaped) to the host interface.

This plugin is only useful when used in addition to other plugins.

## Chaining

The bandwidth plugin applies traffic shaping to interfaces (as described above) created by previously applied plugins.

The following is an example [json configuration list](https://github.com/containernetworking/cni/blob/master/SPEC.md#network-configuration-list-runtime-examples) for creating a `ptp` between the host -> container via veth interfaces, whereby traffic is shaped by the `bandwidth` plugin:

```json
{
  "cniVersion": "0.3.1",
  "name": "mynet",
  "plugins": [
    {
      "type": "ptp",
      "ipMasq": true,
      "mtu": 512,
      "ipam": {
          "type": "host-local",
          "subnet": "10.0.0.0/24"
      },
      "dns": {
        "nameservers": [ "10.1.0.1" ]
      }
    },
    {
      "name": "slowdown",
      "type": "bandwidth",
      "ingressRate": 123,
      "ingressBurst": 456,
      "egressRate": 123,
      "egressBurst": 456
    }
  ]
}
```

The result is an `ifb` device in the host namespace redirecting to the `host-interface`, with `tc tbf` applied on the `ifb` device and the `container-interface`

## Network configuration reference
* ingressRate: is the rate in bps at which traffic can enter an interface. (See http://man7.org/linux/man-pages/man8/tbf.8.html)
* ingressBurst: is the maximum amount in bits that tokens can be made available for instantaneously. (See http://man7.org/linux/man-pages/man8/tbf.8.html)
* egressRate: is the rate in bps at which traffic can leave an interface. (See http://man7.org/linux/man-pages/man8/tbf.8.html)
* egressBurst: is the maximum amount in bits that tokens can be made available for instantaneously. (See http://man7.org/linux/man-pages/man8/tbf.8.html)

Both ingressRate and ingressBurst must be set in order to limit ingress bandwidth. If neither one is set, then ingress bandwidth is not limited.
Both egressRate and egressBurst must be set in order to limit egress bandwidth. If neither one is set, then egress bandwidth is not limited.


## tc tbf documentation

- [tldp traffic control](http://tldp.org/HOWTO/Traffic-Control-HOWTO/components.html)
- [man tbf](http://man7.org/linux/man-pages/man8/tbf.8.html)
- [tc ingress and ifb mirroring](https://serverfault.com/questions/350023/tc-ingress-policing-and-ifb-mirroring)
