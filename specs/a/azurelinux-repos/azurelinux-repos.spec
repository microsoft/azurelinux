## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/azurelinux-repos.azl.macros}

# Select between split and unified repo URL layouts.
# Split: repos are under .../base/{$basearch,debuginfo,srpms} (e.g. release builds).
# Unified: repos are directly under .../{$basearch,debuginfo,srpms} (e.g. daily builds).
# Enable with: --with split_repos   (or build.with in comp.toml)
%bcond split_repos 0

Summary:        Azure Linux package repositories
Name:           azurelinux-repos
Version:        4.0
Release:        %autorelease -b 10
License:        MIT
URL:            https://aka.ms/azurelinux

Provides:       azurelinux-repos(%{version}) = %{release}
Requires:       system-release(%{version})
Requires:       azurelinux-gpg-keys >= %{version}-%{release}
BuildArch:      noarch
# Required by %%check
BuildRequires:  gnupg sed rpm

Source1:        archmap
Source2:        azurelinux-unified.repo.in
Source4:        azurelinux-split.repo.in

Source10:       RPM-GPG-KEY-azurelinux-4.0-primary
Source9999: azurelinux-repos.azl.macros


%description
Azure Linux package repository files for yum and dnf along with gpg public keys.

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
# Select stable repo template based on the split_repos knob.
%if %{with split_repos}
install -m 644 %{_sourcedir}/azurelinux-split.repo.in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo
%else
install -m 644 %{_sourcedir}/azurelinux-unified.repo.in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo
%endif

# Enable stable repos.
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=1/" $repo || exit 1
done

# Compute REPO_URI_PREFIX for the stable repo file.
# If repo_uri_prefix macro is explicitly set, use it directly.
# Otherwise, auto-compute from %%dist date stamp (daily-build default).
%if 0%{?repo_uri_prefix:1}
repo_uri_prefix='%{repo_uri_prefix}'
%else
date_segment=$(echo '%{dist}' | grep -oE '[0-9]{8}' || true)
if [ -n "$date_segment" ]; then
    repo_uri_prefix="https://stcontroltowerdevjwisitg.blob.core.windows.net/daily-repo-dev/${date_segment}"
else
    repo_uri_prefix='https://packages.microsoft.com/azurelinux/$releasever/prod/base'
fi
%endif
sed -i "s|REPO_URI_PREFIX|${repo_uri_prefix}|" $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo

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
    if grep -qE 'AUTO_VALUE|REPO_URI_PREFIX' $repo; then
        echo "ERROR: Repo $repo contains an unsubstituted placeholder value"
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

# Check arch keys exists on supported architectures, and RPM considers
# them valid
TMPRING=$(mktemp)
DBPATH=$(mktemp -d)

echo -n > "$TMPRING"
for ARCH in $(sed -ne "s/^azurelinux-%{version}-primary://p" %{_sourcedir}/archmap)
do
gpg --no-default-keyring --keyring="$TMPRING" \
    --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-%{version}-$ARCH
rpm --dbpath "$DBPATH" --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-%{version}-$ARCH --test
done
# Ensure some arch key was imported
gpg --no-default-keyring --keyring="$TMPRING" --list-keys | grep -A 2 '^pub\s'

rm -f "$TMPRING"

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/azurelinux.repo

%files -n azurelinux-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*


%changelog
## START: Generated by rpmautospec
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
