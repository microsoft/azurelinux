%global evergreen_major 5
%global evergreen_release %{evergreen_major}.0

Summary:        Azure Linux package repositories
Name:           azurelinux-repos
Version:        4.0
Release:        3%{?dist}
License:        MIT
URL:            https://aka.ms/azurelinux

Provides:       azurelinux-repos(%{version}) = %{release}
Requires:       system-release(%{version})
%if "%{evergreen_release}" == "%{version}"
Requires:       azurelinux-repos-evergreen = %{version}-%{release}
%endif
Requires:       azurelinux-gpg-keys >= %{version}-%{release}
BuildArch:      noarch
# Required by %%check
BuildRequires:  gnupg sed rpm

Source1:        archmap
Source2:        azurelinux.repo
Source3:        azurelinux-evergreen.repo

Source10:       RPM-GPG-KEY-azurelinux-4.0-primary

# When bumping Evergreen to fN, create N+1 key (and update archmap). (This
# ensures users have the next future key installed and referenced, even if they
# don't update very often. This will smooth out Evergreen N->N+1 transition for them).

# IMA certs: dracut integrity module only recognizes DER format
# TODO(azl): review
# Source500:      azurelinux-ima-ca.der
# Source501:      azurelinux-4.0-ima.der

%description
Azure Linux package repository files for yum and dnf along with gpg public keys.

%package evergreen
Summary:        Evergreen repo definitions
Requires:       azurelinux-repos = %{version}-%{release}

%description evergreen
This package provides the evergreen repo definitions.

%package -n azurelinux-gpg-keys
Summary:        Azure Linux RPM keys
Requires:       filesystem >= 3.18-1

%description -n azurelinux-gpg-keys
This package provides the RPM signature keys.


