#!/usr/bin/bash
### binsbin-convert.sh
### convert legacy filecontext entries containing /usr/sbin to /usr/bin
### and load an extra selinux module with the new content
### the script takes a policy name as an argument

# Set DEBUG=yes before running the script to get more verbose output
# on the terminal and to the $LOG file
if [ "${DEBUG}" = "yes" ]; then
  set -x
fi

# Auxiliary and log files will be created in OUTPUTDIR
OUTPUTDIR="/run/selinux-policy"
LOG="$OUTPUTDIR/binsbin-log"
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

if ! grep -q ^/usr/sbin ${FILE_CONTEXTS}; then
  [ "${DEBUG}" = "yes" ] && echo "Info: No entries containing /usr/sbin" >> $LOG
  exit
fi

EXTRA_BINSBIN_ENTRIES_WITHDUP="$OUTPUTDIR/extra_binsbin_entries_dup.txt"
EXTRA_BINSBIN_ENTRIES="$OUTPUTDIR/extra_binsbin_entries.txt"
EXTRA_BINSBIN_CIL="$OUTPUTDIR/extra_binsbin.cil"
EXTRA_BINSBIN_MODULE="extra_binsbin"

# Print only /usr/sbin entries
grep ^/usr/sbin ${FILE_CONTEXTS} > ${EXTRA_BINSBIN_ENTRIES_WITHDUP}

# Unify whitespace separators
sed -i 's/[ \t]\+/ /g' ${EXTRA_BINSBIN_ENTRIES_WITHDUP}
sed 's/[ \t]\+/ /g' ${FILE_CONTEXTS} > ${FILE_CONTEXTS_UNIFIED}

# Deduplicate already existing /usr/bin=/usr/sbin entries
while read line
do
  subline="/usr/bin/${line#/usr/sbin/}"
  if ! grep -q "^${subline}" ${FILE_CONTEXTS_UNIFIED}; then
    echo "$line"
  fi
done < ${EXTRA_BINSBIN_ENTRIES_WITHDUP} > ${EXTRA_BINSBIN_ENTRIES}

# Change /usr/sbin to /usr/bin
sed -i 's|^/usr/sbin|/usr/bin|' ${EXTRA_BINSBIN_ENTRIES}

# Exception handling: types changed during the same transaction
sed -i '/^\/usr\/bin\/tlshd/d' ${EXTRA_BINSBIN_ENTRIES}
sed -i '/^\/usr\/bin\/pcm-sensor-server/d' ${EXTRA_BINSBIN_ENTRIES}

# Change format to cil
sed -i 's/^\([^ ]\+\) \([^-]\)/\1 any \2/' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -- /\1 file /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -b /\1 block /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -c /\1 char /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -d /\1 dir /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -l /\1 symlink /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -p /\1 pipe /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) -s /\1 socket /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/^\([^ ]\+\) /(filecon "\1" /' ${EXTRA_BINSBIN_ENTRIES}
sed -i 's/system_u:object_r:\([^:]*\):\(.*\)$/(system_u object_r \1 ((\2) (\2))))/' ${EXTRA_BINSBIN_ENTRIES}

# Handle entries with <<none>> which do not match previous regexps
sed -i s'/ <<none>>$/ ())/' ${EXTRA_BINSBIN_ENTRIES}

# Wrap each line with an optional block
i=1
while read line
do
  echo "(optional extra_binsbin_${i}"
  echo "  $line"
  echo ")"
  ((i++))
done < ${EXTRA_BINSBIN_ENTRIES} > ${EXTRA_BINSBIN_CIL}

# Load module
if [ -s ${EXTRA_BINSBIN_CIL} ]; then
  semodule -l |grep -qw ${EXTRA_BINSBIN_MODULE} && semodule -Nr ${EXTRA_BINSBIN_MODULE}
  semodule ${SEMODULEOPT} -i ${EXTRA_BINSBIN_CIL}
fi

