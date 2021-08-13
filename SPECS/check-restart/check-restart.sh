OUTPUT=$(needs-restarting -r)
echo $OUTPUT
RESTART_REQD='Reboot is required'
if [[ "$OUTPUT" == *"$RESTART_REQD"* ]]; then
    touch /var/run/reboot-required
fi
