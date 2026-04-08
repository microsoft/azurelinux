#!/usr/bin/bash
### varrun-convert.sh
### convert legacy filecontext entries containing /var/run to /run
### and load an extra selinux module with the new content
### the script takes a policy name as an argument

# Set DEBUG=yes before running the script to get more verbose output
# on the terminal and to the $LOG file
if [ "${DEBUG}" = "yes" ]; then
  set -x
fi

# Auxiliary and log files will be created in OUTPUTDIR
OUTPUTDIR="/run/selinux-policy"
LOG="$OUTPUTDIR/log"
mkdir -p ${OUTPUTDIR}

if [ -z ${1} ]; then
  [ "${DEBUG}" = "yes" ] && echo "Error: Policy name required as an argument (e.g. targeted)" >> $LOG
  exit
fi

SEMODULEOPT="-s ${1}"
[ "${DEBUG}" = "yes" ] && SEMODULEOPT="-v ${SEMODULEOPT}"

# Take current file_contexts and unify whitespace separators
FILE_CONTEXTS="/etc/selinux/${1}/contexts/files/file_contexts"
FILE_CONTEXTS_UNIFIED="$OUTPUTDIR/file_contexts_unified"
if [ ! -f ${FILE_CONTEXTS} ]; then
  [ "${DEBUG}" = "yes" ] && echo "Error: File context database file does not exist" >> $LOG
  exit
fi

if ! grep -q ^/var/run ${FILE_CONTEXTS}; then
  [ "${DEBUG}" = "yes" ] && echo "Info: No entries containing /var/run" >> $LOG
  exit
fi

EXTRA_VARRUN_ENTRIES_WITHDUP="$OUTPUTDIR/extra_varrun_entries_dup.txt"
EXTRA_VARRUN_ENTRIES="$OUTPUTDIR/extra_varrun_entries.txt"
EXTRA_VARRUN_CIL="$OUTPUTDIR/extra_varrun.cil"

# Print only /var/run entries
grep ^/var/run ${FILE_CONTEXTS} > ${EXTRA_VARRUN_ENTRIES_WITHDUP}

# Unify whitespace separators
sed -i 's/[ \t]\+/ /g' ${EXTRA_VARRUN_ENTRIES_WITHDUP}
sed 's/[ \t]\+/ /g' ${FILE_CONTEXTS} > ${FILE_CONTEXTS_UNIFIED}

# Deduplicate already existing /var/run=/run entries
while read line
do
  subline="${line#/var}"
  if ! grep -q "^${subline}" ${FILE_CONTEXTS_UNIFIED}; then
    echo "$line"
  fi
done < ${EXTRA_VARRUN_ENTRIES_WITHDUP} > ${EXTRA_VARRUN_ENTRIES}

# Change /var/run to /run
sed -i 's|^/var/run|/run|' ${EXTRA_VARRUN_ENTRIES}

# Exception handling: packages with already duplicate entries
sed -i '/^\/run\/snapd/d' ${EXTRA_VARRUN_ENTRIES}
sed -i '/^\/run\/vfrnav/d' ${EXTRA_VARRUN_ENTRIES}
sed -i '/^\/run\/waydroid/d' ${EXTRA_VARRUN_ENTRIES}

# Change format to cil
sed -i 's/^\([^ ]\+\) \([^-]\)/\1 any \2/' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -- /\1 file /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -b /\1 block /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -c /\1 char /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -d /\1 dir /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -l /\1 symlink /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -p /\1 pipe /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) -s /\1 socket /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/^\([^ ]\+\) /(filecon "\1" /' ${EXTRA_VARRUN_ENTRIES}
sed -i 's/system_u:object_r:\([^:]*\):\(.*\)$/(system_u object_r \1 ((\2) (\2))))/' ${EXTRA_VARRUN_ENTRIES}

# Handle entries with <<none>> which do not match previous regexps
sed -i s'/ <<none>>$/ ())/' ${EXTRA_VARRUN_ENTRIES}

# Wrap each line with an optional block
i=1
while read line
do
  echo "(optional extra_var_run_${i}"
  echo "  $line"
  echo ")"
  ((i++))
done < ${EXTRA_VARRUN_ENTRIES} > ${EXTRA_VARRUN_CIL}

# Load module
[ -s ${EXTRA_VARRUN_CIL} ] &&
/usr/sbin/semodule ${SEMODULEOPT} -i ${EXTRA_VARRUN_CIL}

