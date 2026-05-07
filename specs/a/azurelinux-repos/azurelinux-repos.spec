## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        Azure Linux package repositories
Name:           azurelinux-repos
Version:        4.0
Release:        %autorelease -b 10
License:        MIT
URL:            https://aka.ms/azurelinux

BuildArch:      noarch

# Required by %%check
BuildRequires:  gnupg sed rpm

Source1:        archmap
Source2:        azurelinux.repo.in

Source10:       RPM-GPG-KEY-azurelinux-4.0-primary

# This main package is the default subpackage: official repositories.
# Resolves against packages.microsoft.com; repos and packages are GPG signed.
RemovePathPostfixes: .main
Provides:       azurelinux-repos(%{version}) = %{release}
Requires:       system-release(%{version})
Requires:       azurelinux-gpg-keys >= %{version}-%{release}
Conflicts:      %{name}-dev

%description
This package provides the official Azure Linux yum/dnf repo definitions.

# Alternate subpackage: daily dev repositories. Unsigned; GPG checks disabled.
%package dev
Summary:        Azure Linux development package repository definitions

RemovePathPostfixes: .dev
Provides:       azurelinux-repos(%{version}) = %{release}
Requires:       system-release(%{version})
Requires:       azurelinux-gpg-keys >= %{version}-%{release}
Conflicts:      %{name}

%description dev
This package provides the development Azure Linux yum/dnf repo definitions
that resolve against daily development repositories. Repository
metadata and packages from these repositories are NOT GPG signed; signature
verification is disabled.

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

# Install repo files
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d

# Helper to replace variables in the .repo file template.
render_repo() {
    local outfile="$1" prefix="$2" gpgcheck="$3" repo_gpgcheck="$4" expire="$5"
    install -m 644 %{SOURCE2} "$outfile"
    # Note: REPO_GPGCHECK_VALUE is substituted BEFORE GPGCHECK_VALUE because
    # the latter is a substring of the former — reversing the order would
    # leave a corrupted 'repo_gpgcheck=REPO_<n>_VALUE' line.
    sed -i \
        -e "s|REPO_URI_PREFIX|${prefix}|g" \
        -e "s|REPO_GPGCHECK_VALUE|${repo_gpgcheck}|g" \
        -e "s|GPGCHECK_VALUE|${gpgcheck}|g" \
        -e "s|METADATA_EXPIRE_VALUE|${expire}|g" \
        "$outfile"
}

# Render official .repo file pointing at packages.microsoft.com, signed,
# longer metadata cache. The .main suffix will be removed thanks to
# RemovePathPostfixes.
render_repo \
    "$RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo.main" \
    'https://packages.microsoft.com/azurelinux/$releasever/beta' \
    1 1 '7d'

# Render .repo file pointing at daily dev repos, unsigned, shorter cache.
# The .dev suffix will be removed thanks to RemovePathPostfixes.
render_repo \
    "$RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo.dev" \
    'https://stcontroltowerdevjwisitg.blob.core.windows.net/azl4-dev' \
    0 0 '6h'

%check
# Make sure all repo variables were substituted
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/*.repo.*; do
    if grep -qE 'REPO_URI_PREFIX|GPGCHECK_VALUE|REPO_GPGCHECK_VALUE|METADATA_EXPIRE_VALUE' $repo; then
        echo "ERROR: Repo $repo contains an unsubstituted placeholder value"
        exit 1
    fi
done

main_file=$RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo.main
dev_file=$RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo.dev

# Main repo file must exist with GPG checking enabled on every section.
if [ ! -f "$main_file" ]; then
    echo "ERROR: missing $main_file"
    exit 1
fi
if [ "$(grep -c '^gpgcheck=1' "$main_file")" -ne 3 ] || \
   [ "$(grep -c '^repo_gpgcheck=1' "$main_file")" -ne 3 ]; then
    echo "ERROR: $main_file must enable gpgcheck and repo_gpgcheck on all 3 sections"
    exit 1
fi
if [ "$(grep -c '^metadata_expire=7d' "$main_file")" -ne 3 ]; then
    echo "ERROR: $main_file must have metadata_expire=7d on all 3 sections"
    exit 1
fi

# Dev file must exist with GPG checking disabled on every section.
if [ ! -f "$dev_file" ]; then
    echo "ERROR: missing $dev_file"
    exit 1
fi
if grep -qE '^(gpgcheck|repo_gpgcheck)=1' "$dev_file"; then
    echo "ERROR: $dev_file must not have gpgcheck or repo_gpgcheck enabled"
    exit 1
fi
if [ "$(grep -c '^metadata_expire=6h' "$dev_file")" -ne 3 ]; then
    echo "ERROR: $dev_file must have metadata_expire=6h on all 3 sections"
    exit 1
fi

# Both files must have exactly one enabled=1 section (the base repo) plus
# two enabled=0 sections (debuginfo, source).
for repo in "$main_file" "$dev_file"; do
    if [ "$(grep -c '^enabled=1' "$repo")" -ne 1 ] || \
       [ "$(grep -c '^enabled=0' "$repo")" -ne 2 ]; then
        echo "ERROR: $repo has unexpected enabled-flag distribution"
        exit 1
    fi
done

# Check arch keys exists on supported architectures, and RPM considers
# them valid
TMPRING=$(mktemp)
DBPATH=$(mktemp -d)
echo -n > "$TMPRING"
for ARCH in $(sed -ne "s/^azurelinux-%{version}-primary://p" %{SOURCE1}); do
    gpg --no-default-keyring --keyring="$TMPRING" \
        --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-%{version}-$ARCH
    rpm --dbpath "$DBPATH" --import \
        $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-%{version}-$ARCH --test
done
# Ensure some arch key was imported
gpg --no-default-keyring --keyring="$TMPRING" --list-keys | grep -A 2 '^pub\s' 
rm -f "$TMPRING"

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/azurelinux.repo.main

%files dev
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/azurelinux.repo.dev

%files -n azurelinux-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*


%changelog
## START: Generated by rpmautospec
* Thu May 07 2026 reuben olinsky <reubeno@users.noreply.github.com> - 4.0-15
- refactor(azurelinux-repos): remove repo template for non-split repos

* Thu May 07 2026 reuben olinsky <reubeno@users.noreply.github.com> - 4.0-14
- refactor(azurelinux-repos): remove "evergreen" support

* Thu May 07 2026 reuben olinsky <reubeno@users.noreply.github.com> - 4.0-13
- chore(azurelinux-repos): delete IMA comments

* Thu May 07 2026 reuben olinsky <reubeno@users.noreply.github.com> - 4.0-12
- chore(azurelinux-repos): adopt autorelease

* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 4.0-11
- feat: introduce deterministic commit resolution via Azure Linux lock file

* Thu Jan 01 1970 azldev <> - 4.0-10
- Initial sources
## END: Generated by rpmautospec
