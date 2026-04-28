#! /bin/bash
# shellcheck disable=SC2164

rpm_buildroot="$1"
module_dir="$2"
module_list="$3"

blacklist_conf_files="$(mktemp)"

blacklist()
{
	mkdir -p "$rpm_buildroot/etc/modprobe.d/"
	cat > "$rpm_buildroot/etc/modprobe.d/$1-blacklist.conf" <<-__EOF__
	# This kernel module can be automatically loaded by non-root users. To
	# enhance system security, the module is blacklisted by default to ensure
	# system administrators make the module available for use as needed.
	# See https://access.redhat.com/articles/3760101 for more details.
	#
	# Remove the blacklist by adding a comment # at the start of the line.
	blacklist $1
__EOF__
	echo "%config(noreplace) /etc/modprobe.d/$1-blacklist.conf" >> "$blacklist_conf_files"
}

check_blacklist()
{
	mod="$rpm_buildroot/$1"
	[ ! "$mod" ] && return 0
	if modinfo "$mod" | grep -q '^alias:\s\+net-'; then
		mod="${1##*/}"
		mod="${mod%.ko*}"
		echo "$mod has an alias that allows auto-loading. Blacklisting."
		blacklist "$mod"
	fi
}

foreachp()
{
	P=$(nproc)
	bgcount=0
	while read -r mod; do
		$1 "$mod" &

		bgcount=$((bgcount + 1))
		if [ $bgcount -eq "$P" ]; then
			wait -n
			bgcount=$((bgcount - 1))
		fi
	done

	wait
}

# Many BIOS-es export a PNP-id which causes the floppy driver to autoload
# even though most modern systems don't have a 3.5" floppy driver anymore
# this replaces the old die_floppy_die.patch which removed the PNP-id from
# the module

floppylist=("$rpm_buildroot"/"$module_dir"/kernel/drivers/block/floppy.ko*)
if [[ -n ${floppylist[0]} && -f ${floppylist[0]} ]]; then
     blacklist "floppy"
fi

foreachp check_blacklist < "$module_list"

cat "$blacklist_conf_files" >> "$module_list"
rm -f "$blacklist_conf_files"
