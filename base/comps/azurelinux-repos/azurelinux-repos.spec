Summary:        Azure Linux package repositories
Name:           azurelinux-repos
Version:        4.0
Release:        %autorelease -b 10
License:        MIT
URL:            https://aka.ms/azurelinux

BuildArch:      noarch

# Required by %%check
BuildRequires:  gnupg rpm

Source1:        archmap
Source2:        azurelinux.repo
Source3:        azurelinux-preview.repo
Source4:        cloud-native.repo
Source5:        cloud-native-preview.repo
Source6:        microsoft.repo
Source7:        microsoft-preview.repo

Source10:       RPM-GPG-KEY-azurelinux-4.0-primary

Provides:       azurelinux-repos(%{version}) = %{release}
Requires:       system-release(%{version})
Requires:       azurelinux-gpg-keys >= %{version}-%{release}
Obsoletes:      %{name}-dev < %{version}-%{release}

%description
This package provides the production and preview Azure Linux yum/dnf repo
definitions. Production binary repositories are enabled by default; preview
repositories are temporarily enabled until production repositories are fully
populated; source and debuginfo repositories are disabled by default.

%package -n azurelinux-gpg-keys
Summary:        Azure Linux RPM keys
Requires:       filesystem >= 3.18-1

%description -n azurelinux-gpg-keys
This package provides the RPM signature keys.

%prep

%build

%install
# Install the keys
install -d -m 755 "%{buildroot}%{_sysconfdir}/pki/rpm-gpg"
install -m 644 %{_sourcedir}/RPM-GPG-KEY* "%{buildroot}%{_sysconfdir}/pki/rpm-gpg/"

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-azurelinux-4.0-primary, and archmap
#     says "azurelinux-4.0-primary: x86_64 aarch64",
#     RPM-GPG-KEY-azurelinux-4.0-{x86_64,aarch64} will be symlinked to that key.
pushd "%{buildroot}%{_sysconfdir}/pki/rpm-gpg/"
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
install -d -m 755 "%{buildroot}%{_sysconfdir}/yum.repos.d"
install -m 644 %{SOURCE2} "%{buildroot}%{_sysconfdir}/yum.repos.d/azurelinux.repo"
install -m 644 %{SOURCE3} "%{buildroot}%{_sysconfdir}/yum.repos.d/azurelinux-preview.repo"
install -m 644 %{SOURCE4} "%{buildroot}%{_sysconfdir}/yum.repos.d/cloud-native.repo"
install -m 644 %{SOURCE5} "%{buildroot}%{_sysconfdir}/yum.repos.d/cloud-native-preview.repo"
install -m 644 %{SOURCE6} "%{buildroot}%{_sysconfdir}/yum.repos.d/microsoft.repo"
install -m 644 %{SOURCE7} "%{buildroot}%{_sysconfdir}/yum.repos.d/microsoft-preview.repo"

%check
# Check arch keys exists on supported architectures, and RPM considers
# them valid
TMPRING=$(mktemp)
DBPATH=$(mktemp -d)
echo -n > "$TMPRING"
for ARCH in $(sed -ne "s/^azurelinux-%{version}-primary://p" %{SOURCE1}); do
    gpg --no-default-keyring --keyring="$TMPRING" \
        --import "%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-%{version}-$ARCH"
    rpm --dbpath "$DBPATH" --import \
        "%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-%{version}-$ARCH" --test
done
# Ensure some arch key was imported
gpg --no-default-keyring --keyring="$TMPRING" --list-keys | grep -A 2 '^pub\s' 
rm -f "$TMPRING"

%files
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/yum.repos.d/azurelinux.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/azurelinux-preview.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/cloud-native.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/cloud-native-preview.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/microsoft.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/microsoft-preview.repo

%files -n azurelinux-gpg-keys
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-*


%changelog
%autochangelog
