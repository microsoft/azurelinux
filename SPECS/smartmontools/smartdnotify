#! /bin/sh

# Send mail
if which mail >/dev/null 2>&1
then
  echo "$SMARTD_FULLMESSAGE" | mail -s "$SMARTD_SUBJECT" "$SMARTD_ADDRESS"
fi

# Notify desktop user
MESSAGE="SMART Disk monitor:"
case "$SMARTD_FAILTYPE" in
    "EmailTest"|"Health"|"Temperature"|"Usage")
        ;;
    *)
#       "CurrentPendingSector",       // 10
#       "OfflineUncorrectableSector", // 11
#       "FailedReadSmartErrorLog",    // 7
#       "ErrorCount",                 // 4
#       "FailedReadSmartData",        // 6
#       "FailedHealthCheck",          // 5
#       "FailedOpenDevice",           // 9
#       "SelfTest",                   // 3
#       "FailedReadSmartSelfTestLog", // 8
      exit 0
esac

# direct write to terminals, do not use 'wall', because we don't want its ugly header
for t in $(who | awk '{ print $2; }' | grep -e '^tty' -e '^pts/')
do
  echo "$MESSAGE
$SMARTD_MESSAGE" >/dev/$t 2>/dev/null ||:
done

