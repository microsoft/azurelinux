#!/bin/sh
if [ "q$1" == "q" ]; then
	echo "Usage: $0 <kernel tar path>"
	exit 1
fi
echo "Extracting linux source"
tar -xvf $1
if [ "$?" -ne "0" ]; then
	echo "Error extracting kernel source"
	exit 1
fi
if [ -d "usbip-$1" ]; then
	rm -rf "usbip-$1"
fi
mv "CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-${1}"/tools/usb/usbip "usbip-$1"
echo "Creating usbip archive"
tar -cJvf "usbip-$1".tar.xz "usbip-$1"
rm -rf "linux-$1"
rm -rf "usbip-$1"
