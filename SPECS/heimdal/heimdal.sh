if ! echo ${PATH} | /bin/grep -q /usr/lib/heimdal/bin ; then
	PATH=/usr/lib/heimdal/bin:${PATH}
fi
