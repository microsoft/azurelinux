#!/bin/bash

# Simple shell script to wait for the tty for an uart using BT HCI to show up
# and then invoke btattach with the right parameters, this is intended to be
# invoked from a hardware-activated systemd service
#
# For now this only suports ACPI enumerated Broadcom BT HCIs.
# This has been tested on Bay and Cherry Trail devices with both ACPI and
# PCI enumerated UARTs.
#
# Note the kernel bt developers are working on solving this entirely in the
# kernel, so it is not worth the trouble to write something better then this.

BT_DEV="/sys/bus/platform/devices/$1"
BT_DEV="$(readlink -f $BT_DEV)"
UART_DEV="$(dirname $BT_DEV)"

# Stupid GPD-pocket has USB BT with id 0000:0000, but still claims to have
# an uart attached bt
if [ "$1" = "BCM2E7E:00" ] && lsusb | grep -q "ID 0000:0000"; then
	exit 0
fi

while [ ! -d "$UART_DEV/tty" ]; do
	sleep .2
done

TTY="$(ls $UART_DEV/tty)"

exec btattach --bredr "/dev/$TTY" -P bcm
