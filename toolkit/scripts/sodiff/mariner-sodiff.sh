#!/bin/bash

# Required binaries:
# rpm and dnf on Mariner
# yum and yum-utils on Ubuntu

rpms_folder="$1"
repo_file_path="$2"
mariner_version="$3"
sodiff_out_dir="$4"
sodiff_log_file="${sodiff_out_dir}/sodiff.log"
current_os=$(cat /etc/os-release | grep ^ID | cut -d'=' -f2)
temporary_repo_file="file.repo"

# Setup output dir
mkdir -p "$sodiff_out_dir"
# Empty the log file
echo > "$sodiff_log_file"

function makecache_with_common {
    if [[ "$current_os" == mariner ]]; then
        # Mariner uses DNF repoquery command
        DNF_COMMAND=dnf
        # Cache RPM metadata
        >/dev/null dnf $common_options -y makecache
    else
        # Ubuntu uses repoquery command from yum-utils
        DNF_COMMAND=
        # Cache RPM metadata
        # Ubuntu does not come with gpgcheck plugin for yum
        >/dev/null yum $common_options -y --nogpgcheck makecache
    fi
}

function log_to_file {
    >>$sodiff_log_file echo -- $@
}

# Split the abridged repo file and process each repo separately
# because if any of the repos is not accessible,
# creating cache for the whole .repo file fails.
# However, created caches accumulate, so creating multiple caches
# will not overwrite each other and any failures can be safely ignored

# Flag to track running cache creation for the first match of repo header - skip since repo file not created yet
firstmatch=1
# Make common options point to the temporary repo file for now
common_options="-c $temporary_repo_file --releasever $mariner_version"
# IFS= prevents read from omitting leading/trailing whitespace
# -r prevents read from interpreting backslash escapes
while IFS= read -r line
do
    # If this is a start of a new repo definition
    if grep -Eq "^\[[^]]+\]$" <<<"$line" ; then
        # Do not run the operation on first match - repo file not filled yet
        if [[ "$firstmatch" -eq 1 ]]; then
            firstmatch=0
        else
            # Execute operation on the previous .repo file before proceeding with new one
            makecache_with_common
            echo ""
        fi
        log_to_file "Preparing cache for repo $line"
        # Overwrite line to a repo file
        printf '%s\n' "$line" > $temporary_repo_file
    else
        # Append line to a repo file
        printf '%s\n' "$line" >> $temporary_repo_file
    fi
done < "$repo_file_path"
# Run operation again for the final repo
# In case repo file has only one repo definition, the command will
# run twice on the same repo, but this is fine.
makecache_with_common

# Cache created - now we can point to the abridged file.
common_options="-c $repo_file_path --releasever $mariner_version"

log_to_file "Cache created."

# Get packages from stdin
pkgs=`cat`

# Get a list of files requires_SOFILE where SOFILE is a name of a .so file that did not have a remote equivalent (SO that have been updated during this build but not released yet)
# And its contents are the names of packages that depend upon that SOFILE (candidates for a rebuild)

for rpmpackage in $pkgs; do
    package_path=$(find "$rpms_folder" -name "$rpmpackage" -type f)
    package_provides=`2>/dev/null rpm -qP "$package_path" | grep -E '[.]so[(.]' `
    log_to_file ""
    log_to_file "Processing ${rpmpackage}..."
    # Check every sofile provided by the rpm.
    for sofile in $package_provides; do
        # See if any package in the remote repositories provides this sofile yet.
        sos_found=$( $DNF_COMMAND repoquery $common_options --whatprovides $sofile | wc -l )
        if [ "$sos_found" -eq 0 ] ; then

            log_to_file "Sofile $sofile not found remotely. It is either new so or a new version of preexisting sofile. "
            # SO file not found, meaning this might be a new .SO
            # or a new version of a preexisting .SO.
            # Check if the previous version exists in the database.

            # Remove version part from .SO file
            sofile_no_ver=$(echo "$sofile" | sed -E 's/[.]so[(.].+/.so/')

            # check for generic .so in the repo
            sos_found=$( $DNF_COMMAND repoquery $common_options --whatprovides "${sofile_no_ver}*" | wc -l )

            if ! [ "$sos_found" -eq 0 ] ; then
                log_to_file "Generic version of $sofile - $sofile_no_ver provided remotely, but $sofile_no_ver is not. This might be a new version of a so file."
                # Generic version of SO was found.
                # This means it's a new version of a preexisting SO.
                # Log which packages depend on this functionality
                $DNF_COMMAND repoquery $common_options -s --whatrequires "${sofile_no_ver}*" | sed -E 's/[.][^.]+[.]src[.]rpm//' > "$sodiff_out_dir"/"require_${sofile}"
            fi
        fi
    done
done

# Obtain a list of unique packages to be updated
2>/dev/null cat "$sodiff_out_dir"/require* | sort -u > "$sodiff_out_dir"/sodiff-intermediate-summary.txt
rm -f "$sodiff_out_dir"/sodiff-summary.txt
echo "$pkgs" > "$sodiff_out_dir/sodiff-built-packages.txt"

# Remove packages that have been updated already.
for package in $( cat "$sodiff_out_dir"/sodiff-intermediate-summary.txt ); do
    # Remove version and release
    package_stem=$(echo "$package" | rev | cut -f1,2 -d'-' --complement | rev)
    log_to_file "Processing a potential candidate for update - $package_stem (${package})"
    # Find a highest version of package built during this run and remove .$ARCH.rpm ending
    highest_build_ver_pkg=$(grep -E "$package_stem-[0-9]" "$sodiff_out_dir"/sodiff-built-packages.txt | sort -Vr | head -n 1 | rev | cut -f1,2,3 -d'.' --complement | rev)
    # Check if versions differ
    if [[ "$package" == "$highest_build_ver_pkg" ]]; then
        # They do not: the version is not dash-rolled - report.
        log_to_file "Potential candidate $package is the same as the remote one. Update needed."
        echo "$highest_build_ver_pkg" >> "$sodiff_out_dir"/sodiff-summary.txt
    fi
    # else:
    # the version is higher(dash-rolled) (guaranteed as we are not releasing older packages).
done

rm "$sodiff_out_dir"/sodiff-built-packages.txt
