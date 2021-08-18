# tuning plugin

## Overview

This plugin can change some system controls (sysctls) and several interface attributes (promiscuous mode, MTU and MAC address) in the network namespace.
It does not create any network interfaces and therefore does not bring connectivity by itself.
It is only useful when used in addition to other plugins.

## System Controls Operation
The following network configuration file
```
{
  "name": "mytuning",
  "type": "tuning",
  "sysctl": {
          "net.core.somaxconn": "500"
  }
}
```
will set /proc/sys/net/core/somaxconn to 500.
Other sysctls can be modified as long as they belong to the network namespace (`/proc/sys/net/*`).

A successful result would simply be:
```
{ }
```

## Network sysctls documentation

Some network sysctls are documented in the Linux sources:

- [Documentation/sysctl/net.txt](https://www.kernel.org/doc/Documentation/sysctl/net.txt)
- [Documentation/networking/ip-sysctl.txt](https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt)
- [Documentation/networking/](https://www.kernel.org/doc/Documentation/networking/)

## Interface Attribute Operation
The parameters, "mac", "mtu" and "promisc", changes the interface attributes as followings:

```
{
  "name": "mytuning",
  "type": "tuning",
  "promisc": true,
  "mac": "c2:b0:57:49:47:f1",
  "mtu": 1454
}
```

## Interface attribute configuration reference

* `mac` (string, optional): MAC address (i.e. hardware address) of interface
* `mtu` (integer, optional): MTU of interface
* `promisc` (bool, optional): Change the promiscuous mode of interface

## Supported arguments
The following [CNI_ARGS](https://github.com/containernetworking/cni/blob/master/SPEC.md#parameters) are supported:

* `MAC`: request a specific MAC address for the interface 

    (example: CNI_ARGS="IgnoreUnknown=true;MAC=c2:11:22:33:44:55")

Note: You may add `IgnoreUnknown=true` to allow loose CNI argument verification (see CNI's issue[#560](https://github.com/containernetworking/cni/issues/560)).

