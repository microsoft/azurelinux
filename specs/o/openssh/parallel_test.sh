#!/usr/bin/bash
set -uexo pipefail

# The custom %check script to run the OpenSSH upstream testsuite in parallel.
#
# The upstream testsuite is serial,
# so the idea here is to split the testsuite into several $PARTS:
# * file-tests
# * interop-tests
# * unit
# * ltests-00
# * ltests-01
# * ...
# * ltests-23
# and run them in parallel, using make, each in its own build subtree.

PARALLEL_MAKEFILE=$1

SPLIT=24
PARTS='file-tests interop-tests unit '
for ((i = 1; i < SPLIT; i++)); do ii=$(printf %02d $i);
    PARTS+="t-exec-$ii "
done

# work around a selinux restriction:
chcon -t unconfined_exec_t ssh-sk-helper || :

# work around something else that only crops up in brew
export TEST_SSH_UNSAFE_PERMISSIONS=1

# create a .test directory to store all our files in:
mkdir -p .t .ltests/{in,not-in}

# patch testsuite: use different ports to avoid port collisions
grep -REi 'port=[2-9][0-9]*' regress
sed -i 's|PORT=4242|PORT=$(expr $TEST_SSH_PORT + 1)|' \
    regress/test-exec.sh*
sed -i 's|^P=3301  # test port|P=$(expr $TEST_SSH_PORT + 1)|' \
    regress/multiplex.sh*
sed -i 's|^fwdport=3301|fwdport=$(expr $TEST_SSH_PORT + 1)|' \
    regress/cfgmatch.sh* regress/cfgmatchlisten.sh*
sed -i 's|^LFWD_PORT=.*|LFWD_PORT=$(expr $TEST_SSH_PORT + 1)|' \
    regress/forward-control.sh*
sed -i 's|^RFWD_PORT=.*|RFWD_PORT=$(expr $TEST_SSH_PORT + 2)|' \
    regress/forward-control.sh*
( ! grep -REi 'port=[2-9][0-9]*' regress)  # try to find more of those

# patch testsuite: speed up
sed -i 's|sleep 1$|sleep .25|' regress/forward-control.sh

# extract LTESTS list to .tests/ltests/all:
grep -Ex 'tests:[[:space:]]*file-tests t-exec interop-tests extra-tests unit' Makefile
echo -ne '\necho-ltests:\n\techo ${LTESTS}' >> regress/Makefile
make -s -C regress echo-ltests | tr ' ' '\n' > .ltests/all

# separate ltests into $SPLIT roughly equal .tests/ltests/in/$ii parts:
grep -qFx connect .ltests/all
( ! grep -qFx nonex .ltests/all )
split -d -a2 --number=l/$SPLIT .ltests/all .ltests/in/
wc -l .ltests/in/*
grep -qFx connect .ltests/in/*

# generate the inverses of them --- .ltests/not-in/$ii:
( ! grep -qFx nonex .ltests/in/* )
for ((i = 0; i < SPLIT; i++)); do ii=$(printf %02d $i);
    while read -r tname; do
        if ! grep -qFx "$tname" ".ltests/in/$ii"; then
            echo -n "$tname " >> ".ltests/not-in/$ii"
        fi
    done < .ltests/all
done
grep . .ltests/not-in/*
( ! grep -q ^connect .ltests/not-in/0 )
for ((i = 1; i < SPLIT; i++)); do ii=$(printf %02d $i);
    grep -q ^connect .ltests/not-in/$ii
done

# prepare several test directories:
for PART in $PARTS; do
    mkdir .t/${PART}
    cp -ra * .t/${PART}/
    sed -i "s|abs_top_srcdir=.*|abs_top_srcdir=$(pwd)/.t/${PART}|" \
        .t/${PART}/Makefile
    sed -i "s|abs_top_builddir=.*|abs_top_builddir=$(pwd)/.t/${PART}|" \
        .t/${PART}/Makefile
    sed -i "s|^BUILDDIR=.*|BUILDDIR=$(pwd)/.t/${PART}|" \
        .t/${PART}/Makefile
done

# finally, run tests $PARTS in parallel in their own subtrees:
time make -f "$PARALLEL_MAKEFILE" -j$(nproc) $PARTS
