#!/bin/sh

# config file syntax:
# deviceno   sysfs_opts...
#
# Examples:
# 0.0.0203 readonly=1 failfast=1
# 0.0.0204
# 0.0.0205 erplog=1

[ -z "$DEVPATH" ] && exit 0
[ "$ACTION" != "add" ] && exit 0

CHANNEL=${DEVPATH##*/}

CONFIG=/etc/dasd.conf
PATH=/sbin:/bin
export PATH

warn() {
    [ -e /dev/kmsg ] && echo "<4>dasdconf.sh Warning: $@" > /dev/kmsg
    echo "dasdconf.sh Warning: $@" >&2
}

if [ -f "$CONFIG" ]; then
    if [ ! -d /sys/bus/ccw/drivers/dasd-eckd ] && [ ! -d /sys/bus/ccw/drivers/dasd-fba ]; then
	#warn "No dasd-eckd or dasd-eckd loaded"
        exit 0
    fi
    sed 'y/ABCDEF/abcdef/' < $CONFIG | while read line; do
        case $line in
            \#*) ;;
            *)
                [ -z "$line" ] && continue
                set $line

		# if we are in single add mode, only add the new CHANNEL
		[ "$SUBSYSTEM" = "ccw" ] && [ "$1" != "$CHANNEL" ] && continue

                DEVICE=$1
                SYSFSPATH=

                if [ -r "/sys/bus/ccw/drivers/dasd-eckd/$DEVICE" ]; then
                    SYSFSPATH="/sys/bus/ccw/drivers/dasd-eckd/$DEVICE"
                elif [ -r "/sys/bus/ccw/drivers/dasd-fba/$DEVICE" ]; then
                    SYSFSPATH="/sys/bus/ccw/drivers/dasd-fba/$DEVICE"
                else
		    # if we are in single add mode, this is a failure!
		    [ "$SUBSYSTEM" = "ccw" ] && warn "Could not find $DEVICE in sysfs"
                    continue
                fi

		# skip already onlined devices
		if [ "$(cat $SYSFSPATH/online)" = "1" ]; then
		    if [ "$SUBSYSTEM" = "ccw" ]; then
		        # if we are in single add mode, we should not touch the device
			warn "$DEVICE is already online, not configuring"
			exit 0
		    fi
		    continue
		fi

                shift
                while [ -n "$1" ]; do
                    (
                        attribute="$1"
                        IFS="="
                        set $attribute

                        if [ "$1" = "use_diag" ]; then
			    # this module better only returns after
			    # all sysfs entries have the "use_diag" file
                            modprobe dasd_diag_mod
                        fi

                        if [ -r "$SYSFSPATH/$1" ]; then
                            echo $2 > $SYSFSPATH/$1 || warn "Could not set $1=$2 for $DEVICE"
                        else
			    warn "$1 does not exist for $DEVICE"
                        fi
                    )
                    shift
                done
		
		# Now, put the device online
                echo 1 > $SYSFSPATH/online || echo "Could not activate $DEVICE"

		# if we are in single add mode, we are done
		[ "$SUBSYSTEM" = "ccw" ] && exit 0
                ;;
        esac
    done
fi
exit 0
