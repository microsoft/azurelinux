# CIS: Ensure default user shell timeout is configured.
# Avoid reassigning TMOUT after this file has already made it readonly.
if [ "${TMOUT:-}" != 900 ]; then
    TMOUT=900
fi
readonly TMOUT
export TMOUT
