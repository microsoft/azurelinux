#!/bin/bash
# This script takes the port name and returns a interface name in the format:
# {pci_bus}_p{port_number} for PFs on a NIC (eg '4b_p0')
# {pci_bus}_pf{port_number}vf{vf_number}_rep for representor ports on a NIC (eg '4b_pf0vf0_rep')
PORT_NAME=$1

# ID_PATH will be in the form to "pci-0000:4b:00.1" we want to extract the PCI bus that the NIC is on
# to prefix the interface name with to make it easy to identify which port(s) belong to which card.
prefix=$(echo "${ID_PATH##pci-}" | awk -F ':' '{ print $2 }')
name="${prefix}_${PORT_NAME}"

# p[0,1] is a special case as these are the physical ports on the NIC itself. All other devices that
# arrive here are representor ports for VFs.
if [[ ${PORT_NAME} =~ ^p[0,1] ]]; then
   echo NAME="${name}"
else
   echo NAME="${name}_rep"
fi