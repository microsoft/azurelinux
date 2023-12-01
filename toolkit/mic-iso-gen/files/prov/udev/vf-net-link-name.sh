#!/bin/bash

# This script returns a interface name in the format:
# {pci_bus}_pf{port_number}vf{vf_number}_vf for VFs on a NIC (eg '4b_pf0vf0_vf')

# ID_PATH will be in the form to "pci-0000:4b:00.1"
# we want to extract the PCI bus that the NIC is on
# to prefix the interface name with to make it easy
# to identify which port(s) belong to which card.
prefix=$(echo ${ID_PATH##pci-} | awk -F ':' '{ print $2 }')

# Here we make use of udevs builtin ID_NET_NAME_PATH
# to firstly extract the pf, and then the vf that backs
# the interface.
pf=$(echo ${ID_NET_NAME_PATH##*f} | awk -F 'v' '{ print $1 }')
vf=${ID_NET_NAME_PATH#*v}
echo NAME="${prefix}_pf${pf}vf${vf}_vf"