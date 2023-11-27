#!/bin/bash

# Required binaries:
# rpm and dnf

rpms_folder="$1"
repo_file_path="$2"
mariner_version="$3"
sodiff_out_dir="$4"
sodiff_log_file="${sodiff_out_dir}/sodiff.log"

# Setup output dir
mkdir -p "$sodiff_out_dir"

# Prepare mariner/ubuntu compatibility calls

common_options="-c $repo_file_path --releasever $mariner_version"

DNF_COMMAND=dnf
# Cache RPM metadata
>/dev/null dnf $common_options -y makecache

# Get packages from stdin
pkgs=`cat`

for rpmpackage in $pkgs; do
    package_path=$(find "$rpms_folder" -name "$rpmpackage" -type f)
    package_provides=`2>/dev/null rpm -qP "$package_path" | grep -E '[.]so[(.]' `
    echo "Processing ${rpmpackage}..."
    echo ".so's provided: $package_provides"
    for sofile in $package_provides; do
        # Query local metadata for provides
        sos_found=$( 2>/dev/null $DNF_COMMAND repoquery $common_options --whatprovides $sofile | wc -l )
        echo "Number of .so files found: $sos_found"
        if [ "$sos_found" -eq 0 ] ; then
            # SO file not found, meaning this might be a new .SO
            # or a new version of a preexisting .SO.
            # Check if the previous version exists in the database.

            # Remove version part from .SO file
            sofile_no_ver=$(echo "$sofile" | sed -E 's/[.]so[(.].+/.so/')

            # check for generic .so in the repo
            sos_found=$( 2>/dev/null $DNF_COMMAND repoquery $common_options --whatprovides "${sofile_no_ver}*" | wc -l )
            echo "Number of non-versioned .so files found: $sos_found"
            if ! [ "$sos_found" -eq 0 ] ; then
                # Generic version of SO was found.
                # This means it's a new version of a preexisting SO.
                # Log which packages depend on this functionality
                echo "Packages that require $sofile_no_ver:"
                2>/dev/null $DNF_COMMAND repoquery $common_options -s --whatrequires "${sofile_no_ver}*" | sed -E 's/[.][^.]+[.]src[.]rpm//' | tee "$sodiff_out_dir"/"require_${sofile}"
            fi
        fi
    done
    echo ""
done

# Obtain a list of unique packages to be updated
2>/dev/null cat "$sodiff_out_dir"/require* | sort -u > "$sodiff_out_dir"/sodiff-intermediate-summary.txt

rm "$sodiff_out_dir"/require*
touch "$sodiff_out_dir"/sodiff-summary.txt

# Remove packages that have been dash-rolled already.
echo "$pkgs" > "$sodiff_out_dir/sodiff-built-packages.txt"
pkgsFound=0
for package in $( cat "$sodiff_out_dir"/sodiff-intermediate-summary.txt ); do
    # Remove version and release
    package_stem=$(echo "$package" | rev | cut -f1,2 -d'-' --complement | rev)
    # Find a highest version of package built during this run and remove .$ARCH.rpm ending
    highest_build_ver_pkg=$(grep -E "$package_stem-[0-9]" "$sodiff_out_dir"/sodiff-built-packages.txt | sort -Vr | head -n 1 | rev | cut -f1,2,3 -d'.' --complement | rev)

    # Check if versions differ
    if [[ "$package" == "$highest_build_ver_pkg" ]]; then
        # They do not: the version is not dash-rolled - report.
        echo "$highest_build_ver_pkg" >> "$sodiff_out_dir"/sodiff-summary.txt
        ((pkgsFound+=1))
    fi
    # else:
    # the version is higher(dash-rolled) (guaranteed as we are not releasing older packages).
done

rm "$sodiff_out_dir"/sodiff-built-packages.txt

echo "######################"
if [[ $pkgsFound -gt 0 ]]; then
    echo "The Following Packages Are in Need of an Update:"
    cat "$sodiff_out_dir"/sodiff-summary.txt
else
    echo "No Packages with Conflicting .so Files Found."
fi

