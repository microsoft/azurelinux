#!/bin/bash
#
# This script add IMA signatures to installed RPM package files
usage() {
	echo "Add IMA signatures to installed packages."
	cat <<EOF
usage: $0 [--package=PACKAGE_NAME|ALL] [--ima_cert=IMA_CERT_PATH] [--reinstall_threshold=NUM]

       --package
       By default, it will add IMA sigantures to all installed package files.
       Or you can provide a package name to only add IMA signature for files of
       specicifed package.

       --reinstall_threshold
       When there are >reinstall_threshold (=20 by default) packages in the RPM
       DB missing IMA signatures, reinstalling the packages to add IMA
       signatures to the packages.  By default, IMA sigatures will be obtained
       from the RPM DB. However the RPM DB may not have the signatures. Dectect
       this case by checking if there are >reinstall_threshold package missing
       IMA signatures.

       --ima_cert
       With the signing IMA cert path specified, it will also try to verify the
       added IMA signature.

EOF
	exit 1
}

for _opt in "$@"; do
	case "$_opt" in
	--reinstall_threshold=*)
		reinstall_threshold=${_opt#*=}
		;;
	--package=*)
		package=${_opt#*=}
		;;
	--ima_cert=*)
		ima_cert=${_opt#*=}
		;;
	*)
		[[ -n $1 ]] && usage
		;;
	esac
done

if [[ -z $package ]] || [[ $package == ALL ]]; then
	package="--all"
fi

abort() {
	echo "$1"
	exit 1
}

get_system_ima_key() {
	source /etc/os-release
	local -A name_map=(['Fedora Linux']="fedora" ['Red Hat Enterprise Linux']="redhatimarelease" ['CentOS Stream']='centosimarelease')
	local version_id
	key_name=${name_map[$NAME]}
	version_id=${VERSION_ID/.?/}

	[[ $key_name == fedora ]] && name_suffix=-ima
	key_path=/etc/keys/ima/${key_name}-${version_id}${name_suffix}.der
	if [[ ! -e $key_path ]]; then
		echo "Failed to get system IMA code verification key"
		exit 1
	fi

	echo -n "$key_path"
}

# Add IMA signatures from RPM database
add_from_rpm_db() {
	if ! command -v setfattr &>/dev/null; then
		abort "Please install attr"
	fi

	if [[ -e "$ima_cert" ]]; then
		verify_ima_cert=$ima_cert
	else
		verify_ima_cert=$(get_system_ima_key)
	fi

	# use "|" as deliminator since it won't be used in a filename or signature
	while IFS="|" read -r path sig; do
		# [[ -z "$sig" ]] somehow doesn't work for some files that don't have IMA
		# signatures. This may be a issue of rpm
		if [[ "$sig" != "0"* ]]; then
			continue
		fi

		# Skip directory, soft links, non-existent files and vfat fs
		if [[ -d "$path" || -L "$path" || ! -f "$path" || "$path" == "/boot/efi/EFI/"* ]]; then
			continue
		fi

		# Skip some files that are created on the fly
		if [[ $path == "/usr/share/mime/"* || $path == "/etc/pki/ca-trust/extracted/"* ]]; then
			continue
		fi

		if ! setfattr -n security.ima "$path" -v "0x$sig"; then
			echo "Failed to add IMA sig for $path"
		fi

		if ! evmctl ima_verify -k "$verify_ima_cert" "$path" &>/dev/null; then
			setfattr -x security.ima "$path"
			# When ima_cert is set, shows the verfication result for users
			[[ -e "$ima_cert" ]] && "Failed to verify $path"
			continue
		fi

	done < <(rpm -q --queryformat "[%{FILENAMES}|%{FILESIGNATURES}\n]" "$package")
}

# Add IMA signatures by reinstalling all packages
add_by_reinstall() {
	[[ $package == "--all" ]] && package='*'
	dnf reinstall "$package" -yq >/dev/null
}

if [[ -z $reinstall_threshold ]]; then
	if [[ $package == "--all" ]]; then
		reinstall_threshold=20
	else
		if ! rpm -q --quiet "$package"; then
			dnf install "$package" -yq >/dev/null
			exit 0
		fi
		reinstall_threshold=1
	fi
fi

unsigned_packages_in_rpm_db=$(rpm -q --queryformat "%{SIGPGP:pgpsig}\n" "$package" | grep -c "^(none)$")

if [[ $unsigned_packages_in_rpm_db -ge $reinstall_threshold ]]; then
	add_by_reinstall
else
	add_from_rpm_db
fi
