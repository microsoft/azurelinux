#!/bin/bash
#
# This script takes the merged config files and processes them through olddefconfig
# and listnewconfig to ensure kernel configurations are valid and complete.
#
# Globally disable suggestion of appending '|| exit' or '|| return' to cd/pushd/popd commands
# shellcheck disable=SC2164

# Exit if this is a test environment
test -n "$RHTEST" && exit 0

# Display usage information and available command line options
usage()
{
	# alphabetical order please
	echo "process_configs.sh [ options ] package_name kernel_version"
	echo "     -a: report all errors, equivalent to [-c -n -w -i]"
	echo "     -c: error on mismatched config options"
	echo "     -i: ignore any errors, but print them"
	echo "     -m: specify make options (e.g., -m CC=clang, -m LLVM=1)"
	echo "     -M: commit mismatched configs to pending directory"
	echo "     -n: error on unset config options"
	echo "     -t: test run, do not overwrite original config"
	echo "     -w: error on misconfigured config options"
	echo "     -z: commit new configs to pending directory"
	echo ""
	echo "     A special CONFIG file tag, process_configs_known_broken can be added as a"
	echo "     comment to any CONFIG file.  This tag indicates that there is no way to "
	echo "     fix a CONFIG's entry.  This tag should only be used in extreme cases"
	echo "     and is not to be used as a workaround to solve CONFIG problems."
	exit 1
}

die()
{
	echo "$1"
	exit 1
}

# Determine the correct cross-compiler prefix based on compiler type
# For clang builds, return the architecture directly
# For GCC builds, use the dummy-tools directory
get_cross_compile()
{
	arch=$1
	if [[ "$CC_IS_CLANG" -eq 1 ]]; then
		echo "$arch"
	else
		echo "scripts/dummy-tools/"
	fi
}

# Find the top-level kernel source directory
# (identified by MAINTAINERS file and drivers directory)
switch_to_toplevel()
{
	path="$(pwd)"
	while test -n "$path"
	do
		test -e "$path"/MAINTAINERS && \
			test -d "$path"/drivers && \
			break

		path=$(dirname "$path")
	done

	test -n "$path"  || die "Can't find toplevel"
	echo "$path"
}

# Determine the correct config path based on architecture and variant
# This function maps arch/variant combinations to the proper pending directory
determine_config_path()
{
	local arch="$1"
	local variant="$2"
	local config_path=""

	# Identify the variant - they have their own top-level directories
	if [[ "$variant" == *"rt"* ]]; then
		# RT variant - goes under rt/
		if [[ "$variant" == *"debug"* ]]; then
			config_path="rt/debug"
		else
			config_path="rt/generic"
		fi
	elif [[ "$variant" == *"automotive"* ]]; then
		# Automotive variant - goes under automotive/
		if [[ "$variant" == *"debug"* ]]; then
			config_path="automotive/debug"
		else
			config_path="automotive/generic"
		fi
	else
		# Stock kernel - goes under top-level debug or generic
		if [[ "$variant" == *"debug"* ]]; then
			config_path="debug"
		else
			config_path="generic"
		fi
	fi

	# Add architecture-specific subdirectories
	case "$arch" in
		arm64)
			config_path="$config_path/arm/aarch64"
			;;
		powerpc)
			config_path="$config_path/powerpc"
			;;
		riscv)
			config_path="$config_path/riscv/riscv64"
			;;
		s390)
			if [[ "$variant" == *"zfcpdump"* ]]; then
				config_path="$config_path/s390x/zfcpdump"
			else
				config_path="$config_path/s390x"
			fi
			;;
		x86_64)
			config_path="$config_path/x86"
			;;
		*)
			# For unknown architectures, don't add arch subdirectory
			;;
	esac

	echo "$config_path"
}

