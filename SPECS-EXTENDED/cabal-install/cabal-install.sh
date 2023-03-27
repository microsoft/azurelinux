CABALBIN="${HOME}/.cabal/bin"

if ! echo "${PATH}" | /bin/grep -q "${CABALBIN}" ; then
    if [ -d "${CABALBIN}" ]; then
	PATH="${PATH}:${CABALBIN}"
    fi
fi
unset CABALBIN
