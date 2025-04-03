#!/bin/bash +x
#
# kabi.sh - Automatically extract any kernel symbol checksum from the
#           symvers file and add to RPM deps.  This is used to move the
#           checksum checking from modprobe to rpm install for 3rd party
#           modules (so they can fail during install and not at load).

IFS=$'\n'

for symvers in $(grep -E '(/boot/symvers-.*|/lib/modules/[1-9].*/symvers)\.(gz|xz)') "$@";
do
	cat_prog="cat"
	case "$symvers" in
	*.gz) cat_prog="zcat" ;;
	*.xz) cat_prog="xzcat" ;;
	esac

	# We generate dependencies only for symbols exported by vmlinux itself
	# and not for kmods here as they are spread across subpackages,
	# so Provides: generation for kmods is handled by find-provides.ksyms.
	"$cat_prog" "$symvers" | awk '/[^	]*	[^	]*	vmlinux	.*/ { print "kernel(" $2 ") = " $1 }'
done
