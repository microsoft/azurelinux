#!/bin/sh

# config file syntax:
# deviceno   WWPN   FCPLUN
# deviceno			# allowed when auto LUN scan is enabled and port is in NPIV mode
#
# Example:
# 0.0.4000 0x5005076300C213e9 0x5022000000000000 
# 0.0.4001 0x5005076300c213e9 0x5023000000000000 
# 0.0.5000
#
#
# manual setup:
# modprobe zfcp
# echo 1    > /sys/bus/ccw/drivers/zfcp/0.0.4000/online
# echo LUN  > /sys/bus/ccw/drivers/zfcp/0.0.4000/WWPN/unit_add
# 
# Example:
# modprobe zfcp
# echo 1                  > /sys/bus/ccw/drivers/zfcp/0.0.4000/online
# echo 0x5022000000000000 > /sys/bus/ccw/drivers/zfcp/0.0.4000/0x5005076300c213e9/unit_add

CONFIG=/etc/zfcp.conf
PATH=/bin:/sbin

set_online()
{
   DEVICE=$1

   [ `cat /sys/bus/ccw/drivers/zfcp/${DEVICE}/online` = "0" ] \
      && echo 1 > /sys/bus/ccw/drivers/zfcp/${DEVICE}/online
}

if [ -f "$CONFIG" ]; then
   if [ ! -d /sys/bus/ccw/drivers/zfcp ]; then
      modprobe zfcp
   fi
   if [ ! -d /sys/bus/ccw/drivers/zfcp ]; then
      exit 1
   fi
   sed 'y/ABCDEF/abcdef/' < $CONFIG | while read line; do
       case $line in
	   \#*) ;;
	   *)
	       [ -z "$line" ] && continue
	       set $line
	       if [ $# -eq 1 ]; then
		   DEVICE=${1##*0x}
		   if [ `cat /sys/module/zfcp/parameters/allow_lun_scan` = "Y" ]; then
		      set_online ${DEVICE}
		      grep -q NPIV /sys/bus/ccw/devices/${DEVICE}/host*/fc_host/host*/port_type || \
		         echo "Error: Only device ID (${DEVICE}) given, but port not in NPIV mode"
		   else
		      echo "Error: Only device ID (${DEVICE}) given, but LUN scan is disabled for the zfcp module"
		   fi
		   continue
	       fi
	       if [ $# -eq 5 ]; then
		   DEVICE=$1
		   SCSIID=$2
		   WWPN=$3
		   SCSILUN=$4
		   FCPLUN=$5
		   echo "Warning: Deprecated values in /etc/zfcp.conf, ignoring SCSI ID $SCSIID and SCSI LUN $SCSILUN"
	       elif [ $# -eq 3 ]; then
		   DEVICE=${1##*0x}
		   WWPN=$2
		   FCPLUN=$3
	       fi
	       set_online ${DEVICE}
	       [ ! -d /sys/bus/ccw/drivers/zfcp/${DEVICE}/${WWPN}/${FCPLUN} ] \
		   && echo $FCPLUN > /sys/bus/ccw/drivers/zfcp/${DEVICE}/${WWPN}/unit_add
	       ;;
       esac
   done
fi
exit 0