# Parse mismatched configs found during processing and create
# individual CONFIG files in the pending directory for each
parse_mismatched_configs()
{
	local tmpdir
	local count=$1    # Counter for unique filenames
	local arch=$2
	local variant=$3

	tmpdir=$(mktemp -d)

	# Parse the mismatches file and create individual CONFIG files
	tail -n +2 .mismatches"${count}" | while read -r LINE
	do
		if echo "$LINE" | grep -q "Found # .* is not set, after generation"; then
			# Handle case where we found "# CONFIG_FOO is not set" after generation
			config_name="${LINE#*Found # }"
			config_name="${config_name% is not set, after generation*}"
			if [ -n "$config_name" ]; then
				echo "# Mismatch found in $arch $variant config" > "$tmpdir/$config_name"
				echo "# $config_name is not set" >> "$tmpdir/$config_name"
			fi
		elif echo "$LINE" | grep -q "Found .* after generation"; then
			# Handle case where we found "CONFIG_FOO=value" after generation
			config_name="${LINE#*Found }"
			config_name="${config_name% after generation*}"
			config_name="${config_name%=*}"
			config_value="${LINE#*Found }"
			config_value="${config_value#*=}"
			config_value="${config_value% after generation*}"
			if [ -n "$config_name" ] && [ -n "$config_value" ]; then
				echo "# Mismatch found in $arch $variant config" > "$tmpdir/$config_name"
				echo "$config_name=$config_value" >> "$tmpdir/$config_name"
			fi
		fi
	done

	# Copy the CONFIG files to the pending directory
	config_path=$(determine_config_path "$arch" "$variant")
	mkdir -p "$SCRIPT_DIR/pending-$FLAVOR/$config_path/"
	for f in "$tmpdir"/*; do
		[[ -e "$f" ]] || break
		cp "$f" "$SCRIPT_DIR/pending-$FLAVOR/$config_path/"
	done

	rm -rf "$tmpdir"
}

# Check for configuration mismatches between the original and generated configs
checkoptions()
{
	cfg=$1      # Original config file
	cfgtmp=$2   # Generated config file
	count=$3    # Counter for unique filenames
	variant=$4  # Config variant (e.g., debug, rt)

	# This awk script compares configuration files for mismatches
	/usr/bin/awk '

		/is not set/ {
			split ($0, a, "#");
			split(a[2], b);
			if (NR==FNR) {
				configs[b[1]]="is not set";
			} else {
				if (configs[b[1]] != "" && configs[b[1]] != "is not set")
					 print "Found # "b[1] " is not set, after generation, had " b[1] " " configs[b[1]] " in Source tree";
			}
		}

		/=/     {
			split ($0, a, "=");
			if (NR==FNR) {
				configs[a[1]]=a[2];
			} else {
				if (configs[a[1]] != "" && configs[a[1]] != a[2])
					 print "Found "a[1]"="a[2]" after generation, had " a[1]"="configs[a[1]]" in Source tree";
			}
		}
	' "$cfg" "$cfgtmp" > .mismatches"${count}"

	checkoptions_error=false
	if test -s .mismatches"${count}"
	then
		while read -r LINE
		do
			if find "${REDHAT}"/configs -name "$(echo "$LINE" | awk -F "=" ' { print $1 } ' | awk ' { print $2 }')" -print0 | xargs -0 grep ^ | grep -q "process_configs_known_broken"; then
				# This is a known broken config.
				# See script help warning.
				checkoptions_error=false
			else
				checkoptions_error=true
				break
			fi
		done < .mismatches"${count}"

		! $checkoptions_error && return

		sed -i "1s/^/Error: Mismatches found in configuration files for ${arch} ${variant}\n/" .mismatches"${count}"

		# Add mismatched configs to the pending directory
		if test -n "$COMMITMISMATCHES"; then
			parse_mismatched_configs "$count" "$arch" "$variant"
		fi
	else
		rm -f .mismatches"${count}"
	fi
}

# Parse the output of 'make listnewconfig' and 'make helpnewconfig'
# to create properly formatted configuration files for new configs
parsenewconfigs()
{
	tmpdir=$(mktemp -d)

	# This awk script reads the output of make listnewconfig
	# and puts it into CONFIG_FOO files. Using the output of
	# listnewconfig is much easier to ensure we get the default
	# output.
        /usr/bin/awk -v BASE="$tmpdir" '
                /is not set/ {
                        split ($0, a, "#");
                        split(a[2], b);
                        OUT_FILE=BASE"/"b[1];
                        print $0 >> OUT_FILE;
                }

                /=/     {
                        split ($0, a, "=");
                        OUT_FILE=BASE"/"a[1];
                        if (a[2] == "n")
                                print "# " a[1] " is not set" >> OUT_FILE;
                        else
                                print $0 >> OUT_FILE;
                }

        ' .newoptions

	# This awk script parses the output of helpnewconfig.
	# Each option is separated between ----- markers
	# The goal is to put all the help text as a comment in
	# each CONFIG_FOO file. Because of how awk works
	# there's a lot of moving files around and catting to
	# get what we need.
        /usr/bin/awk -v BASE="$tmpdir" '
                BEGIN { inpatch=0;
			outfile="none";
                        symbol="none";
                        commit=""; }
                /^Symbol: .*$/ {
                        split($0, a, " ");
                        symbol="CONFIG_"a[2];
                        outfile=BASE "/fake_"symbol
                        print "# ~~~" >> outfile;
                }
                /-----/ {
			if (inpatch == 0) {
				inpatch = 1;
			}
                        else {
                                print "# ~~~" >> outfile;
                                if (symbol != "none") {
                                    print "# Commit: "commit >> outfile
                                    system("cat " outfile " " BASE "/" symbol " > " BASE "/tmpf");
                                    system("mv " BASE "/tmpf " BASE "/" symbol);
                                    symbol="none"
                                    commit=""
				}
                                outfile="none"
				inpatch = 0;
                        }
                }
                !/-----/ {
                        if (inpatch == 1 && outfile != "none") {
                                print "# "$0 >> outfile;
                        }
                }
                /^Defined at .*$/ {
                        split($0, x, " ");
                        filenum=x[3];
                        split(filenum, x, ":");
                        file=x[1]
                        line=x[2]
                        cmd="git blame -L " line "," line " " file " | cut -d \" \" -f1 | xargs git log --pretty=format:\"%C(auto)%h %C(cyan)('%s')\" -1"
                        cmd | getline commit
                }


        ' .helpnewconfig

	pushd "$tmpdir" &> /dev/null
	rm fake_*
	popd &> /dev/null
	for f in "$tmpdir"/*; do
		[[ -e "$f" ]] || break
		cp "$f" "$SCRIPT_DIR/pending-$FLAVOR/generic/"
	done

	rm -rf "$tmpdir"
}

# Commit any mismatched configs that were saved to the pending directory
commit_mismatched_configs()
{
	# assume we are in $source_tree/configs, need to get to top level
	pushd "$(switch_to_toplevel)" &>/dev/null

	# Check if there are any modified or untracked mismatched configs to commit
	if git status --porcelain "$SCRIPT_DIR/pending-$FLAVOR/" | grep -q .; then
		echo "Committing mismatched configuration files..."
		git add "$SCRIPT_DIR/pending-$FLAVOR"
		git commit -m "[redhat] AUTOMATIC: Mismatched $FLAVOR configs"
		echo "Mismatched configs committed to pending-$FLAVOR directory"
	else
		echo "No mismatched configs found to commit"
	fi

	popd &>/dev/null
}

# Processes all config files, finds new/unset configs, and commits them
function commit_new_configs()
{
	# assume we are in $source_tree/configs, need to get to top level
	pushd "$(switch_to_toplevel)" &>/dev/null

	for cfg in "$SCRIPT_DIR/${SPECPACKAGE_NAME}${KVERREL}"*.config
	do
		arch=$(head -1 "$cfg" | cut -b 3-)
		cfgtmp="${cfg}.tmp"
		cfgorig="${cfg}.orig"
		cat "$cfg" > "$cfgorig"

		if [ "$arch" = "EMPTY" ]
		then
			# This arch is intentionally left blank
			continue
		fi
		echo -n "Checking for new configs in $cfg ... "

		# shellcheck disable=SC2086
		make ${MAKEOPTS} ARCH="$arch" CROSS_COMPILE="$(get_cross_compile "$arch")" KCONFIG_CONFIG="$cfgorig" listnewconfig >& .listnewconfig
		grep -E 'CONFIG_' .listnewconfig > .newoptions
		if test -s .newoptions
		then
		# shellcheck disable=SC2086
			make ${MAKEOPTS} ARCH="$arch" CROSS_COMPILE="$(get_cross_compile "$arch")" KCONFIG_CONFIG="$cfgorig" helpnewconfig >& .helpnewconfig
			parsenewconfigs
		fi
		rm .newoptions
		echo "done"
	done

	# Commit the new configuration files to git
	git add "$SCRIPT_DIR/pending-$FLAVOR"
	# DO NOT CHANGE THIS MESSAGE! gen_config_patches.sh looks for this commit message.
	git commit -m "[redhat] AUTOMATIC: New configs"
}

# Process a single configuration file
function process_config()
{
	local cfg
	local arch
	local cfgtmp
	local cfgorig
	local count
	local variant

	cfg=$1
	count=$2

	arch=$(head -1 "$cfg" | cut -b 3-)

	if [ "$arch" = "EMPTY" ]
	then
		# This arch is intentionally left blank
		return
	fi

	variant=$(basename "$cfg" | cut -d"-" -f3- | cut -d"." -f1)

	cfgtmp="${cfg}.tmp"
	cfgorig="${cfg}.orig"
	cat "$cfg" > "$cfgorig"

	echo "Processing $cfg ... "

	# shellcheck disable=SC2086
	make ${MAKEOPTS} ARCH="$arch" CROSS_COMPILE="$(get_cross_compile "$arch")" KCONFIG_CONFIG="$cfgorig" listnewconfig >& .listnewconfig"${count}"
	grep -E 'CONFIG_' .listnewconfig"${count}" > .newoptions"${count}"
	if test -n "$NEWOPTIONS" && test -s .newoptions"${count}"
	then
		echo "Found unset config items in ${arch} ${variant}, please set them to an appropriate value" >> .errors"${count}"
		cat .newoptions"${count}" >> .errors"${count}"
		rm .newoptions"${count}"
		RETURNCODE=1
	fi
	rm -f .newoptions"${count}"

	grep -E 'config.*warning' .listnewconfig"${count}" > .warnings"${count}"
	if test -n "$CHECKWARNINGS" && test -s .warnings"${count}"
	then
		echo "Found misconfigured config items in ${arch} ${variant}, please set them to an appropriate value" >> .errors"${count}"
		cat .warnings"${count}" >> .errors"${count}"
	fi
	rm .warnings"${count}"

	rm .listnewconfig"${count}"

	# shellcheck disable=SC2086
	make ${MAKEOPTS} ARCH="$arch" CROSS_COMPILE="$(get_cross_compile "$arch")" KCONFIG_CONFIG="$cfgorig" olddefconfig > /dev/null || exit 1
	echo "# $arch" > "$cfgtmp"
	cat "$cfgorig" >> "$cfgtmp"
	if test -n "$CHECKOPTIONS"
	then
		checkoptions "$cfg" "$cfgtmp" "$count" "$variant"
	fi
	# if test run, don't overwrite original
	if test -n "$TESTRUN"
	then
		rm -f "$cfgtmp"
	else
		mv "$cfgtmp" "$cfg"
	fi
	rm -f "$cfgorig"
	echo "Processing $cfg complete"
}

# Process all configuration files
# Handles parallel processing and error reporting
function process_configs()
{
	# assume we are in $source_tree/configs, need to get to top level
	pushd "$(switch_to_toplevel)" &>/dev/null

	count=0
	for cfg in "$SCRIPT_DIR/${SPECPACKAGE_NAME}${KVERREL}"*.config
	do
		if [ "$count" -eq 0 ]; then
			# do the first one by itself so that tools are built
			process_config "$cfg" "$count"
		fi
		process_config "$cfg" "$count" &
		# shellcheck disable=SC2004
		waitpids[${count}]=$!
		((count++))
		while [ "$(jobs | grep -c Running)" -ge "$RHJOBS" ]; do :; done
	done
	# shellcheck disable=SC2048
	for pid in ${waitpids[*]}; do
		wait "${pid}"
	done

	rm "$SCRIPT_DIR"/*.config*.old

	if ls .errors* 1> /dev/null 2>&1; then
		RETURNCODE=1
		cat .errors*
		rm .errors* -f
	fi

	# Commit any mismatched configs found during processing
	if [ $RETURNCODE -eq 0 ] && test -n "$COMMITMISMATCHES"; then
		rm .mismatches* -f
		commit_mismatched_configs
	# Otherwise, display any mismatched configs
	elif ls .mismatches* 1> /dev/null 2>&1; then
		RETURNCODE=1
		cat .mismatches*
		rm .mismatches* -f
	fi

	popd > /dev/null

	[ $RETURNCODE -eq 0 ] && echo "Processed config files are in $SCRIPT_DIR"
}

CHECKOPTIONS=""
IGNOREERRORS=""
NEWOPTIONS=""
TESTRUN=""
CHECKWARNINGS=""
MAKEOPTS=""
CC_IS_CLANG=0
COMMITMISMATCHES=""

RETURNCODE=0

while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		-a)
			# Enable all error checking options
			CHECKOPTIONS="x"
			IGNOREERRORS="x"
			NEWOPTIONS="x"
			CHECKWARNINGS="x"
			;;
		-c)
			CHECKOPTIONS="x"
			;;
		-h)
			usage
			;;
		-i)
			IGNOREERRORS="x"
			;;
		-n)
			NEWOPTIONS="x"
			;;
		-t)
			TESTRUN="x"
			;;
		-w)
			CHECKWARNINGS="x"
			;;
		-z)
			COMMITNEWCONFIGS="x"
			;;
		-m)
			shift
			# Handle clang compiler options
			if [ "$1" = "CC=clang" ] || [ "$1" = "LLVM=1" ]; then
				CC_IS_CLANG=1
			fi
			MAKEOPTS="$MAKEOPTS $1"
			;;
		-M)
			COMMITMISMATCHES="x"
			CHECKOPTIONS="x"
			;;
		*)
			break;;
	esac
	shift
done

KVERREL="$(test -n "$1" && echo "-$1" || echo "")"
FLAVOR="$(test -n "$2" && echo "$2" || echo "rhel")"
# shellcheck disable=SC2015
SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")

# to handle this script being a symlink
cd "$SCRIPT_DIR"

if test -n "$COMMITNEWCONFIGS"; then
	commit_new_configs
else
	process_configs
fi

if test -n "$IGNOREERRORS"; then
	exit 0
else
	exit $RETURNCODE
fi
