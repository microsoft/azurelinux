# Export BMC URL
#

BMC_INFO="/var/run/bmc-info"

if [ "$(id -u)" = "0" ]; then
	[ -f ${BMC_INFO} ] && . ${BMC_INFO} && \
		export "${BMC_URL}" "${BMC_IPv4}" >/dev/null 2>&1
fi

unset BMC_INFO
