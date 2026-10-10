#! /bin/bash

# The modules_sign target checks for corresponding .o files for every .ko that
# is signed. This doesn't work for package builds which re-use the same build
# directory for every variant, and the .config may change between variants.
# So instead of using this script to just sign lib/modules/$KernelVer/extra,
# sign all .ko in the buildroot.

# This essentially duplicates the 'modules_sign' Kbuild target and runs the
# same commands for those modules.

MODSECKEY=$1
MODPUBKEY=$2
moddir=$3

modules=$(find "$moddir" -type f -name '*.ko')

NPROC=$(nproc)
[ -z "$NPROC" ] && NPROC=1

# NB: this loop runs 2000+ iterations. Try to be fast.
echo "$modules" | xargs -r -n16 -P "$NPROC" sh -c "
for mod; do
    ./scripts/sign-file sha256 $MODSECKEY $MODPUBKEY \$mod
    rm -f \$mod.sig \$mod.dig
done
" DUMMYARG0   # xargs appends ARG1 ARG2..., which go into $mod in for loop.

RANDOMMOD=$(echo "$modules" | sort -R | head -n 1)
if [ "~Module signature appended~" != "$(tail -c 28 "$RANDOMMOD")" ]; then
    echo "*****************************"
    echo "*** Modules are unsigned! ***"
    echo "*****************************"
    exit 1
fi

exit 0