%prep

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-azurelinux-4.0-primary, and archmap
#     says "azurelinux-4.0-primary: x86_64 aarch64",
#     RPM-GPG-KEY-azurelinux-4.0-{x86_64,aarch64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
# Also add a symlink for Evergreen keys
ln -s RPM-GPG-KEY-azurelinux-%{evergreen_release}-primary RPM-GPG-KEY-azurelinux-evergreen-primary
for keyfile in RPM-GPG-KEY*; do
    # resolve symlinks, so that we don't need to keep duplicate entries in archmap
    real_keyfile=$(basename $(readlink -f $keyfile))
    key=${real_keyfile#RPM-GPG-KEY-} # e.g. 'azurelinux-4.0-primary'
    if ! grep -q "^${key}:" %{_sourcedir}/archmap; then
        echo "ERROR: no archmap entry for $key"
        exit 1
    fi
    arches=$(sed -ne "s/^${key}://p" %{_sourcedir}/archmap)
    for arch in $arches; do
        # replace last part with $arch (azurelinux-4.0-primary -> azurelinux-4.0-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-azurelinux-%{version}-primary RPM-GPG-KEY-%{version}-azurelinux
popd

# Install the IMA certs
# TODO(azl): review
# install -d -m 755 $RPM_BUILD_ROOT/etc/keys/ima
# install -m 644 %{_sourcedir}/azurelinux*ima.der $RPM_BUILD_ROOT/etc/keys/ima/
# install -d -m 755 $RPM_BUILD_ROOT/usr/share/ima/
# install -m 644 %{_sourcedir}/azurelinux-ima-ca.der $RPM_BUILD_ROOT/usr/share/ima/ca.der

# Install repo files
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in %{_sourcedir}/azurelinux*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Enable or disable repos based on current release cycle state.
%if "%{evergreen_release}" == "%{version}"
evergreen_enabled=1
stable_enabled=0
%else
evergreen_enabled=0
stable_enabled=1
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux-evergreen*.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${evergreen_enabled}/" $repo || exit 1
done
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${stable_enabled}/" $repo || exit 1
done

# Update BASE_REPO_URI in azurelinux.repo; compute based on dist tag.
# Extract the last dot-delimited segment from %%dist (e.g. "20260303" from ".azl4~bootstrap.20260303").
# If the segment doesn't contain an 8-digit date, fall back to a hard-coded URI.
date_segment=$(echo '%{dist}' | awk -F. '{print $NF}')
if echo "$date_segment" | grep -qE '[0-9]{8}'; then
    base_repo_uri="https://stcontroltowerdevjwisitg.blob.core.windows.net/daily-repo-non-prod/${date_segment}"
else
    base_repo_uri='https://packages.microsoft.com/azurelinux/$releasever/prod/base'
fi
sed -i "s|BASE_REPO_URI|${base_repo_uri}|" $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo

# Adjust Evergreen repo files to include Evergreen+1 GPG key.
# This is necessary for the period when Evergreen gets bumped to N+1 and packages
# start to be signed with a newer key. Without having the key specified in the
# repo file, the system would consider the new packages as untrusted.
evergreen_next=$((%{evergreen_major}+1)).0
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux-evergreen*.repo; do
    sed -i "/^gpgkey=/ s@AUTO_VALUE@file:///etc/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-${evergreen_next}-\$basearch@" \
        $repo || exit 1
done

# Set appropriate metadata_expire in base repo files (6h before Final, 7d after)
%if "%{release}" < "1"
expire_value='6h'
%else
expire_value='7d'
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    sed -i "/^metadata_expire=/ s/AUTO_VALUE/${expire_value}/" \
        $repo || exit 1
done


%check
# Make sure all repo variables were substituted
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/*.repo; do
    if grep -q AUTO_VALUE $repo; then
        echo "ERROR: Repo $repo contains an unsubstituted placeholder value"
        exit 1
    fi
done

# Make sure correct repos were enabled/disabled
enabled_repos=()
disabled_repos=()

%if "%{evergreen_release}" == "%{version}"
enabled_repos+=(azurelinux-evergreen)
disabled_repos+=(azurelinux)
%else
enabled_repos+=(azurelinux)
disabled_repos+=(azurelinux-evergreen)
%endif

for repo in ${enabled_repos[@]}; do
    if ! grep -q 'enabled=1' $RPM_BUILD_ROOT/etc/yum.repos.d/${repo}.repo; then
        echo "ERROR: Repo $repo should have been enabled, but it isn't"
        exit 1
    fi
done
for repo in ${disabled_repos[@]}; do
    if grep -q 'enabled=1' $RPM_BUILD_ROOT/etc/yum.repos.d/${repo}.repo; then
        echo "ERROR: Repo $repo should have been disabled, but it isn't"
        exit 1
    fi
done

# Make sure metadata_expire was correctly set
%if "%{release}" < "1"
expire_value='6h'
%else
expire_value='7d'
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    lines=$(grep '^metadata_expire=' $repo | sort | uniq)
    if [ "$(echo "$lines" | wc -l)" -ne 1 ]; then
        echo "ERROR: Non-matching metadata_expire lines in $repo: $lines"
        exit 1
    fi
    if test "$lines" != "metadata_expire=${expire_value}"; then
        echo "ERROR: Wrong metadata_expire value in $repo: $lines"
        exit 1
    fi
done

# Make sure the Evergreen+1 key wasn't forgotten to be created
evergreen_next=$((%{evergreen_major}+1)).0
test -n "$evergreen_next" || exit 1
if ! test -f $RPM_BUILD_ROOT/etc/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-${evergreen_next}-primary; then
    echo "ERROR: GPG key for Azure Linux ${evergreen_next} is not present"
    exit 1
fi

# Make sure the Evergreen+1 key is present in Evergreen repo files
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux-evergreen*.repo; do
    gpg_lines=$(grep '^gpgkey=' $repo)
    if test -z "$gpg_lines"; then
        echo "ERROR: No gpgkey= lines in $repo"

        exit 1
    fi
    while IFS= read -r line; do
        if ! echo "$line" | grep -q "RPM-GPG-KEY-azurelinux-${evergreen_next}"; then
            echo "ERROR: Azure Linux ${evergreen_next} GPG key missing in $repo"
            exit 1
        fi
    done <<< "$gpg_lines"
done

# Check arch keys exists on supported architectures, and RPM considers
# them valid
TMPRING=$(mktemp)
DBPATH=$(mktemp -d)
for VER in %{version} %{evergreen_release} ${evergreen_next}; do
  echo -n > "$TMPRING"
  for ARCH in $(sed -ne "s/^azurelinux-${VER}-primary://p" %{_sourcedir}/archmap)
  do
    gpg --no-default-keyring --keyring="$TMPRING" \
      --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-$VER-$ARCH
    rpm --dbpath "$DBPATH" --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-$VER-$ARCH --test
  done
  # Ensure some arch key was imported
  gpg --no-default-keyring --keyring="$TMPRING" --list-keys | grep -A 2 '^pub\s'
done
rm -f "$TMPRING"

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/azurelinux.repo

%files evergreen
%config(noreplace) /etc/yum.repos.d/azurelinux-evergreen.repo


%files -n azurelinux-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*

# ima-certs
# TODO(azl): review
# /etc/keys/ima/azurelinux*ima*
# /usr/share/ima/ca.der


%changelog
* Wed Mar 04 2026 Reuben Olinsky <reubeno@microsoft.com> - 4.0-3
- Update .repo files for initial Alpha release.

* Wed Mar 04 2026 Reuben Olinsky <reubeno@microsoft.com> - 4.0-2
- Update .repo files.

* Fri Jan 23 2026 Reuben Olinsky <reubeno@microsoft.com> - 4.0-1
- Initial definition based on fedora-repos spec (forked from upstream 44-0.1).
