# Source based routing plugin

## Introduction

This plugin performs Source Based Routing (SBR). The most common and standard way to
perform routing is to base it purely on the destination. However, in some
applications which are using network separation for traffic management and
security, there is no way to tell *a priori* which interface should be used,
but the application is capable of making the decision.

As an example, a Telco application might have two networks, a management
network and a SIP (telephony) network for traffic, with rules which state that:

- SIP traffic (only) must be routed over the SIP network;

- all other traffic (but no SIP traffic) must be routed over the management
  network.

There is no way of configuring this based on destination IP, since there is no
way of telling whether a destination IP on the internet is (say) an address
used for downloading updated software packages or a remote SIP endpoint.

Hence Source Based Routing is used.

- The application explicitly listens on the correct interface for incoming
  traffic.

- When the application wishes to send to an address via the SIP network, it
  explicitly binds to the IP of the device on that network.

- Routes for the SIP interface are configured in a separate routing table, and
  a rule is configured to use that table based on the source IP address.

Note that in most cases there is a management device (the first one) and that
the SBR plugin is called once for each device after the first, leaving the
default routing table applied to the management device. However, this not
mandatory, and source based routing may be configured on any or all of the
devices as appropriate.

## Usage

This plugin runs as a chained plugin, and requires the following information
passed in from the previous plugin (which has just set up the network device):

- What is the network interface in question?

- What is the IP address (or addresses) of that network interface?

- What is the default gateway for that interface (if any)?

It then reads all routes to the network interface in use.

Here is an example of what the plugin would do. (The `ip` based commands are
implemented in go, but easier to describe via the command line.) Suppose that
it reads that:

- The interface is `net1`.

- The IP address on that interface is `192.168.1.209`.

- The default gateway on that interface is `192.168.1.1`.

- There is one route configured on that network interface, which is
  `192.168.1.0/24`.

Then the actions it takes are the following.

- It creates a new routing table, and sets a rule to use it for the IP address in question.

        ip rule add from 192.168.1.209/32 table 100

- It adds a route to the default gateway for the relevant table.

        ip route add default via 192.168.1.1 dev net1 table 100

- It moves every existing route on the device to the new table.

        ip route del 192.168.1.0/24 dev net1 src 192.168.1.209
        ip route add 192.168.1.0/24 dev net1 src 192.168.1.209 table 100

On deletion it:

- deletes the rule (`ip rule del from 192.168.1.209/32 table 100`), which it
  finds by deleting rules relating to IPs on the device which is about to be
  deleted.

- does nothing with routes (since the kernel automatically removes routes when
  the device with which they are associated is deleted).

## Future enhancements and known limitations

The following are possible future enhancements.

- The table number is currently selected by starting at 100, then incrementing
  the value until an unused table number is found. It might be nice to have an
  option to pass the table number as an input.

- There is no log severity, and there is no logging to file (pending changes to
  CNI logging generally).

- This plugin sets up Source Based Routing, as described above. In future,
  there may be a need for a VRF plugin (that uses
  [VRF routing](https://www.kernel.org/doc/Documentation/networking/vrf.txt)
  instead of source based routing). If and when this happens, it is likely that
  the logic would be virtually identical for the plugin, and so the same plugin
  might offer either SBR or VRF routing depending on configuration.

## Configuration

This plugin must be used as a chained plugin. There are no specific configuration parameters.

A sample configuration for this plugin acting as a chained plugin after flannel
is the following.

~~~json
{
  "name": "flannel-sbr",
  "cniVersion": "0.3.0",
  "plugins":
    [
        { "type": "flannel" },
        {
          "type": "sbr",
        }
    ]
}
~~~
